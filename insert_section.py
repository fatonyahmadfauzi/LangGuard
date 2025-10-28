#!/usr/bin/env python3
"""
Script ULTIMATE COMPLETE - Fixed individual language selection
"""

import os
import re
import sys

# ==================== LANGUAGE MANAGEMENT ====================

def get_all_supported_languages():
    """Daftar semua bahasa yang seharusnya ada - DENGAN URUTAN YANG BENAR"""
    return ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"]

def check_existing_languages(content):
    """Cek bahasa yang sudah ada dengan detection yang lebih akurat"""
    
    print("🔍 Checking existing languages...")
    
    # FIXED: Approach yang lebih reliable dengan brace counting
    start_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        print("❌ DISPLAY_LANGUAGES dictionary not found!")
        return []
    
    # Cari kurung tutup yang sesuai (matching brace)
    start_pos = start_match.end()
    brace_count = 1
    current_pos = start_pos
    
    while brace_count > 0 and current_pos < len(content):
        if content[current_pos] == '{':
            brace_count += 1
        elif content[current_pos] == '}':
            brace_count -= 1
        current_pos += 1
    
    if brace_count != 0:
        print("❌ Invalid DISPLAY_LANGUAGES dictionary structure!")
        return []
    
    languages_section = content[start_match.start():current_pos]
    
    # Deteksi bahasa yang ada
    existing_languages = []
    all_langs = get_all_supported_languages()
    
    for lang in all_langs:
        if f'"{lang}":' in languages_section:
            existing_languages.append(lang)
    
    print(f"✅ Found {len(existing_languages)} existing languages: {', '.join(existing_languages)}")
    
    return existing_languages

def show_all_language_options():
    """Tampilkan pilihan semua bahasa"""
    
    print("\n🎯 ALL LANGUAGE OPTIONS:")
    print("=" * 50)
    
    language_names = {
        "en": "English",
        "pl": "Polish", 
        "zh": "Chinese",
        "jp": "Japanese",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "ru": "Russian",
        "pt": "Portuguese",
        "id": "Indonesian",
        "kr": "Korean"
    }
    
    all_langs = get_all_supported_languages()
    for i, lang_code in enumerate(all_langs, 1):
        lang_name = language_names.get(lang_code, lang_code)
        print(f"  {i}. {lang_code} - {lang_name}")
    
    print("=" * 50)

def get_language_selection():
    """Dapatkan pilihan bahasa dari user"""
    
    while True:
        print(f"\n👉 Enter your choice:")
        print("   - Single number (e.g., 1)")
        print("   - Multiple numbers separated by comma (e.g., 1,3,5)") 
        print("   - 'A' for all languages")
        print("   - 'S' to skip")
        
        choice = input("Your choice: ").strip().upper()
        
        if choice == 'A':
            return get_all_supported_languages()
        elif choice == 'S':
            return []
        elif ',' in choice:
            # Multiple selection
            selected_numbers = choice.split(',')
            selected_languages = []
            all_langs = get_all_supported_languages()
            
            valid_selection = True
            for num_str in selected_numbers:
                num_str = num_str.strip()
                if num_str.isdigit():
                    index = int(num_str) - 1
                    if 0 <= index < len(all_langs):
                        selected_languages.append(all_langs[index])
                    else:
                        print(f"❌ Invalid number: {num_str}. Please enter numbers between 1 and {len(all_langs)}")
                        valid_selection = False
                        break
                else:
                    print(f"❌ Invalid input: {num_str}. Please enter numbers only.")
                    valid_selection = False
                    break
            
            if valid_selection and selected_languages:
                # Remove duplicates while preserving order
                unique_languages = []
                for lang in selected_languages:
                    if lang not in unique_languages:
                        unique_languages.append(lang)
                return unique_languages
            else:
                print("❌ No valid languages selected")
        elif choice.isdigit():
            # Single selection
            all_langs = get_all_supported_languages()
            index = int(choice) - 1
            if 0 <= index < len(all_langs):
                return [all_langs[index]]
            else:
                print(f"❌ Please enter number between 1 and {len(all_langs)}")
        else:
            print("❌ Invalid choice. Please enter a number, multiple numbers separated by comma, 'A', or 'S'")

