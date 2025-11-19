#!/usr/bin/env python3
"""
LangGuard - Add Missing Languages (Modular Version)
WITH AUTO-GENERATE OPTION - FIXED IMPORT (NO CIRCULAR IMPORT)
"""

import re
import os
import sys

# ✅ GUNAKAN language_utils untuk menghindari circular import
try:
    from .language_utils import (
        get_all_supported_languages,
        get_correct_language_order,
        get_existing_languages_from_content,
        extract_english_phrases
    )
    from .language_selection import (
        show_language_selection,
        get_user_language_selection,
        select_languages_for_addition
    )
except ImportError:
    from language_utils import (
        get_all_supported_languages,
        get_correct_language_order,
        get_existing_languages_from_content,
        extract_english_phrases
    )
    from language_selection import (
        show_language_selection,
        get_user_language_selection,
        select_languages_for_addition
    )

def extract_phrases_for_language(content, lang_code):
    """Ekstrak phrases untuk bahasa tertentu"""
    lang_pattern = rf'"{lang_code}":\s*\{{(.*?)\n    \}}'
    lang_match = re.search(lang_pattern, content, re.DOTALL)
    if not lang_match:
        return set()
    
    lang_content = lang_match.group(1)
    phrases1 = re.findall(r'"([^"]+)":\s*"[^"]*"', lang_content)
    phrases2 = re.findall(r'"([^"]+)":\s*"[^{]*\{[^}]*\}[^"]*"', lang_content)
    phrases3 = re.findall(r'"([^"]+)":\s*[^,\n]+', lang_content)
    
    all_phrases = set()
    for phrase_list in [phrases1, phrases2, phrases3]:
        all_phrases.update(phrase_list)
    
    return all_phrases

def get_missing_languages_from_content(content):
    """Dapatkan daftar bahasa yang missing dari konten file"""
    existing_langs = get_existing_languages_from_content(content)
    all_supported = get_all_supported_languages()
    missing_langs = [lang for lang in all_supported if lang not in existing_langs]
    
    correct_order = get_correct_language_order()
    return [lang for lang in correct_order if lang in missing_langs]

# ✅ TAMBAHKAN DI SINI - di add_languages.py
def check_internet_connection():
    """Cek koneksi internet untuk translation"""
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False

def check_display_section_exists(content):
    """Cek apakah DISPLAY_LANGUAGES section ada dan valid"""
    return 'DISPLAY_LANGUAGES = {' in content

