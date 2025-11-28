#!/usr/bin/env python3
"""
Guild Wars Heroes Database
All 29 recruitable heroes with their unlock quests
"""

# Format: (name, profession, campaign, region, unlock_quest, wiki_link)

HEROES = [
    # ========== NIGHTFALL - ISTAN ==========
    ("Koss", "Warrior", "Nightfall", "Istan", "Into Chahbek Village", "Koss"),
    ("Dunkoro", "Monk", "Nightfall", "Istan", "Leaving a Legacy", "Dunkoro"),
    ("Melonni", "Dervish", "Nightfall", "Istan", "Signs and Portents", "Melonni"),
    ("Acolyte Jin", "Ranger", "Nightfall", "Istan", "Student Jin", "Acolyte_Jin"),
    ("Acolyte Sousuke", "Elementalist", "Nightfall", "Istan", "Student Sousuke", "Acolyte_Sousuke"),
    ("Tahlkora", "Monk", "Nightfall", "Istan", "Big News, Small Package", "Tahlkora"),
    
    # ========== NIGHTFALL - KOURNA ==========
    ("Zhed Shadowhoof", "Elementalist", "Nightfall", "Kourna", "Centaur Blackmail", "Zhed_Shadowhoof"),
    ("Margrid the Sly", "Ranger", "Nightfall", "Kourna", "No Me, No Kormir", "Margrid_the_Sly"),
    ("Master of Whispers", "Necromancer", "Nightfall", "Kourna", "To Kill a Demon", "Master_of_Whispers"),
    
    # ========== NIGHTFALL - VABBI ==========
    ("Goren", "Warrior", "Nightfall", "Vabbi", "Brains or Brawn", "Goren"),
    ("Norgu", "Mesmer", "Nightfall", "Vabbi", "The Role of a Lifetime", "Norgu"),
    ("General Morgahn", "Paragon", "Nightfall", "Vabbi", "Grand Court of Sebelkeh (mission)", "General_Morgahn"),
    
    # ========== NIGHTFALL - REALM OF TORMENT ==========
    ("Razah", "Ritualist", "Nightfall", "Realm of Torment", "Finding a Purpose", "Razah"),
    
    # ========== EYE OF THE NORTH - FAR SHIVERPEAKS ==========
    ("Ogden Stonehealer", "Monk", "Eye of the North", "Far Shiverpeaks", "The Beginning of the End", "Ogden_Stonehealer"),
    ("Vekk", "Elementalist", "Eye of the North", "Far Shiverpeaks", "The Beginning of the End", "Vekk"),
    ("Gwen", "Mesmer", "Eye of the North", "Far Shiverpeaks", "The First Vision", "Gwen"),
    ("Xandra", "Ritualist", "Eye of the North", "Far Shiverpeaks", "Norn Fighting Tournament", "Xandra"),
    ("Kahmu", "Dervish", "Eye of the North", "Far Shiverpeaks", "Norn Fighting Tournament", "Kahmu"),
    ("Jora", "Warrior", "Eye of the North", "Far Shiverpeaks", "Curse of the Nornbear", "Jora"),
    
    # ========== EYE OF THE NORTH - CHARR HOMELANDS ==========
    ("Pyre Fierceshot", "Ranger", "Eye of the North", "Charr Homelands", "Warband of Brothers", "Pyre_Fierceshot"),
    ("Anton", "Assassin", "Eye of the North", "Charr Homelands", "The Assassin's Revenge", "Anton"),
    
    # ========== EYE OF THE NORTH - TARNISHED COAST ==========
    ("Hayda", "Paragon", "Eye of the North", "Tarnished Coast", "Give Peace a Chance", "Hayda"),
    ("Livia", "Necromancer", "Eye of the North", "Tarnished Coast", "Finding the Bloodstone", "Livia"),
    
    # ========== BONUS / SPECIAL ==========
    ("M.O.X.", "Dervish", "Bonus", "Special", "M.O.X. (quest)", "M.O.X."),
    ("Olias", "Necromancer", "Nightfall", "Special", "Hunted! (Nightfall)", "Olias"),
    ("Zenmai", "Assassin", "Factions", "Special", "Befriending Zenmai", "Zenmai"),
    ("Keiran Thackeray", "Paragon", "Beyond", "Special", "Hearts of the North", "Keiran_Thackeray"),
    ("Miku", "Assassin", "Beyond", "Special", "Winds of Change", "Miku"),
    ("Zei Ri", "Ritualist", "Beyond", "Special", "Winds of Change", "Zei_Ri"),
]

# Hero armor locations for HoM
HERO_ARMOR = {
    "Sunspear": {"location": "Gate of Pain", "cost": "15 Boss Bounties"},
    "Ancient": {"location": "Gate of Anguish", "cost": "15 Passages + Gems"},
    "Mysterious": {"location": "Eye of the North", "cost": "Cloth of the Brotherhood x5"},
    "Primeval": {"location": "Gate of Pain", "cost": "15 Boss Bounties"},
    "Deldrimor": {"location": "Eye of the North", "cost": "Deldrimor Steel Ingot x5"},
    "Brotherhood": {"location": "Eye of the North", "cost": "Cloth of the Brotherhood x5"},
}

# Professions with icons
HERO_PROFESSIONS = {
    "Warrior": "⚔️",
    "Ranger": "🏹",
    "Monk": "✨",
    "Necromancer": "💀",
    "Mesmer": "🔮",
    "Elementalist": "🔥",
    "Assassin": "🗡️",
    "Ritualist": "👻",
    "Paragon": "🛡️",
    "Dervish": "⚡",
}