def replace_all_languages_in_content(content, languages_to_keep):
    """Ganti semua bahasa di content dengan hanya bahasa yang dipilih"""
    
    if not languages_to_keep:
        print("ℹ️ No languages selected to keep")
        return content
    
    print(f"\n🔄 Replacing ALL languages with selected {len(languages_to_keep)} languages: {', '.join(languages_to_keep)}")
    
    # Template untuk setiap bahasa
    language_templates = {
        "en": '    "en": {\n        # English translations will be added globally later\n    }',
        "pl": '    "pl": {\n        # Polish translations will be added globally later  \n    }',
        "zh": '    "zh": {\n        # Chinese translations will be added globally later\n    }',
        "jp": '    "jp": {\n        # Japanese translations will be added globally later\n    }',
        "de": '    "de": {\n        # German translations will be added globally later\n    }',
        "fr": '    "fr": {\n        # French translations will be added globally later\n    }',
        "es": '    "es": {\n        # Spanish translations will be added globally later\n    }',
        "ru": '    "ru": {\n        # Russian translations will be added globally later\n    }',
        "pt": '    "pt": {\n        # Portuguese translations will be added globally later\n    }',
        "id": '    "id": {\n        # Indonesian translations will be added globally later\n    }',
        "kr": '    "kr": {\n        # Korean translations will be added globally later\n    }'
    }
    
    # Cari DISPLAY_LANGUAGES dictionary
    start_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        print("❌ DISPLAY_LANGUAGES dictionary not found!")
        return content
    
    # Cari kurung tutup yang sesuai
    start_pos = start_match.end()
    brace_count = 1
    current_pos = start_pos
    
    while brace_count > 0 and current_pos < len(content):
        if content[current_pos] == '{':
            brace_count += 1
        elif content[current_pos] == '}':
            brace_count -= 1
        current_pos += 1
    
    if brace_count != 0:
        print("❌ Invalid DISPLAY_LANGUAGES dictionary structure!")
        return content
    
    # Extract bagian sebelum dan sesudah dictionary
    before_dict = content[:start_match.start()]
    after_dict = content[current_pos:]
    
    # Urutan yang diinginkan
    desired_order = ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"]
    
    # Filter languages_to_keep sesuai urutan yang diinginkan
    sorted_languages_to_keep = [lang for lang in desired_order if lang in languages_to_keep]
    
    print(f"📋 Keeping languages in correct order: {', '.join(sorted_languages_to_keep)}")
    
    # Bangun dictionary baru dengan hanya bahasa yang dipilih
    new_dict_content = 'DISPLAY_LANGUAGES = {\n'
    
    for i, lang_code in enumerate(sorted_languages_to_keep):
        if lang_code in language_templates:
            template = language_templates[lang_code]
            # Tambahkan koma kecuali untuk bahasa terakhir
            if i < len(sorted_languages_to_keep) - 1:
                template += ','
            new_dict_content += template + '\n'
    
    new_dict_content += '}'
    
    # Gabungkan konten baru
    new_content = before_dict + new_dict_content + after_dict
    
    print(f"✅ Successfully kept {len(sorted_languages_to_keep)} languages!")
    print(f"📊 Final languages: {', '.join(sorted_languages_to_keep)}")
    
    return new_content

