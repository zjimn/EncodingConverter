import os
import polib
from tkinter import messagebox
from util.path_util import get_base_path


def convert_po_to_mo():

    project_root = get_base_path()
    locales_dir = os.path.join(project_root, 'locales')
    """Convert all .po files in the specified locales directory to .mo files."""
    # Traverse through the locales directory
    for dirpath, dirnames, filenames in os.walk(locales_dir):
        for filename in filenames:
            if filename.endswith('.po'):
                po_file_path = os.path.join(dirpath, filename)
                mo_file_path = os.path.splitext(po_file_path)[0] + '.mo'  # Change the file extension to .mo

                if not os.path.exists(po_file_path):
                    print(f"PO file does not exist: {po_file_path}")
                    continue

                if os.path.exists(mo_file_path):
                    po_mtime = os.path.getmtime(po_file_path)
                    mo_mtime = os.path.getmtime(mo_file_path)
                    if po_mtime <= mo_mtime:
                        print(f"MO file is up to date. No conversion needed for: {mo_file_path}")
                        continue

                po = polib.pofile(po_file_path)
                po.save_as_mofile(mo_file_path)
                print(f"Converted {po_file_path} to {mo_file_path}")

if __name__ == '__main__':
    convert_po_to_mo()
