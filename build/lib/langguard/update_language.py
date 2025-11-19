#!/usr/bin/env python3
import re
import os
import sys

# ✅ IMPORT BARU - tambahkan language_selection
try:
    from .language_selection import select_default_language
except ImportError:
    from language_selection import select_default_language

LANGUAGES = {
    "en": "English",
    "pl": "Polski",
    "zh": "中文",
    "jp": "日本語",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "ru": "Pycckuñ",
    "pt": "Portugués",
    "id": "Indonesia",
    "kr": "한국어"
}

def get_all_supported_languages():
    """Dapatkan semua bahasa yang didukung"""
    return list(LANGUAGES.keys())

def get_available_languages_from_file(file_path):
    """Ambil daftar bahasa yang ada di DISPLAY_LANGUAGES dictionary"""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Cari section DISPLAY_LANGUAGES
    start_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        return []

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

    # Extract semua bahasa dari dict_content
    lang_pattern = r'"([a-z]{2})":\s*\{'
    available_langs = re.findall(lang_pattern, dict_content)
    
    return available_langs

def get_current_display_language(file_path):
    """Dapatkan bahasa default yang sedang aktif di file"""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    display_match = re.search(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', content)
    return display_match.group(1) if display_match else None

def check_functions_exist(content):
    """Cek apakah semua fungsi yang diperlukan ada dan lengkap"""
    required_functions = [
        'DISPLAY_LANG =',
        'def set_display_language(',
        'def t(',
        'def get_display_language(',
        'def get_available_languages('
    ]
    
    missing_functions = []
    for func in required_functions:
        if func not in content:
            missing_functions.append(func)
    
    return missing_functions

def are_functions_complete(content):
    """Cek apakah semua fungsi sudah lengkap (tidak ada yang missing)"""
    return len(check_functions_exist(content)) == 0

def ask_repair_functions(file_path):
    """Tanya user apakah ingin melakukan repair fungsi"""
    print("\n⚠️  Required functions are missing or incomplete!")
    print("💡 The following functions are required for set-global-lang to work:")
    print("   - DISPLAY_LANG =")
    print("   - def set_display_language()")
    print("   - def t()") 
    print("   - def get_display_language()")
    print("   - def get_available_languages()")
    
    while True:
        choice = input("\n👉 Do you want to repair the functions automatically? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🎯 Repairing functions...")
            try:
                from repair_functions import run_repair_functions
                success = run_repair_functions(file_path)
                if success:
                    print("✅ Functions repaired successfully!")
                    return True
                else:
                    print("❌ Failed to repair functions")
                    return False
            except ImportError:
                try:
                    from .repair_functions import run_repair_functions
                    success = run_repair_functions(file_path)
                    if success:
                        print("✅ Functions repaired successfully!")
                        return True
                    else:
                        print("❌ Failed to repair functions")
                        return False
                except ImportError:
                    print("❌ Cannot import repair_functions module")
                    return False
        elif choice in ['n', 'no', '']:
            print("ℹ️ Repair skipped. set-global-lang cannot proceed without functions.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

def ensure_functions_exist(file_path):
    """Pastikan semua fungsi yang diperlukan ada sebelum melanjutkan"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    missing_functions = check_functions_exist(content)
    if missing_functions:
        print(f"❌ Missing required functions: {', '.join(missing_functions)}")
        return ask_repair_functions(file_path)
    
    return True

def set_default_display_language_in_file(file_path, lang_code):
    """Ganti nilai default DISPLAY_LANG dan fallback language di file eksternal."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Cek apakah bahasa yang dipilih ada di DISPLAY_LANGUAGES
    available_langs = get_available_languages_from_file(file_path)
    
    if lang_code not in available_langs:
        print(f"❌ Language '{lang_code}' not found in DISPLAY_LANGUAGES")
        print(f"📋 Available languages: {', '.join(available_langs)}")
        return False

    # Dapatkan bahasa default saat ini
    current_display_lang = get_current_display_language(file_path)
    
    # ✅ PERBAIKAN: Jika bahasa yang dipilih sama dengan yang sudah aktif, tidak perlu perubahan
    if current_display_lang == lang_code:
        print(f"ℹ️ Language '{lang_code}' is already the current default. No changes needed.")
        return True

    # Backup file - HANYA jika ada perubahan
    backup = file_path + ".lang_backup"
    with open(backup, "w", encoding="utf-8") as f:
        f.write(content)

    changes_made = False

    # 1. Ubah DISPLAY_LANG value
    new_content, count_display = re.subn(
        r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']',
        f'DISPLAY_LANG = "{lang_code}"',
        content
    )

    if count_display > 0:
        changes_made = True
        print(f"✅ DISPLAY_LANG changed to '{lang_code}'")

    # 2. Ubah semua fallback language patterns di fungsi t()
    fallback_patterns = [
        # Pattern 1: elif key in DISPLAY_LANGUAGES["en"]:
        (r'elif key in DISPLAY_LANGUAGES\["([a-z]{2})"\]', 
         f'elif key in DISPLAY_LANGUAGES["{lang_code}"]'),
        
        # Pattern 2: DISPLAY_LANGUAGES["en"][key].format
        (r'DISPLAY_LANGUAGES\["([a-z]{2})"\]\[key\]\.format',
         f'DISPLAY_LANGUAGES["{lang_code}"][key].format'),
        
        # Pattern 3: return DISPLAY_LANGUAGES["en"][key].format(**kwargs)
        (r'return DISPLAY_LANGUAGES\["([a-z]{2})"\]\[key\]\.format\(\*\*kwargs\)',
         f'return DISPLAY_LANGUAGES["{lang_code}"][key].format(**kwargs)'),
        
        # Pattern 4: DISPLAY_LANGUAGES.get("en", {}).get(key)
        (r'DISPLAY_LANGUAGES\.get\("([a-z]{2})", \{\}\)\.get\(key\)',
         f'DISPLAY_LANGUAGES.get("{lang_code}", {{}}).get(key)'),
        
        # Pattern 5: in DISPLAY_LANGUAGES["en"]
        (r'in DISPLAY_LANGUAGES\["([a-z]{2})"\]',
         f'in DISPLAY_LANGUAGES["{lang_code}"]')
    ]

    for pattern, replacement in fallback_patterns:
        matches = re.findall(pattern, new_content)
        if matches:
            current_fallback = matches[0]
            if current_fallback != lang_code:
                if current_fallback in available_langs:
                    new_content, count_fallback = re.subn(
                        pattern,
                        replacement,
                        new_content
                    )
                    if count_fallback > 0:
                        changes_made = True
                        print(f"✅ Fallback language changed from '{current_fallback}' to '{lang_code}'")
                else:
                    print(f"⚠️ Previous fallback language '{current_fallback}' not in available languages, updating to '{lang_code}'")
                    new_content, count_fallback = re.subn(
                        pattern,
                        replacement,
                        new_content
                    )
                    if count_fallback > 0:
                        changes_made = True
                        print(f"✅ Fallback language set to '{lang_code}'")

    # 3. Cari dan ganti semua instance fallback language yang spesifik
    specific_fallback_patterns = [
        # Pattern untuk: elif key in DISPLAY_LANGUAGES["id"]:
        r'(elif key in DISPLAY_LANGUAGES\[")([a-z]{2})("\])',
        # Pattern untuk: return DISPLAY_LANGUAGES["kr"][key].format(**kwargs)
        r'(return DISPLAY_LANGUAGES\[")([a-z]{2})("\]\[key\]\.format\(\*\*kwargs\))',
        # Pattern untuk: DISPLAY_LANGUAGES["jp"][key].format
        r'(DISPLAY_LANGUAGES\[")([a-z]{2})("\]\[key\]\.format)',
    ]

    for pattern in specific_fallback_patterns:
        matches = re.finditer(pattern, new_content)
        for match in matches:
            full_match = match.group(0)
            current_lang = match.group(2)
            if current_lang in available_langs and current_lang != lang_code:
                new_fallback = match.group(1) + lang_code + match.group(3)
                new_content = new_content.replace(full_match, new_fallback)
                changes_made = True
                print(f"✅ Specific fallback changed: '{current_lang}' → '{lang_code}'")

    if not changes_made:
        print("❌ No changes were made. DISPLAY_LANG assignment not found.")
        # Hapus backup karena tidak ada perubahan
        if os.path.exists(backup):
            os.remove(backup)
        return False

    # Simpan file baru
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Default display language changed to '{lang_code}' in {file_path}")
    print(f"📁 Backup saved: {backup}")
    return True

def show_current_language(file_path, available_langs=None):
    """Tampilkan bahasa yang sedang aktif di file."""
    if not os.path.exists(file_path):
        return None, None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Cari DISPLAY_LANG value
    display_match = re.search(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', content)
    current_display = display_match.group(1) if display_match else None

    # Cari semua fallback language patterns
    fallback_patterns = [
        r'elif key in DISPLAY_LANGUAGES\["([a-z]{2})"\]',
        r'DISPLAY_LANGUAGES\["([a-z]{2})"\]\[key\]\.format',
        r'return DISPLAY_LANGUAGES\["([a-z]{2})"\]\[key\]\.format\(\*\*kwargs\)',
        r'DISPLAY_LANGUAGES\.get\("([a-z]{2})", \{\}\)\.get\(key\)',
        r'in DISPLAY_LANGUAGES\["([a-z]{2})"\]'
    ]

    current_fallbacks = []
    for pattern in fallback_patterns:
        matches = re.findall(pattern, content)
        current_fallbacks.extend(matches)

    # Ambil fallback yang unik
    current_fallbacks = list(set(current_fallbacks))
    current_fallback = current_fallbacks[0] if current_fallbacks else None

    # Validasi bahasa yang ditemukan jika available_langs diberikan
    if available_langs:
        if current_display and current_display not in available_langs:
            print(f"⚠️ Current display language '{current_display}' not in available languages")
            current_display = None
            
        if current_fallback and current_fallback not in available_langs:
            print(f"⚠️ Current fallback language '{current_fallback}' not in available languages")
            current_fallback = None

    return current_display, current_fallback

def run_add_languages(target_file):
    """Jalankan proses penambahan bahasa - DENGAN AUTO-GENERATE"""
    try:
        from add_languages import run_add_languages as run_add_langs_module
    except ImportError:
        try:
            from .add_languages import run_add_languages as run_add_langs_module
        except ImportError:
            print("❌ Cannot import add_languages module")
            return False

    # Jalankan fungsi add_languages yang sudah memiliki auto-generate
    run_add_langs_module(target_file)
    return True

def run_set_global_lang(file_path):
    """Fungsi utama untuk set-global-lang command - DENGAN FALLBACK STRATEGY YANG BENAR"""
    # ✅ GUNAKAN FALLBACK STRATEGY YANG BARU
    try:
        from .fallback_strategy import fallback_for_set_global_lang
    except ImportError:
        from fallback_strategy import fallback_for_set_global_lang
    
    # Cek section dan generate jika perlu
    if not fallback_for_set_global_lang(file_path):
        return False  # File tidak ada atau user cancel
    
    # Lanjut proses set-global-lang normal (section sudah ada)
    print("🔄 Continuing with set-global-lang process...")
    
    # Dapatkan bahasa yang tersedia SETELAH section mungkin digenerate
    available_langs = get_available_languages_from_file(file_path)
    
    # Jika setelah generate section masih tidak ada bahasa yang tersedia, batalkan operasi
    if not available_langs:
        print("❌ No languages available in DISPLAY_LANGUAGES section. Operation cancelled.")
        return
    
    # ✅ PERBAIKAN BARU: Cek fungsi SEBELUM menampilkan info bahasa
    repair_performed = False
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    missing_functions = check_functions_exist(content)
    if missing_functions:
        print(f"❌ Missing required functions: {', '.join(missing_functions)}")
        if ask_repair_functions(file_path):
            repair_performed = True
            # Baca ulang konten setelah repair
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            return  # Batalkan jika user tidak ingin repair
    
    # ✅ PERBAIKAN BARU: Hanya tampilkan pesan "completed" jika repair dilakukan
    if repair_performed and are_functions_complete(content):
        print("✅ Functions are now complete after repair!")
        
        # Tampilkan status bahasa saat ini
        current_display, current_fallback = show_current_language(file_path, available_langs)
        if current_display:
            print(f"🔍 Current display language: {current_display}")
        if current_fallback:
            print(f"🔍 Current fallback language: {current_fallback}")
        
        print("\n🎯 set-global-lang operation completed successfully!")
        print("💡 The display language functions have been repaired and are now ready to use.")
        print("📋 If you want to change the display language, run this command again.")
        return
    
    # ✅ Jika tidak ada repair yang dilakukan, lanjutkan proses normal
    # ✅ PERBAIKAN: Cek apakah semua bahasa sudah lengkap
    all_supported_langs = set(get_all_supported_languages())
    current_available_langs = set(available_langs)
    all_languages_complete = (current_available_langs == all_supported_langs)
    
    # Hanya tampilkan info ini jika ada bahasa yang tersedia
    print(f"📋 Available languages in file: {', '.join(available_langs)}")
    
    if all_languages_complete:
        print("🎉 All supported languages are available!")
    
    # Tampilkan bahasa saat ini
    current_display, current_fallback = show_current_language(file_path, available_langs)
    if current_display:
        print(f"🔍 Current display language: {current_display}")
    if current_fallback:
        print(f"🔍 Current fallback language: {current_fallback}")

    # ✅ GUNAKAN FUNGSI TERPUSAT untuk pemilihan bahasa default
    current_default = get_current_display_language(file_path)
    lang = select_default_language(available_langs, current_default)

    if not lang:
        # ✅ PERBAIKAN: Jika lang adalah None, ini berarti:
        # - User memilih 'S' (skip), ATAU
        # - User memilih bahasa yang sudah default
        # Dalam kedua kasus, operasi dibatalkan dengan pesan yang sesuai
        print("ℹ️ Operation completed with no changes.")
        return
    
    # Jika user memilih untuk menambah bahasa
    if lang == "add_languages":
        print("\n🎯 Adding new languages...")
        if run_add_languages(file_path):
            # Setelah menambah bahasa, tanya lagi untuk set global language
            print("\n🔄 Now let's set the global language...")
            available_langs = get_available_languages_from_file(file_path)
            current_default = get_current_display_language(file_path)
            lang = select_default_language(available_langs, current_default)
            
            if lang and lang != "add_languages":
                set_default_display_language_in_file(file_path, lang)
            else:
                print("⏭️ Global language setting skipped.")
        else:
            print("❌ Failed to add languages.")
    else:
        # Set global language biasa
        set_default_display_language_in_file(file_path, lang)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a target file.")
        print("Usage: python update_language.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    run_set_global_lang(file_path)