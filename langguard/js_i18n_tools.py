#!/usr/bin/env python3
"""
LangGuard - JavaScript I18N Tools
Feature parity helpers for JS files using LANG_ORDER + I18N + currentLang.
"""

import os
import re
import urllib.request

try:
    from .language_utils import get_all_supported_languages
except ImportError:
    from language_utils import get_all_supported_languages


def _find_matching_brace(text, open_idx):
    brace = 0
    in_string = False
    quote = ''
    escape = False
    for i in range(open_idx, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if in_string:
            if ch == '\\':
                escape = True
            elif ch == quote:
                in_string = False
                quote = ''
            continue
        if ch in ('"', "'"):
            in_string = True
            quote = ch
            continue
        if ch == '{':
            brace += 1
        elif ch == '}':
            brace -= 1
            if brace == 0:
                return i
    return -1


def _split_top_level_props(block):
    props = []
    cur = []
    obj_d = arr_d = par_d = 0
    in_string = False
    quote = ''
    esc = False

    for ch in block:
        if esc:
            cur.append(ch)
            esc = False
            continue
        if in_string:
            cur.append(ch)
            if ch == '\\':
                esc = True
            elif ch == quote:
                in_string = False
                quote = ''
            continue
        if ch in ('"', "'"):
            in_string = True
            quote = ch
            cur.append(ch)
            continue
        if ch == '{':
            obj_d += 1
        elif ch == '}':
            obj_d = max(0, obj_d - 1)
        elif ch == '[':
            arr_d += 1
        elif ch == ']':
            arr_d = max(0, arr_d - 1)
        elif ch == '(':
            par_d += 1
        elif ch == ')':
            par_d = max(0, par_d - 1)

        if ch == ',' and obj_d == 0 and arr_d == 0 and par_d == 0:
            p = ''.join(cur).strip()
            if p:
                props.append(p)
            cur = []
            continue
        cur.append(ch)

    tail = ''.join(cur).strip()
    if tail:
        props.append(tail)
    return props


def parse_js_i18n(content):
    m = re.search(r'const\s+I18N\s*=\s*\{', content)
    if not m:
        return None
    start = m.end() - 1
    end = _find_matching_brace(content, start)
    if end == -1:
        return None

    i18n_block = content[start + 1:end]
    langs = {}
    idx = 0
    while idx < len(i18n_block):
        lm = re.search(r'\b([a-z]{2})\s*:\s*\{', i18n_block[idx:])
        if not lm:
            break
        lang = lm.group(1)
        lang_open = idx + lm.end() - 1
        lang_close = _find_matching_brace(i18n_block, lang_open)
        if lang_close == -1:
            break
        lang_body = i18n_block[lang_open + 1:lang_close]

        kv = {}
        for prop in _split_top_level_props(lang_body):
            pm = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+?)\s*$', prop)
            if not pm:
                continue
            key = pm.group(1)
            value = pm.group(2).strip()
            sm = re.match(r'^["\']([\s\S]*)["\']$', value)
            if sm:
                value = sm.group(1)
            kv[key] = value

        langs[lang] = kv
        idx = lang_close + 1

    return {
        'i18n_start': m.start(),
        'i18n_open': start,
        'i18n_close': end,
        'languages': langs,
    }


def _render_i18n(languages):
    order = get_all_supported_languages()
    langs = [l for l in order if l in languages]
    lines = ['const I18N = {']
    for li, lang in enumerate(langs):
        lines.append(f'  {lang}: {{')
        keys = list(languages[lang].keys())
        for ki, key in enumerate(keys):
            val = str(languages[lang][key]).replace('"', '\\"')
            comma = ',' if ki < len(keys)-1 else ''
            lines.append(f'    {key}: "{val}"{comma}')
        comma_lang = ',' if li < len(langs)-1 else ''
        lines.append(f'  }}{comma_lang}')
    lines.append('};')
    return '\n'.join(lines)


