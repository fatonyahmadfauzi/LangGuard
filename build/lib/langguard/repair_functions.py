#!/usr/bin/env python3
"""
LangGuard - Repair Functions Only (WITH AUTO-GENERATE OPTION - FIXED)
"""

import os
import sys
import re


def check_display_section_exists(content):
    """Cek apakah DISPLAY_LANGUAGES section ada dan valid"""
    return 'DISPLAY_LANGUAGES = {' in content


def repair_braces_structure(content):
    """Fix braces, commas, and structure only."""
    print("🔧 Running FINAL structural repair...")
    
    if not check_display_section_exists(content):
        print("❌ DISPLAY_LANGUAGES section not found. Cannot repair structure.")
        return content

    if 'DISPLAY_LANG =' not in content:
        print("❌ DISPLAY_LANG not found.")
        return content

    before, after = content.split('DISPLAY_LANG =', 1)
    start = before.find('DISPLAY_LANGUAGES = {')
    prefix = before[:start]
    block = before[start:]
    start_brace = block.find('{')
    end_brace = block.rfind('}')
    inner = block[start_brace + 1:end_brace]
    lines = inner.splitlines()

    fixed = []
    inside_lang = False
    brace_depth = 0
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        lang_match = re.match(r'"([a-z]{2})"\s*:?(\s*\{)?', stripped)
        if lang_match:
            if inside_lang and brace_depth > 0:
                fixed.append("    },")
                inside_lang = False
                brace_depth = 0
            lang = lang_match.group(1)
            if "{" not in stripped:
                line = f'    "{lang}": {{'
            fixed.append(line)
            inside_lang = True
            brace_depth = line.count("{") - line.count("}")
            continue
        if inside_lang:
            brace_depth += stripped.count("{") - stripped.count("}")
            fixed.append(line)
            if brace_depth <= 0:
                inside_lang = False
                if not stripped.endswith(","):
                    fixed[-1] = fixed[-1].rstrip(",") + ","
        else:
            fixed.append(line)
    if inside_lang and brace_depth > 0:
        fixed.append("    }")
    while fixed and fixed[-1].strip().endswith(","):
        fixed[-1] = fixed[-1].rstrip(",")
    new_inner = re.sub(r',\s*,', ',', "\n".join(fixed))
    new_inner = re.sub(r'\n\s*\n+', '\n', new_inner)
    rebuilt = f"DISPLAY_LANGUAGES = {{\n{new_inner}\n}}"
    new_content = prefix + rebuilt + "\n\nDISPLAY_LANG =" + after
    print("✅ Structural repair complete.")
    return new_content


