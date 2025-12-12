# import os
# import torch
# import torch.nn as nn
# import numpy as np
# import pandas as pd
# import re
# import logging
# from io import StringIO
# from omegaconf import OmegaConf
# from transformers import BartForConditionalGeneration, AutoTokenizer, AutoConfig
# from torch_geometric.data import Data, Batch
# from torch_geometric.nn import RGCNConv
# import unicodedata
# import torch.nn.functional as F
# # ==========================
# # 📁 ĐỊNH NGHĨA ĐƯỜNG DẪN
# # ==========================
# PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))  # .../backend/offload/src
# MODEL_BASE = "vinai/bartpho-syllable"

# MODEL_DIR = os.path.join(PACKAGE_DIR, "BARTpho_SAT")
# MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pt")
# TOKENIZER_PATH = os.path.join(MODEL_DIR, "best_tokenizer")

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"📦 Model dir: {MODEL_DIR}")

# # ==========================
# # ⚙️ CONFIG YAML
# # ==========================
# config_yaml = """
# BART_MODEL_NAME: 'vinai/bartpho-syllable-base'
# HIDDEN_SIZE: 768
# MAX_INPUT_LENGTH: 200
# MAX_TARGET_LENGTH: 100
# BATCH_SIZE: 32
# BART_LEARNING_RATE: 1e-5
# GNN_LEARNING_RATE: 5e-5
# NUM_EPOCHS: 15
# VAL_SPLIT_SIZE: 0.1
# SAVE_PATH: "./math_qg_bartpho_sat"
# NUM_SAT_LAYERS: 6
# NUM_HEADS_SAT: 8
# OPERATOR_VOCAB:
#   add: 0
#   multiply: 1
#   subtract: 2
#   divide: 3
#   min: 4
#   max: 5
#   lcm: 6
#   floor: 7
#   sqrt: 8
#   negate: 9
# CONSTANT_ID: 10
# TOTAL_VOCAB_SIZE: 11
# D_CAT: 64
# D_NUM: 64
# D_POS: 16
# D_STRUCT: 16
# D_SIGN: 16
# NUM_RELATIONS: 3
# RELATION_OP_TO_OP: 0
# RELATION_OP_TO_CONST: 1
# RELATION_CHILD_TO_PARENT: 2
# SEED: 42
# FREEZE_EPOCHS: 2
# WARMUP_RATIO: 0.05
# WEIGHT_DECAY: 0.01
# MAX_GRAD_NORM: 1.0
# NUM_BEAMS: 4
# NUM_WORKERS: 2
# VAL_SAMPLE_SIZE: 500
# MIXED_PRECISION: 'fp16'
# AUGMENT_SIZE: 10000
# MAX_POSITIONS: 10
# """
# config = OmegaConf.load(StringIO(config_yaml))
# config.D_IN_AST = config.D_CAT + config.D_NUM + config.D_POS + config.D_STRUCT + config.D_SIGN

# def get_const_value(const_str: str) -> str:
#     if not const_str.startswith('const_'):
#         return None
#     val_str = const_str[6:].replace('_', '.')
#     try:
#         # Chúng ta chỉ quan tâm đến số nguyên cho các mẫu câu đơn giản
#         # Bỏ qua các số thập phân (ví dụ 2.5)
#         if '.' in val_str:
#             return None # Bỏ qua
#         int(val_str) # Kiểm tra xem có phải là số
#         return val_str # Trả về chuỗi
#     except ValueError:
#         return None
# def normalize_tone(text: str) -> str:
#     return unicodedata.normalize('NFC', text)
  
# OPERATOR_ARITY = {
#     'add': None, 'multiply': None, 'subtract': None, 'divide': None,
#     'min': None, 'max': None, 'lcm': None, 'floor': 1, 'sqrt': 1, 'negate': 1
# }
# MIN_ARITY = {
#     'add': 2, 'multiply': 2, 'subtract': 1, 'divide': 1,
#     'min': 2, 'max': 2, 'lcm': 2
# }

