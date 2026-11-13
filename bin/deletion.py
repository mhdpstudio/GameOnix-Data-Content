import argparse
from pathlib import Path
from typing import Iterable


IMAGE_FOLDERS = (
    "images/games/posters",
    "images/games/logos",
    "images/games/banners",
    "images/games/ps",
    "videos/pics/webp",
    "images/recharge",
    "images/apps",
    "images/unities",
)
SOURCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".jfif", ".ico", ".avif"}


def find_image_sources(data_directory: Path) -> list[Path]:
    sources: set[Path] = set()
    for relative_folder in IMAGE_FOLDERS:
        folder = data_directory / relative_folder
        if folder.is_dir():
            sources.update(
                file_path
                for file_path in folder.rglob("*")
                if file_path.is_file() and file_path.suffix.lower() in SOURCE_EXTENSIONS
            )
    return sorted(sources)


def delete_converted_sources(source_paths: Iterable[Path]) -> list[Path]:
    sources = list(source_paths)
    for source in sources:
        if source.suffix.lower() not in SOURCE_EXTENSIONS:
            raise ValueError(f"Refusing to delete an unsupported image source: {source}")
        if not source.is_file():
            raise FileNotFoundError(f"Image source disappeared before cleanup: {source}")
        if not source.with_suffix(".webp").is_file():
            raise FileNotFoundError(f"Refusing to delete {source}: its WebP conversion is missing.")

    deleted = []
    failures = []
    for source in sources:
        try:
            source.unlink()
            deleted.append(source)
        except OSError as error:
            failures.append(f"{source}: {error}")
    if failures:
        raise OSError("Some converted source images could not be removed:\n" + "\n".join(failures))
    return deleted


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove source images that already have a WebP copy.")
    parser.add_argument("data_directory", type=Path, help="Path to the GameOnix-Data repository")
    args = parser.parse_args()
    data_directory = args.data_directory.resolve()
    if not data_directory.is_dir():
        parser.error(f"Data directory does not exist: {data_directory}")

    candidates = find_image_sources(data_directory)
    converted = [source for source in candidates if source.with_suffix(".webp").is_file()]
    deleted = delete_converted_sources(converted)
    print(f"Removed {len(deleted)} source image(s) with verified WebP copies.")


if __name__ == "__main__":
    main()
