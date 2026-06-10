# Backend — Bubble Stretch Tool

## Tech Stack

| Technology       | Purpose                           |
|------------------|-----------------------------------|
| FastAPI          | REST API framework                |
| Uvicorn          | ASGI server                       |
| Pillow           | Image loading, manipulation, saving |

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── app/
│   ├── __init__.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── images.py    # /api/health, /api/upload endpoints
│   └── services/
│       ├── __init__.py
│       ├── grid.py       # 3×3 split logic
│       ├── stretch.py    # Per-cell stretch algorithm
│       └── reassemble.py # Stitch cells back together
└── data/
    └── uploads/          # Temporary storage for uploaded & processed images
```

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API is available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## Core Services

### `grid.py`

Splits an image into 3×3 cells. Handles edge cases where dimensions are not evenly divisible by 3.

### `stretch.py`

Scales each cell independently by a configurable stretch factor. The center cell typically gets the highest stretch factor to produce the "bubble" effect.

### `reassemble.py`

Stitches the 9 stretched cells back into a single output image, preserving original aspect ratio where possible.
