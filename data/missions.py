#!/usr/bin/env python3
"""
Guild Wars Missions Database
All story missions with bonus objectives
"""

# Format: (mission_name, region, campaign, wiki_link)
# Bonus = complete bonus objective
# Masters = complete in time (Expert's/Master's)

# ==================== PROPHECIES (25 missions) ====================
PROPHECIES_MISSIONS = [
    # Pre-Searing
    ("Ascalon Academy", "Pre-Searing", "Prophecies", "Ascalon_Academy"),
    
    # Ascalon
    ("The Great Northern Wall", "Ascalon", "Prophecies", "The_Great_Northern_Wall"),
    ("Fort Ranik", "Ascalon", "Prophecies", "Fort_Ranik"),
    ("Ruins of Surmia", "Ascalon", "Prophecies", "Ruins_of_Surmia"),
    ("Nolani Academy", "Ascalon", "Prophecies", "Nolani_Academy"),
    
    # Northern Shiverpeaks
    ("Borlis Pass", "Northern Shiverpeaks", "Prophecies", "Borlis_Pass"),
    ("The Frost Gate", "Northern Shiverpeaks", "Prophecies", "The_Frost_Gate"),
    
    # Kryta
    ("Gates of Kryta", "Kryta", "Prophecies", "Gates_of_Kryta"),
    ("D'Alessio Seaboard", "Kryta", "Prophecies", "D%27Alessio_Seaboard"),
    ("Divinity Coast", "Kryta", "Prophecies", "Divinity_Coast"),
    
    # Maguuma
    ("The Wilds", "Maguuma Jungle", "Prophecies", "The_Wilds"),
    ("Bloodstone Fen", "Maguuma Jungle", "Prophecies", "Bloodstone_Fen"),
    ("Aurora Glade", "Maguuma Jungle", "Prophecies", "Aurora_Glade"),
    ("Riverside Province", "Kryta", "Prophecies", "Riverside_Province"),
    ("Sanctum Cay", "Kryta", "Prophecies", "Sanctum_Cay"),
    
    # Crystal Desert
    ("Dunes of Despair", "Crystal Desert", "Prophecies", "Dunes_of_Despair"),
    ("Thirsty River", "Crystal Desert", "Prophecies", "Thirsty_River"),
    ("Elona Reach", "Crystal Desert", "Prophecies", "Elona_Reach"),
    ("Augury Rock", "Crystal Desert", "Prophecies", "Augury_Rock"),
    ("The Dragon's Lair", "Crystal Desert", "Prophecies", "The_Dragon%27s_Lair"),
    
    # Southern Shiverpeaks
    ("Ice Caves of Sorrow", "Southern Shiverpeaks", "Prophecies", "Ice_Caves_of_Sorrow"),
    ("Iron Mines of Moladune", "Southern Shiverpeaks", "Prophecies", "Iron_Mines_of_Moladune"),
    ("Thunderhead Keep", "Southern Shiverpeaks", "Prophecies", "Thunderhead_Keep"),
    
    # Ring of Fire
    ("Ring of Fire", "Ring of Fire", "Prophecies", "Ring_of_Fire"),
    ("Abaddon's Mouth", "Ring of Fire", "Prophecies", "Abaddon%27s_Mouth"),
    ("Hell's Precipice", "Ring of Fire", "Prophecies", "Hell%27s_Precipice"),
]

