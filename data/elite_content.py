#!/usr/bin/env python3
"""
Guild Wars Elite Content Database
- Elite Missions (end-game group content)
- EotN Dungeons (instanced dungeons)
"""

# ==================== ELITE MISSIONS ====================
# Format: (name, campaign, party_size, description, wiki_link)
ELITE_MISSIONS = [
    # CORE (accessible from anywhere)
    ("Fissure of Woe", "Core", "8", "Realm of Balthazar, 11 quests", "The_Fissure_of_Woe"),
    ("The Underworld", "Core", "8", "Realm of Grenth, 11 quests", "The_Underworld"),
    
    # PROPHECIES
    ("Sorrow's Furnace", "Prophecies", "8", "Dwarven dungeon, Stone Summit", "Sorrow%27s_Furnace"),
    
    # FACTIONS
    ("The Deep", "Factions", "12", "Luxon elite mission, Kanaxai", "The_Deep"),
    ("Urgoz's Warren", "Factions", "12", "Kurzick elite mission, Urgoz", "Urgoz%27s_Warren"),
    
    # NIGHTFALL
    ("Tomb of the Primeval Kings", "Nightfall", "8", "Ancient kings, required for Ebony Citadel", "Tomb_of_the_Primeval_Kings"),
    ("Domain of Anguish", "Nightfall", "8", "4 areas + Mallyx the Unyielding", "Domain_of_Anguish"),
]

# ==================== EOTN DUNGEONS ====================
# Format: (name, region, floors, boss, wiki_link)
EOTN_DUNGEONS = [
    # CHARR HOMELANDS
    ("Cathedral of Flames", "Charr Homelands", 3, "Murakai", "Cathedral_of_Flames"),
    ("Ooze Pit", "Charr Homelands", 1, "Havok Soulwail", "Ooze_Pit"),
    ("Rragar's Menagerie", "Charr Homelands", 3, "Rragar Maneater", "Rragar%27s_Menagerie"),
    
    # FAR SHIVERPEAKS
    ("Darkrime Delves", "Far Shiverpeaks", 3, "Havok Soulwail", "Darkrime_Delves"),
    ("Frostmaw's Burrows", "Far Shiverpeaks", 5, "Frostmaw the Kinslayer", "Frostmaw%27s_Burrows"),
    ("Sepulchre of Dragrimmar", "Far Shiverpeaks", 1, "Remnant of Antiquities", "Sepulchre_of_Dragrimmar"),
    ("Raven's Point", "Far Shiverpeaks", 3, "Plague of Destruction", "Raven%27s_Point"),
    
    # TARNISHED COAST
    ("Arachni's Haunt", "Tarnished Coast", 2, "Arachni", "Arachni%27s_Haunt"),
    ("Bloodstone Caves", "Tarnished Coast", 3, "Inculta, Ascension of Blood", "Bloodstone_Caves"),
    ("Oola's Lab", "Tarnished Coast", 3, "TPS Regulator Golem", "Oola%27s_Lab"),
    ("Vloxen Excavations", "Tarnished Coast", 3, "Zoldark the Unholy", "Vloxen_Excavations"),
    
    # DEPTHS OF TYRIA
    ("Bogroot Growths", "Depths of Tyria", 2, "Khabuus", "Bogroot_Growths"),
    ("Shards of Orr", "Depths of Tyria", 3, "Fendi Nin", "Shards_of_Orr"),
    ("Heart of the Shiverpeaks", "Depths of Tyria", 3, "Duncan the Black", "Heart_of_the_Shiverpeaks"),
    
    # SPECIAL DUNGEONS
    ("Slavers' Exile", "Depths of Tyria", 5, "5 Dungeon Bosses", "Slavers%27_Exile"),
    ("Catacombs of Kathandrax", "Charr Homelands", 3, "Ilsundur, Lord of Fire", "Catacombs_of_Kathandrax"),
    ("Fronis Irontoe's Lair", "Depths of Tyria", 1, "Fronis Irontoe", "Fronis_Irontoe%27s_Lair"),
    ("Secret Lair of the Snowmen", "Far Shiverpeaks", 1, "Freezie", "Secret_Lair_of_the_Snowmen"),
]

# Dungeon regions for filtering
DUNGEON_REGIONS = {
    "Charr Homelands": "🔥",
    "Far Shiverpeaks": "❄️",
    "Tarnished Coast": "🌿",
    "Depths of Tyria": "⛏️",
}

# Campaign icons
CAMPAIGN_ICONS = {
    "Core": "🌐",
    "Prophecies": "⚔️",
    "Factions": "🐉",
    "Nightfall": "☀️",
    "Eye of the North": "🏔️",
}
