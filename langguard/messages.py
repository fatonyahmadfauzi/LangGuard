#!/usr/bin/env python3
"""
LangGuard - Centralized Message System
"""

# ==================== UPDATE LANGUAGE MESSAGES ====================

def get_update_language_messages():
    """Messages for update_language.py module"""
    return {
        # Function repair messages
        "functions_missing": "⚠️  Required functions are missing or incomplete!",
        "functions_required": "💡 The following functions are required for set-global-lang to work:",
        "function_display_lang": "   - DISPLAY_LANG =",
        "function_set_display": "   - def set_display_language()",
        "function_t": "   - def t()", 
        "function_get_display": "   - def get_display_language()",
        "function_get_available": "   - def get_available_languages()",
        
        "repair_functions_prompt": "👉 Do you want to repair the functions automatically? (y/N): ",
        "repairing_functions": "🎯 Repairing functions...",
        "functions_repaired_success": "✅ Functions repaired successfully!",
        "functions_repair_failed": "❌ Failed to repair functions",
        "functions_repair_skipped": "ℹ️ Repair skipped. set-global-lang cannot proceed without functions.",
        "functions_complete_after_repair": "✅ Functions are now complete after repair!",
        
        # Language selection messages
        "language_not_found": "❌ Language '{lang_code}' not found in DISPLAY_LANGUAGES",
        "language_already_default": "ℹ️ Language '{lang_code}' is already the current default. No changes needed.",
        "display_lang_changed": "✅ DISPLAY_LANG changed to '{lang_code}'",
        "fallback_changed": "✅ Fallback language changed from '{current}' to '{new}'",
        "fallback_updated": "✅ Fallback language set to '{lang_code}'",
        "specific_fallback_changed": "✅ Specific fallback changed: '{current}' → '{new}'",
        "no_changes_made_display_lang": "❌ No changes were made. DISPLAY_LANG assignment not found.",
        "default_language_changed": "✅ Default display language changed to '{lang_code}' in {file_path}",
        
        # Status messages
        "current_display_language": "🔍 Current display language: {lang_code}",
        "current_fallback_language": "🔍 Current fallback language: {lang_code}",
        "all_languages_available": "🎉 All supported languages are available!",
        "available_languages_count": "📋 Available languages in file: {languages}",
        "no_languages_available": "❌ No languages available in DISPLAY_LANGUAGES section. Operation cancelled.",
        "operation_completed_no_changes": "ℹ️ Operation completed with no changes.",
        "adding_new_languages": "🎯 Adding new languages...",
        "set_global_language_prompt": "🔄 Now let's set the global language...",
        "global_language_skipped": "⏭️ Global language setting skipped.",
        "add_languages_failed": "❌ Failed to add languages.",
        
        # Process messages
        "functions_ready": "💡 The display language functions have been repaired and are now ready to use.",
        "change_language_hint": "📋 If you want to change the display language, run this command again.",
        
        # Warning messages
        "current_language_not_available": "⚠️ Current display language '{lang_code}' not in available languages",
        "current_fallback_not_available": "⚠️ Current fallback language '{lang_code}' not in available languages",
        
        # Missing functions
        "missing_functions_list": "❌ Missing required functions: {functions}",
        
        # Import errors
        "cannot_import_repair": "❌ Cannot import repair_functions module",
        "cannot_import_add_languages": "❌ Cannot import add_languages module",
    }

# ==================== ANALYSIS MESSAGES ====================

