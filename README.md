# Image Compressor GUI

## Overview
This project provides an easy-to-use GUI for compressing and resizing images. It ensures that images do not exceed a specified file size while maintaining their aspect ratio and quality.

## Features
- **Cross-platform GUI**: Uses Tkinter to provide a simple user interface.
- **Batch Processing**: Select a folder to process multiple images at once.
- **Compression & Resizing**: Reduces file sizes while maintaining image quality.
- **EXIF Orientation Correction**: Ensures images display correctly.
- **Custom File Naming**: Cleans up specific filename formats (e.g., Facetune-generated names).
- **Automatic Folder Management**: Organizes compressed images and those that remain too large.

## Installation
### Requirements
- Python 3.x
- Pillow (PIL Fork)
- Tkinter (comes with most Python distributions)

### Install Dependencies
```sh
pip install pillow
```

## Usage
1. Run the script:
   ```sh
   python image_compressor_gui.py
   ```
2. Select a source folder containing images.
3. Choose a destination folder where compressed images will be saved.
4. Click **Start Compression** to begin processing.
5. The program will compress images over 5MB and move them to a `compressed_images` folder. Images that cannot be reduced under 5MB will be moved to an `incompatible_originals` folder.

## Executable Version
A prebuilt executable version is available for users who do not wish to install Python or dependencies. 

### Warning
The current version of the executable **deletes the original uncompressed images after processing**. Use with caution and make sure to back up your images before running the program.

## Supported Formats
- JPG
- PNG
- BMP
- TIFF

## License
This project is licensed under the MIT License.

## Contributions
Feel free to fork and submit pull requests to enhance functionality!

## Author
[Devin Reid](https://github.com/your-github-profile)

