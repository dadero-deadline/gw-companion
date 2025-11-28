# Guild Wars Companion

Progress tracker for Guild Wars 1. Track quests, missions, skills, titles, and HoM progress.

## Features

- **Quests** - All campaigns and regions
- **Missions** - Normal/Bonus/Hard Mode tracking  
- **Elite Skills** - 300 skills with profession filter
- **Heroes** - 29 heroes with unlock info
- **Dungeons** - Elite missions + EotN dungeons
- **Vanquish** - All ~150 areas
- **Armor** - Elite armor sets
- **Minipets** - 100+ minis
- **Titles** - GWAMM progress
- **HoM** - Hall of Monuments

## Install

```bash
pip install openpyxl
python gw_tracker.py
```

Open http://localhost:8000

Windows: Double-click `GW_Quest_Tracker.bat`

## Structure

```
gw-companion/
├── gw_tracker.py      # Main app
├── data/              # Game data (skills, heroes, etc.)
├── quests/            # Quest Excel files
└── README.md
```

## Contributing

PRs welcome. Could use help with:
- Complete green items database
- Toolbox integration

## License

MIT
