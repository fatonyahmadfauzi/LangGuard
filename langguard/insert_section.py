#!/usr/bin/env python3
"""
LangGuard - Insert Template and Add Languages (Modular Version)
"""

import os
import re
import sys

# ✅ IMPORT BARU - ganti import dari add_languages
try:
    from .language_selection import (
        select_languages_for_addition,
        select_default_language,
        show_language_selection,
        get_user_language_selection
    )
    from .add_languages import (
        add_languages_to_content,
        get_all_supported_languages,
        get_correct_language_order
    )
    from .repair_functions import run_repair_functions
except ImportError:
    # Untuk mode standalone
    from language_selection import (
        select_languages_for_addition,
        select_default_language,
        show_language_selection,
        get_user_language_selection
    )
    from add_languages import (
        add_languages_to_content,
        get_all_supported_languages,
        get_correct_language_order
    )
    from repair_functions import run_repair_functions


# ======================== BASIC CHECKS ========================

def check_display_section_exists(content):
    """Periksa apakah section DISPLAY_LANGUAGES lengkap"""
    required = [
        "DISPLAY_LANGUAGES = {",
        "DISPLAY_LANG = ",
        "def set_display_language",
        "def t(",
        "def get_display_language",
        "def get_available_languages"
    ]
    return all(part in content for part in required)


def get_existing_languages_list(content):
    """Ambil daftar bahasa yang sudah ada - SUPER ACCURATE VERSION"""
    langs = []
    
    # Cari section DISPLAY_LANGUAGES dengan pattern yang lebih spesifik
    start_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        return langs
    
    # Ekstrak seluruh dictionary content
    start_pos = start_match.start()
    brace_count = 0
    in_string = False
    escape_next = False
    dict_content = ""
    
    # Baca karakter demi karakter untuk menemukan akhir dictionary yang tepat
    for i in range(start_pos, len(content)):
        char = content[i]
        dict_content += char
        
        if escape_next:
            escape_next = False
            continue
            
        if char == '\\':
            escape_next = True
            continue
            
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
            
        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    break
    
    # Sekarang extract semua bahasa dari dict_content
    # Pattern: "en": { ... }
    lang_pattern = r'"([a-z]{2})":\s*\{'
    lang_matches = re.findall(lang_pattern, dict_content)
    
    return lang_matches


def create_complete_display_section():
    """Template lengkap DISPLAY_LANGUAGES section dengan urutan yang benar"""
    correct_order = get_correct_language_order()
    
    language_names = {
        "en": "English", "pl": "Polish", "zh": "Chinese", "jp": "Japanese",
        "de": "German", "fr": "French", "es": "Spanish", "ru": "Russian",
        "pt": "Portuguese", "id": "Indonesian", "kr": "Korean"
    }
    
    section = '''# ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------

DISPLAY_LANGUAGES = {'''
    
    for i, lang in enumerate(correct_order):
        lang_name = language_names.get(lang, lang.upper())
        if i == 0:
            section += f'''
    "{lang}": {{
        # {lang_name} translations will be added globally later
    }}'''
        else:
            section += f''',
    "{lang}": {{
        # {lang_name} translations will be added globally later
    }}'''
    
    section += '''
}

# Global variable for display language
DISPLAY_LANG = "en"

def set_display_language(lang_code):
    """Set display language for notifications"""
    global DISPLAY_LANG
    if lang_code in DISPLAY_LANGUAGES:
        DISPLAY_LANG = lang_code
        print(f"✅ Display language set to: {lang_code}")
    else:
        print(f"❌ Language '{lang_code}' not supported. Using English.")

def t(key, **kwargs):
    """Translation function for notifications"""
    global DISPLAY_LANG
    try:
        if DISPLAY_LANG in DISPLAY_LANGUAGES and key in DISPLAY_LANGUAGES[DISPLAY_LANG]:
            return DISPLAY_LANGUAGES[DISPLAY_LANG][key].format(**kwargs)
        elif key in DISPLAY_LANGUAGES["en"]:
            return DISPLAY_LANGUAGES["en"][key].format(**kwargs)
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
    
    return section


# ======================== INSERTION UTILS ========================

def find_best_insert_position(lines):
    """Cari posisi terbaik untuk menyisipkan section"""
    # Setelah import statements
    for i, line in enumerate(lines):
        if line.strip().startswith("import ") or line.strip().startswith("from "):
            for j in range(i + 1, len(lines)):
                if not (lines[j].strip().startswith("import ") or lines[j].strip().startswith("from ")):
                    return j
            return i + 1

    # Setelah docstring
    in_docstring = False
    for i, line in enumerate(lines):
        if line.strip().startswith(('"""', "'''")):
            if not in_docstring:
                in_docstring = True
            else:
                return i + 1

    # Setelah shebang
    if lines and lines[0].startswith("#!"):
        return 1

    return 0


