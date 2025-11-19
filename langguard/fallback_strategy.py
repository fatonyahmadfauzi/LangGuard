#!/usr/bin/env python3
"""
LangGuard - Section Fallback Strategy
Fallback untuk handle file yang belum punya DISPLAY_LANGUAGES section - VERSI DIPERBAIKI
"""

import os
import sys
import re

try:
    from .language_selection import select_languages_for_addition, select_default_language
except ImportError:
    from language_selection import select_languages_for_addition, select_default_language

def check_display_section_exists(content):
    """Cek apakah DISPLAY_LANGUAGES section ada"""
    return 'DISPLAY_LANGUAGES = {' in content

def find_best_insert_position(content):
    """Temukan posisi terbaik untuk menyisipkan section - VERSI DIPERBAIKI"""
    lines = content.splitlines()
    
    # Cari akhir dari import statements saja (bukan variabel global)
    insert_pos = 0
    in_docstring = False
    found_imports = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Handle docstring
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if not in_docstring:
                in_docstring = True
            else:
                in_docstring = False
            continue
            
        # Skip jika masih dalam docstring
        if in_docstring:
            continue
            
        # Jika menemukan import statement, catat posisi
        if stripped.startswith('import ') or stripped.startswith('from '):
            found_imports = True
            insert_pos = i + 1
            continue
            
        # Jika sudah melewati import statements dan menemukan baris kosong, tetap lanjutkan
        if found_imports and not stripped:
            insert_pos = i + 1
            continue
            
        # Jika menemukan variabel global (seperti SOURCE_FILE), BERHENTI di sini
        # Karena kita ingin menyisipkan SEBELUM variabel global
        if (stripped.startswith('SOURCE_FILE') or
            stripped.startswith('CHANGELOG_FILE') or
            stripped.startswith('PACKAGE_JSON') or
            stripped.startswith('OUTPUT_DIR') or
            stripped.startswith('PROTECTED_FILE') or
            stripped.startswith('PROTECT_STATUS_FILE')):
            break
            
        # Jika menemukan kode lain (bukan import/variable), berhenti
        if stripped and not stripped.startswith('#') and found_imports:
            break
    
    # Jika tidak ditemukan import statements, sisipkan setelah docstring
    if insert_pos == 0:
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                else:
                    insert_pos = i + 1
                    break
    
    return insert_pos

