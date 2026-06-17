#!/usr/bin/env python3
"""Download PaddleOCR ONNX models for Commander-AI."""

import os
import sys
import urllib.request

MODELS = {
    "det.onnx": "https://raw.githubusercontent.com/MaaXYZ/MaaCommonAssets/main/OCR/ppocr_v5/zh_cn/det.onnx",
    "rec.onnx": "https://raw.githubusercontent.com/MaaXYZ/MaaCommonAssets/main/OCR/ppocr_v5/zh_cn/rec.onnx",
    "keys.txt": "https://raw.githubusercontent.com/MaaXYZ/MaaCommonAssets/main/OCR/ppocr_v5/zh_cn/keys.txt",
}


def download(url, dest):
    print(f"Downloading {os.path.basename(dest)}...")
    try:
        urllib.request.urlretrieve(url, dest)
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"  OK: {size_mb:.1f} MB")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ocr_dir = os.path.join(base_dir, "..", "assets", "resource", "model", "ocr")
    os.makedirs(ocr_dir, exist_ok=True)

    success = 0
    for filename, url in MODELS.items():
        dest = os.path.join(ocr_dir, filename)
        if download(url, dest):
            success += 1

    print(f"\nDownloaded {success}/{len(MODELS)} files")
    if success == len(MODELS):
        print("All OCR models ready!")
    else:
        print("Some downloads failed. Check network and retry.")
        sys.exit(1)


if __name__ == "__main__":
    main()