def get_analysis_messages():
    """Messages for analysis.py module"""
    return {
        # Status messages
        "analyzing_file": "🔍 Analyzing: {file_path}",
        "continuing_analysis": "🔄 Continuing with detailed analysis process...",
        "skipping_utility": "ℹ️  Skipping utility/template file: {file_path}",
        "skipping_template": "ℹ️  Skipping template file (no actual implementation): {file_path}",
        
        # Language analysis
        "languages_found": "✅ Found {count} languages: {languages}",
        "languages_missing": "❌ MISSING {count} languages: {languages}",
        "missing_languages_found": "⚠️  Found {count} missing languages: {languages}",
        "order_correct": "✅ Language order is correct!",
        "order_correct_detailed": "✅ ORDER: Correct for existing languages",
        "order_incorrect": "⚠️  Language order is incorrect!",
        "order_incorrect_detailed": "❌ ORDER: Incorrect",
        "current_order": "📋 Current order: {order}",
        "expected_order": "🎯 Expected complete order: {order}",
        
        # Translation
        "languages_need_translation": "⚠️  Found {count} languages that need translation:",
        "empty_languages": "   - {count} empty languages: {languages}",
        "empty_languages_detailed": "⚠️  {count} languages have empty phrases: {languages}",
        "empty_languages_summary": "🔴 Empty languages ({count}): {languages}",
        "incomplete_languages": "   - {count} incomplete languages:",
        "incomplete_languages_detailed": "⚠️  {count} languages have incomplete phrases:",
        "incomplete_languages_summary": "🟡 Incomplete languages ({count}):",
        "language_stats": "     - {lang}: {current} phrases (expected: {expected})",
        "language_missing_count": "   - {lang}: {current}/{expected} phrases (missing {missing})",
        "language_missing_details": "   - {lang}: {current}/{expected} phrases (missing {missing})",
        "total_phrases_to_translate": "📝 Total phrases to translate: {count}",
        "translation_skipped": "ℹ️ Translation skipped.",
        "translation_new_skipped": "ℹ️ Translation for new languages skipped.",
        "no_languages_need_translation": "✅ No languages need translation",
        
        # Language addition
        "language_addition_skipped": "ℹ️ Language addition skipped.",
        
        # Auto-fix
        "issues_summary": "📊 ISSUES SUMMARY:",
        "files_missing_langs": "❌ {count} files missing languages:",
        "files_empty_phrases": "⚠️  {count} files with empty phrases:",
        "auto_fix_start": "🎯 AUTO-FIX: Adding missing languages + Translating...",
        "adding_languages": "📥 Adding missing languages to all files...",
        "translating_files": "🌍 Translating all files...",
        "auto_fix_completed": "🎯 AUTO-FIX COMPLETED:",
        "languages_added": "   ✅ Languages added: {success}/{total} files",
        "files_translated": "   ✅ Files translated: {success}/{total} files",
        "files_skipped": "   ⚠️  Files skipped (no English phrases): {count}",
        "auto_fix_skipped": "ℹ️ Auto-fix skipped. No changes were made.",
        
        # File operations
        "translating_file": "   🔄 {filename}: Translating...",
        "translated_success": "      ✅ Translated successfully",
        "translated_failed": "      ❌ Failed to translate",
        "cannot_translate_no_english": "      ⚠️  Cannot translate - English missing (file has: {languages})",
        "cannot_translate_no_langs": "      ⚠️  Cannot translate - No languages found",
        "cannot_translate_error": "      ⚠️  Cannot translate - Error reading file",
        
        # CLI & General messages
        "searching_files": "🔍 Searching for files with DISPLAY_LANGUAGES...",
        "searching_subfolders": "📁 Searching in current folder and all subfolders...",
        "searching_current_only": "📁 Searching in current folder only...",
        "files_summary": "📊 Summary: Found {total_files} files with DISPLAY_LANGUAGES",
        "complete_summary": "🎯 Complete: {complete_files}/{total_files} files have all {lang_count} languages with phrases",
        "search_scope_subfolders": "🌐 Search scope: Current folder + all subfolders",
        "search_scope_current": "📁 Search scope: Current folder only",
        "no_files_found": "❌ No files with DISPLAY_LANGUAGES found",
        "auto_check_start": "🔍 Auto-checking all files...",
        "files_to_analyze": "📊 Found {count} files to analyze:",
        "file_complete": "✅ {filename}: COMPLETE ({current}/{total} languages with phrases)",
        "file_complete_status": "✅ {filename}: COMPLETE ({current}/{total} languages with phrases)",
        "file_incomplete": "⚠️  {filename}: INCOMPLETE ({current}/{total} languages)",
        "file_incomplete_status": "⚠️  {filename}: INCOMPLETE ({current}/{total} languages)",
        "file_missing_langs": "   Missing: {languages}",
        "file_empty_phrases": "   Empty: {languages}",
        "final_summary": "🎯 FINAL SUMMARY: {complete}/{total} files have complete language sets with phrases",
        
        # Quick check messages
        "quick_checking": "🔍 Quick checking: {file_path}",
        "new_languages_empty": "⚠️  Newly added languages have empty phrases: {languages}",
        
        # Analysis details
        "analysis_header": "📊 Language Analysis for: {file_path}\n{separator}",
        "total_languages_found": "✅ Total languages found: {count}",
        "languages_present": "🌍 Languages present: {languages}",
        "missing_languages": "❌ MISSING languages: {languages}",
        "expected_languages": "💡 Expected {expected} languages, but only {current} found",
        "run_translate_suggestion": "💡 Run 'langguard translate {file_path}' to fix {count} languages",
        "all_languages_complete": "🎉 All {count} supported languages are present and have complete phrases!",
        "detailed_analysis": "📝 Detailed Analysis:",
        "language_status": "   {status} {lang}: {count} phrases",
        "consistency_perfect": "🎉 CONSISTENCY: Perfect! All languages have {count} phrases",
        "consistency_inconsistent": "⚠️  CONSISTENCY: Inconsistent phrase counts!",
        "language_expected": "   {lang}: {current} phrases{expected_info}",
        "total_unique_phrases": "📚 Total unique phrases: {count}",
        "unique_phrases_found": "🔍 Unique phrases found: {phrases}",
        "missing_functions": "❌ MISSING FUNCTIONS: {functions}",
        "functions_present": "✅ FUNCTIONS: All required functions present",
        "no_issues_found": "🎉 No issues found - file is in perfect condition!",
        "analysis_completed": "ℹ️ Analysis completed. No changes were made.",
        
        # File operations detailed
        "adding_languages_to_file": "   ➕ {filename}: Adding {count} languages ({languages})",
        "languages_added_success_analysis": "      ✅ Added {count} languages successfully",
        "error_adding_languages": "      ❌ Error adding languages: {error}",
        "error_checking_phrases": "❌ Error checking English phrases in {file_path}: {error}",

        # Pesan fleksibel untuk konteks spesifik
        "file_found_status": "{status} Found: {path} ({current}/{total} languages)",
        "encoding_error": "⚠️  Encoding error in: {path}",
        "error_reading_file": "⚠️  Error reading {path}: {error}",
        "permission_denied": "⛔ Permission denied: {directory}",
        "error_scanning": "⚠️  Error scanning {directory}: {error}",
        
        # Pesan untuk auto-check
        "file_missing_display": "   Missing: {languages}",
        "file_empty_display": "   Empty: {languages}",
        
        # Pesan untuk analysis detail
        "critical_english_empty": "❌ CRITICAL: English section is empty!",
        "critical_english_empty_detailed": "❌ CRITICAL: English section is empty!",
        "english_required": "   💡 English phrases are required as reference for translation",
        "english_reference_required": "   💡 English phrases are required as reference for translation",
        "manual_action_required": "   🔧 Action: Manually add English phrases to enable translation",
        "action_add_english": "   🔧 Action: Manually add English phrases to enable translation",
        
        # User input prompts
        "translate_now_prompt": "\n👉 Do you want to auto-translate now? (y/N): ",
        "add_languages_prompt": "👉 Do you want to add the missing languages now? (y/N): ",
        "translate_new_prompt": "👉 Do you want to auto-translate the new languages now? (y/N): ",
        "translate_new_languages_prompt": "\n👉 Do you want to auto-translate {count} languages now? (y/N): ",
        "fix_all_issues_prompt": "\n👉 Fix all issues automatically? (y/N): ",
        
        # Display messages
        "phrases_list_display": "      Phrases: {phrases}",
        "file_missing_langs_display": "   - {filename}: {languages}",
        "file_empty_phrases_display": "   - {filename}: {languages}",
        "sample_phrases_display": "🔤 Sample phrases: {phrases}{ellipsis}",
        
        # File status in lists
        "file_status_has_languages": "      - {filename}: English missing (has: {languages})",
        "file_status_no_languages": "      - {filename}: No languages found",
        "file_status_error": "      - {filename}: Error reading file",
        
        # Error reporting
        "analysis_error": "❌ Error during analysis: {error}",
    }

