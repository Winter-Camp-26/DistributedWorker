from pathlib import Path

from PIL import Image


def resize_image(payload: dict) -> dict:
    """
    Resize an image according to the job payload.

    Expected payload:
    {
        "image": "/data/input/photo.jpg",
        "width": 800,
        "height": 600
    }

    Returns:
    {
        "output": "/data/output/photo_resized.jpg",
        "width": 800,
        "height": 600
    }
    """

    image_path = payload.get("image")
    width = payload.get("width")
    height = payload.get("height")

    # -------------------------
    # Validate payload
    # -------------------------

    if not image_path:
        raise ValueError("Missing 'image' field")

    if width is None:
        raise ValueError("Missing 'width' field")

    if height is None:
        raise ValueError("Missing 'height' field")

    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("'width' and 'height' must be integers")

    if width <= 0 or height <= 0:
        raise ValueError("'width' and 'height' must be greater than 0")

    # -------------------------
    # Validate input file
    # -------------------------

    input_path = Path(image_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    if not input_path.is_file():
        raise ValueError(
            f"Image path is not a file: {image_path}"
        )

    # -------------------------
    # Prepare output directory
    # -------------------------

    output_dir = Path("/data/output")

    # For local development, allow ./data/output
    if not output_dir.exists():
        output_dir = Path("data/output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        output_dir
        / f"{input_path.stem}_resized{input_path.suffix}"
    )

    # -------------------------
    # Resize image
    # -------------------------

    with Image.open(input_path) as image:

        resized_image = image.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        # JPEG does not support RGBA.
        if (
            output_path.suffix.lower() in [".jpg", ".jpeg"]
            and resized_image.mode in ("RGBA", "LA", "P")
        ):
            resized_image = resized_image.convert("RGB")

        resized_image.save(output_path)

    # -------------------------
    # Return result
    # -------------------------

    return {
        "output": str(output_path),
        "width": width,
        "height": height
    }