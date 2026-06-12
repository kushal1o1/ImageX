```
██╗███╗   ███╗ █████╗  ██████╗ ███████╗██╗  ██╗
██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝╚██╗██╔╝
██║██╔████╔██║███████║██║  ███╗█████╗   ╚███╔╝
██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝   ██╔██╗
██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗██╔╝ ██╗
╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
```

Image processing CLI tool — right in your terminal.

```bash
pip install imagex
imagex
```

Navigate to any folder with images and run `imagex`.

## Features

| Feature | Description |
|---|---|
| Remove Metadata | Strip EXIF/XMP/IPTC (incl. AI generation markers) |
| Convert Format | JPG ↔ PNG ↔ WEBP ↔ TIFF ↔ BMP ↔ GIF ↔ HEIC |
| Compress / Optimize | Reduce file size with quality slider |
| Resize | Percentage, exact dimensions, fit within bounds |
| Rename Batch | Pattern-based renaming (%n, %o) |
| Add Noise | Gaussian or salt & pepper (bypass AI detection) |
| Watermark | Add text/image or remove existing |

Full details in [OPERATIONS.md](OPERATIONS.md).

## Install

```bash
# From PyPI (recommended)
pip install imagex

# Dev mode from repo (changes take effect immediately)
pip install -e .
```

Then run `imagex` from any folder.

## Adding Features

See [CONTRIBUTION.md](CONTRIBUTION.md) for the contribution guide.

## License

MIT
