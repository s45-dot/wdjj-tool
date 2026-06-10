# Tests — Bubble Stretch Tool

## Phase 1 Testing Strategy

Phase 1 testing is **manual and visual**. Automated unit and integration tests will be introduced in Phase 2.

## Test Checklist

### 1. Backend Health Check

```bash
curl http://localhost:8000/api/health
```

Expected: `{"status":"ok","version":"0.1.0","timestamp":"..."}`

### 2. Image Upload and Processing

Use `scripts/upload_test.sh` or a tool like Postman / Insomnia:

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test_image.png"
```

Expected: JSON response with `id`, `original_url`, `processed_url`, and `grid_lines`.

### 3. Visual Grid Inspection

- Upload a test image (suggested: 600×600 PNG with colored quadrants).
- Verify the 3×3 grid lines appear at ⅓ and ⅔ positions.
- Confirm each of the 9 cells is visually distinct.

### 4. Stretch Effect Verification

- Upload an image with a clear center subject (e.g., a circle or face).
- Apply a non-uniform stretch (e.g., center cell = 1.5, edges = 1.0).
- Visually confirm the center is enlarged while edges remain unchanged.

### 5. Frontend Upload Flow

- Open `http://localhost:5173`.
- Drag and drop a test image.
- Confirm the grid overlay renders correctly.
- Adjust stretch sliders and submit.
- Confirm the processed result displays in the comparison view.

### 6. Edge Cases

| Scenario                        | Expected Behavior                        |
|---------------------------------|------------------------------------------|
| Non-square image (800×600)      | Grid adapts to aspect ratio              |
| Very small image (32×32)        | Minimum cell size enforced               |
| Very large image (4000×4000)    | Resized to max dimension before processing |
| Invalid file (PDF)              | 400 Bad Request                          |
| No file in request              | 422 Validation Error                     |
| File > 10 MB                    | 413 Payload Too Large                    |

## Test Images

Place test images in `tests/fixtures/`. Suggested test images:

| File                 | Size     | Description                    |
|----------------------|----------|--------------------------------|
| grid_600x600.png     | 600×600  | Colored quadrants for grid test |
| circle_400x400.png   | 400×400  | Center circle for stretch test  |
| photo_800x600.jpg    | 800×600  | Real photo for visual test      |

## Future (Phase 2)

- **Pytest** for backend unit tests (grid split, stretch, reassemble).
- **Vitest** for frontend component tests.
- **Playwright** for end-to-end browser tests.