# # ========== ⭐ NEW: PARSE FRACTION/PERCENT ==========
# def parse_const_value(val_str: str) -> float | None:
#     """Parse '2_over_3' → 2/3, '50_percent' → 0.5, '25' → 25.0"""
#     val_str_lower = val_str.lower()
    
#     # 1. FRACTION: X_over_Y / X.over.Y
#     frac_match = re.match(r'([0-9]+(?:\.[0-9]+)?)[_\.]?over[_\.]?([0-9]+(?:\.[0-9]+)?)', val_str_lower)
#     if frac_match:
#         num, den = map(float, frac_match.groups())
#         return num / den if den != 0 else None
    
#     # 2. PERCENT
#     percent_match = re.search(r'([0-9]+(?:\.[0-9]+)?)\.?\s*percent', val_str_lower)
#     if percent_match:
#         return float(percent_match.group(1)) / 100
    
#     # 3. PURE NUMERIC (_ → .)
#     cleaned = re.sub(r"[^0-9.]", "", val_str.replace('_', '.'))
#     try:
#         if cleaned.endswith('.'): cleaned = cleaned[:-1]
#         return float(cleaned)
#     except ValueError:
#         return None

# # ========== UPDATED is_constant_node ==========
# def is_constant_node(ast_str: str) -> bool:
#     """const_*, số thuần, fraction, percent"""
#     if ast_str.startswith('const_'):
#         return parse_const_value(ast_str[6:]) is not None
#     try:
#         float(ast_str)
#         return True
#     except ValueError:
#         return False

# # ========== split_nested_args (giữ clamp tốt) ==========
# def split_nested_args(args_string: str) -> list:
#     args, current, level = [], "", 0
#     for char in args_string:
#         if char == ',' and level == 0:
#             args.append(current.strip())
#             current = ""
#         else:
#             current += char
#             if char == '(': level += 1
#             elif char == ')': level = max(level - 1, 0)
#     if current.strip():
#         args.append(current.strip())
#     return args

# # ========== clean_ast (REJECT malformed PERFECT) ==========
# def clean_ast(ast_str: str) -> str | None:
#     if not ast_str: return None
#     # Trim EXCESS )
#     num_open = ast_str.count('(')
#     num_close = ast_str.count(')')
#     excess_close = num_close - num_open
#     if excess_close > 0:
#         ast_str = ast_str[:-excess_close]
#     # Strict STACK (reject ANY invalid)
#     stack = 0
#     for c in ast_str:
#         if c == '(': stack += 1
#         elif c == ')':
#             stack -= 1
#             if stack < 0: return None
#     if stack != 0:  # MISSING ) → REJECT!
#         return None
#     return ast_str

# # ========== ⭐ FIXED parse_ast (NEW CONST PARSER) ==========
# def parse_ast(ast_str: str, node_data, edge_list, node_count, parent_id=-1, pos=0, depth=0):
#     node_id = node_count
#     if not ast_str or ast_str.strip() == "": return -1, node_count, False

#     # ⭐ EARLY CLEAN & REJECT
#     ast_str = clean_ast(ast_str)
#     if not ast_str: return -1, node_count, False

#     # Auto-add const_ for raw numbers
#     try:
#         float(ast_str)
#         ast_str = f'const_{ast_str}'
#     except ValueError:
#         pass

#     # ========== I. CONSTANT (NEW PARSER!) ==========
#     if is_constant_node(ast_str):
#         val_str_part = ast_str[6:]
#         val = parse_const_value(val_str_part)
#         if val is None:
#             logging.warning(f"Invalid constant value: {ast_str}")
#             return -1, node_count, False
        
#         sign = 0 if val > 0 else (1 if val < 0 else 2)
#         node_data.append({
#             'id': node_id, 'type_id': config.CONSTANT_ID, 'value': val,
#             'pos_id': pos, 'depth': depth, 'degree': 0, 'sign': sign
#         })
#         return node_id, node_count + 1, True

#     # ========== II. OPERATOR ==========
#     match = re.match(r'(\w+)\((.*)\)', ast_str)
#     if not match:
#         return -1, node_count, False
#     op_name, args_str = match.groups()
#     if op_name not in config.OPERATOR_VOCAB:
#         return -1, node_count, False
#     op_id = config.OPERATOR_VOCAB[op_name]

