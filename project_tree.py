from pathlib import Path

IGNORE = {
    ".venv",
    "__pycache__",
    ".git",
    ".idea",
    ".pytest_cache",
    "node_modules",
    ".svelte-kit",
}

def print_tree(path: Path, prefix=""):
    # List directories and files separately
    entries = sorted(
        [p for p in path.iterdir() if p.name not in IGNORE],
        key=lambda p: (p.is_file(), p.name.lower())
    )

    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        print(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            print_tree(entry, prefix + extension)

# Print root folder name
root = Path(".").resolve()
print(root.name)
print_tree(root)
