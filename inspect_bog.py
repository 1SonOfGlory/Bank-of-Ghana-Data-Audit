"""Profile Bank of Ghana CSV exports without changing their observations."""
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

REQUIRED = {'Mnemonic', 'Parent Mnemonic', 'Name of Series', 'Data Family', 'Units of Measure'}


def profile_csv(path: Path) -> list[dict]:
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        missing = REQUIRED.difference(fields)
        if missing or len(fields) <= 9:
            raise ValueError(f'{path.name}: expected nine metadata columns followed by periods; missing {sorted(missing)}')
        dates = fields[9:]
        rows = list(reader)
    result = []
    for row in rows:
        values, invalid = {}, []
        for date in dates:
            raw = (row.get(date) or '').strip()
            if not raw:
                continue
            try:
                value = float(raw.replace(',', ''))
                if not math.isfinite(value):
                    raise ValueError('Non-finite observation')
                values[date] = value
            except ValueError:
                invalid.append((date, raw))
        result.append({
            'id': row['Mnemonic'], 'parent': row['Parent Mnemonic'],
            'name': row['Name of Series'], 'family': row['Data Family'],
            'unit': row['Units of Measure'], 'n': len(values),
            'first': next(iter(values), None), 'last': next(reversed(values), None),
            'zeros': sum(value == 0 for value in values.values()),
            'bad': invalid, 'values': values,
        })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for frequency in ('annual', 'monthly', 'quarterly'):
        parser.add_argument('--' + frequency, required=True, type=Path)
    parser.add_argument('--output', type=Path, default=Path('bog_profile.json'))
    args = parser.parse_args()
    profiles = {}
    for frequency in ('annual', 'monthly', 'quarterly'):
        rows = profile_csv(getattr(args, frequency))
        profiles[frequency] = rows
        ids = Counter(row['id'] for row in rows)
        print(f'{frequency}: {len(rows)} series; {sum(row["n"] == 0 for row in rows)} empty; '
              f'{sum(n - 1 for n in ids.values())} duplicate identifiers')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(profiles, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
