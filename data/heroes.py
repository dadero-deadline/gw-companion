#!/usr/bin/env python3
"""
Guild Wars Heroes Database
All 29 recruitable heroes with their unlock quests
"""

# Format: (name, profession, campaign, region, unlock_quest, wiki_link, image_url)

HEROES = [
    # ========== NIGHTFALL - ISTAN ==========
    ("Koss", "Warrior", "Nightfall", "Istan", "Into Chahbek Village", "Koss", "https://wiki.guildwars.com/images/thumb/c/c0/Koss.jpg/150px-Koss.jpg"),
    ("Dunkoro", "Monk", "Nightfall", "Istan", "Leaving a Legacy", "Dunkoro", "https://wiki.guildwars.com/images/thumb/b/b0/Dunkoro_Sunspear_armor.jpg/150px-Dunkoro_Sunspear_armor.jpg"),
    ("Melonni", "Dervish", "Nightfall", "Istan", "Signs and Portents", "Melonni", "https://wiki.guildwars.com/images/thumb/6/67/Melonni_Sunspear_armor.jpg/128px-Melonni_Sunspear_armor.jpg"),
    ("Acolyte Jin", "Ranger", "Nightfall", "Istan", "Student Jin", "Acolyte_Jin", "https://wiki.guildwars.com/images/thumb/f/fe/Acolyte_Jin_Zaishen_armor.jpg/150px-Acolyte_Jin_Zaishen_armor.jpg"),
    ("Acolyte Sousuke", "Elementalist", "Nightfall", "Istan", "Student Sousuke", "Acolyte_Sousuke", "https://wiki.guildwars.com/images/thumb/9/98/Acolyte_Sousuke_Zaishen_armor.jpg/128px-Acolyte_Sousuke_Zaishen_armor.jpg"),
    ("Tahlkora", "Monk", "Nightfall", "Istan", "Big News, Small Package", "Tahlkora", "https://wiki.guildwars.com/images/thumb/5/5a/Tahlkora_Istani_armor.jpg/150px-Tahlkora_Istani_armor.jpg"),
    
    # ========== NIGHTFALL - KOURNA ==========
    ("Zhed Shadowhoof", "Elementalist", "Nightfall", "Kourna", "Centaur Blackmail", "Zhed_Shadowhoof", "https://wiki.guildwars.com/images/thumb/3/3c/Zhed_Shadowhoof_Veldrunner_armor.jpg/192px-Zhed_Shadowhoof_Veldrunner_armor.jpg"),
    ("Margrid the Sly", "Ranger", "Nightfall", "Kourna", "No Me, No Kormir", "Margrid_the_Sly", "https://wiki.guildwars.com/images/thumb/d/db/Margrid_the_Sly_Corsair_armor.jpg/150px-Margrid_the_Sly_Corsair_armor.jpg"),
    ("Master of Whispers", "Necromancer", "Nightfall", "Kourna", "To Kill a Demon", "Master_of_Whispers", "https://wiki.guildwars.com/images/thumb/e/ee/Master_of_Whispers_Mysterious_armor.jpg/150px-Master_of_Whispers_Mysterious_armor.jpg"),
    
    # ========== NIGHTFALL - VABBI ==========
    ("Goren", "Warrior", "Nightfall", "Vabbi", "Brains or Brawn", "Goren", "https://wiki.guildwars.com/images/thumb/4/4d/Goren_Vabbian_armor.jpg/150px-Goren_Vabbian_armor.jpg"),
    ("Norgu", "Mesmer", "Nightfall", "Vabbi", "The Role of a Lifetime", "Norgu", "https://wiki.guildwars.com/images/thumb/d/d0/Norgu_Thespian_armor.jpg/192px-Norgu_Thespian_armor.jpg"),
    ("General Morgahn", "Paragon", "Nightfall", "Vabbi", "Grand Court of Sebelkeh (mission)", "General_Morgahn", "https://wiki.guildwars.com/images/thumb/c/cf/General_Morgahn_Kournan_armor.jpg/128px-General_Morgahn_Kournan_armor.jpg"),
    
    # ========== NIGHTFALL - REALM OF TORMENT ==========
    ("Razah", "Ritualist", "Nightfall", "Realm of Torment", "Finding a Purpose", "Razah", "https://wiki.guildwars.com/images/thumb/b/b7/Razah_Mysterious_armor.jpg/150px-Razah_Mysterious_armor.jpg"),
    
    # ========== EYE OF THE NORTH - FAR SHIVERPEAKS ==========
    ("Ogden Stonehealer", "Monk", "Eye of the North", "Far Shiverpeaks", "The Beginning of the End", "Ogden_Stonehealer", "https://wiki.guildwars.com/images/thumb/e/e3/Ogden_Stonehealer.jpg/150px-Ogden_Stonehealer.jpg"),
    ("Vekk", "Elementalist", "Eye of the North", "Far Shiverpeaks", "The Beginning of the End", "Vekk", "https://wiki.guildwars.com/images/thumb/8/8f/Vekk.jpg/150px-Vekk.jpg"),
    ("Gwen", "Mesmer", "Eye of the North", "Far Shiverpeaks", "The First Vision", "Gwen", "https://wiki.guildwars.com/images/thumb/d/df/Gwen_%28Eye_of_the_North%29.jpg/200px-Gwen_%28Eye_of_the_North%29.jpg"),
    ("Xandra", "Ritualist", "Eye of the North", "Far Shiverpeaks", "Norn Fighting Tournament", "Xandra", "https://wiki.guildwars.com/images/thumb/c/c7/Xandra.jpg/150px-Xandra.jpg"),
    ("Kahmu", "Dervish", "Eye of the North", "Far Shiverpeaks", "Norn Fighting Tournament", "Kahmu", "https://wiki.guildwars.com/images/thumb/2/2c/Kahmu.jpg/150px-Kahmu.jpg"),
    ("Jora", "Warrior", "Eye of the North", "Far Shiverpeaks", "Curse of the Nornbear", "Jora", "https://wiki.guildwars.com/images/thumb/f/fd/Jora.jpg/150px-Jora.jpg"),
    
    # ========== EYE OF THE NORTH - CHARR HOMELANDS ==========
    ("Pyre Fierceshot", "Ranger", "Eye of the North", "Charr Homelands", "Warband of Brothers", "Pyre_Fierceshot", "https://wiki.guildwars.com/images/thumb/d/d1/Pyre_Fierceshot.jpg/150px-Pyre_Fierceshot.jpg"),
    ("Anton", "Assassin", "Eye of the North", "Charr Homelands", "The Assassin's Revenge", "Anton", "https://wiki.guildwars.com/images/thumb/c/c3/Anton.jpg/150px-Anton.jpg"),
    
    # ========== EYE OF THE NORTH - TARNISHED COAST ==========
    ("Hayda", "Paragon", "Eye of the North", "Tarnished Coast", "Give Peace a Chance", "Hayda", "https://wiki.guildwars.com/images/thumb/0/0c/Hayda.jpg/150px-Hayda.jpg"),
    ("Livia", "Necromancer", "Eye of the North", "Tarnished Coast", "Finding the Bloodstone", "Livia", "https://wiki.guildwars.com/images/thumb/3/36/Livia.jpg/150px-Livia.jpg"),
    
    # ========== BONUS / SPECIAL ==========
    ("M.O.X.", "Dervish", "Bonus", "Special", "M.O.X. (quest)", "M.O.X.", "https://wiki.guildwars.com/images/thumb/5/59/M.O.X.jpg/200px-M.O.X.jpg"),
    ("Olias", "Necromancer", "Nightfall", "Special", "Hunted! (Nightfall)", "Olias", "https://wiki.guildwars.com/images/thumb/d/d9/Olias_Krytan_armor.jpg/150px-Olias_Krytan_armor.jpg"),
    ("Zenmai", "Assassin", "Factions", "Special", "Befriending Zenmai", "Zenmai", "https://wiki.guildwars.com/images/thumb/8/8c/Zenmai_Am_Fah_armor.jpg/128px-Zenmai_Am_Fah_armor.jpg"),
    ("Keiran Thackeray", "Paragon", "Beyond", "Special", "Hearts of the North", "Keiran_Thackeray", "https://wiki.guildwars.com/images/thumb/6/6e/Keiran_Thackeray.jpg/196px-Keiran_Thackeray.jpg"),
    ("Miku", "Assassin", "Beyond", "Special", "Winds of Change", "Miku", "https://wiki.guildwars.com/images/thumb/4/4e/Miku.jpg/135px-Miku.jpg"),
    ("Zei Ri", "Ritualist", "Beyond", "Special", "Winds of Change", "Zei_Ri", "https://wiki.guildwars.com/images/thumb/a/a1/Initiate_Zei_Ri.jpg/140px-Initiate_Zei_Ri.jpg"),

    # ========== GUILD WARS REFORGED (Reforged Mode) ==========
    ("Devona", "Warrior", "Beyond", "Special", "The Scourge Beneath or The Hero From Ascalon", "Devona", "https://wiki.guildwars.com/images/thumb/f/f7/Devona.jpg/150px-Devona.jpg"),
    ("Ghost of Althea", "Mesmer", "Beyond", "Special", "The Dreamer and the Zealot", "Ghost_of_Althea", "https://wiki.guildwars.com/images/thumb/7/73/Ghostly_Althea.jpg/180px-Ghostly_Althea.jpg"),
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
