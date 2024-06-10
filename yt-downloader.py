import os
import tkinter as tk
from tkinter import messagebox
import requests
import yt_dlp
import zipfile

def download_video():
    video_link = entry.get()
    output_path = os.path.dirname(os.path.abspath(__file__))
    
    if not os.path.exists("yt-dlp.exe"):
        yt_dlp_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        response = requests.get(yt_dlp_url)
        with open("yt-dlp.exe", "wb") as file:
            file.write(response.content)

    if not os.path.exists("ffmpeg.exe"):
        ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n5.1-latest-win64-gpl-5.1.zip"
        response = requests.get(ffmpeg_url)
        with open("ffmpeg.zip", "wb") as file:
            file.write(response.content)
        with zipfile.ZipFile("ffmpeg.zip", "r") as zip_ref:
            zip_ref.extractall(".")
        ffmpeg_dir = next(dir for dir in os.listdir(".") if dir.startswith("ffmpeg-"))
        os.rename(os.path.join(ffmpeg_dir, "bin", "ffmpeg.exe"), "ffmpeg.exe")
        os.system(f"rmdir /s /q {ffmpeg_dir}")
        os.remove("ffmpeg.zip")

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0"
        }],
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s")
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

    messagebox.showinfo("Download complete", "Video downloaded successfully!")
    window.destroy()

# tk window
# would be nice to let user pick between mp3/mp4 and quality settings 
window = tk.Tk()
window.title("YouTube Video Downloader")
window.geometry("400x150")


label = tk.Label(window, text="Enter the YouTube video link:")
label.pack(pady=10)
entry = tk.Entry(window, width=50)
entry.pack()

# Create the download button
button = tk.Button(window, text="Download", command=download_video)
button.pack(pady=10)

# Start the main event loop
window.mainloop()