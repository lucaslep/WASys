import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Include all Python files from the "utils" folder
include_files = [
    ("utils", "utils"), ("classes", "classes"), ("config", "config"),
    ("constants", "constants"), ("repositories", "repositories")
]

packages = [
    'firebirdsql', 'selenium', 'webdriver_manager', 'urllib'
]

# Build options
build_options = {
    'packages': packages,  # List any additional packages you need
    'excludes': [],  # List any packages to exclude
    'include_files': [],  # List any additional files or data needed
    "zip_include_packages": [],
    "zip_exclude_packages": [],
    "build_exe": "exe" 
}

# Setup cx_Freeze
setup(
    name='IntelectualSysWhatsApp',
    version='1.0',
    description='Modulo de envio de mensagens whatsapp do intelectualSys',
    options={'build_exe': build_options},
    executables= [Executable('PyWPP.py', base=base)]
)