#     # ARITY CHECK (giữ tốt)
#     args = split_nested_args(args_str)
#     actual_arity = len([a for a in args if a.strip()])
#     if actual_arity == 0:
#         return -1, node_count, False

#     expected = OPERATOR_ARITY.get(op_name)
#     min_a = MIN_ARITY.get(op_name, 1)
#     if expected is not None:
#         if actual_arity != expected:
#             return -1, node_count, False
#     elif actual_arity < min_a:
#         return -1, node_count, False

#     # Create node
#     node_data.append({
#         'id': node_id, 'type_id': op_id, 'value': 0.0, 'pos_id': pos,
#         'depth': depth, 'degree': 0, 'sign': 2
#     })
#     node_count += 1
#     current_node_count = node_count
#     children_count = 0

#     # Recurse children
#     for i, arg in enumerate(args):
#         child_ast = clean_ast(arg.strip())  # CLEAN EACH!
#         if not child_ast:
#             return -1, node_count, False
#         child_id, current_node_count, child_is_const = parse_ast(
#             child_ast, node_data, edge_list, current_node_count, node_id, i+1, depth + 1
#         )
#         if child_id == -1: return -1, node_count, False
#         edge_type = config.RELATION_OP_TO_CONST if child_is_const else config.RELATION_OP_TO_OP
#         edge_list.append([node_id, child_id, edge_type])
#         edge_list.append([child_id, node_id, config.RELATION_CHILD_TO_PARENT])
#         children_count += 1

#     node_data[node_id]['degree'] = children_count
#     return node_id, current_node_count, False

# # ========== ast_to_gnn_input_positional (giữ tốt) + node_data return ==========
# def ast_to_gnn_input_positional(ast_str: str) -> tuple[Data | None, list | None]:
#     ast_str = clean_ast(ast_str)
#     if not ast_str: return None, None

#     node_data, edge_list = [], []
#     try:
#         root_id, _, _ = parse_ast(ast_str, node_data, edge_list, 0)
#         if root_id == -1 or not node_data: return None, None
#     except Exception as e:
#         logging.error(f"Parse FAILED: {ast_str} | {e}")
#         return None, None

#     # Features/Edges/Data (giữ nguyên EXACT)
#     N = len(node_data)
#     node_types = torch.tensor([n['type_id'] for n in node_data], dtype=torch.long)
#     values = torch.tensor([n['value'] for n in node_data], dtype=torch.float)
#     positions = torch.tensor([n['pos_id'] for n in node_data], dtype=torch.long)
#     depths = torch.tensor([n['depth'] for n in node_data], dtype=torch.float)
#     degrees = torch.tensor([n.get('degree', 0) for n in node_data], dtype=torch.float)
#     structs = torch.stack([depths, degrees], dim=1)
#     signs = torch.tensor([n['sign'] for n in node_data], dtype=torch.long)

#     sources = [e[0] for e in edge_list]
#     targets = [e[1] for e in edge_list]
#     edge_index = torch.tensor([sources, targets], dtype=torch.long)
#     edge_type = torch.tensor([e[2] for e in edge_list], dtype=torch.long)

#     if edge_index.max() >= N or edge_index.min() < 0: return None, None

#     node_types_f = node_types.float().unsqueeze(1)
#     values_f = values.unsqueeze(1)
#     positions_f = positions.float().unsqueeze(1)
#     signs_f = signs.float().unsqueeze(1)
#     x = torch.cat([node_types_f, values_f, positions_f, structs, signs_f], dim=1)

#     return Data(x=x, edge_index=edge_index, edge_type=edge_type), node_data

# # ========== Alignment (CẢI THIỆN: Sort const by pos/depth) ==========
# def get_ast_token_alignment(ast_str: str, tokenizer, input_ids: list, node_data: list, debug_print=False):
#     if not node_data: return torch.full((len(input_ids),), -1, dtype=torch.long)
    