def create_complete_display_section_from_scratch(content):
    """Buat section DISPLAY LANGUAGE lengkap dari nol dengan penempatan yang tepat"""
    
    print("🆕 Creating complete DISPLAY LANGUAGE section from scratch...")
    
    # Template lengkap untuk section DISPLAY LANGUAGE
    display_language_section = '''# ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------
DISPLAY_LANGUAGES = {
    "en": {
        # English translations will be added globally later
    },
    "pl": {
        # Polish translations will be added globally later  
    },
    "zh": {
        # Chinese translations will be added globally later
    },
    "jp": {
        # Japanese translations will be added globally later
    },
    "de": {
        # German translations will be added globally later
    },
    "fr": {
        # French translations will be added globally later
    },
    "es": {
        # Spanish translations will be added globally later
    },
    "ru": {
        # Russian translations will be added globally later
    },
    "pt": {
        # Portuguese translations will be added globally later
    },
    "id": {
        # Indonesian translations will be added globally later
    },
    "kr": {
        # Korean translations will be added globally later
    }
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
    """Translation function for notifications - will be populated globally"""
    global DISPLAY_LANG
    try:
        # Try to get translation from current display language
        if DISPLAY_LANG in DISPLAY_LANGUAGES and key in DISPLAY_LANGUAGES[DISPLAY_LANG]:
            return DISPLAY_LANGUAGES[DISPLAY_LANG][key].format(**kwargs)
        # Fallback to English
        elif key in DISPLAY_LANGUAGES["en"]:
            return DISPLAY_LANGUAGES["en"][key].format(**kwargs)
        else:
            # Return key as placeholder - will be filled globally
            return f"{key}"
    except Exception as e:
        # Return key on error - will be filled globally
        return f"{key}"

def get_display_language():
    """Get current display language"""
    return DISPLAY_LANG

def get_available_languages():
    """Get list of available languages"""
    return list(DISPLAY_LANGUAGES.keys())

'''
    
    # Analisis struktur file untuk menentukan posisi penyisipan yang tepat
    lines = content.split('\n')
    
    # Cari shebang dan docstring
    has_shebang = lines and lines[0].startswith('#!')
    docstring_start = -1
    docstring_end = -1
    imports_start = -1
    
    # Cari docstring
    for i, line in enumerate(lines):
        if re.match(r'^""".*|^r""".*|^\'\'\'.*|^r\'\'\'.*', line.strip()):
            if docstring_start == -1:
                docstring_start = i
            # Cari akhir docstring
            for j in range(i, len(lines)):
                if '"""' in lines[j] or "'''" in lines[j]:
                    if j > i or ('"""' in line and line.count('"""') == 2) or ("'''" in line and line.count("'''") == 2):
                        docstring_end = j
                        break
            if docstring_end != -1:
                break
    
    # Cari imports
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            imports_start = i
            break
    
    # Tentukan posisi penyisipan
    if imports_start != -1:
        # Sisipkan setelah imports
        insert_position = imports_start + 1
        # Cari akhir block imports
        for i in range(imports_start + 1, len(lines)):
            if not lines[i].strip().startswith('import ') and not lines[i].strip().startswith('from ') and lines[i].strip():
                insert_position = i
                break
    elif docstring_end != -1:
        # Sisipkan setelah docstring
        insert_position = docstring_end + 1
    elif has_shebang:
        # Sisipkan setelah shebang
        insert_position = 1
    else:
        # Sisipkan di awal
        insert_position = 0
    
    # Sisipkan section
    new_lines = lines[:insert_position] + [display_language_section] + lines[insert_position:]
    new_content = '\n'.join(new_lines)
    
    print("✅ Complete DISPLAY LANGUAGE section created successfully!")
    print(f"📍 Inserted at position after line {insert_position}")
    
    return new_content

def check_if_display_language_exists(content):
    """Cek apakah section DISPLAY LANGUAGE sudah ada - DENGAN VALIDASI YANG LEBIH BAIK"""
    
    # Cek apakah ada string DISPLAY_LANGUAGES
    if 'DISPLAY_LANGUAGES' not in content:
        return False
    
    # Cek apakah ada pattern dictionary yang valid
    pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
    match = re.search(pattern, content)
    
    if not match:
        return False
    
    # Cek apakah dictionary memiliki struktur yang benar dengan brace counting
    start_pos = match.end()
    brace_count = 1
    current_pos = start_pos
    
    while brace_count > 0 and current_pos < len(content):
        if content[current_pos] == '{':
            brace_count += 1
        elif content[current_pos] == '}':
            brace_count -= 1
        current_pos += 1
    
    # Jika brace_count == 0, berarti dictionary memiliki struktur yang valid
    return brace_count == 0

