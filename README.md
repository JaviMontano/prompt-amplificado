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
