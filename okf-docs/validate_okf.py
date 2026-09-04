import os
import re
import subprocess
import sys
from datetime import datetime, timezone

from urllib.parse import unquote, urlsplit

import yaml

def get_repo_root():
    """Find the repository containing the current working directory."""
    current = os.path.abspath(os.getcwd())
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.getcwd()

def extract_valid_tags(root_index_path):
    if not os.path.exists(root_index_path):
        return set()
    with open(root_index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return set(re.findall(r'#([a-zA-Z0-9_\-]+)', content))

def get_changed_docs(root):
    """Return docs with content changes, ignoring timestamp-only edits."""
    result = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=ACMRTUXB',
         '-I', r'^timestamp:.*$', 'HEAD', '--', 'docs'],
        cwd=root, check=True, capture_output=True, text=True,
    )
    return set(result.stdout.splitlines())

def extract_timestamp(content):
    match = re.search(r'^timestamp:\s*(.*?)\s*$', content, re.MULTILINE)
    return match.group(1) if match else None

def get_head_timestamp(root, rel_path):
    result = subprocess.run(
        ['git', 'show', f'HEAD:{rel_path}'],
        cwd=root, capture_output=True, text=True,
    )
    return extract_timestamp(result.stdout) if result.returncode == 0 else None

def validate_docs():
    root = get_repo_root()
    docs_dir = os.path.join(root, 'docs')
    if not os.path.exists(docs_dir):
        print(f"ERROR: docs directory not found at {docs_dir}")
        sys.exit(1)

    allowed_tags = extract_valid_tags(os.path.join(docs_dir, 'index.md'))

    errors = []
    changed_docs = get_changed_docs(root)
    link_patterns = (
        re.compile(r'!?\[[^\]]*\]\(\s*(<[^>]*>|[^)\s]+)'),
        re.compile(r'!\[\[([^]|#]+)'),
    )
    markdown_files = []
    updated_timestamps = []

    for dirpath, _, filenames in os.walk(docs_dir):
        for filename in filenames:
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root)

            with open(filepath, encoding='utf-8') as f:
                content = f.read()

            if filename not in ['log.md', 'index.md']:
                if not content.startswith('---'):
                    errors.append(f"{rel_path}: Missing YAML frontmatter")
                    continue

                frontmatter = re.match(r'\A---\n(.*?)\n---', content, re.DOTALL)
                if frontmatter:
                    current = extract_timestamp(frontmatter.group(1))
                    changed = rel_path in changed_docs and current == get_head_timestamp(root, rel_path)
                    # Refresh timestamp using git state.
                    if current is None or changed:
                        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                        header = frontmatter.group(1)
                        if current is None:
                            header += f'\ntimestamp: {timestamp}'
                        else:
                            header = re.sub(r'^timestamp:.*$', f'timestamp: {timestamp}', header, 1, re.MULTILINE)
                        content = f'---\n{header}\n---' + content[frontmatter.end():]
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        updated_timestamps.append(rel_path)

                try:
                    meta = yaml.safe_load(content.split('---')[1]) or {}
                    if 'type' not in meta:
                        errors.append(f"{rel_path}: Missing mandatory 'type' key")

                    for tag in meta.get('tags', []):
                        tag = tag.lstrip('#')
                        if tag not in allowed_tags:
                            errors.append(f"{rel_path}: Tag '#{tag}' is not registered in docs/index.md")
                except Exception as e:
                    errors.append(f"{rel_path}: Invalid YAML formatting ({str(e).strip()})")

            markdown_files.append((rel_path, content))

    # Check local Markdown links and embeds relative to each source file.
    for rel_path, content in markdown_files:
        for pattern in link_patterns:
            for match in pattern.finditer(content):
                link = match.group(1).strip()
                if link.startswith('<') and link.endswith('>'):
                    link = link[1:-1]
                parsed_link = urlsplit(link)
                if not parsed_link.path or parsed_link.scheme or link.startswith('//'):
                    continue
                clean_link = unquote(parsed_link.path)
                base_path = docs_dir if clean_link.startswith('/') else os.path.dirname(os.path.join(root, rel_path))
                target_path = os.path.normpath(os.path.join(base_path, clean_link.lstrip('/')))
                if (
                    os.path.commonpath((docs_dir, target_path)) != docs_dir
                    or not os.path.exists(target_path)
                ):
                    errors.append(f"{rel_path}: Broken link target '{link}'")

    if errors:
        for err in errors:
            print(err)
        sys.exit(1)

    if updated_timestamps:
        print('Updated timestamps: ' + ', '.join(updated_timestamps))
    print("OKF docs validation passed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    validate_docs()