# ==================== ADD LANGUAGES MESSAGES ====================

def get_add_languages_messages():
    """Messages for add_languages.py module"""
    return {
        # Add Languages specific messages
        "file_no_display_section": "❌ File '{file_path}' doesn't have DISPLAY_LANGUAGES section!",
        "generate_section_prompt": "\n👉 Do you want to generate a complete DISPLAY_LANGUAGES section now? (y/N): ",
        "generating_section": "\n🎯 Generating DISPLAY_LANGUAGES section...",
        "section_generated_success": "✅ DISPLAY_LANGUAGES section generated successfully!",
        "section_generation_failed": "❌ Failed to generate DISPLAY_LANGUAGES section",

        "adding_languages_count": "\n🔄 Adding {count} languages: {languages}",
        "all_languages_exist": "ℹ️ All selected languages already exist.",
        "adding_new_languages": "🎯 Adding new languages: {languages}",
        "languages_added_success": "✅ Added {count} languages successfully!",
        "final_language_order": "🔄 Final language order: {languages}",

        "add_languages_target": "🎯 Target: {file_path}",
        "section_still_not_found": "❌ Still no DISPLAY_LANGUAGES section after generation. Operation cancelled.",
        "section_created_success": "\n✅ DISPLAY_LANGUAGES section created successfully!",
        "current_languages_display": "📊 Current languages: {languages}",
        "add_missing_now_prompt": "\n👉 Do you want to add missing languages now? (y/N): ",
        "operation_completed_add_later": "ℹ️ Operation completed. You can add missing languages later with 'langguard add-lang'",

        "all_languages_exist_complete": "🎉 All supported languages already exist!",
        "languages_added_list": "📊 Languages added: {languages}",
        "new_languages_added": "\n🔄 {count} new languages added successfully: {languages}",

        "insert_section_error": "❌ Error running insert_section: {error}",

        # Language status messages
        "language_empty_phrases": "⚠️  {lang}: 0 phrases (empty)",
        "language_incomplete_phrases": "⚠️  {lang}: {current}/{expected} phrases (incomplete)",
        "language_complete_phrases": "✅ {lang}: {count} phrases (complete)",
        "language_section_not_found": "❌ {lang}: Language section not found",
        "all_new_languages_complete": "✅ All {count} new languages have complete phrases content.",
        "complete_languages_summary": "🟢 Complete languages ({count}): {languages}",
    }

# ==================== TRANSLATION MESSAGES ====================

