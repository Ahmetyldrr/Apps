#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test verisi oluşturma scripti
Bu script veritabanına örnek kullanıcılar ekler
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.database import Database

def create_test_data():
    """Veritabanına test kullanıcıları ekler"""
    db = Database()
    
    # Test kullanıcıları
    test_users = [
        "Ahmet",
        "Mehmet", 
        "Ayşe",
        "Fatma",
        "Ali",
        "Veli"
    ]
    
    print("Test kullanıcıları ekleniyor...")
    
    for username in test_users:
        user_id = db.add_user(username)
        if user_id:
            print(f"✓ {username} kullanıcısı eklendi (ID: {user_id})")
        else:
            print(f"✗ {username} kullanıcısı zaten mevcut")
    
    print("\nMevcut kullanıcılar:")
    users = db.get_all_users()
    for user in users:
        print(f"- {user[1]} (ID: {user[0]})")
    
    print(f"\nToplam {len(users)} kullanıcı kayıtlı")

if __name__ == "__main__":
    create_test_data()
