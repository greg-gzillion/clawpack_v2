"""Install constitutional hooks into .git/hooks/"""
import sys, shutil
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
HOOKS_DIR = PROJECT / ".git" / "hooks"
SCRIPTS_DIR = PROJECT / "scripts"

hooks = {
    "pre-commit": SCRIPTS_DIR / "pre_commit.py",
}

for hook_name, source in hooks.items():
    dest = HOOKS_DIR / hook_name
    if sys.platform == "win32":
        # Windows: create .bat wrapper
        bat = HOOKS_DIR / f"{hook_name}.bat"
        bat.write_text(f'@echo off\npython "{source}" %*\n')
        print(f"Installed: {bat}")
    else:
        shutil.copy(source, dest)
        dest.chmod(0o755)
        print(f"Installed: {dest}")

print("\nConstitutional hooks installed.")
