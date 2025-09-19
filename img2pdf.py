#!/usr/bin/env python3
"""
Image to PDF Converter CLI

A command-line tool to convert image files (JPEG, PNG, etc.) to PDF documents.
Supports single image conversion and batch processing of multiple images.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
from PIL import Image, ImageOps
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Supported image formats
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp'}


class ImageToPDFConverter:
    """Main class for converting images to PDF."""
    
    def __init__(self, quality: int = 95, max_size: Optional[tuple] = None):
        """
        Initialize the converter.
        
        Args:
            quality: JPEG quality for compression (1-100)
            max_size: Maximum size tuple (width, height) for resizing
        """
        self.quality = quality
        self.max_size = max_size
    
    def convert_single_image(self, image_path: Path, output_path: Path) -> bool:
        """
        Convert a single image to PDF.
        
        Args:
            image_path: Path to the input image
            output_path: Path for the output PDF
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Converting {image_path} to {output_path}")
            
            # Open and process the image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (for PNG with transparency, etc.)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background for transparent images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if max_size is specified
                if self.max_size:
                    img = ImageOps.fit(img, self.max_size, Image.Resampling.LANCZOS)
                
                # Auto-rotate based on EXIF data
                img = ImageOps.exif_transpose(img)
                
                # Save as PDF
                img.save(output_path, "PDF", quality=self.quality, optimize=True)
                
            logger.info(f"Successfully converted {image_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to convert {image_path}: {e}")
            return False
    
    def convert_multiple_images(self, image_paths: List[Path], output_path: Path) -> bool:
        """
        Convert multiple images into a single PDF.
        
        Args:
            image_paths: List of paths to input images
            output_path: Path for the output PDF
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Converting {len(image_paths)} images to {output_path}")
            
            processed_images = []
            
            for image_path in image_paths:
                try:
                    with Image.open(image_path) as img:
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'LA', 'P'):
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                            img = background
                        elif img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Resize if max_size is specified
                        if self.max_size:
                            img = ImageOps.fit(img, self.max_size, Image.Resampling.LANCZOS)
                        
                        # Auto-rotate based on EXIF data
                        img = ImageOps.exif_transpose(img)
                        
                        # Keep a copy of the processed image
                        processed_images.append(img.copy())
                        
                except Exception as e:
                    logger.warning(f"Skipping {image_path}: {e}")
                    continue
            
            if not processed_images:
                logger.error("No valid images to convert")
                return False
            
            # Save all images as a single PDF
            if len(processed_images) == 1:
                processed_images[0].save(output_path, "PDF", quality=self.quality, optimize=True)
            else:
                processed_images[0].save(
                    output_path, "PDF", 
                    save_all=True, 
                    append_images=processed_images[1:],
                    quality=self.quality,
                    optimize=True
                )
            
            logger.info(f"Successfully created PDF with {len(processed_images)} pages")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create PDF: {e}")
            return False


def find_images_in_directory(directory: Path, recursive: bool = False) -> List[Path]:
    """
    Find all supported image files in a directory.
    
    Args:
        directory: Directory to search
        recursive: Whether to search recursively
        
    Returns:
        List of image file paths
    """
    pattern = "**/*" if recursive else "*"
    image_files = []
    
    for file_path in directory.glob(pattern):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
            image_files.append(file_path)
    
    return sorted(image_files)


def parse_size(size_str: str) -> tuple:
    """Parse size string like '800x600' into tuple (800, 600)."""
    try:
        width, height = map(int, size_str.split('x'))
        return (width, height)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid size format: {size_str}. Use format like '800x600'")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert image files to PDF documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.jpg                          # Convert single image to image.pdf
  %(prog)s image.jpg -o document.pdf          # Convert with custom output name
  %(prog)s *.jpg -o combined.pdf              # Combine multiple images into one PDF
  %(prog)s -d /path/to/images                 # Convert all images in directory
  %(prog)s -d /path/to/images -r              # Recursive directory search
  %(prog)s image.jpg --max-size 800x600       # Resize image before conversion
  %(prog)s image.jpg --quality 85             # Adjust JPEG quality
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        'images', 
        nargs='*', 
        help='Image file(s) to convert'
    )
    input_group.add_argument(
        '-d', '--directory',
        type=Path,
        help='Directory containing images to convert'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output PDF file path (default: auto-generated based on input)'
    )
    
    # Processing options
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Search directory recursively for images'
    )
    parser.add_argument(
        '--quality',
        type=int,
        default=95,
        choices=range(1, 101),
        metavar='1-100',
        help='JPEG quality for compression (default: 95)'
    )
    parser.add_argument(
        '--max-size',
        type=parse_size,
        help='Maximum size for images (format: WIDTHxHEIGHT, e.g., 800x600)'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Create separate PDF for each image instead of combining'
    )
    
    # Logging options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress all output except errors'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.quiet:
        logger.setLevel(logging.ERROR)
    elif args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Validate mutually exclusive arguments
    if args.images and args.directory:
        parser.error("Cannot specify both image files and directory")
    
    # Get list of images to process
    image_paths = []
    
    if args.directory:
        if not args.directory.exists():
            logger.error(f"Directory does not exist: {args.directory}")
            sys.exit(1)
        if not args.directory.is_dir():
            logger.error(f"Not a directory: {args.directory}")
            sys.exit(1)
        
        image_paths = find_images_in_directory(args.directory, args.recursive)
        if not image_paths:
            logger.error(f"No supported image files found in {args.directory}")
            sys.exit(1)
    else:
        # Process individual image files
        for img_path_str in args.images:
            img_path = Path(img_path_str)
            if not img_path.exists():
                logger.error(f"File does not exist: {img_path}")
                sys.exit(1)
            if img_path.suffix.lower() not in SUPPORTED_FORMATS:
                logger.error(f"Unsupported format: {img_path}")
                sys.exit(1)
            image_paths.append(img_path)
    
    logger.info(f"Found {len(image_paths)} image(s) to process")
    
    # Initialize converter
    converter = ImageToPDFConverter(quality=args.quality, max_size=args.max_size)
    
    # Process images
    if args.batch or (len(image_paths) == 1 and not args.output):
        # Create separate PDF for each image
        success_count = 0
        for image_path in image_paths:
            if args.output and len(image_paths) == 1:
                output_path = args.output
            else:
                output_path = image_path.with_suffix('.pdf')
            
            if converter.convert_single_image(image_path, output_path):
                success_count += 1
        
        logger.info(f"Successfully converted {success_count}/{len(image_paths)} images")
        
    else:
        # Combine all images into single PDF
        if args.output:
            output_path = args.output
        else:
            # Generate output name based on directory or first image
            if args.directory:
                output_path = args.directory / f"{args.directory.name}_combined.pdf"
            else:
                output_path = image_paths[0].parent / "combined.pdf"
        
        if converter.convert_multiple_images(image_paths, output_path):
            logger.info(f"All images successfully combined into {output_path}")
        else:
            logger.error("Failed to create combined PDF")
            sys.exit(1)


if __name__ == "__main__":
    main()
