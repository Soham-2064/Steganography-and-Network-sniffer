import tkinter as tk
from tkinter import filedialog, messagebox
from stegano import lsb
from PIL import Image


def open_image():
    path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.png *.bmp")]
    )
    entry_image_path.delete(0, tk.END)
    entry_image_path.insert(0, path)

def save_image():
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )
    return path

def encode_message():
    image_path = entry_image_path.get()
    message = text_message.get("1.0", tk.END).strip()

    if not image_path or not message:
        messagebox.showwarning("Warning", "Please select image and enter a message.")
        return

    try:
        output_path = save_image()
        secret = lsb.hide(image_path, message)
        secret.save(output_path)
        messagebox.showinfo("Success", f"✅ Message hidden successfully!\nSaved as:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode_message():
    image_path = entry_image_path.get()

    if not image_path:
        messagebox.showwarning("Warning", "Please select image.")
        return

    try:
        hidden_message = lsb.reveal(image_path)
        if hidden_message:
            messagebox.showinfo("Hidden Message", f"🕵️ Hidden message found:\n\n{hidden_message}")
        else:
            messagebox.showinfo("Result", "No hidden message found in this image.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI DESIGN

root = tk.Tk()
root.title("🕵️ Simple Steganography Tool")
root.geometry("420x420")

tk.Label(root, text="Select Image:").pack(pady=5)
entry_image_path = tk.Entry(root, width=45)
entry_image_path.pack(pady=5)
tk.Button(root, text="Browse", command=open_image).pack(pady=5)

tk.Label(root, text="Enter Secret Message:").pack(pady=5)
text_message = tk.Text(root, height=5, width=45)
text_message.pack(pady=5)

tk.Button(root, text="Encode Message", command=encode_message, bg="lightgreen").pack(pady=10)
tk.Button(root, text="Decode Message", command=decode_message, bg="lightblue").pack(pady=10)

tk.Label(root, text="Supports PNG, BMP formats only.", fg="gray").pack(pady=10)

root.mainloop()