def _replace_i18n(content, parsed, languages):
    new_block = _render_i18n(languages)
    return content[:parsed['i18n_start']] + new_block + content[parsed['i18n_close'] + 1:]


def _set_lang_order(content, langs):
    arr = ', '.join([f'"{l}"' for l in langs])
    new_line = f'const LANG_ORDER = [{arr}];'
    if re.search(r'const\s+LANG_ORDER\s*=\s*\[[^\]]*\];', content):
        return re.sub(r'const\s+LANG_ORDER\s*=\s*\[[^\]]*\];', new_line, content, count=1)
    return new_line + '\n' + content


def _set_current_lang(content, lang):
    if re.search(r'\b(let|const|var)\s+currentLang\s*=\s*["\'][a-z]{2}["\']\s*;', content):
        return re.sub(r'\b(let|const|var)\s+currentLang\s*=\s*["\'][a-z]{2}["\']\s*;', f'let currentLang = "{lang}";', content, count=1)
    return content + f'\n\nlet currentLang = "{lang}";\n'


def run_js_generate_section(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'const I18N' in content:
        print('ℹ️ JS I18N already exists. Use repair/add-lang instead.')
        return True

    langs = get_all_supported_languages()
    template = {l: {} for l in langs}
    template['en'] = {'hello': 'Hello'}
    content = _set_lang_order(content, langs)
    content += '\n\n' + _render_i18n(template) + '\n'
    content = _set_current_lang(content, 'en')

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ Generated JS LANG_ORDER + I18N section')
    return True


def run_js_add_languages(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    parsed = parse_js_i18n(content)
    if not parsed:
        print('❌ JS I18N not found. Run generate first.')
        return False

    languages = parsed['languages']
    supported = get_all_supported_languages()
    missing = [l for l in supported if l not in languages]
    if not missing:
        print('✅ No missing languages')
        return True

    print(f"💡 Missing languages: {', '.join(missing)}")
    choice = input("Add all missing languages? (Y/n): ").strip().lower()
    if choice in ('n', 'no'):
        return False

    en_keys = languages.get('en', {})
    for lang in missing:
        languages[lang] = {k: '' for k in en_keys.keys()}

    content = _replace_i18n(content, parsed, languages)
    content = _set_lang_order(content, supported)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Added {len(missing)} languages")
    return True


def run_js_remove_languages(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    parsed = parse_js_i18n(content)
    if not parsed:
        print('❌ JS I18N not found')
        return False

    languages = parsed['languages']
    existing = [l for l in get_all_supported_languages() if l in languages]
    print(f"📊 Existing: {', '.join(existing)}")
    choice = input("Enter language codes to remove (comma), except en: ").strip().lower()
    if not choice:
        return False
    to_remove = [x.strip() for x in choice.split(',') if x.strip() and x.strip() != 'en']
    for l in to_remove:
        languages.pop(l, None)

    content = _replace_i18n(content, parsed, languages)
    content = _set_lang_order(content, get_all_supported_languages())
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Removed: {', '.join(to_remove)}")
    return True


def run_js_set_global_lang(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    parsed = parse_js_i18n(content)
    if not parsed:
        print('❌ JS I18N not found')
        return False
    languages = parsed['languages']
    existing = [l for l in get_all_supported_languages() if l in languages]
    print(f"📋 Available languages: {', '.join(existing)}")
    lang = input('Set default language code: ').strip().lower()
    if lang not in existing:
        print('❌ Invalid language')
        return False
    content = _set_current_lang(content, lang)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Default language set to {lang}")
    return True


def run_js_repair(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    parsed = parse_js_i18n(content)
    if not parsed:
        print('❌ JS I18N not found. Try generate first.')
        return False

    languages = parsed['languages']
    if 'en' not in languages:
        print('⚠️ EN missing. Creating EN from union keys of all languages.')
        union_keys = []
        for l, kv in languages.items():
            for k in kv.keys():
                if k not in union_keys:
                    union_keys.append(k)
        languages['en'] = {k: k for k in union_keys}

    en_keys = list(languages['en'].keys())
    if not en_keys:
        print('⚠️ EN has no phrases.')
        if input('Generate EN phrases from key names? (Y/n): ').strip().lower() not in ('n', 'no'):
            union_keys = []
            for l, kv in languages.items():
                for k in kv.keys():
                    if k not in union_keys:
                        union_keys.append(k)
            languages['en'] = {k: k for k in union_keys}
            en_keys = union_keys

    # remove unsupported language keys & normalize known languages order only
    normalized = {}
    for lang in get_all_supported_languages():
        if lang in languages:
            normalized[lang] = dict(languages[lang])

    languages = normalized
    content = _replace_i18n(content, parsed, languages)
    content = _set_lang_order(content, get_all_supported_languages())
    if 'currentLang' not in content:
        content = _set_current_lang(content, 'en')

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ JS repair completed')
    return True


def run_js_translate(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    parsed = parse_js_i18n(content)
    if not parsed:
        print('❌ JS I18N not found')
        return False
    languages = parsed['languages']

    if 'en' not in languages or not languages['en']:
        print('⚠️ EN missing or empty. Create EN first with repair.')
        if input('Run JS repair now? (Y/n): ').strip().lower() not in ('n', 'no'):
            if not run_js_repair(target_file):
                return False
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            parsed = parse_js_i18n(content)
            languages = parsed['languages']
        else:
            return False

    en = languages['en']

    def has_internet():
        try:
            urllib.request.urlopen('https://www.google.com', timeout=5)
            return True
        except Exception:
            return False

    try:
        from deep_translator import GoogleTranslator
    except Exception:
        GoogleTranslator = None

    # Safe default: always fill missing keys with EN text first.
    # Optional machine translation only when user confirms and internet is available.
    use_machine_translation = False
    if GoogleTranslator is not None:
        mt_choice = input('Use online machine translation for missing JS phrases? (y/N): ').strip().lower()
        if mt_choice in ('y', 'yes'):
            if has_internet():
                use_machine_translation = True
            else:
                print('⚠️ No internet detected. Falling back to EN text copy.')

    for lang in list(languages.keys()):
        if lang == 'en':
            continue
        lang_map = languages[lang]
        for k, v in en.items():
            if k not in lang_map or not str(lang_map[k]).strip():
                if use_machine_translation:
                    target_map = {'jp': 'ja', 'kr': 'ko', 'zh': 'zh-CN'}.get(lang, lang)
                    try:
                        translated = GoogleTranslator(source='auto', target=target_map).translate(str(v))
                        if is_suspicious_translation(translated):
                            lang_map[k] = str(v)
                        else:
                            lang_map[k] = translated
                    except KeyboardInterrupt:
                        print('\n⚠️ Translation interrupted. Filling remaining keys with EN fallback...')
                        use_machine_translation = False
                        lang_map[k] = str(v)
                    except Exception:
                        # Never fail hard: fallback to EN text
                        lang_map[k] = str(v)
                else:
                    # Offline-safe fallback
                    lang_map[k] = str(v)

    content = _replace_i18n(content, parsed, languages)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ JS translate completed (missing keys filled)')
    return True


def run_js_autofix(target_file):
    """Auto-fix for JS: repair -> add missing languages -> translate missing keys."""
    if not run_js_repair(target_file):
        return False
    run_js_add_languages(target_file)
    try:
        run_js_translate(target_file)
    except KeyboardInterrupt:
        print('\n⚠️ JS auto-fix interrupted during translate step. Existing repairs were kept.')
        return False
    return True
    def is_suspicious_translation(text):
        low = str(text).lower()
        patterns = [
            r'error\s*500',
            r"that.?s an error",
            r'<html',
            r'</html>',
            r'please try again later',
        ]
        return any(re.search(p, low) for p in patterns)
