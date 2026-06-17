#!/usr/bin/env python3
"""
FindText PicLib Decoder
Converts FindText encoded templates from PicLib.ahk to PNG images for MaaFramework.

FindText encoding:
  name*scale$width.base64data

Where:
  - scale: display scale factor (100 = 1x, 200 = 2x)
  - width: logical pixel width  
  - base64data: custom Base64 bitmap (chars "0123456789+/A-Za-z")
"""

import re
import os
import struct
import zlib
from PIL import Image

# FindText character mapping (standard Base64 but with specific ordering)
CHARS = "0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
CHAR_TO_INDEX = {c: i for i, c in enumerate(CHARS)}


def decode_findtext(encoded_str):
    """Decode FindText base64 string to list of bits (1=foreground, 0=background)."""
    bits = []
    for c in encoded_str:
        if c not in CHAR_TO_INDEX:
            continue
        i = CHAR_TO_INDEX[c]
        # Extract 6 bits from MSB to LSB
        for bit_pos in range(5, -1, -1):
            bits.append((i >> bit_pos) & 1)
    return bits


def bits_to_image(bits, width, height, scale=100):
    """Convert bit list to PIL Image."""
    scale_factor = scale / 100.0
    
    # Logical size
    logical_width = width
    logical_height = height
    
    # Create image at logical resolution
    img = Image.new('L', (logical_width, logical_height), 255)
    pixels = img.load()
    
    for y in range(logical_height):
        for x in range(logical_width):
            idx = y * logical_width + x
            if idx < len(bits):
                # 1 = black (foreground), 0 = white (background)
                pixels[x, y] = 0 if bits[idx] else 255
            else:
                pixels[x, y] = 255
    
    # Scale up if needed
    if scale_factor != 1.0:
        new_w = int(logical_width * scale_factor)
        new_h = int(logical_height * scale_factor)
        img = img.resize((new_w, new_h), Image.NEAREST)
    
    return img


def parse_template(line):
    """Parse a FindText PicLib template line.
    Returns (name, scale, width, data, height) or None if not a template.
    """
    pattern = r'\|<([^>]+)>\*(\d+)\$(\d+)\.([^\s"\']+)'
    match = re.search(pattern, line)
    if not match:
        return None
    
    name = match.group(1).strip()
    scale = int(match.group(2))
    width = int(match.group(3))
    data = match.group(4)
    
    bits = decode_findtext(data)
    height = len(bits) // width if width > 0 else 0
    
    return name, scale, width, data, height


def safe_filename(name):
    """Convert template name to safe filename."""
    # Replace special characters
    name = name.replace('·', '_').replace(' ', '_')
    name = name.replace('/', '_').replace('\\', '_')
    name = name.replace(':', '_').replace('*', '_')
    name = name.replace('?', '_').replace('"', '_')
    name = name.replace('<', '_').replace('>', '_')
    name = name.replace('|', '_')
    return name


def main():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    piclib_path = os.path.join(project_root, '..', 'DoroHelper-AI', 'lib', 'PicLib.ahk')
    output_dir = os.path.join(base_dir, '..', 'assets', 'resource', 'image')
    os.makedirs(output_dir, exist_ok=True)
    
    # Read PicLib
    with open(piclib_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Parse all templates
    templates = []
    for line in lines:
        result = parse_template(line)
        if result:
            templates.append(result)
    
    print(f"Found {len(templates)} templates")
    
    # Decode and save
    success = 0
    fail = 0
    failed_templates = []
    
    for name, scale, width, data, height in templates:
        try:
            bits = decode_findtext(data)
            if height == 0:
                print(f"  SKIP: {name} (zero height)")
                fail += 1
                failed_templates.append(name)
                continue
            
            img = bits_to_image(bits, width, height, scale)
            filename = safe_filename(name) + '.png'
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, 'PNG')
            success += 1
            
            if success <= 10 or success % 20 == 0:
                print(f"  OK: {name} -> {filename} ({width}x{height}, scale={scale})")
                
        except Exception as e:
            print(f"  FAIL: {name} -> {e}")
            fail += 1
            failed_templates.append(name)
    
    print(f"\nDecoded: {success} success, {fail} failed")
    if failed_templates:
        print(f"Failed: {failed_templates[:10]}...")
    
    # Verify some outputs
    png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
    print(f"\nTotal PNG files in output: {len(png_files)}")
    
    # Print first few files
    for f in sorted(png_files)[:5]:
        filepath = os.path.join(output_dir, f)
        size = os.path.getsize(filepath)
        print(f"  {f}: {size} bytes")


if __name__ == '__main__':
    main()
