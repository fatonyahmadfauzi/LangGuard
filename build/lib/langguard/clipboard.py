#!/usr/bin/env python3
"""
LangGuard - Clipboard Functions for Template Management
"""

try:
    from .add_languages import get_correct_language_order
except ImportError:
    from add_languages import get_correct_language_order


def clipboard_template(languages=None):
    """Create DISPLAY_LANGUAGES template and copy to clipboard"""
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
    
    # Copy to clipboard
    try:
        import pyperclip
        pyperclip.copy(template)
        print("✅ Template copied to clipboard!")
        print("💡 You can now paste it into your Python file")
        return True
    except ImportError:
        print("❌ pyperclip not installed. Cannot copy to clipboard.")
        print("💡 Install pyperclip: pip install pyperclip")
        print("📝 Manual: Copy the template above manually")
        return False


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


# ======================== CLI MODE ========================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # Default: copy complete template to clipboard
        clipboard_template()
    elif len(sys.argv) == 2 and sys.argv[1] == "--help":
        print("📋 LangGuard - Clipboard Template")
        print("Usage:")
        print("  python clipboard.py                    # Copy complete template to clipboard")
        print("  python clipboard.py --lang en,id,jp  # Copy custom template to clipboard")
    # clipboard.py - di bagian __main__
    elif "--lang" in sys.argv:  # ✅ ubah "--langs" menjadi "--lang"
        # Extract languages from command line
        langs_index = sys.argv.index("--lang") + 1  # ✅ ubah "--langs" menjadi "--lang"
        if langs_index < len(sys.argv):
            languages = [lang.strip() for lang in sys.argv[langs_index].split(',')]
            clipboard_template(languages)
        else:
            print("❌ Please specify languages after --lang")
    else:
        print("❌ Invalid arguments. Use --help for usage information.")