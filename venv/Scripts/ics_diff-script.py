#!C:\Users\morit\PycharmProjects\AutoInvoice\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'vobject==0.9.6.1','console_scripts','ics_diff'
__requires__ = 'vobject==0.9.6.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('vobject==0.9.6.1', 'console_scripts', 'ics_diff')()
    )
