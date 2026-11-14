import argparse
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageOps

try:
    import pillow_avif  # noqa: F401
except ImportError:
    pillow_avif = None

from deletion import delete_converted_sources, find_image_sources


MAX_DIMENSION = 16383


def convert_image(source: Path) -> Path:
    output = source.with_suffix(".webp")
    temporary = output.with_name(f"{output.stem}.{os.getpid()}.tmp.webp")
    try:
        with Image.open(source) as opened:
            image = ImageOps.exif_transpose(opened)
            has_alpha = image.mode in ("RGBA", "LA") or (
                image.mode == "P" and "transparency" in image.info
            )
            image = image.convert("RGBA" if has_alpha else "RGB")
            if image.width > MAX_DIMENSION or image.height > MAX_DIMENSION:
                image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)

            save_options = {"format": "WEBP", "quality": 90, "method": 6}
            if has_alpha:
                save_options["lossless"] = True
            image.save(temporary, **save_options)
        os.replace(temporary, output)
        return output
    finally:
        if temporary.exists():
            temporary.unlink()


def run(data_directory: Path, keep_sources: tuple[Path, ...] = ()) -> dict[str, list[str]]:
    data_directory = data_directory.resolve()
    if not data_directory.is_dir():
        raise FileNotFoundError(f"Data directory does not exist: {data_directory}")

    sources = find_image_sources(data_directory)
    output_owners: dict[str, Path] = {}
    for source in sources:
        output_key = str(source.with_suffix(".webp")).casefold()
        previous = output_owners.get(output_key)
        if previous is not None:
            raise ValueError(
                f"Image filename collision: {previous.name} and {source.name} "
                f"would both become {source.stem}.webp. No source images were removed."
            )
        output_owners[output_key] = source

    converted = []
    for source in sources:
        try:
            output = convert_image(source)
        except Exception as error:
            raise RuntimeError(
                f"Could not convert {source}. Source images were kept; cleanup was not run. {error}"
            ) from error
        converted.append(output)
        print(f"Converted {source.relative_to(data_directory)}", file=sys.stderr)

    protected_sources = {source.resolve() for source in keep_sources}
    deleted = delete_converted_sources(
        source for source in sources if source.resolve() not in protected_sources
    )
    return {
        "converted": [path.relative_to(data_directory).as_posix() for path in converted],
        "deleted": [path.relative_to(data_directory).as_posix() for path in deleted],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert GameOnix image assets to WebP, then remove converted source files."
    )
    parser.add_argument("data_directory", type=Path, help="Path to the GameOnix-Data repository")
    parser.add_argument(
        "--keep-source",
        action="append",
        type=Path,
        default=[],
        help="Keep a selected source file until the GitHub publish is confirmed.",
    )
    args = parser.parse_args()
    try:
        report = run(args.data_directory, tuple(args.keep_source))
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
    print(json.dumps(report))


if __name__ == "__main__":
    main()
