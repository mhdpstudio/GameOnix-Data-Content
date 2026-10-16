import os

# =========================
# 🔹 المسارات (عادي + recursive)
# =========================
folders = [
    {
        "path": r"E:\Program\Projects\Xhyper\assets\images\games\posters",
        "recursive": False,
    },
    {
        "path": r"E:\Program\Projects\Xhyper\assets\images\games\logos",
        "recursive": False,
    },
    {
        "path": r"E:\Program\Projects\Xhyper\assets\images\games\banners",
        "recursive": False,
    },
    {"path": r"E:\Program\Projects\Xhyper\assets\videos\pics\webp", "recursive": False},
    {
        "path": r"E:\Program\Projects\Xhyper\assets\images\games\ps\banners",
        "recursive": False,
    },
    {
        "path": r"E:\Program\Projects\Xhyper\assets\images\games\ps\logos",
        "recursive": False,
    },
    {
        "path": r"E:\Program\Projects\Xhyper\assets\images\games\ps\posters",
        "recursive": False,
    },
    {
        "path": r"E:\Program\Projects\Xhyper\assets\images\recharge\icons",
        "recursive": False,
    },
    # 🔥 ده recursive (يدخل كل الفولدرات)
    {
        "path": r"E:\Program\Projects\Xhyper\assets\images\recharge\images",
        "recursive": True,
    },
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

# 🔹 الامتدادات اللي هتتمسح
extensions_to_delete = (".png", ".jpg", ".jpeg", ".ico", ".avif")


# =========================
# 🔥 دالة الحذف
# =========================
def delete_file(file_path):
    filename = os.path.basename(file_path)

    try:
        os.remove(file_path)
        print(f"🗑 Deleted: {filename}")
    except Exception as e:
        print(f"❌ Error deleting {filename}: {e}")


# =========================
# 🔄 التشغيل
# =========================
for item in folders:
    folder = item["path"]
    recursive = item["recursive"]

    print(f"\n📂 Cleaning: {folder} (recursive={recursive})")

    if not os.path.exists(folder):
        print(f"⚠ Folder not found")
        continue

    # 🔹 لو recursive
    if recursive:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith(extensions_to_delete):
                    delete_file(os.path.join(root, filename))

    # 🔹 لو عادي
    else:
        for filename in os.listdir(folder):
            if filename.lower().endswith(extensions_to_delete):
                delete_file(os.path.join(folder, filename))


print("\n🔥 Cleanup done!")
