#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chequea fidelidad de longitud de las traducciones part-NNN.json vs el slice ES.
Marca (slice,lang) que necesitan REDO: algún campo con ES>1200 chars y traducción <45%.
No requiere merge. Imprime listas redo por idioma y guarda tools/redo.json."""
import json, os, glob
HERE = os.path.dirname(__file__)
SL = sorted(glob.glob(os.path.join(HERE, 'slices', 'part-*.json')))
FIELDS = ('natural', 'parametros', 'spec')

def load(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return None

def main():
    redo = {'en': [], 'pt': []}
    for s in SL:
        n = os.path.basename(s)
        es = load(s)
        for lang in ('en', 'pt'):
            tr = load(os.path.join(HERE, 'parts', lang, n))
            if tr is None or not isinstance(tr, list) or len(tr) != len(es):
                redo[lang].append(n); continue
            bad = False
            for i in range(len(es)):
                for k in FIELDS:
                    el = len(es[i].get(k) or ''); tl = len(tr[i].get(k) or '')
                    if el > 1200 and tl < el * 0.45:
                        bad = True; break
                if bad: break
            if bad: redo[lang].append(n)
    json.dump(redo, open(os.path.join(HERE, 'redo.json'), 'w'), ensure_ascii=False)
    print('redo EN:', len(redo['en']), '| redo PT:', len(redo['pt']))
    print('EN:', redo['en'][:50])
    print('PT:', redo['pt'][:50])

if __name__ == '__main__':
    main()
