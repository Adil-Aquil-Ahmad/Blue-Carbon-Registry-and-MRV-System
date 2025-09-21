#!/usr/bin/env python3
"""
Project Persistence Manager for Blue Carbon Registry
Saves and restores projects, evidence, and blockchain state.
"""

import os
import shutil
import json
import sqlite3
from datetime import datetime
import subprocess

class ProjectPersistenceManager:
    def __init__(self):
        self.backup_dir = "project-backups"
        self.db_path = "blue-carbon-backend/bluecarbon.db"
        self.contracts_backup = "blue-carbon-contracts/deployed-contracts.json"
        
    def create_backup_dir(self):
        """Create backup directory if it doesn't exist"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            print(f"📁 Created backup directory: {self.backup_dir}")
    
    def backup_projects(self, backup_name=None):
        """Create a backup of all projects and evidence"""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"projects_backup_{timestamp}"
        
        self.create_backup_dir()
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        print(f"💾 Creating project backup: {backup_name}")
        
        try:
            # Create backup subdirectory
            os.makedirs(backup_path, exist_ok=True)
            
            # Backup database
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, os.path.join(backup_path, "bluecarbon.db"))
                print(f"  ✅ Database backed up")
            else:
                print(f"  ⚠️  Database not found: {self.db_path}")
            
            # Backup uploads folder
            uploads_src = "blue-carbon-backend/uploads"
            uploads_dst = os.path.join(backup_path, "uploads")
            if os.path.exists(uploads_src):
                shutil.copytree(uploads_src, uploads_dst, dirs_exist_ok=True)
                file_count = len([f for f in os.listdir(uploads_src) if os.path.isfile(os.path.join(uploads_src, f))])
                print(f"  ✅ Uploads backed up ({file_count} files)")
            else:
                print(f"  ⚠️  Uploads folder not found")
            
            # Backup contract deployment info
            if os.path.exists(self.contracts_backup):
                shutil.copy2(self.contracts_backup, os.path.join(backup_path, "deployed-contracts.json"))
                print(f"  ✅ Contract addresses backed up")
            
            # Create metadata file
            metadata = {\n                "backup_name": backup_name,\n                "timestamp": datetime.now().isoformat(),\n                "version": "1.0",\n                "description": "Blue Carbon Registry project backup"\n            }\n            \n            with open(os.path.join(backup_path, "backup-metadata.json"), "w") as f:\n                json.dump(metadata, f, indent=2)\n            \n            print(f"  ✅ Backup metadata saved")\n            print(f"🎉 Backup completed successfully: {backup_path}")\n            return backup_path\n            \n        except Exception as e:\n            print(f"❌ Backup failed: {e}")\n            return None\n    \n    def list_backups(self):\n        """List all available backups"""\n        if not os.path.exists(self.backup_dir):\n            print("📁 No backups found")\n            return []\n        \n        backups = []\n        print(f"📋 Available backups in {self.backup_dir}:")\n        \n        for item in os.listdir(self.backup_dir):\n            backup_path = os.path.join(self.backup_dir, item)\n            if os.path.isdir(backup_path):\n                metadata_path = os.path.join(backup_path, "backup-metadata.json")\n                if os.path.exists(metadata_path):\n                    try:\n                        with open(metadata_path, "r") as f:\n                            metadata = json.load(f)\n                        \n                        backups.append({\n                            "name": item,\n                            "path": backup_path,\n                            "timestamp": metadata.get("timestamp", "Unknown"),\n                            "description": metadata.get("description", "No description")\n                        })\n                        \n                        print(f"  📦 {item}")\n                        print(f"     📅 {metadata.get('timestamp', 'Unknown time')}")\n                        print(f"     📝 {metadata.get('description', 'No description')}")\n                        print()\n                        \n                    except Exception as e:\n                        print(f"  ⚠️  {item} (corrupted metadata: {e})")\n                else:\n                    print(f"  ⚠️  {item} (no metadata)")\n        \n        return backups\n    \n    def restore_projects(self, backup_name):\n        """Restore projects from a backup"""\n        backup_path = os.path.join(self.backup_dir, backup_name)\n        \n        if not os.path.exists(backup_path):\n            print(f"❌ Backup not found: {backup_name}")\n            return False\n        \n        print(f"🔄 Restoring projects from backup: {backup_name}")\n        \n        try:\n            # Restore database\n            db_backup = os.path.join(backup_path, "bluecarbon.db")\n            if os.path.exists(db_backup):\n                shutil.copy2(db_backup, self.db_path)\n                print(f"  ✅ Database restored")\n            else:\n                print(f"  ⚠️  No database in backup")\n            \n            # Restore uploads\n            uploads_backup = os.path.join(backup_path, "uploads")\n            uploads_target = "blue-carbon-backend/uploads"\n            if os.path.exists(uploads_backup):\n                if os.path.exists(uploads_target):\n                    shutil.rmtree(uploads_target)\n                shutil.copytree(uploads_backup, uploads_target)\n                file_count = len([f for f in os.listdir(uploads_target) if os.path.isfile(os.path.join(uploads_target, f))])\n                print(f"  ✅ Uploads restored ({file_count} files)")\n            else:\n                print(f"  ⚠️  No uploads in backup")\n            \n            # Restore contract addresses (if available)\n            contracts_backup = os.path.join(backup_path, "deployed-contracts.json")\n            if os.path.exists(contracts_backup):\n                shutil.copy2(contracts_backup, self.contracts_backup)\n                print(f"  ✅ Contract addresses restored")\n            \n            print(f"🎉 Restore completed successfully!")\n            print(f"ℹ️  Note: You may need to restart the system to use restored data")\n            return True\n            \n        except Exception as e:\n            print(f"❌ Restore failed: {e}")\n            return False\n    \n    def get_current_project_stats(self):\n        """Get statistics about current projects"""\n        if not os.path.exists(self.db_path):\n            print("❌ Database not found")\n            return None\n        \n        try:\n            conn = sqlite3.connect(self.db_path)\n            cursor = conn.cursor()\n            \n            # Count projects in database (evidence entries)\n            cursor.execute("SELECT COUNT(DISTINCT project_id) FROM mrvdata")\n            project_count = cursor.fetchone()[0]\n            \n            # Count total evidence entries\n            cursor.execute("SELECT COUNT(*) FROM mrvdata")\n            evidence_count = cursor.fetchone()[0]\n            \n            # Count evidence with greenness analysis\n            cursor.execute("SELECT COUNT(*) FROM mrvdata WHERE green_progress_multiplier IS NOT NULL")\n            greenness_count = cursor.fetchone()[0]\n            \n            # Get recent activity\n            cursor.execute("SELECT COUNT(*) FROM mrvdata WHERE timestamp > datetime('now', '-7 days')")\n            recent_activity = cursor.fetchone()[0]\n            \n            conn.close()\n            \n            stats = {\n                "projects": project_count,\n                "evidence_entries": evidence_count,\n                "greenness_analyzed": greenness_count,\n                "recent_activity_7days": recent_activity\n            }\n            \n            print(f"📊 Current Project Statistics:")\n            print(f"  🏗️  Projects: {project_count}")\n            print(f"  📋 Evidence entries: {evidence_count}")\n            print(f"  🌱 Greenness analyzed: {greenness_count}")\n            print(f"  📅 Recent activity (7 days): {recent_activity}")\n            \n            return stats\n            \n        except Exception as e:\n            print(f"❌ Error getting stats: {e}")\n            return None

def main():\n    manager = ProjectPersistenceManager()\n    \n    print("🌿 Blue Carbon Registry - Project Persistence Manager")\n    print("=" * 55)\n    \n    while True:\n        print("\\nChoose an option:")\n        print("1. 💾 Create backup")\n        print("2. 📋 List backups")\n        print("3. 🔄 Restore from backup")\n        print("4. 📊 Show current project stats")\n        print("5. 🚪 Exit")\n        \n        choice = input("\\nEnter your choice (1-5): ").strip()\n        \n        if choice == "1":\n            backup_name = input("Enter backup name (or press Enter for auto-generated): ").strip()\n            if not backup_name:\n                backup_name = None\n            manager.backup_projects(backup_name)\n            \n        elif choice == "2":\n            manager.list_backups()\n            \n        elif choice == "3":\n            backups = manager.list_backups()\n            if backups:\n                backup_name = input("Enter backup name to restore: ").strip()\n                if backup_name:\n                    manager.restore_projects(backup_name)\n                else:\n                    print("❌ Please enter a backup name")\n            \n        elif choice == "4":\n            manager.get_current_project_stats()\n            \n        elif choice == "5":\n            print("👋 Goodbye!")\n            break\n            \n        else:\n            print("❌ Invalid choice. Please enter 1-5.")\n\nif __name__ == "__main__":\n    main()