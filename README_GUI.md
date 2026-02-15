# Minesweeper AI - Graphical Edition

A professional-grade Minesweeper game with full graphical interface and advanced AI assistant.

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
- Double-click `Play_Minesweeper_GUI.bat`

### Option 2: Direct Launch
- Double-click `MinesweeperAI_GUI.exe`

## 🎮 GUI Features

### Professional Interface
- **Full Graphical Interface**: Modern, intuitive GUI design
- **Visual Board**: Click-based gameplay with visual feedback
- **Real-time Updates**: Live mine counter and timer
- **Professional Theme**: Dark theme with color-coded elements

### Game Controls
- **Left Click**: Reveal cell
- **Right Click**: Place/remove flag
- **Menu Buttons**: New game, AI hints, statistics, settings
- **Difficulty Selector**: Choose from 5 difficulty levels

### AI Assistant
- **Visual Hints**: AI suggestions shown in dialog boxes
- **Apply Hints**: One-click application of AI recommendations
- **Probability Analysis**: Risk assessment for uncertain cells
- **Real-time Analysis**: Get AI help anytime during gameplay

### Difficulty Levels
- **Beginner**: 8x8 board, 10 mines
- **Easy**: 10x10 board, 15 mines
- **Medium**: 12x12 board, 25 mines
- **Hard**: 16x16 board, 40 mines
- **Expert**: 20x20 board, 80 mines

## 🎯 How to Play

### Starting the Game
1. Launch the application
2. Select your preferred difficulty
3. Click any cell to start (first click is always safe)

### Gameplay
- **Left-click** cells to reveal them
- **Right-click** cells to flag suspected mines
- **Numbers** show how many mines are adjacent
- **Reveal all non-mine cells** to win

### AI Assistance
- Click **"AI Hints"** button anytime for help
- View certain mines, safe cells, and probability analysis
- Click **"Apply Hints"** to automatically use AI recommendations

### Menu Options
- **New Game**: Start fresh with current difficulty
- **AI Hints**: Get intelligent suggestions
- **Stats**: View your performance statistics
- **Settings**: Configure game options

## 📊 Statistics Tracking

The GUI automatically tracks:
- Games played and won
- Win rate percentage
- Best completion time
- Average completion time
- AI suggestions used

## 🎨 Visual Features

### Color Scheme
- **Dark Theme**: Professional dark interface
- **Color-coded Numbers**: Each number has unique color
- **Visual Feedback**: Clear indication of cell states
- **Flag Icons**: Visual flag markers

### Cell States
- **Unknown**: Dark gray raised buttons
- **Revealed**: Light gray sunken buttons
- **Numbered**: Colored numbers on revealed cells
- **Flagged**: Flag icon on unknown cells
- **Mine**: Bomb icon (shown on game over)

## ⚙️ Settings

Customize your experience:
- **AI Assistant**: Enable/disable AI suggestions
- **Auto-save**: Automatically save statistics

## 🗂️ File Locations

Configuration and statistics are stored in:
```
%USERPROFILE%\.minesweeper_ai\
├── config.json      # Game settings
├── stats.json        # Game statistics
└── logs/            # Application logs
```

## 🔧 Technical Specifications

- **Version**: 1.0.0 GUI Edition
- **Platform**: Windows 10/11
- **Interface**: Tkinter GUI (built-in Python)
- **AI Engine**: Advanced constraint satisfaction and probability analysis
- **Dependencies**: None (fully self-contained executable)
- **Size**: ~10 MB

## 🐛 Troubleshooting

### Common Issues
1. **Game won't start**: Check Windows Defender or antivirus
2. **GUI not responsive**: Restart the application
3. **AI not working**: Ensure AI is enabled in settings

### Error Logs
If you encounter issues, check the log files at:
`%USERPROFILE%\.minesweeper_ai\logs\`

## 📝 Legend

- **Left Click**: Reveal cell
- **Right Click**: Flag/unflag cell
- **Numbers**: Adjacent mine count (color-coded)
- **Flags**: Suspected mine locations
- **AI Hints**: Intelligent suggestions

## 🏆 Tips for Success

1. **Start Smart**: Begin with corners or edges
2. **Use AI**: Click AI Hints button when stuck
3. **Flag First**: Mark certain mines before revealing safe cells
4. **Pattern Recognition**: Learn common mine patterns
5. **Probability**: When uncertain, use AI probability analysis

## 🎮 GUI vs Terminal

### GUI Advantages:
- Visual interface with click controls
- Real-time visual feedback
- Professional appearance
- Easy difficulty switching
- Visual AI hints application

### Terminal Advantages:
- Lightweight and fast
- Works on any terminal
- Lower resource usage
- Keyboard-based controls

Choose the version that best fits your preference!

---

**Minesweeper AI - Graphical Edition v1.0**  
*Professional gaming with artificial intelligence and modern GUI*

Built for the ultimate visual Minesweeper experience with intelligent AI assistance.
