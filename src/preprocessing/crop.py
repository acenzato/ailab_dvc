import argparse
from pathlib import Path

from PIL import Image

def crop_square(img: Image.Image) -> Image.Image:
    width, height = img.size
    if width == height:
        return img
    elif width > height:
        left = (width - height) // 2
        right = left + height
        return img.crop((left, 0, right, height))
    else:
        top = (height - width) // 2
        bottom = top + width
        return img.crop((0, top, width, bottom))

parser = argparse.ArgumentParser(description='Unify image format to png')
parser.add_argument('input', type=Path, help='Input image dir')
parser.add_argument('output', type=Path, help='Output image dir')

args = parser.parse_args()
input_dir: Path = args.input
output_dir: Path = args.output

output_dir.mkdir(parents=True, exist_ok=True)
for img_path in input_dir.glob('*'):
    if img_path.is_file():
        img = Image.open(img_path)
        output_path = output_dir / img_path.name
        img = crop_square(img)
        img.save(output_path)