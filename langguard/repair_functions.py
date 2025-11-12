#!/usr/bin/env python3
"""
LangGuard - Repair Functions Only (PRECISE CLEANING)
HANYA MENGHAPUS FUNGSI DISPLAY LANGUAGE YANG DUPLIKAT - PRESISI
"""

import os
import sys
import re

def check_display_section_exists(content):
    """Cek apakah DISPLAY_LANGUAGES section ada dan valid"""
    return 'DISPLAY_LANGUAGES = {' in content

def detect_language_conflicts(content):
    """Deteksi konflik bahasa dan tentukan yang mana yang dipertahankan"""
    print("🔍 Detecting language conflicts...")
    
    # Cari semua instance DISPLAY_LANG
    display_lang_matches = re.findall(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', content)
    
    if len(display_lang_matches) <= 1:
        print("✅ No language conflicts detected")
        return None
    
    print(f"⚠️  Found {len(display_lang_matches)} DISPLAY_LANG instances: {', '.join(display_lang_matches)}")
    
    # Strategi 1: Prioritaskan bahasa yang ada di DISPLAY_LANGUAGES
    existing_langs = get_existing_languages_from_content(content)
    if existing_langs:
        for lang in display_lang_matches:
            if lang in existing_langs:
                print(f"🎯 Prioritizing '{lang}' (exists in DISPLAY_LANGUAGES)")
                return lang
    
    # Strategi 2: Ambil yang pertama ditemukan (biasanya yang benar)
    first_lang = display_lang_matches[0]
    print(f"🎯 Using first found language: '{first_lang}'")
    return first_lang

def get_existing_languages_from_content(content):
    """Ambil daftar bahasa yang ada di DISPLAY_LANGUAGES"""
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

def find_display_functions_boundaries(content):
    """Temukan batas awal dan akhir dari fungsi display language dengan PRESISI"""
    print("🔍 Finding display functions boundaries precisely...")
    
    # Pattern yang lebih fleksibel untuk mendeteksi berbagai format fungsi display language
    # Mencakup berbagai variasi penulisan yang mungkin
    display_functions_patterns = [
        # Pattern 1: Standard block dengan semua fungsi
        r'(DISPLAY_LANG\s*=\s*["\'][a-z]{2}["\'][\s\S]*?def get_available_languages\(\):[\s\S]*?return list\(DISPLAY_LANGUAGES\.keys\(\)\))',
        
        # Pattern 2: Block dengan fungsi yang mungkin tidak lengkap
        r'(DISPLAY_LANG\s*=\s*["\'][a-z]{2}["\'][\s\S]*?def set_display_language\([\s\S]*?def t\([\s\S]*?def get_display_language)',
        
        # Pattern 3: Hanya fungsi-fungsi utama tanpa DISPLAY_LANG
        r'(def set_display_language\([\s\S]*?def t\([\s\S]*?def get_display_language\([\s\S]*?def get_available_languages\([\s\S]*?return list\(DISPLAY_LANGUAGES\.keys\(\)\))',
        
        # Pattern 4: Fungsi individual yang tersebar
        r'(def set_display_language\([^)]*\):[\s\S]*?"""[^"]*"""[\s\S]*?global DISPLAY_LANG[\s\S]*?if lang_code in DISPLAY_LANGUAGES)',
    ]
    
    all_matches = []
    for pattern in display_functions_patterns:
        matches = list(re.finditer(pattern, content))
        all_matches.extend(matches)
    
    # Filter duplikat (overlapping matches)
    unique_matches = []
    for match in all_matches:
        is_duplicate = False
        for existing in unique_matches:
            if (match.start() >= existing.start() and match.end() <= existing.end()):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_matches.append(match)
    
    if len(unique_matches) == 0:
        print("❌ No display functions found with standard patterns, trying fallback detection...")
        # Fallback: cari fungsi individual
        return find_display_functions_fallback(content)
    
    print(f"✅ Found {len(unique_matches)} display functions block(s)")
    return unique_matches

def find_display_functions_fallback(content):
    """Fallback detection untuk fungsi display language yang tersebar"""
    print("🔍 Using fallback function detection...")
    
    # Cek apakah fungsi-fungsi individual ada
    required_funcs = [
        ('DISPLAY_LANG', r'DISPLAY_LANG\s*=\s*["\'][a-z]{2}["\']'),
        ('set_display_language', r'def set_display_language\([^)]*\):'),
        ('t', r'def t\([^)]*\):'),
        ('get_display_language', r'def get_display_language\([^)]*\):'),
        ('get_available_languages', r'def get_available_languages\([^)]*\):')
    ]
    
    found_funcs = []
    for func_name, pattern in required_funcs:
        if re.search(pattern, content):
            found_funcs.append(func_name)
    
    if len(found_funcs) >= 3:  # Minimal 3 fungsi untuk dianggap valid
        print(f"✅ Found individual functions: {', '.join(found_funcs)}")
        
        # Coba temukan blok yang mengandung sebagian besar fungsi
        start_pattern = r'DISPLAY_LANG\s*=\s*["\'][a-z]{2}["\']'
        start_match = re.search(start_pattern, content)
        
        if start_match:
            # Cari sampai akhir get_available_languages atau batas tertentu
            start_pos = start_match.start()
            end_pattern = r'def get_available_languages\(\):[\s\S]*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)'
            end_match = re.search(end_pattern, content[start_pos:])
            
            if end_match:
                end_pos = start_pos + end_match.end()
                # Buat match object manual
                class MockMatch:
                    def __init__(self, start, end):
                        self.start_pos = start
                        self.end_pos = end
                    def start(self):
                        return self.start_pos
                    def end(self):
                        return self.end_pos
                
                return [MockMatch(start_pos, end_pos)]
    
    print("❌ No complete display functions block found")
    return []

def remove_duplicate_display_functions_precise(content):
    """Hapus fungsi display language yang duplikat dengan PRESISI - hanya hapus duplikatnya saja"""
    print("🔧 Removing duplicate display functions PRECISELY...")
    
    # Temukan semua blok fungsi display
    function_blocks = find_display_functions_boundaries(content)
    
    if len(function_blocks) <= 1:
        print("✅ No duplicates found")
        return content
    
    print(f"⚠️  Found {len(function_blocks)} duplicate function blocks")
    
    # Pertahankan hanya blok pertama, hapus yang lainnya
    first_block = function_blocks[0]
    cleaned_content = content
    
    # Hapus blok duplikat dari yang terakhir ke pertama (agar posisi tidak berubah)
    removed_count = 0
    for block in reversed(function_blocks[1:]):
        print(f"🗑️  Removing duplicate function block at position {block.start()}")
        cleaned_content = cleaned_content[:block.start()] + cleaned_content[block.end():]
        removed_count += 1
    
    # ✅ PERBAIKAN BARU: Cleanup komentar yang tertinggal
    cleaned_content = cleanup_orphaned_comments(cleaned_content)
    
    # Cleanup whitespace
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
    
    print(f"✅ {removed_count} duplicate display functions removed precisely")
    return cleaned_content

def cleanup_orphaned_comments(content):
    """Bersihkan komentar yang tertinggal setelah penghapusan fungsi"""
    print("🧹 Cleaning up orphaned comments...")
    
    # Pattern untuk menemukan komentar "Global variable for display language" yang tidak diikuti DISPLAY_LANG
    orphaned_comment_pattern = r'# Global variable for display language\s*\n(?!\s*DISPLAY_LANG\s*=)'
    
    # Hapus komentar yang orphaned
    cleaned_content = re.sub(orphaned_comment_pattern, '', content)
    
    # Juga hapus baris kosong berlebihan setelah cleanup
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
    
    return cleaned_content

def repair_braces_and_content(content):
    """
    💎 Ultra-Final Repair (Strict Safe Mode) - HANYA untuk DISPLAY_LANGUAGES
    """
    print("🔧 Running ULTRA-FINAL repair for DISPLAY_LANGUAGES only...")

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
            # contoh: "translating_readme"📘 Translating...
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

    # Hapus koma terakhir sebelum penutup blok bahasa (misalnya setelah "folder_deleted")
    new_inner = re.sub(r',\s*\n\s*    \}', '\n    }', new_inner)

    # Hapus koma terakhir sebelum penutup dictionary utama
    new_inner = re.sub(r',\s*\n\s*\}', '\n}', new_inner)

    # --- Tambahan: hilangkan koma terakhir di akhir dictionary utama ---
    new_inner = re.sub(r',\s*\n\}', '\n}', new_inner)
    new_inner = re.sub(r',\s*\Z', '', new_inner)  # jika masih ada koma paling akhir

    # Rebuild dictionary
    rebuilt = f"DISPLAY_LANGUAGES = {{\n{new_inner}\n}}"

    new_content = re.sub(
        r'DISPLAY_LANGUAGES\s*=\s*\{[\s\S]*?\n\}',
        rebuilt,
        content,
    )

    print("✅ DISPLAY_LANGUAGES content repair complete")
    return new_content

def ask_language_selection(file_path, conflicting_langs=None):
    """Tanya user untuk memilih bahasa default saat repair - DENGAN KONFLIK HANDLING"""
    print("\n🌍 Please select the default display language for repair:")
    
    # Jika ada konflik, tampilkan bahasa yang konflik
    if conflicting_langs:
        print(f"⚠️  Conflict detected between: {', '.join(conflicting_langs)}")
    
    # Dapatkan bahasa yang tersedia
    try:
        # Import dinamis untuk menghindari circular import
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from update_language import get_available_languages_from_file
        available_langs = get_available_languages_from_file(file_path)
    except ImportError:
        try:
            from .update_language import get_available_languages_from_file
            available_langs = get_available_languages_from_file(file_path)
        except ImportError:
            print("❌ Cannot import language functions. Using 'en' as default.")
            return "en"
    
    if not available_langs:
        print("❌ No languages available. Using 'en' as default.")
        return "en"
    
    # Tampilkan pilihan bahasa
    language_names = {
        "en": "English", "pl": "Polski", "zh": "中文", "jp": "日本語",
        "de": "Deutsch", "fr": "Français", "es": "Español", "ru": "Pycckuñ",
        "pt": "Portugués", "id": "Indonesia", "kr": "한국어"
    }
    
    for i, lang_code in enumerate(available_langs, 1):
        lang_name = language_names.get(lang_code, lang_code.upper())
        # Tandai bahasa yang sedang konflik
        conflict_indicator = " ⚠️ (CONFLICT)" if conflicting_langs and lang_code in conflicting_langs else ""
        print(f"  {i}. {lang_code} - {lang_name}{conflict_indicator}")
    
    print("  S. Skip (let system decide)")
    
    while True:
        choice = input("\n👉 Enter your choice (number, language code, or S): ").strip()
        
        if choice.upper() == 'S':
            # Biarkan sistem memutuskan
            if conflicting_langs:
                # Prioritaskan bahasa yang ada di DISPLAY_LANGUAGES
                for lang in conflicting_langs:
                    if lang in available_langs:
                        print(f"🎯 System selected: {lang} (exists in DISPLAY_LANGUAGES)")
                        return lang
                # Jika tidak ada yang match, ambil yang pertama
                selected = conflicting_langs[0]
                print(f"🎯 System selected: {selected} (first conflict)")
                return selected
            return "en"
        elif choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_langs):
                return available_langs[choice_num - 1]
            else:
                print(f"❌ Please enter number between 1 and {len(available_langs)}")
        elif choice.lower() in available_langs:
            return choice.lower()
        else:
            print(f"❌ Invalid choice. Please enter a number (1-{len(available_langs)}), language code ({', '.join(available_langs)}), or 'S'")

