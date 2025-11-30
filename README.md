# Guild Wars Companion

🎮 **Live at [gwcompanion.com](https://gwcompanion.com)**

Comprehensive progress tracker for Guild Wars 1. Track every aspect of your journey to GWAMM and beyond.

## ✨ Features

- **📜 Quests** - 1000+ quests across all campaigns and regions
- **🎯 Missions** - Normal/Bonus/Hard Mode tracking with master requirements
- **⚔️ Elite Skills** - 300 elite skills with profession filters and capture locations
- **🗺️ Cartographer** - 276 locations (towns, outposts, missions, explorable areas)
- **⚔️ Vanquisher** - 144 explorable areas to vanquish
- **🦸 Heroes** - 29 heroes with unlock requirements
- **🏰 Dungeons** - Elite missions + Eye of the North dungeons
- **🛡️ Armor** - Elite armor sets with profession filters
- **🐾 Miniatures** - 105 minis (Common/Uncommon/Rare/Unique)
- **🦁 Menagerie** - 37 Zaishen Menagerie animals
- **🏆 Titles** - Full GWAMM progress tracking
- **🏛️ Hall of Monuments** - 50/50 HoM calculator
- **🎁 Collectibles** - Unique items and weapons

## 🚀 Quick Start

**Option 1: Use Online** (No Installation)
Visit [gwcompanion.com](https://gwcompanion.com) and start tracking!

**Option 2: Run Locally**
```bash
# Windows: Double-click GW_Quest_Tracker.bat
# Or manually:
python gw_tracker.py --build-only
# Then open index.html in your browser
```

## 📁 Repository Structure

```
gw-companion/
├── index.html              # Main tracker app
├── gw_tracker.py          # Build script
├── data/                  # Game data
├── quests/                # Quest definitions
├── GW_Quest_Tracker.bat   # Windows launcher
└── README.md
```

## 🛠️ Development

Build the app:
```bash
python gw_tracker.py --build-only
```

The script generates `index.html` from data sources.

## 🤝 Contributing

PRs welcome! Areas that need help:
- Complete unique/green items database
- Additional quest data validation
- UI/UX improvements

## 📄 License

MIT - Feel free to use and modify!
