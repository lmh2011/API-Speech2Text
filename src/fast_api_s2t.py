from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import whisper
import os
import torch
import io
import re
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Thay đổi theo nguồn gốc của bạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whisper_model_name = "base"
device  = torch.device("cuda" if torch.cuda.is_available() else "cpu")
whisper_model = whisper.load_model(whisper_model_name, device = device)

def convert_to_wav(audio_data: bytes, output_file: str):
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_data))
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio.export(output_file, format="wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể chuyển file sang định dạng WAV: {str(e)}")
@app.post("/speech-to-text/")
async def speech_to_text(request: Request):
    """
    API nhận file âm thanh qua body của request và trả về văn bản được chuyển đổi từ giọng nói.
    """
    try:
        body = await request.body()
        
        if not body:
            raise HTTPException(status_code=400, detail="Dữ liệu âm thanh không được gửi trong request.")

        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            convert_to_wav(body, temp_file.name)  # Chuyển đổi sang WAV
            temp_file_path = temp_file.name

        result = whisper_model.transcribe(temp_file_path,
                                        language='vi',
                                        word_timestamps = True,
                                        temperature = [0.2, 0.4, 0.6, 0.8],
                                        logprob_threshold = -0.4)
        segments = []
        """" segments = [{"startTime": 0, "endTime": 5, "content": lê mạnh hà}, {}]"""
        full_content = result['text']
        segments_raw = result['segments'] # phân đoạn câu => cụm và khoảng thời gian 
        for segment_chunk in segments_raw:
            chunk = {}
            chunk["startTime"] = "{0:.2f}".format(segment_chunk["start"])
            chunk["endTime"] = "{0:.2f}".format(segment_chunk["end"])
            chunk["content"]= re.sub(r"[\"']", '', segment_chunk["text"])
            segments.append(chunk)
        return JSONResponse(content={"full_content": full_content, "segments": segments}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Đã xảy ra lỗi trong quá trình xử lý: {str(e)}")

    finally:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/")
def health_check():
    """
    Endpoint kiểm tra API có hoạt động không.
    """
    return {"message": "Whisper API is running!"}
