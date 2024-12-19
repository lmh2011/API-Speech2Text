import requests

# Địa chỉ của API nhận dạng giọng nói
url = "http://127.0.0.1:8000/speech-to-text/"

# Cấu hình tiêu đề yêu cầu
headers = {"Content-Type": "application/octet-stream"}

# Đường dẫn tới tệp âm thanh cần chuyển đổi
audio_file = "speaker_a.wav"

# Mở và đọc tệp âm thanh dưới dạng nhị phân
with open(audio_file, "rb") as f:
    audio_data = f.read()

# Gửi yêu cầu POST với dữ liệu âm thanh
response = requests.post(url, headers=headers, data=audio_data)

# In ra phản hồi từ API (dữ liệu nhận được sau khi xử lý)
print(response.json())
