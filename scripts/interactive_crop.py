#!/usr/bin/env python3
"""
Semi-automated template cropper for Commander-AI.
Shows NIKKE screenshots and lets you select regions to crop as templates.

Controls:
  - Click and drag to select a region
  - Press 's' to save the crop as the current template
  - Press 'n' to skip current template
  - Press 'q' to quit

Templates are saved to assets/resource/image/
"""

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import matplotlib.patches as patches
import cv2
import numpy as np
import os
import json
import sys


def imread_cn(path):
    """Read image with Chinese filename support."""
    with open(path, 'rb') as f:
        return cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)


def onselect(eclick, erelease):
    """Called when user selects a rectangle."""
    global current_rect
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)
    current_rect = (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def on_key(event):
    """Handle keyboard events."""
    global current_idx, current_rect, current_screenshot, template_list, image_dir, ax, fig
    
    if event.key == 'q':
        print("\nExiting...")
        plt.close()
        sys.exit(0)
    
    elif event.key == 'n' or event.key == 'right':
        current_idx = (current_idx + 1) % len(template_list)
        current_rect = None
        show_template()
    
    elif event.key == 'p' or event.key == 'left':
        current_idx = (current_idx - 1) % len(template_list)
        current_rect = None
        show_template()
    
    elif event.key == 's' and current_rect is not None:
        x, y, w, h = current_rect
        if w < 5 or h < 5:
            print("Selection too small, ignored.")
            return
        
        tname = template_list[current_idx]['file']
        tpath = os.path.join(image_dir, tname)
        
        crop = current_screenshot[y:y+h, x:x+w]
        cv2.imwrite(tpath, crop)
        print(f"  Saved: {tname} ({w}x{h})")
        
        # Move to next
        current_idx = (current_idx + 1) % len(template_list)
        current_rect = None
        show_template()
    
    elif event.key == 'd':
        # Delete current selection
        current_rect = None
        show_template()
    
    elif event.key == 'h':
        print("\n=== Help ===")
        print("  Drag: select region")
        print("  s:    save crop")
        print("  n/p:  next/previous template")
        print("  d:    deselect")
        print("  h:    help")
        print("  q:    quit")
        print()


def show_template():
    """Display current screenshot with template info overlay."""
    global current_rect, current_idx, current_screenshot, template_list, ax, fig
    
    ax.clear()
    
    t = template_list[current_idx]
    tname = t['file']
    
    # Check if template already exists
    tpath = os.path.join(image_dir, tname)
    exists = os.path.exists(tpath)
    
    # Display screenshot
    ax.imshow(cv2.cvtColor(current_screenshot, cv2.COLOR_BGR2RGB))
    
    # Title
    status = "[EXISTS]" if exists else "[NEW]"
    color = 'green' if exists else 'red'
    ax.set_title(f"{current_idx+1}/{len(template_list)}: {tname} {status}\n"
                 f"s=save | n=next | p=prev | q=quit | h=help",
                 fontsize=10, color=color)
    
    # Draw existing selection
    if current_rect is not None:
        x, y, w, h = current_rect
        rect = patches.Rectangle((x, y), w, h, linewidth=2,
                                  edgecolor='lime', facecolor='none')
        ax.add_patch(rect)
    
    # If template exists, show it as thumbnail in corner
    if exists:
        existing = imread_cn(tpath)
        if existing is not None:
            eh, ew = existing.shape[:2]
            thumb_h = min(120, eh)
            thumb_w = int(ew * thumb_h / eh)
            thumb = cv2.resize(existing, (thumb_w, thumb_h))
            # Place in bottom-right corner
            ax_thumb = fig.add_axes([0.78, 0.02, 0.2, 0.2])
            ax_thumb.imshow(cv2.cvtColor(thumb, cv2.COLOR_BGR2RGB))
            ax_thumb.set_title(f"{ew}x{eh}", fontsize=8)
            ax_thumb.axis('off')
    
    fig.canvas.draw_idle()


def main():
    global current_idx, current_rect, current_screenshot, template_list, image_dir, ax, fig
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "..", "assets", "resource", "image")
    
    # Load template list from index
    index_path = os.path.join(image_dir, "index.json")
    with open(index_path, encoding='utf-8') as f:
        index = json.load(f)
    
    template_list = index['templates']
    
    # Load screenshot - ask which one
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--screen', type=int, default=1, help='Screenshot number (1-6)')
    args = parser.parse_args()
    
    screenshot_dir = "C:/Users/Min/.workbuddy/clipboard-images"
    screenshots = sorted([f for f in os.listdir(screenshot_dir) if f.startswith("clipboard-2026-06-17T17-1") and f.endswith('.jpg')])
    
    if not screenshots:
        print("No screenshots found in clipboard directory!")
        sys.exit(1)
    
    choice = min(max(args.screen - 1, 0), len(screenshots) - 1)
    
    screenshot_path = os.path.join(screenshot_dir, screenshots[choice])
    current_screenshot = imread_cn(screenshot_path)
    
    if current_screenshot is None:
        print(f"Failed to load screenshot: {screenshot_path}")
        sys.exit(1)
    
    print(f"\nLoaded: {screenshots[choice]} ({current_screenshot.shape[1]}x{current_screenshot.shape[0]})")
    print(f"Templates: {len(template_list)}")
    print(f"\nControls:")
    print(f"  Drag: select region  |  s: save crop")
    print(f"  n: next template     |  p: previous template")
    print(f"  d: deselect          |  h: help")
    print(f"  q: quit")
    print(f"\nGreen title = template already exists, Red = needs cropping")
    print()
    
    # Setup matplotlib
    fig, ax = plt.subplots(figsize=(14, 9))
    plt.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.02)
    
    # Rectangle selector
    rs = RectangleSelector(ax, onselect, useblit=True,
                          button=[1], minspanx=5, minspany=5,
                          spancoords='pixels', interactive=True)
    
    # Disable default matplotlib shortcuts (especially 's' for save)
    plt.rcParams['keymap.save'] = ''
    plt.rcParams['keymap.fullscreen'] = ''
    plt.rcParams['keymap.quit'] = ''
    
    # Keyboard handler
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    # Start with first template
    current_idx = 0
    current_rect = None
    show_template()
    
    plt.show()


if __name__ == "__main__":
    main()
