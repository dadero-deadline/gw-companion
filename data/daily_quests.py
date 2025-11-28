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

# ==================== PRE-SEARING VANGUARD DAILIES ====================
VANGUARD_QUESTS = [
    ("Charr at the Gate", "Daily", "Ascalon City", "Charr_at_the_Gate"),
    ("Farmer Hamnet", "Daily", "Lakeside County", "Farmer_Hamnet_(quest)"),
    ("The Worm Problem", "Daily", "Lakeside County", "The_Worm_Problem"),
    ("Bandit Raid", "Daily", "Lakeside County", "Bandit_Raid"),
    ("The Prize Moa Bird", "Daily", "Wizard's Folly", "The_Prize_Moa_Bird"),
    ("Undead Invasion", "Daily", "Green Hills County", "Undead_Invasion"),
    ("Supplies of War", "Daily", "The Northlands", "Supplies_of_War"),
    ("A Guilds Burden", "Daily", "Wizard's Folly", "A_Guild%27s_Burden"),
    ("Little Thom", "Daily", "Regent Valley", "Little_Thom_(quest)"),
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
