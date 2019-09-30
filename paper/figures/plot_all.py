"""plot_all.py

Simple script to iterate over sub-directories (relative to here)
and run the plotting script in each.

J. Metz <metz.jp@gmail.com>
"""
from pathlib import Path
# import traceback
import subprocess
try:
    import colorama
    use_colorama = True
except ModuleNotFoundError:
    use_colorama = False


if use_colorama:
    colorama.init()

    def subprint(text):
        print(colorama.Fore.YELLOW + text + colorama.Fore.RESET)

else:
    def subprint(text):
        indent = "\t"
        print(indent + text.replace("\n", "\n" + indent))


def main():
    """
    Main entry point function
    """
    folders = [item for item in Path('.').iterdir() if item.is_dir()]
    for folder in folders:
        try:
            run_folder(folder)
        except ValueError as err:
            print(f"Folder failed: {folder}")
            indent = "\t"
            # subprint(traceback.format_exc())
            subprint(f"{err}")


def run_folder(folder):
    """
    Runs the plotting script in the folder
    """
    plotting_script = list(folder.glob("*.py"))
    if len(plotting_script) > 1:
        raise ValueError(f"Too many python scripts in:\n    {folder}")
    elif len(plotting_script) == 0:
        raise ValueError(f"No python scripts found in:\n    {folder}")
    plotting_script = plotting_script[0]
    subprocess.check_call(['python', plotting_script])


if __name__ == '__main__':
    main()
