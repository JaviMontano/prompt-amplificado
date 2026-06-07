#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporta los 2026 prompts (+meta) a 12 JSON: idioma × formato.
  exports/{es,en,pt}/{natural,parametros,spec,dupla}.json  (12 archivos)
  exports/manifest.json
Cada archivo: {manifest, prompts:[{id,command,title,category,tags,format,content}]}
  content = string (natural/parametros/spec) | {system,user} (dupla)
Fuente por idioma: r.tri[lang].formats; fallback ES = formats top-level.
Escribe en AMBOS destinos (live + educativo). Determinista, sin generación."""
import json, os, datetime
HERE = os.path.dirname(__file__)
SRC  = os.path.join(HERE, '..', 'biblioteca-data.json')
DESTS = [
    os.path.join(HERE, '..', 'exports'),
    os.path.join(os.path.expanduser('~'), 'material-educativo-metodologia', 'exports'),
]
LANGS = ('es', 'en', 'pt')
# (archivo, clave en formats)
FORMATS = [('natural', 'natural'), ('parametros', 'natural_params'), ('spec', 'spec'), ('dupla', 'dupla')]

def lang_formats(r, lang):
    """Devuelve dict formats del idioma o None si no existe."""
    tri = r.get('tri') or {}
    blk = tri.get(lang)
    if blk and blk.get('formats'):
        return blk['formats']
    if lang == 'es':
        return r.get('formats') or None
    return None

def lang_title(r, lang):
    tri = r.get('tri') or {}
    blk = tri.get(lang)
    if blk and blk.get('title'):
        return blk['title']
    return r.get('title')

def content_of(formats, key):
    if key == 'dupla':
        du = formats.get('dupla') or {}
        if not isinstance(du, dict):
            du = {'system': '', 'user': str(du)}
        return {'system': du.get('system', '') or '', 'user': du.get('user', '') or ''}
    return formats.get(key, '') or ''

def nonempty(c):
    if isinstance(c, dict):
        return bool(c.get('system') or c.get('user'))
    return bool(c)

def main():
    data = json.load(open(SRC, encoding='utf-8'))
    today = datetime.date.today().isoformat()
    base_manifest = {
        'name': 'MetodologIA · Biblioteca de Prompts',
        'version': 'v-actual', 'generated': today,
        'license': 'CC BY-NC-SA 4.0', 'source': 'biblioteca-data.json',
        'attribution': 'Javier Montaño · MetodologIA',
    }
    # construir los 12 arrays
    bundles = {}   # (lang,fmtfile) -> list
    counts = {}
    for lang in LANGS:
        for fmtfile, key in FORMATS:
            arr = []
            for r in data:
                fmts = lang_formats(r, lang)
                if not fmts:
                    continue
                c = content_of(fmts, key)
                if not nonempty(c):
                    continue
                arr.append({
                    'id': r.get('id'), 'command': r.get('command'),
                    'title': lang_title(r, lang), 'category': r.get('category'),
                    'tags': r.get('tags', []), 'format': fmtfile, 'content': c,
                })
            bundles[(lang, fmtfile)] = arr
            counts['%s/%s' % (lang, fmtfile)] = len(arr)

    manifest = dict(base_manifest, total_records=len(data),
                    files=[f'{l}/{ff}.json' for l in LANGS for ff, _ in FORMATS],
                    counts=counts)

    for dest in DESTS:
        for lang in LANGS:
            os.makedirs(os.path.join(dest, lang), exist_ok=True)
            for fmtfile, key in FORMATS:
                arr = bundles[(lang, fmtfile)]
                payload = {'manifest': dict(base_manifest, language=lang, format=fmtfile, count=len(arr)),
                           'prompts': arr}
                json.dump(payload, open(os.path.join(dest, lang, fmtfile + '.json'), 'w', encoding='utf-8'),
                          ensure_ascii=False, separators=(',', ':'))
        json.dump(manifest, open(os.path.join(dest, 'manifest.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('escrito ->', dest)
    print('counts:', json.dumps(counts, indent=0))

if __name__ == '__main__':
    main()
