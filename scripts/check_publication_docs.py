"""Check document structure, links, quantitative parity and package integrity.

Run from any directory. Optional --peer points to the matching HF package.
Translation meaning still requires human review; these are structural checks.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote


def body(text):
    if text.startswith('---\n'):
        return text.split('---\n', 2)[2]
    return text


def numbers(text):
    text = re.sub(r'\]\([^)]*\)', ']', text)
    return Counter(re.findall(r'(?<![A-Za-z])\d+(?:[.,]\d+)*(?:e-\d+)?', text))


def anchors(text):
    explicit = re.findall(r'<a id="([^"]+)"', text)
    generated = []
    for heading in re.findall(r'^#{1,6} (.+)$', text, re.M):
        heading = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        generated.append(heading)
    return set(explicit + generated)


def table_shape(text):
    return [len(line.split('|')) for line in text.splitlines() if line.startswith('|')]


def check(root):
    docs = {p.relative_to(root): p.read_text(encoding='utf-8')
            for p in root.rglob('*.md') if '.git' not in p.parts}
    for a, b in [('README.md', 'README.id.md'), ('docs/usage.md', 'docs/usage.id.md'),
                 ('docs/results.md', 'docs/results.id.md')]:
        en, ind = body(docs[Path(a)]), body(docs[Path(b)])
        ids = lambda s: re.findall(r'<a id="([^"]+)"', s)
        assert ids(en) and ids(en) == ids(ind), (a, 'section IDs differ')
        assert len(re.findall(r'^## ', en, re.M)) == len(ids(en)), a
        assert len(re.findall(r'^## ', ind, re.M)) == len(ids(ind)), b
        assert numbers(en) == numbers(ind), (a, 'quantitative text differs')
        assert table_shape(en) == table_shape(ind), (a, 'table shapes differ')
        assert re.findall(r'```[^\n]*\n(.*?)```', en, re.S) == re.findall(
            r'```[^\n]*\n(.*?)```', ind, re.S), (a, 'examples differ')
        assert re.findall(r'!\[[^]]*\]\(([^)]+)\)', en) == re.findall(
            r'!\[[^]]*\]\(([^)]+)\)', ind), (a, 'figures differ')
    for name, text in docs.items():
        assert '\ufffd' not in text, (name, 'invalid decoded character')
        assert not re.search(r'\w\?\w', re.sub(r'https?://\S+', '', text)), (
            name, 'possible encoding damage')
        assert text.count('```') % 2 == 0, (name, 'unclosed code fence')
        for snippet in re.findall(r'```python\n(.*?)```', text, re.S):
            compile(snippet, str(name), 'exec')
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if link.startswith(('https:', 'http:', 'mailto:')):
                continue
            target, _, fragment = unquote(link).partition('#')
            destination = (root / name).parent / target if target else root / name
            assert destination.exists(), (name, 'missing target', link)
            if fragment and destination.suffix == '.md':
                assert fragment in anchors(destination.read_text(encoding='utf-8')), (
                    name, 'missing anchor', link)
    metrics = json.loads((root / 'reports/metrics/test_metrics.json').read_text())['test']
    readme = docs[Path('README.md')]
    for key in ['acc_food_type', 'acc_dish', 'acc_cooking']:
        assert f'{metrics[key] * 100:.2f}%' in readme, key
    for key in ['mae_calories_kcal', 'mae_protein_g', 'mae_fat_g', 'mae_carbohydrate_g']:
        assert f'{metrics[key]:.2f}' in readme, key
    for line in (root / 'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
    print(f'PASS: {root.name}: {len(docs)} documents; parity, links, examples, metrics, checksums')
    return docs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--peer', type=Path)
    args = parser.parse_args()
    first = check(args.root)
    if args.peer:
        second = check(args.peer)
        for name in first.keys() & second.keys():
            assert body(first[name]) == body(second[name]), ('cross-platform drift', name)
        print('PASS: all shared Markdown bodies match across platforms (HF YAML excluded)')
