#!/usr/bin/env python3
"""
Guild Wars Daily/Repeatable Quests Database
Zaishen Quests rotate on fixed cycles
"""

from datetime import datetime, timedelta

# ==================== ZAISHEN MISSION ====================
# 69-day cycle, started March 3, 2011
ZAISHEN_MISSION_START = datetime(2011, 3, 4)  # Day after update
ZAISHEN_MISSIONS = [
    ("Augury Rock", "Prophecies", "Crystal Desert", "Augury_Rock_(Zaishen_quest)"),
    ("Grand Court of Sebelkeh", "Nightfall", "Vabbi", "Grand_Court_of_Sebelkeh_(Zaishen_quest)"),
    ("Ice Caves of Sorrow", "Prophecies", "Southern Shiverpeaks", "Ice_Caves_of_Sorrow_(Zaishen_quest)"),
    ("Raisu Palace", "Factions", "Kaineng City", "Raisu_Palace_(Zaishen_quest)"),
    ("Gate of Desolation", "Nightfall", "Desolation", "Gate_of_Desolation_(Zaishen_quest)"),
    ("Thirsty River", "Prophecies", "Crystal Desert", "Thirsty_River_(Zaishen_quest)"),
    ("Blacktide Den", "Nightfall", "Istan", "Blacktide_Den_(Zaishen_quest)"),
    ("Against the Charr", "Eye of the North", "Charr Homelands", "Against_the_Charr_(Zaishen_quest)"),
    ("Abaddon's Mouth", "Prophecies", "Ring of Fire", "Abaddon%27s_Mouth_(Zaishen_quest)"),
    ("Nundu Bay", "Nightfall", "Kourna", "Nundu_Bay_(Zaishen_quest)"),
    ("Divinity Coast", "Prophecies", "Kryta", "Divinity_Coast_(Zaishen_quest)"),
    ("Zen Daijun", "Factions", "Shing Jea", "Zen_Daijun_(Zaishen_quest)"),
    ("Pogahn Passage", "Nightfall", "Kourna", "Pogahn_Passage_(Zaishen_quest)"),
    ("Tahnnakai Temple", "Factions", "Kaineng City", "Tahnnakai_Temple_(Zaishen_quest)"),
    ("The Great Northern Wall", "Prophecies", "Ascalon", "The_Great_Northern_Wall_(Zaishen_quest)"),
    ("Dasha Vestibule", "Nightfall", "Vabbi", "Dasha_Vestibule_(Zaishen_quest)"),
    ("The Wilds", "Prophecies", "Maguuma", "The_Wilds_(Zaishen_quest)"),
    ("Unwaking Waters", "Factions", "Jade Sea", "Unwaking_Waters_(Zaishen_quest)"),
    ("Chahbek Village", "Nightfall", "Istan", "Chahbek_Village_(Zaishen_quest)"),
    ("Aurora Glade", "Prophecies", "Maguuma", "Aurora_Glade_(Zaishen_quest)"),
    ("A Time for Heroes", "Eye of the North", "Depths", "A_Time_for_Heroes_(Zaishen_quest)"),
    ("Consulate Docks", "Nightfall", "Istan", "Consulate_Docks_(Zaishen_quest)"),
    ("Ring of Fire", "Prophecies", "Ring of Fire", "Ring_of_Fire_(Zaishen_quest)"),
    ("Nahpui Quarter", "Factions", "Kaineng City", "Nahpui_Quarter_(Zaishen_quest)"),
    ("The Dragon's Lair", "Prophecies", "Crystal Desert", "The_Dragon%27s_Lair_(Zaishen_quest)"),
    ("Dzagonur Bastion", "Nightfall", "Vabbi", "Dzagonur_Bastion_(Zaishen_quest)"),
    ("D'Alessio Seaboard", "Prophecies", "Kryta", "D%27Alessio_Seaboard_(Zaishen_quest)"),
    ("Assault on the Stronghold", "Eye of the North", "Charr Homelands", "Assault_on_the_Stronghold_(Zaishen_quest)"),
    ("The Eternal Grove", "Factions", "Echovald", "The_Eternal_Grove_(Zaishen_quest)"),
    ("Sanctum Cay", "Prophecies", "Kryta", "Sanctum_Cay_(Zaishen_quest)"),
    ("Rilohn Refuge", "Nightfall", "Kourna", "Rilohn_Refuge_(Zaishen_quest)"),
    ("Warband of Brothers", "Eye of the North", "Charr Homelands", "Warband_of_Brothers_(Zaishen_quest)"),
    ("Borlis Pass", "Prophecies", "Northern Shiverpeaks", "Borlis_Pass_(Zaishen_quest)"),
    ("Imperial Sanctum", "Factions", "Kaineng City", "Imperial_Sanctum_(Zaishen_quest)"),
    ("Moddok Crevice", "Nightfall", "Vabbi", "Moddok_Crevice_(Zaishen_quest)"),
    ("Nolani Academy", "Prophecies", "Ascalon", "Nolani_Academy_(Zaishen_quest)"),
    ("Destruction's Depths", "Eye of the North", "Depths", "Destruction%27s_Depths_(Zaishen_quest)"),
    ("Venta Cemetery", "Nightfall", "Kourna", "Venta_Cemetery_(Zaishen_quest)"),
    ("Fort Ranik", "Prophecies", "Ascalon", "Fort_Ranik_(Zaishen_quest)"),
    ("A Gate Too Far", "Eye of the North", "Depths", "A_Gate_Too_Far_(Zaishen_quest)"),
    ("Minister Cho's Estate", "Factions", "Shing Jea", "Minister_Cho%27s_Estate_(Zaishen_quest)"),
    ("Thunderhead Keep", "Prophecies", "Southern Shiverpeaks", "Thunderhead_Keep_(Zaishen_quest)"),
    ("Tihark Orchard", "Nightfall", "Vabbi", "Tihark_Orchard_(Zaishen_quest)"),
    ("Finding the Bloodstone", "Eye of the North", "Tarnished Coast", "Finding_the_Bloodstone_(Zaishen_quest)"),
    ("Dunes of Despair", "Prophecies", "Crystal Desert", "Dunes_of_Despair_(Zaishen_quest)"),
    ("Vizunah Square", "Factions", "Kaineng City", "Vizunah_Square_(Zaishen_quest)"),
    ("Jokanur Diggings", "Nightfall", "Istan", "Jokanur_Diggings_(Zaishen_quest)"),
    ("Iron Mines of Moladune", "Prophecies", "Southern Shiverpeaks", "Iron_Mines_of_Moladune_(Zaishen_quest)"),
    ("Kodonur Crossroads", "Nightfall", "Kourna", "Kodonur_Crossroads_(Zaishen_quest)"),
    ("G.O.L.E.M.", "Eye of the North", "Tarnished Coast", "G.O.L.E.M._(Zaishen_quest)"),
    ("Arborstone", "Factions", "Echovald", "Arborstone_(Zaishen_quest)"),
    ("Gates of Kryta", "Prophecies", "Kryta", "Gates_of_Kryta_(Zaishen_quest)"),
    ("Gate of Madness", "Nightfall", "Realm of Torment", "Gate_of_Madness_(Zaishen_quest)"),
    ("The Elusive Golemancer", "Eye of the North", "Tarnished Coast", "The_Elusive_Golemancer_(Zaishen_quest)"),
    ("Riverside Province", "Prophecies", "Kryta", "Riverside_Province_(Zaishen_quest)"),
    ("Boreas Seabed", "Factions", "Jade Sea", "Boreas_Seabed_(Zaishen_quest)"),
    ("Ruins of Morah", "Nightfall", "Desolation", "Ruins_of_Morah_(Zaishen_quest)"),
    ("Hell's Precipice", "Prophecies", "Ring of Fire", "Hell%27s_Precipice_(Zaishen_quest)"),
    ("Ruins of Surmia", "Prophecies", "Ascalon", "Ruins_of_Surmia_(Zaishen_quest)"),
    ("Curse of the Nornbear", "Eye of the North", "Far Shiverpeaks", "Curse_of_the_Nornbear_(Zaishen_quest)"),
    ("Sunjiang District", "Factions", "Kaineng City", "Sunjiang_District_(Zaishen_quest)"),
    ("Elona Reach", "Prophecies", "Crystal Desert", "Elona_Reach_(Zaishen_quest)"),
    ("Gate of Pain", "Nightfall", "Realm of Torment", "Gate_of_Pain_(Zaishen_quest)"),
    ("Blood Washes Blood", "Eye of the North", "Charr Homelands", "Blood_Washes_Blood_(Zaishen_quest)"),
    ("Bloodstone Fen", "Prophecies", "Maguuma", "Bloodstone_Fen_(Zaishen_quest)"),
    ("Jennur's Horde", "Nightfall", "Desolation", "Jennur%27s_Horde_(Zaishen_quest)"),
    ("Gyala Hatchery", "Factions", "Jade Sea", "Gyala_Hatchery_(Zaishen_quest)"),
    ("Abaddon's Gate", "Nightfall", "Realm of Torment", "Abaddon%27s_Gate_(Zaishen_quest)"),
    ("The Frost Gate", "Prophecies", "Northern Shiverpeaks", "The_Frost_Gate_(Zaishen_quest)"),
]