# ==================== FUNCTION CLEANING ====================

def remove_all_existing_functions(content):
    """Hapus SEMUA functions DISPLAY LANGUAGE yang ada"""
    
    print("🔍 Removing ALL existing display language functions...")
    
    # Pattern untuk menghapus SEMUA functions dari DISPLAY_LANG sampai functions terakhir
    patterns_to_remove = [
        # Hapus dari DISPLAY_LANG variable sampai akhir section
        r'# Global variable for display language\s*\nDISPLAY_LANG[^\n]*\n.*?def set_display_language\(.*?\):.*?def t\(.*?\):.*?def get_display_language\(.*?\):.*?def get_available_languages\(.*?\):.*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)\s*\n',
        # Pattern individual functions (jika terpisah)
        r'def set_display_language\(.*?\):.*?(?=def |\n\n|\Z)',
        r'def t\(.*?\):.*?(?=def |\n\n|\Z)', 
        r'def get_display_language\(.*?\):.*?(?=def |\n\n|\Z)',
        r'def get_available_languages\(.*?\):.*?(?=def |\n\n|\Z)',
        # Hapus DISPLAY_LANG variable
        r'# Global variable for display language\s*\nDISPLAY_LANG[^\n]*\n',
    ]
    
    original_length = len(content)
    removed_count = 0
    
    for pattern in patterns_to_remove:
        before_len = len(content)
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        after_len = len(content)
        count = (before_len - after_len) // 1000  # Estimate count
        if count > 0:
            print(f"   🗑️ Removed pattern: {count} blocks")
            removed_count += count
    
    print(f"📊 Content reduced: {original_length} -> {len(content)} characters")
    
    return content

def insert_clean_functions(content):
    """Sisipkan functions yang bersih setelah DISPLAY_LANGUAGES"""
    
    print("🔍 Inserting clean functions...")
    
    # Template functions yang bersih dengan spacing tepat
    clean_functions = '''# Global variable for display language
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
    """Translation function for notifications - will be populated globally"""
    global DISPLAY_LANG
    try:
        # Try to get translation from current display language
        if DISPLAY_LANG in DISPLAY_LANGUAGES and key in DISPLAY_LANGUAGES[DISPLAY_LANG]:
            return DISPLAY_LANGUAGES[DISPLAY_LANG][key].format(**kwargs)
        # Fallback to English
        elif key in DISPLAY_LANGUAGES["en"]:
            return DISPLAY_LANGUAGES["en"][key].format(**kwargs)
        else:
            # Return key as placeholder - will be filled globally
            return f"{key}"
    except Exception as e:
        # Return key on error - will be filled globally
        return f"{key}"

def get_display_language():
    """Get current display language"""
    return DISPLAY_LANG

def get_available_languages():
    """Get list of available languages"""
    return list(DISPLAY_LANGUAGES.keys())

'''
    
    # FIXED: Pattern yang lebih akurat untuk menangkap akhir dictionary
    dict_pattern = r'(DISPLAY_LANGUAGES\s*=\s*\{.*?\n\s*\}\n\n)'
    dict_match = re.search(dict_pattern, content, re.DOTALL)
    
    if not dict_match:
        print("❌ DISPLAY_LANGUAGES dictionary not found!")
        return content, False
    
    dict_end = dict_match.end()
    print(f"📍 Inserting after DISPLAY_LANGUAGES at position {dict_end}")
    
    # Sisipkan functions bersih
    new_content = content[:dict_end] + clean_functions + content[dict_end:]
    print("✅ Clean functions inserted")
    
    return new_content, True

# ==================== SPACING FIX ====================

