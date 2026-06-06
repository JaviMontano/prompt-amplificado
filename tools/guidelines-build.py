#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye, desde guidelines.{es,en,pt}.json:
 (a) sección §04 'Cómo crear prompts' inyectada en biblioteca-prompts.html (antes del catálogo, que pasa a §05),
 (b) página dedicada crear-prompts.html (detalle trilingüe),
 (c) enlace 'Crear prompts' en docset-bar de biblioteca + index.
Idempotente por marcadores. Determinista (sin agentes)."""
import json, os, re, html as H
HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, '..')
LANGS = ['es', 'en', 'pt']
DATA = {l: json.load(open(os.path.join(HERE, 'guidelines.%s.json' % l), encoding='utf-8')) for l in LANGS}
ORDER = ['general', 'natural', 'parametros', 'spec', 'dupla']
FMTS = ['natural', 'parametros', 'spec', 'dupla']
SECLBL = {
 'guidelines': {'es': 'Guidelines', 'en': 'Guidelines', 'pt': 'Diretrizes'},
 'guardrails': {'es': 'Guardrails', 'en': 'Guardrails', 'pt': 'Guardrails'},
 'workflow':   {'es': 'Workflow', 'en': 'Workflow', 'pt': 'Fluxo'},
 'acceptance': {'es': 'Criterios de aceptación', 'en': 'Acceptance criteria', 'pt': 'Critérios de aceitação'},
 'dod':        {'es': 'Definition of Done', 'en': 'Definition of Done', 'pt': 'Definition of Done'},
}
UI = {
 'h2':      {'es': 'Cómo crear prompts', 'en': 'How to create prompts', 'pt': 'Como criar prompts'},
 'sub':     {'es': 'Estándar de calidad por formato — guidelines, guardrails, flujo, criterios y DoD.',
             'en': 'Per-format quality standard — guidelines, guardrails, workflow, criteria and DoD.',
             'pt': 'Padrão de qualidade por formato — diretrizes, guardrails, fluxo, critérios e DoD.'},
 'dod':     {'es': 'DoD', 'en': 'DoD', 'pt': 'DoD'},
 'full':    {'es': 'Ver estándar completo →', 'en': 'See full standard →', 'pt': 'Ver padrão completo →'},
 'detail':  {'es': 'Ver detalle →', 'en': 'See detail →', 'pt': 'Ver detalhe →'},
 'crear':   {'es': 'Crear prompts', 'en': 'Create prompts', 'pt': 'Criar prompts'},
 'pagesub': {'es': 'El estándar para crear prompts MetodologIA en cada formato.',
             'en': 'The standard for creating MetodologIA prompts in each format.',
             'pt': 'O padrão para criar prompts MetodologIA em cada formato.'},
}
def esc(s): return H.escape(s, quote=False)
def tri(field):  # field: dict key path -> returns spans per lang from a getter
    return ''.join('<span class="l-%s">%s</span>' % (l, esc(field[l])) for l in LANGS)
def tri_doc(key, attr):
    return ''.join('<span class="l-%s">%s</span>' % (l, esc(DATA[l][key][attr])) for l in LANGS)
def tri_label(sec):
    return ''.join('<span class="l-%s">%s</span>' % (l, SECLBL[sec][l]) for l in LANGS)
def tri_ui(k):
    return ''.join('<span class="l-%s">%s</span>' % (l, esc(UI[k][l])) for l in LANGS)
def tri_list(key, sec, ordered=False):
    tag = 'ol' if ordered else 'ul'
    n = len(DATA['es'][key][sec])
    lis = []
    for i in range(n):
        spans = ''.join('<span class="l-%s">%s</span>' % (l, esc(DATA[l][key][sec][i] if i < len(DATA[l][key][sec]) else DATA['es'][key][sec][i])) for l in LANGS)
        lis.append('<li>' + spans + '</li>')
    return '<%s>%s</%s>' % (tag, ''.join(lis), tag)
def first_dod(key):
    return ''.join('<span class="l-%s">%s</span>' % (l, esc((DATA[l][key]['dod'] or [''])[0])) for l in LANGS)

# ---------- (a) biblioteca §04 summary ----------
def biblio_section():
    cards = []
    for f in FMTS:
        cards.append(
          '<div class="tile"><span class="k">' + tri_doc(f, 'title').replace('Formato ', '') + '</span>'
          + '<p>' + tri_doc(f, 'intro') + '</p>'
          + '<p style="font-size:.78rem"><b>' + tri_ui('dod') + ':</b> ' + first_dod(f) + '</p>'
          + '<a class="go" href="crear-prompts.html#' + f + '">' + tri_ui('detail') + '</a></div>')
    flow = ' → '.join('<b>%s</b>' % ('%s' % (i + 1)) for i in range(len(DATA['es']['general']['workflow'])))
    return (
      '<!-- GUIDELINES:START -->\n'
      '<section class="wrap" id="estandar">\n'
      '<h2><span class="num">§04</span>' + tri_ui('h2') + '</h2>\n'
      '<p class="lead">' + tri_ui('sub') + '</p>\n'
      '<div class="note"><b>' + tri_doc('general', 'title') + '.</b> ' + tri_doc('general', 'intro') + '</div>\n'
      '<div class="fmt-grid">' + ''.join(cards) + '</div>\n'
      '<p style="margin-top:.8rem"><a class="iconbtn" style="background:var(--gold);color:var(--navy2);border-color:var(--gold);font-weight:700" href="crear-prompts.html">' + tri_ui('full') + '</a></p>\n'
      '</section>\n'
      '<!-- GUIDELINES:END -->')

def inject_biblio():
    fp = os.path.join(ROOT, 'biblioteca-prompts.html')
    s = open(fp, encoding='utf-8').read()
    sec = biblio_section()
    if '<!-- GUIDELINES:START -->' in s:
        s = re.sub(r'<!-- GUIDELINES:START -->.*?<!-- GUIDELINES:END -->', lambda m: sec, s, flags=re.S)
    else:
        s = s.replace('  <section class="catwrap" id="catalogo">', sec + '\n\n  <section class="catwrap" id="catalogo">', 1)
        # catálogo §04 -> §05
        s = s.replace('<span class="num">§04</span><span class="l-es">Catálogo</span>', '<span class="num">§05</span><span class="l-es">Catálogo</span>')
        # docset-bar: añadir Crear prompts antes del Hub
        s = s.replace('<span aria-current="page">Biblioteca</span><span class="sep">·</span>\n  <a class="hub" href="index.html">↑ Hub</a>',
                      '<span aria-current="page">Biblioteca</span><span class="sep">›</span>\n  <a href="crear-prompts.html">Crear</a><span class="sep">·</span>\n  <a class="hub" href="index.html">↑ Hub</a>')
    open(fp, 'w', encoding='utf-8').write(s)
    print("biblioteca §04 inyectada/actualizada")

# ---------- (b) crear-prompts.html ----------
def doc_block(key):
    parts = ['<section class="wrap" id="%s">' % (key if key != 'general' else 'general'),
             '<h2>' + tri_doc(key, 'title') + '</h2>',
             '<p class="lead">' + tri_doc(key, 'intro') + '</p>']
    for sec in ['guidelines', 'guardrails', 'workflow', 'acceptance', 'dod']:
        if not DATA['es'][key].get(sec): continue
        parts.append('<h3>' + tri_label(sec) + '</h3>')
        parts.append(tri_list(key, sec, ordered=(sec == 'workflow')))
    parts.append('</section>')
    return '\n'.join(parts)

def fmt_panel(key):
    secs = []
    for sec in ['guidelines', 'guardrails', 'workflow', 'acceptance', 'dod']:
        if not DATA['es'][key].get(sec): continue
        secs.append('<h4>' + tri_label(sec) + '</h4>' + tri_list(key, sec, ordered=(sec == 'workflow')))
    return ('<div class="fmt-panel fp-%s" id="%s"><div class="ph"><span class="fk">%s</span><h3>%s</h3><p>%s</p></div><div class="bd">%s</div></div>'
            % (key, key, key, tri_doc(key, 'title'), tri_doc(key, 'intro'), ''.join(secs)))

def formats_section():
    head = ('<section class="wrap"><h2>'
            '<span class="l-es">Estándar por formato</span><span class="l-en">Standard by format</span><span class="l-pt">Padrão por formato</span>'
            '</h2><p class="lead">'
            '<span class="l-es">Misma estructura en los cuatro formatos: guidelines · guardrails · workflow · criterios · DoD.</span>'
            '<span class="l-en">Same structure across the four formats: guidelines · guardrails · workflow · criteria · DoD.</span>'
            '<span class="l-pt">Mesma estrutura nos quatro formatos: diretrizes · guardrails · fluxo · critérios · DoD.</span>'
            '</p><div class="fmt-cols">')
    return head + ''.join(fmt_panel(f) for f in FMTS) + '</div></section>'

def build_page():
    docset = (
      '<div class="docset-bar">\n'
      '  <span class="set">Prompt Amplificado:</span>\n'
      '  <a href="masterclass.html">Masterclass</a><span class="sep">›</span>\n'
      '  <a href="playbook-prompt-engineering.html">Prompt</a><span class="sep">·</span>\n'
      '  <a href="playbook-context-engineering.html">Context</a><span class="sep">·</span>\n'
      '  <a href="playbook-harness-engineering.html">Harness</a><span class="sep">›</span>\n'
      '  <a href="biblioteca-prompts.html">Biblioteca</a><span class="sep">·</span>\n'
      '  <span aria-current="page">' + tri_ui('crear') + '</span><span class="sep">·</span>\n'
      '  <a class="hub" href="index.html">↑ Hub</a>\n'
      '</div>')
    blocks = doc_block('general') + '\n\n' + formats_section()
    page = (
'''<!doctype html><html lang="es" data-theme="light"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#F9FAFB" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0A122A" media="(prefers-color-scheme: dark)">
<title>Cómo crear prompts · Estándar | MetodologIA</title>
<meta name="description" content="Estándar para crear prompts MetodologIA por formato: guidelines, guardrails, workflow, criterios de aceptación y Definition of Done. ES/EN/PT.">
<link rel="canonical" href="https://javimontano.github.io/prompt-amplificado/crear-prompts.html">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="estilos/doc.css">
<style>
.fmt-cols{display:grid;gap:1rem;grid-template-columns:1fr;margin:1rem 0}
@media(min-width:780px){.fmt-cols{grid-template-columns:1fr 1fr}}
.fmt-panel{border:1px solid var(--rule);border-radius:var(--r2);background:var(--card);overflow:hidden;display:flex;flex-direction:column}
.fmt-panel .ph{padding:.7rem .9rem;border-bottom:3px solid var(--accent,var(--gold));background:var(--navy2);color:#fff}
.fmt-panel .ph .fk{font-family:var(--f-mono);font-size:.6rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent,var(--gold))}
.fmt-panel .ph h3{color:#fff;margin:.1rem 0;font-size:1.02rem}
.fmt-panel .ph p{color:#dfe7f5;font-size:.8rem;margin:.25rem 0 0}
.fmt-panel .bd{padding:.5rem .9rem .9rem}
.fmt-panel h4{font-size:.64rem;text-transform:uppercase;letter-spacing:.05em;color:var(--gold-deep);margin:.8rem 0 .25rem;font-family:var(--f-head)}
.fmt-panel ul,.fmt-panel ol{margin:.2rem 0;padding-left:1.15rem}
.fmt-panel li{margin:.22rem 0;font-size:.85rem;line-height:1.5}
.fp-natural{--accent:var(--blue)}.fp-parametros{--accent:var(--gold-deep)}.fp-spec{--accent:var(--ok)}.fp-dupla{--accent:#7c3aed}
</style>
</head><body>
<div class="reading-progress"></div>
''' + docset + '''
<header class="top">
  <span class="brand">Metodolog<span class="ia">IA</span></span>
  <span class="role"><span class="l-es">Crear prompts</span><span class="l-en">Create prompts</span><span class="l-pt">Criar prompts</span></span>
  <span class="sp"></span>
  <button class="iconbtn" id="langbtn" type="button" title="ES / EN / PT" aria-label="Idioma">ES</button>
  <button class="iconbtn" id="theme" type="button" title="Claro / Oscuro" aria-label="Tema">☾</button>
</header>
<main>
  <section class="wrap hero" style="border-bottom:1px solid var(--rule)">
    <span class="eyebrow"><span class="l-es">Estándar · Recursos abiertos</span><span class="l-en">Standard · Open resources</span><span class="l-pt">Padrão · Recursos abertos</span></span>
    <h1><span class="l-es">Cómo crear <span class="gradient-text">prompts</span></span><span class="l-en">How to create <span class="gradient-text">prompts</span></span><span class="l-pt">Como criar <span class="gradient-text">prompts</span></span></h1>
    <p class="lead">''' + tri_ui('pagesub') + '''</p>
    <div class="flow"><b>Natural</b> · <b>Parámetros</b> · <b>SPEC</b> · <b>Dupla</b></div>
  </section>
''' + blocks + '''
</main>
<div class="docset-version">
  Prompt Amplificado · <span class="l-es">Crear prompts</span><span class="l-en">Create prompts</span><span class="l-pt">Criar prompts</span> · v1.0 · © 2026 MetodologIA · Copyleft (CC BY-SA 4.0) · <a href="biblioteca-prompts.html">Biblioteca</a> · <a href="index.html">↑ Hub</a>
</div>
<script src="estilos/doc.js"></script>
</body></html>
''')
    open(os.path.join(ROOT, 'crear-prompts.html'), 'w', encoding='utf-8').write(page)
    print("crear-prompts.html generado")

def update_index():
    fp = os.path.join(ROOT, 'index.html')
    s = open(fp, encoding='utf-8').read()
    if 'crear-prompts.html' not in s:
        s = s.replace('<a href="biblioteca-prompts.html">Biblioteca</a><span class="sep">·</span>\n  <span aria-current="page">Hub</span>',
                      '<a href="biblioteca-prompts.html">Biblioteca</a><span class="sep">·</span>\n  <a href="crear-prompts.html">Crear</a><span class="sep">·</span>\n  <span aria-current="page">Hub</span>')
        open(fp, 'w', encoding='utf-8').write(s)
        print("index docset-bar actualizado")
    else:
        print("index ya enlaza crear-prompts")

if __name__ == '__main__':
    inject_biblio(); build_page(); update_index()