def run_insert_section_dynamic(target_file):
    """Jalankan insert_section secara langsung"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        try:
            from insert_section import run_insert_section
            run_insert_section(target_file)
            return True
        except ImportError:
            from .insert_section import run_insert_section
            run_insert_section(target_file)
            return True
            
    except Exception as e:
        print(f"❌ Error running insert_section: {e}")
        return False

def ask_generate_section(target_file):
    """Tanya user apakah ingin generate section DISPLAY_LANGUAGES"""
    print(f"\n❌ File '{target_file}' doesn't have DISPLAY_LANGUAGES section!")
    
    while True:
        choice = input("\n👉 Do you want to generate a complete DISPLAY_LANGUAGES section now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🎯 Generating DISPLAY_LANGUAGES section...")
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

def add_languages_to_content(content, languages_to_add):
    """Tambahkan bahasa baru ke dictionary DISPLAY_LANGUAGES dengan urutan yang benar"""
    if not languages_to_add:
        print("ℹ️ No languages selected.")
        return content
    
    print(f"\n🔄 Adding {len(languages_to_add)} languages: {', '.join(languages_to_add)}")

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

    match = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{[\s\S]*?\n\}', content, re.DOTALL)
    if not match:
        print("❌ DISPLAY_LANGUAGES not found in file.")
        return content

    dict_content = match.group(0)
    before = content[:match.start()]
    after = content[match.end():]

    existing_langs = get_existing_languages_from_content(content)
    
    existing_lang_content = {}
    for lang in existing_langs:
        lang_pattern = rf'"{lang}":\s*\{{([\s\S]*?)\n    \}}'
        lang_match = re.search(lang_pattern, dict_content, re.DOTALL)
        if lang_match:
            existing_lang_content[lang] = f'    "{lang}": {{{lang_match.group(1)}\n    }}'
        else:
            existing_lang_content[lang] = templates.get(lang, f'    "{lang}": {{\n        # {lang.upper()} content\n    }}')
    
    new_langs = [lang for lang in languages_to_add if lang not in existing_langs]

    if not new_langs:
        print("ℹ️ All selected languages already exist.")
        return content

    print(f"🎯 Adding new languages: {', '.join(new_langs)}")

    all_langs_combined = existing_langs + new_langs
    correct_order = get_correct_language_order()
    final_langs = [lang for lang in correct_order if lang in all_langs_combined]

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

    new_content = before + new_dict_content + after

    print(f"✅ Added {len(new_langs)} new languages successfully!")
    print(f"🔄 Final language order: {', '.join(final_langs)}")
    return new_content

def ask_translate_new_languages(file_path, new_languages):
    """Tanya user apakah ingin mentranslasi bahasa baru yang kosong - DENGAN DETEKSI PHRASES"""
    if not new_languages:
        return False
    
    print(f"\n🔍 Checking phrases for new languages...")
    
    # Baca file untuk cek phrases
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ✅ GUNAKAN FUNGSI DARI language_utils
    english_phrases = extract_english_phrases(content)
    english_phrase_count = len(english_phrases) if english_phrases else 0
    
    if english_phrase_count == 0:
        print("⚠️  English section is empty - cannot translate without reference phrases")
        return False
    
    # Cek phrases untuk setiap bahasa baru
    empty_languages = []
    incomplete_languages = []
    complete_languages = []
    
    for lang in new_languages:
        lang_pattern = rf'"{lang}":\s*\{{(.*?)\n    \}}'
        lang_match = re.search(lang_pattern, content, re.DOTALL)
        if lang_match:
            lang_content = lang_match.group(1)
            # Hitung phrases
            phrases1 = re.findall(r'"([^"]+)":\s*"[^"]*"', lang_content)
            phrases2 = re.findall(r'"([^"]+)":\s*"[^{]*\{[^}]*\}[^"]*"', lang_content)
            phrases3 = re.findall(r'"([^"]+)":\s*[^,\n]+', lang_content)
            
            all_phrases = set()
            for phrase_list in [phrases1, phrases2, phrases3]:
                all_phrases.update(phrase_list)
            
            phrase_count = len(all_phrases)
            if phrase_count == 0:
                print(f"⚠️  {lang.upper()}: 0 phrases (empty)")
                empty_languages.append(lang)
            elif phrase_count < english_phrase_count:
                print(f"⚠️  {lang.upper()}: {phrase_count}/{english_phrase_count} phrases (incomplete)")
                incomplete_languages.append(lang)
            else:
                print(f"✅ {lang.upper()}: {phrase_count} phrases (complete)")
                complete_languages.append(lang)
        else:
            print(f"❌ {lang.upper()}: Language section not found")
    
    # ✅ PERBAIKAN: Hanya tawarkan translasi jika ada bahasa yang perlu
    languages_need_translation = empty_languages + incomplete_languages
    
    if not languages_need_translation:
        if complete_languages:
            print(f"✅ All {len(complete_languages)} new languages have complete phrases content.")
        else:
            print("✅ No translation needed for new languages.")
        return False
    
    # Tampilkan summary yang lebih detail
    print(f"\n📊 Translation Summary for New Languages:")
    print("-" * 50)
    
    if empty_languages:
        print(f"🔴 Empty languages ({len(empty_languages)}): {', '.join(empty_languages)}")
    
    if incomplete_languages:
        print(f"🟡 Incomplete languages ({len(incomplete_languages)}):")
        for lang in incomplete_languages:
            current_phrases = len(extract_phrases_for_language(content, lang))
            missing_count = english_phrase_count - current_phrases
            print(f"   - {lang.upper()}: {current_phrases}/{english_phrase_count} phrases (missing {missing_count})")
    
    if complete_languages:
        print(f"🟢 Complete languages ({len(complete_languages)}): {', '.join(complete_languages)}")
    
    print("-" * 50)
    
    # Hitung total phrases yang perlu diterjemahkan
    total_missing = 0
    for lang in empty_languages:
        total_missing += english_phrase_count
    
    for lang in incomplete_languages:
        current_phrases = len(extract_phrases_for_language(content, lang))
        total_missing += (english_phrase_count - current_phrases)
    
    print(f"📝 Total phrases to translate: {total_missing}")
    
    # Tampilkan beberapa contoh phrases yang akan diterjemahkan
    if english_phrases and total_missing > 0:
        sample_phrases = list(english_phrases.keys())[:3]
        if sample_phrases:
            print(f"🔤 Sample phrases: {', '.join(sample_phrases)}" + ("..." if len(english_phrases) > 3 else ""))
    
    # ✅ PERBAIKAN: CEK KONEKSI INTERNET SEBELUM MENAWARKAN TRANSLASI
    if not check_internet_connection():
        print("❌ No internet connection! Translation requires internet access.")
        print("💡 Please check your internet connection and run 'langguard translate' later")
        return False
    
    # Konfirmasi dengan user
    while True:
        choice = input(f"\n👉 Do you want to auto-translate {len(languages_need_translation)} languages now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print(f"\n🎯 Running auto-translation for {len(languages_need_translation)} languages...")
            try:
                # ✅ IMPORT DINAMIS - hanya ketika benar-benar dibutuhkan
                from translate import run_translate
                success = run_translate(file_path)
                if success:
                    print(f"✅ Successfully translated {len(languages_need_translation)} new languages!")
                else:
                    print("❌ Translation failed or was cancelled.")
                return True
            except ImportError:
                try:
                    from .translate import run_translate
                    success = run_translate(file_path)
                    if success:
                        print(f"✅ Successfully translated {len(languages_need_translation)} new languages!")
                    else:
                        print("❌ Translation failed or was cancelled.")
                    return True
                except ImportError:
                    print("❌ Cannot import translate module")
                    return False
        elif choice in ['n', 'no', '']:
            print("ℹ️ Translation for new languages skipped.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

def run_add_languages(target_file):
    """Fungsi utama untuk menambah bahasa - DENGAN AUTO-GENERATE YANG LEBIH BAIK"""
    if not os.path.exists(target_file):
        print(f"❌ File {target_file} not found.")
        return False
    
    print(f"🎯 Target: {target_file}")
    print("=" * 60)
    
    # Baca file
    with open(target_file, "r", encoding="utf-8") as f:
        old_content = f.read()  # ✅ SIMPAN KONTEN LAMA UNTUK COMPARISON
    
    # Backup
    backup_path = target_file + ".add_backup"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(old_content)
    print(f"📁 Backup created: {backup_path}")
    
    # Simpan bahasa lama sebelum perubahan
    old_langs = get_existing_languages_from_content(old_content)
    
    # CEK PERTAMA: Apakah section DISPLAY_LANGUAGES ada?
    if not check_display_section_exists(old_content):
        # Jika tidak ada, tanya user apakah ingin generate section
        if ask_generate_section(target_file):
            # Jika user memilih yes, baca file yang sudah di-update
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Cek lagi setelah generate
            if not check_display_section_exists(content):
                print("❌ Still no DISPLAY_LANGUAGES section after generation. Operation cancelled.")
                return False
            
            # PERBAIKAN: Setelah berhasil generate section, tanya user apakah ingin langsung menambah bahasa
            existing_langs = get_existing_languages_from_content(content)
            print(f"\n✅ DISPLAY_LANGUAGES section created successfully!")
            print(f"📊 Current languages: {', '.join(existing_langs)}")
            
            # Tanya user apakah ingin langsung menambah bahasa yang missing
            add_missing_now = input("\n👉 Do you want to add missing languages now? (y/N): ").strip().lower()
            
            if add_missing_now != 'y':
                print("ℹ️ Operation completed. You can add missing languages later with 'langguard add-lang'")
                print(f"💾 Backup: {backup_path}")
                return True
            
            # Update old_langs untuk comparison
            old_langs = existing_langs
            old_content = content
        else:
            return False
    
    # Jika sampai di sini, berarti section DISPLAY_LANGUAGES ADA
    # Sekarang jalankan proses add missing languages seperti biasa
    
    # Dapatkan bahasa yang missing
    existing_langs = get_existing_languages_from_content(old_content)
    all_supported = get_all_supported_languages()
    missing_langs = [lang for lang in all_supported if lang not in existing_langs]
    
    if not missing_langs:
        print("🎉 All supported languages already exist!")
        print("✅ No languages to add.")
        return True
    
    print(f"📊 Current languages: {', '.join(existing_langs)}")
    print(f"💡 Found {len(missing_langs)} missing languages: {', '.join(missing_langs)}")
    
    # ✅ GUNAKAN FUNGSI TERPUSAT untuk pemilihan bahasa missing
    show_language_selection(available_langs=missing_langs, context="add")
    selected_langs = get_user_language_selection(available_langs=missing_langs, allow_multiple=True, context="add")
    
    if selected_langs:
        new_content = add_languages_to_content(old_content, selected_langs)
        if new_content != old_content:
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Added {len(selected_langs)} languages successfully!")
            print(f"📊 Languages added: {', '.join(selected_langs)}")
            
            # ✅ PERBAIKAN: DETEKSI BAHASA BARU DAN TAWARKAN TRANSLASI
            new_langs = [lang for lang in selected_langs if lang not in old_langs]
            if new_langs:
                print(f"\n🔄 {len(new_langs)} new languages added successfully: {', '.join(new_langs)}")
                # Tawarkan translasi untuk bahasa baru
                ask_translate_new_languages(target_file, new_langs)
            
            return True
        else:
            print("ℹ️ No changes made.")
            return True
    else:
        print("ℹ️ No languages selected.")
        return True
    
    print(f"💾 Backup: {backup_path}")

# ======================== CLI MODE ========================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a target file.")
        print("Usage: python add_languages.py <filename>")
        sys.exit(1)
    
    run_add_languages(sys.argv[1])