#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mergea la salida del Workflow de Excelencia (tools/excellence-output.json) en biblioteca-data.json.
Modelo: r.tri = {es,en,pt}, cada uno {title,desc,crit,edge,formats{natural,natural_params,spec,dupla{system,user}},paramLabels,optLabels}.
Top-level (title/desc/crit/edge/formats) = tri.es para back-compat (cards/búsqueda).
params (keys/opts) quedan ESTABLES. Snapshot previo en .pre-xl (ya creado por el flujo)."""
import json, os, sys
HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '..', 'biblioteca-data.json')
OUT = os.path.join(HERE, 'excellence-output.json')

def langblock(L):
    return {
        "title": L["title"], "desc": L["desc"], "crit": L["crit"], "edge": L["edge"],
        "formats": {
            "natural": L["natural"], "natural_params": L["parametros"], "spec": L["spec"],
            "dupla": {"system": L["dupla_system"], "user": L["dupla_user"]}
        },
        "paramLabels": L.get("paramLabels", {}), "optLabels": L.get("optLabels", {})
    }

def main():
    units = json.load(open(OUT, encoding='utf-8'))
    data = json.load(open(DATA, encoding='utf-8'))
    bycmd = {r.get('command'): r for r in data}
    n, miss = 0, []
    for u in units:
        cmd = u.get('command'); r = bycmd.get(cmd)
        if not r or 'tri' not in u:
            miss.append(cmd); continue
        tri = {lang: langblock(u['tri'][lang]) for lang in ('es', 'en', 'pt') if lang in u['tri']}
        r['tri'] = tri
        es = tri.get('es')
        if es:
            r['title'] = es['title']; r['desc'] = es['desc']
            r['crit'] = es['crit']; r['edge'] = es['edge']
            r['formats'] = es['formats']
        n += 1
    if not os.path.exists(DATA + '.pre-xl'):
        import shutil; shutil.copy(DATA, DATA + '.pre-xl')
    json.dump(data, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print("merge: %d/%d comandos con tri{es,en,pt}" % (n, len(units)))
    if miss: print("sin match:", miss)
    # validaciones rápidas
    bad = []
    for r in data:
        if not r.get('tri'): continue
        for lang, L in r['tri'].items():
            blob = json.dumps(L, ensure_ascii=False)
            if '[[' in blob or '{{' in blob: bad.append((r['command'], lang, 'token'))
            for k in ('natural', 'natural_params', 'spec'):
                if 'Protocolo' not in L['formats'][k] and 'Protocol' not in L['formats'][k]:
                    bad.append((r['command'], lang, 'no-proto:' + k))
    print("validación: problemas =", len(bad))
    for b in bad[:15]: print("  ", b)

if __name__ == '__main__':
    main()
