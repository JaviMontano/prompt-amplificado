#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fase 1 (ES): adopta el content rico de v3000 para los 78 comandos.
Parsea las secciones rotuladas y compone 4 versiones por extracción VERBATIM (cero reescritura):
  SPEC = content íntegro · parámetros = INPUTS + cláusulas · natural = ABSTRACT+EJECUCIÓN · dupla = ROL.. / PEDIDO..
Bondades = strategy{how_to_use,importance,common_errors,three_minute_exercise} + example_output.
Escribe r.tri.es + top-level (back-compat). params = quick_inputs. EN/PT se añaden en fase 3.
"""
import json, os, re
HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '..', 'biblioteca-data.json')
V3000 = os.path.expanduser('~/material-educativo-metodologia/prompts_universales_v3000.json')
PROTO = ">> Protocolo MetodologIA: Interpreta > Planifica > Ejecuta. Reformula lo que entiendes y presenta tu plan antes de ejecutar."
ALIAS = {'/traduce': '/v11_traduce'}  # live_command -> v3000 invoke (si difiere)

HDR = re.compile(r'^([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ /()+\-]{2,40}):\s*$')

def parse_sections(content):
    sec = {}; cur = '_PRE'; buf = []
    for ln in content.split('\n'):
        s = ln.strip()
        if s.startswith('—') and 'CLÁUSULAS' in s:
            sec[cur] = '\n'.join(buf).strip(); cur = 'CLÁUSULAS'; buf = []; continue
        m = HDR.match(s)
        if m and cur != 'CLÁUSULAS':
            sec[cur] = '\n'.join(buf).strip(); cur = m.group(1); buf = []; continue
        buf.append(ln)
    sec[cur] = '\n'.join(buf).strip()
    return sec

def clause_headers(clauses_text):
    out = []
    for ln in clauses_text.split('\n'):
        s = ln.strip()
        if s.startswith('[') and (']' in s or '·' in s):
            out.append(s.strip('[]').split(']')[0])
    return out

def first_sentence(t, n=200):
    t = re.sub(r'\s+', ' ', t).strip()
    m = re.split(r'(?<=[.!?])\s', t)
    return (m[0] if m else t)[:n]

def compose(sec):
    g = lambda k: sec.get(k, '').strip()
    abstract = g('ABSTRACT') or g('RESUMEN')
    ejec = g('EJECUCIÓN'); rol = g('ROL'); ped = g('PEDIDO')
    sup = g('SUPUESTOS'); lim = g('LÍMITES'); sal = g('SALIDA OBLIGATORIA') or g('SALIDA')
    inputs = g('INPUTS'); clauses = clause_headers(g('CLÁUSULAS'))
    natural = (abstract + ("\n\nPASOS:\n" + ejec if ejec else "") + "\n\n" + PROTO).strip()
    clause_b = "\n".join("· " + c for c in clauses)
    parametros = ("INPUTS:\n" + inputs +
                  ("\n\nCLÁUSULAS ACTIVAS (defaults · ajústalas al vuelo):\n" + clause_b if clause_b else "") +
                  "\n\n" + PROTO).strip()
    dsys = ("ROL:\n" + rol +
            ("\n\nSUPUESTOS:\n" + sup if sup else "") +
            ("\n\nLÍMITES:\n" + lim if lim else "") +
            "\n\n" + PROTO).strip()
    duser = ("PEDIDO:\n" + ped +
             ("\n\nEJECUCIÓN:\n" + ejec if ejec else "") +
             ("\n\nSALIDA:\n" + sal if sal else "")).strip()
    return natural, parametros, dsys, duser

def main():
    v = json.load(open(V3000, encoding='utf-8'))
    P = v['prompts'] if isinstance(v, dict) else v
    vidx = {}
    for r in P:
        for c in (r.get('invoke') or []):
            vidx.setdefault(c, r)
    data = json.load(open(DATA, encoding='utf-8'))
    n, miss = 0, []
    for r in data:
        cmd = r.get('command')
        if not r.get('params') and not r.get('tri'):
            continue  # solo los 78 comandos (tenían params)
        src = vidx.get(cmd) or vidx.get(ALIAS.get(cmd, ''))
        if not src:
            miss.append(cmd); continue
        content = src['content']
        sec = parse_sections(content)
        natural, parametros, dsys, duser = compose(sec)
        strat = src.get('strategy')
        if isinstance(strat, str):
            try: strat = json.loads(strat)
            except Exception: strat = {}
        strat = strat or {}
        bondades = {
            "how_to_use": strat.get('how_to_use', ''),
            "importance": strat.get('importance', ''),
            "common_errors": strat.get('common_errors', ''),
            "exercise": strat.get('three_minute_exercise', ''),
            "example": src.get('example_output', '')
        }
        keep_title = r.get('title') or src.get('label_title') or cmd  # conserva títulos curados
        es = {
            "title": keep_title,
            "desc": first_sentence(sec.get('ABSTRACT', '') or sec.get('RESUMEN', '') or r.get('desc', '')),
            "bondades": bondades,
            "formats": {
                "natural": natural, "natural_params": parametros, "spec": content,
                "dupla": {"system": dsys, "user": duser}
            }
        }
        r['tri'] = {"es": es}
        # params (Ajustables) desde quick_inputs
        qi = src.get('quick_inputs') or []
        if isinstance(qi, str):
            try: qi = json.loads(qi)
            except Exception: qi = []
        params = []
        for it in qi:
            lbl = it.get('label') or it.get('token', 'param')
            dv = it.get('defaultValue') or 'valor real'
            params.append({"key": re.sub(r'[^a-z0-9]+', '_', lbl.lower()).strip('_') or 'p',
                           "label": lbl, "def": dv, "opts": [[dv, dv]]})
        r['params'] = params
        r['cmd78'] = True
        # back-compat top-level
        r['title'] = es['title']; r['desc'] = es['desc']; r['formats'] = es['formats']
        r['bondades'] = bondades
        # limpiar campos viejos de scaffolds
        r.pop('crit', None); r.pop('edge', None)
        n += 1
    json.dump(data, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print("ES sintetizado: %d comandos" % n)
    if miss: print("sin match en v3000 (%d):" % len(miss), miss)
    # tamaños
    import statistics
    specs = [len(r['tri']['es']['formats']['spec']) for r in data if r.get('tri')]
    nats = [len(r['tri']['es']['formats']['natural']) for r in data if r.get('tri')]
    if specs:
        print("spec chars: avg %d max %d | natural avg %d max %d" % (
            statistics.mean(specs), max(specs), statistics.mean(nats), max(nats)))

if __name__ == '__main__':
    main()
