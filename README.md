# Prompt Amplificado · Ingeniería de Prompts, Contexto y Arneses

> **Método primero, (Gen)IA después.** La IA guía; la persona decide.

Material abierto de **MetodologIA** sobre las tres ingenierías de operar la (Gen)IA:
**prompt**, **contexto** y **arnés (harness)**. Trilingüe **ES · EN · PT**. Sin precios. Copyleft.

🔗 **Sitio en vivo:** https://javimontano.github.io/prompt-amplificado/

---

## Documentos (8)

| Documento | Qué es |
|---|---|
| [`index.html`](index.html) | **Hub** — recorrido progresivo + material abierto |
| [`masterclass.html`](masterclass.html) | Landing conceptual: por qué prompt · contexto · arnés |
| [`workbook.html`](workbook.html) | Ejercicio 1 sesión: tu prompt, context pack y mini-arnés |
| [`playbook-prompt-engineering.html`](playbook-prompt-engineering.html) | SPEC, 5 pilares, rúbrica de 10, few-shot/CoT, anti-patrones, 100✓ |
| [`playbook-context-engineering.html`](playbook-context-engineering.html) | Ventana, context rot, priming, RAG, chunking, MEMORY.md, soberanía |
| [`playbook-harness-engineering.html`](playbook-harness-engineering.html) | Tool use, orquestación, loops, multi-agente, guardrails, evals |
| [`runbook.html`](runbook.html) | El cómo end-to-end: pasos CHECK+PROMPT+TEMPLATE, catálogos, glosario |
| [`biblioteca-prompts.html`](biblioteca-prompts.html) | **2026 prompts** en 4 formatos, filtrables por disciplina |

## Biblioteca

`biblioteca-prompts.html` carga `biblioteca-data.json` (2026 prompts, 16 categorías,
cada uno en 4 formatos: natural · parámetros · SPEC MetodologIA · dupla system/user).
Filtra por **disciplina** (Prompting · Context · Harness · Meta), categoría o tag;
copia, descarga `.md` o lleva el prompt directo a ChatGPT, Claude o Gemini.

### v1.1 (2026-06-05) — robustez

- **Capa editorial**: hero, storytelling, conceptos (diagrama de 3 capas + los 4 formatos) y "cómo usar", reutilizando `estilos/doc.css` (sin CSS duplicado).
- **Performance**: render incremental por lotes (60) con `IntersectionObserver`, búsqueda con debounce e índice precomputado.
- **Búsqueda + comandos**: busca en el **cuerpo** del prompt; **command palette** (`Ctrl/⌘+K` o `/`); **slash-invoke** por `command`; comandos `/a–/z` con toggle; orden por calidad/A-Z/categoría.
- **Deep-linking**: estado en URL (`?q=&disc=&cat=&sort=`) y prompt direccionable por `#id`; botón **Compartir**.
- **A11y · i18n**: `<option>`/placeholder/conteo traducidos (ES·EN·PT), `aria-live`, skip-link, foco al cerrar modal, estado "sin resultados".
- **Capa de invocación parametrizada** (78 prompts: `/0–/9` + 42 verbos + `/a–/z`): cada uno con **2–4 parámetros con defaults** (no inputs, cero fricción). Selectores en el modal reescriben el prompt al vuelo; toggle para anteponer cabecera «Parámetros: …»; los defaults reproducen el comportamiento previo. Generador reproducible: `tools/robustecer-comandos.py` (backup en `biblioteca-data.json.bak`).

## Local

```bash
# La Biblioteca usa fetch(); sírvela por HTTP, no file://
python3 -m http.server 8000
# → http://localhost:8000/
```

## Estructura

```
index.html · masterclass.html · workbook.html
playbook-{prompt,context,harness}-engineering.html · runbook.html
biblioteca-prompts.html + biblioteca-data.json
estilos/doc.css · estilos/doc.js · favicon.svg
```

## Licencia

- **Contenido** (texto, HTML, dataset): **CC BY-SA 4.0** (Copyleft) — atribución a MetodologIA (metodologia.info) + ShareAlike.
- **Código** (CSS/JS): **MIT**.

Ver [`LICENSE`](LICENSE). · Contacto: contacto@metodologia.info · https://metodologia.info/