def fix_spacing_after_section_improved(content):
    """Perbaiki spacing dengan method yang lebih reliable"""
    
    print("🔍 Fixing spacing with improved method...")
    
    # Method 1: Regex replacement yang lebih agresif
    section_end_pattern = r'(def get_available_languages\(\):\s*"""Get list of available languages"""\s*return list\(DISPLAY_LANGUAGES\.keys\(\)\)\s*\n)(\s*\n)+'
    new_content = re.sub(section_end_pattern, r'\1\n\n', content, flags=re.DOTALL)
    
    # Method 2: Jika regex tidak bekerja, gunakan manual method yang lebih robust
    if new_content == content:
        print("🔄 Using robust manual spacing fix...")
        lines = content.split('\n')
        cleaned_lines = []
        in_section = False
        section_end_found = False
        empty_lines_count = 0
        
        for i, line in enumerate(lines):
            # Deteksi akhir section
            if 'return list(DISPLAY_LANGUAGES.keys())' in line:
                in_section = False
                section_end_found = True
                cleaned_lines.append(line)
                # Tambahkan tepat 2 empty lines setelah section
                cleaned_lines.append('')
                cleaned_lines.append('')
                empty_lines_count = 0
                continue
            
            # Jika section sudah berakhir, hitung empty lines
            if section_end_found:
                if line.strip() == '':
                    empty_lines_count += 1
                    # Skip empty lines berlebih
                    if empty_lines_count <= 2:
                        cleaned_lines.append(line)
                else:
                    # Ketemu konten non-empty, reset state
                    section_end_found = False
                    empty_lines_count = 0
                    cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)
        
        new_content = '\n'.join(cleaned_lines)
    
    # Method 3: Final cleanup untuk memastikan spacing tepat
    # Hapus multiple empty lines berlebih di seluruh file
    new_content = re.sub(r'\n\n\n+', '\n\n', new_content)
    
    # Validasi perbaikan
    original_spacing = count_empty_lines_after_section(content)
    new_spacing = count_empty_lines_after_section(new_content)
    
    if original_spacing != new_spacing:
        print(f"✅ Fixed spacing: {original_spacing} -> {new_spacing} empty lines")
    else:
        print(f"ℹ️ Spacing unchanged: {new_spacing} empty lines")
    
    return new_content

def count_empty_lines_after_section(content):
    """Hitung empty lines setelah section DISPLAY LANGUAGE"""
    
    # Cari section DISPLAY LANGUAGE
    section_pattern = r'# -+\s*DISPLAY LANGUAGE SETTINGS\s*-+(.*?)def get_available_languages\(\):.*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)'
    section_match = re.search(section_pattern, content, re.DOTALL)
    
    if not section_match:
        return -1
    
    # Hitung empty lines setelah section
    after_section = content[section_match.end():]
    empty_lines_after = 0
    
    for line in after_section.split('\n'):
        if line.strip() == '':
            empty_lines_after += 1
        else:
            break
    
    return empty_lines_after

# ==================== VALIDATION FUNCTIONS ====================

def count_functions(content):
    """Hitung jumlah setiap function"""
    
    counts = {
        'DISPLAY_LANG vars': len(re.findall(r'DISPLAY_LANG\s*=\s*"', content)),
        'set_display_language': len(re.findall(r'def set_display_language\(', content)),
        't function': len(re.findall(r'def t\(', content)),
        'get_display_language': len(re.findall(r'def get_display_language\(', content)),
        'get_available_languages': len(re.findall(r'def get_available_languages\(', content)),
    }
    
    return counts

def validate_single_functions(content):
    """Validasi bahwa hanya ada SATU instance setiap function"""
    
    print("\n🔍 Validating function counts...")
    
    counts = count_functions(content)
    
    all_valid = True
    for func, count in counts.items():
        status = "✅" if count == 1 else "❌"
        print(f"   {status} {func}: {count}")
        if count != 1:
            all_valid = False
    
    # Juga cek konten yang penting
    content_checks = {
        'DISPLAY_LANG = "en"': 'DISPLAY_LANG = "en"' in content,
        'set_display_language function': 'def set_display_language(lang_code):' in content,
        't function with params': 'def t(key, **kwargs):' in content,
        'get_display_language function': 'def get_display_language():' in content,
        'get_available_languages function': 'def get_available_languages():' in content,
    }
    
    print("\n🔍 Validating function content...")
    for check, exists in content_checks.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {check}")
        if not exists:
            all_valid = False
    
    return all_valid

