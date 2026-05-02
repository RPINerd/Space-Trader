"""
    Space Trader | RPINerd, 2024

    An elite-inspired space trading RPG originally on PalmOS

    Utils Module
    The utils module has a couple of functions that were separated in the original codebase.
    Likely could refactor these into the respective modules, but for now they are here.
"""

import shutil
import sys
from pathlib import Path


class FontManager:

    """"""

    linux_font_path = "~/.fonts/"

    @classmethod
    def init_font_manager(cls) -> bool:
        """"""
        # Linux
        if sys.platform.startswith("linux"):
            try:
                if not Path.expanduser(cls.linux_font_path).is_dir():
                    Path.mkdir(Path.expanduser(cls.linux_font_path), parents=True, exist_ok=True)
                return True
            except Exception as err:
                sys.stderr.write("FontManager error: " + str(err) + "\n")
                return False

        # Other platforms
        else:
            return True

    @classmethod
    def windows_load_font(cls, font_path: str | bytes, private: bool = True, enumerable: bool = False) -> bool:
        """
        Load font on Windows OS (hopefully)

        Function taken from:
        https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309
        """
        from ctypes import byref, create_string_buffer, create_unicode_buffer, windll  # noqa

        FR_PRIVATE = 0x10
        FR_NOT_ENUM = 0x20

        if isinstance(font_path, bytes):
            path_buffer = create_string_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExA
        elif isinstance(font_path, str):
            path_buffer = create_unicode_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError("font_path must be of type bytes or str")

        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        num_fonts_added = add_font_resource_ex(byref(path_buffer), flags, 0)
        return bool(min(num_fonts_added, 1))

    @classmethod
    def load_font(cls, font_path: str) -> bool:
        """"""
        # Windows
        if sys.platform.startswith("win"):
            return cls.windows_load_font(font_path, private=True, enumerable=False)

        # Linux
        if sys.platform.startswith("linux"):
            try:
                shutil.copy(font_path, Path.expanduser(cls.linux_font_path))
                return True
            except Exception as err:
                sys.stderr.write("FontManager error: " + str(err) + "\n")
                return False

        # macOS and others
        else:
            return False
