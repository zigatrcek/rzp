from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
import torchaudio
import torch.nn as nn
from scripts.portable_m2d import PortableM2D
from pathlib import Path
import io

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
model = None
classifier = None
device = None
idx_to_genre = {0: 'ambient', 1: 'dnb', 2: 'house', 3: 'techno', 4: 'trance'}  # Update this

@app.on_event("startup")
async def load_model():
    global model, classifier, device
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Load M2D model
    model = PortableM2D(
        weight_file='models/m2d_vit_base-80x1001p16x16-221006-mr7_as_46ab246d/weights_ep69it3124-0.47929.pth',
        num_classes=None
    )
    model = model.to(device)
    model.eval()
    print("Base M2D model loaded")
    
    # Load classifier
    checkpoint = torch.load('models/best_genre_classifier.pth')
    num_classes = len(idx_to_genre)
    classifier = nn.Linear(3840, num_classes).to(device)
    classifier.load_state_dict(checkpoint['model_state_dict'])
    classifier.eval()
    print("Genre classifier loaded")

@app.post("/predict")
async def predict_genre(file: UploadFile = File(...)):
    # Read file content
    content = await file.read()
    audio_bytes = io.BytesIO(content)
    
    # Load audio
    waveform, sr = torchaudio.load(audio_bytes)
    
    # Resample if necessary
    if sr != model.cfg.sample_rate:
        resampler = torchaudio.transforms.Resample(sr, model.cfg.sample_rate)
        waveform = resampler(waveform)
    
    # Convert to mono if stereo
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    
    # Move to device
    waveform = waveform.to(device)
    
    # Get predictions
    with torch.no_grad():
        embeddings = model(waveform.unsqueeze(0))
        embeddings = embeddings.mean(dim=1)
        outputs = classifier(embeddings)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        pred = outputs.argmax(dim=1)
    
    # Get genre name and probability
    genre = idx_to_genre[pred.item()]
    confidence = probs[0, pred].item()
    
    # Get all probabilities
    all_probs = {idx_to_genre[i]: probs[0, i].item() for i in range(len(idx_to_genre))}
    
    return {
        "predicted_genre": genre,
        "confidence": confidence,
        "all_probabilities": all_probs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
