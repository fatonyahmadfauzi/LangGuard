"""
LangGuard - Multilingual Dictionary Guardian
Author: Fatony Ahmad Fauzi
Email: fatonyahmadfauzi@gmail.com"
"""

from .main import main
# PERBAIKAN: Hapus atau komentar import yang bermasalah
# from .fallback_strategy import fallback_strategy, smart_translate, get_fallback_strategy, FallbackStrategy
from .fallback_strategy import (
    run_section_fallback, 
    fallback_for_check,
    fallback_for_add_lang, 
    fallback_for_translate,
    fallback_for_repair,
    fallback_for_set_global_lang,
    fallback_for_fix_order,
    fallback_for_remove_lang
)
from .analysis import analyze_file, auto_check_all, list_files, is_valid_display_languages_section
from .clipboard import clipboard_template, create_section, create_template_internal
from .translate import run_translate, show_translation_progress
from .fix_order import fix_language_order
from .insert_section import run_insert_section
from .remove_languages import run_remove_languages
from .repair_functions import run_repair_functions
from .update_language import set_default_display_language_in_file, choose_language
from .add_languages import (
    show_all_language_options, 
    get_language_selection, 
    add_languages_to_content,
    get_all_supported_languages,
    show_missing_language_options,      
    get_missing_language_selection,     
    get_missing_languages_from_content,
    get_correct_language_order,
    get_existing_languages_from_content
)
from .language_utils import (
    get_all_supported_languages,
    get_correct_language_order,
    get_existing_languages_from_content,
    extract_english_phrases
)

__version__ = "1.0.0"
__author__ = "Fatony Ahmad Fauzi"
__email__ = "fatonyahmadfauzi@gmail.com"

__all__ = [
    'main',
    # PERBAIKAN: Update nama fungsi fallback
    'run_section_fallback',
    'fallback_for_check',
    'fallback_for_add_lang', 
    'fallback_for_translate',
    'fallback_for_repair',
    'fallback_for_set_global_lang',
    'fallback_for_fix_order',
    'fallback_for_remove_lang',
    'analyze_file',
    'auto_check_all', 
    'is_valid_display_languages_section',
    'clipboard_template',
    'run_translate',
    'extract_english_phrases', 
    'show_translation_progress',
    'create_section',
    'create_template_internal',
    'fix_language_order',
    'run_insert_section',
    'run_remove_languages',
    'run_repair_functions',
    'set_default_display_language_in_file',
    'choose_language',
    'show_all_language_options',
    'get_language_selection',
    'add_languages_to_content',
    'get_all_supported_languages',
    'show_missing_language_options',      
    'get_missing_language_selection',     
    'get_missing_languages_from_content',
    'get_correct_language_order',
    'get_existing_languages_from_content'
]