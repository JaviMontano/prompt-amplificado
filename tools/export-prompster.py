#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera bundles Prompster-ready (dict plano {clave: texto}) desde biblioteca-data.json.
Formato Prompster verificado: { "<trigger>": "<cuerpo del prompt>" }.
Claves con prefijo de formato: ln-(natural) pr-(parametros) spec-(spec) dp-(dupla).
dupla → "SYSTEM:\\n…\\n\\nUSER:\\n…" en una sola entrada.

Salida (AMBOS destinos):
  exports/prompster/{es,en,pt}/{natural,parametros,spec,dupla}.json   (12)
  exports/prompster/prompster_{es,en,pt}.json                          (3, concatenado por idioma)
Determinista, sin generación."""
import json, os, html
HERE = os.path.dirname(__file__)
SRC  = os.path.join(HERE, '..', 'biblioteca-data.json')
DESTS = [
    os.path.join(HERE, '..', 'exports', 'prompster'),
    os.path.join(os.path.expanduser('~'), 'material-educativo-metodologia', 'exports', 'prompster'),
]
LANGS = ('es', 'en', 'pt')
# (archivo, clave_formats, prefijo)
FORMATS = [('natural', 'natural', 'ln'), ('parametros', 'natural_params', 'pr'),
           ('spec', 'spec', 'spec'), ('dupla', 'dupla', 'dp')]

def clean(s):
    return html.unescape(s) if isinstance(s, str) else (s or '')

def lang_formats(r, lang):
    tri = r.get('tri') or {}
    blk = tri.get(lang)
    if blk and blk.get('formats'):
        return blk['formats']
    return r.get('formats') or None

def value_for(fmts, key):
    if key == 'dupla':
        du = fmts.get('dupla') or {}
        if not isinstance(du, dict):
            du = {'system': '', 'user': str(du)}
        sysv, usr = clean(du.get('system')), clean(du.get('user'))
        if not (sysv or usr):
            return ''
        return 'SYSTEM:\n' + sysv + '\n\nUSER:\n' + usr
    return clean(fmts.get(key))

def main():
    data = json.load(open(SRC, encoding='utf-8'))
    # bundles[(lang, fmtfile)] = dict ; concat[lang] = dict
    bundles = {}
    concat = {l: {} for l in LANGS}
    counts = {}
    for lang in LANGS:
        for fmtfile, key, prefix in FORMATS:
            b = {}
            for r in data:
                rid = r.get('id')
                if not rid:
                    continue
                fmts = lang_formats(r, lang)
                if not fmts:
                    continue
                v = value_for(fmts, key)
                if not v:
                    continue
                ckey = prefix + '-' + rid
                b[ckey] = v
                concat[lang][ckey] = v
            bundles[(lang, fmtfile)] = b
            counts['%s/%s' % (lang, fmtfile)] = len(b)

    for dest in DESTS:
        for lang in LANGS:
            os.makedirs(os.path.join(dest, lang), exist_ok=True)
            for fmtfile, key, prefix in FORMATS:
                json.dump(bundles[(lang, fmtfile)],
                          open(os.path.join(dest, lang, fmtfile + '.json'), 'w', encoding='utf-8'),
                          ensure_ascii=False, separators=(',', ':'))
            json.dump(concat[lang],
                      open(os.path.join(dest, 'prompster_%s.json' % lang), 'w', encoding='utf-8'),
                      ensure_ascii=False, separators=(',', ':'))
        print('escrito ->', dest)
    print('counts (idioma/formato):', json.dumps(counts))
    print('concatenado:', {l: len(concat[l]) for l in LANGS})

if __name__ == '__main__':
    main()