def validate_languages_final(content, expected_languages):
    """Validasi akhir untuk languages"""
    
    print("\n🔍 Final language validation...")
    
    existing_languages = check_existing_languages(content)
    
    # Cek apakah semua bahasa yang diharapkan ada
    missing_languages = [lang for lang in expected_languages if lang not in existing_languages]
    extra_languages = [lang for lang in existing_languages if lang not in expected_languages]
    
    if missing_languages:
        print(f"❌ Missing {len(missing_languages)} languages: {', '.join(missing_languages)}")
        return False
    elif extra_languages:
        print(f"❌ Extra languages found: {', '.join(extra_languages)}")
        return False
    else:
        print(f"✅ All {len(expected_languages)} expected languages are present: {', '.join(expected_languages)}")
        return True

def check_spacing_around_section(content):
    """Cek jarak spasi di sekitar section DISPLAY LANGUAGE"""
    
    print("🔍 Checking spacing around DISPLAY LANGUAGE section...")
    
    # Cari section DISPLAY LANGUAGE
    section_pattern = r'# -+\s*DISPLAY LANGUAGE SETTINGS\s*-+(.*?)def get_available_languages\(\):.*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)'
    section_match = re.search(section_pattern, content, re.DOTALL)
    
    if not section_match:
        print("❌ DISPLAY LANGUAGE section not found")
        return False
    
    # Hitung empty lines setelah section
    after_section = content[section_match.end():]
    empty_lines_after = 0
    lines_checked = 0
    
    for line in after_section.split('\n'):
        lines_checked += 1
        if lines_checked > 10:
            break
        if line.strip() == '':
            empty_lines_after += 1
        else:
            break
    
    print(f"📊 Empty lines after section: {empty_lines_after}")
    
    if empty_lines_after == 2:
        print("✅ Perfect spacing after section: 2 empty lines")
        return True
    else:
        print(f"⚠️ Incorrect spacing: {empty_lines_after} lines (should be 2)")
        return False

# ==================== MAIN EXECUTION ====================

