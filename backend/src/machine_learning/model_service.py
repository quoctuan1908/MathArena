# from . import model, tokenizer, DEVICE,get_ast_token_alignment,config,ast_to_gnn_input_positional
# import torch

# def generate_output(input_text: str) -> str:
#     """
#     Hàm gọi model để generate output dựa trên input_text.
#     Sử dụng model và tokenizer đã khởi tạo trong __init__.
#     """
#     try:
#         graph_data, node_data_raw = ast_to_gnn_input_positional(input_text)
#         if graph_data is None or graph_data.num_nodes == 0:
#             print("Invalid AST/Graph, skipping.")
#     except Exception as e:
#         print(f"Graph error: {e}")
#     # Tokenize input
#     inputs = tokenizer(
#         input_text,
#         max_length=config.MAX_INPUT_LENGTH,
#         padding='max_length',
#         truncation=True,
#         return_tensors='pt'
#     ).to(DEVICE)

#     input_ids = inputs['input_ids'].to(DEVICE) 
#     attention_mask = inputs['attention_mask'].to(DEVICE)
#     try:
#         alignment_map = get_ast_token_alignment(
#             input_text, tokenizer, input_ids[0].cpu().tolist(), node_data_raw
#         )
#         if not isinstance(alignment_map, torch.Tensor):
#             alignment_map = torch.tensor(alignment_map, dtype=torch.long)
#         alignment_map = alignment_map.unsqueeze(0).to(DEVICE)
#     except Exception as e:
#         print(f"Alignment error: {e}")
    
#     try:
#         print("Hello 1")
#         with torch.no_grad():
#             outputs = model.generate(
#                 # Truyền vào input_ids GỐC (không bị mask)
#                 input_ids=input_ids, 
#                 attention_mask=attention_mask,
#                 graphs=graph_data,
#                 token_to_node_map=alignment_map,
#                 max_length=config.MAX_TARGET_LENGTH,
#                 num_beams=config.NUM_BEAMS,
#                 early_stopping=True,
#                 no_repeat_ngram_size=3,
#                 do_sample=True
#             )
#         print("HEllo 2")
#         question = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         print(f"Generated: {question}")
#     except Exception as e:
#         print(f"Generate error: {e}")
    
#     return question