#     alignment_map = torch.full((len(input_ids),), -1, dtype=torch.long)
#     decoded_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    
#     # ⭐ FIX: Sort CONST by pos_id (left-to-right order!)
#     const_nodes = sorted(
#         [n for n in node_data if n['type_id'] == config.CONSTANT_ID],
#         key=lambda n: (n['pos_id'], n['depth'])
#     )
#     unmapped_const_ids = [n['id'] for n in const_nodes]
    
#     node_to_type = {n['id']: next((k for k,v in config.OPERATOR_VOCAB.items() if v==n['type_id']), 'UNKNOWN')
#                     for n in node_data if n['type_id'] != config.CONSTANT_ID}
    
#     mapped = set()
#     in_const = False
#     current_const_id = -1
#     op_buffer = ""
    
#     for i, token in enumerate(decoded_tokens):
#         if token in ['<s>', '</s>', '<pad>']: continue
        
#         clean_token = re.sub(r'^ |\([,\)]', '', token).lower().strip('()[],')
        
#         if in_const:
#             if re.match(r'^[0-9_.%]+$', clean_token):
#                 alignment_map[i] = current_const_id
#                 continue
#             in_const = False
        
#         if not in_const:
#             # CONST: 'const_' or NUMBER
#             if 'const_' in token.lower() or re.match(r'^[0-9_.%]+$', clean_token):
#                 if unmapped_const_ids:
#                     current_const_id = unmapped_const_ids.pop(0)
#                     alignment_map[i] = current_const_id
#                     mapped.add(current_const_id)
#                     in_const = True
#                     continue
            
#             # OP: buffer match
#             if re.match(r'^[a-z_]+$', clean_token):
#                 op_buffer += clean_token
#                 for node_id, op_name in node_to_type.items():
#                     if node_id not in mapped and op_name == op_buffer:
#                         alignment_map[i] = node_id
#                         mapped.add(node_id)
#                         op_buffer = ""
#                         break
#                 continue
#             else:
#                 op_buffer = ""
    
#     # Pad
#     if len(alignment_map) < config.MAX_INPUT_LENGTH:
#         alignment_map = F.pad(alignment_map, (0, config.MAX_INPUT_LENGTH - len(alignment_map)), value=-1)
#     return alignment_map[:config.MAX_INPUT_LENGTH]
    

# # ==========================
# # 🧩 ĐỊNH NGHĨA MÔ HÌNH PHỤ TRỢ
# # ==========================
# class MultiFeatureFusion(nn.Module):
#     def __init__(self, total_vocab_size, d_cat, d_num, d_pos, d_struct, d_sign, d_model):
#         super().__init__()
#         self.cat_embed = nn.Embedding(total_vocab_size, d_cat)
        
#         self.num_mlp = nn.Sequential(
#             nn.Linear(1, d_num * 2),
#             nn.GELU(),
#             nn.Linear(d_num * 2, d_num)
#         )
        
#         # --- (SỬA LỖI VỊ TRÍ) Dùng Embedding cho Vị trí ---
#         self.pos_embed = nn.Embedding(config.MAX_POSITIONS, d_pos) 
        
#         self.struct_linear = nn.Linear(2, d_struct)
#         self.sign_embed = nn.Embedding(3, d_sign)
        
#         combined_dim = d_cat + d_pos + d_struct + d_sign + d_num
#         self.final_proj = nn.Linear(combined_dim, d_model)
#         self.final_norm = nn.LayerNorm(d_model)

#     def forward(self, node_features, return_intermediate_ev=False):
#         types = node_features[:, 0].long()
#         values_raw = node_features[:, 1].unsqueeze(-1)
        
#         # pos là long (index)
#         pos = node_features[:, 2].long() 
        
#         structs = node_features[:, 3:5]
#         signs = node_features[:, 5].long()

#         e_cat = self.cat_embed(types)
#         e_pos = self.pos_embed(pos) # Dùng pos_embed
#         e_struct = self.struct_linear(structs)
#         e_sign = self.sign_embed(signs)
        
#         values_scaled = torch.log1p(torch.abs(values_raw))
        
#         # e_v là tín hiệu "giá trị" (value) chưa bị pha loãng
#         e_v = self.num_mlp(values_scaled) # Shape [N, d_num]

#         const_mask_for_concat = (types == config.CONSTANT_ID).unsqueeze(-1).float()
#         e_v_masked_for_concat = e_v * const_mask_for_concat
        
