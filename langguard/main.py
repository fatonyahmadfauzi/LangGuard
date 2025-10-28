#!/usr/bin/env python3
"""
LangGuard - Multilingual Dictionary Guardian
"""

import os
import re
import argparse
import sys
from pathlib import Path

def show_banner():
    print("🛡️ LangGuard - Multilingual Dictionary Guardian")
    print("Author: Fatony Ahmad Fauzi")
    print("Email: fatonyahmadfauzi@gmail.com")
    print("=" * 50)

def main():
    show_banner()
    
    parser = argparse.ArgumentParser(description='LangGuard - Multilingual Dictionary Guardian')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # check command
    check_parser = subparsers.add_parser('check', help='Check file consistency')
    check_parser.add_argument('file', nargs='?', help='Python file to check (optional for auto)')
    check_parser.add_argument('-a', '--auto', action='store_true', help='Auto-check all files')
    
    # template command
    template_parser = subparsers.add_parser('template', help='Create empty template')
    template_parser.add_argument('--langs', help='Languages (comma separated)')
    
    # list command
    subparsers.add_parser('list', help='List files with DISPLAY_LANGUAGES')
    
    # version command
    subparsers.add_parser('version', help='Show version')
    
    # auto command
    subparsers.add_parser('auto', help='Auto analyze all files')
    
    # create command
    create_parser = subparsers.add_parser('create', help='Create DISPLAY_LANGUAGES section')
    create_parser.add_argument('file', help='File to create section in')
    
    args = parser.parse_args()
    
    if args.command == 'check':
        if args.auto:
            auto_check_all()
        elif args.file:
            if os.path.exists(args.file):
                check_file(args.file)
            else:
                print(f"❌ File not found: {args.file}")
        else:
            print("❌ Specify file or use --auto")
            print("   Examples:")
            print("     langguard check myfile.py")
            print("     langguard check --auto")
    
    elif args.command == 'template':
        languages = None
        if args.langs:
            languages = [lang.strip() for lang in args.langs.split(',')]
        create_template(languages)
    
    elif args.command == 'list':
        list_files()
    
    elif args.command == 'version':
        print("LangGuard v1.0.0")
        print("By Fatony Ahmad Fauzi")
        print("Email: fatonyahmadfauzi@gmail.com")
    
    elif args.command == 'auto':
        auto_check_all()
    
    elif args.command == 'create':
        if os.path.exists(args.file):
            create_section(args.file)
        else:
            print(f"❌ File not found: {args.file}")
    
    else:
        parser.print_help()
        print("\n📖 Examples:")
        print("  langguard check my_script.py")
        print("  langguard check --auto")
        print("  langguard template")
        print("  langguard template --langs en,id,jp")
        print("  langguard list")
        print("  langguard create new_file.py")
        print("  langguard auto")

def check_file(file_path):
    """Check consistency of DISPLAY_LANGUAGES in a file"""
    print(f"🔍 Checking: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'DISPLAY_LANGUAGES' in content:
            # Hitung bahasa
            langs = re.findall(r'"(\w+)":\s*{', content)
            unique_langs = set(langs)
            print(f"✅ Found {len(unique_langs)} languages: {', '.join(unique_langs)}")
            
            # Analisis detail setiap bahasa
            lang_stats = {}
            for lang in unique_langs:
                # Cari bagian bahasa tersebut
                lang_pattern = rf'"{lang}":\s*{{(.*?)}}'
                lang_match = re.search(lang_pattern, content, re.DOTALL)
                if lang_match:
                    lang_content = lang_match.group(1)
                    # Hitung phrases (key-value pairs)
                    phrases = re.findall(r'"([^"]+)":\s*"[^"]*"', lang_content)
                    lang_stats[lang] = len(phrases)
                    print(f"   📝 {lang.upper()}: {len(phrases)} phrases")
            
            # Cek konsistensi
            if lang_stats:
                phrase_counts = list(lang_stats.values())
                if len(set(phrase_counts)) == 1:
                    print(f"🎉 SEMUA BAHASA KONSISTEN! ({phrase_counts[0]} phrases each)")
                else:
                    print("⚠️  PERHATIAN: Jumlah phrases tidak konsisten!")
                    for lang, count in lang_stats.items():
                        print(f"   {lang.upper()}: {count} phrases")
            
            return True
        else:
            print("❌ No DISPLAY_LANGUAGES found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def auto_check_all():
    """Automatically check all Python files with DISPLAY_LANGUAGES"""
    print("🔍 Auto-checking all files...")
    files = list_files(quiet=True)
    
    if not files:
        print("❌ No files with DISPLAY_LANGUAGES found")
        return
    
    print(f"\n📊 Found {len(files)} files to analyze:")
    
    consistent_files = 0
    for file_path in files:
        print(f"\n{'='*50}")
        if check_file(file_path):
            consistent_files += 1
    
    print(f"\n🎯 SUMMARY: {consistent_files}/{len(files)} files consistent")

def create_template(languages=None):
    """Create empty DISPLAY_LANGUAGES template"""
    if languages is None:
        languages = ['en', 'pl', 'zh', 'jp', 'de', 'fr', 'es', 'ru', 'pt', 'id', 'kr']
    
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

def list_files(quiet=False):
    """List files with DISPLAY_LANGUAGES"""
    if not quiet:
        print("🔍 Searching for files with DISPLAY_LANGUAGES...")
    
    found_files = []
    
    for file in os.listdir('.'):
        if file.endswith('.py'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    if 'DISPLAY_LANGUAGES' in f.read():
                        found_files.append(file)
                        if not quiet:
                            print(f"✅ Found: {file}")
            except Exception as e:
                if not quiet:
                    print(f"⚠️  Error reading {file}: {e}")
    
    if not quiet:
        print(f"📊 Total files with DISPLAY_LANGUAGES: {len(found_files)}")
    
    return found_files

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

def create_template_internal(quiet=False):
    """Create template (internal version without banner)"""
    languages = ['en', 'pl', 'zh', 'jp', 'de', 'fr', 'es', 'ru', 'pt', 'id', 'kr']
    
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

if __name__ == "__main__":
    main()