#!/usr/bin/env python3
"""
Auto-backup script that preserves projects before system restart.
"""

import os
import shutil
import json
from datetime import datetime

def auto_backup_projects():
    """Automatically backup projects before system restart"""
    print("🔄 Auto-backup: Preserving current projects...")
    
    # Paths
    db_path = "blue-carbon-backend/bluecarbon.db"
    uploads_path = "blue-carbon-backend/uploads"
    backup_path = "last-session-backup"
    
    # Create backup directory
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)
    os.makedirs(backup_path)
    
    projects_found = False
    
    try:
        # Backup database if it exists and has projects
        if os.path.exists(db_path):
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM mrvdata")
            evidence_count = cursor.fetchone()[0]
            conn.close()
            
            if evidence_count > 0:
                shutil.copy2(db_path, os.path.join(backup_path, "bluecarbon.db"))
                print(f"  ✅ Database backed up ({evidence_count} evidence entries)")
                projects_found = True
            else:
                print(f"  ℹ️  No projects to backup")
        
        # Backup uploads if they exist
        if os.path.exists(uploads_path):
            files = [f for f in os.listdir(uploads_path) if os.path.isfile(os.path.join(uploads_path, f))]
            if files:
                shutil.copytree(uploads_path, os.path.join(backup_path, "uploads"))
                print(f"  ✅ Uploads backed up ({len(files)} files)")
                projects_found = True
        
        # Create metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "auto_backup": True,
            "evidence_count": evidence_count if 'evidence_count' in locals() else 0
        }
        
        with open(os.path.join(backup_path, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
        
        if projects_found:
            print(f"  ✅ Auto-backup completed")
            return True
        else:
            print(f"  ℹ️  No projects found to backup")
            return False
            
    except Exception as e:
        print(f"  ❌ Auto-backup failed: {e}")
        return False

def auto_restore_projects():
    """Automatically restore projects from last session"""
    backup_path = "last-session-backup"
    
    if not os.path.exists(backup_path):
        print("ℹ️  No previous session backup found")
        return False
    
    # Check if backup has metadata
    metadata_path = os.path.join(backup_path, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        evidence_count = metadata.get("evidence_count", 0)
        timestamp = metadata.get("timestamp", "Unknown")
        
        if evidence_count > 0:
            print(f"🔄 Found previous session with {evidence_count} projects from {timestamp[:19]}")
            restore_choice = input("Do you want to restore your previous projects? (y/n): ").strip().lower()
            
            if restore_choice == 'y':
                try:
                    # Restore database
                    db_backup = os.path.join(backup_path, "bluecarbon.db")
                    if os.path.exists(db_backup):
                        shutil.copy2(db_backup, "blue-carbon-backend/bluecarbon.db")
                        print("  ✅ Database restored")
                    
                    # Restore uploads
                    uploads_backup = os.path.join(backup_path, "uploads")
                    uploads_target = "blue-carbon-backend/uploads"
                    if os.path.exists(uploads_backup):
                        if os.path.exists(uploads_target):
                            shutil.rmtree(uploads_target)
                        shutil.copytree(uploads_backup, uploads_target)
                        print("  ✅ Uploads restored")
                    
                    print("🎉 Previous projects restored successfully!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Restore failed: {e}")
                    return False
            else:
                print("ℹ️  Starting with fresh system")
                return False
    
    return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "backup":
            auto_backup_projects()
        elif sys.argv[1] == "restore":
            auto_restore_projects()
        else:
            print("Usage: python auto-backup.py [backup|restore]")
    else:
        # Interactive mode
        print("🌿 Blue Carbon Registry - Auto Backup")
        print("=" * 40)
        print("1. Backup current projects")
        print("2. Restore previous session")
        print("3. Both (backup current, then restore)")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            auto_backup_projects()
        elif choice == "2":
            auto_restore_projects()
        elif choice == "3":
            auto_backup_projects()
            auto_restore_projects()
        else:
            print("Invalid choice")