# ==================== ZAISHEN BOUNTY ====================
# 66-day cycle
ZAISHEN_BOUNTY_START = datetime(2009, 6, 12)  # After June 11 2009 update
ZAISHEN_BOUNTIES = [
    ("Droajam, Mage of the Sands", "Nightfall", "Desolation", "Droajam,_Mage_of_the_Sands_(Zaishen_quest)"),
    ("Royen Beastkeeper", "Prophecies", "Maguuma", "Royen_Beastkeeper_(Zaishen_quest)"),
    ("Eldritch Ettin", "Prophecies", "Southern Shiverpeaks", "Eldritch_Ettin_(Zaishen_quest)"),
    ("Vengeful Aatxe", "Core", "Underworld", "Vengeful_Aatxe_(Zaishen_quest)"),
    ("Fronis Irontoe", "Eye of the North", "Depths", "Fronis_Irontoe_(Zaishen_quest)"),
    ("Urgoz", "Factions", "Echovald", "Urgoz_(Zaishen_quest)"),
    ("Fenrir", "Eye of the North", "Far Shiverpeaks", "Fenrir_(Zaishen_quest)"),
    ("Selvetarm", "Eye of the North", "Depths", "Selvetarm_(Zaishen_quest)"),
    ("Mohby Windbeak", "Nightfall", "Istan", "Mohby_Windbeak_(Zaishen_quest)"),
    ("Charged Blackness", "Prophecies", "Ring of Fire", "Charged_Blackness_(Zaishen_quest)"),
    ("Rotscale", "Prophecies", "Kryta", "Rotscale_(Zaishen_quest)"),
    ("Zoldark the Unholy", "Eye of the North", "Depths", "Zoldark_the_Unholy_(Zaishen_quest)"),
    ("Korshek the Immolated", "Nightfall", "Desolation", "Korshek_the_Immolated_(Zaishen_quest)"),
    ("Myish, Lady of the Lake", "Eye of the North", "Far Shiverpeaks", "Myish,_Lady_of_the_Lake_(Zaishen_quest)"),
    ("Frostmaw the Kinslayer", "Eye of the North", "Far Shiverpeaks", "Frostmaw_the_Kinslayer_(Zaishen_quest)"),
    ("Kunvie Firewing", "Factions", "Echovald", "Kunvie_Firewing_(Zaishen_quest)"),
    ("Z'him Monns", "Nightfall", "Desolation", "Z%27him_Monns_(Zaishen_quest)"),
    ("The Greater Darkness", "Eye of the North", "Depths", "The_Greater_Darkness_(Zaishen_quest)"),
    ("TPS Regulator Golem", "Eye of the North", "Depths", "TPS_Regulator_Golem_(Zaishen_quest)"),
    ("Plague of Destruction", "Eye of the North", "Tarnished Coast", "Plague_of_Destruction_(Zaishen_quest)"),
    ("The Darknesses", "Eye of the North", "Depths", "The_Darknesses_(Zaishen_quest)"),
    ("Admiral Kantoh", "Factions", "Jade Sea", "Admiral_Kantoh_(Zaishen_quest)"),
    ("Borrguus Blisterbark", "Eye of the North", "Tarnished Coast", "Borrguus_Blisterbark_(Zaishen_quest)"),
    ("Forgewight", "Eye of the North", "Depths", "Forgewight_(Zaishen_quest)"),
    ("Baubao Wavewrath", "Factions", "Jade Sea", "Baubao_Wavewrath_(Zaishen_quest)"),
    ("Joffs the Mitigator", "Nightfall", "Kourna", "Joffs_the_Mitigator_(Zaishen_quest)"),
    ("Rragar Maneater", "Eye of the North", "Charr Homelands", "Rragar_Maneater_(Zaishen_quest)"),
    ("Chung, the Attuned", "Factions", "Kaineng City", "Chung,_the_Attuned_(Zaishen_quest)"),
    ("Lord Jadoth", "Core", "Domain of Anguish", "Lord_Jadoth_(Zaishen_quest)"),
    ("Nulfastu, Earthbound", "Eye of the North", "Far Shiverpeaks", "Nulfastu,_Earthbound_(Zaishen_quest)"),
    ("The Iron Forgeman", "Eye of the North", "Depths", "The_Iron_Forgeman_(Zaishen_quest)"),
    ("Magmus", "Eye of the North", "Depths", "Magmus_(Zaishen_quest)"),
    ("Mobrin, Lord of the Marsh", "Factions", "Echovald", "Mobrin,_Lord_of_the_Marsh_(Zaishen_quest)"),
    ("Jarimiya the Unmerciful", "Nightfall", "Desolation", "Jarimiya_the_Unmerciful_(Zaishen_quest)"),
    ("Duncan the Black", "Eye of the North", "Depths", "Duncan_the_Black_(Zaishen_quest)"),
    ("Quansong Spiritspeak", "Factions", "Echovald", "Quansong_Spiritspeak_(Zaishen_quest)"),
    ("The Stygian Underlords", "Core", "Domain of Anguish", "The_Stygian_Underlords_(Zaishen_quest)"),
    ("Fozzy Yeoryios", "Nightfall", "Vabbi", "Fozzy_Yeoryios_(Zaishen_quest)"),
    ("The Black Beast of Arrgh", "Eye of the North", "Depths", "The_Black_Beast_of_Arrgh_(Zaishen_quest)"),
    ("Arachni", "Eye of the North", "Tarnished Coast", "Arachni_(Zaishen_quest)"),
    ("The Four Horsemen", "Core", "Underworld", "The_Four_Horsemen_(Zaishen_quest)"),
    ("Remnant of Antiquities", "Eye of the North", "Depths", "Remnant_of_Antiquities_(Zaishen_quest)"),
    ("Arbor Earthcall", "Factions", "Jade Sea", "Arbor_Earthcall_(Zaishen_quest)"),
    ("Prismatic Ooze", "Eye of the North", "Tarnished Coast", "Prismatic_Ooze_(Zaishen_quest)"),
    ("Lord Khobay", "Nightfall", "Desolation", "Lord_Khobay_(Zaishen_quest)"),
    ("Jedeh the Mighty", "Nightfall", "Desolation", "Jedeh_the_Mighty_(Zaishen_quest)"),
    ("Ssuns, Blessed of Dwayna", "Nightfall", "Realm of Torment", "Ssuns,_Blessed_of_Dwayna_(Zaishen_quest)"),
    ("Justiciar Thommis", "Prophecies", "Kryta", "Justiciar_Thommis_(Zaishen_quest)"),
    ("Harn and Maxine Coldstone", "Prophecies", "Southern Shiverpeaks", "Harn_and_Maxine_Coldstone_(Zaishen_quest)"),
    ("Pywatt the Swift", "Nightfall", "Kourna", "Pywatt_the_Swift_(Zaishen_quest)"),
    ("Fendi Nin", "Eye of the North", "Depths", "Fendi_Nin_(Zaishen_quest)"),
    ("Mungri Magicbox", "Nightfall", "Istan", "Mungri_Magicbox_(Zaishen_quest)"),
    ("Priest of Menzies", "Core", "Fissure of Woe", "Priest_of_Menzies_(Zaishen_quest)"),
    ("Ilsundur, Lord of Fire", "Eye of the North", "Depths", "Ilsundur,_Lord_of_Fire_(Zaishen_quest)"),
    ("Kepkhet Marrowfeast", "Nightfall", "Desolation", "Kepkhet_Marrowfeast_(Zaishen_quest)"),
    ("Commander Wahli", "Factions", "Jade Sea", "Commander_Wahli_(Zaishen_quest)"),
    ("Kanaxai", "Factions", "Jade Sea", "Kanaxai_(Zaishen_quest)"),
    ("Khabuus", "Nightfall", "Vabbi", "Khabuus_(Zaishen_quest)"),
    ("Molotov Rocktail", "Eye of the North", "Charr Homelands", "Molotov_Rocktail_(Zaishen_quest)"),
    ("The Stygian Lords", "Core", "Domain of Anguish", "The_Stygian_Lords_(Zaishen_quest)"),
    ("Dragon Lich", "Prophecies", "Ring of Fire", "Dragon_Lich_(Zaishen_quest)"),
    ("Havok Soulwail", "Eye of the North", "Depths", "Havok_Soulwail_(Zaishen_quest)"),
    ("Ghial the Bone Dancer", "Nightfall", "Desolation", "Ghial_the_Bone_Dancer_(Zaishen_quest)"),
    ("Murakai, Lady of the Night", "Eye of the North", "Depths", "Murakai,_Lady_of_the_Night_(Zaishen_quest)"),
    ("Rand Stormweaver", "Prophecies", "Northern Shiverpeaks", "Rand_Stormweaver_(Zaishen_quest)"),
    ("Verata", "Prophecies", "Kryta", "Verata_(Zaishen_quest)"),
]

