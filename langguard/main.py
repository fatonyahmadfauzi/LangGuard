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
    from .insert_section import run_insert_section
    from .remove_languages import run_remove_languages
    from .repair_functions import run_repair_functions
    from .update_language import run_set_global_lang
    from .add_languages import run_add_languages
    from .js_i18n_tools import (
        run_js_generate_section,
        run_js_add_languages,
        run_js_remove_languages,
        run_js_set_global_lang,
        run_js_repair,
        run_js_translate,
    )
except ImportError:
    from analysis import analyze_file, auto_check_all, list_files
    from clipboard import clipboard_template, create_section
    from translate import run_translate
    from insert_section import run_insert_section
    from remove_languages import run_remove_languages
    from repair_functions import run_repair_functions
    from update_language import run_set_global_lang
    from add_languages import run_add_languages
    from js_i18n_tools import (
        run_js_generate_section,
        run_js_add_languages,
        run_js_remove_languages,
        run_js_set_global_lang,
        run_js_repair,
        run_js_translate,
    )


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"

def show_banner():
    print(f"{CYAN}" + "=" * 78 + f"{RESET}")
    print(f"{GREEN}" + r"""
 _                               _____                     _
| |                             / ____|                   | |
| |      __ _ _ __   __ _      | |  __ _   _  __ _ _ __ __| |
| |     / _` | '_ \ / _` |     | | |_ | | | |/ _` | '__/ _` |
| |____| (_| | | | | (_| |     | |__| | |_| | (_| | | | (_| |
|______|\__,_|_| |_|\__, |      \_____|\__,_|\__,_|_|  \__,_|
                     __/ |
                    |___/
""" + f"{RESET}")
    print("Multilingual Dictionary Guardian")
    print("Developer: Fatony Ahmad Fauzi")
    print(f"{CYAN}" + "=" * 78 + f"{RESET}")


def ask_file_path(label="target file"):
    file_path = input(f"{YELLOW}[+] Enter {label}: {RESET}").strip()
    if not file_path:
        print("❌ File path cannot be empty")
        return None
    return file_path


def is_js_file(path):
    return str(path).lower().endswith('.js')


