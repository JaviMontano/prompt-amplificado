#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mergea las traducciones EN/PT (tools/xl-out-*.json) en biblioteca-data.json (r.tri[lang]).
Des-escapa entidades HTML que algún agente pudo introducir. Idempotente por (command,lang)."""
import json, os, glob, html, re
HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '..', 'biblioteca-data.json')

def block(f):
    u = lambda k: html.unescape(f.get(k, '') or '')
    return {
        "title": u('title'), "desc": u('desc'),
        "bondades": {"how_to_use": u('how_to_use'), "importance": u('importance'),
                     "common_errors": u('common_errors'), "exercise": u('exercise'), "example": u('example')},
        "formats": {"natural": u('natural'), "natural_params": u('parametros'), "spec": u('spec'),
                    "dupla": {"system": u('dupla_system'), "user": u('dupla_user')}}
    }

def main():
    data = json.load(open(DATA, encoding='utf-8'))
    bycmd = {r.get('command'): r for r in data}
    files = sorted(glob.glob(os.path.join(HERE, 'xl-out-*.json')))
    n, miss, bad = 0, [], []
    for fp in files:
        for u in json.load(open(fp, encoding='utf-8')):
            r = bycmd.get(u['command'])
            if not r or 'tri' not in r:
                miss.append(u.get('command')); continue
            blk = block(u['fields'])
            # sanity: spec presente y con cláusulas
            if '[' not in blk['formats']['spec'] or len(blk['formats']['spec']) < 800:
                bad.append((u['command'], u['lang'], 'spec-corto'))
            r['tri'][u['lang']] = blk
            n += 1
    json.dump(data, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    # cobertura
    cov = {'es': 0, 'en': 0, 'pt': 0}
    for r in data:
        if r.get('tri'):
            for l in cov:
                if r['tri'].get(l): cov[l] += 1
    print("merged units:", n, "| files:", len(files))
    print("cobertura tri:", cov)
    if miss: print("sin match:", miss[:10])
    if bad: print("sospechosos:", bad[:10])

if __name__ == '__main__':
    main()
