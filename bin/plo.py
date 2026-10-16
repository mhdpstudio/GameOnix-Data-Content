import os
from PIL import Image
import pillow_avif

# =========================
# 🔹 كل المسارات (عادي + recursive)
# =========================
input_folders = [
    {"path": r"E:\Program\Projects\Xhyper\assets\images\games\posters", "recursive": False},
    {"path": r"E:\Program\Projects\Xhyper\assets\images\games\logos", "recursive": False},
    {"path": r"E:\Program\Projects\Xhyper\assets\images\games\banners", "recursive": False},
    {"path": r"E:\Program\Projects\Xhyper\assets\videos\pics\webp", "recursive": False},
    {"path": r"E:\Program\Projects\Xhyper\assets\images\games\ps\banners", "recursive": False},
    {"path": r"E:\Program\Projects\Xhyper\assets\images\games\ps\logos", "recursive": False},
    {"path": r"E:\Program\Projects\Xhyper\assets\images\games\ps\posters", "recursive": False},
    {"path": r"E:\Program\Projects\Xhyper\assets\images\recharge\icons", "recursive": False},
    {"path": r"E:\Program\Projects\Xhyper\assets\images\recharge\images", "recursive": True},
    {"path": r"E:\Program\Projects\Xhyper\assets\images\apps", "recursive": False},

    # 🖥️ Computer

    {"path": r"D:\Documents\Projects\Xhyper\assets\images\games\posters", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\games\logos", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\games\banners", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\videos\pics\webp", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\games\ps\banners", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\games\ps\logos", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\games\ps\posters", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\recharge\icons", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\recharge\images", "recursive": True},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\apps", "recursive": False},
    {"path": r"D:\Documents\Projects\Xhyper\assets\images\unities", "recursive": False},
]

# إزالة limit التحذيري للصور الكبيرة
Image.MAX_IMAGE_PIXELS = None
MAX_DIMENSION = 16383

# الامتدادات المدعومة
SUPPORTED_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".ico",
    ".avif"
)

# =========================
# 🔥 دالة التحويل
# =========================
def convert_image(input_path):
    folder = os.path.dirname(input_path)
    filename = os.path.basename(input_path)

    name_without_ext = os.path.splitext(filename)[0]
    output_path = os.path.join(folder, f"{name_without_ext}.webp")

    # تجاهل لو موجود
    if os.path.exists(output_path):
        print(f"⏭ Skipped: {name_without_ext}.webp")
        return

    try:
        img = Image.open(input_path)

        # إصلاح EXIF Rotation
        try:
            exif = img.getexif()
            orientation = exif.get(274)

            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

        except:
            pass

        # الشفافية
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        # تصغير لو كبير
        if img.width > MAX_DIMENSION or img.height > MAX_DIMENSION:
            img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

        # حفظ WEBP
        save_args = {
            "format": "WEBP",
            "quality": 90,
            "method": 6,
            "optimize": True
        }

        # لو فيه شفافية
        if img.mode == "RGBA":
            save_args["lossless"] = True

        img.save(output_path, **save_args)

        print(f"✔ Converted: {filename} → {name_without_ext}.webp")

    except Exception as e:
        print(f"❌ Error with {filename}: {e}")


# =========================
# 🔄 التشغيل
# =========================
for item in input_folders:
    folder = item["path"]
    recursive = item["recursive"]

    print(f"\n📂 Processing: {folder} (recursive={recursive})")

    if not os.path.exists(folder):
        print("⚠ Folder not found")
        continue

    # 🔹 Recursive
    if recursive:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                    convert_image(os.path.join(root, filename))

    # 🔹 عادي
    else:
        for filename in os.listdir(folder):
            if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                convert_image(os.path.join(folder, filename))

print("\n🔥 All folders done!")