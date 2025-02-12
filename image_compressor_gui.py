import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags

# Constants
MAX_SIZE = 5 * 1024 * 1024  # 5MB

# Function to correct image orientation

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
        pass
    return image

# Function to compress an image
def compress_image(file_path, output_path):
    with Image.open(file_path) as img:
        img = correct_image_orientation(img)
        img.save(output_path, optimize=True, quality=85)

# Function to resize an image
def resize_image(file_path, output_path, max_width=1920, max_height=1080):
    with Image.open(file_path) as img:
        img = correct_image_orientation(img)
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
        img.save(output_path, optimize=True, quality=85)

# Function to clean Facetune filenames
def clean_facetune_filename(filename):
    pattern = r"(Facetune_)(\d{2}-\d{2}-\d{4}-)(\d{2}-\d{2}-\d{2})(\.jpg)"
    return re.sub(pattern, r"\1\3\4", filename) if re.search(pattern, filename) else filename

# Function to process files
def check_and_compress_files(source_dir, destination_dir):
    compressed_folder = os.path.join(destination_dir, 'compressed_images')
    incompatible_folder = os.path.join(destination_dir, 'incompatible_originals')
    os.makedirs(compressed_folder, exist_ok=True)
    os.makedirs(incompatible_folder, exist_ok=True)
    
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if not os.path.isfile(file_path) or not file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
            continue
        
        cleaned_filename = clean_facetune_filename(file_name)
        cleaned_file_path = os.path.join(source_dir, cleaned_filename)
        if cleaned_filename != file_name:
            os.rename(file_path, cleaned_file_path)
            file_path = cleaned_file_path
        
        file_size = os.path.getsize(file_path)
        compressed_file_path = os.path.join(compressed_folder, cleaned_filename)
        
        if file_size > MAX_SIZE:
            compress_image(file_path, compressed_file_path)
            if os.path.getsize(compressed_file_path) > MAX_SIZE:
                resize_image(compressed_file_path, compressed_file_path)
                if os.path.getsize(compressed_file_path) > MAX_SIZE:
                    os.rename(file_path, os.path.join(incompatible_folder, cleaned_filename))
        else:
            os.rename(file_path, compressed_file_path)

# GUI Application
def select_source_folder():
    folder = filedialog.askdirectory()
    if folder:
        source_var.set(folder)

def select_destination_folder():
    folder = filedialog.askdirectory()
    if folder:
        destination_var.set(folder)

def start_compression():
    source = source_var.get()
    destination = destination_var.get()
    if not source or not destination:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return
    check_and_compress_files(source, destination)
    messagebox.showinfo("Success", "Compression process completed!")

# Initialize UI
root = tk.Tk()
root.title("Image Compressor")

source_var = tk.StringVar()
destination_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Source Folder:").grid(row=0, column=0, sticky='w')
tk.Entry(frame, textvariable=source_var, width=50).grid(row=0, column=1)
tk.Button(frame, text="Browse", command=select_source_folder).grid(row=0, column=2)

tk.Label(frame, text="Destination Folder:").grid(row=1, column=0, sticky='w')
tk.Entry(frame, textvariable=destination_var, width=50).grid(row=1, column=1)
tk.Button(frame, text="Browse", command=select_destination_folder).grid(row=1, column=2)

tk.Button(frame, text="Start Compression", command=start_compression).grid(row=2, column=0, columnspan=3)

root.mainloop()


