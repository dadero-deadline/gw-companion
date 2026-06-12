# Guild Wars Companion

🎮 **Live at [gwcompanion.com](https://gwcompanion.com)**

Comprehensive progress tracker for Guild Wars 1. Track every aspect of your journey to GWAMM and beyond.

## ✨ Features

- **📜 Quests** - 1000+ quests across all campaigns and regions
- **🎯 Missions** - Normal/Bonus/Hard Mode tracking with master requirements
- **⚔️ Elite Skills** - 300 elite skills with profession filters and capture locations
- **🗺️ Cartographer** - 275 locations (towns, outposts, missions, explorable areas)
- **⚔️ Vanquisher** - 138 explorable areas to vanquish
- **🦸 Heroes** - 31 heroes with unlock requirements
- **🏰 Dungeons** - Elite missions + Eye of the North dungeons
- **🛡️ Armor** - Elite armor sets with profession filters
- **🐾 Miniatures** - 105 minis (Common/Uncommon/Rare/Unique)
- **🦁 Menagerie** - 37 Zaishen Menagerie animals
- **🏆 Titles** - Full GWAMM progress tracking
- **🏛️ Hall of Monuments** - 50/50 HoM calculator
- **🎁 Collectibles** - Unique items and weapons
- **🎭 Optional Game Modes** - Reforged / Dhuum's Covenant / Melandru's Accord toggles (per character)

## 🎭 Optional Game Modes

Three per-character toggles sit in the header next to the character selector. State is saved per character (in a `gw-modes` localStorage key) and is fully backward-compatible — existing saves load with the default states and nothing is lost.

- **⚒️ Reforged Mode** *(on by default)* — the mechanical toggle. Shows the *Guild Wars Reforged* content: 10 extra Prophecies quests, the heroes **Devona** & **Ghost of Althea**, and the pre-Searing **Piken Square** outpost. Turning it **off** hides those rows and dynamically recalculates every counter, progress bar and dropdown total (e.g. Pre-Searing 72 → 67, Post-Searing 67 → 63, Kryta 31 → 30, Heroes 31 → 29, Outposts 182 → 181).
- **💀 Dhuum's Covenant** *(off by default)* — cosmetic badge next to the character name, tooltip *"One life. No resurrection."*
- **🌿 Melandru's Accord** *(off by default)* — Ironman badge next to the character name; greys out the Zaishen Menagerie section with a *"Blocked under Melandru's Accord"* notice and flags tome-dependent spots.

## 🚀 Quick Start

**Option 1: Use Online** (No Installation)
Visit [gwcompanion.com](https://gwcompanion.com) and start tracking!

**Option 2: Run Locally**
- Simply open `index.html` in your browser, **or** serve it locally (recommended — keeps `localStorage` on a stable origin):

```bash
python serve.py   # serve-only on http://localhost:8000 — never rebuilds
```

## 🛠️ Development

`gw_tracker.py` is the **source of truth**: it generates `index.html` from `data/*.py` and `quests/*.xlsx`. Edit the data/generator — never `index.html` directly — then rebuild:

```bash
python gw_tracker.py --build-only   # regenerates index.html
```

For local viewing during development use the serve-only helper. It **does not rebuild**, so it can never clobber a generated/hand-checked `index.html`:

```bash
python serve.py   # http://localhost:8000
```

> `gw_tracker.html` is a build artifact (identical to `index.html`) and is gitignored — never commit it.

## 📁 Repository Structure

```
gw-companion/
├── index.html              # Generated tracker app (static HTML) — build output
├── gw_tracker.py           # Generator / source of truth (builds index.html)
├── serve.py                # Serve-only dev server (no rebuild)
├── data/                   # Game data (Python modules, incl. cartographer.py)
├── quests/                 # Quest definitions (xlsx)
└── README.md
```

## 🤝 Contributing

PRs welcome! Areas that need help:
- Complete unique/green items database
- Additional quest data validation
- UI/UX improvements

## 📄 License

MIT - Feel free to use and modify!