def insert_section_at_correct_position(content, section):
    """Masukkan section DISPLAY_LANGUAGES ke posisi terbaik"""
    lines = content.splitlines()
    pos = find_best_insert_position(lines)
    new_lines = lines[:pos] + [""] + [""] + section.splitlines() + [""] + [""] + lines[pos:]
    return "\n".join(new_lines)


def fix_trailing_spacing(content):
    """Perbaiki spasi setelah bagian akhir fungsi bahasa"""
    pattern = r"(def get_available_languages\(\):.*?return list\(DISPLAY_LANGUAGES\.keys\(\)\))(\s*\n)*"
    return re.sub(pattern, r"\1\n\n", content, flags=re.DOTALL)


# ======================== GLOBAL LANGUAGE SELECTION ========================

def ask_global_language_selection(selected_languages):
    """Tanya user untuk memilih bahasa global dari bahasa yang dipilih - VERSI DIPERBAIKI"""
    
    # Jika hanya 1 bahasa yang dipilih, otomatis jadikan global language
    if len(selected_languages) == 1:
        lang_code = selected_languages[0]
        lang_name = {
            "en": "English", "pl": "Polish", "zh": "Chinese", "jp": "Japanese",
            "de": "German", "fr": "French", "es": "Spanish", "ru": "Russian",
            "pt": "Portuguese", "id": "Indonesian", "kr": "Korean"
        }.get(lang_code, lang_code.upper())
        print(f"🌍 Global language automatically set to: {lang_name} ({lang_code})")
        return lang_code
    
    # ✅ GUNAKAN FUNGSI TERPUSAT untuk pemilihan default language
    print(f"\n🌍 SELECT GLOBAL DISPLAY LANGUAGE:")
    print("💡 Note: This will be the default language for translations")
    
    default_lang = select_default_language(selected_languages, None)
    
    if default_lang:
        lang_name = {
            "en": "English", "pl": "Polish", "zh": "Chinese", "jp": "Japanese",
            "de": "German", "fr": "French", "es": "Spanish", "ru": "Russian",
            "pt": "Portuguese", "id": "Indonesian", "kr": "Korean"
        }.get(default_lang, default_lang.upper())
        print(f"✅ Global language set to: {lang_name} ({default_lang})")
        return default_lang
    else:
        print("❌ No default language selected. Using 'en' as fallback.")
        return "en"


# ======================== MAIN PROCESS - ULTRA SIMPLE VERSION ========================

