from http.server import HTTPServer, SimpleHTTPRequestHandler
import openpyxl
import sys
sys.path.insert(0, 'data')

from elite_skills import ELITE_SKILLS
from heroes import HEROES, HERO_PROFESSIONS
from unique_items import UNIQUE_QUEST_ITEMS, ITEM_CATEGORIES, PRE_SEARING_REWARDS, GREEN_UNIQUES, HOM_WEAPON_SETS
from elite_content import ELITE_MISSIONS, EOTN_DUNGEONS, DUNGEON_REGIONS, CAMPAIGN_ICONS
from vanquishes import ALL_VANQUISHES, VANQUISH_REGIONS, PROPHECIES_VANQUISHES, FACTIONS_VANQUISHES, NIGHTFALL_VANQUISHES, EOTN_VANQUISHES
from missions import ALL_MISSIONS, MISSION_REGIONS, PROPHECIES_MISSIONS, FACTIONS_MISSIONS, NIGHTFALL_MISSIONS
from armor_sets import ALL_ARMOR, HOM_ARMOR, ARMOR_ICONS, CORE_ARMOR, PROPHECIES_ARMOR, FACTIONS_ARMOR, NIGHTFALL_ARMOR, EOTN_ARMOR, STANDALONE_PIECES
from minipets import ALL_MINIS, RARITY_COLORS, YEAR1_MINIS, YEAR2_MINIS, YEAR3_MINIS, YEAR4_MINIS, YEAR5_MINIS, INGAME_MINIS, FESTIVAL_MINIS
from daily_quests import ZAISHEN_MISSIONS, ZAISHEN_BOUNTIES, ZAISHEN_VANQUISHES, ZAISHEN_COMBAT, VANGUARD_QUESTS, ZAISHEN_MISSION_START, ZAISHEN_BOUNTY_START, ZAISHEN_VANQUISH_START, ZAISHEN_COMBAT_START

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
    <title>Guild Wars Companion</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', system-ui, sans-serif; 
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
        .header h1 { color: #ffd700; font-size: 1.2em; white-space: nowrap; }
        
        /* Character Selector */
        .char-selector {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .char-selector select {
            background: #161b22;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 0.85em;
            cursor: pointer;
            min-width: 100px;
        }
        .char-selector select:hover { border-color: #58a6ff; }
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
        
        /* Elite skill highlighting based on profession */
        tr.elite-capturable { background: rgba(63, 185, 80, 0.15) !important; }
        tr.elite-capturable td:first-child::before { content: "✓ "; color: #3fb950; }
        tr.elite-other { opacity: 0.5; }
        details.prof-match > summary { border-left: 3px solid #3fb950 !important; }
        details.prof-partial > summary { border-left: 3px solid #ffa657 !important; }
        
        /* Quest profession highlighting - highlight matching, dim others */
        tr.my-profession { background: rgba(63, 185, 80, 0.2) !important; border-left: 3px solid #3fb950; }
        tr.my-profession td:first-child::before { content: "⭐ "; }
        tr.my-secondary-profession { background: rgba(255, 166, 87, 0.15) !important; border-left: 3px solid #ffa657; }
        tr.my-secondary-profession td:first-child::before { content: "🔶 "; }
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
        .progress-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
        .progress-text { color: #8b949e; }
        .progress-count { color: #ffd700; font-weight: bold; font-size: 1.2em; }
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
        tr:hover { background: rgba(255,255,255,0.03); }
        tr.completed { opacity: 0.5; }
        tr.completed td { text-decoration: line-through; }
        tr.hidden { display: none; }
        
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
            table { font-size: 0.8em; }
            td, th { padding: 6px 4px; }
            /* Hide less important columns: Order(3), Prereq(7), Reward(9) */
            th:nth-child(3), td:nth-child(3),
            th:nth-child(7), td:nth-child(7),
            th:nth-child(9), td:nth-child(9) { display: none; }
        }
        
        @media (max-width: 480px) {
            .header h1 { display: none; }
            /* Also hide: Location(6), Profession(8) */
            th:nth-child(6), td:nth-child(6),
            th:nth-child(8), td:nth-child(8) { display: none; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚔️ Guild Wars Companion</h1>
        <div class="char-selector">
            <span class="char-label">Character:</span>
            <select id="char-select" onchange="switchCharacter()"></select>
            <select id="campaign-select" class="campaign-dropdown" onchange="setCampaign()">
                <option value="">-- Campaign --</option>
                <option value="prophecies">⚔️ Prophecies</option>
                <option value="factions">🐉 Factions</option>
                <option value="nightfall">🌙 Nightfall</option>
            </select>
            <select id="primary-prof" class="prof-dropdown" onchange="setProfessions()" title="Primary Profession">
                <option value="">Primary</option>
                <option value="warrior">⚔️ Warrior</option>
                <option value="ranger">🏹 Ranger</option>
                <option value="monk">✨ Monk</option>
                <option value="necromancer">💀 Necromancer</option>
                <option value="mesmer">🎭 Mesmer</option>
                <option value="elementalist">🔥 Elementalist</option>
                <option value="assassin">🗡️ Assassin</option>
                <option value="ritualist">👻 Ritualist</option>
                <option value="paragon">🛡️ Paragon</option>
                <option value="dervish">🌀 Dervish</option>
            </select>
            <select id="secondary-prof" class="prof-dropdown" onchange="setProfessions()" title="Secondary Profession">
                <option value="">Secondary</option>
                <option value="warrior">⚔️ Warrior</option>
                <option value="ranger">🏹 Ranger</option>
                <option value="monk">✨ Monk</option>
                <option value="necromancer">💀 Necromancer</option>
                <option value="mesmer">🎭 Mesmer</option>
                <option value="elementalist">🔥 Elementalist</option>
                <option value="assassin">🗡️ Assassin</option>
                <option value="ritualist">👻 Ritualist</option>
                <option value="paragon">🛡️ Paragon</option>
                <option value="dervish">🌀 Dervish</option>
                <option value="none">❌ None</option>
            </select>
            <button class="char-btn" onclick="resetCharacter()" title="Reset all progress for this character">🔄 Reset</button>
            <button class="char-btn add" onclick="addCharacter()">+ New</button>
            <button class="char-btn" onclick="renameCharacter()">✏️</button>
            <button class="char-btn delete" onclick="deleteCharacter()">🗑️</button>
        </div>
    </div>
    
    <div class="main-tabs">
        <button class="main-tab active" data-category="quests" onclick="switchCategory('quests')">📜 Quests</button>
        <button class="main-tab" data-category="daily" onclick="switchCategory('daily')">📅 Daily</button>
        <button class="main-tab" data-category="missions" onclick="switchCategory('missions')">🗺️ Missions</button>
        <button class="main-tab" data-category="elites" onclick="switchCategory('elites')">🎯 Skills</button>
        <button class="main-tab" data-category="heroes" onclick="switchCategory('heroes')">🦸 Heroes</button>
        <button class="main-tab" data-category="dungeons" onclick="switchCategory('dungeons')">🏰 Dungeons</button>
        <button class="main-tab" data-category="vanquish" onclick="switchCategory('vanquish')">⚔️ Vanquish</button>
        <button class="main-tab" data-category="armor" onclick="switchCategory('armor')">🛡️ Armor</button>
        <button class="main-tab" data-category="minis" onclick="switchCategory('minis')">🐾 Minis</button>
        <button class="main-tab" data-category="uniques" onclick="switchCategory('uniques')">💎 Items</button>
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

def generate_area_html(quests, area_id, area_name, is_active=False):
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
    
    active = "active" if is_active else ""
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
                <button class="filter-btn active" data-filter="all">All</button>'''
    
    # Add Main button only for areas that have Main quests
    if area_id in ["pre", "post", "istan", "kourna", "vabbi", "desolation", "torment", "fshiver", "charr", "tarnished", "depths", "wik", "hotn", "woc"]:
        h += '''
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
            <table>
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
        
        h += f'''
                    <tr class="{row_cls}" data-id="{q['id']}" data-type="{q['type'].lower()}" data-prof="{prof}" data-area="{area_id}"{missable_attr}>
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{q['id']}" data-area="{area_id}"></td>
                        <td class="checkbox-cell">{hm_cell}</td>
                        <td class="checkbox-cell">{bonus_cell}</td>
                        <td class="checkbox-cell">{hm_bonus_cell}</td>
                        <td class="order">{q['order']}</td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{q['name']}</a></td>
                        <td>{q['giver']}</td>
                        <td class="location">{q['location']}</td>
                        <td><span class="badge {badge}">{q['type']}</span>{missable_badge}</td>
                        <td>{prof_badge}</td>
                        <td class="prereq">{q['prereq']}</td>
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
    ("vanq_elona", "Elonian Vanquisher", "Vanquisher", 1, 51, "pve", "Nightfall", "All areas vanquished"),
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
    ("survivor1", "Survivor (Tier 1)", "Survivor", 1, 140600, "legendary", "Core", "140,600 XP ohne Tod"),
    ("survivor2", "Survivor (Tier 2)", "Survivor", 2, 587500, "legendary", "Core", "587,500 XP ohne Tod"),
    ("survivor3", "Survivor (Tier 3 - Max)", "Survivor", 3, 1337500, "legendary", "Core", "1,337,500 XP ohne Tod"),
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
        
        h += f'''
                    <tr class="{row_cls}" data-type="{ttype}" data-area="titles" data-id="title_{tid}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="title_{tid}" data-area="titles"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{name}</a><br><span class="prereq">{desc}</span></td>
                        <td>
                            <div style="display:flex;align-items:center;gap:8px;">
                                <input type="number" class="title-progress-input" data-id="title_{tid}" data-max="{max_pts}" min="0" max="{max_pts}" value="0" style="width:70px;padding:4px;background:#161b22;color:#c9d1d9;border:1px solid #30363d;border-radius:4px;">
                                <span style="color:#8b949e;">/ {max_pts:,}</span>
                            </div>
                            <div class="progress-bar" style="height:6px;margin-top:4px;">
                                <div class="progress-fill title-progress-bar" data-id="title_{tid}" style="width:0%;"></div>
                            </div>
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
                        <th>Unlock Quest</th>
                    </tr>
                </thead>
                <tbody>'''
    
    # Group by campaign
    for hero in HEROES:
        name, profession, campaign, region, quest, wiki = hero
        hero_id = f"hero_{name.lower().replace(' ', '_').replace('.', '')}"
        icon = HERO_PROFESSIONS.get(profession, "")
        campaign_lower = campaign.lower()
        
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
        
        h += f'''
                    <tr data-type="{campaign_lower}" data-area="heroes" data-id="{hero_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{hero_id}" data-area="heroes"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{icon} {name}</a></td>
                        <td style="color:#ffa657;">{profession}</td>
                        <td>{region}</td>
                        <td><a href="{quest_url}" target="_blank" style="color:#8b949e;">{quest}</a></td>
                    </tr>'''
    
    h += '''
                </tbody>
            </table>
            </div>
            
            <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                <h4 style="color:#ffa657;margin:0 0 10px 0;">💡 Hero Armor for HoM</h4>
                <ul style="margin:0;color:#8b949e;font-size:0.9em;">
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
    from datetime import datetime, timedelta
    
    # Calculate today's quests
    today = datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Mission (69-day cycle)
    mission_days = (today - ZAISHEN_MISSION_START).days
    mission_idx = mission_days % len(ZAISHEN_MISSIONS)
    today_mission = ZAISHEN_MISSIONS[mission_idx]
    
    # Bounty (66-day cycle)
    bounty_days = (today - ZAISHEN_BOUNTY_START).days
    bounty_idx = bounty_days % len(ZAISHEN_BOUNTIES)
    today_bounty = ZAISHEN_BOUNTIES[bounty_idx]
    
    # Vanquish (136-day cycle, but we only have 10 in our list, so use that)
    vanquish_days = (today - ZAISHEN_VANQUISH_START).days
    vanquish_idx = vanquish_days % len(ZAISHEN_VANQUISHES)
    today_vanquish = ZAISHEN_VANQUISHES[vanquish_idx]
    
    # Combat/PvP (7-day cycle)
    combat_days = (today - ZAISHEN_COMBAT_START).days
    combat_idx = combat_days % len(ZAISHEN_COMBAT)
    today_combat = ZAISHEN_COMBAT[combat_idx]
    
    h = f'''
    <div class="area" id="area-daily">
        <div class="content">
            <div style="text-align:center;margin-bottom:30px;">
                <h2 style="color:#ffd700;margin:0;">📅 Today's Daily Quests</h2>
                <p style="color:#8b949e;margin:5px 0;">{today.strftime("%A, %B %d, %Y")} • Resets at midnight UTC</p>
            </div>
            
            <div style="max-width:600px;margin:0 auto;">
                <h3 style="color:#ffa657;margin:0 0 15px 0;">⚔️ Zaishen Dailies</h3>
                
                <div style="background:#21262d;border-radius:12px;overflow:hidden;">
                    <!-- Mission -->
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;border-bottom:1px solid #30363d;">
                        <input type="checkbox" id="daily-mission" class="quest-checkbox" style="width:22px;height:22px;" data-daily="mission">
                        <div style="flex:1;">
                            <span style="color:#238636;font-weight:bold;">🗺️ Mission:</span>
                            <a href="https://wiki.guildwars.com/wiki/{today_mission[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{today_mission[0]}</a>
                            <span style="color:#8b949e;font-size:0.85em;margin-left:8px;">({today_mission[1]})</span>
                        </div>
                    </div>
                    
                    <!-- Bounty -->
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;border-bottom:1px solid #30363d;">
                        <input type="checkbox" id="daily-bounty" class="quest-checkbox" style="width:22px;height:22px;" data-daily="bounty">
                        <div style="flex:1;">
                            <span style="color:#1f6feb;font-weight:bold;">🎯 Bounty:</span>
                            <a href="https://wiki.guildwars.com/wiki/{today_bounty[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{today_bounty[0]}</a>
                            <span style="color:#8b949e;font-size:0.85em;margin-left:8px;">({today_bounty[1]})</span>
                        </div>
                    </div>
                    
                    <!-- Vanquish -->
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;border-bottom:1px solid #30363d;">
                        <input type="checkbox" id="daily-vanquish" class="quest-checkbox" style="width:22px;height:22px;" data-daily="vanquish">
                        <div style="flex:1;">
                            <span style="color:#f85149;font-weight:bold;">⚔️ Vanquish:</span>
                            <a href="https://wiki.guildwars.com/wiki/{today_vanquish[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{today_vanquish[0]}</a>
                            <span style="color:#8b949e;font-size:0.85em;margin-left:8px;">({today_vanquish[1]})</span>
                        </div>
                    </div>
                    
                    <!-- Combat/PvP -->
                    <div style="display:flex;align-items:center;gap:15px;padding:15px;">
                        <input type="checkbox" id="daily-combat" class="quest-checkbox" style="width:22px;height:22px;" data-daily="combat">
                        <div style="flex:1;">
                            <span style="color:#a855f7;font-weight:bold;">🏆 PvP:</span>
                            <a href="https://wiki.guildwars.com/wiki/{today_combat[3]}" target="_blank" style="color:#fff;text-decoration:none;margin-left:8px;">{today_combat[0]}</a>
                        </div>
                    </div>
                </div>
                
                <h3 style="color:#ffa657;margin:25px 0 15px 0;">🛡️ Pre-Searing Vanguard</h3>
                <div style="background:#21262d;border-radius:12px;overflow:hidden;">'''
    
    for i, quest in enumerate(VANGUARD_QUESTS):
        name, qtype, location, wiki = quest
        quest_id = f"vanguard_{i}"
        border = "border-bottom:1px solid #30363d;" if i < len(VANGUARD_QUESTS) - 1 else ""
        
        h += f'''
                    <div style="display:flex;align-items:center;gap:15px;padding:12px 15px;{border}">
                        <input type="checkbox" id="{quest_id}" class="quest-checkbox" style="width:20px;height:20px;" data-daily="{quest_id}">
                        <a href="https://wiki.guildwars.com/wiki/{wiki}" target="_blank" style="color:#c9d1d9;text-decoration:none;flex:1;">{name}</a>
                        <span style="color:#79c0ff;font-size:0.85em;">{location}</span>
                    </div>'''
    
    h += '''
                </div>
                
                <div style="margin-top:20px;padding:15px;background:#21262d;border-radius:8px;">
                    <h4 style="color:#8b949e;margin:0 0 10px 0;">💡 Tips</h4>
                    <ul style="margin:0;color:#8b949e;font-size:0.85em;">
                        <li>Zaishen Coins → Balthazar faction, lockpicks, tomes</li>
                        <li>Checkboxes reset daily</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>'''
    return h

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
            <table>
                <thead>
                    <tr>
                        <th style="width:50px">Done</th>
                        <th style="width:50px">Bonus</th>
                        <th style="width:50px">HM</th>
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
            region_icon = MISSION_REGIONS.get(region, "🗺️")
            wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
            
            h += f'''
                    <tr data-type="{campaign_lower}" data-area="missions" data-id="{mission_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{mission_id}" data-area="missions" title="Normal Mode"></td>
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{bonus_id}" data-area="missions" title="Bonus/Masters" style="accent-color:#ffa657;"></td>
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{hm_id}" data-area="missions" title="Hard Mode" style="accent-color:#ff6b6b;"></td>
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
                <ul style="margin:0;color:#8b949e;font-size:0.9em;">
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
            <table>
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
        
        h += f'''
                    <tr data-type="elite" data-area="dungeons" data-id="{mission_id}">
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
            <table>
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
                <ul style="margin:0;color:#8b949e;font-size:0.9em;">
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
def generate_vanquish_html():
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
            <table>
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
            area_id = f"vanq_{name.lower().replace(' ', '_').replace(chr(39), '').replace(',', '')}"
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
                <ul style="margin:0;color:#8b949e;font-size:0.9em;">
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
            <table>
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
        wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
        hom_badge = "✅" if hom_eligible else "❌"
        
        h += f'''
                    <tr data-type="{campaign_lower}" data-area="armor" data-id="{armor_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{armor_id}" data-area="armor"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link">{campaign_icon} {name}</a></td>
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
                <ul style="margin:0;color:#8b949e;font-size:0.9em;">
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
            <table>
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
            
            h += f'''
                    <tr data-type="{rarity_lower}" data-area="minis" data-id="{mini_id}">
                        <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{mini_id}" data-area="minis"></td>
                        <td><a href="{wiki_url}" target="_blank" class="quest-link" style="color:{rarity_color};">🐾 {name}</a></td>
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
                <ul style="margin:0;color:#8b949e;font-size:0.9em;">
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
                <span style="font-size:1.5em;">🔗</span>
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

# === ELITE SKILLS (SKILL HUNTER) ===
def generate_elite_skills_html():
    prof_colors = {
        "Warrior": "#FFD700", "Ranger": "#228B22", "Monk": "#87CEEB", 
        "Necromancer": "#2E8B57", "Mesmer": "#DA70D6", "Elementalist": "#FF4500",
        "Assassin": "#4B0082", "Ritualist": "#008B8B", "Paragon": "#FF8C00", "Dervish": "#8B4513"
    }
    
    # Count totals
    total_skills = sum(len(skills) for skills in ELITE_SKILLS.values())
    tyria_count = sum(len([s for s in skills if s[2] == "Prophecies"]) for skills in ELITE_SKILLS.values())
    cantha_count = sum(len([s for s in skills if s[2] == "Factions"]) for skills in ELITE_SKILLS.values())
    elona_count = sum(len([s for s in skills if s[2] == "Nightfall"]) for skills in ELITE_SKILLS.values())
    
    h = f'''
    <div class="area" id="area-elites">
        <div class="content">
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-text">🎯 Legendary Skill Hunter ({total_skills} Elite Skills)</span>
                    <span class="progress-count"><span id="elites-completed">0</span> / <span id="elites-total">{total_skills}</span></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="elites-progress" style="width: 0%"></div>
                </div>
            </div>
            
            <div style="display:flex;gap:20px;margin:15px 0;flex-wrap:wrap;">
                <div style="flex:1;min-width:200px;background:#161b22;padding:10px;border-radius:8px;">
                    <div style="color:#ffd700;font-weight:bold;">Tyrian Skill Hunter</div>
                    <div style="font-size:0.9em;color:#8b949e;">{tyria_count} skills</div>
                    <div class="progress-bar" style="height:6px;margin-top:5px;">
                        <div class="progress-fill" id="elites-tyria-progress" style="width:0%;"></div>
                    </div>
                </div>
                <div style="flex:1;min-width:200px;background:#161b22;padding:10px;border-radius:8px;">
                    <div style="color:#ff6b6b;font-weight:bold;">Canthan Skill Hunter</div>
                    <div style="font-size:0.9em;color:#8b949e;">{cantha_count} skills</div>
                    <div class="progress-bar" style="height:6px;margin-top:5px;">
                        <div class="progress-fill" id="elites-cantha-progress" style="width:0%;"></div>
                    </div>
                </div>
                <div style="flex:1;min-width:200px;background:#161b22;padding:10px;border-radius:8px;">
                    <div style="color:#9d4edd;font-weight:bold;">Elonian Skill Hunter</div>
                    <div style="font-size:0.9em;color:#8b949e;">{elona_count} skills</div>
                    <div class="progress-bar" style="height:6px;margin-top:5px;">
                        <div class="progress-fill" id="elites-elona-progress" style="width:0%;"></div>
                    </div>
                </div>
            </div>
            
            <div style="background:#161b22;padding:15px;border-radius:8px;margin:15px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <span style="font-weight:bold;color:#58a6ff;">📊 Profession Progress (Secondary Switching Planner)</span>
                    <span style="font-size:0.85em;color:#8b949e;">Deine Primary: <span id="prof-progress-primary" style="color:#3fb950;">-</span> | Secondary: <span id="prof-progress-secondary" style="color:#ffa657;">-</span></span>
                </div>
                <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;" id="profession-progress-grid">
                    <div class="prof-progress-item" data-prof="warrior" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">⚔️</div>
                        <div style="font-size:0.75em;color:#FFD700;">Warrior</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-warrior-count">0/{len(ELITE_SKILLS.get('Warrior', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-warrior-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="ranger" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">🏹</div>
                        <div style="font-size:0.75em;color:#228B22;">Ranger</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-ranger-count">0/{len(ELITE_SKILLS.get('Ranger', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-ranger-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="monk" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">✨</div>
                        <div style="font-size:0.75em;color:#87CEEB;">Monk</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-monk-count">0/{len(ELITE_SKILLS.get('Monk', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-monk-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="necromancer" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">💀</div>
                        <div style="font-size:0.75em;color:#2E8B57;">Necromancer</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-necromancer-count">0/{len(ELITE_SKILLS.get('Necromancer', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-necromancer-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="mesmer" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">🎭</div>
                        <div style="font-size:0.75em;color:#DA70D6;">Mesmer</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-mesmer-count">0/{len(ELITE_SKILLS.get('Mesmer', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-mesmer-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="elementalist" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">🔥</div>
                        <div style="font-size:0.75em;color:#FF4500;">Elementalist</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-elementalist-count">0/{len(ELITE_SKILLS.get('Elementalist', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-elementalist-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="assassin" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">🗡️</div>
                        <div style="font-size:0.75em;color:#4B0082;">Assassin</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-assassin-count">0/{len(ELITE_SKILLS.get('Assassin', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-assassin-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="ritualist" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">👻</div>
                        <div style="font-size:0.75em;color:#008B8B;">Ritualist</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-ritualist-count">0/{len(ELITE_SKILLS.get('Ritualist', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-ritualist-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="paragon" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">🛡️</div>
                        <div style="font-size:0.75em;color:#FF8C00;">Paragon</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-paragon-count">0/{len(ELITE_SKILLS.get('Paragon', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-paragon-bar" style="width:0%;"></div></div>
                    </div>
                    <div class="prof-progress-item" data-prof="dervish" style="background:#21262d;padding:8px;border-radius:6px;text-align:center;">
                        <div style="font-size:1.2em;">🌀</div>
                        <div style="font-size:0.75em;color:#8B4513;">Dervish</div>
                        <div style="font-size:0.85em;font-weight:bold;" id="prof-dervish-count">0/{len(ELITE_SKILLS.get('Dervish', []))}</div>
                        <div class="progress-bar" style="height:4px;margin-top:4px;"><div class="progress-fill" id="prof-dervish-bar" style="width:0%;"></div></div>
                    </div>
                </div>
                <div style="margin-top:10px;font-size:0.8em;color:#8b949e;">
                    💡 <strong>Tip:</strong> Select your Primary/Secondary above. Green = your professions, Orange = recommended next (most missing skills).
                </div>
            </div>
            
            <div class="filters" data-area="elites">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="myskills" style="background:#238636;border-color:#238636;">🎯 My Skills</button>
                <button class="filter-btn" data-filter="core">Core</button>
                <button class="filter-btn" data-filter="prophecies">Prophecies</button>
                <button class="filter-btn" data-filter="factions">Factions</button>
                <button class="filter-btn" data-filter="nightfall">Nightfall</button>
            </div>
'''
    
    # Generate tables per profession
    for prof, skills in ELITE_SKILLS.items():
        color = prof_colors.get(prof, "#8b949e")
        prof_id = prof.lower()
        h += f'''
            <details style="margin-top:15px;" data-profession="{prof_id}" open>
                <summary style="cursor:pointer;padding:10px;background:#21262d;border-radius:8px;font-weight:bold;color:{color};">
                    {prof} <span style="color:#8b949e;font-weight:normal;">({len(skills)} skills)</span>
                </summary>
                <div class="container" style="margin-top:10px;">
                <table>
                    <thead>
                        <tr>
                            <th style="width:50px">Cap</th>
                            <th>Skill Name</th>
                            <th>Attribute</th>
                            <th>Campaign</th>
                        </tr>
                    </thead>
                    <tbody>'''
        
        for skill in skills:
            skill_name, _, campaign, attribute, wiki = skill
            skill_id = f"elite_{prof_id}_{skill_name.lower().replace(' ', '_').replace('!', '').replace(chr(39), '')}"
            campaign_lower = campaign.lower()
            wiki_url = f"https://wiki.guildwars.com/wiki/{wiki}"
            
            campaign_badge = {"Core": "badge-side", "Prophecies": "badge-main", "Factions": "badge-special", "Nightfall": "badge-endgame"}.get(campaign, "badge-side")
            
            h += f'''
                        <tr data-type="{campaign_lower}" data-area="elites" data-id="{skill_id}" data-campaign="{campaign_lower}" data-profession="{prof_id}">
                            <td class="checkbox-cell"><input type="checkbox" class="quest-checkbox" data-id="{skill_id}" data-area="elites" data-campaign="{campaign_lower}" data-profession="{prof_id}"></td>
                            <td><a href="{wiki_url}" target="_blank" class="quest-link">{skill_name}</a></td>
                            <td style="color:#8b949e;">{attribute if attribute else "-"}</td>
                            <td><span class="badge {campaign_badge}">{campaign}</span></td>
                        </tr>'''
        
        h += '''
                    </tbody>
                </table>
                </div>
            </details>'''
    
    h += '''
        </div>
    </div>'''
    return h

html += generate_elite_skills_html()

html += '''
    <script>
        // ==================== CHARACTER MANAGEMENT ====================
        let currentCharacter = null;
        
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
            populateCharSelect();
            clearUI();
            updateAllProgress();
        }
        
        function switchCharacter() {
            const select = document.getElementById('char-select');
            setCurrentCharacter(select.value);
            loadCampaign();
            loadProfessions();
            loadProgress();
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
            // Remove from list
            const idx = chars.indexOf(currentCharacter);
            chars.splice(idx, 1);
            saveCharacters(chars);
            // Switch to first char
            setCurrentCharacter(chars[0]);
            populateCharSelect();
            loadProgress();
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
                cb.closest('tr').classList.remove('completed', 'hm-done', 'bonus-done', 'hm-bonus-done');
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
        
        function loadProfessions() {
            const data = JSON.parse(localStorage.getItem(getProfessionKey()) || '{}');
            document.getElementById('primary-prof').value = data.primary || '';
            document.getElementById('secondary-prof').value = data.secondary || '';
            applyProfessionHighlighting();
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
            document.querySelectorAll('tr[data-profession]').forEach(row => {
                row.classList.remove('elite-capturable', 'elite-other');
            });
            
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
            document.querySelectorAll('tr[data-profession]').forEach(row => {
                const prof = row.dataset.profession;
                if (myProfs.includes(prof)) {
                    row.classList.add('elite-capturable');
                } else {
                    row.classList.add('elite-other');
                }
            });
            
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
                
                // Istan: ALL LOCKED - Prophecies chars skip Istan entirely, start in Kamadan later areas
                document.querySelectorAll('tr[data-area="istan"]').forEach(row => lockRow(row));
            }
            
            if (campaign === 'factions') {
                // Pre-Searing: ALL locked
                document.querySelectorAll('tr[data-area="pre"]').forEach(row => lockRow(row));
                
                // Post-Searing: ALL QUESTS locked (require Prophecies char), only Missions OK
                document.querySelectorAll('tr[data-area="post"][data-type="main"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="post"][data-type="side"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="post"][data-type="profession"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="post"][data-type="special"]').forEach(row => lockRow(row));
                
                // N. Shiverpeaks: ALL QUESTS locked (require Prophecies char), only Missions OK
                document.querySelectorAll('tr[data-area="shiver"][data-type="main"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="shiver"][data-type="side"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="shiver"][data-type="profession"]').forEach(row => lockRow(row));
                
                // Shing Jea: OK (home)
                
                // Istan: ALL LOCKED - Factions chars skip Istan entirely
                document.querySelectorAll('tr[data-area="istan"]').forEach(row => lockRow(row));
            }
            
            if (campaign === 'nightfall') {
                // Pre-Searing: ALL locked
                document.querySelectorAll('tr[data-area="pre"]').forEach(row => lockRow(row));
                
                // Post-Searing: ALL QUESTS locked (require Prophecies char), only Missions OK
                document.querySelectorAll('tr[data-area="post"][data-type="main"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="post"][data-type="side"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="post"][data-type="profession"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="post"][data-type="special"]').forEach(row => lockRow(row));
                
                // N. Shiverpeaks: ALL QUESTS locked (require Prophecies char), only Missions OK
                document.querySelectorAll('tr[data-area="shiver"][data-type="main"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="shiver"][data-type="side"]').forEach(row => lockRow(row));
                document.querySelectorAll('tr[data-area="shiver"][data-type="profession"]').forEach(row => lockRow(row));
                
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
                // Other campaigns' attribute quests are unavailable
                document.querySelectorAll('tr[data-area="shingjea"][data-type="attribute"]').forEach(row => row.classList.add('attr-unavailable'));
                document.querySelectorAll('tr[data-area="istan"][data-type="attribute"]').forEach(row => row.classList.add('attr-unavailable'));
            }
            if (campaign === 'factions') {
                document.querySelectorAll('tr[data-area="shingjea"][data-type="attribute"]').forEach(row => row.classList.add('attr-highlight'));
                // Other campaigns' attribute quests are unavailable
                document.querySelectorAll('tr[data-area="desert"][data-type="attribute"]').forEach(row => row.classList.add('attr-unavailable'));
                document.querySelectorAll('tr[data-area="sshiver"][data-type="attribute"]').forEach(row => row.classList.add('attr-unavailable'));
                document.querySelectorAll('tr[data-area="istan"][data-type="attribute"]').forEach(row => row.classList.add('attr-unavailable'));
            }
            if (campaign === 'nightfall') {
                document.querySelectorAll('tr[data-area="istan"][data-type="attribute"]').forEach(row => row.classList.add('attr-highlight'));
                // Other campaigns' attribute quests are unavailable
                document.querySelectorAll('tr[data-area="desert"][data-type="attribute"]').forEach(row => row.classList.add('attr-unavailable'));
                document.querySelectorAll('tr[data-area="sshiver"][data-type="attribute"]').forEach(row => row.classList.add('attr-unavailable'));
                document.querySelectorAll('tr[data-area="shingjea"][data-type="attribute"]').forEach(row => row.classList.add('attr-unavailable'));
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
            } else if (category === 'armor') {
                document.getElementById('area-armor').classList.add('active');
            } else if (category === 'minis') {
                document.getElementById('area-minis').classList.add('active');
            } else if (category === 'uniques') {
                document.getElementById('area-uniques').classList.add('active');
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
        function loadProgress() {
            clearUI();
            const saved = JSON.parse(localStorage.getItem(getProgressKey()) || '{}');
            document.querySelectorAll('.quest-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                    cb.closest('tr').classList.add('completed');
                }
            });
            document.querySelectorAll('.hm-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                    cb.closest('tr').classList.add('hm-done');
                }
            });
            document.querySelectorAll('.bonus-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                    cb.closest('tr').classList.add('bonus-done');
                }
            });
            document.querySelectorAll('.hm-bonus-checkbox').forEach(cb => {
                if (saved[cb.dataset.id]) {
                    cb.checked = true;
                    cb.closest('tr').classList.add('hm-bonus-done');
                }
            });
            // Load title progress
            document.querySelectorAll('.title-progress-input').forEach(input => {
                const val = saved[input.dataset.id + '_progress'] || 0;
                input.value = val;
                updateTitleProgressBar(input);
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
            localStorage.setItem(getProgressKey(), JSON.stringify(progress));
        }
        
        // Update title progress bar
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
        
        // Update progress for an area
        function updateProgress(areaId) {
            // Count only DOABLE quests:
            // - Exclude campaign-locked quests (can't do them with this campaign)
            // - Exclude other-profession quests (can't do them with this build, except Pre-Searing)
            const allRows = document.querySelectorAll(`tr[data-area="${areaId}"]:not(.campaign-locked):not(.other-profession)`);
            const allChecked = document.querySelectorAll(`tr[data-area="${areaId}"]:not(.campaign-locked):not(.other-profession) .quest-checkbox:checked`);
            const total = allRows.length;
            const completed = allChecked.length;
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
            updateProgress('vanquish');
            updateProgress('armor');
            updateProgress('minis');
            updateProgress('daily');
            updateProgress('uniques');
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
        
        // Checkbox handler
        document.querySelectorAll('.quest-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                this.closest('tr').classList.toggle('completed', this.checked);
                saveProgress();
                updateProgress(this.dataset.area);
                if (this.dataset.area === 'elites') updateElitesCampaignProgress();
            });
        });
        
        // HM checkbox handler
        document.querySelectorAll('.hm-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                this.closest('tr').classList.toggle('hm-done', this.checked);
                saveProgress();
            });
        });
        
        // Bonus checkbox handler
        document.querySelectorAll('.bonus-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                this.closest('tr').classList.toggle('bonus-done', this.checked);
                saveProgress();
            });
        });
        
        // HM Bonus checkbox handler
        document.querySelectorAll('.hm-bonus-checkbox').forEach(cb => {
            cb.addEventListener('change', function() {
                this.closest('tr').classList.toggle('hm-bonus-done', this.checked);
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
                
                if (isProfFilter) {
                    this.classList.toggle('active');
                } else {
                    container.querySelectorAll('.filter-btn').forEach(b => {
                        if (!profFilters.includes(b.dataset.filter)) {
                            b.classList.remove('active');
                        }
                    });
                    this.classList.add('active');
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
                
                // For elites, filter by campaign
                if (areaId === 'elites') {
                    let showCampaign = (typeFilter === 'all' || rowCampaign === typeFilter);
                    row.classList.toggle('hidden', !showCampaign);
                } else {
                    let showType = (typeFilter === 'all' || rowType === typeFilter);
                    let showProf = (activeProfs.length === 0 || activeProfs.includes(rowProf) || rowType !== 'profession');
                    
                    if (activeProfs.length > 0 && rowType === 'profession') {
                        showProf = activeProfs.includes(rowProf);
                    }
                    
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
                    localStorage.setItem(getProgressKey(), JSON.stringify(currentProgress));
                    
                    document.querySelectorAll(`tr[data-area="${areaId}"] .quest-checkbox`).forEach(cb => {
                        const isChecked = !!currentProgress[cb.dataset.id];
                        cb.checked = isChecked;
                        cb.closest('tr').classList.toggle('completed', isChecked);
                    });
                    
                    updateProgress(areaId);
                    alert('Import erfolgreich für ' + currentCharacter + '! ' + Object.keys(importedProgress).length + ' Eintraege geladen.');
                } catch (err) {
                    alert('Import Fehler: ' + err.message);
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
        updateElitesCampaignProgress();
        applyProfessionHighlighting();
        
        console.log('GW Companion initialized!');
    </script>
</body>
</html>'''

with open('gw_tracker.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Guild Wars Companion gestartet!")
print("http://localhost:8000")

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/gw_tracker.html'
        return super().do_GET()

HTTPServer(('localhost', 8000), Handler).serve_forever()
