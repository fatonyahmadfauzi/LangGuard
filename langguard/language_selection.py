#!/usr/bin/env python3
"""
LangGuard - Centralized Language Selection Functions
"""

import re

# ✅ GUNAKAN language_utils untuk menghindari circular import
try:
    from .language_utils import (
        get_all_supported_languages,
        get_correct_language_order
    )
except ImportError:
    from language_utils import (
        get_all_supported_languages,
        get_correct_language_order
    )

# Mapping nama bahasa
LANGUAGE_NAMES = {
    "en": "English", "pl": "Polski", "zh": "中文", "jp": "日本語",
    "de": "Deutsch", "fr": "Français", "es": "Español", "ru": "Pycckuñ",
    "pt": "Portugués", "id": "Indonesia", "kr": "한국어"
}

def show_language_selection(available_langs=None, current_default=None, context="add"):
    """
    Tampilkan pilihan bahasa dengan format standar
    
    Args:
        available_langs: List bahasa yang tersedia (None untuk semua)
        current_default: Bahasa default saat ini (untuk penanda)
        context: Konteks penggunaan ('add', 'remove', 'set-default')
    """
    
    if available_langs is None:
        available_langs = get_all_supported_languages()
    
    # Urutkan sesuai standar
    correct_order = get_correct_language_order()
    sorted_langs = [lang for lang in correct_order if lang in available_langs]
    
    # Tampilkan header berdasarkan konteks
    if context == "remove":
        print("\n🎯 Select languages to REMOVE:")
    elif context == "set-default":
        print("\n🎯 Select DEFAULT display language:")
    else:
        print("\n🎯 Select languages for DISPLAY_LANGUAGES:")
    
    print("Available languages:")
    print("=" * 50)
    
    # Tampilkan setiap bahasa
    for i, lang_code in enumerate(sorted_langs, 1):
        lang_name = LANGUAGE_NAMES.get(lang_code, lang_code)
        # Tambahkan penanda default jika ada
        default_indicator = " ⭐ (CURRENT DEFAULT)" if lang_code == current_default else ""
        print(f"  {i}. {lang_code} - {lang_name}{default_indicator}")
    
    print("=" * 50)
    
    # Tampilkan instruksi khusus berdasarkan konteks
    if context == "remove" and current_default:
        print(f"💡 Default language ({current_default}) cannot be removed!")
    elif context == "set-default":
        print("💡 This will be the initial active language")

