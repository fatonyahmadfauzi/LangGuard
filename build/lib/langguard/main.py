#!/usr/bin/env python3
"""
LangGuard - Multilingual Dictionary Guardian
CLI Interface & Command Router
"""

import os
import argparse
import sys

try:
    from .analysis import analyze_file, auto_check_all, list_files
    from .clipboard import clipboard_template, create_section
    from .translate import run_translate
    from .fix_order import fix_language_order
    from .insert_section import run_insert_section
    from .remove_languages import run_remove_languages
    from .repair_functions import run_repair_functions
    from .update_language import choose_language, set_default_display_language_in_file
    from .add_languages import (
        show_all_language_options, 
        get_language_selection, 
        add_languages_to_content,
        show_missing_language_options,      
        get_missing_language_selection,     
        get_missing_languages_from_content,
    )
except ImportError:
    from analysis import analyze_file, auto_check_all, list_files
    from clipboard import clipboard_template, create_section
    from translate import run_translate
    from fix_order import fix_language_order
    from insert_section import run_insert_section
    from remove_languages import run_remove_languages
    from repair_functions import run_repair_functions
    from update_language import choose_language, set_default_display_language_in_file
    from add_languages import (
        show_all_language_options, 
        get_language_selection, 
        add_languages_to_content,
        show_missing_language_options,      
        get_missing_language_selection,     
        get_missing_languages_from_content,
    )


def show_banner():
    print("🛡️ LangGuard - Multilingual Dictionary Guardian")
    print("Author: Fatony Ahmad Fauzi")
    print("Email: fatonyahmadfauzi@gmail.com")
    print("=" * 50)


def main():
    show_banner()
    
    parser = argparse.ArgumentParser(description='LangGuard - Multilingual Dictionary Guardian')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # ANALYSIS COMMANDS (read-only)
    check_parser = subparsers.add_parser('check', help='Analyze DISPLAY_LANGUAGES section (read-only)')
    check_parser.add_argument('file', nargs='?', help='Python file to analyze (optional for auto)')
    check_parser.add_argument('-a', '--auto', action='store_true', help='Auto-analyze all files')
    
    clipboard_parser = subparsers.add_parser('clipboard', help='Copy template to clipboard (read-only)')
    # ✅ PERBAIKAN: Sesuaikan dengan parameter yang benar
    clipboard_parser.add_argument('--lang', help='Languages (comma separated)')

    translate_parser = subparsers.add_parser('translate', help='Auto-translate missing phrases in DISPLAY_LANGUAGES (modifies file)')
    translate_parser.add_argument('file', help='File to translate phrases in')
    
    version_parser = subparsers.add_parser('version', help='Show version (read-only)')
    
    # MAINTENANCE COMMANDS (modifies files)
    fix_order_parser = subparsers.add_parser('fix-order', help='Fix language order in a file (modifies file)')
    fix_order_parser.add_argument('file', help='File to fix order in')
    
    # ✅ UBAH: insert menjadi generate
    generate_parser = subparsers.add_parser('generate', help='Generate complete DISPLAY_LANGUAGES section (modifies file)')
    generate_parser.add_argument('file', help='File to generate section in')
    
    # ✅ UBAH: remove menjadi remove-lang
    remove_lang_parser = subparsers.add_parser('remove-lang', help='Remove languages from file (modifies file)')
    remove_lang_parser.add_argument('file', help='File to remove languages from')
    
    repair_parser = subparsers.add_parser('repair', help='Repair functions only (modifies file)')
    repair_parser.add_argument('file', help='File to repair functions in')

    set_lang_parser = subparsers.add_parser('set-global-lang', help='Set global DISPLAY_LANG value interactively (modifies file)')
    set_lang_parser.add_argument('file', help='File to update display language in')

    add_lang_parser = subparsers.add_parser('add-lang', help='Add missing languages to existing DISPLAY_LANGUAGES (modifies file)')
    add_lang_parser.add_argument('file', help='File to add languages to')
    
    args = parser.parse_args()
    
    # COMMAND ROUTING
    if args.command == 'check':
        if args.auto:
            auto_check_all()
        elif args.file:
            if os.path.exists(args.file):
                analyze_file(args.file)
            else:
                print(f"❌ File not found: {args.file}")
        else:
            print("❌ Specify file or use --auto")
    
    elif args.command == 'clipboard':
        languages = None
        # ✅ PERBAIKAN: Sesuaikan dengan nama parameter yang benar
        if args.lang:
            languages = [lang.strip() for lang in args.lang.split(',')]
        clipboard_template(languages)

    elif args.command == 'translate':
        if os.path.exists(args.file):
            run_translate(args.file)
        else:
            print(f"❌ File not found: {args.file}")
    
    elif args.command == 'version':
        print("LangGuard v1.0.0")
        print("By Fatony Ahmad Fauzi")
        print("Email: fatonyahmadfauzi@gmail.com")
    
    elif args.command == 'fix-order':
        if os.path.exists(args.file):
            fix_language_order(args.file)
        else:
            print(f"❌ File not found: {args.file}")
            
    # ✅ UBAH: insert menjadi generate
    elif args.command == 'generate':
        if os.path.exists(args.file):
            run_insert_section(args.file)
        else:
            print(f"❌ File not found: {args.file}")
            
    # ✅ UBAH: remove menjadi remove-lang
    elif args.command == 'remove-lang':
        if os.path.exists(args.file):
            run_remove_languages(args.file)
        else:
            print(f"❌ File not found: {args.file}")
    
    elif args.command == 'repair':
        if os.path.exists(args.file):
            run_repair_functions(args.file)
        else:
            print(f"❌ File not found: {args.file}")

    elif args.command == 'set-global-lang':
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
        else:
            # Gunakan fungsi yang sudah ada di update_language.py untuk konsistensi
            try:
                from .update_language import run_set_global_lang
                run_set_global_lang(args.file)
            except ImportError:
                from update_language import run_set_global_lang
                run_set_global_lang(args.file)

    # Di main.py - bagian add-lang command
    elif args.command == 'add-lang':
        if os.path.exists(args.file):
            try:
                from .add_languages import run_add_languages
                run_add_languages(args.file)
            except ImportError:
                from add_languages import run_add_languages
                run_add_languages(args.file)
        else:
            print(f"❌ File not found: {args.file}")

    else:
        parser.print_help()
        print("\n📖 COMMAND GUIDE:")
        print("  ANALYSIS COMMANDS (read-only, safe to run):")
        print("    langguard check my_script.py       # Analyze DISPLAY_LANGUAGES section")
        print("    langguard check --auto             # Auto-analyze all files")
        print("    langguard clipboard                # Copy complete template to clipboard")
        print("    langguard clipboard --lang en,id,jp # Copy custom template to clipboard")  # ✅ PERBAIKAN: Sesuaikan dengan parameter yang benar
        print("    langguard version                  # Show version information")
        print("")
        print("  MAINTENANCE COMMANDS (modifies files, creates backup):")
        print("    langguard generate my_script.py    # Generate complete DISPLAY_LANGUAGES section")
        print("    langguard add-lang my_script.py    # Add specific missing languages")
        print("    langguard remove-lang my_script.py # Remove languages from section")
        print("    langguard repair my_script.py      # Repair section structure and functions")
        print("    langguard fix-order my_script.py   # Fix language order only")
        print("    langguard set-global-lang my_script.py # Set default display language")
        print("    langguard translate my_script.py   # Auto-translate missing phrases")
        print("")
        print("💡 TIP: Use 'check' first to see current status before making changes.")

if __name__ == "__main__":
    main()