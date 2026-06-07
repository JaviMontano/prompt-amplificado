#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera slices de los prompts SIN traducción (sin tri.en) para traducir EN/PT.
Cada slice = tools/slices/part-NN.json = array de items planos:
  {id,title,desc,natural,parametros,spec,dupla_system,dupla_user}
Solo incluye campos no vacíos para acotar tokens. ~25 prompts por slice."""
import json, os
HERE = os.path.dirname(__file__)
SRC  = os.path.join(HERE, '..', 'biblioteca-data.json')
SLD  = os.path.join(HERE, 'slices')
SIZE = 5

def item(r):
    f = r.get('formats') or {}
    du = f.get('dupla') or {}
    if not isinstance(du, dict):
        du = {'system': '', 'user': str(du)}
    return {
        'id': r.get('id'),
        'title': r.get('title') or '',
        'desc': r.get('desc') or '',
        'natural': f.get('natural') or '',
        'parametros': f.get('natural_params') or '',
        'spec': f.get('spec') or '',
        'dupla_system': du.get('system') or '',
        'dupla_user': du.get('user') or '',
    }

def main():
    data = json.load(open(SRC, encoding='utf-8'))
    # untranslated = sin tri.en con formats
    todo = []
    for r in data:
        tri = r.get('tri') or {}
        en = (tri.get('en') or {}).get('formats') if tri.get('en') else None
        has_en = bool(en and (en.get('natural') or en.get('spec')))
        if not has_en:
            todo.append(r)
    os.makedirs(SLD, exist_ok=True)
    # limpiar slices viejos
    for fn in os.listdir(SLD):
        if fn.startswith('part-') and fn.endswith('.json'):
            os.remove(os.path.join(SLD, fn))
    n = 0
    for i in range(0, len(todo), SIZE):
        chunk = [item(r) for r in todo[i:i+SIZE]]
        fn = os.path.join(SLD, 'part-%03d.json' % n)
        json.dump(chunk, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        n += 1
    print('untranslated:', len(todo), '| slices:', n, '| size:', SIZE)
    print('dir:', SLD)

if __name__ == '__main__':
    main()