def repair_braces_and_content(content):
    """
    💎 Ultra-Final Repair (Strict Safe Mode)
    """
    print("🔧 Running ULTRA-FINAL repair (strict safe mode)...")

    if not check_display_section_exists(content):
        print("❌ DISPLAY_LANGUAGES section not found. Cannot repair content.")
        return content

    # Ambil isi dictionary
    match = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{([\s\S]*?)\n\}', content)
    if not match:
        print("❌ DISPLAY_LANGUAGES content not found.")
        return content

    inner = match.group(1)
    lines = inner.splitlines()
    fixed = []
    open_quote = False
    last_lang = None

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            continue

        # Komentar
        if stripped.startswith("#"):
            fixed.append("    " + stripped)
            continue

        # Awal bahasa, contoh: "en": {
        lang_match = re.match(r'"([a-z]{2})"\s*:?\s*\{?', stripped)
        if lang_match:
            lang = lang_match.group(1)
            if fixed and not fixed[-1].strip().endswith(","):
                fixed[-1] = fixed[-1].rstrip(",") + ","
            fixed.append(f'    "{lang}": {{')
            last_lang = lang
            continue

        # Tutup bahasa
        if stripped in ["}", "},"]:
            fixed.append("    },")
            continue

        # Baris valid: "key": "value",
        kv = re.match(r'"([^"]+)"\s*:\s*"([^"]*)"?', stripped)
        if kv:
            key = kv.group(1).strip()
            val = kv.group(2).strip()
            if not stripped.endswith(","):
                fixed.append(f'        "{key}": "{val}",')
            else:
                fixed.append(f'        "{key}": "{val}",')
            continue

        # Baris rusak (hilang ':' atau tanda kutip)
        if '"' in stripped and ":" not in stripped:
            # contoh: "translating_readme"📘 Translating...
            parts = stripped.split('"')
            if len(parts) >= 3:
                key = parts[1]
                after = stripped.split('"', 2)[-1].strip().lstrip(":").lstrip()
                if not after.startswith('"'):
                    after = f'"{after}'
                if not after.endswith('"') and not after.endswith('",'):
                    after = after + '"'
                fixed.append(f'        "{key}": {after},')
                continue

        # Jika ada ":" tapi tanda kutip rusak
        if ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip().strip('"')
            val = val.strip()
            if not val.startswith('"'):
                val = f'"{val}'
            if not val.endswith('"') and not val.endswith('",'):
                val += '"'
            fixed.append(f'        "{key}": {val},')
            continue

        # Baris lain: simpan mentah dengan indentasi aman
        fixed.append("        " + stripped)

    # --- Cleanup commas and spacing ---
    new_inner = "\n".join(fixed)

    # Hilangkan koma ganda (,,)
    new_inner = re.sub(r',\s*,', ',', new_inner)

    # Perbaiki koma antar bahasa
    new_inner = re.sub(r'\}\s*\n\s*"([a-z]{2})"', r'},\n    "\1"', new_inner)

    # Hapus koma terakhir sebelum penutup blok bahasa (misalnya setelah "folder_deleted")
    new_inner = re.sub(r',\s*\n\s*    \}', '\n    }', new_inner)

    # Hapus koma terakhir sebelum penutup dictionary utama
    new_inner = re.sub(r',\s*\n\s*\}', '\n}', new_inner)

    # --- Tambahan: hilangkan koma terakhir di akhir dictionary utama ---
    new_inner = re.sub(r',\s*\n\}', '\n}', new_inner)
    new_inner = re.sub(r',\s*\Z', '', new_inner)  # jika masih ada koma paling akhir

    # Rebuild dictionary
    rebuilt = f"DISPLAY_LANGUAGES = {{\n{new_inner}\n}}"

    new_content = re.sub(
        r'DISPLAY_LANGUAGES\s*=\s*\{[\s\S]*?\n\}',
        rebuilt,
        content,
    )

    print("✅ Content repair complete — structure and values restored cleanly (no trailing commas anywhere).")
    return new_content


def repair_functions_force_generate(content):
    """
    🔧 Regenerate only the function block, preserving DISPLAY_LANGUAGES content.
    """
    print("🔧 Regenerating display language functions (preserve active language)...")

    # 1️⃣ Cek apakah DISPLAY_LANGUAGES ada
    if not check_display_section_exists(content):
        print("❌ DISPLAY_LANGUAGES section not found. Cannot generate functions.")
        return content

    # 2️⃣ Deteksi bahasa aktif dari kode sebelumnya
    active_lang = "en"
    lang_match = re.search(r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\']', content)
    if lang_match:
        active_lang = lang_match.group(1)
    print(f"🌍 Detected active language: {active_lang}")

    # 3️⃣ Hapus semua definisi lama tanpa mengganggu DISPLAY_LANGUAGES
    content = re.sub(
        r'(# 🌐 Display Language Control[\s\S]*?)(?=\Z|^#|\ndef\s|\n[A-Za-z_])',
        '',
        content,
        flags=re.MULTILINE
    )
    content = re.sub(
        r'DISPLAY_LANG\s*=\s*["\']([a-z]{2})["\'][\s\S]*?(?=\Z|^#|\ndef\s|\n[A-Za-z_])',
        '',
        content,
        flags=re.MULTILINE
    )
    content = re.sub(
        r'def\s+(set_display_language|t|get_display_language|get_available_languages)\s*\([\s\S]*?(?=\Z|^#|\ndef\s|\n[A-Za-z_])',
        '',
        content,
        flags=re.MULTILINE
    )

    # 4️⃣ Template fungsi baru, pakai bahasa aktif yang terdeteksi
    functions_template = f'''# 🌐 Display Language Control
DISPLAY_LANG = "{active_lang}"

def set_display_language(lang_code):
    """Set display language for notifications"""
    global DISPLAY_LANG
    if lang_code in DISPLAY_LANGUAGES:
        DISPLAY_LANG = lang_code
    else:
        print(f"❌ Language '{{lang_code}}' not supported. Using English.")

def t(key, **kwargs):
    """Translation function for notifications"""
    global DISPLAY_LANG
    try:
        if DISPLAY_LANG in DISPLAY_LANGUAGES and key in DISPLAY_LANGUAGES[DISPLAY_LANG]:
            return DISPLAY_LANGUAGES[DISPLAY_LANG][key].format(**kwargs)
        else:
            # Jika tidak ditemukan, tetap kembalikan key tanpa fallback ke English
            return key
    except Exception:
        return key

def get_display_language():
    """Get current display language"""
    return DISPLAY_LANG

def get_available_languages():
    """Get list of available languages"""
    return list(DISPLAY_LANGUAGES.keys())'''

    # 5️⃣ Temukan posisi akhir dari dictionary DISPLAY_LANGUAGES
    match = re.search(r'DISPLAY_LANGUAGES\s*=\s*\{[\s\S]*?\n\}', content)
    if not match:
        print("❌ DISPLAY_LANGUAGES block not found.")
        return content

    insert_pos = match.end()

    # 6️⃣ Sisipkan fungsi baru setelah block dictionary
    new_content = content[:insert_pos] + "\n\n" + functions_template + "\n" + content[insert_pos:]

    # 7️⃣ Bersihkan newline berlebih
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    print(f"✅ Function block regenerated successfully (kept '{active_lang}' as active language).")
    return new_content

