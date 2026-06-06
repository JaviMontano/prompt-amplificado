#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera tools/xl-workflow.js (workflow de Bucle de Excelencia trilingüe) con el SEED embebido."""
import json, os
HERE = os.path.dirname(__file__)
seed = json.load(open(os.path.join(HERE, 'xl-seed.json'), encoding='utf-8'))
SEED_JS = json.dumps(seed, ensure_ascii=False)

JS = r'''export const meta = {
  name: 'excellence-78-trilingue',
  description: 'Bucle de Excelencia 10/10 · 78 comandos × 4 versiones × ES/EN/PT',
  phases: [{ title: 'Refine', detail: '1 agente por comando: 4 versiones trilingües a 10/10' },
           { title: 'Verify', detail: 'auditoría por rúbrica + restricciones; 1 reparación' }]
}
const SEED = __SEED__;

const PROTO = {
  es: '>> Protocolo MetodologIA: Interpreta > Planifica > Ejecuta. Reformula lo que entiendes y presenta tu plan antes de ejecutar.',
  en: '>> MetodologIA Protocol: Interpret > Plan > Execute. Restate what you understood and present your plan before executing.',
  pt: '>> Protocolo MetodologIA: Interpreta > Planeja > Executa. Reformule o que entendeu e apresente seu plano antes de executar.'
};
const LANGNAME = { es: 'español (neutro, registro profesional)', en: 'English (professional)', pt: 'português (profissional)' };

const RUBRIC = [
 '1. Fundamento: toda afirmación con base o marcada como supuesto.',
 '2. Veracidad: nada inventado; sin promesas exageradas.',
 '3. Calidad: anatomía de prompt sólida (rol/tarea/formato/criterio).',
 '4. Densidad: cero relleno; no se puede borrar nada sin pérdida.',
 '5. Simplicidad: lo más simple que funcione (respeta los topes de longitud).',
 '6. Claridad: comprensible en una lectura; sin ambigüedad.',
 '7. Precisión: términos exactos; criterios/números concretos (nada de "mejor/óptimo" sin definir).',
 '8. Profundidad: cubre lo esencial + criterio de aceptación + límite/caso borde útiles.',
 '9. Coherencia: las 4 versiones alineadas entre sí y con título/desc; ES/EN/PT equivalentes en intención.',
 '10. Valor: utilidad práctica directa; usable tal cual con los defaults.'
].join('\n');

const CONSTR = [
 '- Parámetros = valores por defecto ESCRITOS EN EL TEXTO (el usuario los ajusta editando). PROHIBIDO usar inputs vacíos tipo {{...}} o tokens [[...]].',
 '- Mantén ESTABLES las claves (key) y los valores (value) de los parámetros del seed; solo traduce/pule sus etiquetas visibles (paramLabels y optLabels).',
 '- Las 4 versiones son autónomas y cada una TERMINA con la línea de Protocolo del idioma (te la doy literal; no la alteres).',
 '- Formas: natural = prosa lista para pegar; parametros = bloque con líneas "· Etiqueta: valor"; spec = bloque [S]/[P]/[E]/[C]; dupla = par system/user.',
 '- Teje Criterio de aceptación y Límite/caso borde en cada versión (en natural/parametros como líneas "Criterio:"/"Evita:"; en spec dentro de [E]/[C]; en dupla el límite como guardrail del system y el criterio al final del user).',
 '- Voz MetodologIA: directa, sobria, profesional. SIN metadiscurso, SIN explicar tu proceso, SIN comillas envolventes.',
 '- Topes de longitud por versión: natural ≤110 palabras · parametros ≤170 · spec ≤150 · dupla_system ≤60 · dupla_user ≤110.'
].join('\n');

const LANGOBJ = {
  type: 'object', additionalProperties: false,
  required: ['title','desc','crit','edge','natural','parametros','spec','dupla_system','dupla_user','paramLabels','optLabels'],
  properties: {
    title: { type: 'string' }, desc: { type: 'string' }, crit: { type: 'string' }, edge: { type: 'string' },
    natural: { type: 'string' }, parametros: { type: 'string' }, spec: { type: 'string' },
    dupla_system: { type: 'string' }, dupla_user: { type: 'string' },
    paramLabels: { type: 'object', additionalProperties: { type: 'string' } },
    optLabels: { type: 'object', additionalProperties: { type: 'object', additionalProperties: { type: 'string' } } }
  }
};
const SCHEMA = { type: 'object', additionalProperties: false, required: ['command','tri'],
  properties: { command: { type: 'string' },
    tri: { type: 'object', additionalProperties: false, required: ['es','en','pt'],
      properties: { es: LANGOBJ, en: LANGOBJ, pt: LANGOBJ } } } };
const VERDICT = { type: 'object', additionalProperties: false, required: ['pass','issues'],
  properties: { pass: { type: 'boolean' }, issues: { type: 'string' } } };

function refinePrompt(it, feedback) {
  return [
    'Eres editor experto de prompts de MetodologIA. Aplica un BUCLE DE EXCELENCIA interno: redacta, autoevalúa contra la rúbrica, refina, y repite MENTALMENTE hasta lograr 10/10 en los 10 criterios. Entrega SOLO el resultado final.',
    '',
    'COMANDO (semilla, español de partida):',
    JSON.stringify(it, null, 0),
    '',
    'Produce las 4 versiones del prompt en TRES idiomas (es, en, pt). Versiones: natural, parametros, spec, dupla(system+user).',
    'Línea de Protocolo literal por idioma (debe cerrar cada una de las 4 versiones):',
    'es: ' + PROTO.es, 'en: ' + PROTO.en, 'pt: ' + PROTO.pt,
    '',
    'RÚBRICA (meta 10/10 en todos):', RUBRIC,
    '', 'RESTRICCIONES DURAS:', CONSTR,
    '', 'PARÁMETROS: usa exactamente las key y los value del seed. En paramLabels devuelve key->etiqueta localizada; en optLabels devuelve key->{value->etiqueta localizada}. El valor por defecto (def) debe quedar reflejado como texto dentro de las versiones.',
    'title/desc/crit/edge: púlelos y tradúcelos por idioma (title conserva el prefijo del comando si lo trae).',
    feedback ? ('\nCORRIGE ESTAS FALLAS DE LA VERSIÓN ANTERIOR:\n' + feedback) : '',
    '', 'Devuelve el objeto estructurado. Nada más.'
  ].join('\n');
}

function verifyPrompt(it, unit) {
  return [
    'Audita este comando refinado contra la rúbrica y las restricciones. Sé adversarial y estricto.',
    'Falla (pass=false) si: hay tokens {{...}} o [[...]]; falta la línea de Protocolo en alguna de las 4 versiones de algún idioma; cambió alguna key/value de parámetro respecto al seed; hay metadiscurso; una versión excede su tope de longitud; o algún criterio de la rúbrica no llega a 10.',
    'SEED:', JSON.stringify(it),
    'REFINADO:', JSON.stringify(unit),
    'RESTRICCIONES:', CONSTR,
    'Devuelve {pass, issues}. En issues, lista concreta y accionable de lo que debe corregirse (vacío si pass=true).'
  ].join('\n');
}

async function refineOne(it, feedback) {
  return agent(refinePrompt(it, feedback), { label: 'xl:' + it.command, phase: 'Refine', schema: SCHEMA });
}

const results = await pipeline(SEED,
  it => refineOne(it, null),
  async (r, it) => {
    if (!r) return null;
    const v = await agent(verifyPrompt(it, r), { label: 'verify:' + it.command, phase: 'Verify', schema: VERDICT });
    if (v && v.pass) return r;
    const r2 = await refineOne(it, (v && v.issues) || 'No alcanza 10/10; corrige según la rúbrica y restricciones.');
    return r2 || r;
  }
);
log('Refinados ' + results.filter(Boolean).length + '/' + SEED.length);
return results.filter(Boolean);
'''

out = JS.replace('__SEED__', SEED_JS)
open(os.path.join(HERE, 'xl-workflow.js'), 'w', encoding='utf-8').write(out)
print('escrito tools/xl-workflow.js', len(out), 'bytes')
