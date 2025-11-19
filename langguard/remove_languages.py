#!/usr/bin/env python3
"""
LangGuard - Remove Languages Only
DENGAN FALLBACK STRATEGY
"""

import os
import re
import sys

# ✅ IMPORT BARU - tambahkan language_selection
try:
    from .language_selection import select_languages_for_removal
except ImportError:
    from language_selection import select_languages_for_removal

def get_all_supported_languages():
    return ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"]

def get_current_display_language(content):
    """Dapatkan bahasa yang sedang digunakan sebagai DISPLAY_LANG"""
    display_match = re.search(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', content)
    return display_match.group(1) if display_match else "en"

def check_existing_languages(content):
    print("🔍 Checking existing languages...")
    
    start_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        print("❌ DISPLAY_LANGUAGES dictionary not found!")
        return []
    
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
    
    existing_languages = []
    all_langs = get_all_supported_languages()
    
    for lang in all_langs:
        if f'"{lang}":' in languages_section:
            existing_languages.append(lang)
    
    print(f"✅ Found {len(existing_languages)} existing languages: {', '.join(existing_languages)}")
    return existing_languages

def extract_language_content(dict_content):
    """Ekstrak konten setiap bahasa dengan method yang reliable"""
    languages_content = {}
    
    lines = dict_content.split('\n')
    current_lang = None
    lang_lines = []
    in_language_block = False
    brace_level = 0
    lang_start_index = -1
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip line kosong di awal
        if not stripped and not in_language_block:
            continue
            
        # Cari awal bahasa baru
        if not in_language_block:
            lang_match = re.match(r'"(\w+)"\s*:?\s*\{?', stripped)
            if lang_match:
                current_lang = lang_match.group(1)
                in_language_block = True
                brace_level = 1
                lang_lines = [line]  # Simpan line asli dengan indentasi
                lang_start_index = i
                continue
        
        # Jika sedang dalam block bahasa
        if in_language_block and current_lang:
            # Skip line pertama karena sudah ditambahkan
            if i > lang_start_index:
                lang_lines.append(line)
            
            # Hitung kurung
            brace_level += line.count('{')
            brace_level -= line.count('}')
            
            # Jika brace_count kembali ke 0, kita telah mencapai akhir dictionary bahasa ini
            if brace_level == 0:
                # Gabungkan semua lines untuk bahasa ini
                full_content = '\n'.join(lang_lines)
                
                # Bersihkan whitespace berlebih di akhir
                full_content = full_content.rstrip()
                
                # Hapus koma di akhir jika ada (untuk bahasa terakhir)
                if full_content.endswith(','):
                    full_content = full_content[:-1]
                
                languages_content[current_lang] = full_content
                
                # Reset untuk bahasa berikutnya
                current_lang = None
                in_language_block = False
                lang_lines = []
                lang_start_index = -1
    
    return languages_content

def ensure_proper_spacing(content):
    """Pastikan spacing setelah section DISPLAY LANGUAGE tepat 2 empty lines"""
    
    # Pattern untuk menemukan akhir section DISPLAY LANGUAGE
    section_end_pattern = r'(# -+\s*END DISPLAY LANGUAGE SETTINGS\s*-+)(\s*\n)*'
    
    def replace_spacing(match):
        end_line = match.group(1)
        # Selalu return dengan tepat 2 empty lines setelah END line
        return end_line + '\n\n'
    
    # Ganti semua spacing setelah END line dengan tepat 2 empty lines
    content = re.sub(section_end_pattern, replace_spacing, content)
    
    # Juga handle kasus dimana tidak ada END line (untuk backward compatibility)
    functions_end_pattern = r'(def get_available_languages\(\):.*?return list\(DISPLAY_LANGUAGES\.keys\(\)\))(\s*\n)*'
    
    def replace_functions_spacing(match):
        end_line = match.group(1)
        # Selalu return dengan tepat 2 empty lines setelah functions terakhir
        return end_line + '\n\n'
    
    content = re.sub(functions_end_pattern, replace_functions_spacing, content, flags=re.DOTALL)
    
    return content

def remove_entire_display_section(content):
    """Hapus seluruh section DISPLAY_LANGUAGES termasuk fungsi-fungsinya"""
    print("🗑️ Removing entire DISPLAY_LANGUAGES section...")
    
    # Pattern untuk menemukan seluruh section dari DISPLAY_LANGUAGES sampai akhir fungsi
    section_pattern = r'# -+\s*DISPLAY LANGUAGE SETTINGS\s*-+.*?def get_available_languages\(\):.*?return list\(DISPLAY_LANGUAGES\.keys\(\)\)'
    
    # Cari section
    section_match = re.search(section_pattern, content, re.DOTALL)
    if not section_match:
        print("❌ DISPLAY_LANGUAGES section not found with expected structure")
        return content
    
    # Hapus section
    new_content = content[:section_match.start()] + content[section_match.end():]
    
    # Bersihkan empty lines berlebih
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    print("✅ Entire DISPLAY_LANGUAGES section removed successfully!")
    return new_content

def remove_languages_from_content(content, languages_to_remove, current_display_lang):
    if not languages_to_remove:
        print("ℹ️ No languages to remove")
        return content
    
    # Cek jika ini permintaan hapus seluruh section
    if languages_to_remove == "REMOVE_ALL_SECTION":
        return remove_entire_display_section(content)
    
    print(f"\n🔄 Processing {len(languages_to_remove)} languages to remove: {', '.join(languages_to_remove)}")
    
    # Validasi: pastikan bahasa default tidak termasuk dalam yang akan dihapus
    if current_display_lang in languages_to_remove:
        print(f"❌ Cannot remove default language: {current_display_lang}")
        languages_to_remove = [lang for lang in languages_to_remove if lang != current_display_lang]
        if not languages_to_remove:
            print("ℹ️ No languages to remove after filtering")
            return content
    
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
    
    # Extract bagian dictionary
    before_dict = content[:start_match.start()]
    dict_content = content[start_match.start():current_pos]
    after_dict = content[current_pos:]
    
    # Ekstrak semua bahasa yang ada dengan kontennya
    all_lang_content = extract_language_content(dict_content)
    
    # Filter bahasa yang TIDAK akan dihapus (termasuk bahasa default harus tetap ada)
    languages_to_keep = {lang: content for lang, content in all_lang_content.items() 
                        if lang not in languages_to_remove}
    
    # PASTIKAN bahasa default tetap ada
    if current_display_lang not in languages_to_keep and current_display_lang in all_lang_content:
        languages_to_keep[current_display_lang] = all_lang_content[current_display_lang]
        print(f"🔒 Keeping default language: {current_display_lang}")
    
    if len(languages_to_keep) == 0:
        print("⚠️ Warning: No languages left! Keeping default language.")
        # Buat template untuk bahasa default dengan format yang sama
        default_template = f'    "{current_display_lang}": {{\n        # {current_display_lang.upper()} translations\n    }}'
        languages_to_keep = {current_display_lang: default_template}
    
    print(f"📋 Keeping {len(languages_to_keep)} languages: {', '.join(languages_to_keep.keys())}")
    
    # Urutan yang diinginkan
    desired_order = get_all_supported_languages()
    
    # Urutkan bahasa yang tersisa sesuai urutan standar
    sorted_languages = [lang for lang in desired_order if lang in languages_to_keep]
    
    # Bangun dictionary baru dengan bahasa yang tersisa
    new_dict_content = 'DISPLAY_LANGUAGES = {\n'
    
    for i, lang_code in enumerate(sorted_languages):
        lang_entry = languages_to_keep[lang_code]
        
        # Tambahkan koma kecuali untuk bahasa terakhir
        if i < len(sorted_languages) - 1:
            # Pastikan tidak ada koma di akhir entry sebelum menambahkan
            lang_entry = lang_entry.rstrip()
            if not lang_entry.endswith(','):
                lang_entry += ','
        
        # Tambahkan ke konten baru
        new_dict_content += lang_entry + '\n'
    
    new_dict_content += '}'
    
    # Validasi: pastikan format koma benar
    if ',,' in new_dict_content:
        new_dict_content = new_dict_content.replace(',,', ',')
        print("🔄 Fixed double comma issue")
    
    # Validasi: pastikan tidak ada koma sebelum kurung tutup
    if new_dict_content.endswith(',}'):
        new_dict_content = new_dict_content.replace(',}', '}')
        print("🔄 Fixed trailing comma before closing brace")
    
    # Gabungkan konten baru
    new_content = before_dict + new_dict_content + after_dict
    
    # PASTIKAN SPACING BENAR
    new_content = ensure_proper_spacing(new_content)
    
    print(f"✅ Successfully removed {len(languages_to_remove)} languages!")
    print(f"📊 Remaining languages: {len(sorted_languages)}")
    print(f"🔄 New order: {', '.join(sorted_languages)}")
    print(f"⭐ Default language preserved: {current_display_lang}")
    
    return new_content

def run_remove_languages(target_file):
    """Fungsi utama untuk menghapus bahasa - DENGAN FALLBACK STRATEGY"""
    # ✅ GUNAKAN FALLBACK STRATEGY YANG BARU:
    try:
        from .fallback_strategy import fallback_for_remove_lang
    except ImportError:
        from fallback_strategy import fallback_for_remove_lang
    
    # Cek section dan generate jika perlu
    if not fallback_for_remove_lang(target_file):
        return False  # File tidak ada atau user cancel
    
    # Lanjut proses remove-lang normal (section sudah ada)
    print("🔄 Continuing with remove-lang process...")
    
    # Baca file
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    backup_path = target_file + '.remove_backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📁 Backup created: {backup_path}")
    
    # Dapatkan bahasa default saat ini
    current_display_lang = get_current_display_language(content)
    print(f"⭐ Current default language: {current_display_lang}")
    
    # Tampilkan bahasa yang sudah ada
    existing_languages = check_existing_languages(content)
    
    if not existing_languages:
        print("❌ No languages found to remove")
        return
    
    print(f"\n📊 Currently have {len(existing_languages)} languages: {', '.join(existing_languages)}")
    
    # ✅ GUNAKAN FUNGSI TERPUSAT untuk pemilihan bahasa removal
    languages_to_remove = select_languages_for_removal(existing_languages, current_display_lang)
    
    if not languages_to_remove:
        print("ℹ️ No languages selected for removal")
        return
    
    # Hapus bahasa yang dipilih
    content = remove_languages_from_content(content, languages_to_remove, current_display_lang)
    
    # Tulis file final
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Operation completed successfully!")
    print(f"💾 Backup: {backup_path}")

def main():
    """Entry point untuk standalone execution"""
    import sys
    if len(sys.argv) > 1:
        run_remove_languages(sys.argv[1])
    else:
        print("❌ Please provide a target file")
        print("Usage: python remove_languages.py <filename>")

if __name__ == "__main__":
    main()