def main():
    if len(sys.argv) < 2:
        print("Usage: python insert_section.py <file.py>")
        print("Example: python insert_section.py multidoc_translator.py")
        sys.exit(1)
    
    target_file = sys.argv[1]
    
    if not os.path.exists(target_file):
        print(f"❌ File {target_file} not found")
        sys.exit(1)
    
    print(f"🎯 Target: {target_file}")
    print("=" * 60)
    
    # Baca file
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    backup_path = target_file + '.ultimate_backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📁 Backup created: {backup_path}")
    
    # ========== STEP 0: CHECK IF DISPLAY LANGUAGE SECTION EXISTS ==========
    print("\n🔄 STEP 0: Checking if DISPLAY LANGUAGE section exists...")
    section_exists = check_if_display_language_exists(content)
    
    if not section_exists:
        print("❌ DISPLAY LANGUAGE section not found!")
        print("🆕 The file does not have a valid DISPLAY LANGUAGE section.")
        create_choice = input("Do you want to create complete DISPLAY LANGUAGE section from scratch? (y/N): ").strip().lower()
        if create_choice == 'y':
            content = create_complete_display_section_from_scratch(content)
            print("✅ DISPLAY LANGUAGE section created successfully!")
            # Setelah membuat section, langsung lanjut ke STEP 1
        else:
            print("ℹ️ Skipping DISPLAY LANGUAGE section creation")
            print("❌ Cannot proceed without DISPLAY LANGUAGE section. Exiting.")
            return
    else:
        print("✅ DISPLAY LANGUAGE section found!")
    
    # ========== STEP 1: SELECT LANGUAGES TO KEEP ==========
    print("\n🔄 STEP 1: Language selection")
    
    # Tampilkan bahasa yang sudah ada
    existing_languages = check_existing_languages(content)
    
    if existing_languages:
        print(f"\n📊 Currently have {len(existing_languages)} languages")
        
        # Tanya user apakah ingin memilih bahasa tertentu
        print("\n🎯 Do you want to:")
        print("   1. Keep all current languages")
        print("   2. Select specific languages to keep")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "2":
            print("\n🔄 Let's select which languages to keep...")
            show_all_language_options()
            selected_languages = get_language_selection()
            
            if selected_languages:
                print(f"\n🎯 You selected to keep {len(selected_languages)} languages: {', '.join(selected_languages)}")
                content = replace_all_languages_in_content(content, selected_languages)
                expected_languages = selected_languages
            else:
                print("ℹ️ No languages selected, keeping all current languages")
                expected_languages = existing_languages
        else:
            print("ℹ️ Keeping all current languages")
            expected_languages = existing_languages
    else:
        print("❌ No languages found in DISPLAY_LANGUAGES")
        expected_languages = []
    
    # ========== STEP 2: CLEAN FUNCTIONS ==========
    print("\n🔄 STEP 2: Cleaning functions...")
    
    # Hitung sebelum
    print("📊 BEFORE function cleaning:")
    before_counts = count_functions(content)
    for func, count in before_counts.items():
        print(f"   {func}: {count}")
    
    # Hapus functions lama
    content = remove_all_existing_functions(content)
    
    # Insert functions baru
    content, success = insert_clean_functions(content)
    if not success:
        print("❌ Failed to insert clean functions")
        return
    
    # ========== STEP 3: FIX SPACING ==========
    print("\n🔄 STEP 3: Fixing spacing with improved method...")
    content = fix_spacing_after_section_improved(content)
    
    # ========== STEP 4: VALIDATE EVERYTHING ==========
    print("\n🔄 STEP 4: Final validation...")
    
    # Validasi functions
    functions_ok = validate_single_functions(content)
    
    # Validasi spacing
    spacing_ok = check_spacing_around_section(content)
    
    # Validasi languages
    languages_ok = validate_languages_final(content, expected_languages)
    
    # ========== STEP 5: FINAL SPACING ADJUSTMENT ==========
    if not spacing_ok:
        print("\n🔄 STEP 5: Manual spacing adjustment...")
        # Manual adjustment untuk spacing
        lines = content.split('\n')
        cleaned_lines = []
        section_found = False
        
        for line in lines:
            if 'return list(DISPLAY_LANGUAGES.keys())' in line:
                section_found = True
                cleaned_lines.append(line)
                # Tambahkan tepat 2 empty lines
                cleaned_lines.append('')
                cleaned_lines.append('')
                continue
            
            if section_found:
                # Skip empty lines berlebih setelah section
                if line.strip() != '':
                    cleaned_lines.append(line)
                    section_found = False
            else:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Validasi ulang spacing
        spacing_ok = check_spacing_around_section(content)
        print(f"✅ Manual spacing adjustment completed: {spacing_ok}")
    
    # Tulis file final
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # ========== FINAL REPORT ==========
    print("\n📊 FINAL RESULT:")
    print("=" * 60)
    
    if functions_ok:
        print("✅ FUNCTIONS: Clean and single instance")
    else:
        print("❌ FUNCTIONS: Duplicates or missing functions")
    
    if spacing_ok:
        print("✅ SPACING: Perfect 2 empty lines")
    else:
        print("❌ SPACING: Incorrect spacing")
    
    if languages_ok:
        print(f"✅ LANGUAGES: {len(expected_languages)} languages present as expected")
    else:
        print("❌ LANGUAGES: Language count mismatch")
    
    print("=" * 60)
    
    if functions_ok and spacing_ok and languages_ok:
        print("🎉 ULTIMATE COMPLETE SUCCESSFUL!")
        print(f"   • {len(expected_languages)} languages present as selected")
        print("   • Clean functions without duplicates")
        print("   • Perfect spacing (2 empty lines)")
        print("   • File is perfectly optimized!")
    else:
        print("⚠️ Some issues remain - check above for details")
    
    print(f"💾 Backup: {backup_path}")

if __name__ == "__main__":
    main()