def run_interactive_menu():
    while True:
        pause_after_action = True
        show_banner()
        print(f"{GREEN}[1] Check file / auto-check")
        print("[2] Clipboard template")
        print("[3] Generate DISPLAY_LANGUAGES section")
        print("[4] Add missing languages")
        print("[5] Remove languages")
        print("[6] Set global language")
        print("[7] Repair functions/section")
        print("[8] Auto-translate missing phrases")
        print("[9] Version")
        print(f"{GRAY}[0] Exit{RESET}")

        choice = input(f"\n{YELLOW}[+] Select option: {RESET}").strip()

        if choice == "0":
            print("👋 Bye!")
            return

        if choice == "1":
            mode = input("Use auto mode? (y/N): ").strip().lower()
            target = input("Target folder/file path (empty=current folder): ").strip()
            target_path = target or '.'

            if mode in ["y", "yes"]:
                auto_check_all(target_path=target_path)
                pause_after_action = False
            else:
                if os.path.isfile(target_path):
                    analyze_file(target_path)
                elif os.path.isdir(target_path):
                    print(f"ℹ️ '{target_path}' is a folder. Running auto-check for that folder.")
                    auto_check_all(target_path=target_path)
                else:
                    print(f"❌ Path not found: {target_path}")

        elif choice == "2":
            custom_lang = input("Languages (comma separated, empty=all): ").strip()
            languages = [lang.strip() for lang in custom_lang.split(',')] if custom_lang else None
            clipboard_template(languages)

        elif choice == "3":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_generate_section(file_path)
                else:
                    run_insert_section(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "4":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_add_languages(file_path)
                else:
                    run_add_languages(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "5":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_remove_languages(file_path)
                else:
                    run_remove_languages(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "6":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_set_global_lang(file_path)
                else:
                    run_set_global_lang(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "7":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_repair(file_path)
                else:
                    run_repair_functions(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "8":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_translate(file_path)
                else:
                    run_translate(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "9":
            print("LangGuard v1.0.0")
            print("By Fatony Ahmad Fauzi")
            print("Email: fatonyahmadfauzi@gmail.com")

        else:
            print("❌ Invalid option")

        if pause_after_action:
            input("\nPress Enter to continue...")
            print("\n" * 2)

        choice = input(f"\n{YELLOW}[+] Select option: {RESET}").strip()

        if choice == "0":
            print("👋 Bye!")
            return

        if choice == "1":
            mode = input("Use auto mode? (y/N): ").strip().lower()
            if mode in ["y", "yes"]:
                target = input("Target folder/file path (empty=current folder): ").strip()
                auto_check_all(target_path=target or '.')
                pause_after_action = False
            else:
                file_path = ask_file_path("python file")
                if file_path and os.path.exists(file_path):
                    analyze_file(file_path)
                elif file_path:
                    print(f"❌ File not found: {file_path}")

        elif choice == "2":
            custom_lang = input("Languages (comma separated, empty=all): ").strip()
            languages = [lang.strip() for lang in custom_lang.split(',')] if custom_lang else None
            clipboard_template(languages)

        elif choice == "3":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_generate_section(file_path)
                else:
                    run_insert_section(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "4":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_add_languages(file_path)
                else:
                    run_add_languages(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "5":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_remove_languages(file_path)
                else:
                    run_remove_languages(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "6":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_set_global_lang(file_path)
                else:
                    run_set_global_lang(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "7":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_repair(file_path)
                else:
                    run_repair_functions(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "8":
            file_path = ask_file_path()
            if file_path and os.path.exists(file_path):
                if is_js_file(file_path):
                    run_js_translate(file_path)
                else:
                    run_translate(file_path)
            elif file_path:
                print(f"❌ File not found: {file_path}")

        elif choice == "9":
            print("LangGuard v1.0.0")
            print("By Fatony Ahmad Fauzi")
            print("Email: fatonyahmadfauzi@gmail.com")

        else:
            print("❌ Invalid option")

        if pause_after_action:
            input("\nPress Enter to continue...")
            print("\n" * 2)

        input("\nPress Enter to continue...")
        print("\n" * 2)

        input("\nPress Enter to continue...")
        print("\n" * 2)

def main():
    if len(sys.argv) == 1:
        run_interactive_menu()
        return

    show_banner()

    parser = argparse.ArgumentParser(description='LangGuard - Multilingual Dictionary Guardian')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # ANALYSIS COMMANDS (read-only)
    check_parser = subparsers.add_parser('check', help='Analyze DISPLAY_LANGUAGES section (read-only)')
    check_parser.add_argument('file', nargs='?', help='Python file to analyze (optional for auto)')
    check_parser.add_argument('-a', '--auto', action='store_true', help='Auto-analyze all files')
    check_parser.add_argument('-t', '--target', help='Target folder/file for auto-check (default: current folder)')

    clipboard_parser = subparsers.add_parser('clipboard', help='Copy template to clipboard (read-only)')
    clipboard_parser.add_argument('--lang', help='Languages (comma separated)')

    translate_parser = subparsers.add_parser('translate', help='Auto-translate missing phrases in DISPLAY_LANGUAGES (modifies file)')
    translate_parser.add_argument('file', help='File to translate phrases in')

    version_parser = subparsers.add_parser('version', help='Show version (read-only)')

    generate_parser = subparsers.add_parser('generate', help='Generate complete DISPLAY_LANGUAGES section (modifies file)')
    generate_parser.add_argument('file', help='File to generate section in')

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
            auto_check_all(target_path=args.target or '.')
        elif args.file:
            if os.path.exists(args.file):
                analyze_file(args.file)
            else:
                print(f"❌ File not found: {args.file}")
        else:
            print("❌ Specify file or use --auto")

    elif args.command == 'clipboard':
        languages = None
        if args.lang:
            languages = [lang.strip() for lang in args.lang.split(',')]
        clipboard_template(languages)

    elif args.command == 'translate':
        if os.path.exists(args.file):
            if is_js_file(args.file):
                run_js_translate(args.file)
            else:
                run_translate(args.file)
        else:
            print(f"❌ File not found: {args.file}")

    elif args.command == 'version':
        print("LangGuard v1.0.0")
        print("By Fatony Ahmad Fauzi")
        print("Email: fatonyahmadfauzi@gmail.com")

    elif args.command == 'generate':
        if os.path.exists(args.file):
            if is_js_file(args.file):
                run_js_generate_section(args.file)
            else:
                run_insert_section(args.file)
        else:
            print(f"❌ File not found: {args.file}")

    elif args.command == 'remove-lang':
        if os.path.exists(args.file):
            if is_js_file(args.file):
                run_js_remove_languages(args.file)
            else:
                run_remove_languages(args.file)
        else:
            print(f"❌ File not found: {args.file}")

    elif args.command == 'repair':
        if os.path.exists(args.file):
            if is_js_file(args.file):
                run_js_repair(args.file)
            else:
                run_repair_functions(args.file)
        else:
            print(f"❌ File not found: {args.file}")

    elif args.command == 'set-global-lang':
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
        else:
            if is_js_file(args.file):
                run_js_set_global_lang(args.file)
            else:
                run_set_global_lang(args.file)

    elif args.command == 'add-lang':
        if os.path.exists(args.file):
            if is_js_file(args.file):
                run_js_add_languages(args.file)
            else:
                run_add_languages(args.file)
        else:
            print(f"❌ File not found: {args.file}")

    else:
        parser.print_help()
        print("\n📖 COMMAND GUIDE:")
        print("  ANALYSIS COMMANDS (read-only, safe to run):")
        print("    langguard check my_script.py       # Analyze DISPLAY_LANGUAGES section")
        print("    langguard check --auto             # Auto-analyze all files")
        print("    langguard check --auto --target C:/path/to/folder # Auto-check specific folder")
        print("    langguard clipboard                # Copy complete template to clipboard")
        print("    langguard clipboard --lang en,id,jp # Copy custom template to clipboard")
        print("    langguard version                  # Show version information")
        print("")
        print("  MAINTENANCE COMMANDS (modifies files, creates backup):")
        print("    langguard generate my_script.py    # Generate complete DISPLAY_LANGUAGES section")
        print("    langguard add-lang my_script.py    # Add specific missing languages")
        print("    langguard remove-lang my_script.py # Remove languages from section")
        print("    langguard repair my_script.py      # Repair section structure and functions")
        print("    langguard set-global-lang my_script.py # Set default display language")
        print("    langguard translate my_script.py   # Auto-translate missing phrases")
        print("")
        print("💡 TIP: Use 'check' first to see current status before making changes.")


if __name__ == "__main__":
    main()