def get_translation_messages():
    """Messages for translate.py module"""
    return {
        "translation_progress": "🔄 Translating {count} phrases to {lang_name}...",
        "translating_phrase": "   📝 [{current}/{total}] Translating: {key}",
        "translation_error_detail": "❌ Translation error for '{text}': {error}",
        "language_section_not_found_detail": "❌ {lang_code} section not found!",
        "language_section_end_not_found": "❌ Could not find end of {lang_code} section",
        "language_already_complete": "✅ {lang_code} already complete!",
        "phrases_translated_count": "✅ Translated {count} phrases to {lang_code}",
        "no_english_phrases_found": "❌ No English phrases found to translate",
        "translating_to_language": "🎯 Translating to {lang_name}...",
        
        # Progress display
        "translation_progress_header": "\n📊 TRANSLATION PROGRESS ({total_phrases} phrases):",
        "language_complete_percentage": "✅ {lang_code}: {current}/{total} (100%)",
        "language_progress_percentage": "{status} {lang_code}: {current}/{total} ({percentage}%)",
        "language_no_phrases": "🔴 {lang_code}: 0/{total} (0%)",
        
        # User prompts
        "proceed_translation_prompt": "\n👉 Proceed with auto-translation? (y/N): ",
        "starting_translation_process": "\n🎯 Starting auto-translation...",
        "add_more_languages_prompt": "\n👉 Do you want to add more languages before translating? (y/N): ",
        
        # Language status
        "all_languages_complete_translation": "🎉 All languages already have complete translations!",
        "languages_need_translation_count": "🔍 {count} languages need translation: {languages}",
        
        # Translation summary
        "translation_summary_header": "\n📊 Translation Summary for New Languages:",
        "language_translation_status": "🌍 {lang_name} ({lang_code}): {count} phrases to translate",
        "sample_phrases": "   Sample: {phrases}{ellipsis}",
        
        # Phrases count
        "total_phrases_to_translate_simple": "📝 Total phrases to translate: {count}",
        
        # Language addition in translate
        "all_supported_exist": "\n🎉 All supported languages already exist!",
        "new_languages_detected_translate": "🎯 Newly added languages detected: {languages}",
        "auto_translating_new": "🔄 Automatically translating new languages...",
        "success_new_languages": "✅ Successfully translated {count} phrases for new languages!",
        "no_phrases_new_languages": "ℹ️ No phrases needed translation for new languages.",
        "no_new_languages_detected": "ℹ️ No new languages detected after addition.",
        
        # Final results
        "translation_success_total": "\n✅ SUCCESS: Translated {phrase_count} phrases across {lang_count} languages!",
        "translation_results_header": "\n📈 Translation Results:",
        "language_complete_result": "✅ {lang_name}: Complete ({count} phrases)",
        "language_incomplete_result": "⚠️  {lang_name}: {current}/{total} phrases ({missing} missing)",
        "no_translations_made_simple": "ℹ️ No translations were made.",
        
        # English phrases reference
        "english_phrases_reference": "📖 Found {count} English phrases as reference",
        
        # Continuing process
        "continuing_translation": "🔄 Continuing with translation process...",
        
        # English example
        "english_example": '''   Example:
   "en": {{
       "hello": "Hello",
       "world": "World"
   }}''',
    }

# ==================== FALLBACK STRATEGY MESSAGES ====================

def get_fallback_strategy_messages():
    """Messages for fallback_strategy.py module"""
    return {
        "fallback_command_target": "🎯 {command_name}: {file_path}",
        "display_section_found": "✅ DISPLAY_LANGUAGES section found!",
        "file_no_section_remove": "❌ File '{file_path}' doesn't have DISPLAY_LANGUAGES section!",
        "no_languages_to_remove": "💡 No languages to remove - section doesn't exist",
        "file_no_section_general": "❌ File '{file_path}' doesn't have DISPLAY_LANGUAGES section!",
        "generate_section_prompt_fallback": "👉 Do you want to generate a complete DISPLAY_LANGUAGES section now? (y/N): ",
        "generating_section_for_command": "🎯 Generating DISPLAY_LANGUAGES section for {command_name}...",
        "languages_selected_count": "🌍 Selected {count} languages: {languages}",
        "no_default_language_selected": "❌ No default language selected. Operation cancelled.",
        "default_language_set": "⭐ Default language set to: {lang_name} ({lang_code})",
        "error_during_language_selection": "❌ Error during language selection: {error}",
        "removing_old_functions": "🔄 Removing old display functions if any...",
        "inserting_section_at_position": "📝 Inserting section at position: {position}",
        "section_generated_success_count": "✅ Section generated successfully with {count} languages!",
        "languages_added_list_fallback": "📊 Languages: {languages}",
        "default_language_display": "⭐ Default language: {lang_code}",
        "old_functions_removed": "✅ Old display functions removed and replaced",
        "preview_header": "📋 GENERATED SECTION PREVIEW:",
        "unknown_command": "❌ Unknown command: {command_name}",
        "cli_usage_fallback": "❌ Usage: python fallback_strategy.py <command> <filename>",
        "available_commands": "Available commands: add-lang, translate, repair, set-global-lang, remove-lang",
    }

# ==================== COMMON MESSAGES ====================

