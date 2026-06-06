#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hace que la versión 'natural' (y desc) DEMUESTREN el comportamiento (macro imperativa operativa),
en vez de describirlo. Fuente: seeds operativos de robustecer-comandos.py (render con defaults).
Solo ES aquí; EN/PT se re-traducen después. SPEC/parámetros/dupla (ricos de v3000) se conservan.
"""
import json, os, importlib.util
HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '..', 'biblioteca-data.json')
PROTO = ">> Protocolo MetodologIA: Interpreta > Planifica > Ejecuta. Reformula lo que entiendes y presenta tu plan antes de ejecutar."

spec = importlib.util.spec_from_file_location('rob', os.path.join(HERE, 'robustecer-comandos.py'))
rob = importlib.util.module_from_spec(spec); spec.loader.exec_module(rob)

def op_text(cmd):
    e = rob.S.get(cmd)
    if not e: return None, None
    title, desc, body, params = e
    natural = rob.render(body, params) + "\n\n" + PROTO   # imperativa, defaults aplicados
    return natural, desc

def main():
    data = json.load(open(DATA, encoding='utf-8'))
    n, miss = 0, []
    for r in data:
        if not r.get('cmd78'): continue
        nat, desc = op_text(r['command'])
        if nat is None: miss.append(r['command']); continue
        es = r['tri']['es']
        es['formats']['natural'] = nat
        es['desc'] = desc
        r['formats']['natural'] = nat
        r['desc'] = desc
        n += 1
    json.dump(data, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print("ES natural+desc operativos:", n)
    if miss: print("sin seed:", miss)
    # muestra
    B = {x.get('command'): x for x in data}
    for c in ['/a', '/b', '/e', '/z']:
        print(c, "→", B[c]['tri']['es']['formats']['natural'].split(chr(10))[0][:80])

if __name__ == '__main__':
    main()
