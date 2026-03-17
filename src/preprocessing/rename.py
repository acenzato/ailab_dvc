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

parser = argparse.ArgumentParser(description='rename files and update labels.csv')
parser.add_argument('input', type=Path, help='Input dataset')

args = parser.parse_args()
input_dir: Path = args.input

input_file = input_dir / 'labels.csv'

output_lines = []
with input_file.open('r') as f:
    for i, line in enumerate(f):
        if i == 0:
            output_lines.append(line)  # header
            continue

        line = line.strip()
        dataset, filename, prefix, label = line.split(',')
        new_filename = f"{i-1:04d}.png"

        filename = str(Path(filename).stem) + '.png'  # Ensure the filename has .png extension
        src_file_path = input_dir / prefix / filename
        src_file_path.rename(src_file_path.parent / new_filename)  # Rename the file
        
        output_lines.append(','.join([dataset, new_filename, prefix, label]) + '\n')

with input_file.open('w') as f:
    f.writelines(output_lines)