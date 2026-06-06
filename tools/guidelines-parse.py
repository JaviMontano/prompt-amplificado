#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parsea guidelines/*.md → tools/guidelines.es.json estructurado."""
import json, os, re, glob
HERE = os.path.dirname(__file__)
GDIR = os.path.join(HERE, '..', 'guidelines')
SECMAP = {
    'guidelines': 'guidelines', 'guardrails': 'guardrails', 'workflow': 'workflow',
    'criterios de aceptación': 'acceptance', 'definition of done': 'dod',
}
DOCKEY = {'00-general': 'general', 'natural': 'natural', 'parametros': 'parametros', 'spec': 'spec', 'dupla': 'dupla'}
ORDER = ['general', 'natural', 'parametros', 'spec', 'dupla']

def parse(md):
    title, intro = '', ''
    secs = {'guidelines': [], 'guardrails': [], 'workflow': [], 'acceptance': [], 'dod': []}
    cur = None
    for ln in md.split('\n'):
        s = ln.rstrip()
        if s.startswith('# '): title = s[2:].strip()
        elif s.startswith('> '): intro = s[2:].strip()
        elif s.startswith('## '):
            cur = SECMAP.get(s[3:].strip().lower())
        elif cur and (s.lstrip().startswith('- ') or re.match(r'^\d+\.\s', s.lstrip())):
            item = re.sub(r'^\s*(?:-\s|\d+\.\s)', '', s).strip()
            secs[cur].append(item)
    return {'title': title, 'intro': intro, **secs}

def main():
    out = {}
    for fp in glob.glob(os.path.join(GDIR, '*.md')):
        key = DOCKEY.get(os.path.basename(fp)[:-3])
        if not key: continue
        out[key] = parse(open(fp, encoding='utf-8').read())
    out = {k: out[k] for k in ORDER if k in out}
    json.dump(out, open(os.path.join(HERE, 'guidelines.es.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for k, v in out.items():
        print(k, '|', v['title'][:40], '| g%d gr%d w%d a%d dod%d' % (
            len(v['guidelines']), len(v['guardrails']), len(v['workflow']), len(v['acceptance']), len(v['dod'])))

if __name__ == '__main__':
    main()
