from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from preprocessing import audio_to_spectrogram, spectrogram_to_audio
from genre_transfer_model import Generator
import torch

app = FastAPI()
generator = torch.load("generator_model.pth")  # Load your pre-trained model

@app.post("/upload/")
async def upload_song(file: UploadFile = File(...)):
    # Save the uploaded file
    with open(f"temp/{file.filename}", "wb") as f:
        f.write(file.file.read())
    
    # Preprocess and generate
    spectrogram = audio_to_spectrogram(f"temp/{file.filename}")
    transformed_spectrogram = generator(spectrogram)
    output_path = f"transformed_{file.filename}"
    spectrogram_to_audio(transformed_spectrogram, output_path)
    
    return FileResponse(output_path)

@app.get("/")
def read_root():
    return {"message": "Welcome to Music Genre Transfer API"}