# ==================== ZAISHEN VANQUISH ====================
# 136-day cycle - Nov 28 2025 = Traveler's Vale (index 79)
# So start = Nov 28 2025 - 79 days = Sept 10 2025
ZAISHEN_VANQUISH_START = datetime(2025, 9, 10)  # Calibrated
ZAISHEN_VANQUISHES = [
    ("Jaya Bluffs", "Factions", "Shing Jea", "Jaya_Bluffs_(Zaishen_vanquish)"),
    ("Holdings of Chokhin", "Nightfall", "Vabbi", "Holdings_of_Chokhin_(Zaishen_vanquish)"),
    ("Ice Cliff Chasms", "Eye of the North", "Far Shiverpeaks", "Ice_Cliff_Chasms_(Zaishen_vanquish)"),
    ("Griffon's Mouth", "Prophecies", "Shiverpeaks", "Griffon%27s_Mouth_(Zaishen_vanquish)"),
    ("Kinya Province", "Factions", "Shing Jea", "Kinya_Province_(Zaishen_vanquish)"),
    ("Issnur Isles", "Nightfall", "Istan", "Issnur_Isles_(Zaishen_vanquish)"),
    ("Jaga Moraine", "Eye of the North", "Far Shiverpeaks", "Jaga_Moraine_(Zaishen_vanquish)"),
    ("Ice Floe", "Eye of the North", "Far Shiverpeaks", "Ice_Floe_(Zaishen_vanquish)"),
    ("Maishang Hills", "Factions", "Jade Sea", "Maishang_Hills_(Zaishen_vanquish)"),
    ("Jahai Bluffs", "Nightfall", "Kourna", "Jahai_Bluffs_(Zaishen_vanquish)"),
    ("Riven Earth", "Eye of the North", "Charr Homelands", "Riven_Earth_(Zaishen_vanquish)"),
    ("Icedome", "Eye of the North", "Far Shiverpeaks", "Icedome_(Zaishen_vanquish)"),
    ("Minister Cho's Estate", "Factions", "Shing Jea", "Minister_Cho%27s_Estate_(Zaishen_vanquish)"),
    ("Mehtani Keys", "Nightfall", "Istan", "Mehtani_Keys_(Zaishen_vanquish)"),
    ("Sacnoth Valley", "Eye of the North", "Charr Homelands", "Sacnoth_Valley_(Zaishen_vanquish)"),
    ("Iron Horse Mine", "Prophecies", "Shiverpeaks", "Iron_Horse_Mine_(Zaishen_vanquish)"),
    ("Morostav Trail", "Factions", "Echovald", "Morostav_Trail_(Zaishen_vanquish)"),
    ("Plains of Jarin", "Nightfall", "Istan", "Plains_of_Jarin_(Zaishen_vanquish)"),
    ("Sparkfly Swamp", "Eye of the North", "Tarnished Coast", "Sparkfly_Swamp_(Zaishen_vanquish)"),
    ("Kessex Peak", "Prophecies", "Kryta", "Kessex_Peak_(Zaishen_vanquish)"),
    ("Mourning Veil Falls", "Factions", "Echovald", "Mourning_Veil_Falls_(Zaishen_vanquish)"),
    ("The Alkali Pan", "Nightfall", "Desolation", "The_Alkali_Pan_(Zaishen_vanquish)"),
    ("Varajar Fells", "Eye of the North", "Far Shiverpeaks", "Varajar_Fells_(Zaishen_vanquish)"),
    ("Lornar's Pass", "Prophecies", "Shiverpeaks", "Lornar%27s_Pass_(Zaishen_vanquish)"),
    ("Pongmei Valley", "Factions", "Kaineng", "Pongmei_Valley_(Zaishen_vanquish)"),
    ("The Floodplain of Mahnkelon", "Nightfall", "Kourna", "The_Floodplain_of_Mahnkelon_(Zaishen_vanquish)"),
    ("Verdant Cascades", "Eye of the North", "Tarnished Coast", "Verdant_Cascades_(Zaishen_vanquish)"),
    ("Majesty's Rest", "Prophecies", "Maguuma", "Majesty%27s_Rest_(Zaishen_vanquish)"),
    ("Raisu Palace", "Factions", "Kaineng", "Raisu_Palace_(Zaishen_vanquish)"),
    ("The Hidden City of Ahdashim", "Nightfall", "Vabbi", "The_Hidden_City_of_Ahdashim_(Zaishen_vanquish)"),
    ("Rhea's Crater", "Eye of the North", "Charr Homelands", "Rhea%27s_Crater_(Zaishen_vanquish)"),
    ("Mamnoon Lagoon", "Prophecies", "Maguuma", "Mamnoon_Lagoon_(Zaishen_vanquish)"),
    ("Shadow's Passage", "Factions", "Echovald", "Shadow%27s_Passage_(Zaishen_vanquish)"),
    ("The Mirror of Lyss", "Nightfall", "Vabbi", "The_Mirror_of_Lyss_(Zaishen_vanquish)"),
    ("Saoshang Trail", "Factions", "Shing Jea", "Saoshang_Trail_(Zaishen_vanquish)"),
    ("Nebo Terrace", "Prophecies", "Kryta", "Nebo_Terrace_(Zaishen_vanquish)"),
    ("Shenzun Tunnels", "Factions", "Kaineng", "Shenzun_Tunnels_(Zaishen_vanquish)"),
    ("The Ruptured Heart", "Nightfall", "Desolation", "The_Ruptured_Heart_(Zaishen_vanquish)"),
    ("Salt Flats", "Prophecies", "Crystal Desert", "Salt_Flats_(Zaishen_vanquish)"),
    ("North Kryta Province", "Prophecies", "Kryta", "North_Kryta_Province_(Zaishen_vanquish)"),
    ("Silent Surf", "Factions", "Jade Sea", "Silent_Surf_(Zaishen_vanquish)"),
    ("The Shattered Ravines", "Nightfall", "Desolation", "The_Shattered_Ravines_(Zaishen_vanquish)"),
    ("Scoundrel's Rise", "Prophecies", "Kryta", "Scoundrel%27s_Rise_(Zaishen_vanquish)"),
    ("Old Ascalon", "Prophecies", "Ascalon", "Old_Ascalon_(Zaishen_vanquish)"),
    ("Sunjiang District", "Factions", "Kaineng", "Sunjiang_District_(Zaishen_vanquish)"),
    ("The Sulfurous Wastes", "Nightfall", "Desolation", "The_Sulfurous_Wastes_(Zaishen_vanquish)"),
    ("Magus Stones", "Eye of the North", "Tarnished Coast", "Magus_Stones_(Zaishen_vanquish)"),
    ("Perdition Rock", "Prophecies", "Ring of Fire", "Perdition_Rock_(Zaishen_vanquish)"),
    ("Sunqua Vale", "Factions", "Shing Jea", "Sunqua_Vale_(Zaishen_vanquish)"),
    ("Turai's Procession", "Nightfall", "Desolation", "Turai%27s_Procession_(Zaishen_vanquish)"),
    ("Norrhart Domains", "Eye of the North", "Far Shiverpeaks", "Norrhart_Domains_(Zaishen_vanquish)"),
    ("Pockmark Flats", "Prophecies", "Ascalon", "Pockmark_Flats_(Zaishen_vanquish)"),
    ("Tahnnakai Temple", "Factions", "Kaineng", "Tahnnakai_Temple_(Zaishen_vanquish)"),
    ("Vehjin Mines", "Nightfall", "Vabbi", "Vehjin_Mines_(Zaishen_vanquish)"),
    ("Poisoned Outcrops", "Eye of the North", "Charr Homelands", "Poisoned_Outcrops_(Zaishen_vanquish)"),
    ("Prophet's Path", "Prophecies", "Crystal Desert", "Prophet%27s_Path_(Zaishen_vanquish)"),
    ("The Eternal Grove", "Factions", "Echovald", "The_Eternal_Grove_(Zaishen_vanquish)"),
    ("Tasca's Demise", "Prophecies", "Shiverpeaks", "Tasca%27s_Demise_(Zaishen_vanquish)"),
    ("Resplendent Makuun", "Nightfall", "Vabbi", "Resplendent_Makuun_(Zaishen_vanquish)"),
    ("Reed Bog", "Prophecies", "Maguuma", "Reed_Bog_(Zaishen_vanquish)"),
    ("Unwaking Waters", "Factions", "Jade Sea", "Unwaking_Waters_(Zaishen_vanquish)"),
    ("Stingray Strand", "Nightfall", "Istan", "Stingray_Strand_(Zaishen_vanquish)"),
    ("Sunward Marches", "Nightfall", "Kourna", "Sunward_Marches_(Zaishen_vanquish)"),
    ("Regent Valley", "Prophecies", "Ascalon", "Regent_Valley_(Zaishen_vanquish)"),
    ("Wajjun Bazaar", "Factions", "Kaineng", "Wajjun_Bazaar_(Zaishen_vanquish)"),
    ("Yatendi Canyons", "Nightfall", "Kourna", "Yatendi_Canyons_(Zaishen_vanquish)"),
    ("Twin Serpent Lakes", "Prophecies", "Maguuma", "Twin_Serpent_Lakes_(Zaishen_vanquish)"),
    ("Sage Lands", "Prophecies", "Maguuma", "Sage_Lands_(Zaishen_vanquish)"),
    ("Xaquang Skyway", "Factions", "Kaineng", "Xaquang_Skyway_(Zaishen_vanquish)"),
    ("Zehlon Reach", "Nightfall", "Istan", "Zehlon_Reach_(Zaishen_vanquish)"),
    ("Tangle Root", "Prophecies", "Maguuma", "Tangle_Root_(Zaishen_vanquish)"),
    ("Silverwood", "Prophecies", "Maguuma", "Silverwood_(Zaishen_vanquish)"),
    ("Zen Daijun", "Factions", "Shing Jea", "Zen_Daijun_(Zaishen_vanquish)"),
    ("The Arid Sea", "Prophecies", "Crystal Desert", "The_Arid_Sea_(Zaishen_vanquish)"),
    ("Nahpui Quarter", "Factions", "Kaineng", "Nahpui_Quarter_(Zaishen_vanquish)"),
    ("Skyward Reach", "Prophecies", "Crystal Desert", "Skyward_Reach_(Zaishen_vanquish)"),
    ("The Scar", "Prophecies", "Crystal Desert", "The_Scar_(Zaishen_vanquish)"),
    ("The Black Curtain", "Prophecies", "Kryta", "The_Black_Curtain_(Zaishen_vanquish)"),
    ("Panjiang Peninsula", "Factions", "Shing Jea", "Panjiang_Peninsula_(Zaishen_vanquish)"),
    ("Snake Dance", "Prophecies", "Shiverpeaks", "Snake_Dance_(Zaishen_vanquish)"),
    ("Traveler's Vale", "Prophecies", "Shiverpeaks", "Traveler%27s_Vale_(Zaishen_vanquish)"),
    ("The Breach", "Prophecies", "Ascalon", "The_Breach_(Zaishen_vanquish)"),
    ("Lahtenda Bog", "Nightfall", "Istan", "Lahtenda_Bog_(Zaishen_vanquish)"),
    ("Spearhead Peak", "Prophecies", "Shiverpeaks", "Spearhead_Peak_(Zaishen_vanquish)"),
    ("Mount Qinkai", "Factions", "Jade Sea", "Mount_Qinkai_(Zaishen_vanquish)"),
    ("Marga Coast", "Nightfall", "Kourna", "Marga_Coast_(Zaishen_vanquish)"),
    ("Melandru's Hope", "Prophecies", "Maguuma", "Melandru%27s_Hope_(Zaishen_vanquish)"),
    ("The Falls", "Prophecies", "Maguuma", "The_Falls_(Zaishen_vanquish)"),
    ("Joko's Domain", "Nightfall", "Desolation", "Joko%27s_Domain_(Zaishen_vanquish)"),
    ("Vulture Drifts", "Prophecies", "Crystal Desert", "Vulture_Drifts_(Zaishen_vanquish)"),
    ("Wilderness of Bahdza", "Nightfall", "Vabbi", "Wilderness_of_Bahdza_(Zaishen_vanquish)"),
    ("Talmark Wilderness", "Prophecies", "Kryta", "Talmark_Wilderness_(Zaishen_vanquish)"),
    ("Vehtendi Valley", "Nightfall", "Vabbi", "Vehtendi_Valley_(Zaishen_vanquish)"),
    ("Talus Chute", "Prophecies", "Shiverpeaks", "Talus_Chute_(Zaishen_vanquish)"),
    ("Mineral Springs", "Prophecies", "Shiverpeaks", "Mineral_Springs_(Zaishen_vanquish)"),
    ("Anvil Rock", "Prophecies", "Shiverpeaks", "Anvil_Rock_(Zaishen_vanquish)"),
    ("Arborstone", "Factions", "Echovald", "Arborstone_(Zaishen_vanquish)"),
    ("Witman's Folly", "Prophecies", "Ascalon", "Witman%27s_Folly_(Zaishen_vanquish)"),
    ("Arkjok Ward", "Nightfall", "Kourna", "Arkjok_Ward_(Zaishen_vanquish)"),
    ("Ascalon Foothills", "Prophecies", "Ascalon", "Ascalon_Foothills_(Zaishen_vanquish)"),
    ("Bahdok Caverns", "Nightfall", "Kourna", "Bahdok_Caverns_(Zaishen_vanquish)"),
    ("Cursed Lands", "Prophecies", "Kryta", "Cursed_Lands_(Zaishen_vanquish)"),
    ("Alcazia Tangle", "Eye of the North", "Tarnished Coast", "Alcazia_Tangle_(Zaishen_vanquish)"),
    ("Archipelagos", "Prophecies", "Maguuma", "Archipelagos_(Zaishen_vanquish)"),
    ("Eastern Frontier", "Prophecies", "Ascalon", "Eastern_Frontier_(Zaishen_vanquish)"),
    ("Dejarin Estate", "Nightfall", "Istan", "Dejarin_Estate_(Zaishen_vanquish)"),
    ("Watchtower Coast", "Prophecies", "Kryta", "Watchtower_Coast_(Zaishen_vanquish)"),
    ("Arbor Bay", "Eye of the North", "Tarnished Coast", "Arbor_Bay_(Zaishen_vanquish)"),
    ("Barbarous Shore", "Nightfall", "Kourna", "Barbarous_Shore_(Zaishen_vanquish)"),
    ("Deldrimor Bowl", "Prophecies", "Shiverpeaks", "Deldrimor_Bowl_(Zaishen_vanquish)"),
    ("Boreas Seabed", "Factions", "Jade Sea", "Boreas_Seabed_(Zaishen_vanquish)"),
    ("Cliffs of Dohjok", "Nightfall", "Istan", "Cliffs_of_Dohjok_(Zaishen_vanquish)"),
    ("Diessa Lowlands", "Prophecies", "Ascalon", "Diessa_Lowlands_(Zaishen_vanquish)"),
    ("Bukdek Byway", "Factions", "Kaineng", "Bukdek_Byway_(Zaishen_vanquish)"),
    ("Bjora Marches", "Eye of the North", "Far Shiverpeaks", "Bjora_Marches_(Zaishen_vanquish)"),
    ("Crystal Overlook", "Nightfall", "Desolation", "Crystal_Overlook_(Zaishen_vanquish)"),
    ("Diviner's Ascent", "Prophecies", "Crystal Desert", "Diviner%27s_Ascent_(Zaishen_vanquish)"),
    ("Dalada Uplands", "Eye of the North", "Charr Homelands", "Dalada_Uplands_(Zaishen_vanquish)"),
    ("Drazach Thicket", "Factions", "Echovald", "Drazach_Thicket_(Zaishen_vanquish)"),
    ("Fahranur, the First City", "Nightfall", "Istan", "Fahranur,_the_First_City_(Zaishen_vanquish)"),
    ("Dragon's Gullet", "Prophecies", "Ascalon", "Dragon%27s_Gullet_(Zaishen_vanquish)"),
    ("Ferndale", "Factions", "Echovald", "Ferndale_(Zaishen_vanquish)"),
    ("Forum Highlands", "Nightfall", "Vabbi", "Forum_Highlands_(Zaishen_vanquish)"),
    ("Dreadnought's Drift", "Prophecies", "Shiverpeaks", "Dreadnought%27s_Drift_(Zaishen_vanquish)"),
    ("Drakkar Lake", "Eye of the North", "Far Shiverpeaks", "Drakkar_Lake_(Zaishen_vanquish)"),
    ("Dry Top", "Prophecies", "Maguuma", "Dry_Top_(Zaishen_vanquish)"),
    ("Tears of the Fallen", "Eye of the North", "Depths", "Tears_of_the_Fallen_(Zaishen_vanquish)"),
    ("Gyala Hatchery", "Factions", "Jade Sea", "Gyala_Hatchery_(Zaishen_vanquish)"),
    ("Ettin's Back", "Prophecies", "Shiverpeaks", "Ettin%27s_Back_(Zaishen_vanquish)"),
    ("Gandara, the Moon Fortress", "Nightfall", "Kourna", "Gandara,_the_Moon_Fortress_(Zaishen_vanquish)"),
    ("Grothmar Wardowns", "Eye of the North", "Charr Homelands", "Grothmar_Wardowns_(Zaishen_vanquish)"),
    ("Flame Temple Corridor", "Prophecies", "Ascalon", "Flame_Temple_Corridor_(Zaishen_vanquish)"),
    ("Haiju Lagoon", "Factions", "Shing Jea", "Haiju_Lagoon_(Zaishen_vanquish)"),
    ("Frozen Forest", "Prophecies", "Shiverpeaks", "Frozen_Forest_(Zaishen_vanquish)"),
    ("Garden of Seborhin", "Nightfall", "Vabbi", "Garden_of_Seborhin_(Zaishen_vanquish)"),
    ("Grenth's Footprint", "Prophecies", "Shiverpeaks", "Grenth%27s_Footprint_(Zaishen_vanquish)"),
]