#         combined_features = torch.cat([e_cat, e_pos, e_struct, e_sign, e_v_masked_for_concat], dim=-1)

#         # final_embedding là tín hiệu "tổng hợp" ban đầu cho GNN
#         final_embedding = self.final_proj(combined_features)
#         final_embedding = self.final_norm(final_embedding)

#         # --- (SỬA ĐỔI) ---
#         # Trả về e_v (tín hiệu giá trị) riêng biệt nếu được yêu cầu
#         intermediate_ev_to_return = e_v if return_intermediate_ev else None
#         # --- (KẾT THÚC SỬA ĐỔI) ---

#         if return_intermediate_ev:
#             return final_embedding, intermediate_ev_to_return
#         else:
#             return final_embedding


# class StructuralUpdaterRGCN(nn.Module):
#     def __init__(self, out_channels, num_relations):
#         super().__init__()
#         self.feature_fuser = MultiFeatureFusion(
#             config.TOTAL_VOCAB_SIZE, config.D_CAT, config.D_NUM,
#             config.D_POS, config.D_STRUCT, config.D_SIGN, out_channels
#         )
        
#         num_bases = config.get('RGCN_NUM_BASES', 10)
        
#         # GNN 3 Lớp (Giữ nguyên)
#         self.conv1 = RGCNConv(out_channels, out_channels, num_relations, num_bases=num_bases)
#         self.norm1 = nn.LayerNorm(out_channels)
#         self.conv2 = RGCNConv(out_channels, out_channels, num_relations, num_bases=num_bases)
#         self.norm2 = nn.LayerNorm(out_channels)
#         self.conv3 = RGCNConv(out_channels, out_channels, num_relations, num_bases=num_bases)
#         self.norm3 = nn.LayerNorm(out_channels)
#         self.activation = nn.GELU()

#     def forward(self, graph_data, return_intermediate_ev=False):
#         # --- (SỬA ĐỔI) ---
#         # Gọi fuser với cờ return_intermediate_ev
#         fused_features_or_tuple = self.feature_fuser(
#             graph_data.x, return_intermediate_ev=return_intermediate_ev
#         )
        
#         if return_intermediate_ev:
#             # x là tín hiệu tổng hợp (để vào GNN)
#             # e_v_intermediate là tín hiệu giá trị (để bypass)
#             x, e_v_intermediate = fused_features_or_tuple 
#         else:
#             x = fused_features_or_tuple
#             e_v_intermediate = None
#         # --- (KẾT THÚC SỬA ĐỔI) ---

#         edge_index = graph_data.edge_index
#         edge_type = graph_data.edge_type

#         # GNN 3 Lớp (Giữ nguyên)
#         identity = x
#         x = self.conv1(x, edge_index, edge_type)
#         x = self.norm1(x)
#         x = self.activation(x)
#         x = x + identity
        
#         identity = x
#         x = self.conv2(x, edge_index, edge_type)
#         x = self.norm2(x)
#         x = self.activation(x)
#         x = x + identity
        
#         identity = x
#         x = self.conv3(x, edge_index, edge_type)
#         x = self.norm3(x)
#         x = x + identity
        
#         # x bây giờ là tín hiệu CẤU TRÚC (đã bị pha loãng)
        
#         if return_intermediate_ev:
#             # Trả về cả tín hiệu cấu trúc VÀ tín hiệu giá trị
#             return x, e_v_intermediate
#         else:
#             return x


# class ASTTokenAlignment(nn.Module):
#     def __init__(self, d_model):
#         super().__init__()
#         self.d_model = d_model
#         self.register_buffer('null_ast_embed', torch.zeros(1, d_model))

#     def forward(self, structural_node_features, token_to_node_map):
#         if isinstance(structural_node_features, Batch):
#             node_features = structural_node_features.x
#             ptr = structural_node_features.ptr.to(node_features.device)
#         else:
#             # ✅ FIXED: Strict check
#             batch_size = token_to_node_map.shape[0]
#             if batch_size > 1:
#                 raise ValueError(f"ASTTokenAlignment: Use Batch for batch_size={batch_size}>1. Got tensor!")
#             node_features = structural_node_features  # Single graph OK
#             ptr = torch.tensor([0, node_features.size(0)], device=node_features.device)
    
