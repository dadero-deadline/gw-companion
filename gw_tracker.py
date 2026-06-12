from http.server import HTTPServer, SimpleHTTPRequestHandler
import openpyxl
import sys
import os
import json
sys.path.insert(0, 'data')

from elite_skills import ELITE_SKILLS
from heroes import HEROES, HERO_PROFESSIONS, HERO_ARMOR
from unique_items import UNIQUE_QUEST_ITEMS, ITEM_CATEGORIES, PRE_SEARING_REWARDS, GREEN_UNIQUES, HOM_WEAPON_SETS
from elite_content import ELITE_MISSIONS, EOTN_DUNGEONS, DUNGEON_REGIONS, CAMPAIGN_ICONS
from vanquishes import ALL_VANQUISHES, VANQUISH_REGIONS, PROPHECIES_VANQUISHES, FACTIONS_VANQUISHES, NIGHTFALL_VANQUISHES, EOTN_VANQUISHES
from missions import ALL_MISSIONS, MISSION_REGIONS, PROPHECIES_MISSIONS, FACTIONS_MISSIONS, NIGHTFALL_MISSIONS
from armor_sets import ALL_ARMOR, HOM_ARMOR, ARMOR_ICONS, CORE_ARMOR, PROPHECIES_ARMOR, FACTIONS_ARMOR, NIGHTFALL_ARMOR, EOTN_ARMOR, STANDALONE_PIECES
from minipets import ALL_MINIS, RARITY_COLORS, YEAR1_MINIS, YEAR2_MINIS, YEAR3_MINIS, YEAR4_MINIS, YEAR5_MINIS, INGAME_MINIS, FESTIVAL_MINIS
from daily_quests import ZAISHEN_MISSIONS, ZAISHEN_BOUNTIES, ZAISHEN_VANQUISHES, ZAISHEN_COMBAT, VANGUARD_QUESTS, ZAISHEN_MISSION_START, ZAISHEN_BOUNTY_START, ZAISHEN_VANQUISH_START, ZAISHEN_COMBAT_START
from outposts import OUTPOSTS
from collectibles import MINIATURES, MENAGERIE
from non_elite_skills import NON_ELITE_SKILLS
from cartographer import CARTOGRAPHER, CARTOGRAPHER_TOTAL
import urllib.request, re, urllib.parse

# Reforged Mode content: quests added by the Guild Wars Reforged overhaul.
# Drives the inline "Reforged Mode" badge in the quest name cell (Phase 1) and,
# in Phase 2, data-reforged="1" on these rows for the optional toggle.
REFORGED_QUEST_IDS = {
    "pre_68", "pre_69", "pre_70", "pre_71", "pre_72",
    "post_64", "post_65", "post_66", "post_67",
    "kryta_33",
}

# Simple helper to fetch OpenGraph image from GW wiki hero page
_OG_IMG_CACHE = {}
def get_wiki_og_image(slug):
    if slug in _OG_IMG_CACHE:
        return _OG_IMG_CACHE[slug]
    url = f'https://wiki.guildwars.com/wiki/{slug}'
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            html = resp.read().decode('utf-8', 'ignore')
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if m:
            _OG_IMG_CACHE[slug] = m.group(1)
            return _OG_IMG_CACHE[slug]
    except Exception:
        pass
    _OG_IMG_CACHE[slug] = None
    return None

# Prefer the hero page's infobox image (typically a clean full-body render)
_INFOBOX_IMG_CACHE = {}
def get_wiki_infobox_image(slug):
    if slug in _INFOBOX_IMG_CACHE:
        return _INFOBOX_IMG_CACHE[slug]
    url = f'https://wiki.guildwars.com/wiki/{slug}'
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            html = resp.read().decode('utf-8', 'ignore')
        # Try to find a File: link that matches the slug first
        # Example: href="/wiki/File:Gwen.jpg"
        pat_slug = rf'href="/wiki/File:{re.escape(slug)}[^"\s]*\.(?:jpg|png|gif)"'
        m = re.search(pat_slug, html, flags=re.IGNORECASE)
        if not m:
            # Fallback: first image File: reference on the page
            m = re.search(r'href="/wiki/File:([^"\s]+\.(?:jpg|png|gif))"', html, flags=re.IGNORECASE)
            if m:
                file_name = m.group(1)
                _INFOBOX_IMG_CACHE[slug] = f'https://wiki.guildwars.com/wiki/Special:FilePath/{file_name}'
                return _INFOBOX_IMG_CACHE[slug]
        else:
            href = m.group(0)
            file_name = href.split('/wiki/File:')[-1].split('"')[0]
            _INFOBOX_IMG_CACHE[slug] = f'https://wiki.guildwars.com/wiki/Special:FilePath/{file_name}'
            return _INFOBOX_IMG_CACHE[slug]
    except Exception:
        pass
    _INFOBOX_IMG_CACHE[slug] = None
    return None

# Explicit overrides for tricky hero pages
HERO_IMAGE_OVERRIDES = {
    'M.O.X.': 'M.O.X.jpg',
    'Zei_Ri': 'Initiate_Zei_Ri.jpg',
}

COMMON_SKILL_ICON = "https://wiki.guildwars.com/images/3/33/Any-tango-icon-20.png"  # GWW "Any" tango icon (verified)

def prof_icon_img(prof, px=18):
    """Official Guild Wars Wiki profession tango icon as an <img> (replaces emoji)."""
    url = HERO_PROFESSIONS.get(prof) or (COMMON_SKILL_ICON if prof == "Common" else None)
    return f'<img src="{url}" style="width:{px}px;height:{px}px;vertical-align:middle;" alt="">' if url else ''

# De-emojify: profession/Reforged glyphs are <img> tags; every remaining emoji on the
# page is decorative and is stripped here (deliberate design — the page uses no emoji).
# Functional glyphs (check, dropdown arrow, arrows, profession-row markers) are kept.
_DEEMOJI_KEEP = {0x2190, 0x2192, 0x2713, 0x25BC, 0x25B6, 0x25C0, 0x2605, 0x25C6}
def _is_emoji_cp(cp):
    if cp in _DEEMOJI_KEEP:
        return False
    if cp in (0xFE0F, 0xFE0E, 0x20E3):   # variation selectors / keycap combiner
        return True
    if 0x2190 <= cp <= 0x2BFF:           # arrows, misc symbols, dingbats
        return True
    if 0x1F000 <= cp <= 0x1FAFF:         # astral-plane emoji
        return True
    return False
def deemojify(text):
    out = []
    i, n = 0, len(text)
    while i < n:
        if _is_emoji_cp(ord(text[i])):
            i += 1
            while i < n and ord(text[i]) in (0xFE0F, 0xFE0E, 0x20E3):
                i += 1
            if i < n and text[i] == ' ':   # swallow one trailing space ("📚 Skills" -> "Skills")
                i += 1
            continue
        out.append(text[i]); i += 1
    return ''.join(out)
# Cache for armor images (female/male previews)
_ARMOR_IMG_CACHE = {}
def get_wiki_armor_images(slug):
    if slug in _ARMOR_IMG_CACHE:
        return _ARMOR_IMG_CACHE[slug]
    url = f'https://wiki.guildwars.com/wiki/{slug}'
    f_url = None
    m_url = None
    try:
        with urllib.request.urlopen(url, timeout=7) as resp:
            html = resp.read().decode('utf-8', 'ignore')
        # Collect file links on the page
        files = re.findall(r'href=\"/wiki/File:([^\"\s]+\.(?:jpg|png|gif))\"', html, flags=re.I)
        # Prefer filenames that explicitly indicate female/male
        for fn in files:
            lf = fn.lower()
            if f_url is None and ('_f.' in lf or '-female' in lf):
                f_url = f'https://wiki.guildwars.com/wiki/Special:FilePath/{fn}'
            if m_url is None and ('_m.' in lf or '-male' in lf):
                m_url = f'https://wiki.guildwars.com/wiki/Special:FilePath/{fn}'
            if f_url and m_url:
                break
        # Fallback: first two images on the page
        if (f_url is None or m_url is None) and files:
            if f_url is None and len(files) >= 1:
                f_url = f'https://wiki.guildwars.com/wiki/Special:FilePath/{files[0]}'
            if m_url is None and len(files) >= 2:
                m_url = f'https://wiki.guildwars.com/wiki/Special:FilePath/{files[1]}'
    except Exception:
        pass
    _ARMOR_IMG_CACHE[slug] = {'f': f_url, 'm': m_url}
    return _ARMOR_IMG_CACHE[slug]

# Load both Excel files
def load_quests(filename, area_id):
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    quests = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        quests.append({
            'id': f"{area_id}_{row[0]}",
            'order': row[0],
            'name': row[1],
            'giver': row[2],
            'location': row[3],
            'type': row[4],
            'profession': row[5] or '',
            'prereq': row[6],
            'reward': row[7],
        })
    return quests

pre_quests = load_quests('quests/GuildWars_Quest_Tracker.xlsx', 'pre')
post_quests = load_quests('quests/GuildWars_PostSearing_Ascalon.xlsx', 'post')
shiver_quests = load_quests('quests/GuildWars_Northern_Shiverpeaks.xlsx', 'shiver')
kryta_quests = load_quests('quests/GuildWars_Kryta.xlsx', 'kryta')
maguuma_quests = load_quests('quests/GuildWars_Maguuma_Jungle.xlsx', 'maguuma')
desert_quests = load_quests('quests/GuildWars_Crystal_Desert.xlsx', 'desert')
sshiver_quests = load_quests('quests/GuildWars_Southern_Shiverpeaks.xlsx', 'sshiver')
fire_quests = load_quests('quests/GuildWars_Ring_of_Fire.xlsx', 'fire')

# === FACTIONS ===
shingjea_quests = load_quests('quests/GuildWars_Shing_Jea_Island.xlsx', 'shingjea')
kaineng_quests = load_quests('quests/GuildWars_Kaineng_City.xlsx', 'kaineng')
echovald_quests = load_quests('quests/GuildWars_Echovald_Forest.xlsx', 'echovald')
jadesea_quests = load_quests('quests/GuildWars_Jade_Sea.xlsx', 'jadesea')

# === NIGHTFALL ===
istan_quests = load_quests('quests/GuildWars_Istan.xlsx', 'istan')
kourna_quests = load_quests('quests/GuildWars_Kourna.xlsx', 'kourna')
vabbi_quests = load_quests('quests/GuildWars_Vabbi.xlsx', 'vabbi')
desolation_quests = load_quests('quests/GuildWars_Desolation.xlsx', 'desolation')
torment_quests = load_quests('quests/GuildWars_Realm_of_Torment.xlsx', 'torment')

# === EYE OF THE NORTH ===
fshiver_quests = load_quests('quests/GuildWars_Far_Shiverpeaks.xlsx', 'fshiver')
charr_quests = load_quests('quests/GuildWars_Charr_Homelands.xlsx', 'charr')
tarnished_quests = load_quests('quests/GuildWars_Tarnished_Coast.xlsx', 'tarnished')
depths_quests = load_quests('quests/GuildWars_Depths_of_Tyria.xlsx', 'depths')

# === BEYOND ===
wik_quests = load_quests('quests/GuildWars_War_in_Kryta.xlsx', 'wik')
hotn_quests = load_quests('quests/GuildWars_Hearts_of_the_North.xlsx', 'hotn')
woc_quests = load_quests('quests/GuildWars_Winds_of_Change.xlsx', 'woc')

# === BONUS MISSION PACK ===
bmp_quests = load_quests('quests/GuildWars_Bonus_Mission_Pack.xlsx', 'bmp')

