Add multi-language support to the app using Flask-Babel.

## Languages to support
- English (en) — default
- Spanish (es)
- Portuguese — Brazil (pt_BR)
- French (fr)
- German (de)
- Italian (it)

## Requirements

### Language toggle
- Add a language selector to the navbar (flag icon or language name)
- Persist the selected language in the Flask session
- Default language detected from browser Accept-Language header
- Fallback to English if language not supported

### Translatable content
Every piece of UI text must be wrapped in Flask-Babel's translation function:
- All labels, buttons, titles, placeholders
- All error messages and validation messages
- All toast notifications
- All empty state messages
- All confirmation dialogs

### File structure
app/
translations/
es/LC_MESSAGES/messages.po
pt_BR/LC_MESSAGES/messages.po
fr/LC_MESSAGES/messages.po
de/LC_MESSAGES/messages.po
it/LC_MESSAGES/messages.po
babel.cfg

### Translation quality
- Use accurate, natural translations for each language
- Do not use machine-literal translations
- Financial and UI terminology must be correct in each language

### Technical requirements
- Install Flask-Babel
- Configure babel.cfg
- Add locale_selector function
- Compile .mo files from .po files
- All new features added in the future must also be translatable

### UI requirements
- Language selector must match the premium dark UI style defined in the design rules
- Smooth transition when switching languages
- Selected language must be visually indicated in the selector