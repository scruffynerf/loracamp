import gettext
from pathlib import Path

def setup_i18n(locale_code: str = "en"):
    locale_dir = Path(__file__).parent / "locales"
    
    # Fallback to English if the translation doesn't exist
    translation = gettext.translation(
        "messages", 
        localedir=locale_dir, 
        languages=[locale_code], 
        fallback=True
    )
    translation.install()
    return translation.gettext

# Usage:
# _ = setup_i18n("en")
# print(_("Listen"))
