# Architecture

## Overview

Bubble Stretch Tool uses a 4-layer architecture. Each layer is independently testable and communicates through well-defined interfaces.

```
┌──────────────────────────────────────────────────┐
│                Layer 4: AI Orchestration          │
│  Hermes · QwenCode · Gemini · CodeWhale          │
│  ─ Agent workflow, code gen, review, test        │
├──────────────────────────────────────────────────┤
│                Layer 3: Frontend (Vue 3)          │
│  TypeScript · Vite · Canvas API                  │
│  ─ Image upload, preview, 3×3 grid overlay       │
│  ─ Stretch controls, side-by-side compare        │
│  ─ HTTP calls to backend API                     │
├──────────────────────────────────────────────────┤
│                Layer 2: Backend (FastAPI)          │
│  Python · Uvicorn · Pillow                       │
│  ─ REST API (/api/health, /api/upload, etc.)     │
│  ─ Image validation and storage                  │
│  ─ Delegates processing to Pillow pipeline       │
├──────────────────────────────────────────────────┤
│                Layer 1: Image Processing           │
│  Pillow · Canvas                                 │
│  ─ 3×3 grid splitting                            │
│  ─ Per-cell stretch algorithm                    │
│  ─ Reassembly and output                         │
└──────────────────────────────────────────────────┘
```

## Layer Details

### Layer 1 — Image Processing

The core of the tool. Pillow handles server-side image manipulation; the Canvas API provides a browser-side fallback for real-time preview.

- **Grid splitting**: divide an image into 3×3 cells with configurable overlap or gap.
- **Stretch algorithm**: each cell is scaled independently based on a stretch factor, producing the "bubble" distortion effect.
- **Reassembly**: stretched cells are stitched back into a single output image.

### Layer 2 — Backend (FastAPI)

Serves the REST API and coordinates image processing.

| Endpoint          | Method | Purpose                        |
|-------------------|--------|--------------------------------|
| `/api/health`     | GET    | Service health check           |
| `/api/upload`     | POST   | Accept image, return processed result |

The backend validates uploaded images (format, size), stores them temporarily, invokes the Pillow pipeline, and returns the result to the frontend.

### Layer 3 — Frontend (Vue 3)

Single-page application built with Vue 3, TypeScript, and Vite.

- **Upload panel**: drag-and-drop or file-picker for source images.
- **Grid overlay**: visual 3×3 grid showing cell boundaries before processing.
- **Stretch controls**: sliders or numeric inputs for per-cell stretch factor.
- **Comparison view**: side-by-side or overlay comparison of original vs. processed image.
- **Canvas API**: used for client-side preview and optional lightweight processing.

### Layer 4 — AI Orchestration

Multi-agent setup coordinating development and quality assurance.

- **Hermes**: primary orchestrator, task routing, state management.
- **QwenCode**: code generation and review.
- **Gemini**: alternative review perspective and edge-case analysis.
- **CodeWhale**: runtime agent, tool execution, workspace management.

## Data Flow

```
User uploads image ──► Vue 3 frontend
                           │
                           ▼ POST /api/upload
                    FastAPI backend
                           │
                           ▼ Pillow pipeline
                    3×3 split → stretch → reassemble
                           │
                           ▼ Response (processed image URL)
                    Vue 3 displays result
```

## Key Design Decisions

1. **Server-side processing by default** — Pillow is more reliable for consistent output across browsers.
2. **Canvas as optional frontend path** — enables real-time preview without server round-trip for small images.
3. **REST API over GraphQL** — scope is small; REST keeps the backend simple and testable.
4. **Temporary file storage** — uploaded and processed images live in `backend/data/uploads/` and are cleaned up periodically.
