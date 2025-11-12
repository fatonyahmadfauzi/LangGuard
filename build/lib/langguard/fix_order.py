#!/usr/bin/env python3
"""
Script untuk memperbaiki urutan DISPLAY_LANGUAGES
Versi yang lebih sederhana dan efektif - DENGAN FALLBACK STRATEGY
"""

import re
import os
import sys

# ✅ GUNAKAN language_utils untuk menghindari circular import
try:
    from .language_utils import get_correct_language_order
except ImportError:
    from language_utils import get_correct_language_order

def fix_language_order(file_path):
    """Perbaiki urutan bahasa sesuai standar - DENGAN FALLBACK"""
    
    # ✅ GUNAKAN FALLBACK STRATEGY YANG BARU:
    try:
        from .fallback_strategy import fallback_for_fix_order
    except ImportError:
        from fallback_strategy import fallback_for_fix_order
    
    # Cek section dan generate jika perlu
    if not fallback_for_fix_order(file_path):
        return False  # File tidak ada atau user cancel
    
    # Lanjut proses fix-order normal (section sudah ada)
    print("🔄 Continuing with fix-order process...")
    
    # Urutan standar yang diinginkan - GUNAKAN FUNGSI YANG SUDAH ADA
    correct_order = get_correct_language_order()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Memperbaiki urutan bahasa di: {file_path}")
        
        # Cari section DISPLAY_LANGUAGES
        start_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{'
        start_match = re.search(start_pattern, content)
        
        if not start_match:
            print("❌ DISPLAY_LANGUAGES section tidak ditemukan")
            return False
        
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
            return False
        
        # Ekstrak seluruh dictionary
        dict_content = content[start_pos:end_pos]
        
        # Ekstrak semua bahasa
        lang_pattern = r'"(\w+)":\s*(\{.*?\})(?=,\s*"|\s*\})'
        lang_matches = list(re.finditer(lang_pattern, dict_content, re.DOTALL))
        
        if not lang_matches:
            print("❌ Tidak ada bahasa yang ditemukan dalam DISPLAY_LANGUAGES")
            return False
        
        # Kumpulkan semua bahasa yang ada
        all_langs = {}
        for match in lang_matches:
            lang_code = match.group(1)
            lang_dict = match.group(2)
            all_langs[lang_code] = lang_dict
        
        print(f"📋 Bahasa yang ditemukan: {', '.join(all_langs.keys())}")
        
        # Bangun ulang dictionary dengan urutan yang benar
        new_dict_content = 'DISPLAY_LANGUAGES = {\n'
        
        for i, lang_code in enumerate(correct_order):
            if lang_code in all_langs:
                if i > 0:
                    new_dict_content += ',\n'
                new_dict_content += f'    "{lang_code}": {all_langs[lang_code]}'
        
        new_dict_content += '\n}'
        
        # Ganti bagian lama dengan yang baru
        new_content = content[:start_pos] + new_dict_content + content[end_pos:]
        
        # Backup file lama
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Tulis file baru
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Urutan bahasa diperbaiki!")
        print(f"📁 Backup disimpan sebagai: {backup_path}")
        
        # Tampilkan urutan baru
        new_langs = [lang for lang in correct_order if lang in all_langs]
        print(f"🔄 Urutan baru: {', '.join(new_langs)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_current_order(file_path):
    """Tampilkan urutan bahasa saat ini"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cari semua bahasa
        langs = re.findall(r'"(\w+)":\s*\{', content)
        print(f"🔍 Urutan saat ini di {file_path}:")
        print(f"   {', '.join(langs)}")
        
    except Exception as e:
        print(f"❌ Error membaca file: {e}")

def verify_fix(file_path):
    """Verifikasi bahwa perbaikan berhasil"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cari semua bahasa setelah perbaikan
        langs = re.findall(r'"(\w+)":\s*\{', content)
        expected_order = get_correct_language_order()  # ✅ GUNAKAN FUNGSI
        
        print(f"🔍 Verifikasi urutan setelah perbaikan:")
        print(f"   Urutan aktual: {', '.join(langs)}")
        print(f"   Urutan yang diharapkan: {', '.join(expected_order)}")
        
        # Bandingkan
        if langs == expected_order:
            print("✅ VERIFIKASI BERHASIL: Urutan sudah benar!")
            return True
        else:
            print("❌ VERIFIKASI GAGAL: Urutan masih salah!")
            return False
            
    except Exception as e:
        print(f"❌ Error verifikasi: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fix_language_order(sys.argv[1])
    else:
        print("❌ Please provide a target file")
        print("Usage: python fix_order.py <filename>")