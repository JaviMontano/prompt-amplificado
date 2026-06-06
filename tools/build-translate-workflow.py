#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera workflows de traducción EN/PT por batch (script ≤512KB · unidades comando×idioma · schema plano).
Uso: python3 build-translate-workflow.py <batch_index> <batch_size>
Escribe tools/xl-tr-<index>.js. Lanza con Workflow({scriptPath}).
"""
import json, os, sys, math
HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '..', 'biblioteca-data.json')

def units():
    d = json.load(open(DATA, encoding='utf-8'))
    out = []
    for r in d:
        if not r.get('cmd78'): continue
        es = r['tri']['es']; f = es['formats']; b = es['bondades']
        out.append({
            "command": r['command'],
            "title": es['title'], "desc": es['desc'],
            "natural": f['natural'], "parametros": f['natural_params'],
            "spec": f['spec'], "dupla_system": f['dupla']['system'], "dupla_user": f['dupla']['user'],
            "how_to_use": b.get('how_to_use', ''), "importance": b.get('importance', ''),
            "common_errors": b.get('common_errors', ''), "exercise": b.get('exercise', ''),
            "example": b.get('example', '')
        })
    return out

TPL = r'''export const meta = {
  name: 'translate-batch-__IDX__',
  description: 'Traducción EN/PT · batch __IDX__ (__N__ comandos × 2 idiomas)',
  phases: [{ title: 'Translate', detail: 'comando × idioma · schema plano' }]
}
const SEED = __SEED__;
const LANG = { en: 'English (professional, native)', pt: 'português (profissional, nativo do Brasil)' };
const FIELDS = ['title','desc','natural','parametros','spec','dupla_system','dupla_user','how_to_use','importance','common_errors','exercise','example'];
const SCHEMA = { type:'object', additionalProperties:false, required:FIELDS,
  properties: FIELDS.reduce((o,k)=>{o[k]={type:'string'};return o;}, {}) };
function prompt(u, lang){
  return [
    'Traduce fielmente del español a ' + LANG[lang] + ' los campos de este prompt de MetodologIA. Traducción profesional, natural y completa.',
    'REGLAS DURAS:',
    '- Preserva la ESTRUCTURA y los saltos de línea de cada campo.',
    '- Puedes localizar los rótulos de sección (p.ej. ROL→ROLE, SITUACIÓN→SITUATION, EJECUCIÓN→EXECUTION, SALIDA→OUTPUT) para que suene nativo.',
    '- MANTÉN VERBATIM (sin traducir): etiquetas de procedencia entre llaves ({SUPUESTO} {INFERENCIA} {ADJUNTO} {EXTRAIDO_HILO} {MEMORIA} {CONOCIMIENTO} {WEB} {AUTOCOMPLETADO} {POR_CONFIRMAR} {VACIO_CRITICO}); cabeceras de cláusula entre corchetes [ ... ] y sus params; tokens de input como {[ITEMS]}; nombres de comando (/prioriza, /0, /a); cifras, umbrales (0.95, 0.85) y la marca MetodologIA.',
    '- NADA de comentarios ni metadiscurso. Devuelve solo los campos traducidos, uno a uno, con el mismo significado.',
    'CAMPOS (español):',
    JSON.stringify(u, null, 0)
  ].join('\n');
}
const tasks = [];
for (const u of SEED) for (const lang of ['en','pt']) {
  tasks.push(() => agent(prompt(u, lang), { label: 'tr:'+u.command+':'+lang, phase:'Translate', schema: SCHEMA })
    .then(r => r ? { command: u.command, lang, fields: r } : null));
}
const res = await parallel(tasks);
const ok = res.filter(Boolean);
log('traducidos ' + ok.length + '/' + tasks.length);
return ok;
'''

def main():
    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    U = units()
    json.dump(U, open(os.path.join(HERE, 'xl-es.json'), 'w'), ensure_ascii=False)
    batch = U[idx*size:(idx+1)*size]
    js = TPL.replace('__IDX__', str(idx)).replace('__N__', str(len(batch))).replace('__SEED__', json.dumps(batch, ensure_ascii=False))
    p = os.path.join(HERE, 'xl-tr-%d.js' % idx)
    open(p, 'w', encoding='utf-8').write(js)
    nb = math.ceil(len(U)/size)
    print("total units:", len(U), "| batches:", nb, "| this batch:", len(batch), "| commands:", [u['command'] for u in batch])
    print("script:", p, "size KB:", round(os.path.getsize(p)/1024))

if __name__ == '__main__':
    main()
