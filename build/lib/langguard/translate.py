#!/usr/bin/env python3
"""
LangGuard - Auto Translation Module
Untuk menerjemahkan konten DISPLAY_LANGUAGES secara otomatis
"""

import os
import re
import sys
from deep_translator import GoogleTranslator

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

# Mapping kode bahasa ke nama bahasa untuk translator
LANGUAGE_MAPPING = {
    "en": "english",
    "pl": "polski",
    "zh": "中文",
    "jp": "日本語",
    "de": "deutsch",
    "fr": "français",
    "es": "español",
    "ru": "pycckuñ",
    "pt": "portugués",
    "id": "indonesia",
    "kr": "한국어"
}

# Mapping untuk deep-translator (kode yang berbeda)
TRANSLATOR_LANG_CODES = {
    "en": "en",
    "pl": "pl",
    "zh": "zh-CN",  # Chinese simplified
    "jp": "ja",
    "de": "de",
    "fr": "fr",
    "es": "es",
    "ru": "ru",
    "pt": "pt",
    "id": "id",
    "kr": "ko"
}

# Template untuk placeholder yang tidak boleh diterjemahkan
PLACEHOLDER_PATTERNS = [
    r'\{lang_name\}',
    r'\{lang_code\}',
    r'\{path\}',
    r'\{filename\}',
    r'\{folder\}'
]


def protect_placeholders(text):
    """Lindungi placeholder dari terjemahan"""
    protected_text = text
    placeholder_map = {}
    for i, pattern in enumerate(PLACEHOLDER_PATTERNS):
        matches = re.findall(pattern, protected_text)
        for match in matches:
            token = f"__PLACEHOLDER_{i}_{len(placeholder_map)}__"
            placeholder_map[token] = match
            protected_text = protected_text.replace(match, token)
    return protected_text, placeholder_map


def restore_placeholders(text, placeholder_map):
    """Kembalikan placeholder setelah terjemahan"""
    restored_text = text
    for token, placeholder in placeholder_map.items():
        restored_text = restored_text.replace(token, placeholder)
    return restored_text


def translate_phrase(text, target_lang):
    """Terjemahkan satu phrase dengan proteksi placeholder"""
    if not text.strip():
        return text

    try:
        translator_code = TRANSLATOR_LANG_CODES.get(target_lang, target_lang)
        protected_text, placeholder_map = protect_placeholders(text)
        translated = GoogleTranslator(source='auto', target=translator_code).translate(protected_text)
        final_text = restore_placeholders(translated, placeholder_map)
        return final_text
    except Exception as e:
        print(f"❌ Translation error for '{text}': {e}")
        return text


def get_missing_translations_for_language(content, target_lang):
    """Dapatkan daftar phrases yang belum diterjemahkan untuk bahasa tertentu"""
    existing_phrases = {}
    missing_phrases = {}

    english_phrases = extract_english_phrases(content)
    if not english_phrases:
        return missing_phrases, existing_phrases

    lang_pattern = f'"{target_lang}":\\s*{{([\\s\\S]*?)\\n    \\}}'
    lang_match = re.search(lang_pattern, content, re.DOTALL)
    if lang_match:
        lang_content = lang_match.group(1)
        phrase_pattern = r'"([^"]+)":\s*"([^"]*)"'
        existing = re.findall(phrase_pattern, lang_content)
        for key, value in existing:
            existing_phrases[key] = value

    for key, english_value in english_phrases.items():
        if key not in existing_phrases:
            missing_phrases[key] = english_value

    return missing_phrases, existing_phrases


def create_translated_lang_section(target_lang, english_phrases, existing_phrases):
    """Buat section bahasa yang sudah diterjemahkan"""
    lang_name = LANGUAGE_MAPPING.get(target_lang, target_lang.upper())
    section = '    "' + target_lang + '": {\n'

    all_phrases = {}
    all_phrases.update(existing_phrases)

    if english_phrases:
        print(f"🔄 Translating {len(english_phrases)} phrases to {lang_name}...")
        for i, (key, english_text) in enumerate(english_phrases.items(), 1):
            print(f"   📝 [{i}/{len(english_phrases)}] Translating: {key}")
            translated_text = translate_phrase(english_text, target_lang)
            all_phrases[key] = translated_text

    for i, (key, value) in enumerate(all_phrases.items()):
        if i > 0:
            section += ',\n'
        section += f'        "{key}": "{value}"'
    section += '\n    }'
    return section, len(all_phrases)


def find_and_replace_lang_section(content, lang_code, new_section):
    """Temukan dan ganti section bahasa"""
    lang_pos = content.find(f'"{lang_code}":')
    if lang_pos == -1:
        print(f"❌ {lang_code.upper()} section not found!")
        return content

    start_pos = lang_pos
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
        print(f"❌ Could not find end of {lang_code.upper()} section")
        return content

    has_comma_after = False
    if end_pos < len(content) and content[end_pos] == ',':
        has_comma_after = True
        end_pos += 1

    if has_comma_after:
        return content[:start_pos] + new_section + ',' + content[end_pos:]
    else:
        return content[:start_pos] + new_section + content[end_pos:]


