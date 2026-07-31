import os
import re
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

def validate_docs():
    root = get_repo_root()
    docs_dir = os.path.join(root, 'docs')
    if not os.path.exists(docs_dir):
        print(f"ERROR: docs directory not found at {docs_dir}")
        sys.exit(1)

    allowed_tags = extract_valid_tags(os.path.join(docs_dir, 'index.md'))

    errors = []
    link_patterns = (
        re.compile(r'!?\[[^\]]*\]\(\s*(<[^>]*>|[^)\s]+)'),
        re.compile(r'!\[\[([^]|#]+)'),
    )
    markdown_files = []

    for dirpath, _, filenames in os.walk(docs_dir):
        for filename in filenames:
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            markdown_files.append((rel_path, content))

            if filename not in ['log.md', 'index.md']:
                if not content.startswith('---'):
                    errors.append(f"{rel_path}: Missing YAML frontmatter")
                    continue

                stat = os.stat(filepath)
                timestamp = datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                frontmatter = re.match(r'\A---\n(.*?)\n---', content, re.DOTALL)
                if frontmatter:
                    header = frontmatter.group(1)
                    if re.search(r'^timestamp:.*$', header, re.MULTILINE):
                        header = re.sub(r'^timestamp:.*$', f'timestamp: {timestamp}', header, count=1, flags=re.MULTILINE)
                    else:
                        header += f'\ntimestamp: {timestamp}'
                    updated = f'---\n{header}\n---' + content[frontmatter.end():]
                    if updated != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(updated)
                        os.utime(filepath, ns=(stat.st_atime_ns, stat.st_mtime_ns))
                        content = updated

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

    print("OKF docs validation passed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    validate_docs()
