#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inserta/actualiza los 5 meta-prompts como registros del catálogo (cmd78+tri) en biblioteca-data.json.
Lee tools/meta.{es,en,pt}.json (campos planos por idioma)."""
import json, os, re
HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '..', 'biblioteca-data.json')
M = {l: json.load(open(os.path.join(HERE, 'meta.%s.json' % l), encoding='utf-8')) for l in ('es', 'en', 'pt')}
TAGS = {
 '/crear-natural': ['meta-prompting', 'crear', 'natural'],
 '/crear-parametros': ['meta-prompting', 'crear', 'parametros'],
 '/crear-spec': ['meta-prompting', 'crear', 'spec'],
 '/crear-dupla': ['meta-prompting', 'crear', 'dupla', 'agentic'],
 '/elegir-formato': ['meta-prompting', 'crear', 'maestro', 'selector'],
}
def slug(c): return 'meta_' + re.sub(r'[^a-z0-9]+', '_', c.lstrip('/').lower()).strip('_')
def langblock(f):
    return {"title": f['title'], "desc": f['desc'], "bondades": {},
            "formats": {"natural": f['natural'], "natural_params": f['parametros'], "spec": f['spec'],
                        "dupla": {"system": f['dupla_system'], "user": f['dupla_user']}}}
def main():
    data = json.load(open(DATA, encoding='utf-8'))
    bycmd = {r.get('command'): r for r in data}
    n = 0
    for cmd in M['es'].keys():
        tri = {l: langblock(M[l][cmd]) for l in ('es', 'en', 'pt') if cmd in M[l]}
        es = tri['es']
        rec = bycmd.get(cmd) or {}
        new = (rec.get('command') != cmd)
        rec.update({
            "id": rec.get('id') or slug(cmd), "command": cmd,
            "category": "Meta-Prompting", "subcategory": "Crear", "tags": TAGS.get(cmd, ['meta-prompting']),
            "q": 1.0, "cmd78": True, "params": [], "tri": tri,
            "title": es['title'], "desc": es['desc'], "formats": es['formats'],
        })
        if new: data.append(rec)
        n += 1
    json.dump(data, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print("meta records en catálogo:", n, "| total registros:", len(data))

if __name__ == '__main__':
    main()
