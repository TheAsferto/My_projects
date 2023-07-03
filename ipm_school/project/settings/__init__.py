from pathlib import Path

from split_settings.tools import include, optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

include(
    'base.py',
    optional('/home/nickolay/Документы/Web Projects/IPM_School/local/development.py')
)