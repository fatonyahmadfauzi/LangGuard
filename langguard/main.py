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

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default




def flush_console_input():
    """Best-effort flush for queued keyboard input in Windows consoles."""
    if os.name != "nt":
        return
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
    except Exception:
        pass


def post_action_navigation():
    """Navigation prompt after an action without requiring Enter-to-continue."""
    while True:
        nav = input("\n[1] Back to main menu\n[0] Exit\n[+] Select option: ").strip()
        if nav in ("1", ""):
            return True
        if nav == "0":
            print("👋 Bye!")
            return False
        print("❌ Invalid option")


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default




def flush_console_input():
    """Best-effort flush for queued keyboard input in Windows consoles."""
    if os.name != "nt":
        return
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
    except Exception:
        pass


def post_action_navigation():
    """Navigation prompt after an action without requiring Enter-to-continue."""
    while True:
        nav = input("\n[1] Back to main menu\n[0] Exit\n[+] Select option: ").strip()
        if nav in ("1", ""):
            return True
        if nav == "0":
            print("👋 Bye!")
            return False
        print("❌ Invalid option")


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"

# Backward-compat fallback for older interactive flows that still reference this name
pause_after_action = True  # backward-compat fallback for stale runtime code paths

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default


def flush_console_input():
    """Best-effort flush for queued keyboard input in Windows consoles."""
    if os.name != "nt":
        return
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
    except Exception:
        pass


def post_action_navigation():
    """Navigation prompt after an action without requiring Enter-to-continue."""
    while True:
        nav = input("\n[1] Back to main menu\n[0] Exit\n[+] Select option: ").strip()
        if nav in ("1", ""):
            return True
        if nav == "0":
            print("👋 Bye!")
            return False
        print("❌ Invalid option")


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default


def flush_console_input():
    """Best-effort flush for queued keyboard input in Windows consoles."""
    if os.name != "nt":
        return
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
    except Exception:
        pass


def post_action_navigation():
    """Navigation prompt after an action without requiring Enter-to-continue."""
    while True:
        nav = input("\n[1] Back to main menu\n[0] Exit\n[+] Select option: ").strip()
        if nav in ("1", ""):
            return True
        if nav == "0":
            print("👋 Bye!")
            return False
        print("❌ Invalid option")


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default




def flush_console_input():
    """Best-effort flush for queued keyboard input in Windows consoles."""
    if os.name != "nt":
        return
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
    except Exception:
        pass


def wait_for_enter_once():
    """Wait exactly once for Enter to return to main menu."""
    input("\nPress Enter to continue...")


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default




def flush_console_input():
    """Best-effort flush for queued keyboard input in Windows consoles."""
    if os.name != "nt":
        return
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
    except Exception:
        pass


def wait_for_enter_once():
    """Wait exactly once for Enter to return to main menu."""
    input("\nPress Enter to continue...")


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default


def wait_for_enter_once():
    """Wait exactly once for Enter to return to main menu."""
    input("\nPress Enter to continue...")


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default


def wait_for_enter_once():
    """Wait for a single Enter and clear buffered keystrokes to avoid repeated prompts."""
    try:
        if os.name == 'nt':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import select
            while select.select([sys.stdin], [], [], 0)[0]:
                sys.stdin.readline()
    except Exception:
        pass

    input("\nPress Enter to continue...")

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask_target_path(default='.'):
    target = input("Target folder/file path (empty=current folder): ").strip()
    return target or default


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
    file_path = input("Target folder/file path (empty=current folder): ").strip()
    if not file_path:
        return "."
    return file_path


def is_js_file(path):
    return str(path).lower().endswith('.js')

def print_version_info():
    print("LangGuard v1.0.1")
    print("By Fatony Ahmad Fauzi")
    print("Email: fatonyahmadfauzi@gmail.com")
    print(f"Runtime file: {__file__}")