def get_common_messages():
    """Common messages used across all modules"""
    return {
        # Error messages
        "file_not_found": "❌ File not found: {file_path}",
        "unexpected_error": "❌ Unexpected error: DISPLAY_LANGUAGES section not found after fallback",
        "generic_error": "❌ Error: {error}",
        "english_section_empty": "❌ Cannot translate: English section is empty!",
        "english_section_empty_translation": "⚠️  English section is empty - cannot translate without reference phrases",
        "add_english_first": "💡 Add English phrases first before translating other languages",
        "error_checking_english": "❌ Error checking English phrases: {error}",
        "no_internet": "❌ No internet connection! Translation requires internet access.",
        "check_internet": "💡 Please check your internet connection and run 'langguard translate' later",
        "import_error": "❌ Cannot import {module} module",
        
        # Process messages
        "continuing_process": "🔄 Continuing with analysis process...",
        
        # User input
        "enter_choice": "👉 Enter your choice:",
        "invalid_choice": "❌ Invalid choice. Please enter:",
        "invalid_input_yes_no": "❌ Please enter 'y' for Yes or 'n' for No",
        
        # Process
        "starting_translation": "🎯 Starting auto-translation...",
        "starting_auto_translation": "🎯 Running auto-translation...",
        "starting_language_addition": "🎯 Adding missing languages...",
        "starting_new_language_translation": "🎯 Running auto-translation for new languages...",
        "opening_language_addition": "🎯 Opening language addition mode...",
        "checking_new_languages": "📖 Checking for newly added languages...",
        "checking_new_languages_phrases": "\n🔍 Checking phrases for new languages...",
        "new_languages_detected": "🎯 Newly added languages detected: {languages}",
        "translating_new_languages": "🔄 Automatically translating new languages...",
        "no_new_languages": "ℹ️ No new languages detected after addition.",
        "translation_cancelled": "ℹ️ Translation cancelled.",
        "translation_error": "❌ Translation error: {error}",
        "translation_failed_cancelled": "❌ Translation failed or was cancelled.",
        "translation_success": "✅ Successfully translated {count} new languages!",
        
        # Results
        "success_translated": "✅ SUCCESS: Translated {count} phrases across {lang_count} languages!",
        "no_translations_made": "ℹ️ No translations were made.",
        
        # Warnings
        "warning_files_no_english": "⚠️  WARNING: {count} files have no English phrases:",
        "english_missing_has_languages": "   - {filename}: English missing (has: {languages})",
        "english_missing_no_languages": "   - {filename}: No languages found",
        "english_missing_error": "   - {filename}: Error reading file",
        "translation_requires_english": "   💡 Translation requires English phrases as reference",
        "translation_reference_note": "   💡 Translation requires English phrases as reference",
        
        # Display
        "empty_line": "",
        
        # Separators
        "separator": "=" * 50,
        "analysis_separator": "=" * 60,
        "fallback_separator": "=" * 60,
        "progress_separator": "=" * 50,
        "summary_separator": "-" * 40,
        "results_separator": "-" * 40,
        "preview_separator": "=" * 50,
        
        # Backup
        "backup_saved": "📁 Backup saved: {path}",
        "backup_location": "\n💾 Backup: {path}",
        
        # CLI usage
        "cli_missing_file": "❌ Please provide a target file.",
        "cli_usage": "Usage: python {module}.py <filename>",
        
        # Language templates
        "language_template_en": '    "en": {{\n        # English translations will be added globally later\n    }}',
        "language_template_pl": '    "pl": {{\n        # Polski translations will be added globally later\n    }}',
        "language_template_zh": '    "zh": {{\n        # 中文 translations will be added globally later\n    }}',
        "language_template_jp": '    "jp": {{\n        # 日本語 translations will be added globally later\n    }}',
        "language_template_de": '    "de": {{\n        # Deutsch translations will be added globally later\n    }}',
        "language_template_fr": '    "fr": {{\n        # Français translations will be added globally later\n    }}',
        "language_template_es": '    "es": {{\n        # Español translations will be added globally later\n    }}',
        "language_template_ru": '    "ru": {{\n        # Pycckuñ translations will be added globally later\n    }}',
        "language_template_pt": '    "pt": {{\n        # Portugués translations will be added globally later\n    }}',
        "language_template_id": '    "id": {{\n        # Indonesia translations will be added globally later\n    }}',
        "language_template_kr": '    "kr": {{\n        # 한국어 translations will be added globally later\n    }}',
        "language_template_generic": '    "{lang_code}": {{\n        # {lang_name} translations will be added globally later\n    }}',
        
        # Language format
        "format_language_display": "{lang_code} ({lang_name})",
        "available_languages_display": "📋 Available languages: {languages}",
        
        # ✅ MESSAGE UMUM YANG DIGUNAKAN DI BERBAGAI MODUL
        "operation_cancelled": "ℹ️ Operation cancelled. No changes made.",
        "section_not_found": "❌ DISPLAY_LANGUAGES section not found.",
        "no_languages_selected": "ℹ️ No languages selected.",
        "no_languages_to_add": "✅ No languages to add.",
        "no_changes_needed": "✅ No changes needed.",
        "no_changes_made": "ℹ️ No changes were made.",
    }

# ==================== REMOVE LANGUAGES MESSAGES ====================

def get_remove_languages_messages():
    """Messages for remove_languages.py module"""
    return {
        # Process messages
        "checking_existing_languages": "🔍 Checking existing languages...",
        "processing_languages_removal": "\n🔄 Processing {count} languages to remove: {languages}",
        "removing_entire_section": "🗑️ Removing entire DISPLAY_LANGUAGES section...",
        
        # Success messages
        "entire_section_removed_success": "✅ Entire DISPLAY_LANGUAGES section removed successfully!",
        "languages_removed_success": "✅ Successfully removed {count} languages!",
        "remaining_languages_count": "📊 Remaining languages: {count}",
        "new_language_order": "🔄 New order: {languages}",
        "default_language_preserved": "⭐ Default language preserved: {lang_code}",
        "operation_completed_success": "\n✅ Operation completed successfully!",
        
        # Warning messages
        "cannot_remove_default_language": "❌ Cannot remove default language: {lang_code}",
        "warning_no_languages_left": "⚠️ Warning: No languages left! Keeping default language.",
        "keeping_default_language": "🔒 Keeping default language: {lang_code}",
        "keeping_languages_count": "📋 Keeping {count} languages: {languages}",
        
        # Error messages
        "invalid_dictionary_structure": "❌ Invalid DISPLAY_LANGUAGES dictionary structure!",
        "section_not_found_expected_structure": "❌ DISPLAY_LANGUAGES section not found with expected structure",
        "no_languages_found_to_remove": "❌ No languages found to remove",
        "no_languages_selected_removal": "ℹ️ No languages selected for removal",
        "no_languages_to_remove_after_filter": "ℹ️ No languages to remove after filtering",
        
        # Fix messages
        "fixed_double_comma": "🔄 Fixed double comma issue",
        "fixed_trailing_comma": "🔄 Fixed trailing comma before closing brace",
    }

