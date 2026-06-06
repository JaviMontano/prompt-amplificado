#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mergea traducciones de natural+desc (tools/xl-nd-out*.json) en tri[en|pt]. Des-escapa HTML."""
import json, os, glob, html
HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '..', 'biblioteca-data.json')

def main():
    data = json.load(open(DATA, encoding='utf-8'))
    bycmd = {r.get('command'): r for r in data}
    n = 0
    for fp in sorted(glob.glob(os.path.join(HERE, 'xl-nd-out*.json'))):
        for u in json.load(open(fp, encoding='utf-8')):
            r = bycmd.get(u['command']); lang = u['lang']
            if not r or 'tri' not in r or lang not in r['tri']:
                continue
            f = u['fields']
            r['tri'][lang]['formats']['natural'] = html.unescape(f.get('natural', ''))
            r['tri'][lang]['desc'] = html.unescape(f.get('desc', ''))
            n += 1
    json.dump(data, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print("natdesc merged:", n)

if __name__ == '__main__':
    main()
