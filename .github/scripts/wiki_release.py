"""Prepare wiki release changelogs and select notes for publication."""

import argparse
from datetime import date
from pathlib import Path
import re
import subprocess


def sections(text):
    """Return level-two headings and their bodies, excluding link definitions."""
    matches = list(re.finditer(r"^## (.+)$", text, re.MULTILINE))
    result = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        body = re.split(r"^\[[^]]+\]:", body, maxsplit=1, flags=re.MULTILINE)[0]
        result.append((match.group(1), body.strip(), match.start(), end))
    return result


def has_entries(body):
    """Require at least one Markdown bullet."""
    return bool(re.search(r"^- +\S", body, re.MULTILINE))


def next_tag(tags, text, today):
    """Reserve versions already used by tags or changelog sections."""
    base = f"wiki-{today:%Y.%m}"
    used = set(tags) | set(re.findall(r"^## \[([^]]+)\]", text, re.MULTILINE))
    numbers = [0 if tag == base else int(tag[len(base) + 1:])
               for tag in used if re.fullmatch(re.escape(base) + r"(?:\.[1-9]\d*)?", tag)]
    return base if not numbers else f"{base}.{max(numbers) + 1}"


def prepare(text, tags, today):
    """Move pending entries to a new dated release, retaining empty Unreleased."""
    pending = [item for item in sections(text) if item[0] == '[Unreleased]']
    if len(pending) != 1 or not has_entries(pending[0][1]):
        raise ValueError('Expected one nonempty Unreleased section')
    _, body, start, end = pending[0]
    tag = next_tag(tags, text, today)
    # Existing reference links live after the final section and must be preserved.
    tail = text[end:]
    if end == len(text):
        links = re.search(r"^\[[^]]+\]:", text[start:], re.MULTILINE)
        if links:
            tail = text[start + links.start():]
    replacement = f"## [Unreleased]\n\n## [{tag}] - {today.isoformat()}\n\n{body}\n\n"
    updated = text[:start] + replacement + tail
    updated = updated.rstrip() + f"\n\n[{tag}]: https://github.com/antwanchild/docs/releases/tag/{tag}\n"
    return tag, updated


def release_notes(text, tags):
    """Select only the newest dated wiki section, including across month boundaries."""
    releases = [item for item in sections(text) if item[0] != '[Unreleased]']
    if not releases:
        return None
    heading, body, _, _ = releases[0]
    match = re.fullmatch(r"\[(wiki-\d{4}\.\d{2}(?:\.[1-9]\d*)?)\] - (\d{4}-\d{2}-\d{2})", heading)
    if not match:
        raise ValueError('Invalid wiki release heading')
    tag, released = match.groups()
    date.fromisoformat(released)
    if tag in tags:
        return None
    if not has_entries(body):
        raise ValueError(f'Empty release notes for {tag}')
    return tag, body


def automatic_release(text, tags, today):
    """Retry a prepared release or archive pending entries for a new release."""
    result = release_notes(text, tags)
    if result is not None:
        return text, result
    pending = [item for item in sections(text) if item[0] == '[Unreleased]']
    if len(pending) != 1:
        raise ValueError('Expected exactly one Unreleased section')
    if not has_entries(pending[0][1]):
        return text, None
    _, updated = prepare(text, tags, today)
    return updated, release_notes(updated, tags)


def main():
    """Run from the repository root."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('prepare', 'notes', 'auto'))
    args = parser.parse_args()
    path = Path('wiki/CHANGELOG.md')
    text = path.read_text(encoding='utf-8')
    tags = subprocess.check_output(['git', 'tag', '--list'], text=True).splitlines()
    if args.command == 'prepare':
        tag, updated = prepare(text, tags, date.today())
        path.write_text(updated, encoding='utf-8')
        print(tag)
    else:
        if args.command == 'auto':
            updated, result = automatic_release(text, tags, date.today())
            if updated != text:
                path.write_text(updated, encoding='utf-8')
        else:
            result = release_notes(text, tags)
        if result:
            tag, body = result
            Path('release-notes.md').write_text(body + '\n', encoding='utf-8')
            print('should_release=true')
            print(f'tag={tag}')
        else:
            print('should_release=false')


if __name__ == '__main__':
    main()
