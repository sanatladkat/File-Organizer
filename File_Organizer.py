import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import webbrowser
import logging

# Configure logging
logging.basicConfig(filename='file_organizer.log',
                    level=logging.INFO, format='%(asctime)s - %(message)s')


def confirm_and_organize_desktop():
    confirm = messagebox.askyesno(
        "Confirmation", "Are you sure you want to organize the Desktop folder?")
    if confirm:
        organize_desktop()


def confirm_and_organize_downloads():
    confirm = messagebox.askyesno(
        "Confirmation", "Are you sure you want to organize the Downloads folder?")
    if confirm:
        organize_downloads()


def organize_desktop():
    try:
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        if not os.path.exists(desktop_path):
            raise FileNotFoundError("Desktop folder does not exist")
        organize_folder(desktop_path)
        messagebox.showinfo("Success", "Desktop files organized successfully!")
    except Exception as e:
        messagebox.showerror(
            "Error", f"Error organizing desktop files: {str(e)}")


def organize_downloads():
    try:
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        if not os.path.exists(downloads_path):
            raise FileNotFoundError("Downloads folder does not exist")
        organize_folder(downloads_path)
        messagebox.showinfo(
            "Success", "Downloads files organized successfully!")
    except Exception as e:
        messagebox.showerror(
            "Error", f"Error organizing downloads files: {str(e)}")


def organize_custom_folder():
    try:
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
        if not os.path.exists(folder_path):
            raise FileNotFoundError("Custom folder does not exist")
        organize_folder(folder_path)
        messagebox.showinfo(
            "Success", "Custom folder files organized successfully!")
    except Exception as e:
        messagebox.showerror(
            "Error", f"Error organizing custom folder files: {str(e)}")


def organize_folder(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            if not item.endswith('.lnk'):
                file_type = item.split('.')[-1].lower()
                destination_folder = os.path.join(folder_path, file_type)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                handle_collision(item_path, destination_folder)
                logging.info(f"Moved file: {item_path} to {destination_folder}")


def handle_collision(source_file, destination_folder):
    file_name = os.path.basename(source_file)
    destination_file = os.path.join(destination_folder, file_name)
    if os.path.exists(destination_file):
        choice = messagebox.askyesnocancel("File Collision", f"A file with the name '{file_name}' already exists in the destination folder. What do you want to do? \n\nPress 'Yes' to replace file\nPress 'No' to rename and move file\nPress 'Cancel' to Skip", default="yes")
        if choice is not None:
            if choice:  # Overwrite
                shutil.move(source_file, destination_file)
            else:  # Rename
                file_name, file_extension = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(os.path.join(destination_folder, f"{file_name}_{counter}{file_extension}")):
                    counter += 1
                new_file_name = f"{file_name}_{counter}{file_extension}"
                shutil.move(source_file, os.path.join(destination_folder, new_file_name))
                logging.info(f"Moved file: {source_file} to {os.path.join(destination_folder, new_file_name)}")
    else:
        shutil.move(source_file, destination_file)
        logging.info(f"Moved file: {source_file} to {destination_file}")


def open_github_repo(event):
    webbrowser.open_new("https://github.com/yourusername/yourrepository")


def main():
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("250x200")  # Set the default window size to 400x200 pixels

    # Load custom thumbnail
    #thumbnail = tk.PhotoImage(file="logo.png")
    #root.iconphoto(True, thumbnail)  # Set as application icon

    # Style
    style = ttk.Style()
    style.configure("TButton", padding=6, font=('TkDefaultFont', 10))
    style.configure("TLabel", font=('TkDefaultFont', 11))
    style.configure("TFrame", background="#f0f0f0")

    # Frame for buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    # Buttons for options
    desktop_button = ttk.Button(
        button_frame, text="Organize Desktop", command=confirm_and_organize_desktop)
    desktop_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    downloads_button = ttk.Button(
        button_frame, text="Organize Downloads", command=confirm_and_organize_downloads)
    downloads_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    custom_button = ttk.Button(
        button_frame, text="Organize Custom Folder", command=organize_custom_folder)
    custom_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    # GitHub repository link
    github_label = ttk.Label(
        root, text="GitHub", cursor="hand2", foreground="blue")
    github_label.pack(pady=(5, 5))
    github_label.bind("<Button-1>", open_github_repo)

    root.mainloop()


if __name__ == "__main__":
    main()