# ==================== INSERT SECTION MESSAGES ====================

def get_insert_section_messages():
    """Messages for insert_section.py module"""
    return {
        # Process messages
        "insert_section_target": "🎯 Target: {file_path}",
        "checking_display_section": "\n🔍 Checking DISPLAY LANGUAGE section...",
        "creating_new_section": "\n🎯 Creating new DISPLAY_LANGUAGES section...",
        "section_already_exists": "✅ DISPLAY_LANGUAGES section already exists!",
        "section_detected_complete": "✅ DISPLAY LANGUAGE section detected and complete.",
        "section_missing_incomplete": "⚠️ DISPLAY LANGUAGE section missing or incomplete.",
        
        # Global language selection
        "select_global_language_header": "\n🌍 SELECT GLOBAL DISPLAY LANGUAGE:",
        "global_language_note": "💡 Note: This will be the default language for translations",
        "global_language_auto_set": "🌍 Global language automatically set to: {lang_name} ({lang_code})",
        "global_language_set": "✅ Global language set to: {lang_name} ({lang_code})",
        "global_language_set_display": "🌍 Global language: {lang_code}",
        "no_default_selected_fallback": "❌ No default language selected. Using 'en' as fallback.",
        
        # Success messages
        "new_section_created": "✅ New DISPLAY_LANGUAGES section created with {count} languages!",
        "languages_added_list": "📊 Languages added: {languages}",
        "operation_completed_success": "\n✅ Operation completed!",
        
        # Information messages
        "missing_languages_note": "💡 Note: {count} languages missing: {languages}",
        "all_languages_complete": "🎉 All languages already complete!",
        "all_languages_exist_complete": "🎉 All supported languages already exist!",
        "no_languages_added": "ℹ️ No languages added.",
        
        # User prompts
        "add_missing_languages_prompt": "\n👉 Do you want to add the missing languages? (y/N): ",
        "repair_mode_prompt": "Do you want to run repair mode? (y/N): ",
        "create_new_section_prompt": "Do you want to create a new complete section? (y/N): ",
    }

# ==================== REPAIR FUNCTIONS MESSAGES ====================

