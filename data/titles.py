#!/usr/bin/env python3
"""
Guild Wars Title Tracker
All titles needed for GWAMM (God Walking Amongst Mere Mortals)
"""

# =============================================================================
# GWAMM TITLES - Need 30 maxed titles for GWAMM
# =============================================================================

# Format: (Name, Max Rank, Type, Campaign, Description)
TITLES = [
    # =========================================================================
    # ACCOUNT-WIDE TITLES (shared across all characters)
    # =========================================================================
    ("Lucky", 7, "Account", "Core", "Lucky points from Lucky/Unlucky rolls"),
    ("Unlucky", 7, "Account", "Core", "Unlucky points from Lucky/Unlucky rolls"),
    ("Treasure Hunter", 8, "Account", "Core", "Chests opened"),
    ("Wisdom", 8, "Account", "Core", "Unidentified golds identified"),
    ("Sweet Tooth", 7, "Account", "Core", "Sweets consumed"),
    ("Party Animal", 7, "Account", "Core", "Party items used"),
    ("Drunkard", 7, "Account", "Core", "Minutes spent drunk"),
    
    # =========================================================================
    # PVE CHARACTER TITLES
    # =========================================================================
    # Prophecies
    ("Legendary Defender of Ascalon", 1, "Character", "Prophecies", "Level 20 in Pre-Searing"),
    ("Protector of Tyria", 1, "Character", "Prophecies", "All Prophecies missions with bonus"),
    ("Guardian of Tyria", 1, "Character", "Prophecies", "All Prophecies missions in HM"),
    ("Tyrian Cartographer", 1, "Character", "Prophecies", "100% Tyria map explored"),
    ("Tyrian Skill Hunter", 1, "Character", "Prophecies", "All Tyria elite skills captured"),
    ("Tyrian Vanquisher", 1, "Character", "Prophecies", "All Tyria areas vanquished"),
    
    # Factions
    ("Protector of Cantha", 1, "Character", "Factions", "All Factions missions with bonus"),
    ("Guardian of Cantha", 1, "Character", "Factions", "All Factions missions in HM"),
    ("Canthan Cartographer", 1, "Character", "Factions", "100% Cantha map explored"),
    ("Canthan Skill Hunter", 1, "Character", "Factions", "All Cantha elite skills captured"),
    ("Canthan Vanquisher", 1, "Character", "Factions", "All Cantha areas vanquished"),
    ("Legendary Spearmarshal", 10, "Character", "Factions", "Kurzick or Luxon faction rank"),
    ("Savior of the Kurzicks", 12, "Character", "Factions", "Kurzick faction donated"),
    ("Savior of the Luxons", 12, "Character", "Factions", "Luxon faction donated"),
    
    # Nightfall
    ("Protector of Elona", 1, "Character", "Nightfall", "All Nightfall missions with bonus"),
    ("Guardian of Elona", 1, "Character", "Nightfall", "All Nightfall missions in HM"),
    ("Elonian Cartographer", 1, "Character", "Nightfall", "100% Elona map explored"),
    ("Elonian Skill Hunter", 1, "Character", "Nightfall", "All Elona elite skills captured"),
    ("Elonian Vanquisher", 1, "Character", "Nightfall", "All Elona areas vanquished"),
    ("Sunspear General", 10, "Character", "Nightfall", "Sunspear rank"),
    ("Lightbringer", 8, "Character", "Nightfall", "Lightbringer rank"),
    
    # Eye of the North
    ("Master of the North", 1, "Character", "EotN", "All EotN missions in HM"),
    ("Ebon Vanguard", 10, "Character", "EotN", "Ebon Vanguard rank"),
    ("Deldrimor", 10, "Character", "EotN", "Deldrimor rank"),
    ("Norn", 10, "Character", "EotN", "Norn rank"),
    ("Asura", 10, "Character", "EotN", "Asura rank"),
    
    # =========================================================================
    # ELITE MISSION TITLES
    # =========================================================================
    ("Conqueror of the Fissure of Woe", 1, "Character", "Core", "Complete FoW"),
    ("Conqueror of the Underworld", 1, "Character", "Core", "Complete UW"),
    ("Conqueror of the Deep", 1, "Character", "Factions", "Complete The Deep"),
    ("Conqueror of Urgoz's Warren", 1, "Character", "Factions", "Complete Urgoz's Warren"),
    ("Conqueror of the Domain of Anguish", 1, "Character", "Nightfall", "Complete all DoA areas"),
    
    # =========================================================================
    # OTHER TITLES
    # =========================================================================
    ("Survivor", 3, "Character", "Core", "XP without dying (1,337,500 XP)"),
    ("Legendary Cartographer", 1, "Character", "Core", "All 3 Cartographer titles"),
    ("Legendary Guardian", 1, "Character", "Core", "All 3 Guardian titles"),
    ("Legendary Skill Hunter", 1, "Character", "Core", "All 3 Skill Hunter titles"),
    ("Legendary Vanquisher", 1, "Character", "Core", "All 3 Vanquisher titles"),
    ("People Know Me", 10, "Character", "Core", "Fame from Hero Battles/GvG"),
    ("Champion", 12, "Character", "Core", "Champion points from PvP"),
    ("Codex Disciple", 10, "Character", "Core", "Codex Arena wins"),
    ("Hero of the Zaishen", 6, "Character", "Core", "Zaishen Challenge wins"),
    ("Zaishen Supporter", 8, "Character", "Core", "Zaishen Coin donations"),
]

# =========================================================================
# GWAMM RECOMMENDED TITLES (easiest 30 for PvE players)
# =========================================================================
GWAMM_RECOMMENDED = [
    # PvE Core (7)
    "Lucky", "Unlucky", "Treasure Hunter", "Wisdom", 
    "Sweet Tooth", "Party Animal", "Drunkard",
    
    # Prophecies (6)
    "Protector of Tyria", "Guardian of Tyria", 
    "Tyrian Cartographer", "Tyrian Skill Hunter", "Tyrian Vanquisher",
    "Legendary Defender of Ascalon",  # Optional - takes time
    
    # Factions (5)
    "Protector of Cantha", "Guardian of Cantha",
    "Canthan Cartographer", "Canthan Skill Hunter", "Canthan Vanquisher",
    
    # Nightfall (7)
    "Protector of Elona", "Guardian of Elona",
    "Elonian Cartographer", "Elonian Skill Hunter", "Elonian Vanquisher",
    "Sunspear General", "Lightbringer",
    
    # EotN (5)
    "Master of the North",
    "Ebon Vanguard", "Deldrimor", "Norn", "Asura",
    
    # Legendary (4)
    "Legendary Cartographer", "Legendary Guardian",
    "Legendary Skill Hunter", "Legendary Vanquisher",
    
    # Survivor (1)
    "Survivor",
]

print(f"Total Titles: {len(TITLES)}")
print(f"GWAMM Recommended: {len(GWAMM_RECOMMENDED)} titles")
print(f"Need 30 for GWAMM")
