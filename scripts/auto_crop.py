#!/usr/bin/env python3
"""
FULLY AUTOMATIC template generator.
Detects NIKKE UI elements from screenshots using color/edge analysis.
Zero manual work needed.
"""

import cv2
import numpy as np
import os, json, sys


def imread_cn(path):
    with open(path, 'rb') as f:
        return cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)


def detect_red_dots(img):
    """Detect red notification dots (NIKKE signature UI element)."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Red range (two ranges due to HSV wrap-around)
    lower1 = np.array([0, 150, 100])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 150, 100])
    upper2 = np.array([180, 255, 255])
    
    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [(cv2.boundingRect(c)) for c in contours if cv2.contourArea(c) > 10]


def detect_gold_buttons(img):
    """Detect gold/yellow elements (NIKKE buttons, icons, FREE tags)."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Gold/yellow range
    lower = np.array([15, 80, 100])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    
    # Find connected regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [(cv2.boundingRect(c)) for c in contours if 500 < cv2.contourArea(c) < 80000]


def detect_white_text_boxes(img):
    """Detect bright rectangular areas (text labels, buttons)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bright = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Dilate to connect nearby bright pixels
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(bright, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [(cv2.boundingRect(c)) for c in contours if 100 < cv2.contourArea(c) < 50000]


def detect_all_ui(img):
    """Combine all detection methods, deduplicate, return unique regions."""
    all_regions = []
    
    for method, regions in [("red_dot", detect_red_dots(img)),
                             ("gold", detect_gold_buttons(img)),
                             ("white", detect_white_text_boxes(img))]:
        for (x, y, w, h) in regions:
            if 5 < w < img.shape[1] and 5 < h < img.shape[0]:
                all_regions.append((x, y, w, h, method))
    
    # Merge overlapping regions
    if not all_regions:
        return []
    
    # Sort by area descending
    all_regions.sort(key=lambda r: -r[2]*r[3])
    
    merged = []
    used = set()
    for i, (x1, y1, w1, h1, m1) in enumerate(all_regions):
        if i in used:
            continue
        # Merge with overlapping regions
        x2, y2, w2, h2 = x1, y1, w1, h1
        for j, (xj, yj, wj, hj, mj) in enumerate(all_regions[i+1:], i+1):
            if j in used:
                continue
            # Check overlap
            ox = max(0, min(x2+w2, xj+wj) - max(x2, xj))
            oy = max(0, min(y2+h2, yj+hj) - max(y2, yj))
            overlap = ox * oy
            area_j = wj * hj
            if overlap > 0.5 * area_j:  # >50% overlap
                used.add(j)
                x2 = min(x2, xj)
                y2 = min(y2, yj)
                x2_end = max(x2 + w2, xj + wj)
                y2_end = max(y2 + h2, yj + hj)
                w2 = x2_end - x2
                h2 = y2_end - y2
        
        merged.append((x1, y1, w1, h1, m1))
        used.add(i)
    
    return merged


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "..", "assets", "resource", "image")
    sc_dir = "C:/Users/Min/.workbuddy/clipboard-images"
    
    # All screenshots to process
    screenshot_files = [
        ("lobby",        os.path.join(sc_dir, "clipboard-2026-06-17T16-59-06-500Z-c18dcb8c.jpg")),
        ("cash_shop",    os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-268Z-2bd5ddf2.jpg")),
        ("general_shop", os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-270Z-5a299cd8.jpg")),
        ("arena",        os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-272Z-6c58bed5.jpg")),
        ("interception", os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-273Z-9cfff50f.jpg")),
        ("tower",        os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-275Z-a692abc6.jpg")),
        ("outpost",      os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-278Z-46502c7a.jpg")),
    ]
    
    total = 0
    
    for screen_name, screen_path in screenshot_files:
        img = imread_cn(screen_path)
        if img is None:
            continue
        
        print(f"\n{screen_name}: {img.shape[1]}x{img.shape[0]}")
        regions = detect_all_ui(img)
        print(f"  Detected {len(regions)} UI elements")
        
        # Generate a debug image with boxes
        debug = img.copy()
        for i, (x, y, w, h, method) in enumerate(regions):
            colors = {"red_dot": (0, 0, 255), "gold": (0, 255, 255), "white": (255, 255, 255)}
            color = colors.get(method, (0, 255, 0))
            cv2.rectangle(debug, (x, y), (x+w, y+h), color, 2)
            
            # Save crop
            crop = img[y:y+h, x:x+w]
            fname = f"auto_{screen_name}_{i:02d}_{w}x{h}.png"
            fpath = os.path.join(image_dir, fname)
            cv2.imwrite(fpath, crop)
            total += 1
        
        # Save debug overlay
        debug_path = os.path.join(image_dir, f"DEBUG_{screen_name}.png")
        cv2.imwrite(debug_path, debug)
        print(f"  Debug overlay: DEBUG_{screen_name}.png")
    
    print(f"\nTotal auto-cropped: {total}")
    print(f"Debug overlays saved to assets/resource/image/DEBUG_*.png")
    print("Open the DEBUG images to see what was detected (red=notification, yellow=gold UI, white=bright text)")


if __name__ == "__main__":
    main()