# ==================== ZAISHEN COMBAT (PvP) ====================
# 7-day cycle - Nov 28 2025 = Codex Arena (index 1)
ZAISHEN_COMBAT_START = datetime(2025, 11, 27)  # Calibrated
ZAISHEN_COMBAT = [
    ("Random Arena", "PvP", "Battle Isles", "Random_Arena_(Zaishen_quest)"),
    ("Codex Arena", "PvP", "Battle Isles", "Codex_Arena_(Zaishen_quest)"),
    ("Heroes' Ascent", "PvP", "Battle Isles", "Heroes%27_Ascent_(Zaishen_quest)"),
    ("Guild versus Guild", "PvP", "Battle Isles", "Guild_Versus_Guild_(Zaishen_quest)"),
    ("Alliance Battles", "PvP", "Battle Isles", "Alliance_Battles_(Zaishen_quest)"),
    ("Fort Aspenwood", "PvP", "Battle Isles", "Fort_Aspenwood_(Zaishen_quest)"),
    ("Jade Quarry", "PvP", "Battle Isles", "Jade_Quarry_(Zaishen_quest)"),
]

# ==================== PRE-SEARING VANGUARD DAILIES ====================
# 9-day cycle from Lieutenant Langmar
VANGUARD_QUESTS = [
    ("Vanguard Annihilation: Bandits", "Annihilation", "Pre-Searing", "Vanguard_Annihilation:_Bandits"),
    ("Vanguard Bounty: Utini Wupwup", "Bounty", "Pre-Searing", "Vanguard_Bounty:_Utini_Wupwup"),
    ("Vanguard Rescue: Ascalonian Noble", "Rescue", "Pre-Searing", "Vanguard_Rescue:_Save_the_Ascalonian_Noble"),
    ("Vanguard Annihilation: Undead", "Annihilation", "Pre-Searing", "Vanguard_Annihilation:_Undead"),
    ("Vanguard Bounty: Blazefiend Griefblade", "Bounty", "Pre-Searing", "Vanguard_Bounty:_Blazefiend_Griefblade"),
    ("Vanguard Rescue: Farmer Hamnet", "Rescue", "Pre-Searing", "Vanguard_Rescue:_Farmer_Hamnet"),
    ("Vanguard Annihilation: Charr", "Annihilation", "Pre-Searing", "Vanguard_Annihilation:_Charr"),
    ("Vanguard Bounty: Countess Nadya", "Bounty", "Pre-Searing", "Vanguard_Bounty:_Countess_Nadya"),
    ("Vanguard Rescue: Footman Tate", "Rescue", "Pre-Searing", "Vanguard_Rescue:_Footman_Tate"),
]

