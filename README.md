
# 2Dto3D

## Overview
2Dto3D is a full-stack application that converts 2D images into 3D models using deep learning. It leverages the Pix2Vox neural network model on the backend and provides a smooth interactive experience via a React + Three.js frontend.

---

## Features
- Upload 2D images and get 3D model output
- Powered by Pix2Vox (pretrained on ShapeNet)
- Real-time preview of 3D models
- Fully modular with Flask backend and Vite + React frontend

---

## Tech Stack

### Frontend
- React 18
- Vite
- Three.js (for 3D rendering)
- TailwindCSS (for styling)

### Backend
- Python Flask
- PyTorch (for ML inference)
- Pix2Vox model integration
- CORS-enabled for local dev

---

## Installation

### Prerequisites
- Node.js & npm
- Python 3.8+
- PyTorch with CUDA (for model inference)

### Backend Setup

```bash
cd Backend
pip install -r requirements.txt
python server.py
```

> Note: Make sure Pix2Vox checkpoints are in `Pix2Vox/checkpoints/`.

### Frontend Setup

```bash
cd Frontend
npm install
npm run dev
```

> Access the app at `http://localhost:5173`

---

## How it Works
1. User uploads a 2D image from the frontend.
2. The image is sent to the Flask backend.
3. The backend uses the Pix2Vox model to infer a 3D voxel representation.
4. The resulting `.obj` model is returned and rendered using Three.js.

---

## Output
- 3D `.obj` file downloadable after processing
- 3D visualization in browser