def run_insert_section(target_file):
    """Fungsi utama untuk mengelola DISPLAY_LANGUAGES - DENGAN OPSI TAMBAH BAHASA"""
    if not os.path.exists(target_file):
        print(f"❌ File {target_file} not found.")
        return

    print(f"🎯 Target: {target_file}")
    print("=" * 60)

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    backup = target_file + ".insert_backup"
    with open(backup, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📁 Backup created: {backup}")

    print("\n🔍 Checking DISPLAY LANGUAGE section...")
    
    # ✅ CEK SANGAT SEDERHANA: Apakah DISPLAY_LANGUAGES ada?
    has_display_languages = 'DISPLAY_LANGUAGES = {' in content
    
    if not has_display_languages:
        print("❌ DISPLAY_LANGUAGES section not found.")
        
        # ✅ BUAT SECTION BARU - tampilkan semua bahasa
        print("\n🎯 Creating new DISPLAY_LANGUAGES section...")
        
        # ✅ GUNAKAN FUNGSI TERPUSAT
        selected_langs = select_languages_for_addition()
        
        if not selected_langs:
            print("❌ No languages selected. Operation cancelled.")
            return
        
        # Tanya user untuk memilih global language
        global_lang = ask_global_language_selection(selected_langs)
        
        # Buat section dengan global language yang dipilih
        section = create_custom_display_section(selected_langs, global_lang)
        content = insert_section_at_correct_position(content, section)
        content = fix_trailing_spacing(content)
        
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✅ New DISPLAY_LANGUAGES section created with {len(selected_langs)} languages!")
        print(f"📊 Languages added: {', '.join(selected_langs)}")
        print(f"🌍 Global language: {global_lang}")
        return
    
    # ✅ JIKA SUDAH ADA - TAMPILKAN INFO DAN TANYAKAN APAKAH INGIN MENAMBAH BAHASA
    print("✅ DISPLAY_LANGUAGES section already exists!")
    
    # Hitung bahasa dengan cara SANGAT akurat
    existing_langs = get_existing_languages_list(content)
    all_supported = get_all_supported_languages()
    
    print(f"📊 Found {len(existing_langs)} languages: {', '.join(existing_langs)}")
    
    # Cek apakah ada bahasa yang missing
    missing_langs = [lang for lang in all_supported if lang not in existing_langs]
    
    if missing_langs:
        print(f"💡 Note: {len(missing_langs)} languages missing: {', '.join(missing_langs)}")
        
        # ✅ TANYAKAN USER APAKAH INGIN MENAMBAH BAHASA YANG MISSING
        add_missing = input("\n👉 Do you want to add the missing languages? (y/N): ").strip().lower()
        
        if add_missing == 'y':
            # ✅ GUNAKAN FUNGSI TERPUSAT untuk missing languages
            show_language_selection(available_langs=missing_langs, context="add")
            selected_langs = get_user_language_selection(available_langs=missing_langs, allow_multiple=True, context="add")
            
            if selected_langs:
                content = add_languages_to_content(content, selected_langs)
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Added {len(selected_langs)} languages successfully!")
                print(f"📊 Languages added: {', '.join(selected_langs)}")
            else:
                print("ℹ️ No languages selected.")
        else:
            print("ℹ️ No languages added.")
    else:
        print("🎉 All supported languages already exist!")
        print("✅ No changes needed.")

    print(f"\n✅ Operation completed!")
    print(f"💾 Backup: {backup}")


def create_custom_display_section(selected_languages, global_lang="en"):
    """Buat DISPLAY_LANGUAGES section dengan bahasa yang dipilih user dan global language"""
    
    language_names = {
        "en": "English", "pl": "Polish", "zh": "Chinese", "jp": "Japanese",
        "de": "German", "fr": "French", "es": "Spanish", "ru": "Russian",
        "pt": "Portuguese", "id": "Indonesian", "kr": "Korean"
    }
    
    # Urutkan selected_languages sesuai urutan standar
    correct_order = get_correct_language_order()
    sorted_languages = [lang for lang in correct_order if lang in selected_languages]
    
    section = f'''# ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------

DISPLAY_LANGUAGES = {{'''
    
    for i, lang in enumerate(sorted_languages):
        lang_name = language_names.get(lang, lang.upper())
        if i == 0:
            section += f'''
    "{lang}": {{
        # {lang_name} translations will be added here
    }}'''
        else:
            section += f''',
    "{lang}": {{
        # {lang_name} translations will be added here
    }}'''
    
    section += f'''
}}

# Global variable for display language
DISPLAY_LANG = "{global_lang}"

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
        elif key in DISPLAY_LANGUAGES["{global_lang}"]:
            return DISPLAY_LANGUAGES["{global_lang}"][key].format(**kwargs)
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
    
    return section


# ======================== ALTERNATIVE FLOW (FOR REPAIR MODE) ========================

def run_insert_section_alternative(target_file):
    """Alternative flow dengan repair option jika section rusak"""
    if not os.path.exists(target_file):
        print(f"❌ File {target_file} not found.")
        return

    print(f"🎯 Target: {target_file}")
    print("=" * 60)

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    backup = target_file + ".insert_backup"
    with open(backup, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📁 Backup created: {backup}")

    print("\n🔍 Checking DISPLAY LANGUAGE section...")
    section_ok = check_display_section_exists(content)

    # Jika section rusak atau tidak lengkap
    if not section_ok:
        print("⚠️ DISPLAY LANGUAGE section missing or incomplete.")
        repair_choice = input("Do you want to run repair mode? (y/N): ").strip().lower()
        if repair_choice == "y":
            run_repair_functions(target_file)
            return
        else:
            create_choice = input("Do you want to create a new complete section? (y/N): ").strip().lower()
            if create_choice == "y":
                # ✅ GUNAKAN FUNGSI TERPUSAT
                selected_langs = select_languages_for_addition()
                
                if not selected_langs:
                    print("❌ No languages selected. Operation cancelled.")
                    return
                
                # Tanya user untuk memilih global language
                global_lang = ask_global_language_selection(selected_langs)
                
                section = create_custom_display_section(selected_langs, global_lang)
                content = insert_section_at_correct_position(content, section)
                content = fix_trailing_spacing(content)
                
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(content)
                    
                print(f"✅ New DISPLAY_LANGUAGES section created with {len(selected_langs)} languages!")
                print(f"📊 Languages added: {', '.join(selected_langs)}")
                print(f"🌍 Global language: {global_lang}")
                return
            else:
                print("❌ Operation cancelled.")
                return

    # Jika section sudah ada dan lengkap
    print("✅ DISPLAY LANGUAGE section detected and complete.")
    
    # Hitung bahasa yang ada
    existing_langs = get_existing_languages_list(content)
    count_existing = len(existing_langs)
    print(f"📊 Found {count_existing} languages: {', '.join(existing_langs)}")

    total_langs = len(get_all_supported_languages())

    # Jika sudah lengkap
    if count_existing == total_langs:
        print("🎉 All languages already complete!")
        print("✅ No changes needed.")
        return

    # Jika belum lengkap → tawarkan untuk menambah
    missing = [l for l in get_all_supported_languages() if l not in existing_langs]
    print(f"\n⚠️ Missing {len(missing)} languages: {', '.join(missing)}")
    add_choice = input("Do you want to add the missing languages? (y/N): ").strip().lower()

    if add_choice == "y":
        # ✅ GUNAKAN FUNGSI TERPUSAT untuk missing languages
        show_language_selection(available_langs=missing, context="add")
        selected = get_user_language_selection(available_langs=missing, allow_multiple=True, context="add")
        if selected:
            content = add_languages_to_content(content, selected)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)
            print("✅ Languages added successfully!")
            print(f"📊 Added languages: {', '.join(selected)}")
        else:
            print("ℹ️ No languages selected.")
    else:
        print("ℹ️ No languages added.")

    print(f"\n✅ Operation completed!")
    print(f"💾 Backup: {backup}")


# ======================== CLI MODE ========================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a target file.")
        print("Usage: python insert_section.py <filename>")
        sys.exit(1)
    
    run_insert_section(sys.argv[1])