# ==================== FACTIONS (13 missions) ====================
FACTIONS_MISSIONS = [
    # Shing Jea Island
    ("Minister Cho's Estate", "Shing Jea Island", "Factions", "Minister_Cho%27s_Estate"),
    ("Zen Daijun", "Shing Jea Island", "Factions", "Zen_Daijun"),
    
    # Kaineng City
    ("Vizunah Square", "Kaineng City", "Factions", "Vizunah_Square"),
    ("Nahpui Quarter", "Kaineng City", "Factions", "Nahpui_Quarter"),
    ("Tahnnakai Temple", "Kaineng City", "Factions", "Tahnnakai_Temple"),
    ("Arborstone", "Echovald Forest", "Factions", "Arborstone"),
    ("Boreas Seabed", "The Jade Sea", "Factions", "Boreas_Seabed"),
    
    # Echovald/Jade Sea
    ("The Eternal Grove", "Echovald Forest", "Factions", "The_Eternal_Grove"),
    ("Gyala Hatchery", "The Jade Sea", "Factions", "Gyala_Hatchery"),
    
    # Endgame
    ("Unwaking Waters", "The Jade Sea", "Factions", "Unwaking_Waters"),
    ("Raisu Palace", "Kaineng City", "Factions", "Raisu_Palace"),
    ("Imperial Sanctum", "Kaineng City", "Factions", "Imperial_Sanctum"),
]

# ==================== NIGHTFALL (20 missions) ====================
NIGHTFALL_MISSIONS = [
    # Istan
    ("Chahbek Village", "Istan", "Nightfall", "Chahbek_Village"),
    ("Jokanur Diggings", "Istan", "Nightfall", "Jokanur_Diggings"),
    ("Blacktide Den", "Istan", "Nightfall", "Blacktide_Den"),
    ("Consulate Docks", "Istan", "Nightfall", "Consulate_Docks"),
    
    # Kourna
    ("Venta Cemetery", "Kourna", "Nightfall", "Venta_Cemetery"),
    ("Kodonur Crossroads", "Kourna", "Nightfall", "Kodonur_Crossroads"),
    ("Pogahn Passage", "Kourna", "Nightfall", "Pogahn_Passage"),
    ("Rilohn Refuge", "Kourna", "Nightfall", "Rilohn_Refuge"),
    ("Moddok Crevice", "Kourna", "Nightfall", "Moddok_Crevice"),
    
    # Vabbi
    ("Tihark Orchard", "Vabbi", "Nightfall", "Tihark_Orchard"),
    ("Dasha Vestibule", "Vabbi", "Nightfall", "Dasha_Vestibule"),
    ("Dzagonur Bastion", "Vabbi", "Nightfall", "Dzagonur_Bastion"),
    ("Grand Court of Sebelkeh", "Vabbi", "Nightfall", "Grand_Court_of_Sebelkeh"),
    
    # The Desolation
    ("Jennur's Horde", "The Desolation", "Nightfall", "Jennur%27s_Horde"),
    ("Nundu Bay", "The Desolation", "Nightfall", "Nundu_Bay"),
    ("Gate of Desolation", "The Desolation", "Nightfall", "Gate_of_Desolation"),
    ("Ruins of Morah", "The Desolation", "Nightfall", "Ruins_of_Morah"),
    
    # Realm of Torment
    ("Gate of Pain", "Realm of Torment", "Nightfall", "Gate_of_Pain"),
    ("Gate of Madness", "Realm of Torment", "Nightfall", "Gate_of_Madness"),
    ("Abaddon's Gate", "Realm of Torment", "Nightfall", "Abaddon%27s_Gate"),
]

# ==================== EYE OF THE NORTH (Not missions, but primary quests) ====================
# EotN doesn't have traditional missions, but has primary storyline quests

# Combined list
ALL_MISSIONS = PROPHECIES_MISSIONS + FACTIONS_MISSIONS + NIGHTFALL_MISSIONS

# Region icons
MISSION_REGIONS = {
    # Prophecies
    "Pre-Searing": "🌅",
    "Ascalon": "🏚️",
    "Northern Shiverpeaks": "❄️",
    "Kryta": "🌳",
    "Maguuma Jungle": "🌿",
    "Crystal Desert": "🏜️",
    "Southern Shiverpeaks": "🏔️",
    "Ring of Fire": "🌋",
    # Factions
    "Shing Jea Island": "🏝️",
    "Kaineng City": "🏙️",
    "Echovald Forest": "🌲",
    "The Jade Sea": "💎",
    # Nightfall
    "Istan": "☀️",
    "Kourna": "⚔️",
    "Vabbi": "💰",
    "The Desolation": "💀",
    "Realm of Torment": "😈",
}