def auto_translate_languages(content, languages_to_translate):
    """Terjemahkan otomatis untuk multiple languages"""
    english_phrases = extract_english_phrases(content)
    if not english_phrases:
        print("❌ No English phrases found to translate")
        return content, 0

    total_translated = 0
    for lang_code in languages_to_translate:
        if lang_code == "en":
            continue

        print(f"\n🎯 Translating to {LANGUAGE_MAPPING.get(lang_code, lang_code.upper())}...")
        missing_phrases, existing_phrases = get_missing_translations_for_language(content, lang_code)
        if not missing_phrases:
            print(f"✅ {lang_code.upper()} already complete!")
            continue

        new_section, phrase_count = create_translated_lang_section(lang_code, missing_phrases, existing_phrases)
        content = find_and_replace_lang_section(content, lang_code, new_section)
        translated_count = len(missing_phrases)
        total_translated += translated_count
        print(f"✅ Translated {translated_count} phrases to {lang_code.upper()}")
    return content, total_translated


def show_translation_progress(content):
    """Tampilkan progress terjemahan untuk semua bahasa"""
    english_phrases = extract_english_phrases(content)
    total_phrases = len(english_phrases)
    if not total_phrases:
        return

    print(f"\n📊 TRANSLATION PROGRESS ({total_phrases} phrases):")
    print("=" * 50)
    existing_langs = get_existing_languages_from_content(content)
    for lang_code in existing_langs:
        if lang_code == "en":
            print(f"✅ {lang_code.upper()}: {total_phrases}/{total_phrases} (100%)")
            continue
        lang_pattern = f'"{lang_code}":\\s*{{([\\s\\S]*?)\\n    \\}}'
        lang_match = re.search(lang_pattern, content, re.DOTALL)
        if lang_match:
            lang_content = lang_match.group(1)
            phrase_pattern = r'"([^"]+)":\s*"([^"]*)"'
            existing_phrases = re.findall(phrase_pattern, lang_content)
            translated_count = len(existing_phrases)
            percentage = (translated_count / total_phrases) * 100
            status = "✅" if translated_count == total_phrases else "🟡"
            print(f"{status} {lang_code.upper()}: {translated_count}/{total_phrases} ({percentage:.0f}%)")
        else:
            print(f"🔴 {lang_code.upper()}: 0/{total_phrases} (0%)")


def fix_display_languages_indentation(content):
    """Rapikan indentasi setiap bahasa agar sejalar 4 spasi."""
    fixed_lines = []
    in_display = False
    for line in content.splitlines():
        if "DISPLAY_LANGUAGES" in line and "=" in line:
            in_display = True
            fixed_lines.append(line)
            continue
        if in_display:
            if line.strip() == "}":
                in_display = False
                fixed_lines.append(line)
                continue
            if re.match(r'\s*"[a-z]{2}":\s*\{', line):
                fixed_lines.append("    " + line.strip())
                continue
        fixed_lines.append(line)
    return "\n".join(fixed_lines)

