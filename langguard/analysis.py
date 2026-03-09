#!/usr/bin/env python3
"""
LangGuard - Analysis Functions Module
DENGAN FALLBACK STRATEGY
"""

import os
import re
import sys
from pathlib import Path

# ✅ GUNAKAN language_utils untuk menghindari circular import
try:
    from .language_utils import (
        get_all_supported_languages,
        get_correct_language_order,
        get_existing_languages_from_content,
        extract_english_phrases
    )
except ImportError:
    from language_utils import (
        get_all_supported_languages,
        get_correct_language_order,
        get_existing_languages_from_content,
        extract_english_phrases
    )

# ✅ PERBAIKAN: Pindahkan check_internet_connection ke atas
def check_internet_connection():
    """Cek koneksi internet untuk translation"""
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False

# ✅ PERBAIKAN: Tambahkan fallback strategy untuk analysis
def fallback_for_analysis(target_file):
    """Fallback khusus untuk analysis command"""
    try:
        from .fallback_strategy import fallback_for_check
    except ImportError:
        from fallback_strategy import fallback_for_check
    
    return fallback_for_check(target_file)

def is_valid_display_languages_section(content):
    """Check if content has a valid DISPLAY_LANGUAGES section"""
    if 'DISPLAY_LANGUAGES = {' not in content:
        return False
    
    # Verifikasi struktur dasar
    dict_start = content.find('DISPLAY_LANGUAGES = {')
    dict_end = content.find('}', dict_start)
    
    if dict_end == -1:
        return False
    
    # Harus ada minimal 1 fungsi terkait
    has_required_functions = any(func in content for func in [
        'set_display_language',
        'def t(',
        'DISPLAY_LANG =',
        'get_display_language'
    ])
    
    return has_required_functions


def is_valid_js_i18n_section(content):
    """Check if content has basic JS i18n structure (LANG_ORDER + I18N)."""
    return (
        'const LANG_ORDER' in content and
        'const I18N' in content and
        re.search(r'\ben\s*:\s*\{', content) is not None
    )


def extract_js_i18n_languages(content):
    """Extract language keys from JavaScript I18N object."""
    js_langs = re.findall(r'\b([a-z]{2})\s*:\s*\{', content)
    ordered = []
    for code in js_langs:
        if code not in ordered:
            ordered.append(code)
    return ordered


def extract_js_lang_keys(content, lang_code):
    """Extract top-level key names for a given language in JS I18N object."""
    lang_match = re.search(rf'\b{lang_code}\s*:\s*\{{', content)
    if not lang_match:
        return set()

    start = lang_match.end() - 1  # position of '{'
    brace_count = 0
    in_string = False
    escape_next = False
    quote_char = ''
    block_chars = []

    for i in range(start, len(content)):
        ch = content[i]

        if escape_next:
            block_chars.append(ch)
            escape_next = False
            continue

        if in_string:
            block_chars.append(ch)
            if ch == '\\':
                escape_next = True
            elif ch == quote_char:
                in_string = False
                quote_char = ''
            continue

        if ch in ('"', "'"):
            in_string = True
            quote_char = ch
            block_chars.append(ch)
            continue

        if ch == '{':
            brace_count += 1
            if brace_count > 1:
                block_chars.append(ch)
            continue

        if ch == '}':
            brace_count -= 1
            if brace_count == 0:
                break
            block_chars.append(ch)
            continue

        if brace_count >= 1:
            block_chars.append(ch)

    lang_block = ''.join(block_chars)

    # Split properties at top-level commas (ignore nested objects/arrays/strings)
    props = []
    current = []
    obj_depth = 0
    arr_depth = 0
    paren_depth = 0
    in_string = False
    escape_next = False
    quote_char = ''

    for ch in lang_block:
        if escape_next:
            current.append(ch)
            escape_next = False
            continue

        if in_string:
            current.append(ch)
            if ch == '\\':
                escape_next = True
            elif ch == quote_char:
                in_string = False
                quote_char = ''
            continue

        if ch in ('"', "'"):
            in_string = True
            quote_char = ch
            current.append(ch)
            continue

        if ch == '{':
            obj_depth += 1
            current.append(ch)
            continue
        if ch == '}':
            obj_depth = max(0, obj_depth - 1)
            current.append(ch)
            continue
        if ch == '[':
            arr_depth += 1
            current.append(ch)
            continue
        if ch == ']':
            arr_depth = max(0, arr_depth - 1)
            current.append(ch)
            continue
        if ch == '(':
            paren_depth += 1
            current.append(ch)
            continue
        if ch == ')':
            paren_depth = max(0, paren_depth - 1)
            current.append(ch)
            continue

        if ch == ',' and obj_depth == 0 and arr_depth == 0 and paren_depth == 0:
            prop = ''.join(current).strip()
            if prop:
                props.append(prop)
            current = []
            continue

        current.append(ch)

    tail = ''.join(current).strip()
    if tail:
        props.append(tail)

    keys = []
    for prop in props:
        m = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:', prop)
        if m:
            keys.append(m.group(1))
    return set(keys)


def extract_js_english_keys(content):
    """Extract top-level keys from `en: { ... }` in JS I18N object."""
    return extract_js_lang_keys(content, 'en')


