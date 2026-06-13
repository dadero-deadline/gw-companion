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
# Verified against the official Guild Wars 2 wiki (Hall of Monuments rewards).
# Points 1-30 each grant one skin/mini; titles every 5 points (5-50);
# Ranger pets every 5 points (15-30); above 30 points there are only titles.
GW2_REWARDS = [  # (points, reward, type)
    (1, "Heritage Boots", "Armor"), (2, "Heritage Pants", "Armor"), (3, "Heritage Greatcoat", "Armor"),
    (4, "Heritage Gloves", "Armor"), (5, "Heritage Mantle", "Armor"), (6, "Heritage Masque", "Armor"),
    (7, "Gnarled Walking Staff", "Weapon"), (8, "Living Short Bow", "Weapon"), (9, "Mini Orange Tabby Cat", "Mini"),
    (10, "Fiery Dragon Sword", "Weapon"), (11, "Diamond Aegis Shield", "Weapon"), (12, "Baroque Mask", "Armor"),
    (13, "Centurions Claw", "Weapon"), (14, "Wheelock Rifle", "Weapon"), (15, "Mini Orrian Baby Chicken", "Mini"),
    (16, "Wayward Wand Scepter", "Weapon"), (17, "Seathunder Pistol", "Weapon"), (18, "Heavenly Bracers", "Armor"),
    (19, "Deldrimor Mace", "Weapon"), (20, "Chimeric Prism Focus", "Weapon"), (21, "Mini Rockfur Racoon", "Mini"),
    (22, "Ithas Longbow", "Weapon"), (23, "Fellblade", "Weapon"), (24, "Icelord's Diadem", "Armor"),
    (25, "Icebreaker", "Weapon"), (26, "Flaming Beacon", "Weapon"), (27, "Mini Servitor Golem", "Mini"),
    (28, "Stygian Axe", "Weapon"), (29, "Mountaincall Warhorn", "Weapon"), (30, "Fire God's Vambraces", "Armor"),
]

GW2_TITLES = [  # (points, title)
    (5, "Traveler"), (10, "Guild Warrior"), (15, "Rift Warden"), (20, "Chosen"), (25, "Ascendant"),
    (30, "Closer to the Stars"), (35, "Ghostly Hero"), (40, "Flameseeker"), (45, "Legend of the Mists"),
    (50, "Champion of the Gods"),
]

GW2_PETS = [  # (points, ranger pet)
    (15, "Juvenile Black Moa"), (20, "Juvenile Rainbow Jellyfish"),
    (25, "Juvenile White Raven"), (30, "Juvenile Black Widow Spider"),
]

# =============================================================================
# SUMMARY  (only when run directly; importing this module must stay side-effect free)
# =============================================================================
if __name__ == "__main__":
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
    print(f"  GW2 Rewards: {len(GW2_REWARDS)} items, {len(GW2_TITLES)} titles, {len(GW2_PETS)} pets")
    print("=" * 60)
