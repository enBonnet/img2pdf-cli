# Image to PDF Converter CLI

A powerful command-line tool to convert image files into PDF documents. Supports single image conversion, batch processing, and combining multiple images into a single PDF.

## Features

- **Multiple Input Formats**: Supports JPEG, PNG, BMP, TIFF, GIF, and WebP
- **Flexible Output Options**: Single PDFs or combined multi-page PDFs
- **Batch Processing**: Convert entire directories with optional recursive search
- **Image Processing**: Auto-rotation, transparency handling, and optional resizing
- **Quality Control**: Adjustable JPEG compression quality
- **Error Handling**: Comprehensive validation and informative error messages

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Examples

```bash
# Convert a single image
./img2pdf.py image.jpg

# Convert with custom output name
./img2pdf.py image.jpg -o document.pdf

# Combine multiple images into one PDF
./img2pdf.py *.jpg -o combined.pdf

# Convert all images in a directory
./img2pdf.py -d /path/to/images

# Recursive directory search
./img2pdf.py -d /path/to/images -r
```

### Advanced Options

```bash
# Resize images before conversion
./img2pdf.py image.jpg --max-size 800x600

# Adjust JPEG quality (1-100)
./img2pdf.py image.jpg --quality 85

# Create separate PDFs for each image (batch mode)
./img2pdf.py *.jpg --batch

# Verbose output
./img2pdf.py image.jpg -v

# Quiet mode (errors only)
./img2pdf.py image.jpg -q
```

## Command Line Options

### Input Options
- `images`: Image file(s) to convert (supports wildcards)
- `-d, --directory`: Directory containing images to convert

### Output Options
- `-o, --output`: Output PDF file path
- `--batch`: Create separate PDF for each image instead of combining

### Processing Options
- `-r, --recursive`: Search directory recursively for images
- `--quality`: JPEG quality for compression (1-100, default: 95)
- `--max-size`: Maximum size for images (format: WIDTHxHEIGHT, e.g., 800x600)

### Logging Options
- `-v, --verbose`: Enable verbose output
- `-q, --quiet`: Suppress all output except errors

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- GIF (.gif)
- WebP (.webp)

## Image Processing Features

### Transparency Handling
- PNG images with transparency are converted to RGB with white background
- Maintains image quality while ensuring PDF compatibility

### Auto-Rotation
- Automatically rotates images based on EXIF orientation data
- Ensures proper image orientation in the final PDF

### Resizing
- Optional image resizing with `--max-size` parameter
- Uses high-quality Lanczos resampling for best results
- Maintains aspect ratio while fitting within specified dimensions

## Examples

### Single Image Conversion
```bash
# Basic conversion
./img2pdf.py photo.jpg
# Output: photo.pdf

# Custom output name
./img2pdf.py photo.jpg -o my-document.pdf
```

### Multiple Images
```bash
# Combine into single PDF
./img2pdf.py img1.jpg img2.png img3.bmp -o combined.pdf

# Create separate PDFs
./img2pdf.py *.jpg --batch
```

### Directory Processing
```bash
# Convert all images in current directory
./img2pdf.py -d .

# Recursive search with custom output
./img2pdf.py -d /home/user/photos -r -o family-album.pdf

# Batch process directory
./img2pdf.py -d /home/user/photos --batch
```

### Image Optimization
```bash
# Resize large images and reduce quality
./img2pdf.py large-image.jpg --max-size 1200x1200 --quality 75

# High quality conversion
./img2pdf.py image.png --quality 95
```

## Error Handling

The tool provides comprehensive error handling for common issues:

- **Missing files**: Clear error messages for non-existent files
- **Unsupported formats**: Validation of image file extensions
- **Corrupted images**: Graceful handling of damaged image files
- **Permission issues**: Clear feedback on file access problems
- **Invalid parameters**: Helpful error messages for incorrect arguments

## Installation as System Command

To use the tool from anywhere on your system:

1. Copy the script to a directory in your PATH:
   ```bash
   sudo cp img2pdf.py /usr/local/bin/img2pdf
   ```

2. Or create a symlink:
   ```bash
   sudo ln -s $(pwd)/img2pdf.py /usr/local/bin/img2pdf
   ```

3. Then use it from anywhere:
   ```bash
   img2pdf photo.jpg
   ```

## Requirements

- Python 3.6 or higher
- Pillow (PIL) library for image processing

## License

This project is released under the MIT License.
