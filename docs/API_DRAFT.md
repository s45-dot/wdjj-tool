# API Draft

## Base URL

All endpoints are served under `/api`. During development the backend runs at `http://localhost:8000`.

---

## `GET /api/health`

Health check endpoint.

### Request

```
GET /api/health
```

### Response

**200 OK**

```json
{
  "status": "ok",
  "version": "0.1.0",
  "timestamp": "2026-06-11T12:00:00Z"
}
```

### Notes

- No authentication required during Phase 1.
- Used by `check_all.sh` and frontend startup verification.

---

## `POST /api/upload`

Upload an image for processing.

### Request

```
POST /api/upload
Content-Type: multipart/form-data

file: <image_data>
```

| Field | Type   | Required | Description                   |
|-------|--------|----------|-------------------------------|
| file  | File   | Yes      | JPEG, PNG, or WebP image      |
| stretch_factors | JSON string | No | 3×3 array of stretch factors (default: all 1.0) |

### Response

**200 OK**

```json
{
  "id": "abc123",
  "original_url": "/uploads/abc123_original.png",
  "processed_url": "/uploads/abc123_processed.png",
  "grid_lines": {
    "cols": [0.33, 0.67],
    "rows": [0.33, 0.67]
  },
  "stretch_factors": [
    [1.0, 1.2, 1.0],
    [1.2, 1.5, 1.2],
    [1.0, 1.2, 1.0]
  ]
}
```

**400 Bad Request**

```json
{
  "detail": "Invalid file type. Accepted: image/jpeg, image/png, image/webp"
}
```

**413 Payload Too Large**

```json
{
  "detail": "File too large. Maximum size is 10 MB."
}
```

### Notes

- Uploaded file is saved to `backend/data/uploads/` with a UUID-based filename.
- Processing runs synchronously for Phase 1 (async with background tasks planned for later).
- The `stretch_factors` field, if omitted, defaults to a center-weighted pattern (center cell stretched most, edges less, corners least).

---

## Future Endpoints (Phase 2+)

| Method | Path                  | Purpose                              |
|--------|-----------------------|--------------------------------------|
| GET    | /api/image/{id}       | Retrieve processed image metadata    |
| POST   | /api/batch            | Process multiple images              |
| GET    | /api/presets          | List named stretch presets           |