#         batch_size, seq_len = token_to_node_map.shape
#         safe_node_features = torch.cat([node_features, self.null_ast_embed.to(node_features.device)], dim=0)
#         null_index = node_features.size(0)
    
#         ptr_expanded = ptr[:-1].unsqueeze(1).expand(-1, seq_len)
#         global_node_map = token_to_node_map.clone()
#         aligned_mask = (token_to_node_map != -1)
    
#         global_node_map[aligned_mask] = global_node_map[aligned_mask] + ptr_expanded[aligned_mask]
#         global_node_map[~aligned_mask] = null_index
    
#         global_node_map = torch.clamp(global_node_map, 0, null_index)
#         H_align = safe_node_features[global_node_map]
#         return H_align


# # ==========================
# # 🧠 MÔ HÌNH CHÍNH
# # ==========================
# hf_token = os.getenv("HF_TOKEN")

# class BARTpho_SAT(nn.Module):
#     def __init__(self, tokenizer):
#         super().__init__()
#         self.bartpho = BartForConditionalGeneration.from_pretrained(config.BART_MODEL_NAME)
#         self.tokenizer_config = self.bartpho.config
        
#         d_model = config.HIDDEN_SIZE
        
#         self.token_embeddings = self.bartpho.get_input_embeddings()
#         self.position_embeddings = self.bartpho.model.encoder.embed_positions
        
#         self.structural_updater = StructuralUpdaterRGCN(
#             out_channels=d_model,
#             num_relations=config.NUM_RELATIONS
#         )
#         self.alignment_layer = ASTTokenAlignment(d_model)

#         # Các lớp Norm (Giữ nguyên)
#         self.text_embed_norm = nn.LayerNorm(d_model)
#         self.gnn_pre_fusion_norm = nn.LayerNorm(d_model) # Dùng cho tín hiệu Cấu trúc
#         self.post_fusion_norm = nn.LayerNorm(d_model)

#         # --- (SỬA ĐỔI) Thêm "Đầu chiếu Giá trị" (Value Projection Head) ---
#         # d_num (từ config) là chiều của e_v (ví dụ: 128)
#         self.value_projection_head = nn.Linear(config.D_NUM, d_model)
#         self.value_norm = nn.LayerNorm(d_model) # Thêm norm cho tín hiệu giá trị

#         self.structure_scale = nn.Parameter(torch.tensor(14.0))
#         self.value_scale = nn.Parameter(torch.tensor(14.0))
#         # --- (KẾT THÚC SỬA ĐỔI) ---

#     def resize_token_embeddings(self, new_num_tokens: int):
#         self.bartpho.resize_token_embeddings(new_num_tokens)
#         self.token_embeddings = self.bartpho.get_input_embeddings()
#         logging.info(f" Model embeddings resized to: {self.token_embeddings.num_embeddings}")

#     def forward(self, input_ids, attention_mask, graphs, token_to_node_map, labels=None):
#         device = input_ids.device
        
#         # 1. GNN Pipeline (SỬA ĐỔI)
#         if not isinstance(graphs, Batch): graphs = Batch.from_data_list(graphs)
#         graphs = graphs.to(device)
#         token_to_node_map = token_to_node_map.to(device)
        
#         structural_node_features, e_v_intermediate = self.structural_updater(
#             graphs, return_intermediate_ev=True
#         )
#         # structural_node_features: [N_total, d_model] (Tín hiệu cấu trúc)
#         # e_v_intermediate: [N_total, d_num] (Tín hiệu giá trị, ví dụ: 64)

#         # --- (SỬA LỖI RUNTIME ERROR) ---
        
#         # Luồng 1: Tín hiệu Cấu trúc (Structure) - (Giữ nguyên)
#         graph_batch_structure = Batch(x=structural_node_features, batch=graphs.batch, ptr=graphs.ptr)
#         H_align_structure = self.alignment_layer(graph_batch_structure, token_to_node_map)

