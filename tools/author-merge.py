#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mezcla los prompts re-autorados (/tmp/authored/<id>.json) en biblioteca-data.json.
Reemplaza title + formats (natural, natural_params, spec, dupla{system,user}) y setea tri.es;
BORRA tri.en/tri.pt (quedan obsoletas → re-traducir). Conserva id/command/category/subcategory/
tags/q/params/bondades/cmd78. Snapshot previo: biblioteca-data.json.pre-author. Idempotente."""
import json, os, html
HERE = os.path.dirname(__file__)
SRC  = os.path.join(HERE, '..', 'biblioteca-data.json')
AUTH = os.path.join(HERE, 'authoring', 'out')
SNAP = SRC + '.pre-author'

def clean(s): return html.unescape(s) if isinstance(s, str) else (s or '')

def main():
    data = json.load(open(SRC, encoding='utf-8'))
    if not os.path.exists(SNAP):
        json.dump(data, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        print('snapshot ->', SNAP)
    merged = 0; missing = []; bad = []
    for r in data:
        rid = r.get('id')
        fp = os.path.join(AUTH, '%s.json' % rid)
        if not os.path.exists(fp):
            if r.get('category') != 'Meta-Prompting': missing.append(rid)
            continue
        try:
            a = json.load(open(fp, encoding='utf-8'))
        except Exception as e:
            bad.append((rid, str(e))); continue
        need = ('spec', 'natural', 'parametros', 'dupla_system', 'dupla_user')
        if not all(a.get(k) for k in need):
            bad.append((rid, 'incompleto')); continue
        fmts = {
            'natural': clean(a.get('natural')),
            'natural_params': clean(a.get('parametros')),
            'spec': clean(a.get('spec')),
            'dupla': {'system': clean(a.get('dupla_system')), 'user': clean(a.get('dupla_user'))},
        }
        title = clean(a.get('title')) or r.get('title')
        r['title'] = title
        r['formats'] = fmts
        r['tri'] = {'es': {'title': title, 'desc': r.get('desc', ''), 'formats': fmts}}
        merged += 1
    json.dump(data, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('re-autorados:', merged, '| faltan:', len(missing), '| bad:', len(bad))
    if missing[:10]: print('  missing sample:', missing[:10])
    if bad[:10]: print('  bad sample:', bad[:10])

if __name__ == '__main__':
    main()
