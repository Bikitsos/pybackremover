import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttkb
from rembg import remove
from io import BytesIO

opened_image_path = None

def save_image():
    global opened_image_path
    input_path = opened_image_path  # Use the stored filename
    if input_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            with open(input_path, 'rb') as input_file:
                input_image = input_file.read()
                output_image = remove(input_image)
                with open(output_path, 'wb') as output_file:
                    output_file.write(output_image)

def remove_background():
    global opened_image_path
    input_path = opened_image_path  # Use the stored filename
    if input_path:
        with open(input_path, 'rb') as input_file:
            input_image = input_file.read()
            output_image = remove(input_image)
            # Convert the output image data to an Image object
            output_image = Image.open(BytesIO(output_image))
            # Calculate aspect ratio
            aspect_ratio = output_image.width / output_image.height
            new_width = 350
            new_height = round(new_width / aspect_ratio)
            # Resize the image
            output_image = output_image.resize((new_width, new_height))
            # Create a PhotoImage object from the Image object
            photo = ImageTk.PhotoImage(output_image)
            label2.config(image=photo)
            label2.image = photo
    
def open_image():
    global opened_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        opened_image_path = file_path  # Store the filename
        image = Image.open(file_path)
        # Calculate aspect ratio
        aspect_ratio = image.width / image.height
        new_width = 350
        new_height = round(new_width / aspect_ratio)
        # Resize the image
        image = image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        label1.config(image=photo)
        label1.image = photo  # keep a reference to the image

root = tk.Tk()
root.geometry('708x400')
root.title('Background Remover')
root.resizable(False, False)  # Make the window not resizable

style = ttkb.Style('minty')
style.theme_use()

# Create image placeholders
placeholder = ImageTk.PhotoImage(Image.new('RGB', (350, 350)))

# Create buttons
button_open = ttkb.Button(root, text="Open Image", command=open_image)
button_open.grid(row=0, column=0)  # Place the button in the first column

button_remove_bg = ttkb.Button(root, text="Remove Background", command=remove_background)
button_remove_bg.grid(row=0, column=1)  # Place the button in the second column

button_save = ttkb.Button(root, text="Save Image", command=save_image)
button_save.grid(row=0, column=2)  # Place the button in the third column

# Create a frame
frame = tk.Frame(root)
frame.grid(row=1, column=0, columnspan=3)  # Span the frame across all three columns

# Create labels inside the frame
label1 = tk.Label(frame, image=placeholder)
label1.image = placeholder
label1.pack(side="left")  # Place the label on the left side of the frame

label2 = tk.Label(frame, image=placeholder)
label2.image = placeholder
label2.pack(side="right")  # Place the label on the right side of the frame

root.mainloop()