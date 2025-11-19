#!/usr/bin/env python3
"""
LangGuard - Repair Functions Only (WITH SECTION FALLBACK)
DENGAN LOGIKA CERDAS UNTUK KONFLIK BAHASA - VERSI DIPERBAIKI
"""

import os
import sys
import re

# ==================== FUNGSI UTAMA YANG DIPERLUKAN ====================

def check_display_section_exists(content):
    """Cek apakah DISPLAY_LANGUAGES section ada dan valid"""
    return 'DISPLAY_LANGUAGES = {' in content

def get_existing_languages_from_content(content):
    """Ambil daftar bahasa yang ada di DISPLAY_LANGUAGES dari content"""
    langs = []
    
    start_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        return langs
    
    start_pos = start_match.start()
    brace_count = 0
    in_string = False
    escape_next = False
    dict_content = ""
    
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
    
    lang_pattern = r'"([a-z]{2})":\s*\{'
    lang_matches = re.findall(lang_pattern, dict_content)
    
    return lang_matches

def get_existing_languages_from_file(file_path):
    """Ambil daftar bahasa yang ada di DISPLAY_LANGUAGES dari file"""
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return get_existing_languages_from_content(content)
    except Exception:
        return []

def detect_language_conflicts(content):
    """Deteksi konflik bahasa - VERSI LEBIH AKURAT"""
    print("🔍 Detecting language conflicts...")
    
    # Cari semua instance DISPLAY_LANG
    display_lang_matches = re.findall(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', content)
    
    if len(display_lang_matches) <= 1:
        print("✅ No language conflicts detected")
        return None
    
    # Filter hanya yang unik
    unique_langs = list(set(display_lang_matches))
    
    if len(unique_langs) <= 1:
        print("✅ No actual conflicts (only one unique language)")
        return None
    
    print(f"⚠️  Found {len(unique_langs)} conflicting languages: {', '.join(unique_langs)}")
    
    # Strategi: Prioritaskan bahasa yang ada di DISPLAY_LANGUAGES
    existing_langs = get_existing_languages_from_content(content)
    if existing_langs:
        for lang in unique_langs:
            if lang in existing_langs:
                print(f"🎯 Prioritizing '{lang}' (exists in DISPLAY_LANGUAGES)")
                return lang
    
    # Fallback: ambil yang pertama
    first_lang = unique_langs[0]
    print(f"🎯 Using first found language: '{first_lang}'")
    return first_lang

def get_default_language_from_fallback(file_path):
    """Dapatkan default language yang dipilih user dari fallback process"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cari DISPLAY_LANG yang aktif
        lang_match = re.search(r'DISPLAY_LANG\s*=\s*"([a-z]+)"', content)
        if lang_match:
            return lang_match.group(1)
        
        return None
    except Exception:
        return None

def fix_language_order_in_content(content):
    """Perbaiki urutan bahasa dalam content - INTEGRASI DARI fix_order.py"""
    print("🔧 Fixing language order...")
    
    try:
        # ✅ GUNAKAN language_utils untuk urutan yang benar
        try:
            from .language_utils import get_correct_language_order
        except ImportError:
            from language_utils import get_correct_language_order
        
        correct_order = get_correct_language_order()
        
        # Cari section DISPLAY_LANGUAGES
        start_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
        start_match = re.search(start_pattern, content)
        
        if not start_match:
            print("❌ DISPLAY_LANGUAGES section tidak ditemukan")
            return content
        
        # Temukan awal dan akhir dari dictionary DISPLAY_LANGUAGES
        start_pos = start_match.start()
        
        # Cari penutup dictionary yang sesuai
        brace_count = 0
        in_string = False
        escape_next = False
        end_pos = -1
        
        for i in range(start_pos, len(content)):
            char = content[i]
            
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
                        end_pos = i + 1
                        break
        
        if end_pos == -1:
            print("❌ Tidak dapat menemukan akhir dari DISPLAY_LANGUAGES")
            return content
        
        # Ekstrak seluruh dictionary
        dict_content = content[start_pos:end_pos]
        
        # Ekstrak semua bahasa dengan content lengkap
        lang_pattern = r'"([a-z]{2})":\s*(\{[^}]*\})(?=,\s*"|\s*\})'
        lang_matches = list(re.finditer(lang_pattern, dict_content, re.DOTALL))
        
        if not lang_matches:
            print("❌ Tidak ada bahasa yang ditemukan dalam DISPLAY_LANGUAGES")
            return content
        
        # Kumpulkan semua bahasa yang ada
        all_langs = {}
        for match in lang_matches:
            lang_code = match.group(1)
            lang_dict = match.group(2)
            all_langs[lang_code] = lang_dict
        
        print(f"📋 Languages found: {', '.join(all_langs.keys())}")
        
        # Bangun ulang dictionary dengan urutan yang benar
        new_dict_content = 'DISPLAY_LANGUAGES = {\n'
        
        added_langs = []
        for lang_code in correct_order:
            if lang_code in all_langs:
                if added_langs:  # Jika bukan bahasa pertama, tambahkan koma
                    new_dict_content += ',\n'
                new_dict_content += f'    "{lang_code}": {all_langs[lang_code]}'
                added_langs.append(lang_code)
        
        # Tambahkan bahasa yang tidak ada di correct_order (jika ada)
        for lang_code in all_langs:
            if lang_code not in added_langs:
                if added_langs:  # Jika bukan bahasa pertama, tambahkan koma
                    new_dict_content += ',\n'
                new_dict_content += f'    "{lang_code}": {all_langs[lang_code]}'
                added_langs.append(lang_code)
        
        new_dict_content += '\n}'
        
        # Ganti bagian lama dengan yang baru
        new_content = content[:start_pos] + new_dict_content + content[end_pos:]
        
        print(f"✅ Language order fixed: {', '.join(added_langs)}")
        return new_content
        
    except Exception as e:
        print(f"❌ Error fixing language order: {e}")
        return content

def remove_duplicate_functions(content, preferred_lang=None):
    """Hapus fungsi dan variabel yang duplikat - VERSI DIPERBAIKI"""
    print("🔧 Removing duplicate functions and variables...")
    
    if preferred_lang:
        print(f"🎯 Using preferred language: {preferred_lang}")
    
    # 1. DETEKSI SEMUA BLOK FUNGSI DISPLAY LANGUAGE DENGAN MULTIPLE PATTERNS
    function_blocks = []
    
    # Pattern untuk mendeteksi awal blok fungsi - LEBIH FLEKSIBEL
    start_patterns = [
        r'# Global variable for display language\s*\nDISPLAY_LANG\s*=\s*"[a-z]+"',
        r'# 🌐 Display Language Control\s*\nDISPLAY_LANG\s*=\s*"[a-z]+"',
        r'DISPLAY_LANG\s*=\s*"[a-z]+"\s*\n\s*def set_display_language',
        r'# -+\s*DISPLAY LANGUAGE SETTINGS\s*-+'
    ]
    
    for start_pattern in start_patterns:
        start_matches = list(re.finditer(start_pattern, content, re.DOTALL))
        for start_match in start_matches:
            start_pos = start_match.start()
            
            # Cari akhir dari blok fungsi (akhir get_available_languages)
            end_pattern = r'def get_available_languages\(\):.*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)'
            end_match = re.search(end_pattern, content[start_pos:], re.DOTALL)
            
            if end_match:
                end_pos = start_pos + end_match.end()
                function_blocks.append((start_pos, end_pos))
    
    # 2. JIKA ADA DUPLIKAT, PERTAHANKAN HANYA SATU
    if len(function_blocks) > 1:
        print(f"⚠️  Found {len(function_blocks)} duplicate function blocks")
        
        # Urutkan berdasarkan posisi
        function_blocks.sort()
        
        # PERTAHANKAN HANYA BLOK PERTAMA, HAPUS SISANYA
        kept_block = function_blocks[0]
        blocks_to_remove = function_blocks[1:]
        
        # Mulai dengan konten sebelum blok pertama
        cleaned_content = content[:kept_block[0]]
        
        # Tambahkan blok yang dipertahankan
        cleaned_content += content[kept_block[0]:kept_block[1]]
        
        # Tambahkan konten setelah blok terakhir yang dihapus
        last_removed_end = blocks_to_remove[-1][1]
        cleaned_content += content[last_removed_end:]
        
        print(f"✅ Kept 1 function block, removed {len(blocks_to_remove)} duplicates")
        
        # 3. HAPUS JUGA DISPLAY_LANG VARIABLE YANG TERISOLASI
        cleaned_content = remove_isolated_display_lang(cleaned_content, preferred_lang)
        
        return cleaned_content
    
    print("✅ No duplicate function blocks found")
    
    # Tetap bersihkan DISPLAY_LANG yang terisolasi meski tidak ada duplikat blok
    content = remove_isolated_display_lang(content, preferred_lang)
    return content

def remove_isolated_display_lang(content, preferred_lang):
    """Hapus DISPLAY_LANG variables yang terisolasi di luar blok fungsi"""
    print("🔧 Cleaning isolated DISPLAY_LANG variables...")
    
    # Pattern untuk menemukan DISPLAY_LANG yang terisolasi
    isolated_pattern = r'^\s*DISPLAY_LANG\s*=\s*"[a-z]+"\s*$'
    
    lines = content.splitlines()
    cleaned_lines = []
    in_function_block = False
    display_lang_count = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Deteksi awal blok fungsi
        if (stripped.startswith('def ') or 
            stripped.startswith('# -') or 
            'DISPLAY_LANGUAGES' in stripped):
            in_function_block = True
        elif stripped == '' and in_function_block:
            in_function_block = False
        
        # Jika ini adalah DISPLAY_LANG line
        if re.match(isolated_pattern, stripped):
            display_lang_count += 1
            
            # Pertahankan hanya yang pertama atau sesuai preferred_lang
            if display_lang_count == 1:
                if preferred_lang:
                    # Update dengan bahasa yang dipilih
                    cleaned_lines.append(f'DISPLAY_LANG = "{preferred_lang}"')
                else:
                    cleaned_lines.append(line)
                print(f"✅ Kept DISPLAY_LANG: {stripped}")
            else:
                print(f"🗑️  Removed duplicate DISPLAY_LANG: {stripped}")
                continue
        else:
            cleaned_lines.append(line)
    
    if display_lang_count > 1:
        print(f"✅ Removed {display_lang_count - 1} isolated DISPLAY_LANG variables")
    
    return '\n'.join(cleaned_lines)

def repair_braces_and_content(content):
    """
    💎 Ultra-Final Repair (Strict Safe Mode)
    """
    print("🔧 Running ULTRA-FINAL repair (strict safe mode)...")

    if not check_display_section_exists(content):
        print("❌ DISPLAY_LANGUAGES section not found. Cannot repair content.")
        return content

    # Ambil isi dictionary
    match = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{([\s\S]*?)\n\}', content)
    if not match:
        print("❌ DISPLAY_LANGUAGES content not found.")
        return content

    inner = match.group(1)
    lines = inner.splitlines()
    fixed = []
    open_quote = False
    last_lang = None

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            continue

        # Komentar
        if stripped.startswith("#"):
            fixed.append("    " + stripped)
            continue

        # Awal bahasa, contoh: "en": {
        lang_match = re.match(r'"([a-z]{2})"\s*:?\s*\{?', stripped)
        if lang_match:
            lang = lang_match.group(1)
            if fixed and not fixed[-1].strip().endswith(","):
                fixed[-1] = fixed[-1].rstrip(",") + ","
            fixed.append(f'    "{lang}": {{')
            last_lang = lang
            continue

        # Tutup bahasa
        if stripped in ["}", "},"]:
            fixed.append("    },")
            continue

        # Baris valid: "key": "value",
        kv = re.match(r'"([^"]+)"\s*:\s*"([^"]*)"?', stripped)
        if kv:
            key = kv.group(1).strip()
            val = kv.group(2).strip()
            if not stripped.endswith(","):
                fixed.append(f'        "{key}": "{val}",')
            else:
                fixed.append(f'        "{key}": "{val}",')
            continue

        # Baris rusak (hilang ':' atau tanda kutip)
        if '"' in stripped and ":" not in stripped:
            parts = stripped.split('"')
            if len(parts) >= 3:
                key = parts[1]
                after = stripped.split('"', 2)[-1].strip().lstrip(":").lstrip()
                if not after.startswith('"'):
                    after = f'"{after}'
                if not after.endswith('"') and not after.endswith('",'):
                    after = after + '"'
                fixed.append(f'        "{key}": {after},')
                continue

        # Jika ada ":" tapi tanda kutip rusak
        if ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip().strip('"')
            val = val.strip()
            if not val.startswith('"'):
                val = f'"{val}'
            if not val.endswith('"') and not val.endswith('",'):
                val += '"'
            fixed.append(f'        "{key}": {val},')
            continue

        # Baris lain: simpan mentah dengan indentasi aman
        fixed.append("        " + stripped)

    # --- Cleanup commas and spacing ---
    new_inner = "\n".join(fixed)

    # Hilangkan koma ganda (,,)
    new_inner = re.sub(r',\s*,', ',', new_inner)

    # Perbaiki koma antar bahasa
    new_inner = re.sub(r'\}\s*\n\s*"([a-z]{2})"', r'},\n    "\1"', new_inner)

    # Hapus koma terakhir sebelum penutup blok bahasa
    new_inner = re.sub(r',\s*\n\s*    \}', '\n    }', new_inner)

    # Hapus koma terakhir sebelum penutup dictionary utama
    new_inner = re.sub(r',\s*\n\s*\}', '\n}', new_inner)

    # Hilangkan koma terakhir di akhir dictionary utama
    new_inner = re.sub(r',\s*\n\}', '\n}', new_inner)
    new_inner = re.sub(r',\s*\Z', '', new_inner)

    # Rebuild dictionary
    rebuilt = f"DISPLAY_LANGUAGES = {{\n{new_inner}\n}}"

    new_content = re.sub(
        r'DISPLAY_LANGUAGES\s*=\s*\{[\s\S]*?\n\}',
        rebuilt,
        content,
    )

    print("✅ Content repair complete — structure and values restored cleanly.")
    return new_content

def repair_function_t_directly(content, default_lang="en"):
    """Perbaiki fungsi t() secara langsung dan sederhana"""
    print("🔧 Repairing t() function directly...")
    
    # Template fungsi t() yang benar
    correct_t_function = f'''def t(key, **kwargs):
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
        return key'''
    
    # Cari dan ganti fungsi t() yang rusak
    # Pattern untuk menemukan fungsi t() yang bermasalah
    t_function_patterns = [
        r'def t\(key, \*\*kwargs\):.*?except Exception:.*?return key',
        r'def t\(key, \*\*kwargs\):.*?return key\.format\(\*\*kwargs\).*?return key',
    ]
    
    for pattern in t_function_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, correct_t_function, content, flags=re.DOTALL)
            print(f"✅ Fixed corrupted t() function with language '{default_lang}'")
            return content
    
    # Jika tidak ditemukan pattern yang rusak, coba perbaiki hardcoded language saja
    print("ℹ️  No corrupted t() function found, checking for hardcoded languages...")
    
    # Perbaiki hardcoded language yang tersisa
    content = re.sub(
        r'return DISPLAY_LANGUAGES\["([a-z]+)"\]\[key\]\.format\(\*\*kwargs\)',
        f'return DISPLAY_LANGUAGES["{default_lang}"][key].format(**kwargs)',
        content
    )
    
    return content

def ask_language_selection(file_path, conflicting_langs=None):
    """Tanya user untuk memilih bahasa - VERSI DIPERBAIKI"""
    
    # Dapatkan bahasa yang benar-benar tersedia
    available_langs = get_existing_languages_from_file(file_path)
    
    if not available_langs:
        print("❌ No languages available in DISPLAY_LANGUAGES")
        return "en"
    
    # Jika tidak ada konflik atau hanya 1 bahasa, return langsung
    if not conflicting_langs or len(available_langs) == 1:
        if len(available_langs) == 1:
            print(f"✅ Only one language available: {available_langs[0]}")
            return available_langs[0]
        return available_langs[0] if available_langs else "en"
    
    # Filter konflik yang valid (hanya yang ada di available_langs)
    valid_conflicts = [lang for lang in conflicting_langs if lang in available_langs]
    
    # Jika tidak ada konflik valid, gunakan bahasa pertama yang available
    if not valid_conflicts:
        print(f"🎯 No valid conflicts, using first available language: {available_langs[0]}")
        return available_langs[0]
    
    # Jika hanya 1 konflik valid, return langsung
    if len(valid_conflicts) == 1:
        print(f"✅ Only one valid conflict: {valid_conflicts[0]}")
        return valid_conflicts[0]
    
    # ✅ PERBAIKAN BESAR: Tampilkan SEMUA bahasa yang tersedia, bukan hanya yang konflik
    print("\n🌍 Please select the default display language:")
    print("📋 Available languages in DISPLAY_LANGUAGES:")
    print("=" * 50)
    
    language_names = {
        "en": "English", "pl": "Polski", "zh": "中文", "jp": "日本語",
        "de": "Deutsch", "fr": "Français", "es": "Español", "ru": "Pycckuñ",
        "pt": "Portugués", "id": "Indonesia", "kr": "한국어"
    }
    
    for i, lang_code in enumerate(available_langs, 1):
        lang_name = language_names.get(lang_code, lang_code.upper())
        # Tandai bahasa yang konflik
        conflict_indicator = " ⚠️ (CURRENT CONFLICT)" if lang_code in valid_conflicts else ""
        print(f"  {i}. {lang_code} - {lang_name}{conflict_indicator}")
    
    print("=" * 50)
    print("  S. Skip (let system decide)")
    
    while True:
        choice = input("\n👉 Enter your choice (number, language code, or S): ").strip()
        
        if choice.upper() == 'S':
            # Prioritaskan bahasa yang ada di konflik valid
            for lang in valid_conflicts:
                if lang in available_langs:
                    print(f"🎯 System selected: {lang} (from valid conflicts)")
                    return lang
            # Fallback ke bahasa pertama yang available
            selected = available_langs[0]
            print(f"🎯 System selected: {selected} (first available)")
            return selected
        
        elif choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_langs):
                return available_langs[choice_num - 1]
            else:
                print(f"❌ Please enter number between 1 and {len(available_langs)}")
        
        elif choice.lower() in available_langs:
            return choice.lower()
        
        else:
            print(f"❌ Invalid choice. Please enter:")
            print(f"   - A number (1-{len(available_langs)})")
            print(f"   - Language code ({', '.join(available_langs)})")
            print(f"   - 'S' to skip")

def repair_functions_force_generate(content, default_lang="en"):
    """
    🔧 VERSI DENGAN STRUCTURE VALIDATION KETAT - TIDAK MENGHAPUS KODE PENTING
    """
    print("🔧 Repair mode with strict structure validation...")

    active_lang = default_lang
    print(f"🌍 Using language: '{active_lang}'")

    # ✅ CEK APAKAH SUDAH ADA FUNGSI DISPLAY_LANGUAGE YANG LENGKAP
    required_elements = [
        'DISPLAY_LANGUAGES = {',
        'DISPLAY_LANG = "',
        'def set_display_language(',
        'def t(',
        'def get_display_language(',
        'def get_available_languages('
    ]
    
    has_all_elements = all(element in content for element in required_elements)
    
    if has_all_elements:
        print("✅ DISPLAY_LANGUAGE section already complete!")
        # PERBAIKI: Perbaiki fungsi t() yang rusak
        content = repair_function_t_directly(content, default_lang)
        return content
    
    # ✅ TEMPLATE SECTION DENGAN SPASI DI BAWAH
    complete_section = f'''# ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------

DISPLAY_LANGUAGES = {{
    "{active_lang}": {{
        # {active_lang.upper()} translations will be added here
    }}
}}

# Global variable for display language
DISPLAY_LANG = "{active_lang}"

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
        elif key in DISPLAY_LANGUAGES["{active_lang}"]:
            return DISPLAY_LANGUAGES["{active_lang}"][key].format(**kwargs)
        else:
            return key
    except Exception:
        return key

def get_display_language():
    """Get current display language"""
    return DISPLAY_LANG

def get_available_languages():
    """Get list of available languages"""
    return list(DISPLAY_LANGUAGES.keys())

'''  # ✅ ADA 1 BARIS KOSONG TAMBAHAN DI SINI

    # ✅ CARI POSISI UNTUK MENYISIPKAN SECTION BARU
    try:
        from .fallback_strategy import find_best_insert_position
    except ImportError:
        from fallback_strategy import find_best_insert_position
    
    lines = content.splitlines()
    insert_pos = find_best_insert_position(content)
    
    print(f"📝 Inserting missing functions at position: {insert_pos}")
    new_lines = lines[:insert_pos] + [''] + complete_section.splitlines() + lines[insert_pos:]
    new_content = "\n".join(new_lines)
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    print("✅ Missing functions added successfully!")
    return new_content

def run_insert_section_dynamic(target_file):
    """Jalankan insert_section secara langsung tanpa import dinamis kompleks"""
    try:
        # Tambahkan current directory ke sys.path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import langsung
        try:
            from insert_section import run_insert_section
            run_insert_section(target_file)
            return True
        except ImportError:
            # Coba relative import
            from .insert_section import run_insert_section
            run_insert_section(target_file)
            return True
            
    except Exception as e:
        print(f"❌ Error running insert_section: {e}")
        import traceback
        traceback.print_exc()
        return False

def ask_generate_section(target_file):
    """Tanya user apakah ingin generate section DISPLAY_LANGUAGES"""
    print(f"\n❌ File '{target_file}' doesn't have DISPLAY_LANGUAGES section!")
    
    while True:
        choice = input("\n👉 Do you want to generate a complete DISPLAY_LANGUAGES section now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🎯 Generating DISPLAY_LANGUAGES section...")
            
            # Gunakan import dinamis untuk hindari circular import
            success = run_insert_section_dynamic(target_file)
            
            if success:
                print("✅ DISPLAY_LANGUAGES section generated successfully!")
                return True
            else:
                print("❌ Failed to generate DISPLAY_LANGUAGES section")
                return False
                
        elif choice in ['n', 'no', '']:
            print("ℹ️ Operation cancelled. No changes made.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

# ==================== FUNGSI UTAMA ====================

def run_repair_functions(target_file):
    """Run repair process - DENGAN LOGIKA YANG LEBIH CERDAS"""
    # ✅ GUNAKAN FALLBACK STRATEGY
    try:
        from .fallback_strategy import fallback_for_repair
    except ImportError:
        from fallback_strategy import fallback_for_repair
    
    # Cek section dan generate jika perlu
    if not fallback_for_repair(target_file):
        return False
    
    # Lanjut proses repair normal
    print("🔄 Continuing with repair process...")
    
    with open(target_file, 'r', encoding='utf-8') as f:
        original = f.read()

    backup = target_file + ".backup"
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(original)
    print(f"📁 Backup created: {backup}")

    # ✅ PERBAIKAN: DAPATKAN BAHASA DEFAULT DARI FALLBACK PROCESS
    default_lang = get_default_language_from_fallback(target_file)
    
    # Variabel untuk tracking konflik (untuk menghindari error)
    conflicting_langs_detected = False
    
    if not default_lang:
        # Fallback ke logika lama jika tidak ditemukan
        conflicting_langs = detect_language_conflicts(original)
        conflicting_langs_detected = conflicting_langs is not None
        
        if not conflicting_langs:
            print("✅ No conflicts found, using existing language")
            existing_langs = get_existing_languages_from_content(original)
            if existing_langs:
                default_lang = existing_langs[0]
                print(f"🎯 Using existing language: {default_lang}")
            else:
                default_lang = "en"
                print("ℹ️  No languages found in DISPLAY_LANGUAGES, using 'en'")
        else:
            conflict_list = re.findall(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', original)
            default_lang = ask_language_selection(target_file, conflict_list)
    else:
        print(f"🎯 Using default language from fallback: {default_lang}")
    
    # ✅ JALANKAN REPAIR
    print("🔧 Running FULL REPAIR...")
    
    try:
        content = original
        content = repair_braces_and_content(content)
        content = remove_duplicate_functions(content, default_lang)
        content = repair_functions_force_generate(content, default_lang)
        
        # ✅ PERBAIKAN BARU: FIX LANGUAGE ORDER
        content = fix_language_order_in_content(content)

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Full repair completed successfully!")
        if conflicting_langs_detected:
            print("✅ Language conflicts resolved!")
        print("✅ Duplicate functions and variables removed!")
        print("✅ Language order fixed!")
        print(f"💾 Backup saved: {backup}")
        return True

    except Exception as e:
        print(f"❌ Error during repair: {e}")
        import traceback
        traceback.print_exc()
        
        # Restore from backup
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(original)
        print("🔄 Restored from backup due to error.")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_repair_functions(sys.argv[1])
    else:
        print("❌ Please provide a target file.")
        print("Usage: python repair_functions.py <filename>")