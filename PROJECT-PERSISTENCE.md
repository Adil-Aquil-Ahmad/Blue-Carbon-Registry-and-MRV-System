# 🌿 Blue Carbon Registry - Project Persistence Guide

## 📖 Overview

Your Blue Carbon Registry now has **automatic project persistence**! Projects, evidence, and analysis results are automatically saved and restored between system restarts.

## 🚀 Quick Start

### Starting the System
```bash
# Windows
.\start-system.bat

# The system will:
# 1. Check for previous projects and ask to restore them
# 2. Start all services (blockchain, backend, frontend)  
# 3. Automatically backup current session
```

### Stopping the System
```bash
# Windows
.\shutdown-system.bat

# The system will:
# 1. Backup all current projects
# 2. Stop all services cleanly
# 3. Preserve data for next restart
```

## 💾 Backup Features

### Automatic Backups
- **On Startup**: System checks for previous session and offers to restore
- **On Shutdown**: System automatically backs up current projects
- **Manual**: Use `project-persistence.py` for manual backup management

### What Gets Backed Up
- ✅ **Database**: All projects, evidence entries, and Green Progress analysis
- ✅ **Images**: All uploaded before/after images in `/uploads`
- ✅ **Analysis Results**: Carbon credit calculations and AI analysis
- ✅ **Timestamps**: When each backup was created

## 🔧 Manual Backup Management

### Using the Persistence Manager
```bash
python project-persistence.py
```

**Available Options:**
1. **💾 Create backup** - Manually backup current projects
2. **📋 List backups** - See all available backups with timestamps
3. **🔄 Restore from backup** - Restore from any previous backup
4. **📊 Show current project stats** - View project statistics
5. **🚪 Exit** - Close the manager

### Using Auto-Backup Script
```bash
# Backup current projects
python auto-backup.py backup

# Restore previous session
python auto-backup.py restore

# Interactive mode
python auto-backup.py
```

## 📁 Backup Structure

```
project-backups/
├── projects_backup_20250922_143022/
│   ├── bluecarbon.db           # Database with all projects
│   ├── uploads/                # All uploaded images
│   └── backup-metadata.json   # Backup information
└── last-session-backup/        # Auto-backup from last session
    ├── bluecarbon.db
    ├── uploads/
    └── metadata.json
```

## 🎯 Benefits

### ✅ **No More Lost Projects**
- Projects persist between system restarts
- Evidence and images are preserved
- Green Progress analysis results saved

### ✅ **Automatic Management**  
- No manual intervention required
- Seamless startup and shutdown
- Smart backup scheduling

### ✅ **Multiple Restore Points**
- Manual backups with custom names
- Automatic session backups
- Easy restore from any point

### ✅ **Project Statistics**
- Track project count over time
- Monitor evidence entries
- See Green Progress analysis adoption

## 🔍 Troubleshooting

### Projects Not Restoring?
1. Check if `last-session-backup` folder exists
2. Run `python auto-backup.py restore` manually
3. Use `python project-persistence.py` to list available backups

### Database Issues?
1. Initialize fresh database: `python blue-carbon-backend/init_db.py`
2. Add Green Progress columns: `python blue-carbon-backend/add_green_progress_columns.py`
3. Restore from backup using persistence manager

### Blockchain State Issues?
- Hardhat now uses persistent cache in `blue-carbon-contracts/blockchain-data/`
- Delete this folder to start with fresh blockchain state
- Contract addresses may change, requiring frontend refresh

## 📊 Project Statistics

View current project statistics:
```bash
cd blue-carbon-backend
python ../project-persistence.py
# Choose option 4 for statistics
```

**Statistics Include:**
- 🏗️ Total projects
- 📋 Evidence entries  
- 🌱 Greenness analysis count
- 📅 Recent activity (7 days)

## 🎉 Success!

Your Blue Carbon Registry now features:
- ✅ Automatic project persistence
- ✅ Smart backup and restore
- ✅ Manual backup management
- ✅ Project statistics tracking
- ✅ Clean startup and shutdown

**No more lost projects!** The system automatically preserves your work between sessions. 🌱💚