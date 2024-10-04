import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to add logo to images
def add_logo():
    logo_name = logo_name_entry.get()
    new_folder_name = new_folder_name_entry.get()

    # Validate inputs
    if not logo_name or not new_folder_name:
        messagebox.showerror("Input Error", "Please provide both logo name and new folder name.")
        return

    # Get logo information
    try:
        logo_image = Image.open(logo_name).convert("RGBA")
    except Exception as e:
        messagebox.showerror("File Error", f"Error opening logo file: {e}")
        return

    logo_width, logo_height = logo_image.size

    # Create the folder if it doesn't exist
    if not os.path.exists(new_folder_name):
        os.mkdir(new_folder_name)

    # Loop over images in the current directory
    for filename in os.listdir('.'):
        # Check if file is an image and it's not the logo
        if not (filename.endswith('.png') or filename.endswith('.jpg')) or filename == logo_name:
            continue

        try:
            img = Image.open(filename).convert("RGBA")
            width, height = img.size

            # Resize logo to be a percentage of the original image's width
            logo_scale_factor = 0.1  # Adjust this value as needed (e.g., 0.1 for 10%)
            new_logo_width = int(width * logo_scale_factor)
            new_logo_height = int((logo_height / logo_width) * new_logo_width)

            # Resize the logo using LANCZOS filter for high-quality downsampling
            logo_image_resized = logo_image.resize((new_logo_width, new_logo_height), Image.LANCZOS)

            # Create a new image with the same size as the original image
            new_img = Image.new("RGBA", img.size)

            # Paste the original image into the new image
            new_img.paste(img, (0, 0))

            # Add the resized logo to the image
            new_img.paste(logo_image_resized, (width - new_logo_width, height - new_logo_height), logo_image_resized)

            # Determine the file format for saving
            if filename.endswith('.png'):
                new_img.save(os.path.join(new_folder_name, filename))  # Save as PNG
            else:
                # Convert to RGB before saving as JPEG
                new_img.convert("RGB").save(os.path.join(new_folder_name, filename), format='JPEG')

        except Exception as e:
            messagebox.showerror("Processing Error", f"Error processing file {filename}: {e}")
            continue

    messagebox.showinfo("Success", "All images processed successfully!")

# Create the main window
root = tk.Tk()
root.title("Logo Adder")

# Create and place the logo name label and entry
logo_name_label = tk.Label(root, text="Enter Logo Name with Extension:")
logo_name_label.pack(pady=5)
logo_name_entry = tk.Entry(root, width=40)
logo_name_entry.pack(pady=5)

# Create and place the new folder name label and entry
new_folder_name_label = tk.Label(root, text="Enter The New Folder Name:")
new_folder_name_label.pack(pady=5)
new_folder_name_entry = tk.Entry(root, width=40)
new_folder_name_entry.pack(pady=5)

# Create and place the add logo button
add_logo_button = tk.Button(root, text="Add Logo to Images", command=add_logo)
add_logo_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
