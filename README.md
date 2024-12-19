# Tạo env
- B1: `python -m venv s2t_env`
- B2: Chạy lệnh sau trước khi kích hoạt môi trường: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- B3: Kích hoạt môi trường ảo: `s2t_env/Scripts/activate`
# Môi trường
- `pip install -r requirements.txt`
# Run:
- Send data (dotnet 9.0): `dotnet run`
- Request: `uvicorn fast_api_s2t:app --reload`
