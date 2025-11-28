#!/usr/bin/env python3
"""
Guild Wars Unique Items Database
- Quest Rewards: Items from specific quests
- Green Uniques: Named boss drops (green rarity)
- HoM Weapons: Craftable weapon sets for Hall of Monuments
"""

# ==================== PRE-SEARING QUEST REWARDS ====================
# Format: (item_name, type, quest_name, notes, wiki_link)
PRE_SEARING_REWARDS = [
    ("Longbow", "Bow", "The Hunter's Horn", "15-22 dmg, best bow", "Longbow_(pre-Searing)"),
    ("War Hammer", "Hammer", "The True King", "14-20 dmg", "War_Hammer"),
    ("Battle Axe", "Axe", "Little Thom's Big Cloak", "6-20 dmg", "Battle_Axe"),
    ("Long Sword", "Sword", "Charr at the Gate", "10-15 dmg", "Long_Sword"),
    ("Rinblade", "Sword", "Arthur Ayala (craft)", "Requires Charr Carvings", "Rinblade"),
    ("Air Staff", "Staff", "The Wayward Wizard", "Lightning damage", "Air_Staff"),
    ("Smiting Staff", "Staff", "The Prize Moa Bird", "Holy damage", "Smiting_Staff"),
    ("Jeweled Staff", "Staff", "The Rogue's Replacement", "Chaos damage", "Jeweled_Staff"),
    ("Fire Wand", "Wand", "The Worm Problem", "Fire damage", "Fire_Wand"),
    ("Cane", "Wand", "Little Thom's Big Cloak", "Chaos damage", "Cane"),
    ("Flame Artifact", "Focus", "Bandit Raid", "Fire damage", "Flame_Artifact"),
    ("Healing Ankh", "Focus", "The Poison Devourer", "+Health", "Healing_Ankh"),
    ("Divine Symbol", "Focus", "Poor Tenant", "+Energy", "Divine_Symbol"),
    ("Storm Artifact", "Focus", "The Orchard", "Elemental armor", "Storm_Artifact"),
    ("Inscribed Chakram", "Focus", "A Gift for Althea", "Mesmer focus", "Inscribed_Chakram"),
    ("Deadly Cesta", "Focus", "Across the Wall", "Dark damage", "Deadly_Cesta"),
    ("Grim Cesta", "Focus", "Rites of Remembrance", "Necro focus", "Grim_Cesta"),
    ("Tall Shield", "Shield", "Bandit Raid", "vs Charr", "Tall_Shield"),
]

# ==================== HOM WEAPON SETS ====================
# Format: (set_name, source, points, wiki_link)
HOM_WEAPON_SETS = [
    ("Destroyer Weapon", "Craftable (EotN)", "1-5 pts", "Destroyer_weapon"),
    ("Tormented Weapon", "Domain of Anguish", "1-5 pts", "Tormented_weapon"),
    ("Oppressor's Weapon", "War in Kryta (War Supplies)", "1-5 pts", "Oppressor%27s_weapon"),
]

# ==================== GREEN UNIQUES (Boss Drops) ====================
# Format: (item_name, type, boss_name, location, campaign, wiki_link)
GREEN_UNIQUES = [
    # PROPHECIES - Warrior
    ("Bludgeoner", "Hammer", "Thorgall Bludgeonhammer", "Grenth's Footprint", "Prophecies", "Bludgeoner_(unique)"),
    ("Totem Axe", "Axe", "Root Behemoth", "The Falls", "Prophecies", "Totem_Axe"),
    ("Victo's Blade", "Sword", "The Darkness", "Hall of Heroes", "Prophecies", "Victo%27s_Blade"),
    ("The Ice Breaker", "Hammer", "Mighty Grawl", "Talus Chute", "Prophecies", "The_Ice_Breaker"),
    ("Grognar's Blade", "Sword", "Grognard Gravelhead", "Sorrow's Furnace", "Prophecies", "Grognar%27s_Blade"),
    ("Razorstone", "Axe", "Tanzit Razorstone", "Sorrow's Furnace", "Prophecies", "Razorstone"),
    
    # PROPHECIES - Ranger
    ("Drago's Flatbow", "Bow", "Drago Stoneherder", "Sorrow's Furnace", "Prophecies", "Drago%27s_Flatbow"),
    ("Boulderbeard's Shortbow", "Bow", "Graygore Boulderbeard", "Sorrow's Furnace", "Prophecies", "Boulderbeard%27s_Shortbow"),
    
    # PROPHECIES - Caster
    ("The Yakslapper", "Staff", "Wroth Yakslapper", "Deldrimor Bowl", "Prophecies", "The_Yakslapper"),
    ("Kepkhet's Refuge", "Staff", "Kepkhet Marrowfeast", "Diviner's Ascent", "Prophecies", "Kepkhet%27s_Refuge"),
    
    # FACTIONS - Popular
    ("Naga Fang", "Sword", "Sskai, Dragon's Birth", "Dragon's Throat", "Factions", "Naga_Fang"),
    ("The Ugly Stick", "Hammer", "Ssuns, Blessed of Dwayna", "Maishang Hills", "Factions", "The_Ugly_Stick"),
    ("Zodiac Sword", "Sword", "Willa the Unpleasant", "Silent Surf", "Factions", "Zodiac_Sword"),
    
    # NIGHTFALL - Popular
    ("Droknar's Staff", "Staff", "Various", "Droknar's Forge", "Prophecies", "Droknar%27s_Staff"),
    ("Victo's Maul", "Hammer", "The Darkness", "Hall of Heroes", "Prophecies", "Victo%27s_Maul"),
    
    # ELITE AREA GREENS
    ("Deldrimor Axe", "Axe", "Artisan of Steel", "Droknar's Forge", "Prophecies", "Deldrimor_Axe_(unique)"),
    ("Deldrimor Sword", "Sword", "Artisan of Steel", "Droknar's Forge", "Prophecies", "Deldrimor_Sword_(unique)"),
    ("Deldrimor Longbow", "Bow", "Artisan of Nature", "Droknar's Forge", "Prophecies", "Deldrimor_Longbow_(unique)"),
    
    # FoW/UW Greens
    ("Crystalline Sword", "Sword", "Chest Drop", "Fissure of Woe", "Core", "Crystalline_Sword"),
    ("Voltaic Spear", "Spear", "Chest Drop", "Underworld", "Core", "Voltaic_Spear"),
]

# Categories for filtering
ITEM_CATEGORIES = {
    "Sword": "⚔️",
    "Axe": "🪓",
    "Hammer": "🔨",
    "Bow": "🏹",
    "Staff": "🪄",
    "Wand": "✨",
    "Focus": "🔮",
    "Shield": "🛡️",
    "Spear": "🔱",
}

# Combined list for the tracker
UNIQUE_QUEST_ITEMS = []

# Add Pre-Searing rewards
for item in PRE_SEARING_REWARDS:
    name, itype, quest, notes, wiki = item
    UNIQUE_QUEST_ITEMS.append((name, itype, quest, "Pre-Searing", "Prophecies", notes, wiki))

# Add HoM weapons
for item in HOM_WEAPON_SETS:
    name, source, points, wiki = item
    UNIQUE_QUEST_ITEMS.append((name, "Weapon Set", source, "Various", "HoM", points, wiki))

# Add Green Uniques
for item in GREEN_UNIQUES:
    name, itype, boss, location, campaign, wiki = item
    UNIQUE_QUEST_ITEMS.append((name, itype, boss, location, campaign, "Boss drop", wiki))
