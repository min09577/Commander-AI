#!/usr/bin/env python3
"""Extract FindText templates from PicLib.ahk and decode to PNG."""

import re
import sys
import os

# Read PicLib.ahk
piclib_path = os.path.join(os.path.dirname(__file__), '../../DoroHelper-AI/lib/PicLib.ahk')
with open(piclib_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all FindText templates
pattern = r'\|<([^>]+)>\*(\d+)\$(\d+)\.([^"\']+)'
matches = re.findall(pattern, content)

output_dir = os.path.join(os.path.dirname(__file__), '../assets/resource/image')
os.makedirs(output_dir, exist_ok=True)

print(f"Found {len(matches)} templates")
print(f"Output directory: {output_dir}")

# Collect template names and stats
template_names = []
for name, scale, width, data in matches:
    template_names.append({
        'name': name.strip(),
        'scale': int(scale),
        'width': int(width),
        'data': data
    })

# Write a manifest file
manifest = os.path.join(output_dir, 'TEMPLATE_MANIFEST.md')
with open(manifest, 'w', encoding='utf-8') as f:
    f.write("# Commander-AI Image Template Manifest\n\n")
    f.write(f"Total templates: {len(template_names)}\n\n")
    f.write("## Status\n\n")
    f.write("| # | Template Name | Scale | Width | Status |\n")
    f.write("|---|--------------|-------|-------|--------|\n")
    for i, t in enumerate(template_names, 1):
        f.write(f"| {i} | {t['name']} | {t['scale']} | {t['width']} | ⏳ Pending |\n")

print(f"Wrote template manifest with {len(template_names)} entries")

# Count by category
categories = {}
for t in template_names:
    name = t['name']
    if '·' in name:
        cat = name.split('·')[0]
    elif name.startswith('<') and '·' in name:
        cat = name.split('·')[0]
    else:
        cat = 'Other'
    categories[cat] = categories.get(cat, 0) + 1

print("\nTemplates by category:")
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")

# Also output a JSON index for the pipeline
import json
index = {
    'total': len(template_names),
    'templates': [{'id': i, 'name': t['name'], 'file': t['name'].replace('·', '_').replace(' ', '_') + '.png'} for i, t in enumerate(template_names, 1)]
}
index_path = os.path.join(output_dir, 'index.json')
with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=2, ensure_ascii=False)
print(f"\nWrote image index JSON: {index_path}")
