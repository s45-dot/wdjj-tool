# Frontend — Bubble Stretch Tool

## Tech Stack

| Technology       | Purpose                           |
|------------------|-----------------------------------|
| Vue 3            | Component framework (Composition API) |
| TypeScript       | Type safety                       |
| Vite             | Dev server and build tool         |
| Canvas API       | Client-side image preview & overlay |

## Project Structure

```
frontend/
├── index.html
├── vite.config.ts
├── tsconfig.json
├── package.json
├── public/
└── src/
    ├── main.ts
    ├── App.vue
    ├── components/
    │   ├── ImageUploader.vue    # Drag-and-drop upload
    │   ├── GridOverlay.vue      # 3×3 grid visualization
    │   ├── StretchControls.vue  # Per-cell factor controls
    │   └── ComparisonView.vue   # Before/after display
    ├── services/
    │   └── api.ts               # HTTP client for backend API
    └── types/
        └── index.ts             # TypeScript type definitions
```

## Setup

```bash
cd frontend
npm install
npm run dev
```

The dev server starts at `http://localhost:5173` by default.

## Key Components

- **ImageUploader**: Handles file selection, drag-and-drop, and validation (format, size).
- **GridOverlay**: Renders a 3×3 grid on top of the uploaded image using the Canvas API.
- **StretchControls**: Sliders for each of the 9 cells (arranged in a 3×3 grid UI).
- **ComparisonView**: Side-by-side or overlay comparison between original and processed images.

## API Integration

All backend calls go through `src/services/api.ts`, which wraps `fetch()` calls to `http://localhost:8000/api/...`. The Vite dev server proxies `/api` requests to the backend during development.
