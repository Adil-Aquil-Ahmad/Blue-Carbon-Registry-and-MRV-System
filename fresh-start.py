#!/usr/bin/env python3
"""
Clean slate script - Remove all past entries and start fresh.
"""

import os
import shutil
import sqlite3
from datetime import datetime

def clear_all_data():
    """Remove all projects, evidence, and uploaded files"""
    print("🧹 Starting fresh - Clearing all data...")
    print("=" * 45)
    
    # Paths to clear
    db_path = "blue-carbon-backend/bluecarbon.db"
    uploads_path = "blue-carbon-backend/uploads"
    backups_path = "project-backups"
    last_backup_path = "last-session-backup"
    blockchain_cache = "blue-carbon-contracts/blockchain-data"
    contracts_cache = "blue-carbon-contracts/cache"
    artifacts_path = "blue-carbon-contracts/artifacts"
    
    cleared_items = []
    
    try:
        # 1. Clear database (delete and recreate)
        if os.path.exists(db_path):
            os.remove(db_path)
            cleared_items.append("Database")
            print("  ✅ Database cleared")
        
        # 2. Clear uploads folder
        if os.path.exists(uploads_path):
            shutil.rmtree(uploads_path)
            os.makedirs(uploads_path)
            cleared_items.append("Uploads")
            print("  ✅ Uploads folder cleared")
        
        # 3. Clear backups
        if os.path.exists(backups_path):
            shutil.rmtree(backups_path)
            cleared_items.append("Project backups")
            print("  ✅ Project backups cleared")
        
        if os.path.exists(last_backup_path):
            shutil.rmtree(last_backup_path)
            cleared_items.append("Last session backup")
            print("  ✅ Last session backup cleared")
        
        # 4. Clear blockchain cache
        if os.path.exists(blockchain_cache):
            shutil.rmtree(blockchain_cache)
            cleared_items.append("Blockchain cache")
            print("  ✅ Blockchain cache cleared")
        
        # 5. Clear contract compilation cache
        if os.path.exists(contracts_cache):
            shutil.rmtree(contracts_cache)
            cleared_items.append("Contract cache")
            print("  ✅ Contract cache cleared")
        
        # 6. Clear artifacts (will be regenerated)
        if os.path.exists(artifacts_path):
            shutil.rmtree(artifacts_path)
            cleared_items.append("Contract artifacts")
            print("  ✅ Contract artifacts cleared")
        
        # 7. Remove test images if they exist
        test_files = ["green.png", "red.png"]
        for test_file in test_files:
            if os.path.exists(test_file):
                os.remove(test_file)
                print(f"  ✅ Test file {test_file} removed")
        
        print("")
        print("🎉 Clean slate completed!")
        print(f"📋 Cleared: {', '.join(cleared_items)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return False

def reinitialize_database():
    """Reinitialize the database with fresh schema"""
    print("")
    print("🗃️  Reinitializing database...")
    
    try:
        # Run database initialization
        os.chdir("blue-carbon-backend")
        
        # Initialize fresh database
        import subprocess
        result = subprocess.run(["python", "init_db.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Database initialized")
            
            # Add Green Progress columns
            result2 = subprocess.run(["python", "add_green_progress_columns.py"], capture_output=True, text=True)
            
            if result2.returncode == 0:
                print("  ✅ Green Progress columns added")
                print("  ✅ Database ready for new projects")
                return True
            else:
                print(f"  ❌ Error adding Green Progress columns: {result2.stderr}")
                return False
        else:
            print(f"  ❌ Error initializing database: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Database initialization failed: {e}")
        return False
    finally:
        os.chdir("..")

def create_fresh_test_data():
    """Create fresh test green/red images for testing"""
    print("")
    print("🎨 Creating fresh test images...")
    
    try:
        os.chdir("blue-carbon-backend")
        
        import subprocess
        result = subprocess.run(["python", "create_test_images.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Fresh green.png and red.png created")
            print("  ✅ Ready for greenness analysis testing")
            return True
        else:
            print(f"  ❌ Error creating test images: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Test image creation failed: {e}")
        return False
    finally:
        os.chdir("..")

def main():
    print("🌿 Blue Carbon Registry - Fresh Start")
    print("=" * 40)
    print("This will remove ALL existing:")
    print("  • Projects and evidence")
    print("  • Uploaded images")
    print("  • Backups and cache")
    print("  • Blockchain state")
    print("")
    
    confirm = input("Are you sure you want to start fresh? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        print("")
        success = True
        
        # Step 1: Clear all data
        if not clear_all_data():
            success = False
        
        # Step 2: Reinitialize database
        if success and not reinitialize_database():
            success = False
        
        # Step 3: Create test data
        if success and not create_fresh_test_data():
            success = False
        
        if success:
            print("")
            print("🎉 FRESH START COMPLETE!")
            print("=" * 25)
            print("✅ System reset to clean state")
            print("✅ Database ready with Green Progress support")
            print("✅ Test images available for verification")
            print("")
            print("🚀 Next steps:")
            print("1. Restart the system: .\\start-system.bat")
            print("2. Test with green/red images: python test_green_red_api.py")
            print("3. Upload real projects through the frontend")
            print("")
            print("Your Blue Carbon Registry is ready for fresh projects! 🌱")
        else:
            print("")
            print("❌ Fresh start encountered some errors.")
            print("Please check the output above and retry.")
    
    else:
        print("❌ Fresh start cancelled. No changes made.")

if __name__ == "__main__":
    main()