#!/usr/bin/env python3
"""
Verification script for password columns
User: larabiislem
Date: 2025-11-03 19:35:43 UTC
"""
from sqlalchemy import text, inspect
from database import get_engine, get_session, init_db
from models import Student, Club
from datetime import datetime
import sys


init_db()

def check_columns():
    """Check if password columns exist"""
    print("\n" + "="*60)
    print("  Password Columns Verification")
    print("  User: larabiislem")
    print("  Date: 2025-11-03 19:42:55 UTC")
    print("="*60 + "\n")
    
    try:
        engine = get_engine()
        inspector = inspect(engine)
        
        # Get columns
        students_cols = [col['name'] for col in inspector.get_columns('students')]
        clubs_cols = [col['name'] for col in inspector.get_columns('clubs')]
        
        all_good = True
        
        # Check students.password_hash
        print("Checking students table:")
        if 'password_hash' in students_cols:
            print("  [OK] password_hash column exists")
        else:
            print("  [MISSING] password_hash column NOT found")
            all_good = False
        
        # Check clubs columns
        print("\nChecking clubs table:")
        if 'email' in clubs_cols:
            print("  [OK] email column exists")
        else:
            print("  [MISSING] email column NOT found")
            all_good = False
        
        if 'password_hash' in clubs_cols:
            print("  [OK] password_hash column exists")
        else:
            print("  [MISSING] password_hash column NOT found")
            all_good = False
        
        print("\n" + "="*60)
        
        if all_good:
            print("Result: ALL COLUMNS EXIST")
            print("="*60 + "\n")
            return True
        else:
            print("Result: MISSING COLUMNS")
            print("\nRun this to fix:")
            print("  python scripts/add_passwords_migration.py")
            print("="*60 + "\n")
            return False
            
    except Exception as e:
        print(f"\nError: {e}\n")
        return False


if __name__ == "__main__":
    success = check_columns()
    sys.exit(0 if success else 1)