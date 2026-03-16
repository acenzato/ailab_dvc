import argparse
from pathlib import Path

from PIL import Image

parser = argparse.ArgumentParser(description='Unify image format to png')
parser.add_argument('input', type=Path, help='Input image dir')
parser.add_argument('output', type=Path, help='Output image dir')
parser.add_argument('--format', type=str, default='png', help='Output image format')

args = parser.parse_args()
input_dir: Path = args.input
output_dir: Path = args.output
output_format: str = args.format

output_dir.mkdir(parents=True, exist_ok=True)
for img_path in input_dir.glob('*'):
    if img_path.is_file():
        img = Image.open(img_path)
        output_path = output_dir / (img_path.stem + '.' + output_format)
        img.save(output_path)