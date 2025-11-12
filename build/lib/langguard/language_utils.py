# language_utils.py
#!/usr/bin/env python3
"""
LangGuard - Language Utility Functions
Centralized functions to avoid circular imports
"""

import re

def get_all_supported_languages():
    """Return all supported languages"""
    return ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"]

def get_correct_language_order():
    """Return the correct language order"""
    return ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"]

def get_existing_languages_from_content(content):
    """Ambil daftar bahasa yang sudah ada dari konten file"""
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

def extract_english_phrases(content):
    """Ekstrak semua phrases dari bagian bahasa Inggris"""
    english_phrases = {}

    display_pattern = r'DISPLAY_LANGUAGES\s*=\s*\{([\s\S]*?)\n\}'
    display_match = re.search(display_pattern, content, re.DOTALL)
    if not display_match:
        return english_phrases

    display_content = display_match.group(1)

    en_pattern = r'"en":\s*\{([\s\S]*?)\n    \}'
    en_match = re.search(en_pattern, display_content, re.DOTALL)
    if not en_match:
        return english_phrases

    en_content = en_match.group(1)
    phrase_pattern = r'"([^"]+)":\s*"([^"]*)"'
    phrases = re.findall(phrase_pattern, en_content)
    for key, value in phrases:
        english_phrases[key] = value

    return english_phrases