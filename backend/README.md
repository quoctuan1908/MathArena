# Thực thi backend

## Yêu cầu hệ thống

- Python 3.8+

---

## Cách chạy backend FastAPI

### 1. Vào thư mục backend

```bash
cd backend
```

### 2. (Khuyến nghị) Tạo virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Trên Linux/macOS
# .\venv\Scripts\activate  # Trên Windows

```

### 3. Cài đặt thư viện phụ thuộc

```bash
pip install -r requirements.txt
```
## Chạy tiếp để cài sử dụng CUDA
```bash
pip install torch==2.7.1+cu118 torchvision==0.18.1+cu118 torchaudio==2.8.0+cu118 --index-url https://download.pytorch.org/whl/cu118
```
### 4. Chạy ứng dụng FastAPI
```bash
uvicorn src.main:app --reload
```