def run_section_fallback(target_file, command_name):
    """Fallback utama: Handle file tanpa DISPLAY_LANGUAGES section - VERSI DIPERBAIKI DENGAN MULTIPLE SELECTION"""
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
    
    # ❌ Untuk command lainnya, langsung generate section sederhana
    print(f"❌ File '{target_file}' doesn't have DISPLAY_LANGUAGES section!")
    
    while True:
        choice = input("👉 Do you want to generate a complete DISPLAY_LANGUAGES section now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print(f"🎯 Generating DISPLAY_LANGUAGES section for {command_name}...")
            
            # Backup file sebelum modifikasi
            backup_path = target_file + ".fallback_backup"
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"📁 Backup created: {backup_path}")
            
            # ✅ PERBAIKAN: GUNAKAN FUNGSI TERPUSAT
            try:
                # Pilih bahasa untuk ditambahkan
                selected_langs_sorted = select_languages_for_addition()
                
                if not selected_langs_sorted:
                    print("❌ No languages selected. Operation cancelled.")
                    return False
                
                print(f"🌍 Selected {len(selected_langs_sorted)} languages: {', '.join(selected_langs_sorted)}")
                
                # Pilih bahasa default
                default_lang = select_default_language(selected_langs_sorted, None)
                
                if not default_lang:
                    print("❌ No default language selected. Operation cancelled.")
                    return False
                
                lang_name = {
                    "en": "English", "pl": "Polski", "zh": "中文", "jp": "日本語",
                    "de": "Deutsch", "fr": "Français", "es": "Español", "ru": "Pycckuñ",
                    "pt": "Portugués", "id": "Indonesia", "kr": "한국어"
                }.get(default_lang, default_lang.upper())
                
                print(f"⭐ Default language set to: {lang_name} ({default_lang})")
                
            except Exception as e:
                print(f"❌ Error during language selection: {e}")
                return False
            
            # ✅ LANJUTKAN DENGAN BAGIAN PEMBERSIHAN DAN PEMBUATAN SECTION
            print("🔄 Removing old display functions if any...")
            
            # Pattern untuk menghapus fungsi display language lama
            old_function_patterns = [
                r'# Global variable for display language\s*\nDISPLAY_LANG\s*=\s*"[a-z]+"[\s\S]*?def get_available_languages\(\):[\s\S]*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)\s*\n',
                r'def set_display_language\([^)]*\):[\s\S]*?Using English\."\s*\n',
                r'def t\([^)]*\):[\s\S]*?return key\s*\n',
                r'def get_display_language\([^)]*\):[\s\S]*?return DISPLAY_LANG\s*\n',
                r'def get_available_languages\([^)]*\):[\s\S]*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)\s*\n',
            ]
            
            cleaned_content = content
            for pattern in old_function_patterns:
                cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.DOTALL)
            
            # Cleanup empty lines
            cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
            
            # ✅ PERBAIKAN: BUAT SECTION DENGAN MULTIPLE BAHASA
            simple_section = f'''# ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------

DISPLAY_LANGUAGES = {{'''
            
            # Tambahkan setiap bahasa yang dipilih
            for i, lang_code in enumerate(selected_langs_sorted):
                lang_name = {
                    "en": "English", "pl": "Polski", "zh": "中文", "jp": "日本語",
                    "de": "Deutsch", "fr": "Français", "es": "Español", "ru": "Pycckuñ",
                    "pt": "Portugués", "id": "Indonesia", "kr": "한국어"
                }.get(lang_code, lang_code.upper())
                
                if i == 0:
                    simple_section += f'''
    "{lang_code}": {{
        # {lang_name} translations will be added here
    }}'''
                else:
                    simple_section += f''',
    "{lang_code}": {{
        # {lang_name} translations will be added here
    }}'''
            
            simple_section += f'''
}}

# Global variable for display language
DISPLAY_LANG = "{default_lang}"

def set_display_language(lang_code):
    """Set display language for notifications"""
    global DISPLAY_LANG
    if lang_code in DISPLAY_LANGUAGES:
        DISPLAY_LANG = lang_code
        print(f"✅ Display language set to: {{lang_code}}")
    else:
        print(f"❌ Language '{{lang_code}}' not supported. Using English.")

def t(key, **kwargs):
    """Translation function for notifications"""
    global DISPLAY_LANG
    try:
        if DISPLAY_LANG in DISPLAY_LANGUAGES and key in DISPLAY_LANGUAGES[DISPLAY_LANG]:
            return DISPLAY_LANGUAGES[DISPLAY_LANG][key].format(**kwargs)
        elif key in DISPLAY_LANGUAGES["{default_lang}"]:
            return DISPLAY_LANGUAGES["{default_lang}"][key].format(**kwargs)
        else:
            return key
    except Exception:
        return key

def get_display_language():
    """Get current display language"""
    return DISPLAY_LANG

def get_available_languages():
    """Get list of available languages"""
    return list(DISPLAY_LANGUAGES.keys())'''
            
            # ✅ PERBAIKAN BESAR: TEMUKAN POSISI YANG LEBIH CERDAS
            lines = cleaned_content.splitlines()
            insert_pos = find_best_insert_position(cleaned_content)
            
            print(f"📝 Inserting section at position: {insert_pos}")
            
            # Sisipkan section baru di posisi yang tepat
            if insert_pos > 0:
                # Sisipkan SETELAH header tapi SEBELUM import statements
                new_lines = lines[:insert_pos] + [""] + simple_section.splitlines() + [""] + lines[insert_pos:]
            else:
                # Jika tidak ditemukan posisi yang baik, sisipkan di awal
                new_lines = simple_section.splitlines() + [""] + lines
            
            new_content = "\n".join(new_lines)
            
            # Cleanup final - hapus baris kosong berlebihan
            new_content = re.sub(r'\n{3,}', '\n\n', new_content)
            
            # Tulis file baru
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Section generated successfully with {len(selected_langs_sorted)} languages!")
            print(f"📊 Languages: {', '.join(selected_langs_sorted)}")
            print(f"⭐ Default language: {default_lang}")
            print("✅ Old display functions removed and replaced")
            
            # Tampilkan preview hasil
            print("\n📋 GENERATED SECTION PREVIEW:")
            print("=" * 50)
            preview_lines = new_content.split('\n')[:25]  # Tampilkan 25 baris pertama
            for i, line in enumerate(preview_lines):
                print(f"{line}")
            print("=" * 50)
            
            return True
                
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
        elif command_name == "remove-lang":
            fallback_for_remove_lang(target_file)
        else:
            print(f"❌ Unknown command: {command_name}")
    else:
        print("❌ Usage: python fallback_strategy.py <command> <filename>")
        print("Available commands: add-lang, translate, repair, set-global-lang, remove-lang")