#!/usr/bin/env python3
"""
LangGuard - Template Utility Functions
"""

try:
    from .add_languages import get_correct_language_order
except ImportError:
    from add_languages import get_correct_language_order


def create_template(languages=None):
    """Create empty DISPLAY_LANGUAGES template dengan urutan yang benar"""
    if languages is None:
        languages = get_correct_language_order()
    else:
        # Urutkan bahasa yang dipilih sesuai standar
        correct_order = get_correct_language_order()
        languages = [lang for lang in correct_order if lang in languages]
    
    template = '''# ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------
DISPLAY_LANGUAGES = {'''
    
    for i, lang in enumerate(languages):
        if i == 0:
            template += f'''
    "{lang}": {{
        # {lang.upper()} translations will go here
    }}'''
        else:
            template += f''',
    "{lang}": {{
        # {lang.upper()} translations will go here
    }}'''
    
    template += '\n}'
    
    print("📋 DISPLAY_LANGUAGES TEMPLATE:")
    print("=" * 50)
    print(template)
    print("=" * 50)
    
    # Coba copy ke clipboard
    try:
        import pyperclip
        pyperclip.copy(template)
        print("📋 Template copied to clipboard!")
    except ImportError:
        print("💡 Install pyperclip for auto-copy: pip install pyperclip")
    
    return template


def create_template_internal(quiet=False):
    """Create template (internal version without banner)"""
    languages = get_correct_language_order()
    
    template = '''# ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------
DISPLAY_LANGUAGES = {'''
    
    for i, lang in enumerate(languages):
        if i == 0:
            template += f'''
    "{lang}": {{
        # {lang.upper()} translations will go here
    }}'''
        else:
            template += f''',
    "{lang}": {{
        # {lang.upper()} translations will go here
    }}'''
    
    template += '\n}'
    
    if not quiet:
        print("📋 DISPLAY_LANGUAGES TEMPLATE:")
        print("=" * 50)
        print(template)
        print("=" * 50)
    
    return template


def create_section(file_path):
    """Create DISPLAY_LANGUAGES section in a file"""
    print(f"🛠️ Creating DISPLAY_LANGUAGES section in: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cek apakah sudah ada
        if 'DISPLAY_LANGUAGES' in content:
            print("❌ DISPLAY_LANGUAGES section already exists!")
            return False
        
        # Buat template
        template = create_template_internal(quiet=True)
        
        # Tambahkan ke file (di akhir)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write('\n\n')
            f.write(template)
        
        print("✅ DISPLAY_LANGUAGES section created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False