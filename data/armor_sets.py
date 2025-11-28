#!/usr/bin/env python3
"""
Guild Wars Elite/Prestige Armor Sets Database
For HoM: Resilience Monument
"""

# Format: (armor_name, location, campaign, requirement, hom_eligible, wiki_link)

# ==================== CORE ====================
CORE_ARMOR = [
    ("Obsidian Armor", "Fissure of Woe", "Core", "FoW Quests completed", True, "Obsidian_armor"),
]

# ==================== PROPHECIES ====================
PROPHECIES_ARMOR = [
    # Droknar's Forge - All professions
    ("Elite Charr Hide", "Droknar's Forge", "Prophecies", "15k gold", True, "Warrior_Elite_Charr_Hide_armor"),
    ("Elite Gladiator", "Droknar's Forge", "Prophecies", "15k gold", True, "Warrior_Elite_Gladiator_armor"),
    ("Elite Templar", "Droknar's Forge", "Prophecies", "15k gold", True, "Warrior_Elite_Templar_armor"),
    ("Elite Drakescale", "Droknar's Forge", "Prophecies", "15k gold", True, "Ranger_Elite_Drakescale_armor"),
    ("Elite Druid", "Droknar's Forge", "Prophecies", "15k gold", True, "Ranger_Elite_Druid_armor"),
    ("Elite Saintly", "Droknar's Forge", "Prophecies", "15k gold", True, "Monk_Elite_Saintly_armor"),
    ("Labyrinthine", "Droknar's Forge", "Prophecies", "15k gold", True, "Monk_Labyrinthine_armor"),
    ("Elite Necrotic", "Droknar's Forge", "Prophecies", "15k gold", True, "Necromancer_Elite_Necrotic_armor"),
    ("Elite Scar Pattern", "Droknar's Forge", "Prophecies", "15k gold", True, "Necromancer_Elite_Scar_Pattern_armor"),
    ("Elite Profane", "Droknar's Forge", "Prophecies", "15k gold", True, "Necromancer_Elite_Profane_armor"),
    ("Elite Enchanter", "Droknar's Forge", "Prophecies", "15k gold", True, "Mesmer_Elite_Enchanter_armor"),
    ("Elite Rogue", "Droknar's Forge", "Prophecies", "15k gold", True, "Mesmer_Elite_Rogue_armor"),
    ("Elite Stormforged", "Droknar's Forge", "Prophecies", "15k gold", True, "Elementalist_Elite_Stormforged_armor"),
    ("Elite Stoneforged", "Droknar's Forge", "Prophecies", "15k gold", True, "Elementalist_Elite_Stoneforged_armor"),
]

# ==================== FACTIONS ====================
FACTIONS_ARMOR = [
    # Faction armor
    ("Elite Kurzick", "Vasburg Armory", "Factions", "Kurzick faction", True, "Elite_Kurzick_armor"),
    ("Elite Luxon", "Leviathan Pits", "Factions", "Luxon faction", True, "Elite_Luxon_armor"),
    # Divine Path
    ("Elite Canthan", "Divine Path", "Factions", "Beat Shiro", True, "Elite_Canthan_armor"),
    ("Elite Exotic", "Divine Path", "Factions", "Beat Shiro", True, "Elite_Exotic_armor"),
    ("Elite Imperial", "Divine Path", "Factions", "Beat Shiro", True, "Elite_Imperial_armor"),
]

# ==================== NIGHTFALL ====================
NIGHTFALL_ARMOR = [
    ("Elite Sunspear", "Command Post", "Nightfall", "Prisoners of War quest", True, "Elite_Sunspear_armor"),
    ("Vabbian", "Kodash Bazaar", "Nightfall", "Gems + Gold", True, "Vabbian_armor"),
    ("Ancient", "Bone Palace", "Nightfall", "DoA materials", True, "Ancient_armor"),
    ("Primeval", "Throne of Secrets", "Nightfall", "Beat Abaddon", True, "Primeval_armor"),
]

# ==================== EYE OF THE NORTH ====================
EOTN_ARMOR = [
    # Reputation armor
    ("Asuran Armor", "Rata Sum", "Eye of the North", "Asuran Rank 5", True, "Asuran_armor"),
    ("Monument Armor", "Eye of the North", "Eye of the North", "Vanguard Rank 5", True, "Monument_armor"),
    ("Norn Armor", "Gunnar's Hold", "Eye of the North", "Norn Rank 5", True, "Norn_armor"),
    ("Deldrimor Armor", "Central Transfer Chamber", "Eye of the North", "Deldrimor Rank 5", True, "Deldrimor_armor"),
    ("Silver Eagle", "Central Transfer Chamber", "Eye of the North", "Deldrimor Rank 5", True, "Warrior_Silver_Eagle_armor"),
]

# ==================== STANDALONE PIECES ====================
STANDALONE_PIECES = [
    ("Chaos Gloves", "Central Transfer Chamber", "Eye of the North", "Deldrimor Rank 5", False, "Chaos_Gloves"),
    ("Dragon Gauntlets", "Central Transfer Chamber", "Eye of the North", "Deldrimor Rank 5", False, "Dragon_Gauntlets"),
    ("Stone Gauntlets", "Central Transfer Chamber", "Eye of the North", "Deldrimor Rank 5", False, "Stone_Gauntlets"),
    ("Bandana", "Central Transfer Chamber", "Eye of the North", "Deldrimor Rank 5", False, "Bandana"),
    ("Spectacles", "Rata Sum", "Eye of the North", "Asuran Rank 5", False, "Spectacles"),
    ("Slim Spectacles", "Rata Sum", "Eye of the North", "Asuran Rank 5", False, "Slim_Spectacles"),
    ("Tinted Spectacles", "Rata Sum", "Eye of the North", "Asuran Rank 5", False, "Tinted_Spectacles"),
    ("Norn Woad", "Gunnar's Hold", "Eye of the North", "Norn Rank 5", False, "Norn_Woad"),
    ("Highlander Woad", "Gunnar's Hold", "Eye of the North", "Norn Rank 5", False, "Highlander_Woad"),
]

# All armor combined
ALL_ARMOR = CORE_ARMOR + PROPHECIES_ARMOR + FACTIONS_ARMOR + NIGHTFALL_ARMOR + EOTN_ARMOR + STANDALONE_PIECES

# HoM eligible only
HOM_ARMOR = [a for a in ALL_ARMOR if a[4] == True]

# Campaign icons
ARMOR_ICONS = {
    "Core": "🔥",
    "Prophecies": "⚔️",
    "Factions": "🐉",
    "Nightfall": "☀️",
    "Eye of the North": "⛰️",
}