def get_user_language_selection(available_langs=None, allow_multiple=True, allow_skip=True, context="add"):
    """
    Dapatkan pilihan bahasa dari user
    
    Args:
        available_langs: List bahasa yang tersedia
        allow_multiple: Apakah boleh memilih multiple languages
        allow_skip: Apakah ada opsi skip
        context: Konteks penggunaan
    
    Returns:
        List bahasa yang dipilih, atau string khusus
    """
    
    if available_langs is None:
        available_langs = get_all_supported_languages()
    
    # Urutkan sesuai standar
    correct_order = get_correct_language_order()
    sorted_langs = [lang for lang in correct_order if lang in available_langs]
    
    while True:
        print(f"\n👉 Enter your choice:")
        
        # Instruksi dasar
        instructions = [
            "   - Single number (e.g., 1)",
            "   - Language codes separated by comma (e.g., en,id,kr)"
        ]
        
        # Tambahkan instruksi berdasarkan konteks
        if allow_multiple and len(sorted_langs) > 1:
            instructions.append("   - Multiple numbers separated by comma (e.g., 1,3,5)")
        
        if context != "set-default":  # 'A' tidak relevan untuk set-default
            instructions.append("   - 'A' for all languages")
        
        if allow_skip:
            instructions.append("   - 'S' to skip")
        
        # Instruksi khusus untuk remove
        if context == "remove":
            instructions.append("   - 'T' to remove entire DISPLAY_LANGUAGES section")
        
        # Tampilkan semua instruksi
        for instruction in instructions:
            print(instruction)
        
        choice = input("Your choice: ").strip().upper()
        
        # Handle special cases
        if choice == 'S' and allow_skip:
            print("⏭️ Operation skipped. No changes made.")
            return []
        
        if choice == 'A' and context != "set-default":
            return sorted_langs
        
        if choice == 'T' and context == "remove":
            confirm = input("⚠️  PERINGATAN: Ini akan menghapus SELURUH bagian DISPLAY_LANGUAGES! Lanjutkan? (y/N): ").strip().lower()
            if confirm == 'y':
                return "REMOVE_ALL_SECTION"
            else:
                print("ℹ️ Penghapusan section dibatalkan")
                continue
        
        # Handle language codes input (en,id,kr)
        if any(lang in choice.lower() for lang in sorted_langs):
            selected_codes = [code.strip().lower() for code in choice.split(',')]
            valid_codes = []
            invalid_codes = []
            
            for code in selected_codes:
                if code in sorted_langs:
                    if code not in valid_codes:
                        valid_codes.append(code)
                else:
                    invalid_codes.append(code)
            
            if invalid_codes:
                print(f"❌ Invalid language codes: {', '.join(invalid_codes)}")
                print(f"💡 Available codes: {', '.join(sorted_langs)}")
            
            if valid_codes:
                # Untuk set-default, hanya boleh satu bahasa
                if context == "set-default" and len(valid_codes) > 1:
                    print("❌ Please select only ONE language for default display language")
                    continue
                return valid_codes if allow_multiple else valid_codes[0]
            else:
                print("❌ No valid languages selected")
        
        # Handle number input
        elif ',' in choice and allow_multiple:
            selected_numbers = [num.strip() for num in choice.split(',')]
            selected_languages = []
            
            for num_str in selected_numbers:
                if num_str.isdigit():
                    index = int(num_str) - 1
                    if 0 <= index < len(sorted_langs):
                        lang_code = sorted_langs[index]
                        if lang_code not in selected_languages:
                            selected_languages.append(lang_code)
                    else:
                        print(f"❌ Invalid number: {num_str}")
                        break
                else:
                    print(f"❌ Invalid input: {num_str}")
                    break
            else:  # Jika tidak ada break
                # Untuk set-default, hanya boleh satu bahasa
                if context == "set-default" and len(selected_languages) > 1:
                    print("❌ Please select only ONE language for default display language")
                    continue
                return selected_languages
        
        elif choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(sorted_langs):
                return [sorted_langs[index]] if allow_multiple else sorted_langs[index]
            else:
                print(f"❌ Please enter number between 1 and {len(sorted_langs)}")
        
        else:
            print(f"❌ Invalid choice. Please enter:")
            print(f"   - A number (1-{len(sorted_langs)})")
            if allow_multiple and len(sorted_langs) > 1:
                print(f"   - Multiple numbers (e.g., 1,3,5)")
            print(f"   - Language code(s) ({', '.join(sorted_langs)})")
            if context != "set-default":
                print(f"   - 'A' for all languages")
            if allow_skip:
                print(f"   - 'S' to skip")
            if context == "remove":
                print(f"   - 'T' to remove entire section")

# Fungsi convenience untuk use case umum
def select_languages_for_addition():
    """Pemilihan bahasa untuk penambahan"""
    show_language_selection(context="add")
    return get_user_language_selection(allow_multiple=True, context="add")

def select_languages_for_removal(available_langs, current_default):
    """Pemilihan bahasa untuk penghapusan"""
    show_language_selection(available_langs=available_langs, current_default=current_default, context="remove")
    return get_user_language_selection(available_langs=available_langs, allow_multiple=True, context="remove")

def select_default_language(available_langs, current_default):
    """
    Pemilihan bahasa default
    ✅ PERBAIKAN: Jika hanya ada satu bahasa, otomatis pilih tanpa tanya
    """
    # ✅ PERBAIKAN: Jika hanya ada satu bahasa, otomatis pilih tanpa tanya user
    if len(available_langs) == 1:
        single_lang = available_langs[0]
        lang_name = LANGUAGE_NAMES.get(single_lang, single_lang.upper())
        print(f"🌍 Global language automatically set to: {lang_name} ({single_lang})")
        return single_lang
    
    # Jika ada multiple bahasa, tampilkan pilihan seperti biasa
    show_language_selection(available_langs=available_langs, current_default=current_default, context="set-default")
    return get_user_language_selection(available_langs=available_langs, allow_multiple=False, context="set-default")