def create_clean_display_functions_block(default_lang="en"):
    """Buat block fungsi display language yang BERSIH"""
    functions_template = f'''# 🌐 Display Language Control
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
    
    return functions_template

def check_display_functions_complete(content):
    """Cek apakah fungsi display language sudah lengkap"""
    required_elements = [
        r'DISPLAY_LANG\s*=\s*["\'][a-z]{2}["\']',
        r'def set_display_language\([^)]*\):',
        r'def t\([^)]*\):',
        r'def get_display_language\([^)]*\):',
        r'def get_available_languages\([^)]*\):'
    ]
    
    missing_count = 0
    for pattern in required_elements:
        if not re.search(pattern, content):
            missing_count += 1
    
    # Dianggap lengkap jika maksimal 1 elemen yang missing
    return missing_count <= 1

def remove_incomplete_display_functions(content):
    """Hapus fungsi display language yang tidak lengkap"""
    print("🧹 Removing incomplete display functions...")
    
    # Pattern untuk menemukan bagian-bagian fungsi display language yang terpisah
    display_patterns = [
        r'DISPLAY_LANG\s*=\s*["\'][a-z]{2}["\'][^}]*?def set_display_language\([^)]*\):[^}]*?def t\([^)]*\):[^}]*?def get_display_language\([^)]*\):[^}]*?def get_available_languages\([^)]*\):[^}]*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)',
        r'def set_display_language\([^)]*\):[^}]*?"""[^"]*"""[\s\S]*?global DISPLAY_LANG',
        r'def t\([^)]*\):[^}]*?"""[^"]*"""[\s\S]*?DISPLAY_LANGUAGES\[DISPLAY_LANG\]',
        r'def get_display_language\([^)]*\):[^}]*?return DISPLAY_LANG',
        r'def get_available_languages\([^)]*\):[^}]*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)'
    ]
    
    for pattern in display_patterns:
        content = re.sub(pattern, '', content)
    
    # Juga hapus DISPLAY_LANG yang berdiri sendiri
    content = re.sub(r'DISPLAY_LANG\s*=\s*["\'][a-z]{2}["\']\s*\n', '', content)
    
    # Cleanup whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

def update_display_language_using_module(content, selected_lang):
    """Update display language value dalam content"""
    print(f"🔄 Updating DISPLAY_LANG to '{selected_lang}'...")
    
    # Update DISPLAY_LANG value
    pattern = r'(DISPLAY_LANG\s*=\s*["\'])([a-z]{2})(["\'])'
    replacement = r'\1' + selected_lang + r'\3'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print(f"✅ DISPLAY_LANG updated to '{selected_lang}'")
    else:
        print(f"⚠️ DISPLAY_LANG assignment not found, cannot update to '{selected_lang}'")
    
    return content

def run_repair_functions(target_file):
    """Run repair process - PRESISI CLEANING"""
    # ✅ GUNAKAN FALLBACK STRATEGY YANG BARU
    try:
        from .fallback_strategy import fallback_for_repair
    except ImportError:
        from fallback_strategy import fallback_for_repair
    
    # Cek section dan generate jika perlu
    if not fallback_for_repair(target_file):
        return False  # File tidak ada atau user cancel
    
    # Lanjut proses repair normal (section sudah ada)
    print("🔄 Continuing with PRECISE repair process...")
    
    with open(target_file, 'r', encoding='utf-8') as f:
        original = f.read()

    backup = target_file + ".backup"
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(original)
    print(f"📁 Backup created: {backup}")

    # ✅ PERBAIKAN: CEK DULU APAKAH ADA MASALAH YANG PERLU DIPERBAIKI
    needs_repair = check_if_repair_needed(original)
    
    if not needs_repair:
        print("✅ No repair needed - file is already in good condition!")
        print("💡 All display functions are properly structured with no duplicates.")
        
        # Tampilkan status current
        current_lang = re.search(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', original)
        if current_lang:
            print(f"🔍 Current display language: {current_lang.group(1)}")
        
        # Hapus backup karena tidak ada perubahan
        if os.path.exists(backup):
            os.remove(backup)
            print("🗑️ Backup removed (no changes made)")
        
        return True

    # ✅ HANYA JALANKAN PROSES REPAIR JIKA BENAR-BENAR DIBUTUHKAN
    print("🔧 Running PRECISE REPAIR (fixing issues only)...")
    
    try:
        content = original
        
        # 1. Jika ada konflik bahasa, tanyakan pemilihan
        conflicting_langs = detect_language_conflicts(content)
        if conflicting_langs:
            conflict_list = re.findall(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', content)
            default_lang = ask_language_selection(target_file, conflict_list)
            
            # Repair content dan update language
            content = repair_braces_and_content(content)
            content = ensure_proper_functions_structure_precise(content, default_lang)
        else:
            # 2. Jika tidak ada konflik, hanya lakukan minor fixes
            content = repair_braces_and_content(content)
            content = ensure_proper_functions_structure_precise(content)
        
        # 3. Tulis file final HANYA jika ada perubahan
        if content != original:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print("✅ PRECISE REPAIR successful!")
            print("✅ Only necessary fixes were applied!")
            print(f"💾 Backup saved: {backup}")
        else:
            print("✅ No changes needed - file is already optimal!")
            # Hapus backup karena tidak ada perubahan
            if os.path.exists(backup):
                os.remove(backup)
                print("🗑️ Backup removed (no changes made)")
        
        # Tampilkan preview hasil
        show_repair_preview(content)
        
        return True

    except Exception as e:
        print(f"❌ Error during precise repair: {e}")
        import traceback
        traceback.print_exc()
        
        # Restore from backup
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(original)
        print("🔄 Restored from backup due to error.")
        return False

def check_if_repair_needed(content):
    """Cek apakah file perlu di-repair"""
    print("🔍 Checking if repair is needed...")
    
    issues_found = []
    
    # 1. Cek duplikasi fungsi display language
    function_blocks = find_display_functions_boundaries(content)
    if len(function_blocks) > 1:
        issues_found.append(f"Duplicate functions ({len(function_blocks)} blocks)")
    
    # 2. Cek konflik bahasa
    display_lang_matches = re.findall(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', content)
    if len(display_lang_matches) > 1:
        issues_found.append(f"Language conflicts ({len(display_lang_matches)} DISPLAY_LANG instances)")
    
    # 3. Cek struktur DISPLAY_LANGUAGES yang rusak
    if not check_display_section_exists(content):
        issues_found.append("Missing DISPLAY_LANGUAGES section")
    else:
        # Cek brace balance
        dict_match = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{([\s\S]*?)\n\}', content)
        if not dict_match:
            issues_found.append("Invalid DISPLAY_LANGUAGES structure")
    
    # 4. Cek fungsi yang tidak lengkap
    missing_funcs = check_missing_functions(content)
    if missing_funcs:
        issues_found.append(f"Incomplete functions ({', '.join(missing_funcs)})")
    
    # 5. Cek whitespace berlebihan di section display language
    display_section = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{[\s\S]*?\n\}', content)
    if display_section:
        section_content = display_section.group(0)
        if re.search(r'\n{4,}', section_content):  # 4+ newlines berturut-turut
            issues_found.append("Excessive whitespace in DISPLAY_LANGUAGES")
    
    if issues_found:
        print(f"⚠️ Repair needed: {', '.join(issues_found)}")
        return True
    else:
        print("✅ No repair issues found")
        return False

def check_missing_functions(content):
    """Cek fungsi display language yang missing"""
    required_funcs = {
        'DISPLAY_LANG': r'DISPLAY_LANG\s*=\s*["\'][a-z]{2}["\']',
        'set_display_language': r'def set_display_language\([^)]*\):',
        't': r'def t\([^)]*\):',
        'get_display_language': r'def get_display_language\([^)]*\):',
        'get_available_languages': r'def get_available_languages\([^)]*\):'
    }
    
    missing = []
    for func_name, pattern in required_funcs.items():
        if not re.search(pattern, content):
            missing.append(func_name)
    
    return missing

def show_repair_preview(content):
    """Tampilkan preview hasil repair"""
    print(f"\n📋 DISPLAY FUNCTIONS PREVIEW:")
    print("=" * 50)
    
    lines = content.split('\n')
    display_lines = []
    
    # Cari bagian display language settings
    in_display_section = False
    for line in lines:
        if any(keyword in line for keyword in ['DISPLAY_LANGUAGES', 'DISPLAY_LANG', 'def set_display_language', 'def t(', 'def get_display_language', 'def get_available_languages']):
            in_display_section = True
        
        if in_display_section:
            display_lines.append(line)
            # Stop ketika menemukan fungsi lain atau akhir section
            if line.strip() and not any(keyword in line for keyword in ['DISPLAY_', 'def ', '    ', '}']) and not line.startswith('#'):
                if len(display_lines) > 15:  # Batasi preview
                    break
    
    # Tampilkan maksimal 15 baris
    for line in display_lines[:15]:
        print(f"  {line}")
    
    print("=" * 50)

def ensure_proper_functions_structure_precise(content, default_lang=None):
    """Pastikan struktur fungsi display language benar - VERSI PRESISI & CONSERVATIVE"""
    print("🔧 Ensuring proper display functions structure (PRECISE)...")
    
    # 1. Hapus duplikasi fungsi display language dengan presisi
    original_content = content
    content = remove_duplicate_display_functions_precise(content)
    
    # 2. Cek apakah perlu membuat fungsi baru
    has_valid_functions = check_display_functions_complete(content)
    
    if not has_valid_functions:
        print("🔄 Display functions are missing or incomplete, creating new ones...")
        
        # Hanya hapus jika benar-benar perlu
        content = remove_incomplete_display_functions(content)
        
        # Buat fungsi baru yang lengkap
        if default_lang is None:
            # Coba deteksi bahasa default dari content
            current_lang = re.search(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', original_content)
            default_lang = current_lang.group(1) if current_lang else "en"
        
        functions_block = create_clean_display_functions_block(default_lang)
        
        # Cari posisi setelah DISPLAY_LANGUAGES dictionary
        dict_match = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{[\s\S]*?\n\}', content)
        if dict_match:
            insert_pos = dict_match.end()
            content = content[:insert_pos] + "\n\n" + functions_block + "\n" + content[insert_pos:]
            print("✅ New display functions created")
        else:
            print("❌ Cannot find DISPLAY_LANGUAGES dictionary to insert functions")
    else:
        print("✅ Valid display functions already exist")
        
        # Jika default_lang diberikan, update nilai DISPLAY_LANG
        if default_lang:
            content = update_display_lang_value(content, default_lang)  # ✅ PERBAIKAN: gunakan fungsi yang benar
    
    return content

def update_display_language_using_module(file_path, content, selected_lang):
    """Update display language menggunakan fungsi dari update_language.py"""
    print(f"🔄 Updating display language to '{selected_lang}' using update_language module...")
    
    try:
        # Import fungsi dari update_language.py
        try:
            from .update_language import set_default_display_language_in_file, get_available_languages_from_file
        except ImportError:
            from update_language import set_default_display_language_in_file, get_available_languages_from_file
        
        # Simpan konten sementara ke file
        temp_file = file_path + ".temp_repair"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Cek apakah bahasa yang dipilih tersedia
        available_langs = get_available_languages_from_file(temp_file)
        if selected_lang not in available_langs:
            print(f"⚠️ Selected language '{selected_lang}' not in available languages: {available_langs}")
            print("🔄 Adding selected language to DISPLAY_LANGUAGES...")
            
            # Tambahkan bahasa yang dipilih ke DISPLAY_LANGUAGES jika belum ada
            content = add_language_to_display_languages(content, selected_lang)
            
            # Tulis ulang ke file temp
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Gunakan fungsi set_default_display_language_in_file untuk update yang komprehensif
        success = set_default_display_language_in_file(temp_file, selected_lang)
        
        if success:
            # Baca konten yang sudah diupdate
            with open(temp_file, 'r', encoding='utf-8') as f:
                updated_content = f.read()
            
            print(f"✅ Display language successfully updated to '{selected_lang}'")
            
            # Hapus file temporary
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return updated_content
        else:
            print("⚠️ Could not update display language using module, using fallback method...")
            # Fallback ke metode manual
            return update_display_lang_manually(content, selected_lang)
            
    except Exception as e:
        print(f"⚠️ Error using update_language module: {e}")
        print("🔄 Using fallback manual update...")
        # Fallback ke metode manual
        return update_display_lang_manually(content, selected_lang)

def update_display_lang_value(content, selected_lang):
    """Update nilai DISPLAY_LANG dalam content"""
    print(f"🔄 Updating DISPLAY_LANG to '{selected_lang}'...")
    
    # Pattern untuk menemukan dan mengganti nilai DISPLAY_LANG
    pattern = r'(DISPLAY_LANG\s*=\s*["\'])([a-z]{2})(["\'])'
    replacement = r'\1' + selected_lang + r'\3'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print(f"✅ DISPLAY_LANG updated to '{selected_lang}'")
    else:
        print(f"⚠️ DISPLAY_LANG assignment not found, cannot update to '{selected_lang}'")
    
    return content

def update_display_lang_manually(content, selected_lang):
    """Update display language secara manual (fallback)"""
    print(f"🔄 Manually updating DISPLAY_LANG to '{selected_lang}'...")
    
    # 1. Update DISPLAY_LANG value
    pattern = r'(DISPLAY_LANG\s*=\s*["\'])([a-z]{2})(["\'])'
    replacement = r'\1' + selected_lang + r'\3'
    content = re.sub(pattern, replacement, content)
    
    # 2. Update fallback language dalam fungsi t()
    fallback_patterns = [
        (r'elif key in DISPLAY_LANGUAGES\["([a-z]{2})"\]', 
         f'elif key in DISPLAY_LANGUAGES["{selected_lang}"]'),
        (r'DISPLAY_LANGUAGES\["([a-z]{2})"\]\[key\]\.format',
         f'DISPLAY_LANGUAGES["{selected_lang}"][key].format'),
    ]
    
    for pattern, replacement in fallback_patterns:
        content = re.sub(pattern, replacement, content)
    
    print(f"✅ Manual update completed: DISPLAY_LANG = '{selected_lang}'")
    return content

def add_language_to_display_languages(content, lang_code):
    """Tambahkan bahasa baru ke DISPLAY_LANGUAGES jika belum ada"""
    # Cari DISPLAY_LANGUAGES dictionary
    start_match = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{', content)
    if not start_match:
        return content
    
    # Cari posisi akhir dictionary yang tepat
    start_pos = start_match.start()
    brace_count = 0
    in_string = False
    escape_next = False
    
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
                    # Insert bahasa baru sebelum closing brace
                    insert_pos = i
                    new_lang_entry = f'    "{lang_code}": {{\n        # {lang_code.upper()} translations\n    }},\n'
                    content = content[:insert_pos] + new_lang_entry + content[insert_pos:]
                    print(f"✅ Added '{lang_code}' to DISPLAY_LANGUAGES")
                    break
    
    return content

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_repair_functions(sys.argv[1])
    else:
        print("❌ Please provide a target file.")
        print("Usage: python repair_functions.py <filename>")