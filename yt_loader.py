import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from os import getcwd, chdir
from ttkthemes import ThemedTk
import threading
import yt_dlp


def start_download():
    threading.Thread(target=download_video).start()

def select_directory():
    folder_path = filedialog.askdirectory()
    dir_label['text'] = f"Current directory: {folder_path}"
    root.update_idletasks()
    try:
        chdir(folder_path)
    except Exception as e:
        messagebox.showerror(f"Cannot access directory\n{e}")

def download_video():
    try:
        url = url_entry.get()
        if not url:
            messagebox.showwarning("Error", "Please, enter a URL.")
            return
        if not "youtube.com/" in url.lower():
            messagebox.showwarning("Error", "Enter a valid YouTube link")
            return

        download_button['text'] = "Loading"
        root.update_idletasks()

        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Video successfuly downloaded!")
        except yt_dlp.DownloadError:
            messagebox.showerror("Error", "Invalid URL")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error occured:\n{str(e)}")
    finally:
        url_entry.delete(0, tk.END)
        download_button.config(text="Download")

root = ThemedTk(theme='plastik')
root.title("YouTube loader")
root.geometry('400x280')
root.resizable(False, False)

head_label = ttk.Label(root, text="Enter a YouTube video URL")
head_label.pack(pady=5)

url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=10)

dir_label = ttk.Label(root, text=f"Current directory: {getcwd()}")
dir_label.pack(pady=10)

directory_button = ttk.Button(root, text="Select directory", command=select_directory)
directory_button.pack(pady=5)

download_button = ttk.Button(root, text="Download", command=start_download)
download_button.pack(pady=20)

root.mainloop()