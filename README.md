# Electronic Music Genre Classification

This repository contains code for electronic music genre classification using the M2D (Masked Modeling Duo) model architecture. The classifier can identify the following electronic music genres:

- Ambient
- Drum and Bass
- House
- Techno
- Trance

## Requirements

Install required dependencies:

```bash
pip install timm einops nnAudio torchaudio pandas tqdm
```

## Model Structure

The system uses a two-stage approach:

1. M2D model as feature extractor (pretrained on audio data)
2. Linear classifier head trained on electronic music genres

## Usage

### Inference

To run inference on audio files:

1. Download the M2D base model weights and trained genre classifier:
   - Place M2D weights in `m2d_vit_base-80x1001p16x16-221006-mr7_as_46ab246d/weights_ep69it3124-0.47929.pth`
   - Place genre classifier weights in `best_genre_classifier.pth`

2. Use the inference notebook:
   ```bash
   jupyter notebook scripts/inference_m2d.ipynb
   ```

The notebook provides two main functions:

- `predict_genre()`: Classify a single audio file
- `predict_directory()`: Batch classify all audio files in a directory

### Example

```python
# Single file prediction
result = predict_genre("path/to/audio.mp3")
print(f"Predicted genre: {result['predicted_genre']}")
print(f"Confidence: {result['confidence']:.2%}")

# Directory prediction
results = predict_directory("path/to/music/folder") 
```

## Server

### Setup

1. Install additional server dependencies:
```bash
pip install fastapi uvicorn python-multipart
```

2. Start the server:
```bash
python server.py
```

The server will start on `http://localhost:8000` by default.

### API Endpoints

- `POST /predict`: Upload audio file for genre prediction
- `GET /health`: Server health check

Example curl request:
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/audio.mp3" \
  -H "accept: application/json"
```

## Frontend

### Setup

1. Install dependencies:
```bash
cd genre-classifier
npm install
```

2. Start development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### Features

- Drag & drop audio file upload
- Real-time genre prediction
- Confidence scores visualization

## Model Details

- Input: Audio waveform (resampled to 16kHz if needed)
- Feature extraction: M2D Vision Transformer architecture 
- Feature dimension: 3840
- Output: 5 genre probabilities
