import os
import re
from PIL import Image, ExifTags

# Set the max file size to 5MB (5 * 1024 * 1024 bytes)
MAX_SIZE = 5 * 1024 * 1024

# Function to correct image orientation based on EXIF data
def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # Image doesn't have EXIF data or orientation info
        pass
    return image

def compress_image(file_path, output_path):
    with Image.open(file_path) as img:
        img = correct_image_orientation(img)
        # Reduce quality or resize to reduce file size
        img.save(output_path, optimize=True, quality=85)

def resize_image(file_path, output_path, max_width=1920, max_height=1080):
    with Image.open(file_path) as img:
        img = correct_image_orientation(img)
        # Resize image while maintaining the aspect ratio
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
        img.save(output_path, optimize=True, quality=85)

def clean_facetune_filename(filename):
    pattern = r"(Facetune_)(\d{2}-\d{2}-\d{4}-)(\d{2}-\d{2}-\d{2})(\.jpg)"

    # Check if the pattern exists in the filename
    if re.search(pattern, filename):
        # Use re.sub to remove the date part from the filename
        new_filename = re.sub(pattern, r"\1\3\4", filename)
        return new_filename
    else:
        # If no pattern is found, return the original filename
        return filename


def check_and_compress_files(directory):
    # Create subfolders for compressed images and incompatible originals
    compressed_folder = os.path.join(directory, 'compressed_images')
    incompatible_folder = os.path.join(directory, 'incompatible_originals')

    if not os.path.exists(compressed_folder):
        os.makedirs(compressed_folder)
    if not os.path.exists(incompatible_folder):
        os.makedirs(incompatible_folder)

    # Initialize a flag to check if any image files are found
    found_image_files = False

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        
        # Check if it's an image file and it's not a directory
        if os.path.isfile(file_path) and file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
            found_image_files = True  # Set the flag to True as we found an image file


            
            # Get the file size
            file_size = os.path.getsize(file_path)
            

            cleaned_filename = clean_facetune_filename(file_name)
            cleaned_file_path = os.path.join(root, cleaned_filename)


            if cleaned_filename != file_name:
                    os.rename(file_path, cleaned_file_path)
                    file_path = cleaned_file_path
                # If the file is larger than 5MB
            if file_size > MAX_SIZE:
                    print(f"{file_name} is larger than 5MB, compressing...")
                    
                    # Create a path for the compressed file in the subfolder
                    compressed_file_path = os.path.join(compressed_folder, f"compressed_{file_name}")
                    
                    # First try compressing the image
                    compress_image(file_path, compressed_file_path)
                    
                    # Check the size of the compressed image
                    compressed_size = os.path.getsize(compressed_file_path)
                    
                    if compressed_size > MAX_SIZE:
                        print(f"{file_name} is still too large, resizing...")
                        # Resize the image if compression isn't enough
                        resize_image(compressed_file_path, compressed_file_path)
                    
                    # Double check if the size is now less than 5MB
                    final_size = os.path.getsize(compressed_file_path)
                    if final_size <= MAX_SIZE:
                        print(f"{file_name} is now under 5MB.")
                    else:
                        print(f"Failed to reduce {file_name} under 5MB, moving original to incompatible folder.")
                        # Move the original file to the incompatible folder
                        incompatible_file_path = os.path.join(incompatible_folder, cleaned_filename)
                        os.rename(file_path, incompatible_file_path)
            else:
                    print(f"{file_name} is already under 5MB, moving to compressed folder.")
                    # Move file to compressed folder if it's already under 5MB
                    compressed_file_path = os.path.join(compressed_folder, cleaned_filename)
                    os.rename(file_path, compressed_file_path)

    if not found_image_files:
        print("No image files found in the specified directory.")

def move_leftover_files(directory):
    """Move any leftover files over 5MB to the incompatible folder."""
    incompatible_folder = os.path.join(directory, 'incompatible_originals')
    if not os.path.exists(incompatible_folder):
        os.makedirs(incompatible_folder)
    
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Skip the compressed images and incompatible folder to avoid recursion
            if 'compressed_images' in root or 'incompatible_originals' in root:
                continue
            
            # Check if it's an image file
            if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
                # Get the file size
                file_size = os.path.getsize(file_path)

                # Move file if it's larger than 5MB
                if file_size > MAX_SIZE:
                    print(f"Moving leftover file {file_name} over 5MB to the incompatible folder.")
                    incompatible_file_path = os.path.join(incompatible_folder, file_name)
                    os.rename(file_path, incompatible_file_path)


# Set the directory you want to scan
directory = r"C:\Users\Dreid\Desktop\Brain\Projects\Set Up Tiktok Shop\Pics"
check_and_compress_files(directory)
move_leftover_files(directory)

# FIX BUG WITH NAME LENGTH!