# ==================== NICHOLAS THE TRAVELER ====================
# Weekly rotation, 137 weeks cycle
NICHOLAS_START = datetime(2009, 4, 23)
NICHOLAS_GIFTS = [
    # (Week, Item, Quantity, Location, Region)
    # Full list would be very long - key items only
]

# ==================== WANTED BY SHINING BLADE ====================
WANTED_BOUNTIES = [
    ("Wanted: Inquisitor Bauer", "War in Kryta", "Kryta", "Wanted:_Inquisitor_Bauer"),
    ("Wanted: Inquisitor Lashona", "War in Kryta", "Kryta", "Wanted:_Inquisitor_Lashona"),
    ("Wanted: Inquisitor Lovisa", "War in Kryta", "Kryta", "Wanted:_Inquisitor_Lovisa"),
    # More bounties...
]


def get_current_zaishen_mission():
    """Calculate today's Zaishen Mission"""
    today = datetime.now()
    days_since_start = (today - ZAISHEN_MISSION_START).days
    index = days_since_start % len(ZAISHEN_MISSIONS)
    return ZAISHEN_MISSIONS[index]


def get_current_zaishen_bounty():
    """Calculate today's Zaishen Bounty"""
    today = datetime.now()
    days_since_start = (today - ZAISHEN_BOUNTY_START).days
    index = days_since_start % len(ZAISHEN_BOUNTIES)
    return ZAISHEN_BOUNTIES[index]


def get_upcoming_zaishen(days=7):
    """Get upcoming Zaishen quests for next N days"""
    missions = []
    bounties = []
    today = datetime.now()
    
    for i in range(days):
        date = today + timedelta(days=i)
        
        mission_idx = (date - ZAISHEN_MISSION_START).days % len(ZAISHEN_MISSIONS)
        missions.append((date.strftime("%Y-%m-%d"), ZAISHEN_MISSIONS[mission_idx]))
        
        bounty_idx = (date - ZAISHEN_BOUNTY_START).days % len(ZAISHEN_BOUNTIES)
        bounties.append((date.strftime("%Y-%m-%d"), ZAISHEN_BOUNTIES[bounty_idx]))
    
    return {"missions": missions, "bounties": bounties}
