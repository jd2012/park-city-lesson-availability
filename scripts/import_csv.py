import csv
import io
import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def parse(text):
    reader = csv.DictReader(io.StringIO(text.lstrip('\ufeff')), strict=True)
    required = {'begindate', 'enddate', 'category_or_activity_code', 'day1', 'date1'}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError('Upload a Ski School Summary CSV with daily dates and counts.')
    data = {}
    for row in reader:
        key = {'18190': 'ski', '18195': 'snowboard'}.get(row['category_or_activity_code'].strip())
        if not key:
            continue
        begin = datetime.strptime(row['begindate'].strip(), '%b %d %Y').date()
        end = datetime.strptime(row['enddate'].strip(), '%b %d %Y').date()
        for n in range(1, 26):
            raw = (row.get(f'date{n}') or '').strip()
            if not raw:
                continue
            month, day = map(int, raw.split('/'))
            year = begin.year + ((month, day) < (begin.month, begin.day))
            current = date(year, month, day)
            if not begin <= current <= end:
                raise ValueError(f'Date outside report range: {raw}')
            count = (row.get(f'day{n}') or '').strip()
            if not re.fullmatch(r'[0-9]+', count):
                raise ValueError(f'Invalid {key} count for {current}')
            entry = data.setdefault(current.isoformat(), {})
            if key in entry:
                raise ValueError(f'Duplicate {key} count for {current}')
            entry[key] = int(count)
    if not data or any(set(v) != {'ski', 'snowboard'} for v in data.values()):
        raise ValueError('Both Ski and Snowboard counts are required for every date.')
    dates = sorted(data)
    if (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days + 1 != len(dates):
        raise ValueError('Report has missing dates.')
    return dict(sorted(data.items()))


def main():
    # Git history, rather than checkout timestamps or filenames, determines the newest upload.
    commits = subprocess.check_output(['git', 'rev-list', 'HEAD', '--', 'uploads'], text=True).splitlines()
    selected = None
    for commit in commits:
        names = subprocess.check_output(['git', 'diff-tree', '--root', '--no-commit-id', '--name-only', '-r', '-z', '--diff-filter=AM', commit, '--', 'uploads'], text=True).split('\0')
        files = [Path(name) for name in names if name.lower().endswith('.csv') and Path(name).is_file()]
        if len(files) > 1:
            raise ValueError('Upload one CSV per commit so the latest report is unambiguous.')
        if files:
            selected = files[0]
            break
    if selected is None:
        print('No CSV uploaded yet; preserving current data.json.')
        return
    if selected.stat().st_size > 5 * 1024 * 1024:
        raise ValueError('CSV exceeds the 5 MB limit.')
    data = parse(selected.read_text(encoding='utf-8-sig'))
    old = json.loads(Path('data.json').read_text())
    if old.get('availability') == data and old.get('source') == selected.name:
        print('Availability is already current.')
        return
    payload = {'schemaVersion': 1, 'updatedAt': datetime.now(ZoneInfo('America/Denver')).isoformat(timespec='seconds'), 'source': selected.name, 'availability': data}
    Path('data.json').write_text(json.dumps(payload, indent=2) + '\n')
    print(f'Validated {len(data)} days from {selected.name}.')


if __name__ == '__main__':
    main()
