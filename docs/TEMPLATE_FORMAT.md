# Template File Format (`.bubble-template.json`)

## Overview

A `.bubble-template.json` file defines a reusable preset for bubble-stretch
parameters. Unlike a full project file, a template only stores insets, scale,
and direction — it is image-agnostic and can be applied to any project.

## File Format

- **Extension:** `.bubble-template.json`
- **MIME type:** `application/json`
- **Encoding:** UTF-8
- **Required fields at root:** `format`, `version`, `name`, `description`,
  `capInsets`, `contentInsets`, `scale`, `direction`

## Top-level Structure

```jsonc
{
  "format": "bubble-template",     // string, literal — file type identifier
  "version": 1,                     // number, literal — schema version
  "name": "Rounded Chat",           // human-readable template name
  "description": "...",             // description of when to use this preset
  "capInsets": { /* see Insets */ },
  "contentInsets": { /* see Insets */ },
  "scale": 1,                       // 1 | 2 | 3
  "direction": "left"               // "left" | "right"
}
```

### Fields

| Field          | Type   | Required | Description                            |
|----------------|--------|----------|----------------------------------------|
| `format`       | string | yes      | Must be `"bubble-template"`            |
| `version`      | number | yes      | Must be `1`                            |
| `name`         | string | yes      | Human-readable preset name             |
| `description`  | string | yes      | Short description of the preset        |
| `capInsets`    | object | yes      | Stretch cap insets (see Insets below)  |
| `contentInsets`| object | yes      | Content padding insets (see Insets)    |
| `scale`        | number | yes      | Image scale — `1`, `2`, or `3`        |
| `direction`    | string | yes      | Bubble direction — `"left"` or `"right"` |

### Insets

Same format as the project file insets.

| Field    | Type   | Required | Description      |
|----------|--------|----------|------------------|
| `top`    | number | yes      | Top inset in px  |
| `right`  | number | yes      | Right inset in px|
| `bottom` | number | yes      | Bottom inset in px|
| `left`   | number | yes      | Left inset in px |

## Complete Example

```json
{
  "format": "bubble-template",
  "version": 1,
  "name": "Rounded Chat Default",
  "description": "Standard rounded-rectangle chat bubble with 60px horizontal caps and 30px vertical caps. Suitable for most chat bubble images with rounded corners.",
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
  "direction": "left"
}
```

## Validation Rules

A `.bubble-template.json` file is valid when all of the following hold:

1. Root is a JSON object
2. `format` is exactly the string `"bubble-template"`
3. `version` is exactly the number `1`
4. `name` is a string
5. `description` is a string
6. `capInsets` and `contentInsets` are objects with finite number values for
   `top`, `right`, `bottom`, `left`
7. `scale` is `1`, `2`, or `3`
8. `direction` is `"left"` or `"right"`
