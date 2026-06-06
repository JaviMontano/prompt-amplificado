#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye workflows de REINTENTO solo para los pares (comando,idioma) faltantes en tri.
Chunks ≤ ~380KB para correr SECUENCIAL (evita saturación). Escribe tools/xl-retry-<k>.js."""
import json, os
HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '..', 'biblioteca-data.json')
ES = json.load(open(os.path.join(HERE, 'xl-es.json'), encoding='utf-8'))
esByCmd = {u['command']: u for u in ES}
data = json.load(open(DATA, encoding='utf-8'))

missing = []  # (command, lang)
for r in data:
    if not r.get('cmd78'): continue
    tri = r.get('tri', {})
    for lang in ('en', 'pt'):
        if not tri.get(lang):
            missing.append((r['command'], lang))
print("faltantes:", len(missing))

# chunk por tamaño de ES embebido (por comando único en el chunk)
THRESH = 360_000
chunks = []
cur, cur_cmds, cur_size = [], set(), 0
for cmd, lang in missing:
    add = 0 if cmd in cur_cmds else len(json.dumps(esByCmd[cmd], ensure_ascii=False))
    if cur and cur_size + add > THRESH:
        chunks.append(cur); cur, cur_cmds, cur_size = [], set(), 0
    cur.append((cmd, lang)); cur_cmds.add(cmd); cur_size += add
if cur: chunks.append(cur)
print("chunks:", len(chunks), "| sizes(pairs):", [len(c) for c in chunks])

TPL = r'''export const meta = {
  name: 'retry-__K__',
  description: 'Reintento EN/PT · __N__ pares faltantes',
  phases: [{ title: 'Translate' }]
}
const UNITS = __UNITS__;   // {command: esUnit}
const PAIRS = __PAIRS__;   // [[command,lang],...]
const LANG = { en: 'English (professional, native)', pt: 'português (profissional, nativo do Brasil)' };
const FIELDS = ['title','desc','natural','parametros','spec','dupla_system','dupla_user','how_to_use','importance','common_errors','exercise','example'];
const SCHEMA = { type:'object', additionalProperties:false, required:FIELDS, properties:FIELDS.reduce((o,k)=>{o[k]={type:'string'};return o;},{}) };
function prompt(u, lang){
  return [
    'Traduce fielmente del español a ' + LANG[lang] + ' los campos de este prompt de MetodologIA. Traducción profesional, natural y completa.',
    'REGLAS DURAS:',
    '- Preserva la ESTRUCTURA y saltos de línea.',
    '- Puedes localizar rótulos de sección (ROL→ROLE, SITUACIÓN→SITUATION, EJECUCIÓN→EXECUTION, SALIDA→OUTPUT).',
    '- MANTÉN VERBATIM: etiquetas {SUPUESTO}{INFERENCIA}{ADJUNTO}... ; cabeceras de cláusula [ ... ] y sus params; tokens {[ITEMS]}; nombres de comando (/0,/a,/prioriza); cifras y umbrales (0.95,0.85); marca MetodologIA.',
    '- Sin comentarios ni metadiscurso. Devuelve solo los campos traducidos.',
    'CAMPOS (español):', JSON.stringify(u, null, 0)
  ].join('\n');
}
const tasks = PAIRS.map(([cmd,lang]) => () =>
  agent(prompt(UNITS[cmd], lang), { label:'rt:'+cmd+':'+lang, phase:'Translate', schema:SCHEMA })
    .then(r => r ? { command:cmd, lang, fields:r } : null));
const res = await parallel(tasks);
const ok = res.filter(Boolean);
log('reintento ' + ok.length + '/' + tasks.length);
return ok;
'''

for k, ch in enumerate(chunks):
    cmds = {c for c, _ in ch}
    units = {c: esByCmd[c] for c in cmds}
    js = (TPL.replace('__K__', str(k)).replace('__N__', str(len(ch)))
            .replace('__UNITS__', json.dumps(units, ensure_ascii=False))
            .replace('__PAIRS__', json.dumps(ch, ensure_ascii=False)))
    p = os.path.join(HERE, 'xl-retry-%d.js' % k)
    open(p, 'w', encoding='utf-8').write(js)
    print("  xl-retry-%d.js" % k, "KB", round(os.path.getsize(p)/1024), "pairs", len(ch))