def run_interactive_menu():
    while True:
        action_executed = False
        clear_screen()
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

        flush_console_input()
        choice = input(f"\n{YELLOW}[+] Select option: {RESET}").strip()

        if not choice:
            continue

        if choice == "0":
            print("👋 Bye!")
            return

        if choice == "1":
            mode = input("Use auto mode? (y/N): ").strip().lower()
            target_path = ask_target_path()

            if mode in ["y", "yes"]:
                auto_check_all(target_path=target_path)
                action_executed = True
            else:
                if os.path.isfile(target_path):
                    analyze_file(target_path)
                    action_executed = True
                elif os.path.isdir(target_path):
                    print(f"ℹ️ '{target_path}' is a folder. Running auto-check for that folder.")
                    auto_check_all(target_path=target_path)
                    action_executed = True
                else:
                    print(f"❌ Path not found: {target_path}")
                    action_executed = True

        elif choice == "2":
            custom_lang = input("Languages (comma separated, empty=all): ").strip()
            languages = [lang.strip() for lang in custom_lang.split(',')] if custom_lang else None
            clipboard_template(languages)
            action_executed = True

        elif choice == "3":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_generate_section(file_path)
                else:
                    run_insert_section(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "4":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_add_languages(file_path)
                else:
                    run_add_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "5":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_remove_languages(file_path)
                else:
                    run_remove_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "6":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_set_global_lang(file_path)
                else:
                    run_set_global_lang(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "7":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_repair(file_path)
                else:
                    run_repair_functions(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "8":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_translate(file_path)
                else:
                    run_translate(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "9":
            print_version_info()
            action_executed = True

        else:
            print("❌ Invalid option")
            action_executed = True

        if action_executed:
            if not post_action_navigation():
                return

        if choice == "0":
            print("👋 Bye!")
            return

        if choice == "1":
            mode = input("Use auto mode? (y/N): ").strip().lower()
            target_path = ask_target_path()

            if mode in ["y", "yes"]:
                auto_check_all(target_path=target_path)
                action_executed = True
            else:
                if os.path.isfile(target_path):
                    analyze_file(target_path)
                    action_executed = True
                elif os.path.isdir(target_path):
                    print(f"ℹ️ '{target_path}' is a folder. Running auto-check for that folder.")
                    auto_check_all(target_path=target_path)
                    action_executed = True
                else:
                    print(f"❌ Path not found: {target_path}")
                    action_executed = True

        elif choice == "2":
            custom_lang = input("Languages (comma separated, empty=all): ").strip()
            languages = [lang.strip() for lang in custom_lang.split(',')] if custom_lang else None
            clipboard_template(languages)
            action_executed = True

        elif choice == "3":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_generate_section(file_path)
                else:
                    run_insert_section(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "4":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_add_languages(file_path)
                else:
                    run_add_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "5":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_remove_languages(file_path)
                else:
                    run_remove_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "6":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_set_global_lang(file_path)
                else:
                    run_set_global_lang(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "7":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_repair(file_path)
                else:
                    run_repair_functions(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "8":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_translate(file_path)
                else:
                    run_translate(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "9":
            print("LangGuard v1.0.0")
            print("By Fatony Ahmad Fauzi")
            print("Email: fatonyahmadfauzi@gmail.com")
            action_executed = True

        else:
            print("❌ Invalid option")
            action_executed = True

        if action_executed:
            if not post_action_navigation():
                return

        if action_executed:
            if not post_action_navigation():
                return

        if not choice:
            continue

        if choice == "0":
            print("👋 Bye!")
            return

        if choice == "1":
            mode = input("Use auto mode? (y/N): ").strip().lower()
            target_path = ask_target_path()

            if mode in ["y", "yes"]:
                auto_check_all(target_path=target_path)
                action_executed = True
            else:
                if os.path.isfile(target_path):
                    analyze_file(target_path)
                    action_executed = True
                elif os.path.isdir(target_path):
                    print(f"ℹ️ '{target_path}' is a folder. Running auto-check for that folder.")
                    auto_check_all(target_path=target_path)
                    action_executed = True
                else:
                    print(f"❌ Path not found: {target_path}")
                    action_executed = True

        elif choice == "2":
            custom_lang = input("Languages (comma separated, empty=all): ").strip()
            languages = [lang.strip() for lang in custom_lang.split(',')] if custom_lang else None
            clipboard_template(languages)
            action_executed = True

        elif choice == "3":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_generate_section(file_path)
                else:
                    run_insert_section(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "4":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_add_languages(file_path)
                else:
                    run_add_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "5":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_remove_languages(file_path)
                else:
                    run_remove_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "6":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_set_global_lang(file_path)
                else:
                    run_set_global_lang(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "7":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_repair(file_path)
                else:
                    run_repair_functions(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "8":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_translate(file_path)
                else:
                    run_translate(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "9":
            print("LangGuard v1.0.0")
            print("By Fatony Ahmad Fauzi")
            print("Email: fatonyahmadfauzi@gmail.com")
            action_executed = True

        else:
            print("❌ Invalid option")

        if action_executed:
            if not post_action_navigation():
                return

def ask_file_path(label="target file"):
    file_path = input("Target folder/file path (empty=current folder): ").strip()
    if not file_path:
        return "."
    return file_path


def is_js_file(path):
    return str(path).lower().endswith('.js')


def run_interactive_menu():
    while True:
        action_executed = False
        clear_screen()
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

        flush_console_input()
        choice = input(f"\n{YELLOW}[+] Select option: {RESET}").strip()

        if not choice:
            continue

        if choice == "0":
            print("👋 Bye!")
            return

        if choice == "1":
            mode = input("Use auto mode? (y/N): ").strip().lower()
            target_path = ask_target_path()

            if mode in ["y", "yes"]:
                auto_check_all(target_path=target_path)
                action_executed = True
            else:
                if os.path.isfile(target_path):
                    analyze_file(target_path)
                    action_executed = True
                elif os.path.isdir(target_path):
                    print(f"ℹ️ '{target_path}' is a folder. Running auto-check for that folder.")
                    auto_check_all(target_path=target_path)
                    action_executed = True
                else:
                    print(f"❌ Path not found: {target_path}")
                    action_executed = True

        elif choice == "2":
            custom_lang = input("Languages (comma separated, empty=all): ").strip()
            languages = [lang.strip() for lang in custom_lang.split(',')] if custom_lang else None
            clipboard_template(languages)
            action_executed = True

        elif choice == "3":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_generate_section(file_path)
                else:
                    run_insert_section(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "4":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_add_languages(file_path)
                else:
                    run_add_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "5":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_remove_languages(file_path)
                else:
                    run_remove_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "6":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_set_global_lang(file_path)
                else:
                    run_set_global_lang(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "7":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_repair(file_path)
                else:
                    run_repair_functions(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "8":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_translate(file_path)
                else:
                    run_translate(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "9":
            print("LangGuard v1.0.0")
            print("By Fatony Ahmad Fauzi")
            print("Email: fatonyahmadfauzi@gmail.com")
            action_executed = True

        else:
            print("❌ Invalid option")

        if action_executed:
            wait_for_enter_once()


def run_interactive_menu():
    while True:
        action_executed = False
        clear_screen()
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

        flush_console_input()
        choice = input(f"\n{YELLOW}[+] Select option: {RESET}").strip()

        if not choice:
            continue

        if choice == "0":
            print("👋 Bye!")
            return

        if choice == "1":
            mode = input("Use auto mode? (y/N): ").strip().lower()
            target_path = ask_target_path()

            if mode in ["y", "yes"]:
                auto_check_all(target_path=target_path)
                action_executed = True
            else:
                if os.path.isfile(target_path):
                    analyze_file(target_path)
                    action_executed = True
                elif os.path.isdir(target_path):
                    print(f"ℹ️ '{target_path}' is a folder. Running auto-check for that folder.")
                    auto_check_all(target_path=target_path)
                    action_executed = True
                else:
                    print(f"❌ Path not found: {target_path}")
                    action_executed = True

        elif choice == "2":
            custom_lang = input("Languages (comma separated, empty=all): ").strip()
            languages = [lang.strip() for lang in custom_lang.split(',')] if custom_lang else None
            clipboard_template(languages)
            action_executed = True

        elif choice == "3":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_generate_section(file_path)
                else:
                    run_insert_section(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "4":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_add_languages(file_path)
                else:
                    run_add_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "5":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_remove_languages(file_path)
                else:
                    run_remove_languages(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "6":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_set_global_lang(file_path)
                else:
                    run_set_global_lang(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "7":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_repair(file_path)
                else:
                    run_repair_functions(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "8":
            file_path = ask_file_path()
            if os.path.isfile(file_path):
                if is_js_file(file_path):
                    run_js_translate(file_path)
                else:
                    run_translate(file_path)
            elif os.path.isdir(file_path):
                print(f"❌ This command needs a file path, not folder: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
            action_executed = True

        elif choice == "9":
            print("LangGuard v1.0.0")
            print("By Fatony Ahmad Fauzi")
            print("Email: fatonyahmadfauzi@gmail.com")
            action_executed = True

        else:
            print("❌ Invalid option")

        if action_executed:
            wait_for_enter_once()

        elif choice == "9":
            print("LangGuard v1.0.0")
            print("By Fatony Ahmad Fauzi")
            print("Email: fatonyahmadfauzi@gmail.com")

        else:
            print("❌ Invalid option")

        if pause_after_action:
            input("\nPress Enter to continue...")
            print("\n" * 2)

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
        print_version_info()

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