def ask_add_more_languages():
    """Tanya user apakah ingin menambah bahasa lain"""
    while True:
        choice = input("\n👉 Do you want to add more languages before translating? (y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no', '']:
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

# ✅ OPTIONAL: Tambahkan pengecekan apakah ada akses internet
def check_internet_connection():
    """Cek koneksi internet untuk translation"""
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False

def run_translate(target_file):
    """Fungsi utama untuk menjalankan terjemahan otomatis - DENGAN FALLBACK STRATEGY YANG BENAR"""
    # ✅ GUNAKAN FALLBACK STRATEGY YANG BARU
    try:
        from .fallback_strategy import fallback_for_translate
    except ImportError:
        from fallback_strategy import fallback_for_translate
    
    # Cek section dan generate jika perlu
    if not fallback_for_translate(target_file):
        return False  # File tidak ada atau user cancel
    
    # Lanjut proses translate normal (section sudah ada)
    print("🔄 Continuing with translation process...")
    
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    backup_path = target_file + ".translate_backup"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📁 Backup created: {backup_path}")

    # ✅ PERBAIKAN: Validasi English phrases SEBELUM melanjutkan
    english_phrases = extract_english_phrases(content)
    if not english_phrases:
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
        return

    # ✅ OPTIONAL: Cek koneksi internet SEBELUM memulai proses translate
    if not check_internet_connection():
        print("❌ No internet connection! Translation requires internet access.")
        print("💡 Please check your internet connection and try again")
        return

    print(f"📖 Found {len(english_phrases)} English phrases as reference")
    
    existing_langs = get_existing_languages_from_content(content)
    languages_need_translation = []
    
    # ✅ DETEKSI KHUSUS: Cari bahasa yang kosong atau incomplete
    for lang_code in existing_langs:
        if lang_code == "en":
            continue
            
        missing_phrases, existing_phrases = get_missing_translations_for_language(content, lang_code)
        if missing_phrases:
            languages_need_translation.append(lang_code)
    
    if not languages_need_translation:
        print("🎉 All languages already have complete translations!")
        print("✅ No translation needed.")
        return
    
    print(f"🔍 {len(languages_need_translation)} languages need translation: {', '.join(languages_need_translation)}")
    
    # ✅ Tampilkan detail bahasa yang perlu diterjemahkan
    print("\n📊 Translation Summary:")
    print("-" * 40)
    
    for lang_code in languages_need_translation:
        missing_phrases, existing_phrases = get_missing_translations_for_language(content, lang_code)
        lang_name = LANGUAGE_MAPPING.get(lang_code, lang_code.upper())
        print(f"🌍 {lang_name} ({lang_code}): {len(missing_phrases)} phrases to translate")
        
        # Tampilkan beberapa contoh phrases yang akan diterjemahkan
        if missing_phrases:
            sample_phrases = list(missing_phrases.keys())[:3]  # Ambil 3 contoh
            if sample_phrases:
                print(f"   Sample: {', '.join(sample_phrases)}" + ("..." if len(missing_phrases) > 3 else ""))
    
    print("-" * 40)
    
    # ✅ Konfirmasi dengan user sebelum melanjutkan
    total_phrases_to_translate = sum([len(get_missing_translations_for_language(content, lang_code)[0]) for lang_code in languages_need_translation])
    
    print(f"📝 Total phrases to translate: {total_phrases_to_translate}")
    
    while True:
        confirm = input(f"\n👉 Proceed with auto-translation? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            break
        elif confirm in ['n', 'no', '']:
            print("ℹ️ Translation cancelled.")
            return
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")

    # ✅ PROSES TRANSLATE UTAMA
    print("\n🎯 Starting auto-translation...")
    
    # Cek apakah semua bahasa sudah lengkap sebelum tanya
    existing_langs = set(existing_langs)
    supported_langs = set(get_all_supported_languages())
    missing_langs = sorted(list(supported_langs - existing_langs))

    if not missing_langs:
        print("\n🎉 All supported languages already exist!")
        print("✅ No languages to add.")
    else:
        # Tanya lagi untuk tambah bahasa
        if ask_add_more_languages():
            print("\n🎯 Opening language addition mode...")
            try:
                from add_languages import run_add_languages
                run_add_languages(target_file)
            except ImportError:
                try:
                    from .add_languages import run_add_languages
                    run_add_languages(target_file)
                except ImportError:
                    print("❌ Cannot import add_languages module")
                    return

            print("\n📖 Checking for newly added languages...")
            with open(target_file, "r", encoding="utf-8") as f:
                updated_content = f.read()

            before = set(get_existing_languages_from_content(content))
            after = set(get_existing_languages_from_content(updated_content))
            new_langs = sorted(list(after - before))

            if new_langs:
                print(f"🎯 Newly added languages detected: {', '.join(new_langs)}")
                print("🔄 Automatically translating new languages...")
                updated_content, count_new = auto_translate_languages(updated_content, new_langs)
                if count_new > 0:
                    updated_content = fix_display_languages_indentation(updated_content)
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    print(f"✅ Successfully translated {count_new} phrases for new languages!")
                    show_translation_progress(updated_content)
                else:
                    print("ℹ️ No phrases needed translation for new languages.")
            else:
                print("ℹ️ No new languages detected after addition.")
            print(f"\n💾 Backup: {backup_path}")
            return  # ✅ Penting agar tidak lanjut ke proses translate utama

    # Proses terjemahan utama untuk bahasa yang sudah ada
    new_content, total_translated = auto_translate_languages(content, languages_need_translation)
    
    if total_translated > 0:
        new_content = fix_display_languages_indentation(new_content)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"\n✅ SUCCESS: Translated {total_translated} phrases across {len(languages_need_translation)} languages!")
        show_translation_progress(new_content)
        
        # Tampilkan summary hasil terjemahan
        print("\n📈 Translation Results:")
        print("-" * 40)
        for lang_code in languages_need_translation:
            missing_after, existing_after = get_missing_translations_for_language(new_content, lang_code)
            lang_name = LANGUAGE_MAPPING.get(lang_code, lang_code.upper())
            if not missing_after:
                print(f"✅ {lang_name}: Complete ({len(existing_after)} phrases)")
            else:
                print(f"⚠️  {lang_name}: {len(existing_after)}/{len(english_phrases)} phrases ({len(missing_after)} missing)")
        
    else:
        print("ℹ️ No translations were made.")

    print(f"\n💾 Backup: {backup_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a target file.")
        print("Usage: python translate.py <filename>")
        sys.exit(1)
    run_translate(sys.argv[1])