def run_insert_section_dynamic(target_file):
    """Jalankan insert_section secara langsung tanpa import dinamis kompleks"""
    try:
        # Tambahkan current directory ke sys.path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import langsung
        try:
            from insert_section import run_insert_section
            run_insert_section(target_file)
            return True
        except ImportError:
            # Coba relative import
            from .insert_section import run_insert_section
            run_insert_section(target_file)
            return True
            
    except Exception as e:
        print(f"❌ Error running insert_section: {e}")
        import traceback
        traceback.print_exc()
        return False
    
def ask_generate_section(target_file):
    """Tanya user apakah ingin generate section DISPLAY_LANGUAGES"""
    print(f"\n❌ File '{target_file}' doesn't have DISPLAY_LANGUAGES section!")
    
    while True:
        choice = input("\n👉 Do you want to generate a complete DISPLAY_LANGUAGES section now? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🎯 Generating DISPLAY_LANGUAGES section...")
            
            # Gunakan import dinamis untuk hindari circular import
            success = run_insert_section_dynamic(target_file)
            
            if success:
                print("✅ DISPLAY_LANGUAGES section generated successfully!")
                return True
            else:
                print("❌ Failed to generate DISPLAY_LANGUAGES section")
                return False
                
        elif choice in ['n', 'no', '']:
            print("ℹ️ Operation cancelled. No changes made.")
            return False
        else:
            print("❌ Please enter 'y' for Yes or 'n' for No")


def run_repair_functions(target_file):
    """Run repair process - dengan opsi auto-generate jika section tidak ada"""
    if not os.path.exists(target_file):
        print(f"❌ File {target_file} not found.")
        return

    print(f"🎯 Repairing: {target_file}")
    with open(target_file, 'r', encoding='utf-8') as f:
        original = f.read()

    backup = target_file + ".backup"
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(original)
    print(f"📁 Backup created: {backup}")

    # Cek apakah file memiliki DISPLAY_LANGUAGES section
    if not check_display_section_exists(original):
        # Tanya user apakah ingin generate section
        if ask_generate_section(target_file):
            # Jika user memilih yes, baca file yang sudah di-update
            with open(target_file, 'r', encoding='utf-8') as f:
                original = f.read()
            
            # Cek lagi setelah generate
            if not check_display_section_exists(original):
                print("❌ Still no DISPLAY_LANGUAGES section after generation. Repair cancelled.")
                return
            
            # ✅ PERBAIKAN: Jika section berhasil digenerate, TIDAK PERLU repair lagi
            print("✅ Section successfully generated. No additional repair needed.")
            return
        else:
            return  # User memilih no

    # ✅ HANYA JALANKAN REPAIR JIKA SECTION SUDAH ADA
    print("🔧 Running FULL REPAIR (braces + content + functions)...")
    
    content = original
    try:
        # Jalankan semua repair secara berurutan
        content = repair_braces_structure(content)
        content = repair_braces_and_content(content)
        content = repair_functions_force_generate(content)

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Full repair completed successfully!")
        print(f"💾 Backup saved: {backup}")

    except Exception as e:
        print(f"❌ Error: {e}")
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(original)
        print("🔄 Restored from backup due to error.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_repair_functions(sys.argv[1])
    else:
        print("❌ Please provide a target file.")
        print("Usage: python repair_functions.py <filename>")