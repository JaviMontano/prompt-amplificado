#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mezcla traducciones EN/PT de los prompts BASE (tools/parts/{en,pt}/part-NNN.json, keyed by id)
en biblioteca-data.json. Para cada prompt sin tri.en completo construye tri={es,en,pt}:
  es    = desde formats top-level (ES, intacto)
  en/pt = desde las partes traducidas (por id)
html.unescape; valida (4 formatos no vacíos, sin tokens [[/{{, longitud coherente).
Snapshot previo: biblioteca-data.json.pre-tri . Idempotente."""
import json, os, html, re
HERE = os.path.dirname(__file__)
SRC  = os.path.join(HERE, '..', 'biblioteca-data.json')
PARTS = os.path.join(HERE, 'parts')
SNAP = SRC + '.pre-tri'
LANGS = ('en', 'pt')

def load_parts(lang):
    d = os.path.join(PARTS, lang); out = {}
    if not os.path.isdir(d): return out
    for fn in sorted(os.listdir(d)):
        if not (fn.startswith('part-') and fn.endswith('.json')): continue
        try:
            arr = json.load(open(os.path.join(d, fn), encoding='utf-8'))
        except Exception as e:
            print('  ! parse fail', lang, fn, e); continue
        if isinstance(arr, dict) and 'items' in arr: arr = arr['items']
        for it in arr:
            if isinstance(it, dict) and it.get('id'): out[it['id']] = it
    return out

def clean(s): return html.unescape(s) if isinstance(s, str) else (s or '')

def fmt_block(d):
    return {'title': clean(d.get('title')), 'desc': clean(d.get('desc')),
            'formats': {'natural': clean(d.get('natural')), 'natural_params': clean(d.get('parametros')),
                        'spec': clean(d.get('spec')),
                        'dupla': {'system': clean(d.get('dupla_system')), 'user': clean(d.get('dupla_user'))}}}

def es_from_record(r):
    f = r.get('formats') or {}; du = f.get('dupla') or {}
    if not isinstance(du, dict): du = {'system': '', 'user': str(du)}
    return {'title': r.get('title') or '', 'desc': r.get('desc') or '',
            'formats': {'natural': f.get('natural') or '', 'natural_params': f.get('natural_params') or '',
                        'spec': f.get('spec') or '',
                        'dupla': {'system': du.get('system') or '', 'user': du.get('user') or ''}}}

TOKEN = re.compile(r'\[\[|\]\]|\{\{|\}\}')

def issues(es, tr, rid, lang):
    out = []; ef, tf = es['formats'], tr['formats']
    for k in ('natural', 'natural_params', 'spec'):
        if ef.get(k) and not tf.get(k): out.append('%s/%s/%s vacío' % (rid, lang, k))
        if TOKEN.search(tf.get(k) or ''): out.append('%s/%s/%s token' % (rid, lang, k))
        el, tl = len(ef.get(k) or ''), len(tf.get(k) or '')
        if el > 200 and tl and (tl < el*0.25 or tl > el*3.2):
            out.append('%s/%s/%s long %d vs %d' % (rid, lang, k, tl, el))
    return out

def main():
    data = json.load(open(SRC, encoding='utf-8'))
    if not os.path.exists(SNAP):
        json.dump(data, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        print('snapshot ->', SNAP)
    parts = {l: load_parts(l) for l in LANGS}
    print('partes: en=%d pt=%d' % (len(parts['en']), len(parts['pt'])))
    merged = 0; missing = {l: 0 for l in LANGS}; probs = []
    for r in data:
        rid = r.get('id'); tri = r.get('tri') or {}
        if (tri.get('en') or {}).get('formats', {}).get('spec'):
            continue  # ya traducido
        es = es_from_record(r); new = {'es': es}; ok = True
        for l in LANGS:
            it = parts[l].get(rid)
            if not it: missing[l] += 1; ok = False; continue
            blk = fmt_block(it); probs += issues(es, blk, rid, l); new[l] = blk
        if ok:
            r['tri'] = new; merged += 1
    json.dump(data, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('merged tri:', merged, '| missing en=%d pt=%d' % (missing['en'], missing['pt']))
    if probs:
        print('AVISOS (%d):' % len(probs))
        for p in probs[:30]: print('  -', p)
    cov = {'es': 0, 'en': 0, 'pt': 0}
    for r in data:
        for l in cov:
            tspec = (r.get('tri') or {}).get(l, {}).get('formats', {}).get('spec')
            if tspec or (l == 'es' and (r.get('formats') or {}).get('spec')): cov[l] += 1
    print('cobertura spec: es=%d en=%d pt=%d / %d' % (cov['es'], cov['en'], cov['pt'], len(data)))

if __name__ == '__main__':
    main()
