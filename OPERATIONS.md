# ImageX  Operations

## Remove Metadata

Strips all EXIF, XMP, and IPTC metadata from images. This removes camera info, GPS location, software tags (like "StableDiffusion", "DALL·E", "Midjourney"), and any AI-generation markers embedded in the file.

**Supported formats:** JPEG, PNG, WEBP, TIFF, BMP, GIF

**How it works:**
- JPEG: Saves with `exif=b""` — strips everything
- PNG/WEBP/TIFF/BMP/GIF: Re-saves clean, discarding all metadata

---

## Convert Format

Converts images between different formats. Handles transparency correctly (RGBA → RGB with white background when converting to JPEG).

**Supported conversions:**

| From | To |
|---|---|
| Any format | JPEG, PNG, WEBP, TIFF, BMP, GIF, HEIC |

**HEIC (iPhone) support:**
- Requires `pip install pillow-heif`
- If not installed, HEIC is hidden from the menu
- Supports both reading and writing HEIC

---

## Compress / Optimize

Reduces file size with a quality slider (1–100). Prints before/after size for every file.

**Format-specific behavior:**

| Format | Quality 50–100 | Quality 1–49 |
|---|---|---|
| JPEG | `quality=N` + `optimize=True` | Same (lower quality = smaller file) |
| PNG | `optimize=True` (lossless) | Quantizes to palette (lossy, ~90% smaller) |
| WEBP | `quality=N` | Same |
| Other | Re-saved with defaults | Re-saved with defaults |

---

## Resize

Scales images to new dimensions. Uses `LANCZOS` resampling for highest quality.

**Available methods:**

| Method | What it does |
|---|---|
| **Percentage** | Scale by % of original (50 = half, 200 = double) |
| **Exact dimensions** | Force specific width × height (may stretch) |
| **Fit within** | Scale to fit max width/height while maintaining aspect ratio. Never upscales. |

---

## Rename Batch

Renames multiple image files using a pattern. Supports in-place rename only (no output mode needed).

**Pattern variables:**

| Variable | What it does |
|---|---|
| `%n` | Auto-numbering with zero-padding (`001`, `002`, ...) |
| `%o` | Original filename (without extension) |

**Example:**
- Pattern: `vacation_%n`
- Start: `1`, Padding: `3`
- `IMG_001.jpg` → `vacation_001.jpg`
- `IMG_002.jpg` → `vacation_002.jpg`

Shows a preview before committing. If you don't like it, cancel with Ctrl+C.

---

## Add Noise

Adds random pixel noise to images. Useful for making AI-generated images harder to detect by adding subtle imperfections.

**Noise types:**

| Type | Effect |
|---|---|
| **Gaussian** | Subtle uniform noise across the image. Lower intensities (1–10) are barely visible to the eye but effective. |
| **Salt & Pepper** | Random white/black pixels scattered. More noticeable, simulates sensor noise. |

**Intensity scale:** 1 (barely visible) → 100 (heavily distorted). Recommended: 3–15 for undetectable noise.

---

## Watermark

Two modes: **Add** your own watermark or **Remove** an existing watermark from an image.

### ADD Mode

Place a text or image watermark on your images.

**Options:**

| Option | Details |
|---|---|
| **Type** | Text or Image (logo file) |
| **Position** | Top-Left, Top-Right, Bottom-Left, Bottom-Right, Center |
| **Opacity** | 1–100 (alpha blending) |

**Text options:** Content, font size, color (name or hex like `red`, `#FFFFFF`).

**Image options:** Path to logo file, scale as % of image width.

No extra dependencies — uses pure Pillow.

### REMOVE Mode

Fills the watermark region by sampling surrounding pixels and blending with a blur. Works without OpenCV or any extra libraries.

**Options:**

| Option | Details |
|---|---|
| **Position** | Top-Left, Top-Right, Bottom-Left, Bottom-Right, Center |
| **Size** | Small (10%), Medium (20%), Large (30%) of image dimensions |

**How it works:**
- Samples border pixels around the selected region
- Fills region with average border color
- Applies Gaussian blur to blend

---

## Rotate

Rotates images 90° Left, 90° Right, or 180° (Upside Down). No quality loss — uses Pillow's built-in transpose.

---

## Flip

Mirrors images across an axis. Unlike Rotate, this produces a *reflection* — a flipped image cannot be reproduced by any rotation.

**Directions:**

| Direction | What it does |
|---|---|
| **Horizontal** | Mirror left ↔ right (e.g. un-mirror a selfie) |
| **Vertical** | Mirror top ↔ bottom (reflection, **not** the same as a 180° rotation) |

No quality loss — uses Pillow's built-in transpose.

---

## Planned Features

See [CONTRIBUTION.md](CONTRIBUTION.md) for how to add new features.