def get_repair_functions_messages():
    """Messages for repair_functions.py module"""
    return {
        # Process messages
        "detecting_language_conflicts": "🔍 Detecting language conflicts...",
        "fixing_language_order": "🔧 Fixing language order...",
        "removing_duplicate_functions": "🔧 Removing duplicate functions and variables...",
        "cleaning_isolated_variables": "🔧 Cleaning isolated DISPLAY_LANG variables...",
        "running_ultra_final_repair": "🔧 Running ULTRA-FINAL repair (strict safe mode)...",
        "repairing_t_function": "🔧 Repairing t() function directly...",
        "repair_mode_strict_validation": "🔧 Repair mode with strict structure validation...",
        "running_full_repair": "🔧 Running FULL REPAIR...",

        # Priority selection messages
        "languages_with_phrases_priority": "💡 Bahasa dengan ✅ sudah memiliki phrases dan diutamakan",
        "language_with_phrases_selected": "✅ Global language set to: {lang_name} ({lang_code}) - memiliki {phrase_count} phrases",
        "system_selected_with_phrases": "🎯 System selected: {lang_code} (memiliki {phrase_count} phrases)",
        "language_option_with_phrases": "  {number}. {lang_code} - {lang_name} ✅ ({phrase_count} phrases)",
        "language_option_without_phrases": "  {number}. {lang_code} - {lang_name} ⏳ (0 phrases)",
        "phrases_count_display": "   💡 Dipilih karena memiliki {phrase_count} phrases",  # ✅ INI YANG DITAMBAH
        
        # Priority indicators
        "phrases_available_indicator": " ✅ ",
        "phrases_pending_indicator": " ⏳ ",
        
        # Success messages
        "no_language_conflicts": "✅ No language conflicts detected",
        "no_actual_conflicts": "✅ No actual conflicts (only one unique language)",
        "language_order_fixed": "✅ Language order fixed: {languages}",
        "content_repair_complete": "✅ Content repair complete — structure and values restored cleanly.",
        "fixed_corrupted_t_function": "✅ Fixed corrupted t() function with language '{lang_code}'",
        "missing_functions_added": "✅ Missing functions added successfully!",
        "full_repair_completed": "✅ Full repair completed successfully!",
        "language_conflicts_resolved": "✅ Language conflicts resolved!",
        "duplicate_functions_removed": "✅ Duplicate functions and variables removed!",
        "restored_from_backup": "🔄 Restored from backup due to error.",
        
        # Conflict detection
        "found_conflicting_languages": "⚠️  Found {count} conflicting languages: {languages}",
        "prioritizing_language": "🎯 Prioritizing '{lang_code}' (exists in DISPLAY_LANGUAGES)",
        "using_first_found_language": "🎯 Using first found language: '{lang_code}'",
        
        # Function block management
        "found_duplicate_blocks": "⚠️  Found {count} duplicate function blocks",
        "kept_function_blocks": "✅ Kept {kept} function block, removed {removed} duplicates",
        "no_duplicate_blocks": "✅ No duplicate function blocks found",
        "kept_display_lang": "✅ Kept DISPLAY_LANG: {lang_code}",
        "removed_duplicate_display_lang": "🗑️  Removed duplicate DISPLAY_LANG: {lang_code}",
        "removed_isolated_variables": "✅ Removed {count} isolated DISPLAY_LANG variables",
        
        # Language selection
        "select_default_language_header": "\n🌍 Please select the default display language:",
        "available_languages_header": "📋 Available languages in DISPLAY_LANGUAGES:",
        "language_selection_option": "  {number}. {lang_code} - {lang_name}{indicator}",
        "conflict_indicator": " ⚠️ (CURRENT CONFLICT)",
        "skip_option": "  S. Skip (let system decide)",
        "language_selection_prompt": "\n👉 Enter your choice (number, language code, or S): ",
        "system_selected_from_conflicts": "🎯 System selected: {lang_code} (from valid conflicts)",
        "system_selected_first_available": "🎯 System selected: {lang_code} (first available)",
        "order_fix_skipped_safety": "⚠️  Order fix skipped for safety - manual review recommended",
        
        # Error messages
        "section_not_found_order": "❌ DISPLAY_LANGUAGES section tidak ditemukan",
        "cannot_find_section_end": "❌ Tidak dapat menemukan akhir dari DISPLAY_LANGUAGES",
        "no_languages_found_in_section": "❌ Tidak ada bahasa yang ditemukan dalam DISPLAY_LANGUAGES",
        "error_fixing_order": "❌ Error fixing language order: {error}",
        "section_not_found_repair": "❌ DISPLAY_LANGUAGES section not found. Cannot repair content.",
        "section_content_not_found": "❌ DISPLAY_LANGUAGES content not found.",
        "no_corrupted_t_function": "ℹ️  No corrupted t() function found, checking for hardcoded languages...",
        "no_languages_available": "❌ No languages available in DISPLAY_LANGUAGES",
        "error_during_repair": "❌ Error during repair: {error}",
        
        # Information messages
        "languages_found_order": "📋 Languages found: {languages}",
        "using_preferred_language": "🎯 Using preferred language: {lang_code}",
        "no_conflicts_found": "✅ No conflicts found, using existing language",
        "using_existing_language": "🎯 Using existing language: {lang_code}",
        "no_languages_using_en": "ℹ️  No languages found in DISPLAY_LANGUAGES, using 'en'",
        "using_default_from_fallback": "🎯 Using default language from fallback: {lang_code}",
        "only_one_language_available": "✅ Only one language available: {lang_code}",
        "no_valid_conflicts": "🎯 No valid conflicts, using first available language: {lang_code}",
        "only_one_valid_conflict": "✅ Only one valid conflict: {lang_code}",
        "section_already_complete": "✅ DISPLAY_LANGUAGE section already complete!",
        "inserting_missing_functions": "📝 Inserting missing functions at position: {position}",
        "fixing_inconsistent_display_lang": "🔄 Fixing inconsistent DISPLAY_LANG: '{current}' → '{new}'",
        "add_english_suggestion": "💡 Add English phrases first to enable translation for other languages",
        "display_lang_consistency_fixed": "✅ DISPLAY_LANG consistency fixed to: {lang_code}",
        "using_existing_display_lang": "✅ Using existing DISPLAY_LANG: {lang_code}",
        "using_valid_display_lang": "✅ Using valid DISPLAY_LANG from file: {lang_code}",
        "using_first_available_language": "✅ Using first available language: {lang_code}",
        "invalid_display_lang_detected": "⚠️  Current DISPLAY_LANG '{current}' not found in DISPLAY_LANGUAGES",
        
        # User input validation
        "invalid_number_range": "❌ Please enter number between 1 and {max}",
        "invalid_choice_instructions": "❌ Invalid choice. Please enter:\n   - A number (1-{count})\n   - Language code ({languages})\n   - 'S' to skip",
    }

# ==================== LANGUAGE SELECTION MESSAGES ====================

def get_language_selection_messages():
    """Messages for language_selection.py module"""
    return {
        # Headers
        "language_selection_remove_header": "\n🎯 Select languages to REMOVE:",
        "language_selection_default_header": "\n🎯 Select DEFAULT display language:",
        "language_selection_add_header": "\n🎯 Select languages for DISPLAY_LANGUAGES:",
        "language_selection_available": "Available languages:",
        
        # Options and indicators
        "language_selection_option": "  {number}. {lang_code} - {lang_name}{indicator}",
        "current_default_indicator": " ⭐ (CURRENT DEFAULT)",
        "conflict_indicator": " ⚠️ (CURRENT CONFLICT)",
        
        # Notes and instructions
        "cannot_remove_default_note": "💡 Default language ({lang_code}) cannot be removed!",
        "default_language_note": "💡 This will be the initial active language",
        
        # Selection instructions
        "selection_instruction_single": "   - Single number (e.g., 1)",
        "selection_instruction_codes": "   - Language codes separated by comma (e.g., en,id,kr)",
        "selection_instruction_multiple": "   - Multiple numbers separated by comma (e.g., 1,3,5)",
        "selection_instruction_all": "   - 'A' for all languages",
        "selection_instruction_skip": "   - 'S' to skip",
        "selection_instruction_remove_all": "   - 'T' to remove entire DISPLAY_LANGUAGES section",
        
        # Confirmation prompts
        "confirm_remove_all_prompt": "⚠️  PERINGATAN: Ini akan menghapus SELURUH bagian DISPLAY_LANGUAGES! Lanjutkan? (y/N): ",
        
        # Success messages
        "operation_skipped": "⏭️ Operation skipped. No changes made.",
        "remove_all_cancelled": "ℹ️ Penghapusan section dibatalkan",
        "global_language_auto_set": "🌍 Global language automatically set to: {lang_name} ({lang_code})",
        
        # Error messages
        "invalid_language_codes": "❌ Invalid language codes: {codes}",
        "available_language_codes": "💡 Available codes: {codes}",
        "no_valid_languages_selected": "❌ No valid languages selected",
        "select_only_one_default": "❌ Please select only ONE language for default display language",
        "invalid_number": "❌ Invalid number: {number}",
        "invalid_input": "❌ Invalid input: {input}",
        
        # Error instructions
        "invalid_choice_number": "❌ Invalid choice. Please enter:",
        "invalid_choice_range": "   - A number (1-{max})",
        "invalid_choice_multiple": "   - Multiple numbers (e.g., 1,3,5)",
        "invalid_choice_codes": "   - Language code(s) ({codes})",
        "invalid_choice_all": "   - 'A' for all languages",
        "invalid_choice_skip": "   - 'S' to skip",
        "invalid_choice_remove": "   - 'T' to remove entire section",
    }