html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Unofficial fan-made progress tracker for Guild Wars 1: quests, missions, elite skills, titles, HoM, and daily rotations. Works offline using local storage.">
    <meta name="theme-color" content="#0d1117">
    <meta property="og:title" content="GW Companion — Unofficial Guild Wars Fan Tracker">
    <meta property="og:description" content="Unofficial fan-made progress tracker for Guild Wars 1: quests, missions, elite skills, titles, HoM, and daily rotations.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://gwcompanion.com/">
    <meta property="og:image" content="https://gwcompanion.com/assets/gwc_logo.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="GW Companion — Unofficial Guild Wars Fan Tracker">
    <meta name="twitter:description" content="Unofficial fan-made progress tracker for Guild Wars 1: quests, missions, elite skills, titles, HoM, and daily rotations.">
    <meta name="twitter:image" content="https://gwcompanion.com/assets/gwc_logo.png">
    <link rel="canonical" href="https://gwcompanion.com/">
    <link rel="preconnect" href="https://wiki.guildwars.com">
    <link rel="dns-prefetch" href="//wiki.guildwars.com">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='8' fill='%23161b22'/%3E%3Cpath d='M24 6 L38 11 L38 24 Q38 36 24 42 Q10 36 10 24 L10 11 Z' fill='none' stroke='%23c9a227' stroke-width='2'/%3E%3Ctext x='24' y='28' text-anchor='middle' font-size='14' fill='%23e3bf57' font-family='Georgia,serif'%3EGW%3C/text%3E%3Cline x1='16' y1='33' x2='32' y2='33' stroke='%23c9a227' stroke-width='1'/%3E%3C/svg%3E">
    <link rel="preload" href="assets/gwc_logo.png" as="image">
    <title>GW Companion — Unofficial Guild Wars Fan Tracker</title>
    <style>
        @font-face { font-family: 'Cinzel'; font-style: normal; font-weight: 400 900; font-display: swap; src: url('assets/fonts/cinzel-latin-var.woff2') format('woff2'); }
        @font-face { font-family: 'EB Garamond'; font-style: normal; font-weight: 400 800; font-display: swap; src: url('assets/fonts/ebgaramond-latin-var.woff2') format('woff2'); }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        h1, h2, h3, h4, .progress-text { font-family: 'Cinzel', Georgia, serif; letter-spacing: 0.5px; }
        body { 
            font-family: 'EB Garamond', Georgia, 'Times New Roman', serif; 
            background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
            min-height: 100vh;
            color: #c9d1d9;
        }
        
        /* Header */
        .header {
            background: #21262d;
            padding: 10px 15px;
            border-bottom: 1px solid #30363d;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .header h1 { 
            color: #ffd700; 
            font-size: 1.4em; 
            white-space: nowrap; 
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.5), 0 0 20px rgba(255, 215, 0, 0.3);
            letter-spacing: 1px;
        }
        .header h1 img { 
            width: 32px; 
            height: 32px; 
            filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.6));
            opacity: 0;
            transition: opacity 0.2s ease-in;
        }
        .header h1 img.loaded {
            opacity: 1;
        }
        
        /* Character Selector */
        .char-selector {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .char-selector select {
            background: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 0.85em;
            cursor: pointer;
            min-width: 100px;
            transition: all 0.2s;
        }
        .char-selector select:hover { background: #30363d; border-color: #58a6ff; }
        .char-btn {
            background: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
        }
        .char-btn:hover { background: #30363d; border-color: #58a6ff; }
        .char-btn.add { color: #3fb950; }
        .char-btn.delete { color: #f85149; }
        .char-label { color: #8b949e; font-size: 0.85em; }
        .prof-dropdown { padding: 4px 8px; border-radius: 6px; border: 1px solid #30363d; background: #21262d; color: #c9d1d9; font-size: 0.85em; min-width: 90px; }
        /* Toolbox connector */
        .tb-conn { display: inline-flex; align-items: center; gap: 6px; margin-left: 8px; }
        .tb-dot { width: 10px; height: 10px; border-radius: 50%; border: 1px solid #30363d; background: #6e7681; display: inline-block; }
        .tb-dot.ok { background: #2ea043; }
        .tb-dot.err { background: #f85149; }
        
        /* Elite skill highlighting based on profession */
        tr.elite-capturable { background: rgba(63, 185, 80, 0.15) !important; }
        tr.elite-capturable td:first-child::before { content: "✓ "; color: #3fb950; }
        tr.elite-other { opacity: 0.5; }
        details.prof-match > summary { border-left: 3px solid #3fb950 !important; }
        details.prof-partial > summary { border-left: 3px solid #ffa657 !important; }
        
        /* Quest profession highlighting - highlight matching, dim others */
        tr.my-profession { background: rgba(63, 185, 80, 0.2) !important; border-left: 3px solid #3fb950; }
        tr.my-profession td:first-child::before { content: "★ "; }
        tr.my-secondary-profession { background: rgba(255, 166, 87, 0.15) !important; border-left: 3px solid #ffa657; }
        tr.my-secondary-profession td:first-child::before { content: "◆ "; }
        tr.other-profession { opacity: 0.5; }
        
        /* Profession progress grid */
        .prof-progress-item { transition: all 0.2s; border: 2px solid transparent; }
        .prof-progress-item.is-primary { border-color: #3fb950; background: rgba(63,185,80,0.15) !important; }
        .prof-progress-item.is-secondary { border-color: #ffa657; background: rgba(255,166,87,0.15) !important; }
        .prof-progress-item.is-complete { opacity: 0.6; }
        .prof-progress-item.is-complete::after { content: "✓"; position: absolute; top: 2px; right: 5px; color: #3fb950; font-size: 0.8em; }
        .prof-progress-item { position: relative; }
        .prof-progress-item.recommend { border-color: #f0883e; animation: pulse-recommend 2s infinite; }
        @keyframes pulse-recommend { 0%, 100% { box-shadow: 0 0 0 0 rgba(240,136,62,0.4); } 50% { box-shadow: 0 0 0 4px rgba(240,136,62,0); } }
        
        /* Main Category Tabs */
        .main-tabs {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 4px;
            padding: 10px 10px 0;
            background: #0d1117;
            border-bottom: 1px solid #30363d;
        }
        .main-tab {
            padding: 8px 12px;
            background: #21262d;
            border: 1px solid #30363d;
            border-bottom: none;
            border-radius: 6px 6px 0 0;
            color: #8b949e;
            cursor: pointer;
            font-size: 0.85em;
            font-weight: 500;
            transition: all 0.2s;
            white-space: nowrap;
        }
        .main-tab:hover { background: #30363d; color: #c9d1d9; }
        .main-tab.active { 
            background: #161b22; 
            color: #58a6ff; 
            border-color: #58a6ff;
            border-bottom: 2px solid #161b22;
            margin-bottom: -1px;
        }
        
        /* Region Selector */
        .region-selector {
            background: #161b22;
            padding: 15px 20px;
            border-bottom: 1px solid #30363d;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
        }
        .region-selector.hidden { display: none; }
        .region-select {
            background: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            min-width: 280px;
        }
        .region-select:hover { border-color: #58a6ff; }
        .region-select optgroup { 
            background: #21262d; 
            color: #ffd700;
            font-weight: bold;
        }
        .region-select option { 
            background: #161b22; 
            color: #c9d1d9;
            padding: 8px;
        }
        
        /* Content */
        .content { padding: 20px; }
        .area { display: none; }
        .area.active { display: block; }
        
        /* Progress */
        .progress-container {
            max-width: 600px;
            margin: 0 auto 20px;
            background: #21262d;
            border-radius: 10px;
            padding: 15px 20px;
        }
        .progress-header { display: flex; justify-content: space-between; align-items: baseline; gap: 6px 10px; flex-wrap: wrap; margin-bottom: 8px; }
        .progress-text { color: #8b949e; }
        .progress-count { color: #ffd700; font-weight: bold; font-size: 1.2em; white-space: nowrap; flex: 0 0 auto; margin-left: auto; }
        .progress-bar { height: 12px; background: #30363d; border-radius: 6px; overflow: hidden; }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #238636 0%, #3fb950 100%);
            border-radius: 6px;
            transition: width 0.3s ease;
        }
        
        /* IO Buttons */
        .io-section {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .io-btn {
            padding: 8px 16px;
            border: 1px solid #30363d;
            background: #21262d;
            color: #c9d1d9;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
        }
        .io-btn:hover { border-color: #58a6ff; background: #30363d; }
        .io-btn.export { border-color: #238636; }
        .io-btn.export:hover { background: #238636; color: #fff; }
        .io-btn.import { border-color: #1f6feb; }
        .io-btn.import:hover { background: #1f6feb; color: #fff; }
        
        /* Filters */
        .filters {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 8px 16px;
            border: 1px solid #30363d;
            background: #21262d;
            color: #c9d1d9;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
        }
        .filter-btn:hover { border-color: #58a6ff; }
        .filter-btn.active { background: #238636; border-color: #238636; color: #fff; }
        .filter-btn[data-filter="mini"].active { background: #d4a017; border-color: #d4a017; }
        .filter-btn[data-filter="mission"].active { background: #7030a0; border-color: #7030a0; }
        .filter-btn[data-filter="vanguard"].active { background: #9e6a03; border-color: #9e6a03; }
        .filter-btn[data-filter="special"].active { background: #9e6a03; border-color: #9e6a03; }
        .filter-btn[data-filter="travel"].active { background: #00bfff; border-color: #00bfff; color: #000; }
        .filter-btn.prof-warrior.active { background: #c00000; border-color: #c00000; }
        .filter-btn.prof-ranger.active { background: #548235; border-color: #548235; }
        .filter-btn.prof-monk.active { background: #2e75b6; border-color: #2e75b6; }
        .filter-btn.prof-necromancer.active { background: #7030a0; border-color: #7030a0; }
        .filter-btn.prof-mesmer.active { background: #c55a90; border-color: #c55a90; }
        .filter-btn.prof-elementalist.active { background: #bf9000; border-color: #bf9000; }
        .filter-btn.prof-assassin.active { background: #4a4a4a; border-color: #4a4a4a; }
        .filter-btn.prof-ritualist.active { background: #00a86b; border-color: #00a86b; }
        .filter-btn.prof-paragon.active { background: #ffd700; border-color: #ffd700; color: #000; }
        .filter-btn.prof-dervish.active { background: #8b4513; border-color: #8b4513; }
        
        /* Table */
        .container { max-width: 1800px; margin: 0 auto; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
        th { 
            background: #21262d; color: #c9d1d9; padding: 12px 8px; 
            text-align: left; position: sticky; top: 0; z-index: 10;
            border-bottom: 2px solid #30363d;
        }
        td { padding: 10px 8px; border-bottom: 1px solid #21262d; }
        /* Tighter, perfectly aligned checkbox columns for Missions */
        .missions-table { table-layout: fixed; }
        .missions-table th:nth-child(1),
        .missions-table th:nth-child(2),
        .missions-table th:nth-child(3),
        .missions-table th:nth-child(4) { text-align: center; width: 50px !important; }
        
        /* Force exact centering of inputs in the first 4 columns */
        
        
        /* Normalize checkbox size across all four columns in Missions and center them exactly */
        .missions-table .quest-checkbox,
        .missions-table .bonus-checkbox,
        .missions-table .hm-checkbox,
        .missions-table .hm-bonus-checkbox { width: 18px !important; height: 18px !important; display: block; margin: 0 auto; }
        tr:hover { background: rgba(255,255,255,0.03); }
        tr.completed { opacity: 0.5; }
        tr.completed td { text-decoration: line-through; }
        tr.hidden, tr.hidden-restrict { display: none !important; }
        
        .type-main { background: rgba(88,166,255,0.1); }
        .type-mission { background: rgba(112,48,160,0.15); }
        .type-profession { background: rgba(63,185,80,0.08); }
        .type-vanguard, .type-special { background: rgba(247,129,102,0.1); }
        .type-travel { background: rgba(0,191,255,0.15); }
        .type-attribute { background: rgba(156,39,176,0.1); }
        tr.attr-highlight { box-shadow: inset 3px 0 0 #9c27b0; background: rgba(156,39,176,0.15) !important; }
        tr.attr-unavailable { opacity: 0.5; }
        
        .badge { padding: 3px 8px; border-radius: 4px; font-size: 0.8em; font-weight: 500; }
        .badge-main { background: #1f6feb; color: #fff; }
        .badge-side { background: #30363d; color: #8b949e; }
        .badge-mini { background: #d4a017; color: #fff; }
        .badge-mission { background: #7030a0; color: #fff; }
        .badge-profession { background: #238636; color: #fff; }
        .badge-vanguard, .badge-special { background: #9e6a03; color: #fff; }
        .badge-travel { background: #00bfff; color: #000; font-weight: bold; }
        .badge-endgame { background: #ff4500; color: #fff; font-weight: bold; }
        .badge-attribute { background: #9c27b0; color: #fff; font-weight: bold; }
        .badge-missable { border: 1px solid #ff9800; color: #ff9800; background: transparent; margin-left: 4px; font-size: 0.75em; padding: 2px 6px; }
        
        .prof { padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8em; color: #fff; }
        .prof-warrior { background: #c00000; }
        .prof-ranger { background: #548235; }
        .prof-monk { background: #2e75b6; }
        .prof-necromancer { background: #7030a0; }
        .prof-mesmer { background: #c55a90; }
        .prof-elementalist { background: #bf9000; }
        .prof-assassin { background: #4a4a4a; }
        .prof-ritualist { background: #00a86b; }
        .prof-paragon { background: #ffd700; color: #000; }
        .prof-dervish { background: #8b4513; }
        
        .quest-link { color: #ffd700; text-decoration: none; font-weight: 500; }
        .quest-link:hover { color: #fff; text-decoration: underline; }
        .location { color: #79c0ff; }
        .prereq { color: #8b949e; font-size: 0.9em; }
        .reward { color: #7ee787; font-size: 0.9em; }
        .order { color: #484f58; text-align: center; width: 40px; }
        .checkbox-cell { text-align: center; width: 50px; }
        /* Checkbox grid styles */
        .checks4-table td:nth-child(1) input,
        .checks4-table td:nth-child(2) input,
        .checks4-table td:nth-child(3) input,
        .checks4-table td:nth-child(4) input { display:block; margin:0 auto; width:18px; height:18px; }
        .has-checkbox-first th:nth-child(1) { text-align:center; width:50px; }
        .has-checkbox-first td:nth-child(1) { text-align:center; width:50px; padding:8px 0; }
        .has-checkbox-first td:nth-child(1) input { display:block; margin:0 auto; width:18px; height:18px; }
        .quest-checkbox { width: 20px; height: 20px; cursor: pointer; accent-color: #238636; }
        .bonus-checkbox { width: 18px; height: 18px; cursor: pointer; accent-color: #ffd700; }
        .bonus-done .bonus-checkbox { box-shadow: 0 0 8px #ffd700; }
        .hm-checkbox { width: 18px; height: 18px; cursor: pointer; accent-color: #f85149; }
        tr.hm-done .hm-checkbox { box-shadow: 0 0 8px #f85149; }
        .hm-bonus-checkbox { width: 18px; height: 18px; cursor: pointer; accent-color: #ff6b00; }
        tr.hm-bonus-done .hm-bonus-checkbox { box-shadow: 0 0 8px #ff6b00; }
        tr.campaign-locked { opacity: 0.4; background: rgba(100,100,100,0.1); }
        tr.campaign-locked .quest-checkbox { cursor: not-allowed; }
        tr.missable-row { box-shadow: inset 2px 0 0 #ff9800; background: rgba(255,152,0,0.06); }
        
        .reset-btn {
            display: block; margin: 20px auto; padding: 10px 20px;
            background: #c00000; color: #fff; border: none;
            border-radius: 6px; cursor: pointer; font-size: 0.9em;
        }
        .reset-btn:hover { background: #ff3333; }
        
        /* Tablet */
        @media (max-width: 1024px) {
            .header h1 { font-size: 1em; }
            .char-label { display: none; }
            .main-tab { padding: 6px 10px; font-size: 0.8em; }
        }
        
        /* Mobile */
        @media (max-width: 768px) {
            .header { padding: 8px 10px; }
            .header h1 { font-size: 0.9em; }
            .char-selector select { min-width: 80px; padding: 4px 6px; font-size: 0.75em; }
            .char-btn { padding: 4px 8px; font-size: 0.75em; }
            .main-tab { padding: 5px 8px; font-size: 0.75em; }
            .content { padding: 10px; }
            .tab { padding: 10px 16px; font-size: 0.85em; }
            .filters { gap: 5px; flex-wrap: wrap; }
            .filter-btn { padding: 4px 8px; font-size: 0.7em; }
            .io-btn { padding: 4px 8px; font-size: 0.7em; }
            table { font-size: 0.7em; }
            td, th { padding: 4px 2px; }
            /* Hide less important columns: Bonus(3), HM+B(4), Giver(7), Type(9), Profession(10), Prerequisite(11), Reward(12) */
            th:nth-child(3), td:nth-child(3),
            th:nth-child(4), td:nth-child(4),
            th:nth-child(7), td:nth-child(7),
            th:nth-child(9), td:nth-child(9),
            th:nth-child(10), td:nth-child(10),
            th:nth-child(11), td:nth-child(11),
            th:nth-child(12), td:nth-child(12) { display: none; }
        }
        
        @media (max-width: 480px) {
            .header h1 {
                font-size: 0.8em;
                white-space: normal;
            }
            /* Also hide Location(8) on very small screens */
            th:nth-child(8), td:nth-child(8) { display: none; }
        }
        .skip-link {
            position: absolute;
            top: 0;
            left: 0;
            transform: translateY(-120%);
            background: #58a6ff;
            color: #0d1117;
            padding: 8px 12px;
            border-radius: 0 0 8px 0;
            z-index: 2000;
            text-decoration: none;
            font-weight: 600;
        }
        .skip-link:focus { transform: translateY(0); }
        :focus-visible { outline: 2px solid #58a6ff; outline-offset: 2px; }
        .custom-dropdown { position: relative; display: inline-block; min-width: 120px; }
        .dropdown-header { 
            padding: 6px 12px; 
            border-radius: 6px; 
            border: 1px solid #30363d; 
            background: #21262d; 
            color: #c9d1d9; 
            font-size: 0.85em; 
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }
        .dropdown-header:hover { background: #30363d; border-color: #58a6ff; }
        .dropdown-arrow { font-size: 0.7em; color: #8b949e; transition: transform 0.2s; }
        .dropdown-header.open .dropdown-arrow { transform: rotate(180deg); }
        .dropdown-list {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 4px;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            z-index: 1000;
            max-height: 300px;
            overflow-y: auto;
        }
        .dropdown-option {
            padding: 8px 12px;
            cursor: pointer;
            color: #c9d1d9;
            font-size: 0.85em;
            transition: background 0.15s;
            display: flex;
            align-items: center;
        }
        .dropdown-option:hover { background: #21262d; }
        .dropdown-option:first-child { border-radius: 6px 6px 0 0; }
        .dropdown-option:last-child { border-radius: 0 0 6px 6px; }
        /* Game mode toggles */
        .mode-toggles { display: inline-flex; gap: 5px; align-items: center; margin-left: 4px; }
        .mode-toggle { background: #21262d; border: 1px solid #30363d; border-radius: 6px; padding: 2px 5px; cursor: pointer; opacity: 0.4; filter: grayscale(100%); transition: all 0.2s; display: inline-flex; align-items: center; line-height: 0; }
        .mode-toggle:hover { border-color: #58a6ff; opacity: 0.8; }
        .mode-toggle.active { opacity: 1; filter: none; border-color: #58a6ff; box-shadow: 0 0 6px rgba(88,166,255,0.4); }
        .mode-toggle img { width: 22px; height: 22px; }
        .mode-badge { width: 20px; height: 20px; vertical-align: middle; margin-left: 4px; }
        body.mode-reforged-off tr[data-reforged="1"] { display: none; }
        body.mode-melandru-on .menagerie-grid { opacity: 0.4; pointer-events: none; filter: grayscale(60%); }
        .menagerie-blocked { display: none; }
        body.mode-melandru-on .menagerie-normal { display: none; }
        body.mode-melandru-on .menagerie-blocked { display: inline; color: #f85149; font-weight: 600; }
        .melandru-block { display: none; margin: 10px 0; padding: 10px 14px; border-radius: 8px; background: rgba(248,81,73,0.12); border: 1px solid #f85149; color: #f0a39c; font-weight: 600; }
        body.mode-melandru-on .melandru-block { display: block; }
        .melandru-hint { display: none; }
        body.mode-melandru-on .melandru-hint { display: block; flex: 1 1 100%; order: 10; color: #f85149; font-size: 0.85em; margin-left: 0; }
        /* Skills profession grid: 6 columns on desktop, wrap on small screens to avoid horizontal page overflow */
        @media (max-width: 480px) {
            #skills-prof-grid { grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)) !important; }
            #elites-prof-grid { grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)) !important; }
            .menagerie-grid { grid-template-columns: 1fr !important; }
        }
    </style>
</head>
<body>
    <a class="skip-link" href="#app-main">Skip to main content</a>
    <div class="header">
        <h1 id="main-header" style="cursor:pointer;" onclick="location.reload()" title="Reload page" role="button" tabindex="0" aria-label="Reload page">
            <svg width="38" height="38" viewBox="0 0 48 48" aria-hidden="true" style="flex:0 0 auto;"><path d="M24 4 L40 10 L40 24 Q40 38 24 44 Q8 38 8 24 L8 10 Z" fill="none" stroke="#c9a227" stroke-width="2"/><text x="24" y="27" text-anchor="middle" font-family="Cinzel, Georgia, serif" font-size="15" fill="#e3bf57">GW</text><line x1="15" y1="33" x2="33" y2="33" stroke="#c9a227" stroke-width="1"/></svg>
            <span style="display:inline-flex;flex-direction:column;line-height:1.15;vertical-align:middle;"><span style="letter-spacing:2.5px;">GW COMPANION</span><span style="font-size:0.45em;letter-spacing:1.5px;color:#8b949e;font-family:'EB Garamond', Georgia, serif;">UNOFFICIAL FAN TRACKER</span></span>
        </h1>
        <div class="char-selector">
            <span class="char-label">Character:</span>
            <select id="char-select" onchange="switchCharacter()"></select>
            <span id="mode-badges"></span>
            <div class="mode-toggles">
                <button class="mode-toggle" id="toggle-reforged" onclick="toggleMode('reforged')" aria-pressed="true" title="Reforged Mode — overhauled Prophecies content (quests, heroes, Piken Square pre)"><img src="https://wiki.guildwars.com/images/1/19/ReforgedMode-Small.png" alt="Reforged Mode"></button>
                <button class="mode-toggle" id="toggle-dhuum" onclick="toggleMode('dhuum')" aria-pressed="false" title="Dhuum's Covenant — One life. No resurrection."><img src="https://wiki.guildwars.com/images/0/05/DhuumCovenant-Small.png" alt="Dhuum's Covenant"></button>
                <button class="mode-toggle" id="toggle-melandru" onclick="toggleMode('melandru')" aria-pressed="false" title="Melandru's Accord — Ironman: no trading, no tomes, no price traders"><img src="https://wiki.guildwars.com/images/1/11/Melandrus_Accord-Small.png" alt="Melandru's Accord"></button>
            </div>
            <select id="campaign-select" class="campaign-dropdown" onchange="setCampaign()">
                <option value="">-- Campaign --</option>
                <option value="prophecies">⚔️ Prophecies</option>
                <option value="factions">🐉 Factions</option>
                <option value="nightfall">🌙 Nightfall</option>
            </select>
            <div class="custom-dropdown" id="primary-prof-wrapper">
                <div class="dropdown-header" onclick="toggleDropdown('primary-prof')">
                    <span id="primary-prof-selected">Primary</span>
                    <span class="dropdown-arrow">▼</span>
                </div>
                <div class="dropdown-list" id="primary-prof-list" style="display:none;">
                    <div class="dropdown-option" data-value="" onclick="selectProf('primary-prof', '', 'Primary', null)">Primary</div>
                    <div class="dropdown-option" data-value="warrior" onclick="selectProf('primary-prof', 'warrior', 'Warrior', 'https://wiki.guildwars.com/images/3/3b/Warrior-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/3/3b/Warrior-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Warrior
                    </div>
                    <div class="dropdown-option" data-value="ranger" onclick="selectProf('primary-prof', 'ranger', 'Ranger', 'https://wiki.guildwars.com/images/d/dc/Ranger-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/d/dc/Ranger-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Ranger
                    </div>
                    <div class="dropdown-option" data-value="monk" onclick="selectProf('primary-prof', 'monk', 'Monk', 'https://wiki.guildwars.com/images/f/f8/Monk-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/f/f8/Monk-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Monk
                    </div>
                    <div class="dropdown-option" data-value="necromancer" onclick="selectProf('primary-prof', 'necromancer', 'Necromancer', 'https://wiki.guildwars.com/images/7/7b/Necromancer-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/7/7b/Necromancer-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Necromancer
                    </div>
                    <div class="dropdown-option" data-value="mesmer" onclick="selectProf('primary-prof', 'mesmer', 'Mesmer', 'https://wiki.guildwars.com/images/f/fb/Mesmer-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/f/fb/Mesmer-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Mesmer
                    </div>
                    <div class="dropdown-option" data-value="elementalist" onclick="selectProf('primary-prof', 'elementalist', 'Elementalist', 'https://wiki.guildwars.com/images/a/ab/Elementalist-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/a/ab/Elementalist-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Elementalist
                    </div>
                    <div class="dropdown-option" data-value="assassin" onclick="selectProf('primary-prof', 'assassin', 'Assassin', 'https://wiki.guildwars.com/images/5/5f/Assassin-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/5/5f/Assassin-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Assassin
                    </div>
                    <div class="dropdown-option" data-value="ritualist" onclick="selectProf('primary-prof', 'ritualist', 'Ritualist', 'https://wiki.guildwars.com/images/8/81/Ritualist-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/8/81/Ritualist-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Ritualist
                    </div>
                    <div class="dropdown-option" data-value="paragon" onclick="selectProf('primary-prof', 'paragon', 'Paragon', 'https://wiki.guildwars.com/images/5/55/Paragon-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/5/55/Paragon-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Paragon
                    </div>
                    <div class="dropdown-option" data-value="dervish" onclick="selectProf('primary-prof', 'dervish', 'Dervish', 'https://wiki.guildwars.com/images/3/3e/Dervish-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/3/3e/Dervish-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Dervish
                    </div>
                </div>
            </div>
            <input type="hidden" id="primary-prof" value="">
            <div class="custom-dropdown" id="secondary-prof-wrapper">
                <div class="dropdown-header" onclick="toggleDropdown('secondary-prof')">
                    <span id="secondary-prof-selected">Secondary</span>
                    <span class="dropdown-arrow">▼</span>
                </div>
                <div class="dropdown-list" id="secondary-prof-list" style="display:none;">
                    <div class="dropdown-option" data-value="" onclick="selectProf('secondary-prof', '', 'Secondary', null)">Secondary</div>
                    <div class="dropdown-option" data-value="warrior" onclick="selectProf('secondary-prof', 'warrior', 'Warrior', 'https://wiki.guildwars.com/images/3/3b/Warrior-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/3/3b/Warrior-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Warrior
                    </div>
                    <div class="dropdown-option" data-value="ranger" onclick="selectProf('secondary-prof', 'ranger', 'Ranger', 'https://wiki.guildwars.com/images/d/dc/Ranger-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/d/dc/Ranger-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Ranger
                    </div>
                    <div class="dropdown-option" data-value="monk" onclick="selectProf('secondary-prof', 'monk', 'Monk', 'https://wiki.guildwars.com/images/f/f8/Monk-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/f/f8/Monk-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Monk
                    </div>
                    <div class="dropdown-option" data-value="necromancer" onclick="selectProf('secondary-prof', 'necromancer', 'Necromancer', 'https://wiki.guildwars.com/images/7/7b/Necromancer-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/7/7b/Necromancer-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Necromancer
                    </div>
                    <div class="dropdown-option" data-value="mesmer" onclick="selectProf('secondary-prof', 'mesmer', 'Mesmer', 'https://wiki.guildwars.com/images/f/fb/Mesmer-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/f/fb/Mesmer-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Mesmer
                    </div>
                    <div class="dropdown-option" data-value="elementalist" onclick="selectProf('secondary-prof', 'elementalist', 'Elementalist', 'https://wiki.guildwars.com/images/a/ab/Elementalist-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/a/ab/Elementalist-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Elementalist
                    </div>
                    <div class="dropdown-option" data-value="assassin" onclick="selectProf('secondary-prof', 'assassin', 'Assassin', 'https://wiki.guildwars.com/images/5/5f/Assassin-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/5/5f/Assassin-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Assassin
                    </div>
                    <div class="dropdown-option" data-value="ritualist" onclick="selectProf('secondary-prof', 'ritualist', 'Ritualist', 'https://wiki.guildwars.com/images/8/81/Ritualist-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/8/81/Ritualist-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Ritualist
                    </div>
                    <div class="dropdown-option" data-value="paragon" onclick="selectProf('secondary-prof', 'paragon', 'Paragon', 'https://wiki.guildwars.com/images/5/55/Paragon-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/5/55/Paragon-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Paragon
                    </div>
                    <div class="dropdown-option" data-value="dervish" onclick="selectProf('secondary-prof', 'dervish', 'Dervish', 'https://wiki.guildwars.com/images/3/3e/Dervish-tango-icon-20.png')">
                        <img src="https://wiki.guildwars.com/images/3/3e/Dervish-tango-icon-20.png" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">Dervish
                    </div>
                    <div class="dropdown-option" data-value="none" onclick="selectProf('secondary-prof', 'none', '❌ None', null)">❌ None</div>
                </div>
            </div>
            <input type="hidden" id="secondary-prof" value="">
            <button class="char-btn" onclick="resetCharacter()" title="Reset all progress for this character">🔄 Reset</button>
            <button class="char-btn add" onclick="addCharacter()" aria-label="Add character" title="Add character">+ New</button>
            <button class="char-btn" onclick="renameCharacter()" aria-label="Rename character" title="Rename character"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="vertical-align:-2px;"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg></button>
            <button class="char-btn delete" onclick="deleteCharacter()" aria-label="Delete character" title="Delete character"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="vertical-align:-2px;"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg></button>
        </div>
    </div>
    
    <main id="app-main" role="main">
    <div class="main-tabs">
        <button class="main-tab active" data-category="quests" onclick="switchCategory('quests')">📜 Quests</button>
        <button class="main-tab" data-category="daily" onclick="switchCategory('daily')">📅 Daily</button>
        <button class="main-tab" data-category="missions" onclick="switchCategory('missions')">🗺️ Missions</button>
        <button class="main-tab" data-category="elites" onclick="switchCategory('elites')">🎯 Elite Skills</button>
        <button class="main-tab" data-category="skills" onclick="switchCategory('skills')">📚 All Skills</button>
        <button class="main-tab" data-category="heroes" onclick="switchCategory('heroes')">🦸 Heroes</button>
        <button class="main-tab" data-category="dungeons" onclick="switchCategory('dungeons')">🏰 Dungeons</button>
        <button class="main-tab" data-category="vanquish" onclick="switchCategory('vanquish')">⚔️ Vanquish</button>
        <button class="main-tab" data-category="cartographer" onclick="switchCategory('cartographer')">🗺️ Cartographer</button>
        <button class="main-tab" data-category="armor" onclick="switchCategory('armor')">🛡️ Armor</button>
        <button class="main-tab" data-category="minis" onclick="switchCategory('minis')">🐾 Minis</button>
        <button class="main-tab" data-category="menagerie" onclick="switchCategory('menagerie')">🦁 Menagerie</button>
        <button class="main-tab" data-category="uniques" onclick="switchCategory('uniques')">💎 Items</button>
        <button class="main-tab" data-category="outposts" onclick="switchCategory('outposts')">🏘️ Outposts</button>
        <button class="main-tab" data-category="titles" onclick="switchCategory('titles')">🏆 Titles</button>
        <button class="main-tab" data-category="hom" onclick="switchCategory('hom')">🏛️ HoM</button>
    </div>
    
    <div class="region-selector" id="quests-selector">
        <select id="region-select" class="region-select" onchange="switchRegion()">
            <optgroup label="⚔️ PROPHECIES">
                <option value="pre" data-total="''' + str(len(pre_quests)) + '''">Pre-Searing (0/''' + str(len(pre_quests)) + ''')</option>
                <option value="post" data-total="''' + str(len(post_quests)) + '''">Post-Searing Ascalon (0/''' + str(len(post_quests)) + ''')</option>
                <option value="shiver" data-total="''' + str(len(shiver_quests)) + '''">Northern Shiverpeaks (0/''' + str(len(shiver_quests)) + ''')</option>
                <option value="kryta" data-total="''' + str(len(kryta_quests)) + '''">Kryta (0/''' + str(len(kryta_quests)) + ''')</option>
                <option value="maguuma" data-total="''' + str(len(maguuma_quests)) + '''">Maguuma Jungle (0/''' + str(len(maguuma_quests)) + ''')</option>
                <option value="desert" data-total="''' + str(len(desert_quests)) + '''">Crystal Desert (0/''' + str(len(desert_quests)) + ''')</option>
                <option value="sshiver" data-total="''' + str(len(sshiver_quests)) + '''">Southern Shiverpeaks (0/''' + str(len(sshiver_quests)) + ''')</option>
                <option value="fire" data-total="''' + str(len(fire_quests)) + '''">Ring of Fire (0/''' + str(len(fire_quests)) + ''')</option>
            </optgroup>
            <optgroup label="🐉 FACTIONS">
                <option value="shingjea" data-total="''' + str(len(shingjea_quests)) + '''">Shing Jea Island (0/''' + str(len(shingjea_quests)) + ''')</option>
                <option value="kaineng" data-total="''' + str(len(kaineng_quests)) + '''">Kaineng City (0/''' + str(len(kaineng_quests)) + ''')</option>
                <option value="echovald" data-total="''' + str(len(echovald_quests)) + '''">Echovald Forest (0/''' + str(len(echovald_quests)) + ''')</option>
                <option value="jadesea" data-total="''' + str(len(jadesea_quests)) + '''">The Jade Sea (0/''' + str(len(jadesea_quests)) + ''')</option>
            </optgroup>
            <optgroup label="🌙 NIGHTFALL">
                <option value="istan" data-total="''' + str(len(istan_quests)) + '''">Istan (0/''' + str(len(istan_quests)) + ''')</option>
                <option value="kourna" data-total="''' + str(len(kourna_quests)) + '''">Kourna (0/''' + str(len(kourna_quests)) + ''')</option>
                <option value="vabbi" data-total="''' + str(len(vabbi_quests)) + '''">Vabbi (0/''' + str(len(vabbi_quests)) + ''')</option>
                <option value="desolation" data-total="''' + str(len(desolation_quests)) + '''">The Desolation (0/''' + str(len(desolation_quests)) + ''')</option>
                <option value="torment" data-total="''' + str(len(torment_quests)) + '''">Realm of Torment (0/''' + str(len(torment_quests)) + ''')</option>
            </optgroup>
            <optgroup label="⛰️ EYE OF THE NORTH">
                <option value="fshiver" data-total="''' + str(len(fshiver_quests)) + '''">Far Shiverpeaks (0/''' + str(len(fshiver_quests)) + ''')</option>
                <option value="charr" data-total="''' + str(len(charr_quests)) + '''">Charr Homelands (0/''' + str(len(charr_quests)) + ''')</option>
                <option value="tarnished" data-total="''' + str(len(tarnished_quests)) + '''">Tarnished Coast (0/''' + str(len(tarnished_quests)) + ''')</option>
                <option value="depths" data-total="''' + str(len(depths_quests)) + '''">Depths of Tyria (0/''' + str(len(depths_quests)) + ''')</option>
            </optgroup>
            <optgroup label="💫 BEYOND">
                <option value="wik" data-total="''' + str(len(wik_quests)) + '''">War in Kryta (0/''' + str(len(wik_quests)) + ''')</option>
                <option value="hotn" data-total="''' + str(len(hotn_quests)) + '''">Hearts of the North (0/''' + str(len(hotn_quests)) + ''')</option>
                <option value="woc" data-total="''' + str(len(woc_quests)) + '''">Winds of Change (0/''' + str(len(woc_quests)) + ''')</option>
            </optgroup>
            <optgroup label="🎁 BONUS">
                <option value="bmp" data-total="''' + str(len(bmp_quests)) + '''">Bonus Mission Pack (0/''' + str(len(bmp_quests)) + ''')</option>
            </optgroup>
        </select>
    </div>
'''

def generate_area_html(quests, area_id, area_name, is_first, is_bonus_pack=False):
    type_class = {"Main": "type-main", "Mission": "type-mission", "Mini": "type-mini", 
                  "Profession": "type-profession", "Vanguard": "type-vanguard", "Special": "type-special",
                  "Endgame": "type-endgame", "Attribute": "type-attribute",
                  "Travel": "type-travel"}
    badge_class = {"Main": "badge-main", "Side": "badge-side", "Mini": "badge-mini", "Mission": "badge-mission",
                   "Profession": "badge-profession", "Vanguard": "badge-vanguard", "Special": "badge-special",
                   "Travel": "badge-travel", "Endgame": "badge-endgame", "Attribute": "badge-attribute"}
    prof_class = {"Warrior": "prof-warrior", "Ranger": "prof-ranger", "Monk": "prof-monk", 
                  "Necromancer": "prof-necromancer", "Mesmer": "prof-mesmer", "Elementalist": "prof-elementalist",
                  "Assassin": "prof-assassin", "Ritualist": "prof-ritualist",
                  "Paragon": "prof-paragon", "Dervish": "prof-dervish"}
    
    active = "active" if is_first else ""
    h = f'''
    <div class="area {active}" id="area-{area_id}">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">{area_name}</span>
                    <span class="progress-count"><span id="{area_id}-completed">0</span> / <span id="{area_id}-total">{len(quests)}</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="{area_id}-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="io-section">
                <button class="io-btn export" onclick="exportJSON('{area_id}')">Export JSON</button>
                <button class="io-btn export" onclick="exportCSV('{area_id}')">Export CSV</button>
                <button class="io-btn import" onclick="document.getElementById('import-{area_id}').click()">Import JSON</button>
                <input type="file" id="import-{area_id}" accept=".json" onchange="importJSON(event, '{area_id}')" style="display:none">
            </div>
            
            <div class="filters" data-area="{area_id}">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="main">Main</button>'''

    if area_id == "pre":
        h += '''
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="mini">Mini</button>
                <button class="filter-btn" data-filter="profession">Profession</button>
                <button class="filter-btn" data-filter="vanguard">Vanguard</button>'''
    elif area_id == "post":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="profession">Profession</button>
                <button class="filter-btn" data-filter="special">Special</button>'''
    elif area_id == "shingjea":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="profession">Profession</button>'''
    elif area_id == "kaineng":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="special">Special</button>
                <button class="filter-btn" data-filter="travel">✈️ Travel</button>'''
    elif area_id in ["echovald", "jadesea"]:
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="special">Special</button>'''
    elif area_id == "shiver":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="profession">Profession</button>'''
    elif area_id == "kryta":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="profession">Profession</button>
                <button class="filter-btn" data-filter="special">Special</button>
                <button class="filter-btn" data-filter="travel">✈️ Travel</button>'''
    elif area_id == "istan":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="special">Special</button>
                <button class="filter-btn" data-filter="travel">✈️ Travel</button>'''
    elif area_id in ["kourna", "vabbi", "desolation"]:
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>'''
    elif area_id == "torment":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="endgame">🏆 Endgame</button>'''
    elif area_id in ["fshiver", "tarnished"]:
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="special">Special</button>
                <button class="filter-btn" data-filter="travel">✈️ Travel</button>'''
    elif area_id == "charr":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>'''
    elif area_id == "sshiver":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="endgame">🏆 Endgame</button>'''
    elif area_id == "depths":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>
                <button class="filter-btn" data-filter="travel">✈️ Travel</button>'''
    elif area_id == "wik":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>'''
    elif area_id == "hotn":
        h += '''
                <button class="filter-btn" data-filter="side">Side</button>'''
    elif area_id == "woc":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>'''
    elif area_id == "bmp":
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>'''
    else:
        h += '''
                <button class="filter-btn" data-filter="mission">Mission</button>
                <button class="filter-btn" data-filter="side">Side</button>'''
    
    h += '''
            </div>
            
            <div class="container">
            <table class="has-checkbox-first">
                <thead>
                    <tr>
                        <th style="width:50px">Done</th>
                        <th style="width:40px">HM</th>
                        <th style="width:50px">Bonus</th>
                        <th style="width:50px">HM+B</th>
                        <th style="width:40px">#</th>
                        <th>Quest</th>
                        <th>Giver</th>
                        <th>Location</th>
                        <th>Type</th>
                        <th>Profession</th>
                        <th>Prerequisite</th>
                        <th>Reward</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for q in quests:
        row_cls = type_class.get(q['type'], "")
        prof = q['profession']
        wiki_name = q['name'].replace("'", "%27").replace(" ", "_").replace("(", "%28").replace(")", "%29")
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki_name}"
        badge = badge_class.get(q['type'], 'badge-side')
        prof_badge = f'<span class="prof {prof_class.get(prof, "")}">{prof}</span>' if prof else ''

        prereq = q.get('prereq', '')
        if isinstance(prereq, str):
            prereq = prereq.strip()

        # Clarify campaign prerequisites (ownership/access) vs. origin-locking.
        # Only touch values that are purely campaign names or campaign combinations.
        campaign_prereqs = {
            'Prophecies',
            'Factions',
            'Nightfall',
            'Eye of the North',
            'Prophecies/Factions',
            'Prophecies/Nightfall',
            'Factions/Nightfall',
        }
        if prereq in campaign_prereqs and not prereq.startswith('Requires '):
            prereq = f'Requires {prereq}'

        # Missable quest: Message from a Friend (only in Pre-Searing list)
        missable_attr = ''
        missable_badge = ''
        if area_id == "pre" and q['name'] == "Message from a Friend":
            missable_attr = ' data-missable="1"'
            missable_badge = '<span class="badge badge-missable">Missable</span>'
        
        # HM und Bonus checkboxes nur für Missions
        is_mission = q['type'] == 'Mission'
        hm_cell = f'<input type="checkbox" class="hm-checkbox" data-id="{q["id"]}-hm" data-area="{area_id}">' if is_mission else ''
        bonus_cell = f'<input type="checkbox" class="bonus-checkbox" data-id="{q["id"]}-bonus" data-area="{area_id}">' if is_mission else ''
        hm_bonus_cell = f'<input type="checkbox" class="hm-bonus-checkbox" data-id="{q["id"]}-hm-bonus" data-area="{area_id}">' if is_mission else ''

        # Reforged Mode badge in the quest name cell (matches the deployed site)
        reforged_badge = '<br><span class="prereq"><img src="https://wiki.guildwars.com/images/1/19/ReforgedMode-Small.png" alt="" style="height:14px;width:auto;vertical-align:-2px;margin-right:3px;"> Reforged Mode</span>' if q['id'] in REFORGED_QUEST_IDS else ''
        reforged_attr = ' data-reforged="1"' if q['id'] in REFORGED_QUEST_IDS else ''

        h += f'''
                    <tr class="{row_cls}" data-id="{q['id']}" data-type="{q['type'].lower()}" data-prof="{prof}" data-area="{area_id}"{missable_attr}{reforged_attr}>
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{q['id']}" data-area="{area_id}"></td>
                        <td class="checkbox-cell">{hm_cell}</td>
                        <td class="checkbox-cell">{bonus_cell}</td>
                        <td class="checkbox-cell">{hm_bonus_cell}</td>
                        <td class="order">{q['order']}</td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{q['name']}</a>{reforged_badge}</td>
                        <td>{q['giver']}</td>
                        <td class="location">{q['location']}</td>
                        <td><span class="badge {badge}">{q['type']}</span>{missable_badge}</td>
                        <td>{prof_badge}</td>
                        <td class="prereq">{prereq}</td>
                        <td class="reward">{q['reward']}</td>
                    </tr>'''
    
    h += f'''
                </tbody>
            </table>
            </div>
            <button class="reset-btn" onclick="resetProgress('{area_id}')">{area_name} Progress Reset</button>
        </div>
    </div>'''
    return h

html += generate_area_html(pre_quests, "pre", "Pre-Searing", True)
html += generate_area_html(post_quests, "post", "Post-Searing Ascalon", False)
html += generate_area_html(shiver_quests, "shiver", "Northern Shiverpeaks", False)
html += generate_area_html(kryta_quests, "kryta", "Kryta", False)
html += generate_area_html(maguuma_quests, "maguuma", "Maguuma Jungle", False)
html += generate_area_html(desert_quests, "desert", "Crystal Desert", False)
html += generate_area_html(sshiver_quests, "sshiver", "Southern Shiverpeaks", False)
html += generate_area_html(fire_quests, "fire", "Ring of Fire Islands", False)

# === FACTIONS ===
html += generate_area_html(shingjea_quests, "shingjea", "Shing Jea Island", False)
html += generate_area_html(kaineng_quests, "kaineng", "Kaineng City", False)
html += generate_area_html(echovald_quests, "echovald", "Echovald Forest (Kurzick)", False)
html += generate_area_html(jadesea_quests, "jadesea", "The Jade Sea (Luxon)", False)

# === NIGHTFALL ===
html += generate_area_html(istan_quests, "istan", "Istan", False)
html += generate_area_html(kourna_quests, "kourna", "Kourna", False)
html += generate_area_html(vabbi_quests, "vabbi", "Vabbi", False)
html += generate_area_html(desolation_quests, "desolation", "The Desolation", False)
html += generate_area_html(torment_quests, "torment", "Realm of Torment", False)

# === EYE OF THE NORTH ===
html += generate_area_html(fshiver_quests, "fshiver", "Far Shiverpeaks", False)
html += generate_area_html(charr_quests, "charr", "Charr Homelands", False)
html += generate_area_html(tarnished_quests, "tarnished", "Tarnished Coast", False)
html += generate_area_html(depths_quests, "depths", "Depths of Tyria", False)

# === BEYOND ===
html += generate_area_html(wik_quests, "wik", "War in Kryta", False)
html += generate_area_html(hotn_quests, "hotn", "Hearts of the North", False)
html += generate_area_html(woc_quests, "woc", "Winds of Change", False)

# === BONUS MISSION PACK ===
html += generate_area_html(bmp_quests, "bmp", "Bonus Mission Pack", False)

# === TITLES DATA ===
TITLES = [
    # (id, name, wiki_name, max_rank, max_points, type, campaign, description)
    # Account Titles
    ("lucky", "Lucky", "Lucky", 7, 2500000, "account", "Core", "Lucky points"),
    ("unlucky", "Unlucky", "Unlucky", 7, 500000, "account", "Core", "Unlucky points"),
    ("treasure", "Treasure Hunter", "Treasure_Hunter", 8, 10000, "account", "Core", "Chests opened"),
    ("wisdom", "Wisdom", "Wisdom", 8, 10000, "account", "Core", "Golds identified"),
    ("sweet", "Sweet Tooth", "Sweet_Tooth", 7, 10000, "account", "Core", "Sweets consumed"),
    ("party", "Party Animal", "Party_Animal", 7, 10000, "account", "Core", "Party items used"),
    ("drunk", "Drunkard", "Drunkard", 7, 10000, "account", "Core", "Minutes drunk"),
    # Prophecies
    ("ldoa", "Legendary Defender of Ascalon", "Defender_of_Ascalon", 1, 1, "pve", "Prophecies", "Level 20 Pre-Searing"),
    ("prot_tyria", "Protector of Tyria", "Protector_of_Tyria", 1, 25, "pve", "Prophecies", "All missions + bonus"),
    ("guard_tyria", "Guardian of Tyria", "Guardian_of_Tyria", 1, 25, "pve", "Prophecies", "All HM + bonus"),
    ("cart_tyria", "Tyrian Cartographer", "Tyrian_Cartographer", 1, 100, "pve", "Prophecies", "100% map"),
    ("skill_tyria", "Tyrian Skill Hunter", "Skill_Hunter", 1, 90, "pve", "Prophecies", "All elites captured"),
    ("vanq_tyria", "Tyrian Vanquisher", "Vanquisher", 1, 54, "pve", "Prophecies", "All areas vanquished"),
    # Factions
    ("prot_cantha", "Protector of Cantha", "Protector_of_Cantha", 1, 13, "pve", "Factions", "All missions + bonus"),
    ("guard_cantha", "Guardian of Cantha", "Guardian_of_Cantha", 1, 13, "pve", "Factions", "All HM + bonus"),
    ("cart_cantha", "Canthan Cartographer", "Canthan_Cartographer", 1, 100, "pve", "Factions", "100% map"),
    ("skill_cantha", "Canthan Skill Hunter", "Skill_Hunter", 1, 120, "pve", "Factions", "All elites captured"),
    ("vanq_cantha", "Canthan Vanquisher", "Vanquisher", 1, 33, "pve", "Factions", "All areas vanquished"),
    # Nightfall
    ("prot_elona", "Protector of Elona", "Protector_of_Elona", 1, 20, "pve", "Nightfall", "All missions + bonus"),
    ("guard_elona", "Guardian of Elona", "Guardian_of_Elona", 1, 20, "pve", "Nightfall", "All HM + bonus"),
    ("cart_elona", "Elonian Cartographer", "Elonian_Cartographer", 1, 100, "pve", "Nightfall", "100% map"),
    ("skill_elona", "Elonian Skill Hunter", "Skill_Hunter", 1, 140, "pve", "Nightfall", "All elites captured"),
    ("vanq_elona", "Elonian Vanquisher", "Vanquisher", 1, 34, "pve", "Nightfall", "All areas vanquished"),
    ("sunspear", "Sunspear General", "Sunspear_rank", 10, 50000, "pve", "Nightfall", "Sunspear points"),
    ("lightbringer", "Lightbringer", "Lightbringer_rank", 8, 50000, "pve", "Nightfall", "LB points"),
    # EotN
    ("master_north", "Master of the North", "Master_of_the_North", 1, 18, "pve", "EotN", "All dungeons HM"),
    ("ebon", "Ebon Vanguard", "Ebon_Vanguard_rank", 10, 160000, "pve", "EotN", "Ebon points"),
    ("deldrimor", "Deldrimor", "Deldrimor_rank", 10, 160000, "pve", "EotN", "Deldrimor points"),
    ("norn", "Norn", "Norn_rank", 10, 160000, "pve", "EotN", "Norn points"),
    ("asura", "Asura", "Asura_rank", 10, 160000, "pve", "EotN", "Asura points"),
    # Legendary
    ("leg_cart", "Legendary Cartographer", "Cartographer", 1, 3, "legendary", "Core", "All 3 Cartographers"),
    ("leg_guard", "Legendary Guardian", "Guardian", 1, 3, "legendary", "Core", "All 3 Guardians"),
    ("leg_skill", "Legendary Skill Hunter", "Skill_Hunter", 1, 3, "legendary", "Core", "All 3 Skill Hunters"),
    ("leg_vanq", "Legendary Vanquisher", "Vanquisher", 1, 3, "legendary", "Core", "All 3 Vanquishers"),
    ("survivor1", "Survivor (Tier 1)", "Survivor", 1, 140600, "legendary", "Core", "140,600 XP without dying"),
    ("survivor2", "Survivor (Tier 2)", "Survivor", 2, 587500, "legendary", "Core", "587,500 XP without dying"),
    ("survivor3", "Survivor (Tier 3 - Max)", "Survivor", 3, 1337500, "legendary", "Core", "1,337,500 XP without dying"),
]

def generate_titles_html():
    type_badges = {"account": ("badge-special", "Account"), "pve": ("badge-main", "PvE"), "legendary": ("badge-endgame", "Legendary")}
    type_classes = {"account": "type-special", "pve": "type-main", "legendary": "type-endgame"}
    
    h = '''
    <div class="area" id="area-titles">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🏆 GWAMM Progress (30 Titles needed)</span>
                    <span class="progress-count"><span id="titles-completed">0</span> / <span id="titles-total">30</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="titles-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="titles">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="account">Account</button>
                <button class="filter-btn" data-filter="pve">PvE</button>
                <button class="filter-btn" data-filter="legendary">Legendary</button>
                <span style="width:30px"></span>
                <input type="file" id="toolbox-file" accept=".json" onchange="importToolboxFile(event)" style="display:none">
                <button class="io-btn import" onclick="document.getElementById('toolbox-file').click()">📁 Import JSON</button>
                <span id="toolbox-status" style="color:#8b949e;font-size:0.85em;"></span>
            </div>
            
            <div class="container">
            <table>
                <thead>
                    <tr>
                        <th style="width:50px">Max</th>
                        <th>Title</th>
                        <th style="width:200px">Progress</th>
                        <th>Type</th>
                        <th>Campaign</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for t in TITLES:
        tid, name, wiki, max_rank, max_pts, ttype, campaign, desc = t
        badge_cls, badge_text = type_badges.get(ttype, ("badge-side", ttype))
        row_cls = type_classes.get(ttype, "")
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        
        # Legendary titles have auto-calculated progress, no manual input
        if ttype == "legendary" and tid in ("leg_cart", "leg_guard", "leg_skill", "leg_vanq"):
            progress_html = f'''
                            <span style="color:#8b949e;font-style:italic;">Auto-calculated</span>'''
        else:
            progress_html = f'''
                            <div style="display:flex;align-items:center;gap:8px;">
                                <input type="number" class="title-progress-input" data-id="title_{tid}" data-max="{max_pts}" min="0" max="{max_pts}" value="0" style="width:70px;padding:4px;background:#161b22;color:#c9d1d9;border:1px solid #30363d;border-radius:4px;">
                                <span style="color:#8b949e;">/ {max_pts:,}</span>
                            </div>
                            <div class="progress-bar" style="height:6px;margin-top:4px;">
                                <div class="progress-fill title-progress-bar" data-id="title_{tid}" style="width:0%;"></div>
                            </div>'''
        
        h += f'''
                    <tr class="{row_cls}" data-type="{ttype}" data-area="titles" data-id="title_{tid}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="title_{tid}" data-area="titles"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{name}</a><br><span class="prereq">{desc}</span></td>
                        <td>{progress_html}
                        </td>
                        <td><span class="badge {badge_cls}">{badge_text}</span></td>
                        <td>{campaign}</td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            </div>
        </div>
    </div>'''
    return h

html += generate_titles_html()

# === HEROES ===
def generate_heroes_html():
    h = '''
    <div class="area" id="area-heroes">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🦸 Heroes (''' + str(len(HEROES)) + ''' total)</span>
                    <span class="progress-count"><span id="heroes-completed">0</span> / <span id="heroes-total">''' + str(len(HEROES)) + '''</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="heroes-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="heroes">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="nightfall">Nightfall</button>
                <button class="filter-btn" data-filter="eye of the north">Eye of the North</button>
                <button class="filter-btn" data-filter="beyond">Beyond</button>
                <button class="filter-btn" data-filter="special">Special</button>
            </div>
            
            <div class="container">
            <table>
                <thead>
                    <tr>
                        <th style="width:50px">Got</th>
                        <th>Hero</th>
                        <th>Profession</th>
                        <th>Region</th>
                        <th style="width:220px">Armor</th>
                        <th>Unlock Quest</th>
                    </tr>
                </thead>
                <tbody>'''
    
    # Group by campaign
    for hero in HEROES:
        name, profession, campaign, region, quest, wiki, hero_img = hero
        hero_id = f"hero_{name.lower().replace(' ', '_').replace('.', '')}"
        hero_reforged = ' data-reforged="1"' if name in ("Devona", "Ghost of Althea") else ''
        icon = HERO_PROFESSIONS.get(profession, "")
        campaign_lower = campaign.lower()
        region_lower = region.lower()
        
        # Badge color based on campaign
        badge_class = {
            "Nightfall": "badge-main",
            "Eye of the North": "badge-special", 
            "Beyond": "badge-endgame",
            "Bonus": "badge-side",
            "Factions": "badge-profession"
        }.get(campaign, "badge-side")
        
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        quest_url = f"https://wiki.guildwars.com/wiki/{quest.replace(' ', '_')}"
        # Explicit harvested portrait URL (from heroes.py — GWW infobox image).
        # Fall back to override / constructed path only if an explicit URL is missing.
        if not hero_img:
            override_file = HERO_IMAGE_OVERRIDES.get(wiki)
            hero_img = f"https://wiki.guildwars.com/wiki/Special:FilePath/{override_file or wiki + '.jpg'}"
        
        # Hero armor variants (non-exclusive toggles), based on campaign
        variants = []
        if campaign == "Nightfall":
            variants = ["Sunspear", "Ancient", "Primeval"]
        elif campaign == "Eye of the North":
            variants = ["Brotherhood", "Deldrimor", "Mysterious"]
        else:
            variants = []
        
        if variants:
            armor_items = []
            for v in variants:
                armor_id = f"{hero_id}_armor_{v.lower()}"
                info = HERO_ARMOR.get(v, {})
                loc = info.get("location", "")
                cost = info.get("cost", "")
                tip = f"{v} — {loc} ({cost})".strip()
                armor_items.append(f'''<label title="{tip}" style="display:inline-flex;align-items:center;gap:6px;margin-right:10px;color:#8b949e;">
                    <input type="checkbox" class="armor-checkbox" data-id="{armor_id}" data-hero="{hero_id}" data-variant="{v.lower()}" style="width:18px;height:18px;accent-color:#58a6ff;">
                    <span>{v}</span>
                </label>''')
            armor_html = '<div class="hero-armor-wrap">' + ''.join(armor_items) + '</div>'
        else:
            armor_html = '<span style="color:#8b949e;">—</span>'
        
        h += f'''
                    <tr data-type="{campaign_lower}" data-area="heroes" data-region="{region_lower}" data-id="{hero_id}"{hero_reforged}>
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{hero_id}" data-area="heroes"></td>
                        <td>
                            <div style="display:flex;align-items:center;gap:8px;">
                                <div style="width:120px;height:120px;border-radius:10px;overflow:hidden;background:#0d1117;border:1px solid #30363d;display:flex;align-items:center;justify-content:center;flex:0 0 auto;">
                                    <img src="{hero_img}" alt="{name}" referrerpolicy="no-referrer" loading="lazy" style="width:100%;height:100%;object-fit:contain;display:block;background:#0d1117;" onerror="this.onerror=null; this.src='https://wiki.guildwars.com/wiki/Special:FilePath/{wiki}.png'; this.onerror=function(){{this.src='https://wiki.guildwars.com/wiki/Special:FilePath/{wiki}.gif'; this.onerror=function(){{this.style.display='none'; var f=this.parentNode.querySelector('.hero-fallback'); if(f) f.style.display='inline-flex';}}}}">
                                    <span class="hero-fallback" style="display:none;width:100%;height:100%;align-items:center;justify-content:center;color:#c9d1d9;font-weight:600;">{name[0]}</span>
                                </div>
                                <a href="{wiki_url}" target="_blank" class="quest-link">{name}</a>
                            </div>
                        </td>
                        <td style="color:#ffa657;">{prof_icon_img(profession)} {profession}</td>
                        <td>{region}</td>
                        <td>{armor_html}</td>
                        <td><a href="{quest_url}" target="_blank" style="color:#8b949e;">{quest}</a></td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            </div>
            
            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#ffa657;margin:0 0 10px 0;">💡 Hero Armor for HoM</h4>
                <ul style="margin:0;padding-left:1.2em;color:#8b949e;font-size:0.9em;">
                    <li><strong>Sunspear/Primeval</strong> - Gate of Pain (15 Boss Bounties)</li>
                    <li><strong>Ancient</strong> - Gate of Anguish (Passages + Gems)</li>
                    <li><strong>Brotherhood/Deldrimor/Mysterious</strong> - Eye of the North (Cloth/Steel)</li>
                </ul>
            </div>
        </div>
    </div>'''
    return h

html += generate_heroes_html()

# === DAILY QUESTS ===
def generate_daily_html():
    from datetime import datetime
    import json

    # Server-side initial values (the daily tab's JS recomputes the authoritative,
    # UTC-reset rotation client-side on open via the arrays emitted below).
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    mission = ZAISHEN_MISSIONS[(today - ZAISHEN_MISSION_START).days % len(ZAISHEN_MISSIONS)]
    bounty = ZAISHEN_BOUNTIES[(today - ZAISHEN_BOUNTY_START).days % len(ZAISHEN_BOUNTIES)]
    vanquish = ZAISHEN_VANQUISHES[(today - ZAISHEN_VANQUISH_START).days % len(ZAISHEN_VANQUISHES)]
    combat = ZAISHEN_COMBAT[(today - ZAISHEN_COMBAT_START).days % len(ZAISHEN_COMBAT)]
    vanguard = VANGUARD_QUESTS[(today - datetime(2025, 11, 26)).days % len(VANGUARD_QUESTS)]

    h = f'''
    <div class="area" id="area-daily">
        <div class="content">
            <div style="text-align:center;margin-bottom:30px;">
                <h2 style="color:#ffd700;margin:0;">📅 Today's Daily Quests</h2>
                <p id="daily-date" style="color:#8b949e;margin:5px 0;">Loading daily date…</p>
            </div>

            <div style="max-width:600px;margin:0 auto;">
                <h3 style="color:#ffa657;margin:0 0 15px 0;">⚔️ Zaishen Dailies</h3>

                <div style="background:#21262d;border-radius:12px;overflow:hidden;">
                    <!-- Mission -->
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;border-bottom:1px solid #30363d;">
                        <input type="checkbox" id="daily-mission" class="quest-checkbox" style="width:22px;height:22px;" data-daily="mission">
                        <div style="flex:1;">
                            <span style="color:#238636;font-weight:bold;">🗺️ Mission:</span>
                            <a id="daily-mission-link" href="https://wiki.guildwars.com/wiki/{mission[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{mission[0]}</a>
                            <span id="daily-mission-campaign" style="color:#8b949e;font-size:0.85em;margin-left:8px;">({mission[1]})</span>
                        </div>
                    </div>

                    <!-- Bounty -->
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;border-bottom:1px solid #30363d;">
                        <input type="checkbox" id="daily-bounty" class="quest-checkbox" style="width:22px;height:22px;" data-daily="bounty">
                        <div style="flex:1;">
                            <span style="color:#1f6feb;font-weight:bold;">🎯 Bounty:</span>
                            <a id="daily-bounty-link" href="https://wiki.guildwars.com/wiki/{bounty[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{bounty[0]}</a>
                            <span id="daily-bounty-campaign" style="color:#8b949e;font-size:0.85em;margin-left:8px;">({bounty[1]})</span>
                        </div>
                    </div>

                    <!-- Vanquish -->
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;border-bottom:1px solid #30363d;">
                        <input type="checkbox" id="daily-vanquish" class="quest-checkbox" style="width:22px;height:22px;" data-daily="vanquish">
                        <div style="flex:1;">
                            <span style="color:#f85149;font-weight:bold;">⚔️ Vanquish:</span>
                            <a id="daily-vanquish-link" href="https://wiki.guildwars.com/wiki/{vanquish[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{vanquish[0]}</a>
                            <span id="daily-vanquish-campaign" style="color:#8b949e;font-size:0.85em;margin-left:8px;">({vanquish[1]})</span>
                        </div>
                    </div>

                    <!-- Combat/PvP -->
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;">
                        <input type="checkbox" id="daily-combat" class="quest-checkbox" style="width:22px;height:22px;" data-daily="combat">
                        <div style="flex:1;">
                            <span style="color:#a855f7;font-weight:bold;">🏆 PvP:</span>
                            <a id="daily-combat-link" href="https://wiki.guildwars.com/wiki/{combat[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{combat[0]}</a>
                        </div>
                    </div>
                </div>

                <h3 style="color:#ffa657;margin:25px 0 15px 0;">🛡️ Pre-Searing Vanguard</h3>
                <div style="background:#21262d;border-radius:12px;overflow:hidden;">
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;">
                        <input type="checkbox" id="daily-vanguard" class="quest-checkbox" style="width:22px;height:22px;" data-daily="vanguard">
                        <div style="flex:1;">
                            <span style="color:#ffa657;font-weight:bold;">🛡️ Vanguard:</span>
                            <a id="daily-vanguard-link" href="https://wiki.guildwars.com/wiki/{vanguard[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{vanguard[0]}</a>
                            <span id="daily-vanguard-region" style="color:#8b949e;font-size:0.85em;margin-left:8px;">({vanguard[2]})</span>
                        </div>
                    </div>
                </div>

                <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                    <h4 style="color:#8b949e;margin:0 0 10px 0;">💡 Tips</h4>
                    <ul style="margin:0;padding-left:1.2em;color:#8b949e;font-size:0.85em;">
                        <li>Zaishen Coins → Balthazar faction, lockpicks, tomes</li>
                        <li>Checkboxes reset daily</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>'''

    # Client-side rotation data (generated from data/daily_quests.py) + logic.
    # updateTodaysZaishen() in the main script calls updateDailyRotation()/updateDailyDate()
    # when the daily tab opens; these globals are initialized at page load.
    def _arr(varname, rows):
        items = ",\n            ".join(
            "{ name: %s, campaign: %s, region: %s, wiki: %s }" % (
                json.dumps(r[0]), json.dumps(r[1]), json.dumps(r[2]), json.dumps(r[3]))
            for r in rows)
        return "        const %s = [\n            %s\n        ];\n" % (varname, items)

    data_js = (
        "        const ZAISHEN_MISSION_START_UTC = Date.UTC(2025, 10, 26);\n"
        "        const ZAISHEN_BOUNTY_START_UTC = Date.UTC(2025, 10, 20);\n"
        "        const ZAISHEN_VANQUISH_START_UTC = Date.UTC(2025, 8, 9);\n"
        "        const ZAISHEN_COMBAT_START_UTC = Date.UTC(2025, 10, 27);\n"
        "        const VANGUARD_START_UTC = Date.UTC(2025, 10, 26);\n"
        + _arr("ZAISHEN_MISSIONS_DATA", ZAISHEN_MISSIONS)
        + _arr("ZAISHEN_BOUNTIES_DATA", ZAISHEN_BOUNTIES)
        + _arr("ZAISHEN_VANQUISHES_DATA", ZAISHEN_VANQUISHES)
        + _arr("ZAISHEN_COMBAT_DATA", ZAISHEN_COMBAT)
        + _arr("VANGUARD_QUESTS_DATA", VANGUARD_QUESTS)
    )

    logic_js = '''
        function getUtcDayOffset(startUtc) {
            const RESET_HOUR_UTC = 16;
            const RESET_MINUTE_UTC = 1;
            const resetOffsetMs = ((RESET_HOUR_UTC * 60) + RESET_MINUTE_UTC) * 60 * 1000;
            const now = new Date();
            const shiftedNow = now.getTime() - resetOffsetMs;
            return Math.floor((shiftedNow - startUtc) / 86400000);
        }
        function updateDailyDate() {
            const el = document.getElementById('daily-date');
            if (!el) return;
            const now = new Date();
            const weekday = now.toLocaleDateString('en-US', { weekday: 'long', timeZone: 'UTC' });
            const month = now.toLocaleDateString('en-US', { month: 'long', timeZone: 'UTC' });
            const day = now.toLocaleDateString('en-US', { day: 'numeric', timeZone: 'UTC' });
            const year = now.toLocaleDateString('en-US', { year: 'numeric', timeZone: 'UTC' });
            // Reset is fixed at 16:01 UTC; the Pacific wall-clock time shifts with DST (8:01 PST / 9:01 PDT)
            const resetUtc = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 16, 1));
            const pacific = resetUtc.toLocaleTimeString('en-US', { timeZone: 'America/Los_Angeles', hour: 'numeric', minute: '2-digit', timeZoneName: 'short' });
            el.textContent = `${weekday}, ${month} ${day}, ${year} • Resets at 16:01 UTC (${pacific})`;
        }
        function updateDailyRotation() {
            const missionLink = document.getElementById('daily-mission-link');
            const missionCampaign = document.getElementById('daily-mission-campaign');
            const bountyLink = document.getElementById('daily-bounty-link');
            const bountyCampaign = document.getElementById('daily-bounty-campaign');
            const vanquishLink = document.getElementById('daily-vanquish-link');
            const vanquishCampaign = document.getElementById('daily-vanquish-campaign');
            const combatLink = document.getElementById('daily-combat-link');
            const vanguardLink = document.getElementById('daily-vanguard-link');
            const vanguardRegion = document.getElementById('daily-vanguard-region');

            if (missionLink && missionCampaign && ZAISHEN_MISSIONS_DATA.length) {
                const days = getUtcDayOffset(ZAISHEN_MISSION_START_UTC);
                const idx = ((days % ZAISHEN_MISSIONS_DATA.length) + ZAISHEN_MISSIONS_DATA.length) % ZAISHEN_MISSIONS_DATA.length;
                const m = ZAISHEN_MISSIONS_DATA[idx];
                missionLink.href = 'https://wiki.guildwars.com/wiki/' + m.wiki;
                missionLink.textContent = m.name;
                missionCampaign.textContent = '(' + m.campaign + ')';
            }

            if (bountyLink && bountyCampaign && ZAISHEN_BOUNTIES_DATA.length) {
                const days = getUtcDayOffset(ZAISHEN_BOUNTY_START_UTC);
                const idx = ((days % ZAISHEN_BOUNTIES_DATA.length) + ZAISHEN_BOUNTIES_DATA.length) % ZAISHEN_BOUNTIES_DATA.length;
                const b = ZAISHEN_BOUNTIES_DATA[idx];
                bountyLink.href = 'https://wiki.guildwars.com/wiki/' + b.wiki;
                bountyLink.textContent = b.name;
                bountyCampaign.textContent = '(' + b.campaign + ')';
            }

            if (vanquishLink && vanquishCampaign && ZAISHEN_VANQUISHES_DATA.length) {
                const days = getUtcDayOffset(ZAISHEN_VANQUISH_START_UTC);
                const idx = ((days % ZAISHEN_VANQUISHES_DATA.length) + ZAISHEN_VANQUISHES_DATA.length) % ZAISHEN_VANQUISHES_DATA.length;
                const v = ZAISHEN_VANQUISHES_DATA[idx];
                vanquishLink.href = 'https://wiki.guildwars.com/wiki/' + v.wiki;
                vanquishLink.textContent = v.name;
                vanquishCampaign.textContent = '(' + v.campaign + ')';
            }

            if (combatLink && ZAISHEN_COMBAT_DATA.length) {
                const days = getUtcDayOffset(ZAISHEN_COMBAT_START_UTC);
                const idx = ((days % ZAISHEN_COMBAT_DATA.length) + ZAISHEN_COMBAT_DATA.length) % ZAISHEN_COMBAT_DATA.length;
                const c = ZAISHEN_COMBAT_DATA[idx];
                combatLink.href = 'https://wiki.guildwars.com/wiki/' + c.wiki;
                combatLink.textContent = c.name;
            }

            if (vanguardLink && vanguardRegion && VANGUARD_QUESTS_DATA.length) {
                const days = getUtcDayOffset(VANGUARD_START_UTC);
                const idx = ((days % VANGUARD_QUESTS_DATA.length) + VANGUARD_QUESTS_DATA.length) % VANGUARD_QUESTS_DATA.length;
                const q = VANGUARD_QUESTS_DATA[idx];
                vanguardLink.href = 'https://wiki.guildwars.com/wiki/' + q.wiki;
                vanguardLink.textContent = q.name;
                vanguardRegion.textContent = '(' + q.region + ')';
            }
        }
'''
    return h + '\n    <script>\n' + data_js + logic_js + '    </script>\n'

html += generate_daily_html()

# === MISSIONS ===
def generate_missions_html():
    h = '''
    <div class="area" id="area-missions">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🗺️ Story Missions (''' + str(len(ALL_MISSIONS)) + ''' total)</span>
                    <span class="progress-count"><span id="missions-completed">0</span> / <span id="missions-total">''' + str(len(ALL_MISSIONS)) + '''</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="missions-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="missions">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="prophecies">Prophecies (''' + str(len(PROPHECIES_MISSIONS)) + ''')</button>
                <button class="filter-btn" data-filter="factions">Factions (''' + str(len(FACTIONS_MISSIONS)) + ''')</button>
                <button class="filter-btn" data-filter="nightfall">Nightfall (''' + str(len(NIGHTFALL_MISSIONS)) + ''')</button>
            </div>
            
            <div class="container">'''
    
    # Group by campaign
    campaigns = [
        ("Prophecies", PROPHECIES_MISSIONS, "badge-main"),
        ("Factions", FACTIONS_MISSIONS, "badge-special"),
        ("Nightfall", NIGHTFALL_MISSIONS, "badge-endgame"),
    ]
    
    for campaign_name, missions, badge_class in campaigns:
        campaign_lower = campaign_name.lower()
        h += f'''
            <h3 style="color:#58a6ff;margin:20px 0 10px 0;">🗺️ {campaign_name} ({len(missions)} missions)</h3>
            <table class="has-checkbox-first">
                <thead>
                    <tr>
                        <th style="width:50px">Done</th>
                        <th style="width:50px">Bonus</th>
                        <th style="width:50px">HM</th>                        <th style="width:50px"><span title="Hard Mode + Bonus/Masters">HM+B</span></th>
                        <th>Mission</th>
                        <th>Region</th>
                    </tr>
                </thead>
                <tbody>'''
        
        for mission in missions:
            name, region, campaign, wiki = mission
            mission_id = f"mission_{name.lower().replace(' ', '_').replace(chr(39), '')}"
            bonus_id = f"bonus_{name.lower().replace(' ', '_').replace(chr(39), '')}"
            hm_id = f"hm_{name.lower().replace(' ', '_').replace(chr(39), '')}"
            hm_bonus_id = f"hm_bonus_{name.lower().replace(' ', '_').replace(chr(39), '')}"
            region_icon = MISSION_REGIONS.get(region, "🗺️")
            wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"

            # Availability rules
            has_bonus = True
            has_hm = True
            has_hm_bonus = True
            if campaign_name == 'Prophecies' and region == 'Pre-Searing' and name == 'Ascalon Academy':
                has_bonus = False
                has_hm = False
                has_hm_bonus = False

            bonus_cell = f'<input type="checkbox" class="quest-checkbox" data-id="{bonus_id}" data-area="missions" title="Bonus/Masters" style="accent-color:#ffa657;">' if has_bonus else ''
            hm_cell = f'<input type="checkbox" class="quest-checkbox" data-id="{hm_id}" data-area="missions" title="Hard Mode" style="accent-color:#ff6b6b;">' if has_hm else ''
            hmb_cell = f'<input type="checkbox" class="hm-bonus-checkbox" data-id="{hm_bonus_id}" data-area="missions" title="Hard Mode + Bonus/Masters" style="accent-color:#d97706;">' if (has_hm and has_bonus and has_hm_bonus) else ''

            h += f'''
                    <tr data-type="{campaign_lower}" data-area="missions" data-id="{mission_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{mission_id}" data-area="missions" title="Normal Mode"></td>
                        <td class="checkbox-cell">{bonus_cell}</td>
                        <td class="checkbox-cell">{hm_cell}</td>
                        <td class="checkbox-cell">{hmb_cell}</td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{name}</a></td>
                        <td style="color:#8b949e;">{region_icon} {region}</td>
                    </tr>'''
        
        h += '''
                </tbody>
            </table>'''
    
    h += '''
            </div>
            
            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#58a6ff;margin:0 0 10px 0;">💡 Mission Objectives</h4>
                <ul style="margin:0;padding-left:1.2em;color:#8b949e;font-size:0.9em;">
                    <li><strong>✅ Done</strong> - Completed mission in Normal Mode</li>
                    <li><strong>🟠 Bonus</strong> - Completed bonus objective (Masters in Factions/Nightfall)</li>
                    <li><strong>🔴 HM</strong> - Completed in Hard Mode (for Guardian title)</li>
                    <li><strong>Protector</strong> - All bonuses in Normal Mode</li>
                    <li><strong>Guardian</strong> - All missions in Hard Mode</li>
                </ul>
            </div>
        </div>
    </div>'''
    return h

html += generate_missions_html()

# === DUNGEONS & ELITE MISSIONS ===
def generate_dungeons_html():
    total_content = len(ELITE_MISSIONS) + len(EOTN_DUNGEONS)
    h = '''
    <div class="area" id="area-dungeons">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🏰 Elite Missions & Dungeons (''' + str(total_content) + ''' total)</span>
                    <span class="progress-count"><span id="dungeons-completed">0</span> / <span id="dungeons-total">''' + str(total_content) + '''</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="dungeons-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="dungeons">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="elite">⚔️ Elite Missions</button>
                <button class="filter-btn" data-filter="dungeon">🏔️ EotN Dungeons</button>
            </div>
            
            <div class="container">
            
            <!-- ELITE MISSIONS -->
            <h3 style="color:#ff6b6b;margin:15px 0 10px 0;">⚔️ Elite Missions (End-Game Content)</h3>
            <table class="has-checkbox-first">
                <thead>
                    <tr>
                        <th style="width:50px">Done</th>
                        <th>Mission</th>
                        <th>Campaign</th>
                        <th>Party Size</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for mission in ELITE_MISSIONS:
        name, campaign, party_size, desc, wiki = mission
        mission_id = f"elite_{name.lower().replace(' ', '_').replace(chr(39), '')}"
        icon = CAMPAIGN_ICONS.get(campaign, "🌐")
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        
        badge_class = {
            "Core": "badge-side",
            "Prophecies": "badge-main",
            "Factions": "badge-special",
            "Nightfall": "badge-endgame",
        }.get(campaign, "badge-side")
        
        elite_reforged = ' data-reforged="1"' if name in ("Forsaken Tunnels", "Tunnels of the Forsaken") else ''
        h += f'''
                    <tr data-type="elite" data-area="dungeons" data-id="{mission_id}"{elite_reforged}>
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{mission_id}" data-area="dungeons"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link" style="color:#ff6b6b;">{icon} {name}</a></td>
                        <td><span class="badge {badge_class}">{campaign}</span></td>
                        <td style="color:#8b949e;text-align:center;">{party_size} players</td>
                        <td style="font-size:0.85em;color:#8b949e;">{desc}</td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            
            <!-- EOTN DUNGEONS -->
            <h3 style="color:#58a6ff;margin:25px 0 10px 0;">🏔️ Eye of the North Dungeons (18)</h3>
            <table class="has-checkbox-first">
                <thead>
                    <tr>
                        <th style="width:50px">Done</th>
                        <th>Dungeon</th>
                        <th>Region</th>
                        <th>Floors</th>
                        <th>Final Boss</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for dungeon in EOTN_DUNGEONS:
        name, region, floors, boss, wiki = dungeon
        dungeon_id = f"dungeon_{name.lower().replace(' ', '_').replace(chr(39), '')}"
        region_icon = DUNGEON_REGIONS.get(region, "🏔️")
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        
        h += f'''
                    <tr data-type="dungeon" data-area="dungeons" data-id="{dungeon_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{dungeon_id}" data-area="dungeons"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{name}</a></td>
                        <td style="color:#8b949e;">{region_icon} {region}</td>
                        <td style="text-align:center;">{floors}</td>
                        <td style="color:#ffa657;">{boss}</td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            </div>
            
            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#58a6ff;margin:0 0 10px 0;">💡 Dungeon Tips</h4>
                <ul style="margin:0;padding-left:1.2em;color:#8b949e;font-size:0.9em;">
                    <li><strong>Dungeon Guide Mode</strong> - First completion per character gives bonus rewards</li>
                    <li><strong>Master Dungeon Guide</strong> - EotN title for completing all dungeons</li>
                    <li><strong>Slavers' Exile</strong> - Hardest dungeon, 5 separate boss areas</li>
                </ul>
            </div>
        </div>
    </div>'''
    return h

html += generate_dungeons_html()

# === VANQUISH ===
# Same-name locations that appear twice (mission outpost vs explorable area, town vs
# explorable) historically shared ONE checkbox id = one localStorage key. The emitters
# rename the second occurrence to '<id>_2'; the {new: old} map is injected into the page
# as DUP_ID_MIGRATION so saved progress is copied to the split id once on load.
DUP_ID_RENAMES = {}

def _dedup_data_id(data_id, seen):
    rid = data_id
    if data_id in seen:
        rid = data_id + '_2'
        assert rid not in seen, f"triple data-id {data_id}"
        DUP_ID_RENAMES[rid] = data_id
    seen.add(rid)
    seen.add(data_id)
    return rid

def generate_vanquish_html():
    seen_ids = set()
    h = '''
    <div class="area" id="area-vanquish">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">⚔️ Vanquish Areas (''' + str(len(ALL_VANQUISHES)) + ''' total)</span>
                    <span class="progress-count"><span id="vanquish-completed">0</span> / <span id="vanquish-total">''' + str(len(ALL_VANQUISHES)) + '''</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="vanquish-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="vanquish">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="prophecies">Prophecies (''' + str(len(PROPHECIES_VANQUISHES)) + ''')</button>
                <button class="filter-btn" data-filter="factions">Factions (''' + str(len(FACTIONS_VANQUISHES)) + ''')</button>
                <button class="filter-btn" data-filter="nightfall">Nightfall (''' + str(len(NIGHTFALL_VANQUISHES)) + ''')</button>
                <button class="filter-btn" data-filter="eye of the north">EotN (''' + str(len(EOTN_VANQUISHES)) + ''')</button>
            </div>
            
            <div class="container">'''
    
    # Group by campaign
    campaigns = [
        ("Prophecies", PROPHECIES_VANQUISHES, "badge-main"),
        ("Factions", FACTIONS_VANQUISHES, "badge-special"),
        ("Nightfall", NIGHTFALL_VANQUISHES, "badge-endgame"),
        ("Eye of the North", EOTN_VANQUISHES, "badge-profession"),
    ]
    
    for campaign_name, areas, badge_class in campaigns:
        campaign_lower = campaign_name.lower()
        h += f'''
            <h3 style="color:#ffa657;margin:20px 0 10px 0;">⚔️ {campaign_name} ({len(areas)} areas)</h3>
            <table class="has-checkbox-first">
                <thead>
                    <tr>
                        <th style="width:50px">Done</th>
                        <th>Area</th>
                        <th>Region</th>
                    </tr>
                </thead>
                <tbody>'''
        
        for area in areas:
            name, region, campaign, wiki = area
            area_id = _dedup_data_id(f"vanq_{name.lower().replace(' ', '_').replace(chr(39), '').replace(',', '')}", seen_ids)
            region_icon = VANQUISH_REGIONS.get(region, "🗺️")
            wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
            
            h += f'''
                    <tr data-type="{campaign_lower}" data-area="vanquish" data-id="{area_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{area_id}" data-area="vanquish"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{name}</a></td>
                        <td style="color:#8b949e;">{region_icon} {region}</td>
                    </tr>'''
        
        h += '''
                </tbody>
            </table>'''
    
    h += '''
            </div>
            
            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#ffa657;margin:0 0 10px 0;">💡 Vanquishing Tips</h4>
                <ul style="margin:0;padding-left:1.2em;color:#8b949e;font-size:0.9em;">
                    <li><strong>Hard Mode only</strong> - Must be in Hard Mode to vanquish</li>
                    <li><strong>Kill counter</strong> - Shows remaining enemies in top-left</li>
                    <li><strong>Vanquisher title</strong> - Complete all areas in a campaign</li>
                    <li><strong>Cartographer</strong> - Explore while vanquishing for map %</li>
                </ul>
            </div>
        </div>
    </div>'''
    return h

html += generate_vanquish_html()


def generate_cartographer_html():
    """Cartographer (mapping title) locations, grouped campaign -> region.
    Data lives in data/cartographer.py (extracted from the deployed site).
    Same-name pairs (mission/explorable, town/explorable) are distinct rows;
    their previously-shared ids are deduplicated via _dedup_data_id."""
    total = CARTOGRAPHER_TOTAL
    seen_ids = set()
    h = f'''
    <div class="area" id="area-cartographer">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">\U0001f5fa️ Cartographer Locations ({total} total)</span>
                    <span class="progress-count"><span id="cartographer-completed">0</span> / <span id="cartographer-total">{total}</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="cartographer-progress" style="width: 0%"></div>
                </div>
            </div>

            <div class="filters" data-area="cartographer">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="prophecies">Prophecies</button>
                <button class="filter-btn" data-filter="factions">Factions</button>
                <button class="filter-btn" data-filter="nightfall">Nightfall</button>
            </div>

            <div class="container">
'''
    for camp_key, camp_header, regions in CARTOGRAPHER:
        h += f'            <h3 style="color:#ffa657;margin:20px 0 10px 0;">{camp_header}</h3>\n'
        for region_header, rows in regions:
            h += f'            <h4 style="color:#58a6ff;margin:15px 0 8px 0;">{region_header}</h4>\n'
            h += '''            <table class="has-checkbox-first">
                <thead>
                    <tr>
                        <th style="width:50px">✓</th>
                        <th>Location</th>
                        <th style="width:150px">Type</th>
                    </tr>
                </thead>
                <tbody>
'''
            for cid, name, slug, typ in rows:
                cid = _dedup_data_id(cid, seen_ids)
                h += f'''                    <tr data-type="{camp_key}" data-area="cartographer" data-id="{cid}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{cid}" data-area="cartographer"></td>
                        <td><a href="https://wiki.guildwars.com/wiki/{slug}" target="_blank" class="quest-link">{name}</a></td>
                        <td style="color:#8b949e;">{typ}</td>
                    </tr>
'''
            h += '''                </tbody>
            </table>
'''
    h += '''            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#ffa657;margin:0 0 10px 0;">\U0001f4a1 Cartographer Tips</h4>
                <ul style="margin:0;padding-left:1.2em;color:#8b949e;font-size:0.9em;">
                    <li><strong>Wall Hugging</strong> - Walk along edges to uncover map</li>
                    <li><strong>All locations</strong> - Towns, outposts, missions, and explorable areas all count</li>
                    <li><strong>100% per continent</strong> - Tyria, Cantha, and Elona each need 100%</li>
                    <li><strong>Dungeons excluded</strong> - Underground areas do not count</li>
                    <li><strong>EotN separate</strong> - Eye of the North has its own "Master of the North" title</li>
                </ul>
            </div>
        </div>
    </div>
    </div>'''
    return h

html += generate_cartographer_html()

# === ARMOR SETS ===
def generate_armor_html():
    h = '''
    <div class="area" id="area-armor">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🛡️ Elite Armor Sets (''' + str(len(HOM_ARMOR)) + ''' HoM eligible)</span>
                    <span class="progress-count"><span id="armor-completed">0</span> / <span id="armor-total">''' + str(len(HOM_ARMOR)) + '''</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="armor-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="armor">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="core">Core</button>
                <button class="filter-btn" data-filter="prophecies">Prophecies</button>
                <button class="filter-btn" data-filter="factions">Factions</button>
                <button class="filter-btn" data-filter="nightfall">Nightfall</button>
                <button class="filter-btn" data-filter="eye of the north">EotN</button>
            </div>
            
            <div class="container">
            <table class="has-checkbox-first">
                <thead>
                    <tr>
                        <th style="width:50px">Got</th>
                        <th>Armor Set</th>
                        <th>Location</th>
                        <th>Requirement</th>
                        <th>HoM</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for armor in ALL_ARMOR:
        name, location, campaign, requirement, hom_eligible, wiki = armor
        armor_id = f"armor_{name.lower().replace(' ', '_').replace(chr(39), '')}"
        campaign_lower = campaign.lower()
        campaign_icon = ARMOR_ICONS.get(campaign, "🛡️")
        # profession from slug prefix if present (e.g., Warrior_Elite_...)
        _prof_prefix = wiki.split('_')[0].lower() if '_' in wiki else ''
        _known_profs = ['warrior','ranger','monk','necromancer','mesmer','elementalist','assassin','ritualist','paragon','dervish']
        prof_lower = _prof_prefix if _prof_prefix in _known_profs else 'all'
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        hom_badge = "✓" if hom_eligible else "—"
        
        h += f'''
                    <tr data-type="{campaign_lower}" data-area="armor" data-profession="{prof_lower}" data-id="{armor_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{armor_id}" data-area="armor"></td>
                        <td>
    <div style="display:flex;align-items:center;gap:8px;">
        <div style="display:flex;gap:4px;flex:0 0 auto;">
            <img class="armor-preview-f" src="" alt="" referrerpolicy="no-referrer" loading="lazy" style="width:96px;height:96px;border-radius:10px;background:#0d1117;border:1px solid #30363d;object-fit:contain;display:none;" onerror="this.style.display='none'">
            <img class="armor-preview-m" src="" alt="" referrerpolicy="no-referrer" loading="lazy" style="width:96px;height:96px;border-radius:10px;background:#0d1117;border:1px solid #30363d;object-fit:contain;display:none;" onerror="this.style.display='none'">
        </div>
        <a href="{wiki_url}" target="_blank" class="quest-link">{campaign_icon} {name}</a>
    </div>
</td>
                        <td style="color:#8b949e;">{location}</td>
                        <td style="font-size:0.85em;color:#ffa657;">{requirement}</td>
                        <td style="text-align:center;">{hom_badge}</td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            </div>
            
            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#ffa657;margin:0 0 10px 0;">💡 HoM Resilience Monument</h4>
                <ul style="margin:0;padding-left:1.2em;color:#8b949e;font-size:0.9em;">
                    <li><strong>Elite Armor</strong> counts for the Resilience monument</li>
                    <li><strong>Obsidian Armor</strong> from Fissure of Woe is the most prestigious</li>
                    <li><strong>Vabbian Armor</strong> requires expensive gems from Vabbi</li>
                    <li><strong>EotN Armor</strong> requires Rank 5 in reputation titles</li>
                </ul>
            </div>
        </div>
    </div>'''
    return h

html += generate_armor_html()

# === MINIPETS ===
def generate_minis_html():
    h = '''
    <div class="area" id="area-minis">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🐾 Miniatures (''' + str(len(ALL_MINIS)) + ''' total, 20 for max HoM)</span>
                    <span class="progress-count"><span id="minis-completed">0</span> / <span id="minis-total">''' + str(len(ALL_MINIS)) + '''</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="minis-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="minis">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="white" style="color:#fff;">⚪ Common</button>
                <button class="filter-btn" data-filter="purple" style="color:#a855f7;">🟣 Uncommon</button>
                <button class="filter-btn" data-filter="gold" style="color:#ffd700;">🟡 Rare</button>
                <button class="filter-btn" data-filter="green" style="color:#00ff00;">🟢 Unique</button>
            </div>
            
            <div class="container">'''
    
    # Group by source
    sources = [
        ("1st Birthday", YEAR1_MINIS),
        ("2nd Birthday", YEAR2_MINIS),
        ("3rd Birthday", YEAR3_MINIS),
        ("4th Birthday", YEAR4_MINIS),
        ("5th Birthday", YEAR5_MINIS),
        ("In-Game Rewards", INGAME_MINIS),
        ("Festivals", FESTIVAL_MINIS),
    ]
    
    for source_name, minis in sources:
        h += f'''
            <h3 style="color:#ffa657;margin:20px 0 10px 0;">🎁 {source_name} ({len(minis)})</h3>
            <table class="has-checkbox-first">
                <thead>
                    <tr>
                        <th style="width:50px">Got</th>
                        <th>Miniature</th>
                        <th>Rarity</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>'''
        
        for mini in minis:
            name, rarity, source, wiki = mini
            mini_id = f"mini_{name.lower().replace(' ', '_').replace(chr(39), '')}"
            rarity_lower = rarity.lower()
            rarity_color = RARITY_COLORS.get(rarity, "#fff")
            wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
            # Build a base file path and fall back across extensions; also avoid sending referrers.
            # On the Guild Wars Wiki, Special:FilePath works reliably for images.
            icon_base = f"https://wiki.guildwars.com/wiki/Special:FilePath/{wiki}"
            icon_base_js = icon_base.replace("'", "%27")  # JS-string-safe for single-quoted onerror fallbacks

            h += f'''
                    <tr data-type="{rarity_lower}" data-area="minis" data-id="{mini_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{mini_id}" data-area="minis"></td>
                        <td>
                            <div style="display:flex;align-items:center;gap:6px;">
                                <img src="{icon_base}.png" alt="" referrerpolicy="no-referrer" loading="lazy" style="width:32px;height:32px;border-radius:4px;" onerror="this.onerror=null; this.src='{icon_base_js}.jpg'; this.onerror=function(){{this.src='{icon_base_js}.gif'; this.onerror=function(){{this.style.display='none'}}}}">
                                <a href="{wiki_url}" target="_blank" class="quest-link" style="color:{rarity_color};">{name}</a>
                            </div>
                        </td>
                        <td style="color:{rarity_color};font-weight:bold;">{rarity}</td>
                        <td style="color:#8b949e;font-size:0.9em;">{source}</td>
                    </tr>'''

        
        h += '''
                </tbody>
            </table>'''
    
    h += '''
            </div>
            
            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#ffa657;margin:0 0 10px 0;">💡 HoM Devotion Monument</h4>
                <ul style="margin:0;padding-left:1.2em;color:#8b949e;font-size:0.9em;">
                    <li><strong>20 unique minis</strong> for maximum HoM points</li>
                    <li><strong>Any rarity counts</strong> - White minis are cheapest</li>
                    <li><strong>Birthday presents</strong> - Characters get one each year</li>
                    <li><strong>Dedicated minis</strong> become account-bound</li>
                </ul>
            </div>
        </div>
    </div>'''
    return h

html += generate_minis_html()

# === UNIQUE ITEMS ===
def generate_uniques_html():
    h = '''
    <div class="area" id="area-uniques">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">💎 Unique Items (''' + str(len(UNIQUE_QUEST_ITEMS)) + ''' items)</span>
                    <span class="progress-count"><span id="uniques-completed">0</span> / <span id="uniques-total">''' + str(len(UNIQUE_QUEST_ITEMS)) + '''</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="uniques-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="uniques">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="pre-searing" style="background:#4a3728;border-color:#8B4513;">🏰 Pre-Searing</button>
                <button class="filter-btn" data-filter="hom" style="background:#238636;border-color:#238636;">🏛️ HoM Sets</button>
                <button class="filter-btn" data-filter="prophecies">Prophecies</button>
                <button class="filter-btn" data-filter="factions">Factions</button>
                <button class="filter-btn" data-filter="core">Core (FoW/UW)</button>
            </div>
            
            <div class="container">
            
            <!-- PRE-SEARING QUEST REWARDS -->
            <h3 style="color:#ffa657;margin:15px 0 10px 0;">🏰 Pre-Searing Quest Rewards</h3>
            <table>
                <thead>
                    <tr>
                        <th style="width:50px">Got</th>
                        <th>Item</th>
                        <th>Type</th>
                        <th>Quest</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for item in PRE_SEARING_REWARDS:
        name, itype, quest, notes, wiki = item
        item_id = f"unique_{name.lower().replace(' ', '_').replace(chr(39), '')}"
        icon = ITEM_CATEGORIES.get(itype, "📦")
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        quest_wiki = quest.replace(" ", "_").replace("'", "%27")
        quest_url = f"https://wiki.guildwars.com/wiki/{quest_wiki}"
        
        h += f'''
                    <tr data-type="pre-searing" data-area="uniques" data-id="{item_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{item_id}" data-area="uniques"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{icon} {name}</a></td>
                        <td style="color:#8b949e;">{itype}</td>
                        <td><a href="{quest_url}" target="_blank" style="color:#ffa657;">{quest}</a></td>
                        <td style="font-size:0.85em;color:#8b949e;">{notes}</td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            
            <!-- HOM WEAPON SETS -->
            <h3 style="color:#238636;margin:25px 0 10px 0;">🏛️ Hall of Monuments Weapon Sets</h3>
            <table>
                <thead>
                    <tr>
                        <th style="width:50px">Got</th>
                        <th>Weapon Set</th>
                        <th>Source</th>
                        <th>HoM Points</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for item in HOM_WEAPON_SETS:
        name, source, points, wiki = item
        item_id = f"unique_hom_{name.lower().replace(' ', '_').replace(chr(39), '')}"
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        
        h += f'''
                    <tr data-type="hom" data-area="uniques" data-id="{item_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{item_id}" data-area="uniques"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">⚔️ {name}</a></td>
                        <td style="color:#ffa657;">{source}</td>
                        <td style="color:#238636;font-weight:bold;">{points}</td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            
            <!-- GREEN UNIQUES (BOSS DROPS) -->
            <h3 style="color:#00ff00;margin:25px 0 10px 0;">💚 Green Uniques (Boss Drops)</h3>
            <table>
                <thead>
                    <tr>
                        <th style="width:50px">Got</th>
                        <th>Item</th>
                        <th>Type</th>
                        <th>Boss</th>
                        <th>Location</th>
                        <th>Campaign</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for item in GREEN_UNIQUES:
        name, itype, boss, location, campaign, wiki = item
        item_id = f"unique_green_{name.lower().replace(' ', '_').replace(chr(39), '')}"
        icon = ITEM_CATEGORIES.get(itype, "📦")
        campaign_lower = campaign.lower()
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        
        badge_class = {
            "Prophecies": "badge-main",
            "Factions": "badge-special",
            "Nightfall": "badge-endgame",
            "Core": "badge-side",
        }.get(campaign, "badge-side")
        
        h += f'''
                    <tr data-type="{campaign_lower}" data-area="uniques" data-id="{item_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{item_id}" data-area="uniques"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link" style="color:#00ff00;">{icon} {name}</a></td>
                        <td style="color:#8b949e;">{itype}</td>
                        <td style="color:#ffa657;">{boss}</td>
                        <td style="color:#8b949e;">{location}</td>
                        <td><span class="badge {badge_class}">{campaign}</span></td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            </div>
            
            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#00ff00;margin:0 0 10px 0;">💡 About Green Uniques</h4>
                <p style="margin:0;color:#8b949e;font-size:0.9em;">
                    Green items (unique items) drop from specific bosses. This is a small selection of popular greens - 
                    there are hundreds more! Check the <a href="https://wiki.guildwars.com/wiki/Unique_item" target="_blank" style="color:#58a6ff;">Wiki</a> for the full list.
                </p>
            </div>
        </div>
    </div>'''
    return h

html += generate_uniques_html()

# === HALL OF MONUMENTS ===
html += '''
    <div class="area" id="area-hom">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🏛️ Hall of Monuments (50 points for GW2)</span>
                    <span class="progress-count"><span id="hom-completed">0</span> / <span id="hom-total">50</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="hom-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div style="display:flex;gap:10px;align-items:center;margin:15px 0;padding:15px;background:#238636;border-radius:8px;">
                <span style="display:inline-flex;align-items:center;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></span>
                <div style="flex:1;">
                    <strong>Official HoM Calculator</strong><br>
                    <span style="font-size:0.85em;opacity:0.9;">Check your HoM rewards for GW2</span>
                </div>
                <button onclick="openHoMCalculator()" style="padding:10px 20px;background:#fff;color:#238636;border:none;border-radius:6px;font-weight:bold;cursor:pointer;">
                    🌐 Open
                </button>
            </div>
            
            <div class="filters" data-area="hom">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="devotion">Devotion</button>
                <button class="filter-btn" data-filter="fellowship">Fellowship</button>
                <button class="filter-btn" data-filter="honor">Honor</button>
                <button class="filter-btn" data-filter="resilience">Resilience</button>
                <button class="filter-btn" data-filter="valor">Valor</button>
            </div>
            
            <div class="container">
            <table>
                <thead>
                    <tr>
                        <th style="width:50px">Done</th>
                        <th>Item</th>
                        <th>Monument</th>
                        <th>Points</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- DEVOTION - Minipets -->
                    <tr class="type-special" data-type="devotion" data-area="hom" data-id="hom_mini_1">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_mini_1" data-area="hom"></td>
                        <td class="quest-link">1 Minipet dedicated</td><td><span class="badge badge-special">Devotion</span></td><td>1</td><td class="prereq">Any miniature</td>
                    </tr>
                    <tr class="type-special" data-type="devotion" data-area="hom" data-id="hom_mini_20">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_mini_20" data-area="hom"></td>
                        <td class="quest-link">20 Minipets dedicated</td><td><span class="badge badge-special">Devotion</span></td><td>5</td><td class="prereq">20 unique miniatures</td>
                    </tr>
                    <tr class="type-special" data-type="devotion" data-area="hom" data-id="hom_mini_rare">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_mini_rare" data-area="hom"></td>
                        <td class="quest-link">Rare minipet dedicated</td><td><span class="badge badge-special">Devotion</span></td><td>2</td><td class="prereq">Gold or Green mini</td>
                    </tr>
                    
                    <!-- FELLOWSHIP - Heroes -->
                    <tr class="type-profession" data-type="fellowship" data-area="hom" data-id="hom_hero_1">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_hero_1" data-area="hom"></td>
                        <td class="quest-link">1 Hero with armor</td><td><span class="badge badge-profession">Fellowship</span></td><td>1</td><td class="prereq">Any hero + elite armor</td>
                    </tr>
                    <tr class="type-profession" data-type="fellowship" data-area="hom" data-id="hom_hero_8">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_hero_8" data-area="hom"></td>
                        <td class="quest-link">8 Heroes with armor</td><td><span class="badge badge-profession">Fellowship</span></td><td>4</td><td class="prereq">8 heroes + elite armor</td>
                    </tr>
                    <tr class="type-profession" data-type="fellowship" data-area="hom" data-id="hom_hero_20">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_hero_20" data-area="hom"></td>
                        <td class="quest-link">20 Heroes with armor</td><td><span class="badge badge-profession">Fellowship</span></td><td>3</td><td class="prereq">20 heroes + elite armor</td>
                    </tr>
                    
                    <!-- HONOR - Titles -->
                    <tr class="type-main" data-type="honor" data-area="hom" data-id="hom_title_1">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_title_1" data-area="hom"></td>
                        <td class="quest-link">Any PvE title displayed</td><td><span class="badge badge-main">Honor</span></td><td>1</td><td class="prereq">Display any title</td>
                    </tr>
                    <tr class="type-main" data-type="honor" data-area="hom" data-id="hom_title_max">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_title_max" data-area="hom"></td>
                        <td class="quest-link">Any maxed title</td><td><span class="badge badge-main">Honor</span></td><td>2</td><td class="prereq">Max any title</td>
                    </tr>
                    <tr class="type-main" data-type="honor" data-area="hom" data-id="hom_gwamm">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_gwamm" data-area="hom"></td>
                        <td class="quest-link">GWAMM displayed</td><td><span class="badge badge-main">Honor</span></td><td>5</td><td class="prereq">30 maxed titles</td>
                    </tr>
                    
                    <!-- RESILIENCE - Armors -->
                    <tr class="type-mission" data-type="resilience" data-area="hom" data-id="hom_armor_1">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_armor_1" data-area="hom"></td>
                        <td class="quest-link">1 Elite armor set</td><td><span class="badge badge-mission">Resilience</span></td><td>1</td><td class="prereq">Any elite armor</td>
                    </tr>
                    <tr class="type-mission" data-type="resilience" data-area="hom" data-id="hom_armor_5">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_armor_5" data-area="hom"></td>
                        <td class="quest-link">5 Elite armor sets</td><td><span class="badge badge-mission">Resilience</span></td><td>4</td><td class="prereq">5 different armors</td>
                    </tr>
                    <tr class="type-mission" data-type="resilience" data-area="hom" data-id="hom_armor_obs">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_armor_obs" data-area="hom"></td>
                        <td class="quest-link">Obsidian armor</td><td><span class="badge badge-mission">Resilience</span></td><td>3</td><td class="prereq">FoW armor</td>
                    </tr>
                    
                    <!-- VALOR - Weapons -->
                    <tr class="type-endgame" data-type="valor" data-area="hom" data-id="hom_weapon_1">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_weapon_1" data-area="hom"></td>
                        <td class="quest-link">1 Prestige weapon</td><td><span class="badge badge-endgame">Valor</span></td><td>1</td><td class="prereq">Tormented/Destroyer/Oppressor</td>
                    </tr>
                    <tr class="type-endgame" data-type="valor" data-area="hom" data-id="hom_weapon_5">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_weapon_5" data-area="hom"></td>
                        <td class="quest-link">5 Prestige weapons</td><td><span class="badge badge-endgame">Valor</span></td><td>4</td><td class="prereq">5 different weapons</td>
                    </tr>
                    <tr class="type-endgame" data-type="valor" data-area="hom" data-id="hom_weapon_11">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="hom_weapon_11" data-area="hom"></td>
                        <td class="quest-link">11 Prestige weapons</td><td><span class="badge badge-endgame">Valor</span></td><td>3</td><td class="prereq">11 different weapons</td>
                    </tr>
                </tbody>
            </table>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #21262d; border-radius: 8px; max-width: 600px; margin-left: auto; margin-right: auto;">
                <h3 style="color: #ffd700; margin-bottom: 10px;">🎁 GW2 Rewards by Points</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.9em;">
                    <div>3 pts: Fiery Dragon Sword</div>
                    <div>10 pts: Gnarled Walking Stick</div>
                    <div>15 pts: Orange Tabby Cat</div>
                    <div>30 pts: Rainbow Jellyfish</div>
                    <div>40 pts: Rhythm of Green Woods</div>
                    <div>50 pts: Lava Spider</div>
                </div>
            </div>
        </div>
    </div>
'''

# === OUTPOSTS ===
def generate_outposts_html():
    # Group by campaign
    campaigns = {}
    for name, campaign, wiki_slug in OUTPOSTS:
        if campaign not in campaigns:
            campaigns[campaign] = []
        campaigns[campaign].append((name, wiki_slug))
    
    total = len(OUTPOSTS)
    
    h = f'''
    <div class="area" id="area-outposts">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🏘️ Cities & Outposts ({total} total)</span>
                    <span class="progress-count"><span id="outposts-completed">0</span> / <span id="outposts-total">{total}</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="outposts-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="filters" data-area="outposts">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="Prophecies">Prophecies</button>
                <button class="filter-btn" data-filter="Factions">Factions</button>
                <button class="filter-btn" data-filter="Nightfall">Nightfall</button>
                <button class="filter-btn" data-filter="Eye of the North">EotN</button>
            </div>
            
            <table class="quest-table">
                <thead>
                    <tr>
                        <th style="width:40px;">✓</th>
                        <th>Location</th>
                        <th>Campaign</th>
                    </tr>
                </thead>
                <tbody>'''
    
    campaign_badges = {
        "Prophecies": "badge-main",
        "Factions": "badge-endgame",
        "Nightfall": "badge-side",
        "Eye of the North": "badge-special"
    }

    # Explicit id overrides where the deployed page's id differs from the default slug
    # (the hand-added Reforged pre-Searing outpost). Keeps localStorage keys stable.
    outpost_id_overrides = {
        "Piken Square (pre-Searing)": "outpost_piken_square_pre_searing",
    }

    for name, campaign, wiki_slug in OUTPOSTS:
        outpost_id = outpost_id_overrides.get(name) or f"outpost_{name.lower().replace(' ', '_').replace(chr(39), '')}"
        outpost_reforged = ' data-reforged="1"' if outpost_id == "outpost_piken_square_pre_searing" else ''
        badge_cls = campaign_badges.get(campaign, "badge-side")
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki_slug}"
        
        h += f'''
                    <tr data-type="{campaign}" data-area="outposts" data-id="{outpost_id}"{outpost_reforged}>
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{outpost_id}" data-area="outposts"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{name}</a></td>
                        <td><span class="badge {badge_cls}">{campaign}</span></td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
        </div>
    </div>'''
    return h

html += generate_outposts_html()

# === NON-ELITE SKILLS ===
def generate_skills_html():
    prof_data = {
        "Common": {"color": "#9CA3AF", "icon": "🌟"},
        "Warrior": {"color": "#FFD700", "icon": "⚔️"},
        "Ranger": {"color": "#228B22", "icon": "🏹"},
        "Monk": {"color": "#87CEEB", "icon": "✨"},
        "Necromancer": {"color": "#2E8B57", "icon": "💀"},
        "Mesmer": {"color": "#DA70D6", "icon": "🎭"},
        "Elementalist": {"color": "#FF4500", "icon": "🔥"},
        "Assassin": {"color": "#4B0082", "icon": "🗡️"},
        "Ritualist": {"color": "#008B8B", "icon": "👻"},
        "Paragon": {"color": "#FF8C00", "icon": "🛡️"},
        "Dervish": {"color": "#8B4513", "icon": "🌀"},
    }
    
    total = len(NON_ELITE_SKILLS)
    
    # Group by profession
    skills_by_prof = {}
    for name, prof, slug in NON_ELITE_SKILLS:
        if prof not in skills_by_prof:
            skills_by_prof[prof] = []
        skills_by_prof[prof].append((name, slug))
    
    h = f'''
    <div class="area" id="area-skills">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">📚 Non-Elite Skills ({total} total)</span><span class="melandru-hint">⚖️ Skill tomes blocked under Melandru's Accord — skills still available from trainers (base pool), quest rewards, and elite capture.</span>
                    <span class="progress-count"><span id="skills-completed">0</span> / <span id="skills-total">{total}</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="skills-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:15px 0;" id="skills-prof-grid">'''
    
    # Profession progress grid
    prof_order = ["Common", "Warrior", "Ranger", "Monk", "Necromancer", "Mesmer", "Elementalist", "Assassin", "Ritualist", "Paragon", "Dervish"]
    for prof in prof_order:
        if prof in skills_by_prof:
            count = len(skills_by_prof[prof])
            data = prof_data.get(prof, {"color": "#9CA3AF", "icon": "❓"})
            h += f'''
                <div style="background:#161b22;padding:8px;border-radius:6px;text-align:center;cursor:pointer;" onclick="document.getElementById('skills-{prof.lower()}').scrollIntoView({{behavior:'smooth'}});">
                    <div style="font-size:1.3em;">{prof_icon_img(prof, 26)}</div>
                    <div style="font-size:0.7em;color:{data["color"]};font-weight:bold;">{prof}</div>
                    <div style="font-size:0.8em;" id="skills-{prof.lower()}-count">0/{count}</div>
                </div>'''
    
    h += '''
            </div>'''
    
    # Skills by profession in collapsible sections
    for prof in prof_order:
        if prof in skills_by_prof:
            skills = skills_by_prof[prof]
            data = prof_data.get(prof, {"color": "#9CA3AF", "icon": "❓"})
            
            h += f'''
            <details open style="margin:10px 0;background:#161b22;border-radius:8px;border:1px solid #30363d;" id="skills-{prof.lower()}">
                <summary style="padding:12px;cursor:pointer;font-weight:bold;color:{data["color"]};">
                    {prof_icon_img(prof)} {prof} ({len(skills)} skills)
                </summary>
                <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:6px;padding:10px;">'''
            
            for name, wiki_slug in skills:
                clean_name = name.lower().replace(' ', '_').replace("'", '').replace('!', '').replace('"', '')
                skill_id = f"skill_{clean_name}"
                wiki_url = f"https://wiki.guildwars.com/wiki/{wiki_slug}"
                icon_url = f"https://wiki.guildwars.com/wiki/Special:Redirect/file/{wiki_slug}.jpg"
                
                h += f'''
                    <div data-type="{prof}" data-area="skills" data-id="{skill_id}" style="display:flex;align-items:center;gap:8px;padding:5px;background:#21262d;border-radius:4px;">
                        <input type="checkbox" class="quest-checkbox" data-id="{skill_id}" data-area="skills" style="width:16px;height:16px;">
                        <img src="{icon_url}" alt="" style="width:32px;height:32px;border-radius:4px;" onerror="this.style.display='none'">
                        <a href="{wiki_url}" target="_blank" class="quest-link" style="font-size:0.85em;">{name}</a>
                    </div>'''
            
            h += '''
                </div>
            </details>'''
    
    h += '''
        </div>
    </div>'''
    return h

html += generate_skills_html()

# === MENAGERIE ===
def generate_menagerie_html():
    total = len(MENAGERIE)
    
    h = f'''
    <div class="area" id="area-menagerie">
        <div class="melandru-block">🚫 Blocked under Melandru's Accord — the Zaishen Menagerie requires trading/donation, disallowed under Ironman rules.</div>
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🦁 Zaishen Menagerie ({total} animals)</span>
                    <span class="progress-count"><span class="menagerie-normal"><span id="menagerie-completed">0</span> / <span id="menagerie-total">{total}</span></span><span class="menagerie-blocked">n/a — Blocked under Melandru's Accord</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="menagerie-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <p style="color:#8b949e;margin:15px 0;font-size:0.9em;">
                Collect and donate animals to the <a href="https://wiki.guildwars.com/wiki/Zaishen_Menagerie" target="_blank" style="color:#58a6ff;">Zaishen Menagerie</a> to unlock them as pets for all characters!
            </p>
            
            <div class="menagerie-grid" style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'''
    
    # Some animals have different image names on the wiki
    img_name_map = {
        "Moa_Bird": "Strider",
    }
    
    for name, wiki_slug in MENAGERIE:
        animal_id = f"animal_{name.lower().replace(' ', '_')}"
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki_slug}"
        
        # Get the image name (may differ from wiki_slug)
        img_name = img_name_map.get(wiki_slug, wiki_slug)
        img_url = f"https://wiki.guildwars.com/wiki/Special:Redirect/file/{img_name}.jpg"
        # %27-encode apostrophes: img_url_png is emitted inside a single-quoted onerror JS string
        img_url_png = f"https://wiki.guildwars.com/wiki/Special:Redirect/file/{img_name}.png".replace("'", "%27")
        
        h += f'''
                <div data-area="menagerie" data-id="{animal_id}" style="display:flex;align-items:center;gap:15px;padding:12px;background:#161b22;border-radius:10px;border:1px solid #30363d;">
                    <input type="checkbox" class="quest-checkbox" data-id="{animal_id}" data-area="menagerie" style="width:22px;height:22px;cursor:pointer;">
                    <img src="{img_url}" alt="{name}" style="width:80px;height:80px;object-fit:contain;border-radius:8px;" onerror="this.onerror=null;this.src='{img_url_png}';this.onerror=function(){{this.style.display='none';this.nextElementSibling.style.display='flex';}}">
                    <span style="display:none;width:96px;height:96px;background:#21262d;border-radius:8px;align-items:center;justify-content:center;color:#8b949e;"><svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="6" cy="9" r="2.2"/><circle cx="10" cy="5.5" r="2.2"/><circle cx="14.5" cy="5.5" r="2.2"/><circle cx="18.5" cy="9" r="2.2"/><path d="M12.2 10c-3 0-5.5 2.6-5.5 5.2 0 1.7 1.3 2.8 3 2.8 1 0 1.7-.4 2.5-.4s1.5.4 2.5.4c1.7 0 3-1.1 3-2.8 0-2.6-2.5-5.2-5.5-5.2z"/></svg></span>
                    <a href="{wiki_url}" target="_blank" class="quest-link" style="flex:1;font-size:1.1em;">{name}</a>
                </div>'''
    
    h += '''
            </div>
        </div>
    </div>'''
    return h

html += generate_menagerie_html()

# === ELITE SKILLS (SKILL HUNTER) ===
def generate_elite_skills_html():
    prof_data = {
        "Warrior": {"color": "#FFD700", "icon": "⚔️"},
        "Ranger": {"color": "#228B22", "icon": "🏹"},
        "Monk": {"color": "#87CEEB", "icon": "✨"},
        "Necromancer": {"color": "#2E8B57", "icon": "💀"},
        "Mesmer": {"color": "#DA70D6", "icon": "🎭"},
        "Elementalist": {"color": "#FF4500", "icon": "🔥"},
        "Assassin": {"color": "#4B0082", "icon": "🗡️"},
        "Ritualist": {"color": "#008B8B", "icon": "👻"},
        "Paragon": {"color": "#FF8C00", "icon": "🛡️"},
        "Dervish": {"color": "#8B4513", "icon": "🌀"},
    }
    
    total_skills = sum(len(skills) for skills in ELITE_SKILLS.values())
    
    h = f'''
    <div class="area" id="area-elites">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🎯 Legendary Skill Hunter ({total_skills} Elite Skills)</span><span class="melandru-hint">⚖️ Elite tomes blocked under Melandru's Accord — elite skills still available from capture and quest rewards.</span>
                    <span class="progress-count"><span id="elites-completed">0</span> / <span id="elites-total">{total_skills}</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="elites-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:15px 0;" id="elites-prof-grid">'''
    
    # Profession progress grid
    prof_order = ["Warrior", "Ranger", "Monk", "Necromancer", "Mesmer", "Elementalist", "Assassin", "Ritualist", "Paragon", "Dervish"]
    for prof in prof_order:
        if prof in ELITE_SKILLS:
            count = len(ELITE_SKILLS[prof])
            data = prof_data.get(prof, {"color": "#9CA3AF", "icon": "❓"})
            h += f'''
                <div style="background:#161b22;padding:8px;border-radius:6px;text-align:center;cursor:pointer;" onclick="document.getElementById('elites-{prof.lower()}').scrollIntoView({{behavior:'smooth'}});">
                    <div style="font-size:1.3em;">{prof_icon_img(prof, 26)}</div>
                    <div style="font-size:0.7em;color:{data["color"]};font-weight:bold;">{prof}</div>
                    <div style="font-size:0.8em;" id="elites-{prof.lower()}-count">0/{count}</div>
                </div>'''
    
    h += '''
            </div>'''
    
    # Icon name mapping for skills with special characters (shouts have quotes - URL encoded as %22)
    icon_map = {
        "Charge!": '%22Charge!%22',
        "Coward!": '%22Coward!%22',
        "Together_as_One!": '%22Together_as_One!%22',
        "You%27re_All_Alone!": '%22You%27re_All_Alone!%22',
        "Incoming!": '%22Incoming!%22',
        "It%27s_Just_a_Flesh_Wound": '%22It%27s_Just_a_Flesh_Wound.%22',
    }
    
    # Skills by profession in collapsible sections
    for prof in prof_order:
        if prof in ELITE_SKILLS:
            skills = ELITE_SKILLS[prof]
            data = prof_data.get(prof, {"color": "#9CA3AF", "icon": "❓"})
            prof_id = prof.lower()
            
            h += f'''
            <details open style="margin:10px 0;background:#161b22;border-radius:8px;border:1px solid #30363d;" id="elites-{prof_id}">
                <summary style="padding:12px;cursor:pointer;font-weight:bold;color:{data["color"]};">
                    {prof_icon_img(prof)} {prof} ({len(skills)} elite skills)
                </summary>
                <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px;padding:10px;">'''
            
            for skill in skills:
                skill_name, _, campaign, attribute, wiki = skill
                skill_id = f"elite_{prof_id}_{skill_name.lower().replace(' ', '_').replace('!', '').replace(chr(39), '')}"
                wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
                # Get icon name - strip ! and special chars for image URL
                icon_name = icon_map.get(wiki, wiki.replace('!', '').replace('%27', "'"))
                icon_url = f"https://wiki.guildwars.com/wiki/Special:Redirect/file/{icon_name}.jpg"
                
                campaign_color = {"Core": "#8b949e", "Prophecies": "#ffd700", "Factions": "#ff6b6b", "Nightfall": "#9d4edd"}.get(campaign, "#8b949e")
                
                h += f'''
                    <div data-area="elites" data-id="{skill_id}" data-campaign="{campaign.lower()}" data-profession="{prof_id}" style="display:flex;align-items:center;gap:8px;padding:5px;background:#21262d;border-radius:4px;">
                        <input type="checkbox" class="quest-checkbox" data-id="{skill_id}" data-area="elites" data-campaign="{campaign.lower()}" data-profession="{prof_id}" style="width:16px;height:16px;">
                        <img src="{icon_url}" alt="" style="width:32px;height:32px;border-radius:4px;border:2px solid {campaign_color};" onerror="this.style.display='none'">
                        <div style="flex:1;min-width:0;">
                            <a href="{wiki_url}" target="_blank" class="quest-link" style="font-size:0.85em;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{skill_name}</a>
                            <span style="font-size:0.7em;color:{campaign_color};">{campaign}</span>
                        </div>
                    </div>'''
            
            h += '''
                </div>
            </details>'''
    
    h += '''
        </div>
    </div>'''
    return h

html += generate_elite_skills_html()

html += '''
    </main>
    <script>
        // ==================== CHARACTER MANAGEMENT ====================
        let currentCharacter = null;
        // ==================== TOOLBOX BRIDGE (LOCAL) ====================
        function getToolboxPort() {
            const p = parseInt(localStorage.getItem('gw-toolbox-port') || '61337');
            return isNaN(p) ? 61337 : p;
        }
        function setToolboxPort(p) {
            const n = parseInt(p);
            if (!isNaN(n) && n > 0) localStorage.setItem('gw-toolbox-port', String(n));
        }
        function toolboxBase() { return `http://127.0.0.1:${getToolboxPort()}`; }
        function toolboxSetDot(ok) {
            const dot = document.getElementById('tb-dot');
            if (!dot) return;
            dot.classList.toggle('ok', !!ok);
            dot.classList.toggle('err', !ok);
        }
        async function toolboxPing() {
            try {
                const ctrl = new AbortController();
                const t = setTimeout(() => ctrl.abort(), 1200);
                const r = await fetch(toolboxBase() + '/ping', { cache: 'no-store', signal: ctrl.signal });
                clearTimeout(t);
                const j = await r.json().catch(() => ({}));
                const ok = r.ok && j && (j.ok !== false);
                toolboxSetDot(ok);
                return ok;
            } catch (e) {
                toolboxSetDot(false);
                return false;
            }
        }
        function toolboxPromptPort() {
            const cur = getToolboxPort();
            const p = prompt('Toolbox local port', String(cur));
            if (p != null && p.trim() !== '') { setToolboxPort(p.trim()); toolboxPing(); }
        }
        async function toolboxSendChat(msg) {
            try {
                const r = await fetch(toolboxBase() + '/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ msg }) });
                return await r.json();
            } catch (e) { return { ok: false, error: String(e) }; }
        }
        function ensureToolboxUI() {
            if (document.getElementById('tb-dot')) return;
            const host = document.querySelector('.char-selector');
            if (!host) return;
            const span = document.createElement('span');
            span.className = 'tb-conn';
            span.innerHTML = '<span id="tb-dot" class="tb-dot" title="Toolbox connection"></span>'+
                             ' <button class="char-btn" onclick="toolboxPing()" title="Connect to Toolbox">Toolbox</button>'+
                             ' <button class="char-btn" onclick="toolboxPromptPort()" title="Set Toolbox port">Cfg</button>';
            host.appendChild(span);
            try {
                const conn = span;
                const bTest = document.createElement('button');
                bTest.className = 'char-btn'; bTest.textContent = 'Test'; bTest.title = 'Send test chat';
                bTest.onclick = toolboxTest; conn.appendChild(bTest);
                const bSync = document.createElement('button');
                bSync.className = 'char-btn'; bSync.textContent = 'Sync'; bSync.title = 'Sync progress';
                bSync.onclick = toolboxSyncProgress; conn.appendChild(bSync);
                const bCfg = document.createElement('button');
                bCfg.className = 'char-btn'; bCfg.textContent = 'Cfg'; bCfg.title = 'Set Toolbox port';
                bCfg.onclick = toolboxPromptPort; conn.appendChild(bCfg);
            } catch (e) {}
        }
        function initToolboxBridge() {
            ensureToolboxUI();
            toolboxPing();
            if (window.__tbTimer) clearInterval(window.__tbTimer);
            window.__tbTimer = setInterval(toolboxPing, 5000);
        }
        
        function getCharacters() {
            return JSON.parse(localStorage.getItem('gw-characters') || '["Default"]');
        }
        
        function saveCharacters(chars) {
            localStorage.setItem('gw-characters', JSON.stringify(chars));
        }
        
        function getCurrentCharacter() {
            return localStorage.getItem('gw-current-char') || 'Default';
        }
        
        function setCurrentCharacter(name) {
            localStorage.setItem('gw-current-char', name);
            currentCharacter = name;
        }
        
        function getProgressKey() {
            return 'gw-progress-' + currentCharacter;
        }
        
        function populateCharSelect() {
            const select = document.getElementById('char-select');
            const chars = getCharacters();
            select.innerHTML = chars.map(c => 
                `<option value="${c}" ${c === currentCharacter ? 'selected' : ''}>${c}</option>`
            ).join('');
        }
        
        function addCharacter() {
            const name = prompt('New character name:');
            if (!name || name.trim() === '') return;
            const chars = getCharacters();
            if (chars.includes(name.trim())) {
                alert('Character already exists!');
                return;
            }
            chars.push(name.trim());
            saveCharacters(chars);
            setCurrentCharacter(name.trim());
            // Explicit default modes for the new character (Reforged on, others off)
            const modes = getModes();
            modes[name.trim()] = { reforged: true, dhuum: false, melandru: false };
            localStorage.setItem('gw-modes', JSON.stringify(modes));
            populateCharSelect();
            clearUI();
            applyModes();
        }
        
        function switchCharacter(name) {
            const select = document.getElementById('char-select');
            if (name && select) select.value = name;
            setCurrentCharacter(select.value);
            loadCampaign();
            loadProfessions();
            loadProgress();
            applyModes();
        }
        
        function renameCharacter() {
            const newName = prompt('Rename character to:', currentCharacter);
            if (!newName || newName.trim() === '' || newName === currentCharacter) return;
            const chars = getCharacters();
            if (chars.includes(newName.trim())) {
                alert('Name already exists!');
                return;
            }
            // Rename in list
            const idx = chars.indexOf(currentCharacter);
            chars[idx] = newName.trim();
            saveCharacters(chars);
            // Move progress data
            const oldKey = getProgressKey();
            const progress = JSON.parse(localStorage.getItem(oldKey) || '{}');
            // Migrate mode settings to the new name
            const modes = getModes();
            if (modes[currentCharacter] !== undefined) {
                modes[newName.trim()] = modes[currentCharacter];
                delete modes[currentCharacter];
                localStorage.setItem('gw-modes', JSON.stringify(modes));
            }
            setCurrentCharacter(newName.trim());
            localStorage.setItem(getProgressKey(), JSON.stringify(progress));
            localStorage.removeItem(oldKey);
            populateCharSelect();
        }
        
        function deleteCharacter() {
            const chars = getCharacters();
            if (chars.length <= 1) {
                alert('Cannot delete last character!');
                return;
            }
            if (!confirm(`Delete character "${currentCharacter}"?`)) return;
            // Remove progress data
            localStorage.removeItem(getProgressKey());
            // Remove mode settings (no orphan entries)
            const modes = getModes();
            if (modes[currentCharacter] !== undefined) {
                delete modes[currentCharacter];
                localStorage.setItem('gw-modes', JSON.stringify(modes));
            }
            // Remove from list
            const idx = chars.indexOf(currentCharacter);
            chars.splice(idx, 1);
            saveCharacters(chars);
            // Switch to first char
            setCurrentCharacter(chars[0]);
            populateCharSelect();
            loadProgress();
            applyModes();
        }
        
        function resetCharacter() {
            if (!confirm(`Reset all progress for "${currentCharacter}"?`)) return;
            // Clear all progress for this character
            localStorage.removeItem(getProgressKey());
            clearUI();
            applyCampaignRestrictions();
            updateAllProgress();
        }
        
        function clearUI() {
            document.querySelectorAll('.quest-checkbox, .hm-checkbox, .bonus-checkbox, .hm-bonus-checkbox').forEach(cb => {
                cb.checked = false;
                const row = cb.closest('tr');
                if (row) row.classList.remove('completed', 'hm-done', 'bonus-done', 'hm-bonus-done');
            });
        }
        
        // Migrate old progress data to new character system
        function migrateOldProgress() {
            const oldKey = 'gw-quest-progress-all';
            const oldProgress = localStorage.getItem(oldKey);
            if (oldProgress && !localStorage.getItem('gw-migrated')) {
                // Move old progress to Default character
                localStorage.setItem('gw-progress-Default', oldProgress);
                localStorage.setItem('gw-migrated', 'true');
                console.log('Migrated old progress to Default character');
            }
        }
        
        // Initialize character system
        migrateOldProgress();
        currentCharacter = getCurrentCharacter();
        const chars = getCharacters();
        if (!chars.includes(currentCharacter)) {
            currentCharacter = chars[0];
            setCurrentCharacter(currentCharacter);
        }
        populateCharSelect();
        
        // ==================== CAMPAIGN MANAGEMENT ====================
        function getCampaignKey() {
            return 'gw-campaign-' + currentCharacter;
        }
        
        function setCampaign() {
            const campaign = document.getElementById('campaign-select').value;
            const oldCampaign = localStorage.getItem(getCampaignKey());
            
            // If campaign changed, ask to reset
            if (oldCampaign && oldCampaign !== campaign) {
                if (confirm('Campaign changed! Reset progress?')) {
                    localStorage.removeItem(getProgressKey());
                    clearUI();
                }
            }
            
            localStorage.setItem(getCampaignKey(), campaign);
            loadProgress(); // Reload saved progress
            applyCampaignRestrictions();
            updateAllProgress();
        }
        
        function loadCampaign() {
            const campaign = localStorage.getItem(getCampaignKey()) || '';
            document.getElementById('campaign-select').value = campaign;
            applyCampaignRestrictions();
            updateAllProgress(); // Update counters after restrictions applied
        }
        
        // ==================== PROFESSION MANAGEMENT ====================
        function getProfessionKey() {
            return 'gw-professions-' + currentCharacter;
        }
        
        function setProfessions() {
            const primary = document.getElementById('primary-prof').value;
            const secondary = document.getElementById('secondary-prof').value;
            const data = { primary, secondary };
            localStorage.setItem(getProfessionKey(), JSON.stringify(data));
            applyProfessionHighlighting();
            updateAllProgress(); // Update counters after profession change
        }
        
        function toggleDropdown(dropdownId) {
            const wrapper = document.getElementById(dropdownId + '-wrapper');
            const list = document.getElementById(dropdownId + '-list');
            if (!wrapper || !list) return;
            const header = wrapper.querySelector('.dropdown-header');
            if (!header) return;
            
            // Close other dropdowns
            document.querySelectorAll('.dropdown-list').forEach(dl => {
                if (dl.id !== dropdownId + '-list') {
                    dl.style.display = 'none';
                    dl.previousElementSibling?.classList.remove('open');
                    dl.previousElementSibling?.setAttribute('aria-expanded', 'false');
                }
            });
            
            // Toggle this dropdown
            if (list.style.display === 'none' || !list.style.display) {
                list.style.display = 'block';
                header.classList.add('open');
                header.setAttribute('aria-expanded', 'true');
            } else {
                list.style.display = 'none';
                header.classList.remove('open');
                header.setAttribute('aria-expanded', 'false');
            }
        }
        
        function selectProf(dropdownId, value, label, iconUrl) {
            // Update hidden input
            const input = document.getElementById(dropdownId);
            input.value = value;
            
            // Update displayed text
            const selectedSpan = document.getElementById(dropdownId + '-selected');
            if (iconUrl) {
                selectedSpan.innerHTML = `<img src="${iconUrl}" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">${label}`;
            } else {
                selectedSpan.textContent = label;
            }
            
            // Close dropdown
            const list = document.getElementById(dropdownId + '-list');
            const header = list.previousElementSibling;
            list.style.display = 'none';
            header.classList.remove('open');
            header.setAttribute('aria-expanded', 'false');
            
            // Trigger change event (1:1 like before - let existing event listeners handle it)
            const event = new Event('change', { bubbles: true });
            input.dispatchEvent(event);
            if (typeof setProfessions === 'function') {
                setProfessions();
            }
        }
        
        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.custom-dropdown')) {
                document.querySelectorAll('.dropdown-list').forEach(dl => {
                    dl.style.display = 'none';
                    if (dl.previousElementSibling) {
                        dl.previousElementSibling.classList.remove('open');
                        dl.previousElementSibling.setAttribute('aria-expanded', 'false');
                    }
                });
            }
        });

        (function() {
            document.querySelectorAll('.custom-dropdown').forEach(wrapper => {
                const header = wrapper.querySelector('.dropdown-header');
                const list = wrapper.querySelector('.dropdown-list');
                if (!header || !list) return;

                const dropdownId = (wrapper.id || '').replace(/-wrapper$/, '');

                header.setAttribute('role', 'button');
                header.tabIndex = 0;
                header.setAttribute('aria-haspopup', 'listbox');
                header.setAttribute('aria-controls', list.id);
                header.setAttribute('aria-expanded', header.classList.contains('open') ? 'true' : 'false');
                header.dataset.dropdownId = dropdownId;

                list.setAttribute('role', 'listbox');

                const options = Array.from(list.querySelectorAll('.dropdown-option'));
                options.forEach((opt, idx) => {
                    opt.setAttribute('role', 'option');
                    opt.tabIndex = 0;
                    opt.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            opt.click();
                        } else if (e.key === 'Escape') {
                            e.preventDefault();
                            list.style.display = 'none';
                            header.classList.remove('open');
                            header.setAttribute('aria-expanded', 'false');
                            header.focus();
                        } else if (e.key === 'ArrowDown') {
                            e.preventDefault();
                            options[(idx + 1) % options.length]?.focus();
                        } else if (e.key === 'ArrowUp') {
                            e.preventDefault();
                            options[(idx - 1 + options.length) % options.length]?.focus();
                        }
                    });
                });

                header.addEventListener('keydown', (e) => {
                    const id = header.dataset.dropdownId;
                    if (!id) return;

                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        toggleDropdown(id);
                    } else if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        const wasClosed = (list.style.display === 'none' || !list.style.display);
                        if (wasClosed) toggleDropdown(id);
                        options[0]?.focus();
                    } else if (e.key === 'ArrowUp') {
                        e.preventDefault();
                        const wasClosed = (list.style.display === 'none' || !list.style.display);
                        if (wasClosed) toggleDropdown(id);
                        options[options.length - 1]?.focus();
                    } else if (e.key === 'Escape') {
                        const isOpen = !(list.style.display === 'none' || !list.style.display);
                        if (isOpen) {
                            e.preventDefault();
                            list.style.display = 'none';
                            header.classList.remove('open');
                            header.setAttribute('aria-expanded', 'false');
                        }
                    }
                });
            });
        })();

        function loadProfessions() {
            const data = JSON.parse(localStorage.getItem(getProfessionKey()) || '{}');
            const primary = data.primary || '';
            const secondary = data.secondary || '';

            // Set hidden input values
            document.getElementById('primary-prof').value = primary;
            document.getElementById('secondary-prof').value = secondary;
            
            // Update displayed values in custom dropdowns
            const profMap = {
                'warrior': { label: 'Warrior', icon: 'https://wiki.guildwars.com/images/3/3b/Warrior-tango-icon-20.png' },
                'ranger': { label: 'Ranger', icon: 'https://wiki.guildwars.com/images/d/dc/Ranger-tango-icon-20.png' },
                'monk': { label: 'Monk', icon: 'https://wiki.guildwars.com/images/f/f8/Monk-tango-icon-20.png' },
                'necromancer': { label: 'Necromancer', icon: 'https://wiki.guildwars.com/images/7/7b/Necromancer-tango-icon-20.png' },
                'mesmer': { label: 'Mesmer', icon: 'https://wiki.guildwars.com/images/f/fb/Mesmer-tango-icon-20.png' },
                'elementalist': { label: 'Elementalist', icon: 'https://wiki.guildwars.com/images/a/ab/Elementalist-tango-icon-20.png' },
                'assassin': { label: 'Assassin', icon: 'https://wiki.guildwars.com/images/5/5f/Assassin-tango-icon-20.png' },
                'ritualist': { label: 'Ritualist', icon: 'https://wiki.guildwars.com/images/8/81/Ritualist-tango-icon-20.png' },
                'paragon': { label: 'Paragon', icon: 'https://wiki.guildwars.com/images/5/55/Paragon-tango-icon-20.png' },
                'dervish': { label: 'Dervish', icon: 'https://wiki.guildwars.com/images/3/3e/Dervish-tango-icon-20.png' }
            };
            
            const primarySpan = document.getElementById('primary-prof-selected');
            const secondarySpan = document.getElementById('secondary-prof-selected');
            
            if (primary && profMap[primary]) {
                primarySpan.innerHTML = `<img src="${profMap[primary].icon}" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">${profMap[primary].label}`;
            } else {
                primarySpan.textContent = 'None';
            }
            
            if (secondary && profMap[secondary]) {
                secondarySpan.innerHTML = `<img src="${profMap[secondary].icon}" style="width:16px;height:16px;vertical-align:middle;margin-right:6px;" alt="">${profMap[secondary].label}`;
            } else {
                secondarySpan.textContent = 'None';
            }
            
            applyProfessionHighlighting();
            
            // Update armor filtering based on loaded profession
            if (typeof updateArmorPreviews === 'function') updateArmorPreviews();
            if (typeof updateArmorVisibility === 'function') updateArmorVisibility();
            
            updateAllProgress(); // Update counters after profession highlighting
        }
        
        function applyProfessionHighlighting() {
            const primary = document.getElementById('primary-prof').value;
            const secondary = document.getElementById('secondary-prof').value;
            const myProfs = [primary, secondary].filter(p => p && p !== 'none');
            const primaryCapitalized = primary ? primary.charAt(0).toUpperCase() + primary.slice(1) : '';
            
            // Reset all highlighting
            document.querySelectorAll('details[data-profession]').forEach(d => {
                d.classList.remove('prof-match', 'prof-partial');
            });
document.querySelectorAll('tr[data-area="elites"][data-profession]').forEach(row => { row.classList.remove('elite-capturable', 'elite-other'); });
            
            // Reset quest profession highlighting
            document.querySelectorAll('tr[data-type="profession"]').forEach(row => {
                row.classList.remove('my-profession', 'other-profession');
            });
            
            // If no professions set, just update the grid but don't highlight
            if (myProfs.length === 0) {
                if (typeof updateProfessionProgress === 'function') {
                    updateProfessionProgress();
                }
                return;
            }
            
            // Highlight matching professions in Elite Skills
            document.querySelectorAll('details[data-profession]').forEach(d => {
                const prof = d.dataset.profession;
                if (prof === primary) {
                    d.classList.add('prof-match');
                } else if (prof === secondary) {
                    d.classList.add('prof-partial');
                }
            });
            
            // Highlight capturable elite skills
document.querySelectorAll('tr[data-area="elites"][data-profession]').forEach(row => { const prof = row.dataset.profession; if (myProfs.includes(prof)) { row.classList.add('elite-capturable'); } else { row.classList.add('elite-other'); } });
            
            // Highlight profession quests based on Wiki research:
            // 1. "[Class] Test" quests = PRIMARY only (never secondary!)
            // 2. "Secondary-Choice quests" = ANYONE can do (if no secondary chosen yet)
            //    - Grawl Invasion (Warrior), The Ranger's Companion, A Monk's Mission,
            //    - The Necromancer's Novice, A Mesmer's Burden, The Elementalist Experiment
            // 3. Other profession quests = PRIMARY or SECONDARY of that class
            const secondaryCapitalized = secondary ? secondary.charAt(0).toUpperCase() + secondary.slice(1) : '';
            
            // These quests can be done by ANYONE to choose their secondary
            const secondaryChoiceQuests = [
                "Grawl Invasion", "The Ranger's Companion", "A Monk's Mission",
                "The Necromancer's Novice", "A Mesmer's Burden", "The Elementalist Experiment"
            ];
            
            // Pre-Searing "[Class] Test" quests - PRIMARY ONLY
            const preSearingTestQuests = [
                "Warrior Test", "Ranger Test", "Monk Test",
                "Necromancer Test", "Mesmer Test", "Elementalist Test"
            ];
            
            document.querySelectorAll('tr[data-type="profession"]').forEach(row => {
                const rowProf = row.dataset.prof;
                const questLink = row.querySelector('.quest-link');
                const questName = questLink ? questLink.textContent : '';
                row.classList.remove('my-profession', 'my-secondary-profession', 'other-profession');
                
                const isSecondaryChoiceQuest = secondaryChoiceQuests.includes(questName);
                const isPreSearingTestQuest = preSearingTestQuests.includes(questName);
                
                // Only apply filtering if primary is set
                if (!primaryCapitalized) return;
                
                if (rowProf === primaryCapitalized) {
                    // PRIMARY profession quests - always doable
                    row.classList.add('my-profession');
                } else if (isPreSearingTestQuest) {
                    // Pre-Searing "[Class] Test" quests are PRIMARY ONLY - never for secondary!
                    row.classList.add('other-profession');
                } else if (isSecondaryChoiceQuest) {
                    // Secondary choice quest - doable if no secondary yet, or if it's YOUR secondary
                    if (!secondaryCapitalized || secondaryCapitalized === 'None') {
                        // No secondary chosen - all 5 other secondary-choice quests are available
                        // (but only visible, not highlighted)
                    } else if (rowProf === secondaryCapitalized) {
                        // This is YOUR secondary choice quest
                        row.classList.add('my-secondary-profession');
                    } else {
                        // Already chose a different secondary - can't do this one
                        row.classList.add('other-profession');
                    }
                } else if (rowProf === secondaryCapitalized && secondaryCapitalized !== 'None') {
                    // Other secondary profession quests (after choosing secondary)
                    row.classList.add('my-secondary-profession');
                } else {
                    // Not your primary or secondary - can't do
                    row.classList.add('other-profession');
                }
            });
            
            // Update profession progress grid
            if (typeof updateProfessionProgress === 'function') {
                updateProfessionProgress();
            }
        }
        
        function applyCampaignRestrictions() {
            const campaign = document.getElementById('campaign-select').value;
            
            // Reset all campaign-locked states
            document.querySelectorAll('tr[data-area]').forEach(row => {
                row.classList.remove('campaign-locked');
                const cb = row.querySelector('.quest-checkbox');
                if (cb) cb.disabled = false;
            });
            
            if (!campaign) return;
            
            // Lock a row
            function lockRow(row) {
                row.classList.add('campaign-locked');
                const cb = row.querySelector('.quest-checkbox');
                if (cb) {
                    cb.checked = true;
                    cb.disabled = true;
                    row.classList.add('completed');
                }
            }
            
            // Apply restrictions based on campaign
            // Prophecies: Can't do Shing Jea/Istan Main+Tutorial, Assassin/Ritualist/Paragon/Dervish
            // Factions: Can't do Pre-Searing, Post/Shiver Main+Profession, Istan Main, Paragon/Dervish
            // Nightfall: Can't do Pre-Searing, Post/Shiver Main+Profession, Shing Jea Main+Tutorial, Assassin/Ritualist
            
            if (campaign === 'prophecies') {
                // Pre-Searing: OK (home)
                
                // Shing Jea: ALL LOCKED - Prophecies chars skip Shing Jea entirely, start in Kaineng
                document.querySelectorAll('tr[data-area="shingjea"]').forEach(row => lockRow(row));
                
                // Istan: lock only Nightfall-origin quests; allow missions/travel and any cross-campaign quests
                const nfOnlyIstanIdsForNonNightfall = new Set([
                    'istan_5',
                    'istan_6',
                    'istan_7',
                    'istan_8',
                    'istan_9',
                    'istan_11',
                    'istan_12',
                    'istan_13',
                    'istan_15',
                    'istan_16',
                    'istan_17',
                    'istan_18',
                    'istan_19',
                    'istan_20',
                    'istan_21',
                    'istan_22',
                    'istan_23',
                    'istan_25',
                    'istan_26',
                    'istan_27',
                    'istan_28',
                    'istan_29',
                    'istan_30',
                    'istan_32',
                    'istan_33',
                    'istan_34',
                    'istan_35',
                    'istan_36',
                    'istan_37',
                    'istan_38',
                    'istan_39',
                    'istan_40',
                    'istan_41',
                    'istan_42',
                    'istan_43',
                    'istan_45',
                    'istan_47',
                    'istan_48',
                    'istan_49',
                    'istan_50',
                    'istan_51',
                    'istan_52',
                    'istan_53',
                    'istan_54',
                    'istan_55',
                    'istan_56',
                    'istan_57',
                    'istan_58',
                    'istan_59',
                    'istan_61',
                    'istan_62',
                    'istan_63',
                    'istan_64',
                    'istan_65',
                    'istan_66',
                    'istan_67',
                    'istan_68',
                    'istan_69',
                    'istan_70',
                    'istan_71',
                    'istan_72',
                    'istan_73',
                    'istan_74',
                    'istan_75',
                    'istan_76',
                    'istan_77',
                    'istan_78',
                    'istan_79',
                    'istan_80',
                    'istan_81',
                    'istan_82',
                    'istan_84',
                    'istan_85',
                    'istan_86',
                    'istan_87',
                    'istan_88',
                    'istan_89',
                    'istan_90',
                    'istan_92',
                    'istan_93',
                    'istan_94',
                    'istan_95',
                    'istan_96',
                    'istan_97',
                    'istan_98',
                    'istan_99'
                ]);
                document.querySelectorAll('tr[data-area="istan"]').forEach(row => {
                    const id = row.getAttribute('data-id') || '';
                    const type = row.getAttribute('data-type') || '';
                    if (type === 'mission' || type === 'travel') return;
                    if (nfOnlyIstanIdsForNonNightfall.has(id)) lockRow(row);
                });
            }
            
            if (campaign === 'factions') {
                // Pre-Searing: ALL locked (requires Prophecies-origin character)
                document.querySelectorAll('tr[data-area="pre"]').forEach(row => lockRow(row));
                
                // Shing Jea: OK (home / Factions-origin only)
                
                // Istan: lock Nightfall-origin quests; allow missions/travel and any cross-campaign quests
                const nfOnlyIstanIdsForNonNightfall = new Set([
                    'istan_5',
                    'istan_6',
                    'istan_7',
                    'istan_8',
                    'istan_9',
                    'istan_11',
                    'istan_12',
                    'istan_13',
                    'istan_15',
                    'istan_16',
                    'istan_17',
                    'istan_18',
                    'istan_19',
                    'istan_20',
                    'istan_21',
                    'istan_22',
                    'istan_23',
                    'istan_25',
                    'istan_26',
                    'istan_27',
                    'istan_28',
                    'istan_29',
                    'istan_30',
                    'istan_32',
                    'istan_33',
                    'istan_34',
                    'istan_35',
                    'istan_36',
                    'istan_37',
                    'istan_38',
                    'istan_39',
                    'istan_40',
                    'istan_41',
                    'istan_42',
                    'istan_43',
                    'istan_45',
                    'istan_47',
                    'istan_48',
                    'istan_49',
                    'istan_50',
                    'istan_51',
                    'istan_52',
                    'istan_53',
                    'istan_54',
                    'istan_55',
                    'istan_56',
                    'istan_57',
                    'istan_58',
                    'istan_59',
                    'istan_61',
                    'istan_62',
                    'istan_63',
                    'istan_64',
                    'istan_65',
                    'istan_66',
                    'istan_67',
                    'istan_68',
                    'istan_69',
                    'istan_70',
                    'istan_71',
                    'istan_72',
                    'istan_73',
                    'istan_74',
                    'istan_75',
                    'istan_76',
                    'istan_77',
                    'istan_78',
                    'istan_79',
                    'istan_80',
                    'istan_81',
                    'istan_82',
                    'istan_84',
                    'istan_85',
                    'istan_86',
                    'istan_87',
                    'istan_88',
                    'istan_89',
                    'istan_90',
                    'istan_92',
                    'istan_93',
                    'istan_94',
                    'istan_95',
                    'istan_96',
                    'istan_97',
                    'istan_98',
                    'istan_99'
                ]);
                document.querySelectorAll('tr[data-area="istan"]').forEach(row => {
                    const id = row.getAttribute('data-id') || '';
                    const type = row.getAttribute('data-type') || '';
                    if (type === 'mission' || type === 'travel') return;
                    if (nfOnlyIstanIdsForNonNightfall.has(id)) lockRow(row);
                });
            }
            
            if (campaign === 'nightfall') {
                // Pre-Searing: ALL locked
                document.querySelectorAll('tr[data-area="pre"]').forEach(row => lockRow(row));
                
                // Shing Jea: ALL LOCKED - Nightfall chars skip Shing Jea entirely
                document.querySelectorAll('tr[data-area="shingjea"]').forEach(row => lockRow(row));
                
                // Istan: OK (home)
            }
            
            // Highlight Attribute quests based on campaign
            // Reset all attribute highlighting first
            document.querySelectorAll('tr[data-type="attribute"]').forEach(row => {
                row.classList.remove('attr-highlight', 'attr-unavailable');
            });
            
            // Prophecies: Crystal Desert + Southern Shiverpeaks attribute quests count
            // Factions: Shing Jea attribute quests count
            // Nightfall: Istan attribute quests count
            if (campaign === 'prophecies') {
                document.querySelectorAll('tr[data-area="desert"][data-type="attribute"]').forEach(row => row.classList.add('attr-highlight'));
                document.querySelectorAll('tr[data-area="sshiver"][data-type="attribute"]').forEach(row => row.classList.add('attr-highlight'));
            }
            if (campaign === 'factions') {
                document.querySelectorAll('tr[data-area="shingjea"][data-type="attribute"]').forEach(row => row.classList.add('attr-highlight'));
            }
            if (campaign === 'nightfall') {
                document.querySelectorAll('tr[data-area="istan"][data-type="attribute"]').forEach(row => row.classList.add('attr-highlight'));
            }
        }
        
        loadCampaign();
        loadProfessions();
        
        // ==================== CATEGORY SWITCHING ====================
        const questAreas = ['pre','post','shiver','kryta','maguuma','desert','sshiver','fire','shingjea','kaineng','echovald','jadesea','istan','kourna','vabbi','desolation','torment','fshiver','charr','tarnished','depths','wik','hotn','woc','bmp'];
        
        function switchCategory(category) {
            // Update tab buttons
            document.querySelectorAll('.main-tab').forEach(t => t.classList.remove('active'));
            document.querySelector(`.main-tab[data-category="${category}"]`).classList.add('active');
            
            // Show/hide quest selector
            const questSelector = document.getElementById('quests-selector');
            questSelector.classList.toggle('hidden', category !== 'quests');
            
            // Hide all areas first
            document.querySelectorAll('.area').forEach(a => a.classList.remove('active'));
            
            if (category === 'quests') {
                // Show selected quest region
                const region = document.getElementById('region-select').value || 'pre';
                document.getElementById('area-' + region).classList.add('active');
            } else if (category === 'daily') {
                document.getElementById('area-daily').classList.add('active');
                updateTodaysZaishen();
            } else if (category === 'missions') {
                document.getElementById('area-missions').classList.add('active');
            } else if (category === 'elites') {
                document.getElementById('area-elites').classList.add('active');
            } else if (category === 'heroes') {
                document.getElementById('area-heroes').classList.add('active');
            } else if (category === 'dungeons') {
                document.getElementById('area-dungeons').classList.add('active');
            } else if (category === 'vanquish') {
                document.getElementById('area-vanquish').classList.add('active');
            } else if (category === 'cartographer') {
                document.getElementById('area-cartographer').classList.add('active');
            } else if (category === 'armor') {
                document.getElementById('area-armor').classList.add('active');
                try { updateArmorPreviews && updateArmorPreviews(); } catch(e) {}
                try { updateArmorVisibility && updateArmorVisibility(); } catch(e) {}
                try { updateProgress && updateProgress('armor'); } catch(e) {}
            } else if (category === 'minis') {
                document.getElementById('area-minis').classList.add('active');
            } else if (category === 'menagerie') {
                document.getElementById('area-menagerie').classList.add('active');
            } else if (category === 'uniques') {
                document.getElementById('area-uniques').classList.add('active');
            } else if (category === 'outposts') {
                document.getElementById('area-outposts').classList.add('active');
            } else if (category === 'skills') {
                document.getElementById('area-skills').classList.add('active');
            } else if (category === 'titles') {
                document.getElementById('area-titles').classList.add('active');
            } else if (category === 'hom') {
                document.getElementById('area-hom').classList.add('active');
            }
            
            localStorage.setItem('gw-active-category', category);
        }
        
        // ==================== REGION SWITCHING ====================
        function switchRegion() {
            const select = document.getElementById('region-select');
            const region = select.value;
            document.querySelectorAll('.area').forEach(a => a.classList.remove('active'));
            document.getElementById('area-' + region).classList.add('active');
            localStorage.setItem('gw-active-tab', region);
        }
        
        // Restore last active category and region
        const lastCategory = localStorage.getItem('gw-active-category') || 'quests';
        const lastTab = localStorage.getItem('gw-active-tab') || 'pre';
        
        // Set initial state
        document.querySelectorAll('.main-tab').forEach(t => t.classList.remove('active'));
        document.querySelector(`.main-tab[data-category="${lastCategory}"]`).classList.add('active');
        document.getElementById('quests-selector').classList.toggle('hidden', lastCategory !== 'quests');
        document.getElementById('region-select').value = lastTab;
        
        // Show correct area
        document.querySelectorAll('.area').forEach(a => a.classList.remove('active'));
        if (lastCategory === 'quests') {
            document.getElementById('area-' + lastTab).classList.add('active');
        } else {
            document.getElementById('area-' + lastCategory).classList.add('active');
        }
        
        // ==================== PROGRESS MANAGEMENT ====================
        // Duplicate checkbox ids were split (second same-name row -> '<id>_2'). Both rows
        // historically shared the old key, so the new id inherits its value once; the old
        // key is never deleted (it still drives the first row).
        const DUP_ID_MIGRATION = __DUP_ID_MIGRATION__;
        function migrateDupIds(progress) {
            let changed = false;
            Object.keys(DUP_ID_MIGRATION).forEach(newKey => {
                const oldKey = DUP_ID_MIGRATION[newKey];
                if (progress[oldKey] !== undefined && progress[newKey] === undefined) {
                    progress[newKey] = progress[oldKey];
                    changed = true;
                }
            });
            return changed;
        }

        function loadProgress() {
            clearUI();
            const saved = JSON.parse(localStorage.getItem(getProgressKey()) || '{}');
            if (migrateDupIds(saved)) localStorage.setItem(getProgressKey(), JSON.stringify(saved));
            document.querySelectorAll('.quest-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                    const row = cb.closest('tr');
                    if (row) row.classList.add('completed');
                }
            });
            document.querySelectorAll('.hm-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                    const row = cb.closest('tr');
                    if (row) row.classList.add('hm-done');
                }
            });
            document.querySelectorAll('.bonus-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                    const row = cb.closest('tr');
                    if (row) row.classList.add('bonus-done');
                }
            });
            document.querySelectorAll('.hm-bonus-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                    const row = cb.closest('tr');
                    if (row) row.classList.add('hm-bonus-done');
                }
            });
            // Load title progress
            document.querySelectorAll('.title-progress-input').forEach(input => {
                const val = saved[input.dataset.id + '_progress'] || 0;
                input.value = val;
                updateTitleProgressBar(input);
            });
            // Load hero armor toggles (non-exclusive)
            document.querySelectorAll('.armor-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                }
            });
            updateAllProgress();
        }
        
        function saveProgress() {
            const progress = {};
            document.querySelectorAll('.quest-checkbox:checked').forEach(cb => {
                progress[cb.dataset.id] = true;
            });
            document.querySelectorAll('.hm-checkbox:checked').forEach(cb => {
                progress[cb.dataset.id] = true;
            });
            document.querySelectorAll('.bonus-checkbox:checked').forEach(cb => {
                progress[cb.dataset.id] = true;
            });
            document.querySelectorAll('.hm-bonus-checkbox:checked').forEach(cb => {
                progress[cb.dataset.id] = true;
            });
            // Save title progress
            document.querySelectorAll('.title-progress-input').forEach(input => {
                progress[input.dataset.id + '_progress'] = parseInt(input.value) || 0;
            });
            // Save hero armor toggles
            document.querySelectorAll('.armor-checkbox:checked').forEach(cb => {
                progress[cb.dataset.id] = true;
            });
            localStorage.setItem(getProgressKey(), JSON.stringify(progress));
        }
        
        // Update title progress bar
        // Auto-calc Vanquisher title progress from the Vanquish tab (matches deployed site)
        function updateVanquisherTitlesFromVanquish() {
            const mapping = { prophecies: 'title_vanq_tyria', factions: 'title_vanq_cantha', nightfall: 'title_vanq_elona' };
            Object.entries(mapping).forEach(([type, titleId]) => {
                const total = document.querySelectorAll(`tr[data-area="vanquish"][data-type="${type}"] .quest-checkbox`).length;
                const done = document.querySelectorAll(`tr[data-area="vanquish"][data-type="${type}"] .quest-checkbox:checked`).length;
                const input = document.querySelector(`.title-progress-input[data-id="${titleId}"]`);
                if (input) { input.value = Math.min(done, parseInt(input.dataset.max)||done); updateTitleProgressBar(input); }
            });
            const tv = document.querySelector('.quest-checkbox[data-id="title_vanq_tyria"]');
            const cv = document.querySelector('.quest-checkbox[data-id="title_vanq_cantha"]');
            const ev = document.querySelector('.quest-checkbox[data-id="title_vanq_elona"]');
            const lv = document.querySelector('.quest-checkbox[data-id="title_leg_vanq"]');
            if (tv && cv && ev && lv) {
                const all = !!(tv.checked && cv.checked && ev.checked);
                if (lv.checked !== all) { lv.checked = all; const row=lv.closest('tr'); if (row) row.classList.toggle('completed', all); }
            }
        }

        function updateTitleProgressBar(input) {
            const val = parseInt(input.value) || 0;
            const max = parseInt(input.dataset.max) || 1;
            const percent = Math.min(100, (val / max) * 100);
            const bar = document.querySelector(`.title-progress-bar[data-id="${input.dataset.id}"]`);
            if (bar) bar.style.width = percent + '%';
            // Auto-check if maxed
            const row = input.closest('tr');
            const cb = row.querySelector('.quest-checkbox');
            if (val >= max && cb && !cb.checked) {
                cb.checked = true;
                row.classList.add('completed');
                saveProgress();
            }
        }
        
        // Update dropdown option text
        function updateDropdownCount(areaId, completed, total) {
            const option = document.querySelector(`#region-select option[value="${areaId}"]`);
            if (option) {
                const name = option.textContent.replace(/\s*\(\d+\/\d+\)$/, '');
                option.textContent = `${name} (${completed}/${total})`;
            }
        }
        
        // ==================== GAME MODE TOGGLES (Reforged / Dhuum / Melandru) ====================
        // Per-character mode state in localStorage 'gw-modes' (backward-compatible: missing = defaults).
        function getModes() {
            try { return JSON.parse(localStorage.getItem('gw-modes') || '{}'); } catch (e) { return {}; }
        }
        function getCharModes() {
            const m = getModes()[currentCharacter] || {};
            // Defaults: Reforged ON, Dhuum OFF, Melandru OFF
            return { reforged: m.reforged !== false, dhuum: m.dhuum === true, melandru: m.melandru === true };
        }
        function setMode(name, val) {
            const all = getModes();
            const cur = getCharModes();
            cur[name] = val;
            all[currentCharacter] = cur;
            localStorage.setItem('gw-modes', JSON.stringify(all));
        }
        function toggleMode(name) {
            const cur = getCharModes();
            setMode(name, !cur[name]);
            applyModes();
        }
        function updateModeBadges(m) {
            const el = document.getElementById('mode-badges');
            if (!el) return;
            let html = '';
            if (m.dhuum) html += `<img class="mode-badge" src="https://wiki.guildwars.com/images/0/05/DhuumCovenant-Small.png" alt="Dhuum's Covenant" title="One life. No resurrection.">`;
            if (m.melandru) html += `<img class="mode-badge" src="https://wiki.guildwars.com/images/1/11/Melandrus_Accord-Small.png" alt="Melandru's Accord" title="Melandru's Accord (Ironman)">`;
            el.innerHTML = html;
        }
        function applyModes() {
            const m = getCharModes();
            document.body.classList.toggle('mode-reforged-off', !m.reforged);
            document.body.classList.toggle('mode-dhuum-on', m.dhuum);
            document.body.classList.toggle('mode-melandru-on', m.melandru);
            const map = { reforged: 'toggle-reforged', dhuum: 'toggle-dhuum', melandru: 'toggle-melandru' };
            Object.keys(map).forEach(k => {
                const b = document.getElementById(map[k]);
                if (b) { b.classList.toggle('active', m[k]); b.setAttribute('aria-pressed', m[k] ? 'true' : 'false'); }
            });
            updateModeBadges(m);
            updateAllProgress();
        }

        // Menagerie checkboxes live in DIVs (not TRs); count them directly.
        function updateMenagerieProgress() {
            const total = document.querySelectorAll('.quest-checkbox[data-area="menagerie"]').length;
            const completed = document.querySelectorAll('.quest-checkbox[data-area="menagerie"]:checked').length;
            const blocked = document.body.classList.contains('mode-melandru-on');
            // Swap the counter for an "n/a" notice on the actual rendered spans (inline style beats any CSS)
            const normal = document.querySelector('#area-menagerie .menagerie-normal');
            const blockedEl = document.querySelector('#area-menagerie .menagerie-blocked');
            if (normal) normal.style.display = blocked ? 'none' : 'inline';
            if (blockedEl) blockedEl.style.display = blocked ? 'inline' : 'none';
            const cEl = document.getElementById('menagerie-completed');
            const tEl = document.getElementById('menagerie-total');
            const bar = document.getElementById('menagerie-progress');
            if (cEl) cEl.textContent = completed;
            if (tEl) tEl.textContent = total;
            if (bar) bar.style.width = (blocked ? 0 : (total > 0 ? completed / total * 100 : 0)) + '%';
        }

        // Skill checkboxes live in DIVs inside per-profession <details id="skills-{prof}">.
        // Counters never updated (no mode gating — skills are doable under every mode).
        // Per-profession totals are derived from the DOM so they stay correct if data changes.
        function updateSkillCounts() {
            let grandTotal = 0, grandDone = 0;
            document.querySelectorAll('[id^="skills-"][id$="-count"]').forEach(span => {
                const prof = span.id.slice(7, -6); // strip "skills-" prefix and "-count" suffix
                const box = document.getElementById('skills-' + prof);
                if (!box) return;
                const total = box.querySelectorAll('.quest-checkbox[data-area="skills"]').length;
                const done = box.querySelectorAll('.quest-checkbox[data-area="skills"]:checked').length;
                span.textContent = done + '/' + total;
                grandTotal += total; grandDone += done;
            });
            const cEl = document.getElementById('skills-completed');
            const tEl = document.getElementById('skills-total');
            const bar = document.getElementById('skills-progress');
            if (cEl) cEl.textContent = grandDone;
            if (tEl) tEl.textContent = grandTotal;
            if (bar) bar.style.width = (grandTotal > 0 ? grandDone / grandTotal * 100 : 0) + '%';
        }

        // Elite skills (Legendary Skill Hunter) — same DIV-not-TR structure as skills:
        // per-profession <details id="elites-{prof}"> feeding the visible elites-{prof}-count grid.
        // Totals DOM-derived; no mode gating (elites doable via capture/quest under every mode).
        function updateEliteCounts() {
            let grandTotal = 0, grandDone = 0;
            document.querySelectorAll('[id^="elites-"][id$="-count"]').forEach(span => {
                const prof = span.id.slice(7, -6); // strip "elites-" prefix and "-count" suffix
                const box = document.getElementById('elites-' + prof);
                if (!box) return;
                const total = box.querySelectorAll('.quest-checkbox[data-area="elites"]').length;
                const done = box.querySelectorAll('.quest-checkbox[data-area="elites"]:checked').length;
                span.textContent = done + '/' + total;
                grandTotal += total; grandDone += done;
            });
            const cEl = document.getElementById('elites-completed');
            const tEl = document.getElementById('elites-total');
            const bar = document.getElementById('elites-progress');
            if (cEl) cEl.textContent = grandDone;
            if (tEl) tEl.textContent = grandTotal;
            if (bar) bar.style.width = (grandTotal > 0 ? grandDone / grandTotal * 100 : 0) + '%';
        }

        // Update progress for an area
        function updateProgress(areaId) {
            if (areaId === 'menagerie') { updateMenagerieProgress(); return; }
            if (areaId === 'skills') { updateSkillCounts(); return; }
            if (areaId === 'elites') { updateEliteCounts(); return; }
            // Count only DOABLE quests/pieces
            // - Exclude campaign-locked quests (can't do them with this campaign)
            // - Exclude other-profession quests (can't do them with this build, except Pre-Searing)
            // - For armor: also exclude rows currently hidden by profession rules
            const hiddenFilter = (areaId === 'armor') ? ':not(.hidden):not(.hidden-restrict)' : '';
            const reforgedFilter = document.body.classList.contains('mode-reforged-off') ? ':not([data-reforged="1"])' : '';
            const allRows = document.querySelectorAll(`tr[data-area="${areaId}"]:not(.campaign-locked):not(.other-profession)${hiddenFilter}${reforgedFilter}`);
            let total = allRows.length;
            let completed;
            if (areaId === 'missions') {
                // Count only main mission completion (exclude bonus/hm checkboxes)
                completed = document.querySelectorAll(`tr[data-area="missions"] .quest-checkbox[data-id^="mission_"]:checked`).length;
            } else {
                const allChecked = document.querySelectorAll(`tr[data-area="${areaId}"]:not(.campaign-locked):not(.other-profession)${hiddenFilter}${reforgedFilter} .quest-checkbox:checked`);
                completed = allChecked.length;
            }
            const percent = total > 0 ? (completed / total * 100) : 0;
            
            // Update dropdown with counts
            updateDropdownCount(areaId, completed, total);
            
            const progressBar = document.getElementById(areaId + '-progress');
            const completedEl = document.getElementById(areaId + '-completed');
            const totalEl = document.getElementById(areaId + '-total');
            
            if (progressBar) progressBar.style.width = percent + '%';
            if (completedEl) completedEl.textContent = completed;
            if (totalEl) totalEl.textContent = total;
        }
        
        function updateAllProgress() {
            updateProgress('pre');
            updateProgress('post');
            updateProgress('shiver');
            updateProgress('kryta');
            updateProgress('maguuma');
            updateProgress('desert');
            updateProgress('sshiver');
            updateProgress('fire');
            updateProgress('shingjea');
            updateProgress('kaineng');
            updateProgress('echovald');
            updateProgress('jadesea');
            updateProgress('istan');
            updateProgress('kourna');
            updateProgress('vabbi');
            updateProgress('desolation');
            updateProgress('torment');
            updateProgress('fshiver');
            updateProgress('charr');
            updateProgress('tarnished');
            updateProgress('depths');
            updateProgress('wik');
            updateProgress('hotn');
            updateProgress('woc');
            updateProgress('bmp');
            updateProgress('titles');
            updateProgress('hom');
            updateProgress('elites');
            updateProgress('heroes');
            updateProgress('missions');
            updateProgress('dungeons');
            updateProgress('vanquish');\n            try { updateVanquisherTitlesFromVanquish && updateVanquisherTitlesFromVanquish(); } catch (e) {}
            updateProgress('armor');
            updateProgress('minis');
            updateProgress('daily');
            updateProgress('uniques');
            updateProgress('outposts');
            updateProgress('cartographer');
            updateProgress('skills');
            updateProgress('menagerie');
            updateElitesCampaignProgress();
        }
        
        // Update elite skills campaign-specific progress
        function updateElitesCampaignProgress() {
            const campaigns = ['tyria', 'cantha', 'elona'];
            const campaignMap = {prophecies: 'tyria', factions: 'cantha', nightfall: 'elona'};
            
            campaigns.forEach(camp => {
                const campKey = camp === 'tyria' ? 'prophecies' : (camp === 'cantha' ? 'factions' : 'nightfall');
                const rows = document.querySelectorAll(`tr[data-area="elites"][data-campaign="${campKey}"]`);
                const checked = document.querySelectorAll(`tr[data-area="elites"][data-campaign="${campKey}"] .quest-checkbox:checked`);
                const percent = rows.length > 0 ? (checked.length / rows.length * 100) : 0;
                const bar = document.getElementById(`elites-${camp}-progress`);
                if (bar) bar.style.width = percent + '%';
            });
            
            // Update profession progress grid
            updateProfessionProgress();
        }
        
        // Update profession progress grid
        function updateProfessionProgress() {
            const profs = ['warrior', 'ranger', 'monk', 'necromancer', 'mesmer', 'elementalist', 'assassin', 'ritualist', 'paragon', 'dervish'];
            const primary = document.getElementById('primary-prof').value;
            const secondary = document.getElementById('secondary-prof').value;
            
            // Update primary/secondary display
            const primLabel = document.getElementById('prof-progress-primary');
            const secLabel = document.getElementById('prof-progress-secondary');
            if (primLabel) primLabel.textContent = primary ? primary.charAt(0).toUpperCase() + primary.slice(1) : '-';
            if (secLabel) secLabel.textContent = (secondary && secondary !== 'none') ? secondary.charAt(0).toUpperCase() + secondary.slice(1) : '-';
            
            let maxMissing = 0;
            let recommendProf = null;
            
            profs.forEach(prof => {
                const rows = document.querySelectorAll(`tr[data-area="elites"][data-profession="${prof}"]`);
                const checked = document.querySelectorAll(`tr[data-area="elites"][data-profession="${prof}"] .quest-checkbox:checked`);
                const total = rows.length;
                const done = checked.length;
                const percent = total > 0 ? (done / total * 100) : 0;
                const missing = total - done;
                
                // Update count and bar
                const countEl = document.getElementById(`prof-${prof}-count`);
                const barEl = document.getElementById(`prof-${prof}-bar`);
                if (countEl) countEl.textContent = `${done}/${total}`;
                if (barEl) barEl.style.width = percent + '%';
                
                // Update item styling
                const item = document.querySelector(`.prof-progress-item[data-prof="${prof}"]`);
                if (item) {
                    item.classList.remove('is-primary', 'is-secondary', 'is-complete', 'recommend');
                    if (prof === primary) item.classList.add('is-primary');
                    else if (prof === secondary) item.classList.add('is-secondary');
                    if (done >= total) item.classList.add('is-complete');
                    
                    // Track which incomplete profession has most missing skills (for recommendation)
                    if (done < total && prof !== primary && prof !== secondary) {
                        if (missing > maxMissing) {
                            maxMissing = missing;
                            recommendProf = prof;
                        }
                    }
                }
            });
            
            // Highlight recommended next secondary
            if (recommendProf) {
                const recItem = document.querySelector(`.prof-progress-item[data-prof="${recommendProf}"]`);
                if (recItem && !recItem.classList.contains('is-complete')) {
                    recItem.classList.add('recommend');
                }
            }
        }
        
        // Auto-calculate legendary titles (IDs have title_ prefix)
        const legendaryMappings = {
            'title_leg_guard': ['title_guard_tyria', 'title_guard_cantha', 'title_guard_elona'],
            'title_leg_cart': ['title_cart_tyria', 'title_cart_cantha', 'title_cart_elona'],
            'title_leg_skill': ['title_skill_tyria', 'title_skill_cantha', 'title_skill_elona'],
            'title_leg_vanq': ['title_vanq_tyria', 'title_vanq_cantha', 'title_vanq_elona']
        };
        
        function checkLegendaryTitles() {
            for (const [legendary, requirements] of Object.entries(legendaryMappings)) {
                let doneCount = 0;
                requirements.forEach(reqId => {
                    const cb = document.querySelector(`.quest-checkbox[data-id="${reqId}"]`);
                    if (cb && cb.checked) doneCount++;
                });
                
                const legCb = document.querySelector(`.quest-checkbox[data-id="${legendary}"]`);
                const legRow = legCb ? legCb.closest('tr') : null;
                
                // Update progress display (1/3, 2/3, 3/3)
                if (legRow) {
                    const prereq = legRow.querySelector('.prereq');
                    if (prereq) {
                        prereq.textContent = `${doneCount}/3 complete`;
                        prereq.style.color = doneCount === 3 ? '#3fb950' : (doneCount > 0 ? '#f0883e' : '#8b949e');
                    }
                }
                
                // Auto-check when all 3 done
                if (legCb && doneCount === 3 && !legCb.checked) {
                    legCb.checked = true;
                    if (legRow) legRow.classList.add('completed');
                    console.log('🏆 Auto-completed:', legendary);
                }
            }
            
            // Check GWAMM (30+ max titles) - also auto-check HoM GWAMM display
            const maxedTitles = document.querySelectorAll('.quest-checkbox[data-area="titles"]:checked').length;
            if (maxedTitles >= 30) {
                const homGwamm = document.querySelector('.quest-checkbox[data-id="hom_gwamm"]');
                if (homGwamm && !homGwamm.checked) {
                    homGwamm.checked = true;
                    const row = homGwamm.closest('tr');
                    if (row) row.classList.add('completed');
                    console.log('🌟 GWAMM UNLOCKED! You have', maxedTitles, 'maxed titles!');
                }
            }
            
            // Update GWAMM progress display
            const gwammCount = document.getElementById('titles-completed');
            if (gwammCount) gwammCount.textContent = maxedTitles;
        }
        
        // Checkbox handler
        document.querySelectorAll('.quest-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                const row = this.closest('tr');
                if (row) row.classList.toggle('completed', this.checked);

                // Missions: keep HM+Bonus in sync when HM/Bonus are toggled
                const id = this.dataset.id || '';
                if (this.dataset.area === 'missions' && (id.startsWith('hm_') || id.startsWith('bonus_'))) {
                    const slug = id.startsWith('hm_') ? id.substring(3) : id.substring(6);
                    const hm = document.querySelector(`.quest-checkbox[data-id="hm_${slug}"]`);
                    const bonus = document.querySelector(`.quest-checkbox[data-id="bonus_${slug}"]`);
                    const hmb = document.querySelector(`.hm-bonus-checkbox[data-id="hm_bonus_${slug}"]`);
                    if (hmb) {
                        hmb.checked = !!(hm && hm.checked && bonus && bonus.checked);
                    }
                }

                saveProgress();
                updateProgress(this.dataset.area);
                if (this.dataset.area === 'elites') updateElitesCampaignProgress();
                if (this.dataset.area === 'titles') checkLegendaryTitles(); if (this.dataset.area === 'vanquish') { try { updateVanquisherTitlesFromVanquish && updateVanquisherTitlesFromVanquish(); } catch(e){} updateProgress('titles'); checkLegendaryTitles(); }
            });
        });
        
        // HM checkbox handler
        document.querySelectorAll('.hm-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                const row = this.closest('tr');
                if (row) row.classList.toggle('hm-done', this.checked);
                saveProgress();
            });
        });
        
        // Bonus checkbox handler
        document.querySelectorAll('.bonus-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                const row = this.closest('tr');
                if (row) row.classList.toggle('bonus-done', this.checked);
                saveProgress();
            });
        });
        
        // Hero armor toggles handler
        document.querySelectorAll('.armor-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                saveProgress();
            });
        });

        // Missions: HM+Bonus handler (auto-toggle HM and Bonus)
        document.querySelectorAll('.hm-bonus-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                const id = this.dataset.id || '';
                const slug = id.replace(/^hm_bonus_/, '');
                const hm = document.querySelector(`.quest-checkbox[data-id="hm_${slug}"]`);
                const bonus = document.querySelector(`.quest-checkbox[data-id="bonus_${slug}"]`);
                if (hm) hm.checked = this.checked;
                if (bonus) bonus.checked = this.checked;
                saveProgress();
                updateProgress('missions');
            });
        });
        
        // HM Bonus checkbox handler
        document.querySelectorAll('.hm-bonus-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                const row = this.closest('tr');
                if (row) row.classList.toggle('hm-bonus-done', this.checked);
                saveProgress();
            });
        });
        
        // Filters
        const profFilters = ['Warrior','Ranger','Monk','Necromancer','Mesmer','Elementalist','Assassin','Ritualist','Paragon','Dervish'];
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const container = this.closest('.filters');
                const areaId = container.dataset.area;
                const filter = this.dataset.filter;
                const isProfFilter = profFilters.includes(filter);
                
                // For skills and outposts: simple exclusive filters (only one active at a time)
                if (areaId === 'skills' || areaId === 'outposts') {
                    container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                } else if (isProfFilter) {
                    this.classList.toggle('active');
                } else {
                    container.querySelectorAll('.filter-btn').forEach(b => {
                        if (!profFilters.includes(b.dataset.filter)) {
                            b.classList.remove('active');
                        }
                    });
                    this.classList.add('active');
                }
                
                if (areaId === 'armor') {
                    try { updateArmorVisibility && updateArmorVisibility(); } catch (e) {}
                }
                applyFilters(areaId);
            });
        });
        
        function applyFilters(areaId) {
            const container = document.querySelector(`.filters[data-area="${areaId}"]`);
            const activeType = container.querySelector('.filter-btn.active:not(.prof-warrior):not(.prof-ranger):not(.prof-monk):not(.prof-necromancer):not(.prof-mesmer):not(.prof-elementalist):not(.prof-assassin):not(.prof-ritualist):not(.prof-paragon):not(.prof-dervish)');
            const typeFilter = activeType ? activeType.dataset.filter : 'all';
            
            const activeProfs = [];
            container.querySelectorAll('.filter-btn.active').forEach(btn => {
                if (profFilters.includes(btn.dataset.filter)) {
                    activeProfs.push(btn.dataset.filter);
                }
            });
            
            // Special handling for Elite Skills "My Skills" filter
            if (areaId === 'elites' && typeFilter === 'myskills') {
                const primary = document.getElementById('primary-prof').value;
                const secondary = document.getElementById('secondary-prof').value;
                const myProfs = [primary, secondary].filter(p => p && p !== 'none');
                
                document.querySelectorAll(`tr[data-area="elites"]`).forEach(row => {
                    const rowProf = row.dataset.profession;
                    row.classList.toggle('hidden', !myProfs.includes(rowProf));
                });
                
                // Also collapse non-matching profession sections
                document.querySelectorAll('details[data-profession]').forEach(d => {
                    const prof = d.dataset.profession;
                    if (!myProfs.includes(prof)) {
                        d.removeAttribute('open');
                    } else {
                        d.setAttribute('open', '');
                    }
                });
                
                updateProgress(areaId);
                return;
            }
            
            // Regular filter handling
            document.querySelectorAll(`tr[data-area="${areaId}"]`).forEach(row => {
                const rowType = row.dataset.type;
                const rowProf = row.dataset.prof;
                const rowCampaign = row.dataset.campaign;
                const rowRegion = row.dataset.region;
                
                // For elites, filter by campaign
                if (areaId === 'elites') {
                    let showCampaign = (typeFilter === 'all' || rowCampaign === typeFilter);
                    row.classList.toggle('hidden', !showCampaign);
                } else if (areaId === 'skills' || areaId === 'outposts') {
                    // Simple profession/campaign filter for skills and outposts
                    let show = (typeFilter === 'all' || rowType === typeFilter);
                    row.classList.toggle('hidden', !show);
                } else {
                    let showType = (typeFilter === 'all' || rowType === typeFilter);
                    // Heroes: allow filtering by region 'special' even if campaign differs (e.g., Beyond heroes in Special region)
                    if (areaId === 'heroes' && typeFilter === 'special') {
                        showType = (rowRegion === 'special');
                    }
                    let showProf = (activeProfs.length === 0 || activeProfs.includes(rowProf) || rowType !== 'profession');
                    
                    if (activeProfs.length > 0 && rowType === 'profession') {
                        showProf = activeProfs.includes(rowProf);
                    }
                    
                    // 'hidden' is owned by the filter buttons; profession availability lives in
                    // 'hidden-restrict' (updateArmorVisibility). Both hide via CSS and both are
                    // excluded by the counters, so they must stay independent: baking the restrict
                    // state into 'hidden' goes stale when the profession changes without a filter click.
                    row.classList.toggle('hidden', !(showType && showProf));
                }
            });
            
            // Reset details open state when switching to All
            if (areaId === 'elites' && typeFilter === 'all') {
                document.querySelectorAll('details[data-profession]').forEach(d => {
                    d.setAttribute('open', '');
                });
            }
            
            updateProgress(areaId);
        }
        
        // Export JSON
        function exportJSON(areaId) {
            const progress = JSON.parse(localStorage.getItem(getProgressKey()) || '{}');
            const areaProgress = {};
            Object.keys(progress).forEach(k => {
                if (k.startsWith(areaId + '_')) areaProgress[k] = true;
            });
            const data = { character: currentCharacter, area: areaId, exported: new Date().toISOString(), progress: areaProgress };
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `gw_${currentCharacter}_${areaId}_progress.json`;
            a.click();
        }
        
        // Export CSV
        function exportCSV(areaId) {
            let csv = 'Quest_ID,Quest_Name,Done\\n';
            document.querySelectorAll(`tr[data-area="${areaId}"]`).forEach(row => {
                const id = row.dataset.id;
                const name = row.querySelector('.quest-link')?.textContent.replace(/,/g, ' ') || '';
                const done = row.querySelector('.quest-checkbox')?.checked ? 'TRUE' : 'FALSE';
                csv += `${id},${name},${done}\\n`;
            });
            const blob = new Blob([csv], {type: 'text/csv'});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `gw_${areaId}_progress.csv`;
            a.click();
        }
        
        // Import JSON
        function importJSON(event, areaId) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    const importedProgress = data.progress || data;
                    
                    const currentProgress = JSON.parse(localStorage.getItem(getProgressKey()) || '{}');
                    Object.assign(currentProgress, importedProgress);
                    migrateDupIds(currentProgress); // imports may carry pre-split ids
                    localStorage.setItem(getProgressKey(), JSON.stringify(currentProgress));
                    
                    document.querySelectorAll(`tr[data-area="${areaId}"] .quest-checkbox`).forEach(cb => {
                        const isChecked = !!currentProgress[cb.dataset.id];
                        cb.checked = isChecked;
                        cb.closest('tr').classList.toggle('completed', isChecked);
                    });
                    
                    updateProgress(areaId);
                    alert('Import successful for ' + currentCharacter + '! ' + Object.keys(importedProgress).length + ' entries loaded.');
                } catch (err) {
                    alert('Import error: ' + err.message);
                }
            };
            reader.readAsText(file);
            event.target.value = '';
        }
        
        // Reset
        function resetProgress(areaId) {
            if (!confirm('Progress für ' + currentCharacter + ' in dieser Region loeschen?')) return;
            const progress = JSON.parse(localStorage.getItem(getProgressKey()) || '{}');
            Object.keys(progress).forEach(k => {
                if (k.startsWith(areaId + '_')) delete progress[k];
            });
            localStorage.setItem(getProgressKey(), JSON.stringify(progress));
            document.querySelectorAll(`tr[data-area="${areaId}"] .quest-checkbox`).forEach(cb => {
                cb.checked = false;
                cb.closest('tr').classList.remove('completed');
            });
            document.querySelectorAll(`tr[data-area="${areaId}"] .hm-checkbox`).forEach(cb => {
                cb.checked = false;
                cb.closest('tr').classList.remove('hm-done');
            });
            document.querySelectorAll(`tr[data-area="${areaId}"] .bonus-checkbox`).forEach(cb => {
                cb.checked = false;
                cb.closest('tr').classList.remove('bonus-done');
            });
            document.querySelectorAll(`tr[data-area="${areaId}"] .hm-bonus-checkbox`).forEach(cb => {
                cb.checked = false;
                cb.closest('tr').classList.remove('hm-bonus-done');
            });
            updateProgress(areaId);
        }
        
        // Title progress input handler
        document.querySelectorAll('.title-progress-input').forEach(input => {
            input.addEventListener('input', function() {
                updateTitleProgressBar(this);
                saveProgress();
                updateProgress('titles');
            });
        });
        
        // ==================== JSON IMPORT ====================
        // Import from JSON file (manual export)
        function importToolboxFile(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const status = document.getElementById('toolbox-status');
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    applyToolboxData(data);
                    status.textContent = '✅ Imported from file!';
                    status.style.color = '#3fb950';
                } catch (err) {
                    status.textContent = '❌ Invalid JSON';
                    status.style.color = '#f85149';
                }
            };
            reader.readAsText(file);
            event.target.value = '';
        }
        
        // Apply Toolbox data to inputs
        function applyToolboxData(data) {
            if (data.titles) {
                Object.entries(data.titles).forEach(([titleId, value]) => {
                    const input = document.querySelector(`.title-progress-input[data-id="title_${titleId}"]`);
                    if (input) {
                        input.value = value;
                        updateTitleProgressBar(input);
                    }
                });
                saveProgress();
                updateProgress('titles');
            }
        }
        
        // Load/save daily checkboxes
        function updateTodaysZaishen() {
            updateDailyDate();
            updateDailyRotation();
            loadDailyCheckboxes();
        }
        
        function loadDailyCheckboxes() {
            const today = new Date().toISOString().split('T')[0];
            const charName = getCurrentCharacter();
            const key = 'gw-daily-' + charName + '-' + today;
            
            const saved = localStorage.getItem(key);
            const progress = saved ? JSON.parse(saved) : {};
            
            // Load all daily checkboxes
            document.querySelectorAll('[data-daily]').forEach(cb => {
                const dailyId = cb.getAttribute('data-daily');
                cb.checked = progress[dailyId] || false;
                cb.addEventListener('change', saveDailyCheckboxes);
            });
        }
        
        function saveDailyCheckboxes() {
            const today = new Date().toISOString().split('T')[0];
            const charName = getCurrentCharacter();
            const key = 'gw-daily-' + charName + '-' + today;
            
            const progress = {};
            document.querySelectorAll('[data-daily]').forEach(cb => {
                const dailyId = cb.getAttribute('data-daily');
                progress[dailyId] = cb.checked;
            });
            
            localStorage.setItem(key, JSON.stringify(progress));
        }
        
        // Open official HoM Calculator with character name
        function openHoMCalculator() {
            const charName = getCurrentCharacter();
            // The official calculator accepts character names in the URL
            const baseUrl = 'https://hom.guildwars2.com/en/';
            
            // If we have a character name, append it (user still needs to click "Calculate")
            if (charName && charName !== 'Default') {
                // Open with character name hint in a prompt
                const url = baseUrl + '#page=main';
                window.open(url, '_blank');
                
                // Show a helpful message
                setTimeout(() => {
                    alert('Search for your character: ' + charName + '\\n\\n(Copy the name and paste it in the search field)');
                }, 500);
            } else {
                window.open(baseUrl, '_blank');
            }
        }
        
        
        // Initialize everything
        loadProgress();
        updateAllProgress();
        applyModes();
        updateElitesCampaignProgress();
        applyProfessionHighlighting();
        checkLegendaryTitles(); // Auto-check legendary titles on load
        
        
// === Armor Preview Helpers ===
function getPrimaryOrDefault() {
    const el = document.getElementById('primary-prof');
    const p = el ? (el.value || '') : '';
    return (p && p !== 'none') ? p.toLowerCase() : 'warrior';
}
function armorCandidatesFor(prof, slug, gender) {
    prof = (prof || 'warrior').toLowerCase();
    const Prof = prof.charAt(0).toUpperCase() + prof.slice(1);
    const clean = slug || '';
    const alt = clean.replace(/^Elite_/i, '');
    const names = [];
    if (clean.toLowerCase().startsWith(prof + '_')) {
        names.push(clean + '_' + gender);
    } else {
        names.push(Prof + '_' + clean + '_' + gender);
        names.push(Prof + '_' + alt + '_' + gender);
        names.push(clean + '_' + gender);
    }
    const exts = ['.jpg','.png','.gif'];
    const urls = [];
    names.forEach(n => exts.forEach(e => urls.push('https://wiki.guildwars.com/wiki/Special:FilePath/' + n + e)));
    return urls;
}
function setArmorImage(img, urls) {
    if (!img) return;
    if (!urls || urls.length === 0) { img.style.display='none'; return; }
    let i = 0;
    img.onerror = function(){ i++; if (i < urls.length) { this.src = urls[i]; } else { this.style.display='none'; } };
    img.style.display='';
    img.src = urls[0];
}
function updateArmorPreviews() {
    const prof = getPrimaryOrDefault();
    document.querySelectorAll('tr[data-area="armor"][data-id]').forEach(row => {
        const link = row.querySelector('a.quest-link');
        if (!link) return;
        const href = link.getAttribute('href') || '';
        const m = href.match(/\/wiki\/(.+)$/);
        const slug = m ? decodeURIComponent(m[1]) : '';
        const fImg = row.querySelector('img.armor-preview-f');
        const mImg = row.querySelector('img.armor-preview-m');
        setArmorImage(fImg, armorCandidatesFor(prof, slug, 'f'));
        setArmorImage(mImg, armorCandidatesFor(prof, slug, 'm'));
    });
}
(document.getElementById('primary-prof')||{})&& (function(el){ if(el && el.addEventListener){ el.addEventListener('change', function(){ try{ updateArmorPreviews && updateArmorPreviews(); updateArmorVisibility && updateArmorVisibility(); updateAllProgress && updateAllProgress(); }catch(e){} }); } })(document.getElementById('primary-prof')); 
updateArmorPreviews();
        updateArmorVisibility();
        if (typeof updateAllProgress === 'function') { updateAllProgress(); }


        // Single source of truth for armor availability (verified against GWW Prestige_armor):
        // - profession-specific sets (wiki slug prefix Warrior_/Ranger_/...): primary profession only
        // - Elite Exotic / Elite Imperial: Assassin + Ritualist only
        // - Elite Kurzick / Luxon / Canthan: not available to Paragon / Dervish
        // - Elite Sunspear / Primeval: not available to Assassin / Ritualist
        // - no profession selected: show everything
        // Only toggles 'hidden-restrict'; 'hidden' belongs to the campaign filter buttons (applyFilters).
        function updateArmorVisibility() {
    const primary = document.getElementById('primary-prof') ? document.getElementById('primary-prof').value : '';
    const prof = (primary && primary !== 'none') ? primary.toLowerCase() : '';
    const known = ['warrior','ranger','monk','necromancer','mesmer','elementalist','assassin','ritualist','paragon','dervish'];
    const isAR = (prof === 'assassin' || prof === 'ritualist');
    const isPd = (prof === 'paragon' || prof === 'dervish');
    document.querySelectorAll('tr[data-area="armor"][data-id]').forEach(row => {
        let allowed = true;
        if (prof) {
            const link = row.querySelector('a.quest-link');
            const href = link ? (link.getAttribute('href') || '') : '';
            const m = href.match(/\/wiki\/(.+)$/);
            const slug = m ? decodeURIComponent(m[1]).toLowerCase() : '';
            const pref = known.find(p => slug.startsWith(p + '_'));
            if (pref) { allowed = (pref === prof); }
            if (/^elite_(exotic|imperial)_armor$/.test(slug)) { allowed = isAR; }
            if (/^elite_(kurzick|luxon|canthan)_armor$/.test(slug)) { allowed = !isPd; }
            if (/^(elite_sunspear|primeval)_armor$/.test(slug)) { allowed = !isAR; }
        }
        row.classList.toggle('hidden-restrict', !allowed);
    });
}
        // (single profession-change listener registered above; init call runs at script end)
    
                function copyDiscordName() {
            // navigator.clipboard only exists in secure contexts (https / localhost)
            if (!navigator.clipboard || !navigator.clipboard.writeText) return;
            navigator.clipboard.writeText('daestro420').then(() => {
                const el = document.getElementById('discord-copy-label');
                if (!el) return;
                const orig = el.textContent;
                el.textContent = '✓ Copied!';
                setTimeout(() => { el.textContent = orig; }, 1500);
            }).catch(() => {});
        }
        console.log('GW Companion initialized!');
    </script>

    <footer style="background:#161b22;border-top:1px solid #30363d;padding:15px 20px;text-align:center;color:#8b949e;font-size:0.85em;margin-top:20px;">
        <div style="display:flex;justify-content:center;align-items:center;gap:15px;flex-wrap:wrap;">
            <span>Created by <strong style="color:#ffd700;">Dadero</strong></span>
            <span style="color:#30363d;">|</span>
            <span id="discord-copy" style="color:#5865F2;display:inline-flex;align-items:center;gap:5px;cursor:pointer;" title="Click to copy Discord username" onclick="copyDiscordName()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515a.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0a12.64 12.64 0 0 0-.617-1.25a.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057a19.9 19.9 0 0 0 5.993 3.03a.078.078 0 0 0 .084-.028a14.09 14.09 0 0 0 1.226-1.994a.076.076 0 0 0-.041-.106a13.107 13.107 0 0 1-1.872-.892a.077.077 0 0 1-.008-.128a10.2 10.2 0 0 0 .372-.292a.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127a12.299 12.299 0 0 1-1.873.892a.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028a19.839 19.839 0 0 0 6.002-3.03a.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.956-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.955-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.946 2.418-2.157 2.418z"/></svg>
                <span id="discord-copy-label">daestro420</span>
            </span>
            <span style="color:#30363d;">|</span>
            <a href="https://github.com/dadero-deadline/gw-companion/issues" target="_blank" style="color:#58a6ff;text-decoration:none;display:inline-flex;align-items:center;gap:5px;">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
                Feedback &amp; Suggestions
            </a>
        </div>
        <div style="margin-top:8px;font-size:0.78em;color:#8b949e;opacity:0.75;line-height:1.5;">GW Companion is an unofficial fan site. Guild Wars and all associated logos and designs are trademarks or registered trademarks of NCSOFT Corporation. Not affiliated with or endorsed by ArenaNet or NCSOFT.</div>
        <div style="margin-top:4px;font-size:0.75em;color:#8b949e;opacity:0.6;">Privacy-friendly visitor counting by <a href="https://www.goatcounter.com" target="_blank" style="color:inherit;">GoatCounter</a> — no cookies, no personal data stored.</div>
    </footer>

    <script>
        // GoatCounter analytics - production domain only (keeps the localhost
        // tracker and file:// previews out of the stats). Public site code, no secret.
        if (location.hostname === 'gwcompanion.com' || location.hostname.endsWith('.gwcompanion.com')) {
            var _gc = document.createElement('script');
            _gc.async = true;
            _gc.src = 'https://gc.zgo.at/count.js';
            _gc.setAttribute('data-goatcounter', 'https://dadero.goatcounter.com/count');
            document.body.appendChild(_gc);
        }
    </script>
</body>
</html>'''

html = html.replace('__DUP_ID_MIGRATION__', json.dumps(DUP_ID_RENAMES, sort_keys=True))
html = deemojify(html)
with open('gw_tracker.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

DEFAULT_PORT = 8000

def parse_port(value, label):
    if value is None:
        return None
    try:
        port = int(value)
    except ValueError:
        print(f"{label} '{value}' is not a valid port. Ignoring.", file=sys.stderr)
        return None
    if not (1 <= port <= 65535):
        print(f"{label} '{value}' is outside the valid range (1-65535). Ignoring.", file=sys.stderr)
        return None
    return port

cli_port = parse_port(sys.argv[1], 'CLI port') if len(sys.argv) > 1 else None
env_port = parse_port(os.environ.get('GW_COMPANION_PORT'), 'GW_COMPANION_PORT')
PORT = cli_port or env_port or DEFAULT_PORT

print("Guild Wars Companion gestartet!")
print(f"http://localhost:{PORT}")

class Handler(SimpleHTTPRequestHandler):
    # Force UTF-8 for all HTML files
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        '.html': 'text/html; charset=utf-8',
        '.htm': 'text/html; charset=utf-8',
    }
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/gw_tracker.html'
        return super().do_GET()

# Build-only mode: exit after generating HTML (no server)
BUILD_ONLY = any(a in ('build','--build','--build-only') for a in sys.argv[1:]) or os.environ.get('GW_COMPANION_BUILD_ONLY') == '1'
if BUILD_ONLY:
    print('Build complete (no server started).')
    raise SystemExit(0)

HTTPServer(('localhost', PORT), Handler).serve_forever()