#         # Luồng 2: Tín hiệu Giá trị (Value Bypass)
        
#         # Bước 2a: Chiếu (project) Tín hiệu Giá trị LÊN d_model TRƯỚC
#         projected_value = self.value_projection_head(e_v_intermediate) # [N_total, d_model]
#         projected_value_norm = self.value_norm(projected_value)
        
#         # Bước 2b: TẠO BATCH TỪ TÍN HIỆU ĐÃ CHIẾU
#         graph_batch_value = Batch(x=projected_value_norm, batch=graphs.batch, ptr=graphs.ptr)
        
#         # Bước 2c: Alignment (Bây giờ đã an toàn, 768 vs 768)
#         H_align_value = self.alignment_layer(graph_batch_value, token_to_node_map)
#         # --- (KẾT THÚC SỬA LỖI) ---

#         # 2. Text Embeddings (Giữ nguyên)
#         try:
#             inputs_embeds = self.token_embeddings(input_ids)
#         except IndexError as e:
#             logging.error(f"Lỗi IndexError: {e}", exc_info=True); raise e
        
#         padding_idx = self.bartpho.config.pad_token_id
#         position_ids = torch.arange(input_ids.shape[1], dtype=torch.long, device=device).unsqueeze(0).expand_as(input_ids)
#         position_ids = position_ids * attention_mask.long() + padding_idx * (1 - attention_mask.long())
#         position_embeds = self.position_embeddings(position_ids)
#         text_embeds = inputs_embeds + position_embeds 

#         text_embeds_norm = self.text_embed_norm(text_embeds)
#         H_align_structure_norm = self.gnn_pre_fusion_norm(H_align_structure)
#         H_align_value_norm = self.value_norm(H_align_value)
#         aligned_mask_expanded = (token_to_node_map != -1).unsqueeze(-1).float().to(text_embeds_norm.dtype)
        
#         # Nhân với hệ số scale
#         x_fused_struct = H_align_structure_norm * aligned_mask_expanded * self.structure_scale
#         x_fused_value = H_align_value_norm * aligned_mask_expanded * self.value_scale
        
#         # Thay thế và Cộng
#         x_fused = (text_embeds_norm * (1.0 - aligned_mask_expanded)) + x_fused_struct
#         x_fused = x_fused + x_fused_value
        
#         x_fused = self.post_fusion_norm(x_fused)

#         # (Log giữ nguyên)
#         try:
#             with torch.no_grad():
#                 idx_log = 0
#                 norm_text = torch.linalg.vector_norm(text_embeds_norm[idx_log], dim=-1).mean().item()
#                 norm_struct = torch.linalg.vector_norm(H_align_structure_norm[idx_log], dim=-1).mean().item()
#                 norm_value = torch.linalg.vector_norm(H_align_value[idx_log], dim=-1).mean().item()
#                 norm_fused = torch.linalg.vector_norm(x_fused[idx_log], dim=-1).mean().item()
#         except Exception as log_e:
#             logging.warning(f" Lỗi khi logging embed norms: {log_e}")

#         # 4. Encoder
#         try:
#             encoder_outputs = self.bartpho.model.encoder(
#                 inputs_embeds=x_fused, attention_mask=attention_mask, return_dict=True
#             )
#         except Exception as e: logging.error(f"Lỗi BART Encoder: {e}", exc_info=True); raise e
        
#         # 5. Decoder/Loss
#         if labels is not None:
#             try:
#                 decoder_outputs = self.bartpho(
#                     encoder_outputs=encoder_outputs, attention_mask=attention_mask,
#                     labels=labels, return_dict=True
#                 )
#                 return decoder_outputs.loss
#             except Exception as e: logging.error(f"Lỗi BART Decoder/Loss: {e}", exc_info=True); raise e
#         else:
#             return encoder_outputs

#     def generate(self, input_ids, attention_mask, graphs, token_to_node_map, **kwargs):
#         device = input_ids.device
#         print("Hello 3")
#         # 1. GNN Pipeline (Giữ nguyên)
#         if isinstance(graphs, Data):
#             graphs = Batch.from_data_list([graphs])
#         graphs = graphs.to(device)
#         token_to_node_map = token_to_node_map.to(device)
        
