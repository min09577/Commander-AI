#!/usr/bin/env python3
"""
Extract key templates from fresh NIKKE screenshots.
Uses feature matching to find UI elements.
"""

import cv2
import numpy as np
import os, json, sys


def imread_cn(path):
    with open(path, 'rb') as f:
        return cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)


def multi_scale_match(screen_gray, template_gray, scales=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]):
    """Find template at multiple scales, return best match."""
    best_score = 0
    best_loc = None
    best_scale = 1.0
    best_w, best_h = 0, 0
    
    th, tw = template_gray.shape
    
    for scale in scales:
        new_w = int(tw * scale)
        new_h = int(th * scale)
        if new_w < 20 or new_h < 20:
            continue
        if new_w > screen_gray.shape[1] or new_h > screen_gray.shape[0]:
            continue
        
        scaled = cv2.resize(template_gray, (new_w, new_h))
        result = cv2.matchTemplate(screen_gray, scaled, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val > best_score:
            best_score = max_val
            best_loc = max_loc
            best_scale = scale
            best_w, best_h = new_w, new_h
    
    return best_score, best_loc, best_w, best_h, best_scale


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "..", "assets", "resource", "image")
    
    # NEW screenshots (provided by user)
    screenshots = {
        "lobby":        imread_cn("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-18T07-18-45-432Z-b8104da2.jpg"),
        "general_shop": imread_cn("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-18T07-18-45-435Z-4ea4512f.jpg"),
        "cash_shop":    imread_cn("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-18T07-18-45-437Z-fc3f87ee.jpg"),
        "ark":          imread_cn("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-18T07-18-45-441Z-6e34ddf8.jpg"),
        "tower":        imread_cn("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-18T07-18-45-443Z-4310b2da.jpg"),
        "arena":        imread_cn("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-18T07-18-45-445Z-9100bd59.jpg"),
        "interception": imread_cn("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-18T07-18-45-447Z-9662af31.jpg"),
        "outpost":      imread_cn("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-18T07-18-45-449Z-01c3f9f3.jpg"),
    }
    
    # Check loaded
    for name, img in screenshots.items():
        if img is None:
            print(f"Failed to load {name}")
            return
        print(f"{name}: {img.shape[1]}x{img.shape[0]}")
    
    # Load index
    with open(os.path.join(image_dir, "index.json"), encoding='utf-8') as f:
        index = json.load(f)
    
    # KEY templates we actually need (from pipeline)
    KEY_TEMPLATES = {
        # Lobby
        "白色的叉叉.png": ("lobby", 0.4),
        "不再显示的框.png": ("lobby", 0.4),
        "签到_全部领取.png": ("lobby", 0.5),
        "登录_扭蛋.png": ("lobby", 0.5),
        "节日签到.png": ("lobby", 0.4),
        "ENGLISH.png": ("lobby", 0.6),
        "日本语.png": ("lobby", 0.6),
        "确认.png": ("lobby", 0.5),
        "确认的白色勾.png": ("lobby", 0.5),
        "带圈白勾.png": ("lobby", 0.5),
        "圈中的感叹号.png": ("lobby", 0.5),
        "灰色空心方框.png": ("lobby", 0.5),
        "方舟的图标.png": ("lobby", 0.5),
        "确认的白色勾.png": ("lobby", 0.5),
        "公告的图标.png": ("lobby", 0.4),
        "抽卡_确认.png": ("lobby", 0.5),
        "全部领取的图标.png": ("lobby", 0.5),
        
        # Shop
        "商店的图标.png": ("lobby", 0.5),
        "左上角的百货商店.png": ("general_shop", 0.4),
        "竞技场商店的图标.png": ("general_shop", 0.4),
        "公司武器熔炉.png": ("general_shop", 0.4),
        "代码手册选择宝箱的图标.png": ("general_shop", 0.4),
        "废铁商店的图标.png": ("general_shop", 0.4),
        "FREE.png": ("cash_shop", 0.6),
        "芯尘盒.png": ("general_shop", 0.5),
        "简介个性化礼包.png": ("general_shop", 0.5),
        "礼物的下半.png": ("cash_shop", 0.5),
        "珠宝.png": ("general_shop", 0.5),
        "黄色的礼物图标.png": ("general_shop", 0.4),
        "资源的图标.png": ("general_shop", 0.4),
        "团队合作宝箱图标.png": ("general_shop", 0.4),
        "保养工具箱图标.png": ("general_shop", 0.4),
        "企业精选武装图标.png": ("general_shop", 0.4),
        
        # Arena
        "免费.png": ("arena", 0.6),
        "方舟_竞技场.png": ("arena", 0.5),
        "晋级赛内部的应援.png": ("arena", 0.5),
        "左上角的竞技场.png": ("arena", 0.4),
        
        # Tower
        "无限之塔的无限.png": ("tower", 0.5),
        "无限之塔_OPEN.png": ("tower", 0.5),
        "塔内的无限之塔.png": ("tower", 0.5),
        
        # Interception
        "拦截战.png": ("interception", 0.5),
        "异常拦截_向右的箭头.png": ("interception", 0.4),
        "拦截战_进入战斗的进.png": ("interception", 0.5),
        "克拉肯的克.png": ("interception", 0.5),
        "镜像容器的镜.png": ("interception", 0.5),
        "茵迪维利亚的茵.png": ("interception", 0.5),
        
        # Outpost
        "派遣公告栏最左上角的派遣.png": ("outpost", 0.5),
        "咨询的图标.png": ("outpost", 0.5),
        "好友的图标.png": ("outpost", 0.5),
        "领取.png": ("outpost", 0.5),
        "每日任务_MISSION.png": ("outpost", 0.5),
        "通行证_奖励.png": ("outpost", 0.5),
        "前哨基地的图标.png": ("outpost", 0.5),
    }
    
    print(f"\nProcessing {len(KEY_TEMPLATES)} key templates...\n")
    
    good = 0
    bad = 0
    
    for tname, (screen_name, scale_hint) in KEY_TEMPLATES.items():
        tpath = os.path.join(image_dir, tname)
        screen = screenshots.get(screen_name)
        
        if screen is None:
            print(f"  SKIP: {tname} (no screenshot)")
            bad += 1
            continue
        
        # Load existing template (low-res from FindText)
        template = imread_cn(tpath)
        if template is None:
            print(f"  SKIP: {tname} (no template file)")
            bad += 1
            continue
        
        # Convert to grayscale
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        # Match
        score, loc, w, h, scale = multi_scale_match(screen_gray, template_gray)
        
        if score > 0.4:
            # Extract crop
            x, y = loc
            crop = screen[y:y+h, x:x+w]
            cv2.imwrite(tpath, crop)
            print(f"  OK: {tname} score={score:.2f} {w}x{h} @{screen_name}")
            good += 1
        else:
            print(f"  LOW: {tname} score={score:.2f} (skipped)")
            bad += 1
    
    print(f"\nDone: {good} success, {bad} failed")


if __name__ == "__main__":
    main()