def analyze_js_i18n_file(file_path):
    """Analyze JavaScript file that uses LANG_ORDER + I18N object."""
    print(f"🔍 Analyzing JavaScript i18n: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not is_valid_js_i18n_section(content):
            print("❌ JS i18n pattern not found. Expected: const LANG_ORDER + const I18N + en section")
            return False

        all_supported = get_all_supported_languages()
        existing_langs = extract_js_i18n_languages(content)
        missing_langs = [lang for lang in all_supported if lang not in existing_langs]

        print(f"📊 Language Analysis for JS file: {file_path}")
        print("=" * 60)
        print(f"✅ Total languages found: {len(existing_langs)}")
        print(f"🌍 Languages present: {', '.join(existing_langs)}")

        if missing_langs:
            print(f"⚠️  Missing languages ({len(missing_langs)}): {', '.join(missing_langs)}")
        else:
            print("✅ No missing languages")

        # Cek key coverage berdasarkan English
        english_keys = extract_js_english_keys(content)
        if not english_keys:
            print("⚠️  English (en) section has no detectable keys.")
            return True

        print(f"🔑 English key count: {len(english_keys)}")
        incomplete = []
        for lang in existing_langs:
            if lang == 'en':
                continue

            lang_keys = extract_js_lang_keys(content, lang)
            if not lang_keys:
                incomplete.append((lang, 0))
                continue

            if len(lang_keys) < len(english_keys):
                incomplete.append((lang, len(lang_keys)))

        if incomplete:
            print("⚠️  Languages with incomplete key coverage:")
            for lang, count in incomplete:
                print(f"   - {lang}: {count}/{len(english_keys)} keys")
        else:
            print("✅ All languages have key coverage equal to English")

        return True
    except Exception as e:
        print(f"❌ Error during JS analysis: {e}")
        return False

def get_js_incomplete_languages(content):
    """Return JS languages with key count lower than English reference."""
    english_keys = extract_js_english_keys(content)
    if not english_keys:
        return []

    incomplete = []
    for lang in extract_js_i18n_languages(content):
        if lang == 'en':
            continue
        lang_keys = extract_js_lang_keys(content, lang)
        if len(lang_keys) < len(english_keys):
            incomplete.append((lang, len(lang_keys), len(english_keys)))
    return incomplete

def get_js_suspicious_values(content):
    """Detect suspicious translated values in non-EN languages."""
    suspicious_patterns = [
        r'error\s*500',
        r"that.?s an error",
        r'<html',
        r'</html>',
        r'google',
        r'please try again later',
    ]

    susp = []
    en_keys = extract_js_english_keys(content)
    if not en_keys:
        return susp

    en_match = re.search(r'\ben\s*:\s*\{([\s\S]*?)\n\s*\}\s*,?', content)
    if not en_match:
        return susp
    en_content = en_match.group(1)

    for lang in extract_js_i18n_languages(content):
        if lang == 'en':
            continue

        lang_match = re.search(rf'\b{lang}\s*:\s*\{{([\s\S]*?)\n\s*\}}\s*,?', content)
        if not lang_match:
            continue

        lang_content = lang_match.group(1)
        for key in en_keys:
            vm = re.search(rf'\b{re.escape(key)}\s*:\s*"([\s\S]*?)"\s*(,|$)', lang_content)
            if not vm:
                continue
            value = vm.group(1)
            low = value.lower()

            en_vm = re.search(rf'\b{re.escape(key)}\s*:\s*"([\s\S]*?)"\s*(,|$)', en_content)
            en_value = en_vm.group(1) if en_vm else ''
            untouched_en = (
                value == en_value and
                len(re.findall(r'[A-Za-z]{3,}', en_value)) >= 3 and
                not re.search(r'https?://|`|\$\{|/api/|\.py|\.exe', en_value)
            )

            if any(re.search(p, low) for p in suspicious_patterns) or untouched_en:
                susp.append((lang, key, value[:80]))
    return susp

def should_check_file(file_path):
    """Tentukan apakah file harus diperiksa DISPLAY_LANGUAGES-nya"""
    
    # Hanya skip file-file utility LangGuard yang jelas-jelas template
    skip_files = {
        'setup.py', '__init__.py', 'test_', 'conftest.py',
        'template_utils.py', 'insert_section.py', 'add_languages.py',
        'repair_functions.py', 'analysis.py',
        'remove_languages.py', 'update_language.py', 'main.py'
    }
    
    filename = os.path.basename(file_path)
    
    # Jika file ada di list skip_files, berarti itu utility LangGuard
    is_langguard_utility = any(skip_file in filename for skip_file in skip_files)
    
    # Juga skip jika file berada di folder langguard/
    is_in_langguard_folder = 'langguard' in file_path.split(os.sep)
    
    return not (is_langguard_utility or is_in_langguard_folder)

def is_actual_display_section(content, file_path):
    """Versi yang lebih akurat - deteksi file aplikasi vs utility"""
    
    # Skip file utility LangGuard
    if not should_check_file(file_path):
        return False
    
    # Pattern yang lebih spesifik untuk aplikasi utama
    has_complete_structure = (
        'DISPLAY_LANGUAGES = {' in content and
        'DISPLAY_LANG = ' in content and
        'def t(' in content
    )
    
    # File dengan nama 'test.py' dianggap sebagai aplikasi utama
    is_main_app_file = (
        'test.py' in file_path or 
        'main.py' in file_path or
        'app.py' in file_path or
        'script.py' in file_path
    )
    
    return has_complete_structure or is_main_app_file

def check_file_quick(file_path):
    """Quick consistency check of DISPLAY_LANGUAGES in a file - DENGAN FALLBACK"""
    
    # Skip file-file utility/template
    if not should_check_file(file_path):
        print(f"ℹ️  Skipping utility/template file: {file_path}")
        return False
        
    print(f"🔍 Quick checking: {file_path}")
    
    # ✅ PERBAIKAN: Gunakan fallback strategy untuk handle file tanpa section
    if not fallback_for_analysis(file_path):
        return False  # File tidak ada atau user cancel generate section
    
    # Lanjut proses analysis normal (section sudah ada)
    print("🔄 Continuing with analysis process...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ✅ SEKARANG section sudah pasti ada (karena fallback)
        if 'DISPLAY_LANGUAGES' in content:
            # Skip jika ini bukan implementasi aktual
            if not is_actual_display_section(content, file_path):
                print(f"ℹ️  Skipping template file (no actual implementation): {file_path}")
                return False
                
            # ✅ GUNAKAN FUNGSI DARI language_utils
            existing_langs = get_existing_languages_from_content(content)
            all_supported = get_all_supported_languages()
            missing_langs = [lang for lang in all_supported if lang not in existing_langs]
            
            print(f"✅ Found {len(existing_langs)} languages: {', '.join(existing_langs)}")
            
            if missing_langs:
                print(f"❌ MISSING {len(missing_langs)} languages: {', '.join(missing_langs)}")
            
            # Cek urutan bahasa
            raw_langs = re.findall(r'"(\w+)":\s*\{', content)
            correct_order = get_correct_language_order()
            expected_order = [lang for lang in correct_order if lang in existing_langs]  # ✅ PERBAIKAN: gunakan existing_langs, bukan all_supported
            
            if raw_langs == expected_order:
                print("✅ Language order is correct!")
            else:
                print("⚠️  Language order is incorrect!")
                print(f"   Current: {', '.join(raw_langs)}")
                print(f"   Expected: {', '.join(expected_order)}")
            
            return True
        else:
            # ❌ Ini seharusnya tidak terjadi karena fallback sudah handle
            print("❌ Unexpected error: DISPLAY_LANGUAGES section not found after fallback")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def ask_translate_missing_phrases(file_path, inconsistent_langs):
    """Tanya user apakah ingin mentranslasi bahasa dengan phrases yang kurang/kosong"""
    if not inconsistent_langs:
        return False
    
    # ✅ PERBAIKAN: Cek English phrases SEBELUM menawarkan translasi
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        english_phrases = extract_english_phrases(content)
        if not english_phrases:
            print("❌ Cannot translate: English section is empty!")
            print("💡 Add English phrases first before translating other languages")
            return False
    except Exception as e:
        print(f"❌ Error checking English phrases: {e}")
        return False
    
    # ✅ PERBAIKAN: Cek koneksi internet SEBELUM menawarkan translasi
    if not check_internet_connection():
        print("❌ No internet connection! Translation requires internet access.")
        print("💡 Please check your internet connection and run 'langguard translate' later")
        return False
    
    # ✅ PERBAIKAN: Filter bahasa yang benar-benar perlu diterjemahkan (kecuali English)
    translatable_langs = {}
    for lang_code, stats in inconsistent_langs.items():
        if lang_code != "en":  # Skip English
            translatable_langs[lang_code] = stats
    
    if not translatable_langs:
        print("✅ No languages need translation")
        return False
    
    # Tampilkan hanya bahasa yang bisa diterjemahkan
    print(f"\n⚠️  Found {len(translatable_langs)} languages that need translation:")
    
    empty_langs = []
    incomplete_langs = {}
    
    for lang_code, stats in translatable_langs.items():
        if stats['count'] == 0:
            empty_langs.append(lang_code)
        else:
            incomplete_langs[lang_code] = stats
    
    if empty_langs:
        print(f"   - {len(empty_langs)} empty languages: {', '.join(empty_langs)}")
    
    if incomplete_langs:
        print(f"   - {len(incomplete_langs)} incomplete languages:")
        for lang_code, stats in incomplete_langs.items():
            print(f"     - {lang_code.upper()}: {stats['count']} phrases (expected: {stats['expected_count']})")
    
    # Hitung total phrases yang perlu diterjemahkan
    total_missing = 0
    for lang_code, stats in translatable_langs.items():
        total_missing += (stats['expected_count'] - stats['count'])
    
    if total_missing > 0:
        print(f"📝 Total phrases to translate: {total_missing}")
    
    # Konfirmasi dengan user
    while True:
        choice = input(f"\n👉 Do you want to auto-translate now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🎯 Running auto-translation...")
            try:
                # ✅ PERBAIKAN: Import dinamis dengan error handling
                try:
                    from translate import run_translate
                    run_translate(file_path)
                    return True
                except ImportError:
                    try:
                        from .translate import run_translate
                        run_translate(file_path)
                        return True
                    except ImportError:
                        print("❌ Cannot import translate module")
                        return False
            except Exception as e:
                print(f"❌ Translation error: {e}")
                return False
        elif choice in ['n', 'no', '']:
            print("ℹ️ Translation skipped.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

def ask_add_missing_languages(file_path, missing_langs):
    """Tanya user apakah ingin menambah bahasa yang missing"""
    if not missing_langs:
        return False
    
    print(f"\n⚠️  Found {len(missing_langs)} missing languages: {', '.join(missing_langs)}")
    
    while True:
        choice = input(f"👉 Do you want to add the missing languages now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🎯 Adding missing languages...")
            try:
                # ✅ IMPORT DINAMIS - hanya ketika benar-benar dibutuhkan
                try:
                    from add_languages import run_add_languages
                    success = run_add_languages(file_path)
                    return success
                except ImportError:
                    try:
                        from .add_languages import run_add_languages
                        success = run_add_languages(file_path)
                        return success
                    except ImportError:
                        print("❌ Cannot import add_languages module")
                        return False
            except Exception as e:
                print(f"❌ Error adding languages: {e}")
                return False
        elif choice in ['n', 'no', '']:
            print("ℹ️ Language addition skipped.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

def ask_translate_new_languages(file_path, new_languages):
    """Tanya user apakah ingin mentranslasi bahasa baru yang kosong"""
    if not new_languages:
        return False
    
    print(f"\n⚠️  Newly added languages have empty phrases: {', '.join(new_languages)}")
    
    while True:
        choice = input(f"👉 Do you want to auto-translate the new languages now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🎯 Running auto-translation for new languages...")
            try:
                try:
                    from translate import run_translate
                    run_translate(file_path)
                    return True
                except ImportError:
                    try:
                        from .translate import run_translate
                        run_translate(file_path)
                        return True
                    except ImportError:
                        print("❌ Cannot import translate module")
                        return False
            except Exception as e:
                print(f"❌ Translation error: {e}")
                return False
        elif choice in ['n', 'no', '']:
            print("ℹ️ Translation for new languages skipped.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

def run_translate_on_file(file_path):
    """Jalankan translate pada file tertentu"""
    try:
        try:
            from translate import run_translate
            run_translate(file_path)
            return True
        except ImportError:
            try:
                from .translate import run_translate
                run_translate(file_path)
                return True
            except ImportError:
                print(f"❌ Cannot import translate module for {file_path}")
                return False
    except Exception as e:
        print(f"❌ Translation error for {file_path}: {e}")
        return False

def add_all_missing_languages_to_file(file_path):
    """Tambahkan semua bahasa yang missing ke file secara otomatis"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ✅ GUNAKAN FUNGSI DARI language_utils
        existing_langs = get_existing_languages_from_content(content)
        all_supported = get_all_supported_languages()
        missing_langs = [lang for lang in all_supported if lang not in existing_langs]
        
        if not missing_langs:
            return True
        
        print(f"   ➕ {os.path.basename(file_path)}: Adding {len(missing_langs)} languages ({', '.join(missing_langs)})")
        
        # Backup file
        backup_path = file_path + ".auto_add_backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Template untuk bahasa baru
        templates = {
            "en": '    "en": {\n        # English translations will be added globally later\n    }',
            "pl": '    "pl": {\n        # Polski translations will be added globally later\n    }',
            "zh": '    "zh": {\n        # 中文 translations will be added globally later\n    }',
            "jp": '    "jp": {\n        # 日本語 translations will be added globally later\n    }',
            "de": '    "de": {\n        # Deutsch translations will be added globally later\n    }',
            "fr": '    "fr": {\n        # Français translations will be added globally later\n    }',
            "es": '    "es": {\n        # Español translations will be added globally later\n    }',
            "ru": '    "ru": {\n        # Pycckuñ translations will be added globally later\n    }',
            "pt": '    "pt": {\n        # Portugués translations will be added globally later\n    }',
            "id": '    "id": {\n        # Indonesia translations will be added globally later\n    }',
            "kr": '    "kr": {\n        # 한국어 translations will be added globally later\n    }'
        }

        # Cari section DISPLAY_LANGUAGES
        match = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{[\s\S]*?\n\}', content, re.DOTALL)
        if not match:
            print(f"      ❌ DISPLAY_LANGUAGES section not found")
            return False

        dict_content = match.group(0)
        before = content[:match.start()]
        after = content[match.end():]

        # Ekstrak bahasa yang sudah ada
        existing_lang_content = {}
        for lang in existing_langs:
            lang_pattern = rf'"{lang}":\s*\{{([\s\S]*?)\n    \}}'
            lang_match = re.search(lang_pattern, dict_content, re.DOTALL)
            if lang_match:
                existing_lang_content[lang] = f'    "{lang}": {{{lang_match.group(1)}\n    }}'
            else:
                existing_lang_content[lang] = templates.get(lang, f'    "{lang}": {{\n        # {lang.upper()} content\n    }}')
        
        # Gabungkan semua bahasa (yang sudah ada + yang baru)
        all_langs_combined = existing_langs + missing_langs
        correct_order = get_correct_language_order()
        final_langs = [lang for lang in correct_order if lang in all_langs_combined]

        # Bangun dictionary baru
        new_dict_content = 'DISPLAY_LANGUAGES = {\n'
        
        for i, lang_code in enumerate(final_langs):
            if i > 0:
                new_dict_content += ',\n'
            
            if lang_code in existing_lang_content:
                new_dict_content += existing_lang_content[lang_code]
            elif lang_code in templates:
                new_dict_content += templates[lang_code]
            else:
                new_dict_content += f'    "{lang_code}": {{\n        # {lang_code.upper()} translations\n    }}'
        
        new_dict_content += '\n}'

        # Gabungkan konten baru
        new_content = before + new_dict_content + after

        # Tulis file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"      ✅ Added {len(missing_langs)} languages successfully")
        return True
        
    except Exception as e:
        print(f"      ❌ Error adding languages: {e}")
        return False

def check_english_phrases(file_path):
    """Cek apakah bahasa Inggris memiliki phrases - FIXED VERSION"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern yang lebih akurat untuk mencari bagian bahasa Inggris
        en_pattern = r'"en":\s*\{([\s\S]*?)\n    \}'
        en_match = re.search(en_pattern, content, re.DOTALL)
        
        if not en_match:
            return False, 0
        
        en_content = en_match.group(1)
        
        # ✅ PERBAIKAN: Pattern yang lebih akurat untuk mencari phrases
        # Pattern 1: "key": "value"
        phrases1 = re.findall(r'"([^"]+)":\s*"([^"]*)"', en_content)
        # Pattern 2: "key": "value {placeholder}"
        phrases2 = re.findall(r'"([^"]+)":\s*"[^{]*\{[^}]*\}[^"]*"', en_content)
        
        all_phrases = set()
        # Hanya ambil key dari pattern 1 dan 2
        for key, value in phrases1:
            if key.strip():  # Pastikan key tidak kosong
                all_phrases.add(key)
        for key, value in phrases2:
            if key.strip():  # Pastikan key tidak kosong
                all_phrases.add(key)
        
        return len(all_phrases) > 0, len(all_phrases)
    
    except Exception as e:
        print(f"❌ Error checking English phrases in {file_path}: {e}")
        return False, 0

LANGUAGE_NAMES = {
    "en": "English", "pl": "Polski", "zh": "中文", "jp": "日本語",
    "de": "Deutsch", "fr": "Français", "es": "Español", "ru": "Pycckuñ",
    "pt": "Portugués", "id": "Indonesia", "kr": "한국어"
}

# analysis.py - perbaikan fungsi ask_fix_all_issues

def ask_fix_all_issues(files_with_missing_langs, files_with_empty_phrases):
    """Tanya user apakah ingin memperbaiki semua masalah di semua file"""
    total_issues = len(files_with_missing_langs) + len(files_with_empty_phrases)
    
    if total_issues == 0:
        return False
    
    print(f"\n📊 ISSUES SUMMARY:")
    print("=" * 50)
    
    if files_with_missing_langs:
        print(f"❌ {len(files_with_missing_langs)} files missing languages:")
        for file_path, missing_langs in files_with_missing_langs:
            # ✅ PERBAIKAN: Tampilkan dengan nama bahasa asli
            missing_display = []
            for lang_code in missing_langs:
                lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                missing_display.append(f"{lang_code} ({lang_name})")
            print(f"   - {os.path.basename(file_path)}: {', '.join(missing_display)}")
    
    if files_with_empty_phrases:
        print(f"⚠️  {len(files_with_empty_phrases)} files with empty phrases:")
        for file_path, empty_langs in files_with_empty_phrases:
            # ✅ PERBAIKAN: Tampilkan dengan nama bahasa asli
            empty_display = []
            for lang_code in empty_langs:
                lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                empty_display.append(f"{lang_code} ({lang_name})")
            print(f"   - {os.path.basename(file_path)}: {', '.join(empty_display)}")
    
    print("=" * 50)
    
    # ✅ PERBAIKAN: Cek file yang tidak memiliki English phrases dengan benar
    files_without_english = []
    all_files_to_check = list(set([fp for fp, _ in files_with_missing_langs] + [fp for fp, _ in files_with_empty_phrases]))
    
    for file_path in all_files_to_check:
        has_english, phrase_count = check_english_phrases(file_path)
        if not has_english:
            files_without_english.append(file_path)
    
    if files_without_english:
        print(f"\n⚠️  WARNING: {len(files_without_english)} files have no English phrases:")
        for file_path in files_without_english:
            # Tampilkan bahasa yang sebenarnya ada di file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                existing_langs = get_existing_languages_from_content(content)
                if existing_langs:
                    # ✅ PERBAIKAN: Tampilkan nama bahasa yang ada dengan konsisten
                    existing_lang_names = []
                    for lang_code in existing_langs:
                        lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                        existing_lang_names.append(f"{lang_code} ({lang_name})")
                    print(f"   - {os.path.basename(file_path)}: English missing (has: {', '.join(existing_lang_names)})")
                else:
                    print(f"   - {os.path.basename(file_path)}: No languages found")
            except Exception:
                print(f"   - {os.path.basename(file_path)}: Error reading file")
        print("   💡 Translation requires English phrases as reference")
    
    # Pertanyaan sederhana
    while True:
        choice = input(f"\n👉 Fix all issues automatically? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🎯 AUTO-FIX: Adding missing languages + Translating...")
            
            success_count_add = 0
            success_count_translate = 0
            
            # Step 1: Add semua bahasa yang missing ke semua file
            if files_with_missing_langs:
                print("\n📥 Adding missing languages to all files...")
                for file_path, missing_langs in files_with_missing_langs:
                    if add_all_missing_languages_to_file(file_path):
                        success_count_add += 1
            
            # Step 2: Translate semua file
            all_files_to_translate = list(set([fp for fp, _ in files_with_empty_phrases] + [fp for fp, _ in files_with_missing_langs]))
            
            if all_files_to_translate:
                print("\n🌍 Translating all files...")
                for file_path in all_files_to_translate:
                    print(f"   🔄 {os.path.basename(file_path)}: Translating...")
                    
                    # Cek dulu apakah file memiliki English phrases
                    has_english, phrase_count = check_english_phrases(file_path)
                    if not has_english:
                        # Tampilkan bahasa yang sebenarnya ada
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            existing_langs = get_existing_languages_from_content(content)
                            if existing_langs:
                                # ✅ PERBAIKAN: Tampilkan nama bahasa yang ada dengan konsisten
                                existing_lang_names = []
                                for lang_code in existing_langs:
                                    lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                                    existing_lang_names.append(f"{lang_code} ({lang_name})")
                                print(f"      ⚠️  Cannot translate - English missing (file has: {', '.join(existing_lang_names)})")
                            else:
                                print(f"      ⚠️  Cannot translate - No languages found")
                        except Exception:
                            print(f"      ⚠️  Cannot translate - Error reading file")
                        continue
                    
                    if run_translate_on_file(file_path):
                        success_count_translate += 1
                        print(f"      ✅ Translated successfully")
                    else:
                        print(f"      ❌ Failed to translate")
            
            print(f"\n🎯 AUTO-FIX COMPLETED:")
            if files_with_missing_langs:
                print(f"   ✅ Languages added: {success_count_add}/{len(files_with_missing_langs)} files")
            print(f"   ✅ Files translated: {success_count_translate}/{len(all_files_to_translate)} files")
            
            if files_without_english:
                print(f"   ⚠️  Files skipped (no English phrases): {len(files_without_english)}")
                for file_path in files_without_english:
                    # Tampilkan bahasa yang sebenarnya ada
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        existing_langs = get_existing_languages_from_content(content)
                        if existing_langs:
                            existing_lang_names = []
                            for lang_code in existing_langs:
                                lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                                existing_lang_names.append(f"{lang_code} ({lang_name})")
                            print(f"      - {os.path.basename(file_path)} (has: {', '.join(existing_lang_names)})")
                        else:
                            print(f"      - {os.path.basename(file_path)} (no languages)")
                    except Exception:
                        print(f"      - {os.path.basename(file_path)}")
            
            return True
            
        elif choice in ['n', 'no', '']:
            print("ℹ️ Auto-fix skipped. No changes were made.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

def analyze_file(file_path):
    """Detailed analysis of DISPLAY_LANGUAGES section / JS I18N - DENGAN FALLBACK STRATEGY"""

    # JS support (non-destructive, read-only)
    if file_path.endswith('.js'):
        return analyze_js_i18n_file(file_path)

    # Skip file-file utility/template
    if not should_check_file(file_path):
        print(f"ℹ️  Skipping utility/template file: {file_path}")
        return False
        
    print(f"🔍 Analyzing: {file_path}")
    
    # ✅ PERBAIKAN: Gunakan fallback strategy untuk handle file tanpa section
    if not fallback_for_analysis(file_path):
        return False  # File tidak ada atau user cancel generate section
    
    # Lanjut proses analysis normal (section sudah ada)
    print("🔄 Continuing with detailed analysis process...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ✅ SEKARANG section sudah pasti ada (karena fallback)
        if 'DISPLAY_LANGUAGES' in content:
            # Skip jika ini bukan implementasi aktual
            if not is_actual_display_section(content, file_path):
                print(f"ℹ️  Skipping template file (no actual implementation): {file_path}")
                return False
            
            # ✅ PERBAIKAN: CEK ENGLISH PHRASES DI AWAL SEBELUM ANALISIS LAINNYA
            english_phrases = extract_english_phrases(content)
            english_empty = len(english_phrases) == 0
            
            if english_empty:
                print("❌ CRITICAL ERROR: No English phrases found in DISPLAY_LANGUAGES!")
                print("💡 English phrases are required as reference for translation")
                print("🔧 Action: Manually add English phrases to the 'en' section")
                print("")
                print("   Example:")
                print('   "en": {')
                print('       "hello": "Hello",')
                print('       "world": "World"')
                print('   }')
                print("")
                print("💡 After adding English phrases, run 'langguard translate' again")
                return False  # HENTIKAN ANALISIS DI SINI
            
            # ✅ GUNAKAN FUNGSI DARI language_utils
            existing_langs = get_existing_languages_from_content(content)
            all_supported = get_all_supported_languages()
            missing_langs = [lang for lang in all_supported if lang not in existing_langs]
            
            print(f"📊 Language Analysis for: {file_path}")
            print("=" * 60)
            print(f"✅ Total languages found: {len(existing_langs)}")
            print(f"🌍 Languages present: {', '.join(existing_langs)}")
            
            # ✅ PERBAIKAN: Cek apakah semua bahasa memiliki phrases
            lang_stats = {}
            all_phrases = set()
            english_phrases_count = 0
            
            # Hitung phrases untuk setiap bahasa
            for lang in existing_langs:
                lang_pattern = rf'"{lang}":\s*\{{(.*?)\n    \}}'
                lang_match = re.search(lang_pattern, content, re.DOTALL)
                if lang_match:
                    lang_content = lang_match.group(1)
                    
                    # ✅ PERBAIKAN: Pattern yang lebih akurat untuk mencari phrases
                    # Pattern 1: "key": "value"
                    phrases1 = re.findall(r'"([^"]+)":\s*"([^"]*)"', lang_content)
                    # Pattern 2: "key": "value {placeholder}"
                    phrases2 = re.findall(r'"([^"]+)":\s*"[^{]*\{[^}]*\}[^"]*"', lang_content)
                    # Pattern 3: "key": value (tanpa quotes)
                    phrases3 = re.findall(r'"([^"]+)":\s*[^",\n][^,\n]*', lang_content)
                    
                    all_phrases_for_lang = set()
                    # Hanya ambil key dari pattern 1 dan 2
                    for key, value in phrases1:
                        all_phrases_for_lang.add(key)
                    for key, value in phrases2:
                        all_phrases_for_lang.add(key)
                    # Untuk pattern 3, ambil langsung key
                    all_phrases_for_lang.update(phrases3)
                    
                    lang_stats[lang] = {
                        'count': len(all_phrases_for_lang),
                        'phrases': all_phrases_for_lang
                    }
                    
                    # Simpan jumlah phrases bahasa Inggris sebagai referensi
                    if lang == "en":
                        english_phrases_count = len(all_phrases_for_lang)
                    
                    all_phrases.update(all_phrases_for_lang)
            
            # ✅ PERBAIKAN KHUSUS: Deteksi bahasa dengan phrases kosong ATAU kurang dari bahasa Inggris
            empty_languages = []
            incomplete_languages = {}  # Bahasa yang punya phrases tapi kurang dari English
            
            for lang in existing_langs:
                phrase_count = lang_stats.get(lang, {}).get('count', 0)
                
                if phrase_count == 0:
                    empty_languages.append(lang)
                elif lang != "en" and phrase_count < english_phrases_count:
                    incomplete_languages[lang] = {
                        'current_count': phrase_count,
                        'expected_count': english_phrases_count,
                        'missing_count': english_phrases_count - phrase_count
                    }
            
            # ✅ PERBAIKAN: Tampilkan status English secara khusus
            english_empty = "en" in empty_languages
            if english_empty:
                print("❌ CRITICAL: English section is empty!")
                print("   💡 English phrases are required as reference for translation")
                print("   🔧 Action: Manually add English phrases to enable translation")
                print("")
            
            if missing_langs:
                print(f"❌ MISSING languages: {', '.join(missing_langs)}")
                print(f"💡 Expected {len(all_supported)} languages, but only {len(existing_langs)} found")
            elif empty_languages or incomplete_languages:
                # ✅ HANYA tampilkan pesan jika ada bahasa kosong ATAU incomplete
                if empty_languages:
                    # Filter English dari daftar empty languages untuk pesan
                    empty_non_english = [lang for lang in empty_languages if lang != "en"]
                    if empty_non_english:
                        print(f"⚠️  {len(empty_non_english)} languages have empty phrases: {', '.join(empty_non_english)}")
                
                if incomplete_languages:
                    print(f"⚠️  {len(incomplete_languages)} languages have incomplete phrases:")
                    for lang, stats in incomplete_languages.items():
                        print(f"   - {lang.upper()}: {stats['current_count']}/{stats['expected_count']} phrases (missing {stats['missing_count']})")
                
                # ✅ PERBAIKAN: HANYA tawarkan translate jika English memiliki phrases
                languages_need_translation = []
                if not english_empty:  # Hanya jika English tidak kosong
                    for lang in empty_languages + list(incomplete_languages.keys()):
                        if lang != "en":  # Jangan include English
                            languages_need_translation.append(lang)
                
                if languages_need_translation:
                    print(f"💡 Run 'langguard translate {file_path}' to fix {len(languages_need_translation)} languages")
                else:
                    if english_empty:
                        print("💡 Add English phrases first before translating other languages")
                    else:
                        print("🎉 All languages have complete phrases!")
            else:
                print(f"🎉 All {len(all_supported)} supported languages are present and have complete phrases!")
            
            # Analisis urutan
            raw_langs = re.findall(r'"(\w+)":\s*\{', content)
            correct_order = get_correct_language_order()
            
            print(f"📋 Current order: {', '.join(raw_langs)}")
            print(f"🎯 Expected complete order: {', '.join(correct_order)}")
            
            # Cek urutan untuk bahasa yang ada
            expected_order_for_existing = [lang for lang in correct_order if lang in existing_langs]
            
            if raw_langs == expected_order_for_existing:
                print("✅ ORDER: Correct for existing languages")
            else:
                print("❌ ORDER: Incorrect")
            
            # Analisis detail setiap bahasa
            print("\n📝 Detailed Analysis:")
            
            for lang in existing_langs:
                phrase_count = lang_stats.get(lang, {}).get('count', 0)
                phrases_list = lang_stats.get(lang, {}).get('phrases', set())
                
                # Tampilkan status dengan emoji yang sesuai
                if phrase_count == 0:
                    status = "🔴"
                elif phrase_count < english_phrases_count and lang != "en":
                    status = "🟡"
                else:
                    status = "🟢"
                
                print(f"   {status} {lang.upper()}: {phrase_count} phrases")
                
                # Tampilkan phrases yang ditemukan untuk bahasa ini
                if phrases_list:
                    print(f"      Phrases: {', '.join(sorted(phrases_list))}")
            
            # Cek konsistensi
            inconsistent_langs = {}
            if lang_stats:
                # Cari jumlah phrases terbanyak sebagai expected count
                phrase_counts = [stats['count'] for stats in lang_stats.values()]
                max_count = max(phrase_counts) if phrase_counts else 0
                
                for lang, stats in lang_stats.items():
                    if stats['count'] != max_count and stats['count'] > 0:
                        lang_stats[lang]['expected_count'] = max_count
                        inconsistent_langs[lang] = lang_stats[lang]
                    elif stats['count'] == 0:
                        lang_stats[lang]['expected_count'] = max_count
                        inconsistent_langs[lang] = lang_stats[lang]
                
                if len(set(phrase_counts)) == 1:
                    print(f"🎉 CONSISTENCY: Perfect! All languages have {phrase_counts[0]} phrases")
                else:
                    print("⚠️  CONSISTENCY: Inconsistent phrase counts!")
                    for lang, stats in lang_stats.items():
                        expected_info = f" (expected: {max_count})" if lang in inconsistent_langs else ""
                        print(f"   {lang.upper()}: {stats['count']} phrases{expected_info}")
            
            # Cek coverage
            if all_phrases:
                print(f"📚 Total unique phrases: {len(all_phrases)}")
                print(f"🔍 Unique phrases found: {', '.join(sorted(all_phrases))}")
            
            # Cek fungsi
            required_functions = [
                'set_display_language',
                't', 
                'get_display_language',
                'get_available_languages'
            ]
            missing_functions = []
            for func in required_functions:
                if f'def {func}(' not in content:
                    missing_functions.append(func)
            
            if missing_functions:
                print(f"❌ MISSING FUNCTIONS: {', '.join(missing_functions)}")
            else:
                print("✅ FUNCTIONS: All required functions present")
            
            print("=" * 60)
            
            # ✅ PERBAIKAN: Tawarkan perbaikan interaktif berdasarkan masalah yang ditemukan
            actions_taken = False
            
            # 1. Tawarkan tambah bahasa yang missing
            if missing_langs:
                if ask_add_missing_languages(file_path, missing_langs):
                    actions_taken = True
                    # Setelah menambah bahasa, refresh data untuk analisis selanjutnya
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    existing_langs = get_existing_languages_from_content(content)
                    raw_langs = re.findall(r'"(\w+)":\s*\{', content)
                    expected_order_for_existing = [lang for lang in correct_order if lang in existing_langs]
            
            # 2. ✅ PERBAIKAN: Tawarkan translasi HANYA jika English memiliki phrases
            # (Kita sudah cek di awal, jadi pasti English tidak kosong)
            languages_need_translation = []
            
            for lang in existing_langs:
                if lang == "en":
                    continue
                    
                phrase_count = lang_stats.get(lang, {}).get('count', 0)
                if phrase_count == 0 or (english_phrases_count > 0 and phrase_count < english_phrases_count):
                    languages_need_translation.append(lang)
            
            if languages_need_translation:
                # Buat inconsistent_langs structure untuk fungsi yang ada
                inconsistent_langs = {}
                for lang in languages_need_translation:
                    current_count = lang_stats.get(lang, {}).get('count', 0)
                    inconsistent_langs[lang] = {
                        'count': current_count,
                        'expected_count': english_phrases_count
                    }
                
                if ask_translate_missing_phrases(file_path, inconsistent_langs):
                    actions_taken = True
            
            # 3. Jika tidak ada masalah atau user memilih skip semua
            has_issues = (missing_langs or 
                         len([lang for lang in empty_languages if lang != "en"]) > 0 or 
                         incomplete_languages or 
                         raw_langs != expected_order_for_existing)
            
            if not actions_taken and not has_issues:
                print("\n🎉 No issues found - file is in perfect condition!")
            elif not actions_taken:
                print("\nℹ️ Analysis completed. No changes were made.")
            
            return True
        else:
            # ❌ Ini seharusnya tidak terjadi karena fallback sudah handle
            print("❌ Unexpected error: DISPLAY_LANGUAGES section not found after fallback")
            return False
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def list_files(quiet=False, search_subfolders=True, target_path='.'):
    """List files with DISPLAY_LANGUAGES/JS I18N - recursive from target path."""
    if not quiet:
        print("🔍 Searching for files with DISPLAY_LANGUAGES...")
        if search_subfolders:
            print("📁 Searching in current folder and all subfolders...")
        else:
            print("📁 Searching in current folder only...")

    if not os.path.exists(target_path):
        if not quiet:
            print(f"❌ Target path not found: {target_path}")
        return []
    
    found_files = []
    
    # ✅ FILE YANG DI-SKIP (tidak mengandung DISPLAY_LANGUAGES section)
    skip_files = {
        'setup.py',
        '__init__.py',
        'test_',
        'conftest.py',
    }
    
    # ✅ FOLDER YANG DI-SKIP
    skip_folders = {
        '__pycache__', '.git', 'venv', 'env', 
        'node_modules', '.idea', '.vscode', 
        'build', 'dist', '.pytest_cache',
    }
    
    def should_skip_folder(folder_name):
        """Check if folder should be skipped"""
        return (folder_name in skip_folders or 
                folder_name.startswith('.') or
                folder_name.startswith('_'))
    
    def should_skip_file(filename):
        """Check if file should be skipped"""
        return any(skip_file in filename for skip_file in skip_files)
    
    def search_in_directory(directory):
        """Search recursively in directory"""
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                
                # Skip folders tertentu
                if os.path.isdir(item_path):
                    if should_skip_folder(item):
                        continue
                    if search_subfolders:
                        search_in_directory(item_path)  # Rekursif
                    continue
                
                # Process Python and JavaScript files
                if (item.endswith('.py') or item.endswith('.js')) and not should_skip_file(item):
                    try:
                        with open(item_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                            is_py_valid = (
                                item.endswith('.py') and
                                is_valid_display_languages_section(content) and
                                is_actual_display_section(content, item_path)
                            )
                            is_js_valid = item.endswith('.js') and is_valid_js_i18n_section(content)

                            if is_py_valid or is_js_valid:
                                found_files.append(item_path)
                                if not quiet:
                                    all_supported = get_all_supported_languages()
                                    if item.endswith('.js'):
                                        langs = extract_js_i18n_languages(content)
                                    else:
                                        langs = get_existing_languages_from_content(content)

                                    missing_langs = [lang for lang in all_supported if lang not in langs]
                                    lang_count = len(langs)
                                    missing_count = len(missing_langs)
                                    relative_path = os.path.relpath(item_path)

                                    status = "✅" if missing_count == 0 else "⚠️"
                                    file_type = "JS" if item.endswith('.js') else "PY"
                                    print(f"{status} Found [{file_type}]: {relative_path} ({lang_count}/{len(all_supported)} languages)")
                                    if missing_count > 0:
                                        print(f"     Missing: {', '.join(missing_langs)}")

                    except UnicodeDecodeError:
                        if not quiet:
                            print(f"⚠️  Encoding error in: {item_path}")
                    except Exception as e:
                        if not quiet:
                            print(f"⚠️  Error reading {item_path}: {e}")
        except PermissionError:
            if not quiet:
                print(f"⛔ Permission denied: {directory}")
        except Exception as e:
            if not quiet:
                print(f"⚠️  Error scanning {directory}: {e}")
    
    # Mulai pencarian
    if os.path.isfile(target_path):
        search_in_directory(os.path.dirname(target_path) or '.')
        found_files = [fp for fp in found_files if os.path.abspath(fp) == os.path.abspath(target_path)]
    else:
        search_in_directory(target_path)
    
    if not quiet:
        if found_files:
            total_files = len(found_files)
            complete_files = 0
            
            # Hitung file yang lengkap (Python DISPLAY_LANGUAGES + JS I18N)
            for file_path in found_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                all_supported = get_all_supported_languages()

                if file_path.endswith('.js'):
                    existing_langs = extract_js_i18n_languages(content)
                    english_keys = extract_js_english_keys(content)
                    all_have_phrases = len(english_keys) > 0 and len(get_js_incomplete_languages(content)) == 0
                else:
                    # ✅ GUNAKAN FUNGSI DARI language_utils
                    existing_langs = get_existing_languages_from_content(content)

                    # ✅ PERBAIKAN: Cek apakah semua bahasa memiliki phrases
                    all_have_phrases = True
                    for lang in existing_langs:
                        lang_pattern = rf'"{lang}":\s*\{{(.*?)\n    \}}'
                        lang_match = re.search(lang_pattern, content, re.DOTALL)
                        if lang_match:
                            lang_content = lang_match.group(1)
                            phrases1 = re.findall(r'"([^"]+)":\s*"[^"]*"', lang_content)
                            phrases2 = re.findall(r'"([^"]+)":\s*"[^{]*\{[^}]*\}[^"]*"', lang_content)
                            all_phrases = set(phrases1 + phrases2)
                            if len(all_phrases) == 0:
                                all_have_phrases = False
                                break
                
                if len(existing_langs) == len(all_supported) and all_have_phrases:
                    complete_files += 1
            
            print(f"\n📊 Summary: Found {total_files} files with DISPLAY_LANGUAGES/JS I18N")
            print(f"🎯 Complete: {complete_files}/{total_files} files have all {len(all_supported)} languages with phrases")
            if search_subfolders:
                print("🌐 Search scope: Current folder + all subfolders")
            else:
                print("📁 Search scope: Current folder only")
        else:
            print("❌ No files with DISPLAY_LANGUAGES/JS I18N found")
    
    return found_files

LANGUAGE_NAMES = {
    "en": "English", "pl": "Polski", "zh": "中文", "jp": "日本語",
    "de": "Deutsch", "fr": "Français", "es": "Español", "ru": "Pycckuñ",
    "pt": "Portugués", "id": "Indonesia", "kr": "한국어"
}

def auto_check_all(target_path='.'):
    """Automatically check all Python/JS files with i18n language blocks"""
    print("🔍 Auto-checking all files...")
    files = list_files(quiet=True, search_subfolders=True, target_path=target_path)
    
    if not files:
        print("❌ No files with DISPLAY_LANGUAGES/JS I18N found")
        return
    
    print(f"\n📊 Found {len(files)} files to analyze:")
    
    complete_files = 0
    files_with_missing_langs = []
    files_with_empty_phrases = []
    js_files_need_fix = []
    
    for file_path in files:
        print(f"\n{'='*50}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        all_supported = get_all_supported_languages()

        if file_path.endswith('.js'):
            existing_langs = extract_js_i18n_languages(content)
            english_keys = extract_js_english_keys(content)
            incomplete_js = get_js_incomplete_languages(content)
            suspicious_js = get_js_suspicious_values(content)
            languages_with_empty_phrases = [] if english_keys else ['en']
        else:
            existing_langs = get_existing_languages_from_content(content)
            incomplete_js = []
            suspicious_js = []

            # Cek bahasa yang memiliki phrases kosong
            languages_with_empty_phrases = []
            for lang in existing_langs:
                lang_pattern = rf'"{lang}":\s*\{{(.*?)\n    \}}'
                lang_match = re.search(lang_pattern, content, re.DOTALL)
                if lang_match:
                    lang_content = lang_match.group(1)
                    phrases1 = re.findall(r'"([^"]+)":\s*"[^"]*"', lang_content)
                    phrases2 = re.findall(r'"([^"]+)":\s*"[^{]*\{[^}]*\}[^"]*"', lang_content)
                    all_phrases = set(phrases1 + phrases2)
                    if len(all_phrases) == 0:
                        languages_with_empty_phrases.append(lang)
        
        missing_langs = [lang for lang in all_supported if lang not in existing_langs]
        
        has_all_languages = len(existing_langs) == len(all_supported)
        all_languages_have_phrases = (
            len(languages_with_empty_phrases) == 0 and
            len(incomplete_js) == 0 and
            len(suspicious_js) == 0
        )
        
        if has_all_languages and all_languages_have_phrases:
            complete_files += 1
            print(f"✅ {os.path.basename(file_path)}: COMPLETE ({len(existing_langs)}/{len(all_supported)} languages with phrases)")
        else:
            if missing_langs:
                # ✅ PERBAIKAN: Tampilkan dengan nama bahasa asli
                missing_display = []
                for lang_code in missing_langs:
                    lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                    missing_display.append(f"{lang_code} ({lang_name})")
                
                print(f"⚠️  {os.path.basename(file_path)}: INCOMPLETE ({len(existing_langs)}/{len(all_supported)} languages)")
                print(f"   Missing: {', '.join(missing_display)}")
                if not file_path.endswith('.js'):
                    files_with_missing_langs.append((file_path, missing_langs))
                else:
                    if file_path not in js_files_need_fix:
                        js_files_need_fix.append(file_path)
            
            if languages_with_empty_phrases:
                # ✅ PERBAIKAN: Tampilkan dengan nama bahasa asli
                empty_display = []
                for lang_code in languages_with_empty_phrases:
                    lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                    empty_display.append(f"{lang_code} ({lang_name})")
                
                print(f"⚠️  {os.path.basename(file_path)}: {len(languages_with_empty_phrases)} languages have empty phrases")
                print(f"   Empty: {', '.join(empty_display)}")
                if not file_path.endswith('.js'):
                    files_with_empty_phrases.append((file_path, languages_with_empty_phrases))
                else:
                    if file_path not in js_files_need_fix:
                        js_files_need_fix.append(file_path)

            if incomplete_js:
                print(f"⚠️  {os.path.basename(file_path)}: {len(incomplete_js)} languages have incomplete key coverage vs EN")
                for lang_code, current_count, expected_count in incomplete_js:
                    lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                    print(f"   - {lang_code} ({lang_name}): {current_count}/{expected_count} keys")
                if file_path not in js_files_need_fix:
                    js_files_need_fix.append(file_path)

            if suspicious_js:
                print(f"⚠️  {os.path.basename(file_path)}: {len(suspicious_js)} suspicious translated values detected")
                for lang_code, key, snippet in suspicious_js[:10]:
                    lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                    print(f"   - {lang_code} ({lang_name}) key '{key}': {snippet}")
                if len(suspicious_js) > 10:
                    print(f"   ... and {len(suspicious_js)-10} more")
                if file_path not in js_files_need_fix:
                    js_files_need_fix.append(file_path)
            
            if not missing_langs and not languages_with_empty_phrases:
                print(f"⚠️  {os.path.basename(file_path)}: INCOMPLETE ({len(existing_langs)}/{len(all_supported)} languages)")
    
    print(f"\n🎯 FINAL SUMMARY: {complete_files}/{len(files)} files have complete language sets with phrases")
    
    if files_with_missing_langs or files_with_empty_phrases:
        ask_fix_all_issues(files_with_missing_langs, files_with_empty_phrases)
    else:
        print("ℹ️ Auto-fix suggestions are available for Python files only.")

    if js_files_need_fix:
        print(f"\n🛠️ JS files needing fixes: {len(js_files_need_fix)}")
        for fp in js_files_need_fix:
            print(f"   - {os.path.basename(fp)}")
        try:
            choice = input("👉 Run JS auto-fix now? (y/N): ").strip().lower()
        except EOFError:
            choice = 'n'
        if choice in ['y', 'yes']:
            try:
                from .js_i18n_tools import run_js_autofix
            except ImportError:
                from js_i18n_tools import run_js_autofix

            success = 0
            for fp in js_files_need_fix:
                print(f"\n🔧 Auto-fixing JS: {fp}")
                try:
                    if run_js_autofix(fp):
                        success += 1
                except KeyboardInterrupt:
                    print("\n⚠️ JS auto-fix interrupted by user. Continuing without crash.")
                    break
            print(f"✅ JS auto-fix completed: {success}/{len(js_files_need_fix)} files")

# ======================== CLI MODE ========================

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            check_file_quick(sys.argv[2])
        elif sys.argv[1] == "analyze":
            analyze_file(sys.argv[2])
        elif sys.argv[1] == "list":
            list_files()
    else:
        print("❌ Please provide a command: check, analyze, or list")
        print("Usage: python analysis.py <command> <filename>")