# ==================== COMBINE ALL MESSAGES ====================

def get_all_messages():
    """Combine all messages from all modules"""
    common_messages = get_common_messages()
    update_messages = get_update_language_messages()
    analysis_messages = get_analysis_messages()
    add_languages_messages = get_add_languages_messages()
    translation_messages = get_translation_messages()
    fallback_messages = get_fallback_strategy_messages()
    remove_languages_messages = get_remove_languages_messages()
    insert_section_messages = get_insert_section_messages()
    repair_functions_messages = get_repair_functions_messages()
    language_selection_messages = get_language_selection_messages()
    
    # Combine all messages, with common messages as base
    all_messages = {**common_messages, **update_messages, **analysis_messages, 
                   **add_languages_messages, **translation_messages, **fallback_messages,
                   **remove_languages_messages, **insert_section_messages, 
                   **repair_functions_messages, **language_selection_messages}
    
    return all_messages

# ==================== LANGUAGE TEMPLATES ====================

def get_language_templates():
    """Get templates for all supported languages"""
    messages = get_all_messages()
    return {
        "en": messages["language_template_en"],
        "pl": messages["language_template_pl"],
        "zh": messages["language_template_zh"],
        "jp": messages["language_template_jp"],
        "de": messages["language_template_de"],
        "fr": messages["language_template_fr"],
        "es": messages["language_template_es"],
        "ru": messages["language_template_ru"],
        "pt": messages["language_template_pt"],
        "id": messages["language_template_id"],
        "kr": messages["language_template_kr"]
    }

def get_language_template(lang_code, lang_name=None):
    """Get template for specific language"""
    templates = get_language_templates()
    if lang_code in templates:
        return templates[lang_code]
    
    # Fallback untuk bahasa yang tidak ada di template spesifik
    messages = get_all_messages()
    lang_display = lang_name or lang_code.upper()
    return messages["language_template_generic"].format(lang_code=lang_code, lang_name=lang_display)

# ==================== FORMATTED MESSAGES ====================

def format_no_english_phrases(default_lang="en"):
    """Format pesan error untuk English phrases yang missing"""
    return f"""
❌ CRITICAL ERROR: No English phrases found in DISPLAY_LANGUAGES!
💡 English phrases are required as reference for translation
🔧 Action: Manually add English phrases to the 'en' section

   Example:
   "en": {{
       "hello": "Hello",
       "world": "World"
   }}

🌍 Default display language: '{default_lang}'
📝 Note: The 't()' function uses English as fallback when translations are missing
💡 After adding English phrases, run 'langguard translate' again
"""

def format_analysis_header(file_path):
    messages = get_all_messages()
    separator = "=" * 60
    return messages["analysis_header"].format(file_path=file_path, separator=separator)

def format_language_order(current, expected):
    messages = get_all_messages()
    return f"{messages['order_incorrect']}\n{messages['current_order'].format(current=current)}\n{messages['expected_order'].format(expected=expected)}"

# ==================== CONVENIENCE FUNCTIONS ====================

def get_message(key, **kwargs):
    """Get formatted message dengan parameter"""
    messages = get_all_messages()
    if key in messages:
        return messages[key].format(**kwargs)
    return f"Message not found: {key}"

def print_message(key, **kwargs):
    """Print message langsung"""
    print(get_message(key, **kwargs))

# ==================== COMMON UTILITY FUNCTIONS ====================

def check_internet_connection():
    """Cek koneksi internet untuk translation"""
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False

LANGUAGE_NAMES = {
    "en": "English", "pl": "Polski", "zh": "中文", "jp": "日本語",
    "de": "Deutsch", "fr": "Français", "es": "Español", "ru": "Pycckuñ",
    "pt": "Portugués", "id": "Indonesia", "kr": "한국어"
}

def format_language_display(lang_code):
    """Format tampilan bahasa: en (English)"""
    lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
    return get_message("format_language_display", lang_code=lang_code, lang_name=lang_name)

def format_languages_list(lang_codes):
    """Format list bahasa menjadi string"""
    formatted_langs = [format_language_display(lang) for lang in lang_codes]
    return ', '.join(formatted_langs)