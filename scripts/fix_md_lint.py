#!/usr/bin/env python3
"""
Fix common markdown lint issues (MD022, MD031, MD040) in one or more .md files.

Usage:
    python scripts/fix_md_lint.py docs/ref-sample.md docs/ref-creator.md
    python scripts/fix_md_lint.py docs/*.md
"""
import re
import sys
from pathlib import Path


def fix_table_spacing(line: str) -> str:
    """Ensure exactly one space around each pipe in a markdown table row."""
    if "|" not in line:
        return line
    stripped = line.strip()
    # Check if it looks like a table row: starts and ends with |, and not a code fence
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return line
    if stripped.startswith("```"):
        return line

    parts = line.split("|")
    new_parts = []
    for i, part in enumerate(parts):
        # parts[0] is everything before the first |
        # parts[-1] is everything after the last |
        if i == 0:
            new_parts.append(part.rstrip()) # Keep leading indent
            continue
        if i == len(parts) - 1:
            new_parts.append(part.lstrip())
            continue
        
        # For columns: ensure one space on each side
        # Handle empty columns properly (don't add double space)
        p = part.strip()
        if p:
            new_parts.append(f" {p} ")
        else:
            new_parts.append(" ") # Result is | | instead of |  |
        
    return "|".join(new_parts)


def fix_markdown(filepath: str) -> bool:
    """Fix common markdown lint issues in a file. Returns True if changes were made."""
    p = Path(filepath)
    if not p.exists() or p.suffix != ".md":
        print(f"  Skipping {filepath} (not a .md file or does not exist)")
        return False

    original = p.read_text(encoding="utf-8")
    content = original

    # 1. Normalize excessive blank lines (max 1 blank line between content)
    content = re.sub(r"\n{3,}", "\n\n", content)

    # 2. Ensure blank lines around headings (MD022)
    #    - Blank line after heading if next line is not blank
    #    - Blank line before heading if previous line is not blank
    lines = content.split("\n")
    result: list[str] = []
    for i, line in enumerate(lines):
        is_heading = bool(re.match(r"^#{1,6}\s", line))
        prev_line = result[-1] if result else ""

        # Insert blank line BEFORE heading if previous line is non-blank content
        if is_heading and prev_line.strip() != "" and not prev_line.startswith("```"):
            result.append("")

        result.append(line)

        # Insert blank line AFTER heading if next line is non-blank content
        if is_heading and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip() != "":
                result.append("")

    lines = result

    # 3. Ensure blank lines around fenced code blocks (MD031)
    result = []
    in_code = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        is_fence = stripped.startswith("```")

        if is_fence and not in_code:
            # Opening fence — ensure blank line before it
            if result and result[-1].strip() != "":
                result.append("")
            in_code = True
            result.append(line)
        elif is_fence and in_code:
            # Closing fence — remove trailing blanks inside block, then ensure blank after
            while result and result[-1].strip() == "":
                result.pop()
            result.append(line)
            in_code = False
        else:
            # Fix table spacing (MD060) outside code blocks
            fixed_line = fix_table_spacing(line)
            result.append(fixed_line)

    content = "\n".join(result)

    # 4. Normalize again after insertions
    content = re.sub(r"\n{3,}", "\n\n", content)

    # 5. Ensure file ends with exactly one newline
    content = content.rstrip("\n") + "\n"

    if content != original:
        p.write_text(content, encoding="utf-8")
        print(f"  Fixed: {filepath}")
        return True
    else:
        print(f"  OK (no changes): {filepath}")
        return False


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/fix_md_lint.py <file.md> [file2.md ...]")
        sys.exit(1)

    files = sys.argv[1:]
    fixed = 0
    for f in files:
        if fix_markdown(f):
            fixed += 1

    print(f"\nDone. {fixed}/{len(files)} file(s) updated.")


if __name__ == "__main__":
    main()
