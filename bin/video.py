import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

# فتح نافذة اختيار ملف
Tk().withdraw()

input_file = askopenfilename(
    title="Select Video File",
    filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov"), ("All files", "*.*")],
)

if not input_file:
    print("❌ No file selected")
    exit()

# تحديد اسم ملف الناتج
folder = os.path.dirname(input_file)
filename = os.path.splitext(os.path.basename(input_file))[0]
output_file = os.path.join(folder, filename + ".webm")

# لو الملف موجود مسبقًا
if os.path.exists(output_file):
    print(f"⏭ Skipped (already exists): {output_file}")
else:
    try:
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-c:v",
            "libvpx-vp9",
            "-crf",
            "30",
            "-b:v",
            "0",
            "-c:a",
            "libopus",
            output_file,
        ]

        subprocess.run(cmd, check=True)
        print(f"✔ Converted: {output_file}")

    except subprocess.CalledProcessError as e:
        print("❌ Error during conversion:", e)

print("🔥 Done!")
