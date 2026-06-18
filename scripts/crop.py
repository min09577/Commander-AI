#!/usr/bin/env python3
"""
Commander-AI Smart Template Cropper — only shows what needs cropping.
Automatically picks the right screenshot for each template.
"""

import cv2
import numpy as np
import os, sys, json


def imread_cn(path):
    with open(path, 'rb') as f:
        return cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "..", "assets", "resource", "image")
    sc_dir = "C:/Users/Min/.workbuddy/clipboard-images"
    
    # Screenshot paths
    screenshots = {
        "lobby":        os.path.join(sc_dir, "clipboard-2026-06-17T16-59-06-500Z-c18dcb8c.jpg"),
        "cash_shop":    os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-268Z-2bd5ddf2.jpg"),
        "general_shop": os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-270Z-5a299cd8.jpg"),
        "arena":        os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-272Z-6c58bed5.jpg"),
        "interception": os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-273Z-9cfff50f.jpg"),
        "tower":        os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-275Z-a692abc6.jpg"),
        "outpost":      os.path.join(sc_dir, "clipboard-2026-06-17T17-16-22-278Z-46502c7a.jpg"),
    }
    
    # Template name keywords -> which screenshot they belong to
    CATEGORIES = {
        "lobby":        ["登录", "签到", "扭蛋", "账号", "ENGLISH", "日本语", "繁体", "简体", "公告", 
                         "SUBMENU", "右上角", "确认", "带圈白勾", "圈中的感叹号", "灰色空心", "叉叉",
                         "不再显示", "全部领取", "节日", "抽卡", "招募", "SKIP", "记录播放", "WIFI",
                         "死神的死", "自动选择", "编队", "档案", "白底蓝色", "蓝底白色", "ESC", "复活",
                         "放弃战斗", "不获得", "对话框", "白色", "红框中的0"],
        "cash_shop":    ["付费", "商店", "FREE", "芯尘盒", "简介个性化", "礼物的",
                         "百货", "左上角的百货"],
        "general_shop": ["普通", "百货", "FREE", "芯尘盒", "简介个性化", "礼物的",
                         "一般"],
        "arena":        ["竞技场", "免费", "ON", "OFF", "晋级赛", "应援", "左上角的竞技场"],
        "interception": ["拦截战", "异常拦截", "克拉肯", "镜像容器", "茵迪维利亚", "过激派",
                         "达成阶段", "快速战斗"],
        "tower":        ["无限之塔", "OPEN", "STAGE", "塔内"],
        "outpost":      ["派遣", "咨询", "好友", "领取", "每日任务", "通行证", "前哨基地",
                         "同步器", "循环室", "妮姬", "地面玩法", "协同作战", "单人突击",
                         "个人突击", "进行战斗", "进入战斗", "准备", "开始匹配", "开始模拟",
                         "模拟室", "模拟结束", "大活动", "小活动", "剧情活动", "活动",
                         "推图", "MAX", "1.png", "2.png", "BIOS", "COOP", "GalGame",
                         "Star", "Left", "Right", "Normal", "RAID", "STAGE",
                         "挑战关卡", "活动关卡", "关卡车", "小游戏", "签到印章", "剩余时间",
                         "全部领取的图标", "签到_全部"],
    }
    
    # Load screencaps
    screens = {}
    for name, path in screenshots.items():
        screens[name] = imread_cn(path)
    
    # Load template index
    with open(os.path.join(image_dir, "index.json"), encoding='utf-8') as f:
        index = json.load(f)
    
    # Filter templates: only show [NEED] ones + auto-assign screenshot
    todo = []
    for t in index['templates']:
        tname = t['file']
        tpath = os.path.join(image_dir, tname)
        if os.path.exists(tpath):
            # Check if it's a real crop or a tiny FindText placeholder
            existing = imread_cn(tpath)
            if existing is not None and existing.shape[0] > 30 and existing.shape[1] > 30:
                continue  # Already has a decent crop, skip
        
        # Auto-assign screenshot based on name keywords
        assigned = "lobby"  # default
        for cat, keywords in CATEGORIES.items():
            for kw in keywords:
                if kw in tname:
                    assigned = cat
                    break
            if assigned != "lobby":
                break
        
        todo.append({"name": tname, "screen": assigned, "path": tpath})
    
    print(f"\nTotal templates: {len(index['templates'])}")
    print(f"Already cropped: {len(index['templates']) - len(todo)}")
    print(f"Need cropping: {len(todo)}")
    print()
    
    if len(todo) == 0:
        print("ALL DONE! Every template has been cropped.")
        input("Press Enter...")
        return
    
    # Group by screenshot for summary
    from collections import Counter
    by_screen = Counter(t["screen"] for t in todo)
    print("By screenshot:")
    for s, n in by_screen.most_common():
        print(f"  {s}: {n} templates")
    print()
    
    idx = 0
    while idx < len(todo):
        t = todo[idx]
        screen = screens.get(t["screen"])
        if screen is None:
            idx += 1
            continue
        
        screen_h, screen_w = screen.shape[:2]
        display = screen.copy()
        
        # Draw info
        title = f"[{idx+1}/{len(todo)}] {t['name']}  << {t['screen']} >>"
        cv2.putText(display, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.55, (0, 255, 255), 2)
        cv2.putText(display, "ENTER=save  C=skip  ESC=quit  B=back",
                    (10, screen_h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        cv2.imshow("Commander-AI Smart Cropper", display)
        
        # resize window to fit screen
        cv2.resizeWindow("Commander-AI Smart Cropper", 
                        min(1400, screen_w), min(900, screen_h))
        
        key = cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        
        if key == 27:  # ESC
            break
        elif key == ord('c'):  # skip
            idx += 1
        elif key == ord('b'):  # back
            idx = max(0, idx - 1)
        elif key == 13:  # Enter - use selectROI
            roi = cv2.selectROI("Select region", display, False)
            cv2.destroyWindow("Select region")
            x, y, w, h = roi
            
            if w > 10 and h > 10:
                crop = screen[y:y+h, x:x+w]
                cv2.imwrite(t["path"], crop)
                print(f"  SAVED: {t['name']} ({w}x{h})")
                idx += 1
            else:
                print(f"  SKIP: {t['name']} (no selection)")
                idx += 1
    
    done = sum(1 for t in index['templates'] if os.path.exists(os.path.join(image_dir, t['file'])))
    print(f"\nDone! {done}/{len(index['templates'])} templates cropped.")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
