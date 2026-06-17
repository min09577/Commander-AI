#!/usr/bin/env python3
"""Multi-scale template matcher: find UI elements in high-res screenshots using low-res FindText templates."""

import cv2
import numpy as np
import os
import glob
import json

# Screenshot mapping: which screenshot likely contains which templates
SCREENSHOTS = {
    "shop": glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-268Z-*.jpg")[0] if glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-268Z-*.jpg") else None,
    "general_shop": glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-270Z-*.jpg")[0] if glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-270Z-*.jpg") else None,
    "arena": glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-272Z-*.jpg")[0] if glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-272Z-*.jpg") else None,
    "interception": glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-273Z-*.jpg")[0] if glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-273Z-*.jpg") else None,
    "tower": glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-275Z-*.jpg")[0] if glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-275Z-*.jpg") else None,
    "outpost": glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-278Z-*.jpg")[0] if glob.glob("C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T17-16-22-278Z-*.jpg") else None,
    "lobby": "C:/Users/Min/.workbuddy/clipboard-images/clipboard-2026-06-17T16-59-06-500Z-c18dcb8c.jpg",
}

# Which templates to try matching on which screenshots
TEMPLATE_TARGETS = {
    "shop": ["商店的图标.png", "FREE.png", "礼物的下半.png", "芯尘盒.png", "简介个性化礼包.png",
             "竞技场商店的图标.png", "公司武器熔炉.png", "代码手册选择宝箱的图标.png",
             "废铁商店的图标.png", "珠宝.png", "黄色的礼物图标.png", "资源的图标.png",
             "团队合作宝箱图标.png", "保养工具箱图标.png", "企业精选武装图标.png"],
    "general_shop": ["FREE.png", "芯尘盒.png", "简介个性化礼包.png"],
    "arena": ["免费.png", "方舟_竞技场.png", "晋级赛内部的应援.png", "左上角的竞技场.png"],
    "interception": ["拦截战.png", "异常拦截_向右的箭头.png", "拦截战_进入战斗的进.png"],
    "tower": ["无限之塔的无限.png", "塔内的无限之塔.png", "无限之塔_OPEN.png"],
    "outpost": ["派遣公告栏最左上角的派遣.png", "咨询的图标.png", "好友的图标.png", "领取.png",
               "每日任务_MISSION.png", "通行证_奖励.png", "前哨基地的图标.png"],
    "lobby": ["登录_扭蛋.png", "商店的图标.png", "方舟的图标.png", "确认.png", "确认的白色勾.png",
              "带圈白勾.png", "圈中的感叹号.png"],
}


def multi_scale_match(screen, template, scales=[0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]):
    """Try template matching at multiple scales, return best match."""
    best_score = 0
    best_scale = 1.0
    best_loc = (0, 0)
    best_size = (0, 0)
    
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    th, tw = template.shape[:2]
    
    for scale in scales:
        new_w = int(tw * scale)
        new_h = int(th * scale)
        if new_w < 5 or new_h < 5 or new_w > screen.shape[1] or new_h > screen.shape[0]:
            continue
        
        scaled = cv2.resize(template, (new_w, new_h))
        result = cv2.matchTemplate(screen_gray, cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY) if len(scaled.shape) == 3 else scaled,
                                   cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val > best_score:
            best_score = max_val
            best_scale = scale
            best_loc = max_loc
            best_size = (new_w, new_h)
    
    return best_score, best_scale, best_loc, best_size


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "..", "assets", "resource", "image")
    
    matches = []
    
    for screen_name, screen_path in SCREENSHOTS.items():
        if not screen_path or not os.path.exists(screen_path):
            continue
        
        screen = cv2.imread(screen_path)
        if screen is None:
            continue
        
        # Get list of templates to try
        targets = TEMPLATE_TARGETS.get(screen_name, [])
        
        for tname in targets:
            tpath = os.path.join(image_dir, tname)
            if not os.path.exists(tpath):
                continue
            
            template = cv2.imread(tpath)
            if template is None:
                continue
            
            score, scale, loc, size = multi_scale_match(screen, template)
            status = "HIT" if score > 0.5 else "LOW" if score > 0.3 else "MISS"
            
            print(f"  [{status}] {tname} on {screen_name}: scale={scale:.1f}x score={score:.2f} @ ({loc[0]},{loc[1]})")
            
            if score > 0.3:
                matches.append({
                    "template": tname,
                    "screen": screen_name,
                    "score": float(score),
                    "scale": float(scale),
                    "x": int(loc[0]),
                    "y": int(loc[1]),
                    "w": int(size[0]),
                    "h": int(size[1])
                })
    
    # Save match results
    results_path = os.path.join(image_dir, "match_results.json")
    with open(results_path, "w") as f:
        json.dump({"matches": matches, "total": len(matches)}, f, indent=2)
    
    good = sum(1 for m in matches if m["score"] > 0.5)
    print(f"\nResults: {good}/{len(matches)} good matches saved to {results_path}")


if __name__ == "__main__":
    main()
