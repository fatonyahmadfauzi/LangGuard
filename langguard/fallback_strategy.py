#!/usr/bin/env python3
"""
LangGuard - Section Fallback Strategy
Fallback untuk handle file yang belum punya DISPLAY_LANGUAGES section
"""

import os
import sys

def check_display_section_exists(content):
    """Cek apakah DISPLAY_LANGUAGES section ada"""
    return 'DISPLAY_LANGUAGES = {' in content

def run_section_fallback(target_file, command_name):
    """
    Fallback utama: Handle file tanpa DISPLAY_LANGUAGES section
    
    Args:
        target_file: File yang akan diproses
        command_name: Nama command yang dijalankan (e.g., 'add-lang', 'translate')
    
    Returns:
        bool: True jika section ada/generated, False jika dibatalkan
    """
    print(f"🎯 {command_name}: {target_file}")
    print("=" * 60)
    
    if not os.path.exists(target_file):
        print(f"❌ File {target_file} not found.")
        return False
    
    # Baca file
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Cek apakah section sudah ada
    if check_display_section_exists(content):
        print("✅ DISPLAY_LANGUAGES section found!")
        return True
    
    # ❌ Section tidak ada - handle khusus untuk remove-lang
    if command_name == "remove-lang":
        print(f"❌ File '{target_file}' doesn't have DISPLAY_LANGUAGES section!")
        print("💡 No languages to remove - section doesn't exist")
        return False
    
    # ❌ Untuk command lainnya, jalankan fallback normal
    print(f"❌ File '{target_file}' doesn't have DISPLAY_LANGUAGES section!")
    
    while True:
        choice = input("👉 Do you want to generate a complete DISPLAY_LANGUAGES section now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print(f"🎯 Generating DISPLAY_LANGUAGES section for {command_name}...")
            # Panggil fungsi generate section dengan import dinamis
            try:
                from .insert_section import run_insert_section
                success = run_insert_section(target_file)
            except ImportError:
                from insert_section import run_insert_section
                success = run_insert_section(target_file)
            
            if success:
                print("✅ Section generated successfully — continuing with original command...")
                return True  # ✅ PERBAIKAN: Langsung return True, tidak jalankan lagi
            else:
                print("❌ Failed to generate section.")
                return False
        elif choice in ['n', 'no', '']:
            print("ℹ️ Operation cancelled. No changes made.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

# Convenience functions untuk command-specific fallback
def fallback_for_check(target_file):
    """Fallback khusus untuk check/analysis command"""
    return run_section_fallback(target_file, "check")

def fallback_for_add_lang(target_file):
    """Fallback khusus untuk add-lang command"""
    return run_section_fallback(target_file, "add-lang")

def fallback_for_translate(target_file):
    """Fallback khusus untuk translate command"""
    return run_section_fallback(target_file, "translate")

def fallback_for_repair(target_file):
    """Fallback khusus untuk repair command"""
    return run_section_fallback(target_file, "repair")

def fallback_for_set_global_lang(target_file):
    """Fallback khusus untuk set-global-lang command"""
    return run_section_fallback(target_file, "set-global-lang")

def fallback_for_fix_order(target_file):
    """Fallback khusus untuk fix-order command"""
    return run_section_fallback(target_file, "fix-order")

def fallback_for_remove_lang(target_file):
    """Fallback khusus untuk remove-lang command"""
    return run_section_fallback(target_file, "remove-lang")

# ======================== CLI MODE ========================
if __name__ == "__main__":
    if len(sys.argv) > 2:
        command_name = sys.argv[1]
        target_file = sys.argv[2]
        
        if command_name == "add-lang":
            fallback_for_add_lang(target_file)
        elif command_name == "translate":
            fallback_for_translate(target_file)
        elif command_name == "repair":
            fallback_for_repair(target_file)
        elif command_name == "set-global-lang":
            fallback_for_set_global_lang(target_file)
        elif command_name == "fix-order":
            fallback_for_fix_order(target_file)
        elif command_name == "remove-lang":
            fallback_for_remove_lang(target_file)
        else:
            print(f"❌ Unknown command: {command_name}")
    else:
        print("❌ Usage: python fallback_strategy.py <command> <filename>")
        print("Available commands: add-lang, translate, repair, set-global-lang, fix-order, remove-lang")