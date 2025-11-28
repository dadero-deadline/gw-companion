#!/usr/bin/env python3
"""
Guild Wars Hall of Monuments Tracker
50 points maximum for GW2 rewards
"""

# =============================================================================
# HALL OF MONUMENTS - 50 POINTS FOR GW2 REWARDS
# =============================================================================

# MONUMENT OF DEVOTION - Minipets (8 points max)
MINIPETS = {
    "points": [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 35, 40],  # pets needed for each rank
    "max_points": 8,
    "description": "Miniatures dedicated",
    "rewards": [
        (1, "Mini pets title"),
        (3, "Miniature Rytlock"),
        (8, "Orange Tabby Cat mini"),
    ]
}

# MONUMENT OF FELLOWSHIP - Heroes with armor (8 points max)
HEROES = [
    # Core Heroes
    ("Olias", "Necromancer", "Core"),
    ("Zenmai", "Assassin", "Core"),
    ("Norgu", "Mesmer", "Core"),
    ("Goren", "Warrior", "Core"),
    ("Margrid the Sly", "Ranger", "Core"),
    ("Tahlkora", "Monk", "Core"),
    ("Master of Whispers", "Necromancer", "Core"),
    ("Acolyte Jin", "Ranger", "Core"),
    ("Acolyte Sousuke", "Elementalist", "Core"),
    ("Zhed Shadowhoof", "Elementalist", "Core"),
    ("General Morgahn", "Paragon", "Core"),
    ("Koss", "Warrior", "Nightfall"),
    ("Dunkoro", "Monk", "Nightfall"),
    ("Melonni", "Dervish", "Nightfall"),
    ("Razah", "Any", "Nightfall"),
    ("Vekk", "Asura/Elementalist", "EotN"),
    ("Ogden Stonehealer", "Monk", "EotN"),
    ("Gwen", "Mesmer", "EotN"),
    ("Jora", "Warrior", "EotN"),
    ("Pyre Fierceshot", "Ranger", "EotN"),
    ("Livia", "Necromancer", "EotN"),
    ("Hayda", "Paragon", "EotN"),
    ("Kahmu", "Dervish", "EotN"),
    ("Xandra", "Ritualist", "EotN"),
    ("Anton", "Assassin", "EotN"),
    ("M.O.X.", "Dervish", "EotN"),
    ("Keiran Thackeray", "Paragon", "Beyond"),
]

HERO_POINTS = {
    "statues_needed": [1, 2, 4, 8, 11, 15, 20],  # heroes with armor for each rank
    "max_points": 8,
    "description": "Heroes with elite armor displayed",
}

# MONUMENT OF HONOR - Titles (8 points max)
HONOR_TITLES = [
    ("Any PvE title", 1),
    ("Any max title", 2),
    ("People Know Me", 3),  # R3+ gives 3 points
    ("GWAMM", 5),
    ("Kind of a Big Deal", 1),  # Any account title
]

HONOR_POINTS = {
    "max_points": 8,
    "description": "Titles displayed",
    "rewards": [
        (1, "Heritage armor"),
        (5, "Fiery Dragon Sword"),
        (8, "Droknar's Forgehammer"),
    ]
}

# MONUMENT OF RESILIENCE - Armors (8 points max)
ARMORS = [
    ("Elite Kurzick", "Any", "Factions"),
    ("Elite Luxon", "Any", "Factions"),
    ("Elite Sunspear", "Any", "Nightfall"),
    ("Primeval", "Any", "Nightfall"),
    ("Vabbian", "Any", "Nightfall"),
    ("Ancient", "Any", "Nightfall"),
    ("Monument", "Any", "EotN"),
    ("Deldrimor", "Any", "EotN"),
    ("Norn", "Any", "EotN"),
    ("Asuran", "Any", "EotN"),
    ("Silver Eagle", "Any", "EotN"),
    ("Obsidian", "Any", "Core"),
    ("Destroyer", "Any", "EotN"),
    ("Tormented", "Any", "Nightfall"),
    ("Chaos Gloves", "Any", "Beyond"),
]

ARMOR_POINTS = {
    "statues_needed": [1, 2, 3, 5, 7],  # armors for each rank
    "max_points": 8,
    "description": "Elite armors displayed",
}

# MONUMENT OF VALOR - Weapons (8 points max)
WEAPONS = [
    ("Tormented", "Domain of Anguish", "Nightfall"),
    ("Destroyer", "EotN dungeons", "EotN"),
    ("Oppressor", "War in Kryta", "Beyond"),
]

WEAPON_POINTS = {
    "statues_needed": [1, 5, 11],  # weapons for each rank
    "max_points": 8,
    "description": "Weapons displayed",
    "rewards": [
        (1, "Fellblade"),
        (5, "Fiery Dragon Sword"),
    ]
}

# ACCOUNT-WIDE TITLES (also count for Honor)
ACCOUNT_TITLES = [
    ("Kind of a Big Deal", "Any 5 maxed titles"),
    ("I'm Very Important", "Any 10 maxed titles"),
    ("I Have Many Leather-Bound Books", "Any 15 maxed titles"),
    ("People Know Me", "Any 20 maxed titles"),
    ("I'm a Big Deal", "Any 25 maxed titles"),
    ("God Walking Amongst Mere Mortals", "Any 30 maxed titles"),
]

# =============================================================================
# GW2 REWARDS BY POINTS
# =============================================================================
GW2_REWARDS = [
    (1, "Heritage Armor"),
    (3, "Fiery Dragon Sword"),
    (5, "Ithas Longbow"),
    (8, "Legacy Pillars of Honor (Mini)"),
    (10, "Gnarled Walking Stick"),
    (15, "Orange Tabby Cat (Mini)"),
    (18, "Stygian Reaver Greatsword"),
    (20, "Tapestry Shawl"),
    (25, "Droknar's Chaingun (Focus)"),
    (30, "Rainbow Jellyfish (Mini)"),
    (35, "Tormented Shield"),
    (40, "Rhythm of the Green Woods"),
    (45, "Destroyer Knuckles"),
    (50, "Lava Spider (Mini)"),
]

# =============================================================================
# SUMMARY
# =============================================================================
print("=" * 60)
print("  HALL OF MONUMENTS CALCULATOR")
print("=" * 60)
print(f"\n  Maximum Points: 50")
print(f"\n  Monument Breakdown:")
print(f"    Devotion (Minipets):   8 points max")
print(f"    Fellowship (Heroes):   8 points max")
print(f"    Honor (Titles):        8 points max")
print(f"    Resilience (Armors):   8 points max")
print(f"    Valor (Weapons):       8 points max")
print(f"    Bonuses:              10 points max")
print(f"\n  Total Heroes Available: {len(HEROES)}")
print(f"  Total Armors Available: {len(ARMORS)}")
print(f"  GW2 Rewards: {len(GW2_REWARDS)} items")
print("=" * 60)