#         structural_node_features, e_v_intermediate = self.structural_updater(
#             graphs, return_intermediate_ev=True
#         )
#         print("Hello 4")
#         # 2. Tạo 2 luồng Alignment (Giữ nguyên, đã sửa lỗi RuntimeError)
#         # Luồng 1: Cấu trúc
#         graph_batch_structure = Batch(x=structural_node_features, batch=graphs.batch, ptr=graphs.ptr)
#         H_align_structure = self.alignment_layer(graph_batch_structure, token_to_node_map)

#         # Luồng 2: Giá trị (Chiếu TRƯỚC, Align SAU)
#         projected_value = self.value_projection_head(e_v_intermediate)
#         projected_value_norm = self.value_norm(projected_value)
#         graph_batch_value = Batch(x=projected_value_norm, batch=graphs.batch, ptr=graphs.ptr)
#         H_align_value = self.alignment_layer(graph_batch_value, token_to_node_map)
#         print("Hello 5")
#         # 3. Text Embeddings (SỬA LỖI NAME ERROR)
        
#         # --- (SỬA LỖI) ---
#         # Thêm dòng bị thiếu này:
#         inputs_embeds = self.token_embeddings(input_ids)
#         # --- (KẾT THÚC SỬA) ---
        
#         padding_idx = self.bartpho.config.pad_token_id
#         position_ids = torch.arange(input_ids.shape[1], dtype=torch.long, device=device).unsqueeze(0).expand_as(input_ids)
#         position_ids = position_ids * attention_mask.long() + padding_idx * (1 - attention_mask.long())
#         position_embeds = self.position_embeddings(position_ids)
#         text_embeds = inputs_embeds + position_embeds
#         print("Hello 6")
#         text_embeds_norm = self.text_embed_norm(text_embeds)
#         H_align_structure_norm = self.gnn_pre_fusion_norm(H_align_structure)
#         H_align_value_norm = self.value_norm(H_align_value)
#         aligned_mask_expanded = (token_to_node_map != -1).unsqueeze(-1).float().to(text_embeds_norm.dtype)
        
#         # Nhân với hệ số scale
#         x_fused_struct = H_align_structure_norm * aligned_mask_expanded * self.structure_scale
#         x_fused_value = H_align_value_norm * aligned_mask_expanded * self.value_scale
        
#         # Thay thế và Cộng
#         x_fused = (text_embeds_norm * (1.0 - aligned_mask_expanded)) + x_fused_struct
#         x_fused = x_fused + x_fused_value
        
#         x_fused = self.post_fusion_norm(x_fused)

#         # 5. Encoder (Giữ nguyên)
#         encoder_outputs = self.bartpho.model.encoder(
#             inputs_embeds=x_fused,
#             attention_mask=attention_mask,
#             return_dict=True
#         )
#         print("Hello 7")
#         # 6. Generation (Giữ nguyên)
#         final_gen_kwargs = {
#             'max_length': kwargs.get('max_length', config.MAX_TARGET_LENGTH),
#             'num_beams': kwargs.get('num_beams', config.NUM_BEAMS),
#             'early_stopping': kwargs.get('early_stopping', True),
#             'no_repeat_ngram_size': kwargs.get('no_repeat_ngram_size', 3),
#             'do_sample': kwargs.get('do_sample', False),
#             **kwargs 
#         }
#         print("Hello 8")
#         outputs = self.bartpho.generate(
#             encoder_outputs=encoder_outputs, 
#             attention_mask=attention_mask, 
#             **final_gen_kwargs 
#         )
#         return outputs


# # ==========================
# # 🚀 KHỞI TẠO MODEL
# # ==========================
# tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, token=hf_token)
# model = BARTpho_SAT(tokenizer)
# model.resize_token_embeddings(len(tokenizer))

# state_dict = torch.load(MODEL_PATH, map_location="cpu")
# model.load_state_dict(state_dict)
# model.to(DEVICE)
# model.eval()

# # ==========================
# # 🔁 EXPORT
# # ==========================
# __all__ = ["model", "tokenizer", "DEVICE"]
