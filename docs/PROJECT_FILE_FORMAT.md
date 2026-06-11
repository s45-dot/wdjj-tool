# Project File Format (`.bubble.json`)

## Overview

The `.bubble.json` project file stores the complete editor state for a Bubble
Stretch Tool session. It can be exported to save work-in-progress and re-imported
to restore all parameters.

## File Format

- **Extension:** `.bubble.json`
- **MIME type:** `application/json`
- **Encoding:** UTF-8
- **Required fields at root:** `format`, `version`, `createdAt`, `updatedAt`,
  `asset`, `capInsets`, `contentInsets`, `scale`, `preview`

## Top-level Structure

```jsonc
{
  "format": "bubble-project",           // string, literal — file type identifier
  "version": 1,                          // number, literal — schema version
  "createdAt": "2026-06-11T10:00:00Z",  // ISO 8601 timestamp
  "updatedAt": "2026-06-11T10:30:00Z",  // ISO 8601 timestamp

  "asset": { /* see Asset */ },
  "capInsets": { /* see Insets */ },
  "contentInsets": { /* see Insets */ },
  "scale": 1,                            // 1 | 2 | 3
  "preview": { /* see Preview */ },

  "exportOptions": { /* optional, see ExportOptions */ }
}
```

### Asset

Describes the source image file.

| Field      | Type   | Required | Description                    |
|------------|--------|----------|--------------------------------|
| `filename` | string | yes      | Original uploaded filename     |
| `width`    | number | yes      | Image width in pixels          |
| `height`   | number | yes      | Image height in pixels         |
| `mimeType` | string | yes      | MIME type (e.g. `"image/png"`) |

```jsonc
{
  "filename": "chat_bubble.png",
  "width": 300,
  "height": 120,
  "mimeType": "image/png"
}
```

### Insets

Four-side inset definition used for both `capInsets` and `contentInsets`.

| Field    | Type   | Required | Description      |
|----------|--------|----------|------------------|
| `top`    | number | yes      | Top inset in px  |
| `right`  | number | yes      | Right inset in px|
| `bottom` | number | yes      | Bottom inset in px|
| `left`   | number | yes      | Left inset in px |

```jsonc
{
  "top": 20,
  "right": 40,
  "bottom": 20,
  "left": 40
}
```

### Scale

The image scale factor used for measurement conversions.

- **Type:** number
- **Allowed values:** `1`, `2`, `3`

### Preview

Chat bubble preview parameters.

| Field            | Type   | Required | Allowed Values |
|------------------|--------|----------|----------------|
| `text`           | string | yes      | Any string     |
| `fontSize`       | number | yes      | Positive px    |
| `lineHeight`     | number | yes      | Positive px    |
| `maxBubbleWidth` | number | yes      | Positive px    |
| `direction`      | string | yes      | `"left"` or `"right"` |

```jsonc
{
  "text": "Hello world",
  "fontSize": 16,
  "lineHeight": 22,
  "maxBubbleWidth": 280,
  "direction": "left"
}
```

### ExportOptions (optional)

_This section is optional._ When present it carries the last-used export
settings from the Export panel.

| Field          | Type   | Required | Description                  |
|----------------|--------|----------|------------------------------|
| `outputs`      | object | yes      | Boolean flags per format     |
| `targetWidth`  | number | yes      | Export target width in px    |
| `targetHeight` | number | yes      | Export target height in px   |
| `scale`        | number | yes      | Export scale (1, 2, or 3)    |

**outputs object:**

| Field               | Type    | Description                 |
|---------------------|---------|-----------------------------|
| `androidNinePatch`  | boolean | Generate Android .9.png     |
| `iosJson`           | boolean | Generate iOS JSON           |
| `androidJson`       | boolean | Generate Android JSON       |
| `previewPng`        | boolean | Generate preview PNG        |
| `readme`            | boolean | Generate README             |
| `sourcePng`         | boolean | Include source PNG          |

```jsonc
{
  "outputs": {
    "androidNinePatch": true,
    "iosJson": true,
    "androidJson": true,
    "previewPng": true,
    "readme": true,
    "sourcePng": true
  },
  "targetWidth": 240,
  "targetHeight": 80,
  "scale": 1
}
```

## Complete Example

```json
{
  "format": "bubble-project",
  "version": 1,
  "createdAt": "2026-06-11T10:00:00Z",
  "updatedAt": "2026-06-11T10:30:00Z",
  "asset": {
    "filename": "chat_bubble.png",
    "width": 300,
    "height": 120,
    "mimeType": "image/png"
  },
  "capInsets": {
    "top": 30,
    "right": 60,
    "bottom": 30,
    "left": 60
  },
  "contentInsets": {
    "top": 10,
    "right": 20,
    "bottom": 10,
    "left": 20
  },
  "scale": 1,
  "preview": {
    "text": "Hello world",
    "fontSize": 16,
    "lineHeight": 22,
    "maxBubbleWidth": 280,
    "direction": "left"
  },
  "exportOptions": {
    "outputs": {
      "androidNinePatch": true,
      "iosJson": true,
      "androidJson": true,
      "previewPng": true,
      "readme": true,
      "sourcePng": true
    },
    "targetWidth": 240,
    "targetHeight": 80,
    "scale": 1
  }
}
```

## Validation Rules

A `.bubble.json` file is considered valid when all of the following hold:

1. Root is a JSON object
2. `format` is exactly the string `"bubble-project"`
3. `version` is exactly the number `1`
4. `createdAt` and `updatedAt` are strings
5. `asset` is an object with string `filename`, positive number `width`,
   positive number `height`, and string `mimeType`
6. `capInsets` and `contentInsets` are objects with finite number values for
   `top`, `right`, `bottom`, `left`
7. `scale` is `1`, `2`, or `3`
8. `preview` is an object with string `text`, finite number `fontSize`,
   finite number `lineHeight`, finite number `maxBubbleWidth`, and
   `direction` equal to `"left"` or `"right"`
