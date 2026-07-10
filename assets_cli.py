#!/usr/bin/env python3
"""CLI sederhana untuk mengelola ASSETS.csv dan menambah transaksi ke VIRTUAL-MONEY.md

Usage examples:
  python assets_cli.py list-assets
  python assets_cli.py add-asset --name "Rekening Pribadi" --service gembe.x1 --account 08123 --balance 100000
  python assets_cli.py update-balance --id 1 --balance 120000
  python assets_cli.py add-transaction --service gembe.x1 --type Top-up --amount 100000 --note "Top-up bank" --balance_after 200000

This script uses only Python stdlib (csv, argparse).
"""

import argparse
import csv
import os
from datetime import datetime

ASSETS_FILE = 'ASSETS.csv'
VIRTUAL_MD = 'VIRTUAL-MONEY.md'


def ensure_assets_file():
    if not os.path.exists(ASSETS_FILE):
        with open(ASSETS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id','name','service','account_id','balance','currency','source','notes','last_updated','status_transaksi'])


def list_assets():
    ensure_assets_file()
    with open(ASSETS_FILE, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            print('No assets found.')
            return
        widths = {h: max(len(h), *(len(r[h]) for r in rows)) for h in reader.fieldnames}
        hdr = ' | '.join(h.ljust(widths[h]) for h in reader.fieldnames)
        print(hdr)
        print('-' * len(hdr))
        for r in rows:
            print(' | '.join(r[h].ljust(widths[h]) for h in reader.fieldnames))


def add_asset(args):
    ensure_assets_file()
    with open(ASSETS_FILE, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    next_id = 1
    if rows:
        next_id = max(int(r['id']) for r in rows) + 1
    now = datetime.now().strftime('%Y-%m-%d')
    new = {
        'id': str(next_id),
        'name': args.name,
        'service': args.service,
        'account_id': args.account,
        'balance': str(args.balance),
        'currency': args.currency or 'IDR',
        'source': args.source or '',
        'notes': args.notes or '',
        'last_updated': now,
        'status_transaksi': args.status or 'active'
    }
    with open(ASSETS_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new.keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(new)
    print('Asset added with id', next_id)


def update_balance(args):
    ensure_assets_file()
    updated = False
    with open(ASSETS_FILE, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for r in rows:
        if r['id'] == str(args.id):
            r['balance'] = str(args.balance)
            r['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            updated = True
    if not updated:
        print('Asset id not found')
        return
    with open(ASSETS_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print('Balance updated for id', args.id)


def add_transaction(args):
    # prepare row
    date = args.date or datetime.now().strftime('%Y-%m-%d')
    row = f"| {date} | {args.service} | {args.type} | {args.amount} | {args.note or ''} | {args.balance_after or ''} |\n"
    if not os.path.exists(VIRTUAL_MD):
        print('VIRTUAL-MONEY.md not found in current directory.')
        return
    with open(VIRTUAL_MD, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # find Riwayat Transaksi table header
    header = '| Tanggal | Aplikasi | Jenis | Jumlah | Keterangan | Saldo Setelah |'
    if header not in ''.join(lines):
        # append new section
        lines.append('\n## 4. Riwayat Transaksi\n')
        lines.append(header + '\n')
        lines.append('| --- | --- | --- | --- | --- | --- |\n')
        lines.append(row)
    else:
        # find start index of header line
        idx = next(i for i,l in enumerate(lines) if header in l)
        # find next section start (line starting with '## ' after idx)
        end_idx = None
        for j in range(idx+1, len(lines)):
            if lines[j].startswith('## '):
                end_idx = j
                break
        if end_idx is None:
            # append at end
            lines.append(row)
        else:
            # insert before end_idx
            lines.insert(end_idx, row)
    with open(VIRTUAL_MD, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('Transaction added to VIRTUAL-MONEY.md')


def parse_args():
    p = argparse.ArgumentParser(description='Manage personal virtual assets (CSV) and add transactions')
    sub = p.add_subparsers(dest='cmd')

    sub.add_parser('list-assets')

    pa = sub.add_parser('add-asset')
    pa.add_argument('--name', required=True)
    pa.add_argument('--service', required=True)
    pa.add_argument('--account', required=True)
    pa.add_argument('--balance', type=float, default=0)
    pa.add_argument('--currency', default='IDR')
    pa.add_argument('--source', default='')
    pa.add_argument('--notes', default='')
    pa.add_argument('--status', default='active')

    pu = sub.add_parser('update-balance')
    pu.add_argument('--id', required=True)
    pu.add_argument('--balance', required=True, type=float)

    pt = sub.add_parser('add-transaction')
    pt.add_argument('--date', help='YYYY-MM-DD')
    pt.add_argument('--service', required=True)
    pt.add_argument('--type', required=True)
    pt.add_argument('--amount', required=True)
    pt.add_argument('--note', default='')
    pt.add_argument('--balance_after', default='')

    return p.parse_args()


def main():
    args = parse_args()
    if args.cmd == 'list-assets':
        list_assets()
    elif args.cmd == 'add-asset':
        add_asset(args)
    elif args.cmd == 'update-balance':
        update_balance(args)
    elif args.cmd == 'add-transaction':
        add_transaction(args)
    else:
        print('No command. Use -h for help')


if __name__ == '__main__':
    main()
