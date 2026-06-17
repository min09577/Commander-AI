#!/usr/bin/env python3
"""Map English template names in pipeline to actual Chinese PNG filenames."""

import json, os

# Semantic mapping from English pipeline names to actual PNG filenames
MAPPING = {
    "login_shiftup_logo.png": "登录_扭蛋.png",
    "shop_cash.png": "商店的图标.png",
    "shop_cash_free.png": "FREE.png",
    "shop_cash_free_stepup.png": "礼物的下半.png",
    "shop_general.png": "左上角的百货商店.png",
    "shop_general_free.png": "FREE.png",
    "shop_general_dust.png": "芯尘盒.png",
    "shop_general_package.png": "简介个性化礼包.png",
    "shop_arena.png": "竞技场商店的图标.png",
    "shop_arena_book.png": "代码手册选择宝箱的图标.png",
    "shop_arena_code_box.png": "代码手册选择宝箱的图标.png",
    "shop_arena_package.png": "简介个性化礼包.png",
    "shop_arena_furnace.png": "公司武器熔炉.png",
    "shop_recycling.png": "废铁商店的图标.png",
    "shop_recycling_gem.png": "珠宝.png",
    "shop_recycling_voucher.png": "黄色的礼物图标.png",
    "shop_recycling_resources.png": "资源的图标.png",
    "shop_recycling_teamwork_box.png": "团队合作宝箱图标.png",
    "shop_recycling_arms.png": "企业精选武装图标.png",
    "simulation_normal.png": "模拟室.png",
    "simulation_overclock.png": "模拟室超频_获得.png",
    "arena_award.png": "免费.png",
    "arena_rookie.png": "方舟_竞技场.png",
    "arena_special.png": "晋级赛内部的应援.png",
    "arena_champion.png": "左上角的竞技场.png",
    "tower_company.png": "无限之塔的无限.png",
    "tower_universal.png": "塔内的无限之塔.png",
    "interception_normal.png": "拦截战.png",
    "interception_anomaly.png": "异常拦截_向右的箭头.png",
    "outpost_dispatch.png": "派遣公告栏最左上角的派遣.png",
    "affinity_consult.png": "咨询的图标.png",
    "friendship_points.png": "好友的图标.png",
    "mail_claim.png": "领取.png",
    "mission_claim.png": "每日任务_MISSION.png",
    "pass_claim.png": "通行证_奖励.png",
    "coordinated_operation.png": "协同作战_捍卫者.png",
    "solo_raid_daily.png": "单人突击_挑战.png",
    "story_mode.png": "记录播放的播放.png",
    "instant_burst.png": "MAX.png",
    "campaign_mode.png": "推图_放大镜.png",
}

# Load pipeline JSONs
base_dir = os.path.dirname(os.path.abspath(__file__))
pipeline_dir = os.path.join(base_dir, "..", "assets", "resource", "pipeline")

for pipe_name in ["Daily.json", "Tools.json"]:
    pipe_path = os.path.join(pipeline_dir, pipe_name)
    with open(pipe_path, encoding="utf-8") as f:
        pipeline = json.load(f)
    
    updated = 0
    for task_name, node in pipeline.items():
        if "template" in node:
            old = node["template"]
            if old in MAPPING:
                node["template"] = MAPPING[old]
                updated += 1
            else:
                print(f"  WARNING: No mapping for {old}")
    
    with open(pipe_path, "w", encoding="utf-8") as f:
        json.dump(pipeline, f, indent=4, ensure_ascii=False)
    
    print(f"{pipe_name}: Updated {updated} template references")

# Verify
print("\nVerifying...")
image_dir = os.path.join(base_dir, "..", "assets", "resource", "image")
png_files = set(f for f in os.listdir(image_dir) if f.endswith(".png"))

for pipe_name in ["Daily.json", "Tools.json"]:
    pipe_path = os.path.join(pipeline_dir, pipe_name)
    with open(pipe_path, encoding="utf-8") as f:
        pipeline = json.load(f)
    
    missing = []
    for task_name, node in pipeline.items():
        if "template" in node:
            if node["template"] not in png_files:
                missing.append(node["template"])
    
    if missing:
        print(f"{pipe_name}: {len(missing)} MISSING templates")
    else:
        print(f"{pipe_name}: All templates found!")
