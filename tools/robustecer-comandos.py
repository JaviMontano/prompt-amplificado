#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robustece + parametriza la capa de invocación de la Biblioteca (live).
Alcance: /0–/9 (pipeline P.I.V.O.T.E.) + 42 verbos + /a–/z (78 prompts).

Modelo:
- Cada prompt gana `params: [{key,label,opts:[[v,label,text]],def}]` (2–4).
- El cuerpo usa tokens `[[key]]`. Render con DEFAULTS == comportamiento actual.
- Parámetros, NO inputs: cero {{...}}. Sin fricción; ajustables al vuelo.

Salida: reescribe los 78 registros en biblioteca-data.json (formats con tokens
+ params + title/desc mejorados). Crea backup .bak antes de escribir.
"""
import json, re, os, sys, shutil

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA = os.path.join(ROOT, 'biblioteca-data.json')
PROTO = ">> Protocolo MetodologIA: Interpreta > Planifica > Ejecuta. Reformula lo que entiendes y presenta tu plan antes de ejecutar."

# ---------- presets opcionales (default vacío -> no cambia el comportamiento) ----------
def opt(key, label, pairs):
    # pairs: list of (v, optionLabel, injectedText). Primera = default.
    return {"key": key, "label": label, "opts": [[v, lbl, txt] for (v, lbl, txt) in pairs], "def": pairs[0][0]}

def P_tono():
    return opt("tono", "Tono", [
        ("std", "estándar", ""),
        ("ejec", "ejecutivo", " Tono ejecutivo: conciso y orientado a decisión."),
        ("did", "didáctico", " Tono didáctico: explica paso a paso, sin jerga."),
        ("tec", "técnico", " Tono técnico: preciso, con terminología del dominio."),
    ])
def P_ext():
    return opt("extension", "Extensión", [
        ("std", "estándar", ""),
        ("breve", "breve", " Extensión: lo más breve posible, sin relleno."),
        ("amplio", "extenso", " Extensión: desarrolla en profundidad con ejemplos."),
    ])
def P_idioma():
    return opt("idioma", "Idioma", [
        ("es", "español", ""),
        ("en", "inglés", " Responde en inglés profesional."),
        ("pt", "portugués", " Responde en portugués profesional."),
    ])
def P_evid():
    return opt("evidencia", "Evidencia", [
        ("std", "estándar", ""),
        ("fuentes", "con fuentes", " Respalda cada afirmación con una fuente citable."),
        ("datos", "con datos", " Cuantifica con datos, cifras o rangos fundamentados."),
    ])
def P_formato_salida():
    return opt("salida", "Formato", [
        ("std", "estándar", ""),
        ("bullets", "bullets", " Formato: viñetas escaneables."),
        ("tabla", "tabla", " Formato: tabla estructurada."),
        ("prosa", "prosa", " Formato: prosa continua."),
    ])

# inline param: pairs (v, optionLabel, injectedText); injectedText reemplaza el token
def ip(key, label, pairs):
    return {"key": key, "label": label, "opts": [[v, lbl, txt] for (v, lbl, txt) in pairs], "def": pairs[0][0]}

# ---------- especificaciones de los 78 ----------
# spec: command -> (title, desc, body_template, [params...])
# body_template usa [[key]] por cada param inline; los opcionales se anexan al final.
S = {}

def add(cmd, title, desc, body, params, tail=("tono","ext")):
    # tail: presets opcionales a anexar (claves cortas)
    presets = {"tono": P_tono, "ext": P_ext, "idioma": P_idioma, "evid": P_evid, "salida": P_formato_salida}
    plist = list(params)
    toks = ""
    for t in tail:
        plist.append(presets[t]())
        toks += "[[%s]]" % presets[t]()["key"]
    S[cmd] = (title, desc, body + toks, plist)

# ===== /0–/9 — Pipeline P.I.V.O.T.E. =====
add("/0", "0 · Priming — Setear contexto",
    "Carga el contexto antes de ejecutar: lee, reformula y pregunta lo crítico. Base de todo el pipeline.",
    "PRIMING — Setear contexto\n\n1. Lee todo lo que comparto (texto, adjuntos, contexto). NO ejecutes nada.\n2. Reformula en tus palabras: quién soy, qué hacemos, qué restricciones hay.\n3. Pregunta máx [[preguntas]] ambigüedades críticas.\n\nSi el priming es correcto, todo fluye. Si no, todo es desperdicio.",
    [ip("preguntas","Preguntas máx",[("3","3","3"),("0","0 (no preguntes)","0"),("5","5","5")])],
    tail=("idioma","tono"))
add("/1", "1 · Entender — Comprender la necesidad",
    "Convierte una idea vaga en una necesidad precisa: Qué + Para qué + Para quién, validada antes de avanzar.",
    "ENTENDER — Comprender la necesidad\n\n1. Escucha mi idea/tarea/problema (puede ser vago).\n2. Reformula en [[lineas]]: Qué + Para Qué + Para Quién.\n3. Identifica lo que falta para actuar con precisión.\n4. Presenta tu comprensión para validación ANTES de continuar.",
    [ip("lineas","Síntesis",[("1 oración","1 oración","1 oración"),("2-3 oraciones","2-3 oraciones","2-3 oraciones"),("1 párrafo","1 párrafo","1 párrafo")])],
    tail=("tono","idioma"))
add("/2", "2 · Definir — Construir el SPEC",
    "Levanta el contrato SPEC (Situación · Pedido · Ejecución · Criterio) y lo presenta para aprobación.",
    "DEFINIR — Construir el SPEC\n\n1. S: ¿Para qué? ¿Qué se desbloquea? Contexto y restricciones.\n2. P: Arquetipo experto + entregable concreto + alcance (SÍ/NO incluye).\n3. E: Método, fases, decisiones que requieren mi validación.\n4. C: Formato, audiencia, tono, medida de éxito.\n\nPresenta el SPEC completo para aprobación. Es el contrato.",
    [], tail=("tono","idioma"))
add("/3", "3 · Planificar — Plan de acción",
    "Descompone en fases secuenciales con dependencias y riesgos; no ejecuta sin plan aprobado.",
    "PLANIFICAR — Plan de acción\n\n1. Descompone en fases secuenciales: qué produces, qué necesitas.\n2. Identifica dependencias y riesgos.\n3. Presenta el plan para aprobación.\n\nNo ejecutes sin plan aprobado.",
    [], tail=("salida","tono"))
add("/4", "4 · Ejecutar — Primera versión",
    "Produce un draft completo siguiendo SPEC y plan; completitud sobre perfección, marca pendientes.",
    "EJECUTAR — Primera versión\n\n1. Sigue el SPEC (paso 2) y el Plan (paso 3).\n2. Completitud > perfección. Es un draft.\n3. Marca [PENDIENTE] y [VERIFICAR] donde aplique.\n4. Entrega COMPLETO, no parcial.",
    [], tail=("tono","ext"))
add("/5", "5 · Robustecer — Agregar sustancia",
    "Solidifica con datos, fuentes y ejemplos verificables; resuelve pendientes. Más sólido, no más largo.",
    "ROBUSTECER — Agregar sustancia\n\n1. [[fuente]]\n2. Ejemplos concretos y casos reales.\n3. Resuelve todos los [PENDIENTE] y [VERIFICAR].\n\nMás sólido, no más largo.",
    [ip("fuente","Sustancia",[("Datos, fuentes, estadísticas verificables.","datos+fuentes","Datos, fuentes, estadísticas verificables."),("Datos y cifras cuantificadas.","solo datos","Datos y cifras cuantificadas."),("Fuentes citables y referencias.","solo fuentes","Fuentes citables y referencias.")])],
    tail=("evid","tono"))
add("/6", "6 · Simplificar — Destilar valor",
    "Elimina duplicados, pasivos y relleno; el output debe quedar más corto que el input.",
    "SIMPLIFICAR — Destilar valor\n\n1. Duplicados > queda uno. Pasivos > activos. Relleno > eliminado.\n2. Si quitarlo no empeora el resultado, quitarlo.\n3. El output DEBE ser más corto que el input.\n\nSimplificar es destilar. Lo que sobrevive es diamante.",
    [], tail=("tono","idioma"))
add("/7", "7 · Validar — Verificar calidad",
    "Corre el checklist punto por punto (OK/AJUSTE/FALLA) y enruta de vuelta si algo falla.",
    "VALIDAR — Verificar calidad\n\n1. Ejecuta [checklist] punto por punto: OK / AJUSTE / FALLA.\n2. Verifica coherencia y soporte de afirmaciones.\n3. Si FALLA: volver a paso 5 o 6. Si AJUSTE: corregir y avanzar.[[rigor]]",
    [ip("rigor","Rigor",[("","estándar",""),("estricto"," Modo estricto: cualquier AJUSTE bloquea la entrega."," Modo estricto: cualquier AJUSTE bloquea la entrega.")])],
    tail=("tono",))
add("/8", "8 · Entregar — Formato final",
    "Aplica tono y formato del Criterio; verifica que sea usable sin edición por la audiencia destino.",
    "ENTREGAR — Formato final\n\n1. Aplica tono y formato del Criterio (C).\n2. Verifica: usable sin edición por la audiencia destino.\n3. Test: si lo recibe alguien exigente, ¿lo aceptaría tal cual?",
    [], tail=("salida","tono"))
add("/9", "9 · Cristalizar — Ingeniería inversa",
    "Convierte la sesión en activos reutilizables: un priming + un SPEC de alto rendimiento de 1 paso.",
    "CRISTALIZAR — Ingeniería inversa\n\nAnaliza el historial completo. Genera [[entregables]]:\n\nA) Priming (máx 200 palabras): contexto + rol + restricciones.\nB) SPEC de Alto Rendimiento: [inputs]/[prompt] S-P-E-C/[checklist] que produzca el resultado en 1 paso.\n\nEl proceso de hoy construye el atajo de mañana.",
    [ip("entregables","Salida",[("2 prompts reutilizables","2 prompts","2 prompts reutilizables"),("solo el SPEC","solo SPEC","el SPEC reutilizable"),("3 prompts (priming + SPEC + checklist)","3 prompts","3 prompts reutilizables")])],
    tail=("idioma","tono"))

# ===== 42 verbos =====
add("/compara", "Compara", "Tabla comparativa con scoring ponderado y recomendación fundamentada.",
    "Tabla comparativa estructurada. Columnas: criterios clave. Filas: opciones. Scoring numérico ([[escala]]) por criterio. Totales ponderados. Recomendación fundamentada al final.",
    [ip("escala","Escala",[("1-5","1-5","1-5"),("1-10","1-10","1-10"),("Alto/Medio/Bajo","A/M/B","alto/medio/bajo")])])
add("/prioriza", "Prioriza", "Ordena por impacto real: top N con criterios y formato ajustables.",
    "Ordena por impacto real. Top [[top]] con justificación explícita. Usa criterios: [[criterios]]. Presenta como [[formato]].",
    [ip("top","Top",[("3","3","3"),("5","5","5"),("10","10","10")]),
     ip("criterios","Criterios",[("impacto, esfuerzo, urgencia","impacto/esfuerzo/urgencia","impacto (alto/medio/bajo), esfuerzo (alto/medio/bajo), urgencia"),("RICE","RICE","RICE (reach, impact, confidence, effort)"),("valor vs riesgo","valor/riesgo","valor de negocio vs riesgo")]),
     ip("formato","Formato",[("matriz o lista priorizada","matriz/lista","matriz o lista priorizada"),("tabla","tabla","tabla priorizada"),("matriz 2x2","matriz 2x2","matriz 2x2 impacto/esfuerzo")])], tail=())
add("/reformula", "Reformula", "Reescribe con claridad profesional: mismo mensaje, mejor forma.",
    "Reescribe con claridad profesional. Mismo mensaje, mejor forma. Activa verbos pasivos, elimina ambigüedades, mejora flujo lógico. Entrega solo la versión mejorada.",
    [], tail=("tono","idioma"))
add("/debate", "Debate", "Debate socrático con 3 perspectivas confrontadas y síntesis integradora.",
    "Debate socrático. Presenta [[perspectivas]] confrontadas sobre el tema. Cada perspectiva con argumentos sólidos. Cierra con síntesis que integre lo mejor de todas.",
    [ip("perspectivas","Perspectivas",[("3 perspectivas (a favor, en contra, tercera vía)","3","3 perspectivas: a favor, en contra y una tercera vía"),("2 posturas (a favor/en contra)","2","2 posturas: a favor y en contra"),("4 perspectivas","4","4 perspectivas distintas")])], tail=("tono",))
add("/investiga", "Investiga", "Investigación estructurada con fuentes verificables y gaps identificados.",
    "Investigación estructurada con fuentes verificables. Formato: hallazgos clave + evidencia + gaps identificados + implicaciones. Cada hallazgo con [FUENTE]. Cero afirmaciones sin soporte.",
    [], tail=("ext","idioma"))
add("/documenta", "Documenta", "Formaliza en documento profesional listo para archivar o compartir.",
    "Formaliza en documento profesional con: título, fecha, autor, estructura con secciones numeradas, metadata relevante. Listo para archivar o compartir sin edición.",
    [], tail=("salida","idioma"))
add("/diagrama", "Diagrama", "Representación visual del concepto en notación de diagramas.",
    "Crea representación visual del concepto: [[tipo]] según aplique. Usa [[notacion]].",
    [ip("tipo","Tipo",[("diagrama de flujo, mapa mental, matriz, timeline o arquitectura","auto","diagrama de flujo, mapa mental, matriz, timeline o arquitectura"),("diagrama de flujo","flujo","diagrama de flujo"),("mapa mental","mapa mental","mapa mental"),("arquitectura","arquitectura","diagrama de arquitectura")]),
     ip("notacion","Notación",[("Mermaid","Mermaid","sintaxis Mermaid"),("PlantUML","PlantUML","sintaxis PlantUML"),("ASCII","ASCII","diagrama ASCII")])], tail=())
add("/evalua", "Evalúa", "Evaluación sistemática con rúbrica explícita y scoring.",
    "Evaluación sistemática con rúbrica explícita. Define criterios, escala ([[escala]]), evalúa cada dimensión, presenta scoring total y recomendación fundamentada.",
    [ip("escala","Escala",[("1-5 o 1-10","1-5/1-10","1-5 o 1-10"),("1-10","1-10","1-10"),("1-5","1-5","1-5")])], tail=("tono",))
add("/optimiza", "Optimiza", "Detecta ineficiencias y propone mejoras priorizadas por beneficio/esfuerzo.",
    "Identifica ineficiencias, cuellos de botella y desperdicios. Propone mejoras concretas con impacto estimado. Prioriza por ratio beneficio/esfuerzo. Formato: problema > solución > impacto.",
    [], tail=("evid","tono"))
add("/automatiza", "Automatiza", "Identifica lo automatizable con herramienta, ROI y complejidad.",
    "Identifica lo automatizable en el proceso descrito. Para cada oportunidad: qué automatizar, con qué herramienta, ROI estimado (horas/semana ahorradas), complejidad de implementación. Prioriza por quick wins.",
    [], tail=("evid","tono"))
add("/desafia", "Desafía", "Challenge mode: ataca la propuesta desde múltiples ángulos de viabilidad.",
    "Challenge mode. Ataca la propuesta desde [[angulos]]. Busca fallas, supuestos no validados y riesgos ocultos. Sé constructivo pero implacable.",
    [ip("angulos","Ángulos",[("3 ángulos (técnico, financiero, operativo)","3","3 ángulos: viabilidad técnica, financiera y operativa"),("solo viabilidad técnica","técnico","el ángulo de viabilidad técnica"),("5 ángulos (técnico, financiero, operativo, legal, humano)","5","5 ángulos: técnico, financiero, operativo, legal y humano")])], tail=("tono",))
add("/calibra", "Calibra", "Ajusta tono, profundidad y formato a una audiencia específica.",
    "Ajusta tono, profundidad y formato a la audiencia [[audiencia]]. Adapta nivel de detalle, lenguaje y foco según corresponda.",
    [ip("audiencia","Audiencia",[("especificada","auto","especificada"),("C-level","C-level","C-level: conciso, estratégico, orientado a decisión"),("técnica","técnica","técnica: detallado, preciso, con evidencia"),("general","general","general: claro, sin jerga, con ejemplos")])], tail=("idioma",))
add("/resume", "Resume", "Resumen ejecutivo de 3 párrafos: conclusión, evidencia, próximos pasos.",
    "Resume en formato ejecutivo: máx [[parrafos]]. Conclusión y recomendación principal; evidencia y fundamento clave; próximos pasos concretos con responsable y fecha.",
    [ip("parrafos","Extensión",[("3 párrafos","3 párrafos","3 párrafos"),("1 párrafo","1 párrafo","1 párrafo"),("5 bullets","5 bullets","5 viñetas")])], tail=("idioma",))
add("/traduce", "Traduce", "Traduce preservando tono, intención y matices culturales.",
    "Traduce [[direccion]] manteniendo tono, intención y matices culturales. Preserva términos técnicos. Solo la traducción.",
    [ip("direccion","Dirección",[("al otro idioma","auto","al otro idioma"),("ES→EN","ES→EN","del español al inglés profesional"),("EN→ES","EN→ES","del inglés al español latinoamericano profesional"),("→PT","→PT","al portugués profesional")])], tail=())
add("/profundiza", "Profundiza", "Expande a nivel de experto senior: datos, casos y matices.",
    "Expande con nivel de experto senior: datos, ejemplos concretos, casos de estudio, matices no explorados, perspectivas contrarias. [[multiplicador]] de valor que el contenido actual.",
    [ip("multiplicador","Profundidad",[("3x más","3x","3x más"),("2x más","2x","2x más"),("5x más","5x","5x más")])], tail=("evid",))
add("/simplifica", "Simplifica", "Reduce a lo esencial: cada palabra se gana su lugar.",
    "Reduce a lo esencial. Cada palabra debe ganarse su lugar. Elimina redundancias. Si se puede decir en 1 oración, no uses 3. El resultado debe ser más corto que el input.",
    [], tail=("tono","idioma"))
add("/contextualiza", "Contextualiza", "Sitúa en antecedentes, marco teórico y por qué importa ahora.",
    "Sitúa en contexto: antecedentes históricos, marco teórico, tendencias relevantes, y por qué importa AHORA. Conecta con el panorama general sin perder foco en lo específico.",
    [], tail=("ext","idioma"))
add("/cuantifica", "Cuantifica", "Convierte lo cualitativo en números, rangos o estimaciones.",
    "Convierte lo cualitativo en cuantitativo. Cada afirmación con número, porcentaje, rango o estimación fundamentada. Si no hay dato exacto, proporciona orden de magnitud.",
    [], tail=("evid","salida"))
add("/visualiza", "Visualiza", "Describe cómo representar visualmente: tipo, layout y jerarquía.",
    "Describe cómo representar visualmente: qué tipo de gráfico, mapa, diagrama o infografía. Especifica layout, paleta, jerarquía. El visual debe comunicar sin texto adicional.",
    [], tail=("tono",))
add("/personaliza", "Personaliza", "Adapta cada recomendación a tu rol, sector y restricciones reales.",
    "Adapta a mi contexto profesional específico. No respuestas genéricas — cada recomendación debe considerar mi rol, sector, equipo, herramientas y restricciones reales.",
    [], tail=("tono","idioma"))
add("/estructura", "Estructura", "Organiza en pirámide MECE: conclusión primero, evidencia después.",
    "Organiza en estructura piramidal: conclusión primero, argumentos de soporte después, evidencia al final. Cada nivel responde al 'por qué' del nivel superior. MECE.",
    [], tail=("salida","tono"))
add("/argumenta", "Argumenta", "Construye argumento sólido con tesis, soporte y contra-argumentos.",
    "Construye argumento sólido: tesis clara, [[puntos]] de soporte con evidencia, anticipación de contra-argumentos, conclusión. Cada afirmación con dato o razonamiento explícito.",
    [ip("puntos","Puntos",[("3 puntos","3","3 puntos"),("2 puntos","2","2 puntos"),("5 puntos","5","5 puntos")])], tail=("evid",))
add("/predice", "Predice", "Proyecta 3 escenarios fundamentados con probabilidad e implicaciones.",
    "Proyecta [[escenarios]] basados en la información actual. Cada uno con condiciones, probabilidad estimada e implicaciones. No adivinar — extrapolar con fundamento.",
    [ip("escenarios","Escenarios",[("3 escenarios (optimista, probable, pesimista)","3","3 escenarios: optimista, probable y pesimista"),("2 escenarios (mejor/peor caso)","2","2 escenarios: mejor y peor caso")])], tail=("evid",))
add("/mapea", "Mapea", "Mapa visual de elementos, relaciones, jerarquías y flujos.",
    "Crea un mapa visual del concepto: elementos, relaciones, jerarquías, dependencias, flujos. Formato: [[notacion]].",
    [ip("notacion","Notación",[("texto estructurado compatible con Mermaid o ASCII","auto","texto estructurado compatible con Mermaid o diagrama ASCII"),("Mermaid","Mermaid","sintaxis Mermaid"),("ASCII","ASCII","diagrama ASCII")])], tail=())
add("/pareto", "Pareto", "Aplica 80/20: el 20% que produce el 80% del resultado.",
    "Aplica principio 80/20: identifica el 20% de acciones/factores que producen el 80% del resultado. Presenta como lista priorizada con justificación por ítem.",
    [], tail=("evid","salida"))
add("/verifica", "Verifica", "Verifica cada afirmación contra fuentes y marca nivel de confianza.",
    "Verifica cada afirmación contra fuentes. Marca: verificado / requiere fuente / potencialmente incorrecto. Para lo no verificable, indica nivel de confianza (alto/medio/bajo).",
    [], tail=("salida",))
add("/operacionaliza", "Operacionaliza", "Convierte el plan abstracto en operaciones concretas y medibles.",
    "Convierte el plan abstracto en operaciones concretas: quién hace qué, cuándo, con qué, cómo se mide, dónde se documenta. Cero ambigüedad. Todo ejecutable mañana.",
    [], tail=("salida","tono"))
add("/sintetiza", "Sintetiza", "Unifica múltiples fuentes en 1 documento: solo lo que importa.",
    "De múltiples fuentes o inputs, produce 1 documento unificado. Solo lo que importa. Elimina redundancias, resuelve contradicciones, mantiene la esencia. Máx [[limite]].",
    [ip("limite","Límite",[("1 página","1 página","1 página"),("½ página","½ página","media página"),("2 páginas","2 páginas","2 páginas")])], tail=("idioma",))
add("/segmenta", "Segmenta", "Divide en segmentos manejables con entregable parcial por bloque.",
    "Divide en segmentos manejables con criterio lógico. Cada segmento: nombre, alcance, dependencias, entregable parcial. Presenta como plan de trabajo segmentado.",
    [], tail=("salida",))
add("/escenarios", "Escenarios", "3 escenarios alternativos con supuestos, implicaciones y acciones.",
    "Genera [[n]] escenarios alternativos para la situación. Para cada uno: supuestos, implicaciones, acciones recomendadas, probabilidad estimada.",
    [ip("n","Escenarios",[("3 (conservador, base, agresivo)","3","3 escenarios: conservador, base y agresivo"),("2 (base, agresivo)","2","2 escenarios: base y agresivo")])], tail=("evid",))
add("/prototipa", "Prototipa", "MVP descartable: lo mínimo para validar la idea.",
    "Versión mínima viable. Lo suficiente para validar la idea o concepto. Rápido, funcional, descartable. Identifica: qué valida este prototipo y qué NO valida.",
    [], tail=("tono",))
add("/escala", "Escala", "Diseña para 10x volumen: qué se rompe y qué automatizar.",
    "Toma lo que funciona y disénalo para [[factor]] volumen. Identifica: qué se rompe al escalar, qué necesita cambiar, qué automatizar. Presenta plan de escalamiento progresivo.",
    [ip("factor","Factor",[("10x","10x","10x"),("2x","2x","2x"),("100x","100x","100x")])], tail=("tono",))
add("/aterriza", "Aterriza", "De lo abstracto a acción, fecha, responsable y entregable medible.",
    "De lo abstracto a lo concreto. Cada concepto se traduce en: acción específica, fecha, responsable, entregable medible. Cero generalidades.",
    [], tail=("salida",))
add("/conecta", "Conecta", "Encuentra relaciones, patrones e insights de segundo orden.",
    "Encuentra relaciones entre conceptos aparentemente separados. Mapea conexiones, patrones transversales y sinergias. Presenta como [[salida_conecta]].",
    [ip("salida_conecta","Salida",[("mapa de relaciones o insight de segundo orden","mapa/insight","mapa de relaciones o insight de segundo orden"),("lista de conexiones","lista","lista de conexiones"),("diagrama","diagrama","diagrama de relaciones")])], tail=())
add("/auditoria", "Auditoría", "Revisión exhaustiva: marca completo/faltante/incorrecto por severidad.",
    "Revisión exhaustiva y sistemática. Marca cada elemento: completo / faltante / incorrecto. Presenta hallazgos ordenados por severidad. Incluye recomendaciones de corrección.",
    [], tail=("salida",))
add("/narrativa", "Narrativa", "Transforma datos en historia con arco situación-tensión-resolución.",
    "Transforma datos, hechos o análisis en historia con arco narrativo: situación > tensión > resolución. Conecta con emociones y acciones. El dato cuenta la historia, la historia mueve a la acción.",
    [], tail=("tono","idioma"))
add("/benchmark", "Benchmark", "Compara contra mejores prácticas del sector con gaps y quick wins.",
    "Compara contra mejores prácticas del sector o industria. Identifica gaps, oportunidades de mejora y quick wins. Formato: métrica > tu estado > mejor práctica > gap > acción.",
    [], tail=("evid",))
add("/diagnostica", "Diagnostica", "Diagnóstico de situación: fortalezas, fallas, síntomas y causas.",
    "Análisis de situación actual. Fortalezas (qué funciona), debilidades (qué falla), síntomas (qué se observa), causas (por qué pasa). Formato: diagnóstico + prescripción.",
    [], tail=("evid","tono"))
add("/estrategia", "Estrategia", "Visión de largo plazo: objetivo, palancas, trade-offs y riesgos.",
    "Visión de largo plazo. Define: objetivo estratégico, palancas clave, trade-offs, riesgos, timeline. Conecta con recursos disponibles y restricciones reales.",
    [], tail=("ext","tono"))
add("/feedback", "Feedback", "Feedback SBI: Situación, Comportamiento, Impacto + pedido de cambio.",
    "Feedback SBI estructurado: Situación (cuándo/dónde), Comportamiento (qué observaste, hechos), Impacto (qué efecto tuvo). Cierra con pedido de cambio concreto y espacio para diálogo.",
    [], tail=("tono",))
add("/reversa", "Reversa", "Ingeniería inversa de la sesión: priming + SPEC de 1 paso.",
    "Ingeniería inversa. Analiza el historial completo de esta sesión. Genera: 1 prompt de priming (contexto + rol) + 1 SPEC de alto rendimiento (que produzca el mismo resultado en 1 paso). Listos para copiar.",
    [], tail=("idioma",))
add("/defiende", "Defiende", "Prepara defensa: anticipa objeciones con respuesta y evidencia.",
    "Prepara argumentos defensivos para la posición actual. Anticipa [[objeciones]] probables. Para cada una: objeción, respuesta fundamentada, evidencia de soporte. Formato: tabla de objeciones-respuestas.",
    [ip("objeciones","Objeciones",[("5 objeciones","5","5 objeciones"),("3 objeciones","3","3 objeciones"),("10 objeciones","10","10 objeciones")])], tail=("evid",))

# ===== /a–/z — macros =====
add("/a", "A · Aprobar — Proceder", "Aprueba y procede con el plan presentado, repasando insights clave.",
    "Aprobado. Proceder con el plan presentado. Repasa los insights clave antes de avanzar con lo operativo.", [], tail=("tono",))
add("/b", "B · Buscar info", "Investiga fuentes complementarias y entrega briefing con fuentes.",
    "Busca información adicional. Investiga fuentes complementarias, datos recientes y perspectivas alternas. Presenta hallazgos como briefing ejecutivo con fuentes.", [], tail=("ext","idioma"))
add("/c", "C · Corregir", "Corrige ortografía, gramática y claridad; entrega versión limpia.",
    "Corrige y mejora: ortografía, gramática, coherencia, tono y claridad. Entrega versión limpia sin marcas de cambio. Si hay ambigüedades, resuelve a favor de la claridad.", [], tail=("idioma",))
add("/d", "D · Desglosar", "Descompone en componentes fundamentales con dependencias.",
    "Desglosa en partes. Descompone en componentes fundamentales. Cada parte con: definición, relevancia y dependencias. Presenta como [[salida_d]].",
    [ip("salida_d","Formato",[("árbol o mapa","árbol/mapa","árbol o mapa"),("lista jerárquica","lista","lista jerárquica"),("tabla","tabla","tabla")])], tail=())
add("/e", "E · Excelencia — Bucle 10/10", "Bucle de excelencia: rúbrica de 10 criterios, itera hasta 10/10.",
    "Bucle de Excelencia. Define rúbrica interna con 10 criterios: fundamento, veracidad, calidad, densidad, simplicidad, claridad, precisión, profundidad, coherencia, utilidad. Autoevalúa, itera hasta [[meta]] y entrega solo la versión final.",
    [ip("meta","Meta",[("10/10","10/10","10/10 en todos"),("9/10","9/10","mínimo 9/10"),("8/10","8/10","mínimo 8/10")])], tail=())
add("/f", "F · Formatear", "Aplica formato profesional escaneable en 5 segundos.",
    "Formatea profesionalmente. Aplica headers, bullets, tablas, negritas, separadores lógicos. El resultado debe ser escaneable y ejecutivo en 5 segundos.", [], tail=("tono",))
add("/g", "G · Generar alternativas", "5+ alternativas en tabla con enfoque, ventaja y trade-off.",
    "Genera [[n]] alternativas. Cada una con: nombre descriptivo, enfoque, ventaja principal, trade-off. Presenta en tabla comparativa.",
    [ip("n","Cantidad",[("5+","5+","5 o más"),("3","3","3"),("10","10","10")])], tail=())
add("/h", "H · Hacer checklist", "Checklist accionable y verificable, ordenado por prioridad.",
    "Haz checklist accionable. Cada ítem: acción concreta, verificable, con responsable implícito y resultado esperado. Ordena por prioridad de impacto.", [], tail=("salida",))
add("/i", "I · Identificar contexto", "Resume objetivo, decisiones, temas abiertos y próximos pasos.",
    "Identifica contexto completo de esta conversación. Resume: objetivo principal, decisiones tomadas, temas abiertos, supuestos activos, próximos pasos. Formato: briefing.", [], tail=("idioma",))
add("/j", "J · Justificar", "Cada afirmación con dato, fuente, marco o razonamiento explícito.",
    "Justifica con evidencia. Cada afirmación o recomendación debe tener: dato, fuente, marco teórico, caso de referencia o razonamiento lógico explícito.", [], tail=("evid",))
add("/k", "K · Key takeaways", "5-7 insights con implicación y acción sugerida.",
    "Key takeaways. Extrae [[n]] insights más importantes. Cada uno: insight + implicación + acción sugerida. Formato escaneable.",
    [ip("n","Cantidad",[("5-7","5-7","5-7"),("3","3","3"),("10","10","10")])], tail=())
add("/l", "L · Pros y contras", "Evalúa ventajas y desventajas con ponderación y recomendación.",
    "Lista pros y contras. Evalúa objetivamente ventajas y desventajas. Incluye ponderación de impacto (alto/medio/bajo) por punto. Cierra con recomendación.", [], tail=("tono",))
add("/m", "M · Mejorar", "Eleva el último entregable: más profundidad, estructura y precisión.",
    "Mejora significativamente. Toma el último entregable y elévalo: más profundidad, mejor estructura, datos más sólidos, redacción más precisa. Entrega solo la versión mejorada.", [], tail=("evid","tono"))
add("/n", "N · Next step", "La acción inmediata más valiosa con máxima concreción.",
    "Next step. Identifica la acción inmediata más valiosa. Describe: qué, quién, cuándo, con qué recursos, resultado esperado. Máxima concreción.", [], tail=("idioma",))
add("/o", "O · Organizar cronológico", "Timeline ordenado con hitos, dependencias y fechas.",
    "Organiza cronológicamente. Crea timeline o secuencia ordenada. Incluye hitos, dependencias y fechas estimadas cuando sea posible.", [], tail=("salida",))
add("/p", "P · Profundizar", "Expande a nivel experto senior con ejemplos y matices.",
    "Profundiza. Expande con mayor detalle, ejemplos concretos, datos de soporte, casos reales y matices no explorados. Nivel: experto senior.", [], tail=("evid","idioma"))
add("/q", "Q · Preguntar lo que falta", "Identifica preguntas críticas no formuladas y brechas.",
    "Pregunta lo que falta. Identifica preguntas críticas NO formuladas. Brechas de información que podrían cambiar conclusiones o mejorar significativamente el resultado.", [], tail=("idioma",))
add("/r", "R · Resumen ejecutivo", "3 párrafos: conclusión, evidencia, próximos pasos.",
    "Resume ejecutivo. Máx [[parrafos]]. Conclusión y recomendación; evidencia y fundamento; próximos pasos concretos.",
    [ip("parrafos","Extensión",[("3 párrafos","3 párrafos","3 párrafos"),("1 párrafo","1 párrafo","1 párrafo"),("5 bullets","5 bullets","5 viñetas")])], tail=("idioma",))
add("/s", "S · Sintetizar opciones", "Consolida la mejor solución integrando fortalezas.",
    "Sintetiza opciones abiertas. Consolida la mejor solución integrando fortalezas de todas las alternativas y mitigando debilidades de cada una.", [], tail=("tono",))
add("/t", "T · Traducir", "Traduce preservando tono y matices; solo la traducción.",
    "Traduce [[direccion]] manteniendo tono, intención y matices culturales. Solo la traducción, sin explicaciones.",
    [ip("direccion","Dirección",[("al otro idioma","auto","al otro idioma"),("ES→EN","ES→EN","del español al inglés profesional"),("EN→ES","EN→ES","del inglés al español profesional")])], tail=())
add("/u", "U · Unificar", "De múltiples versiones, un documento único y coherente.",
    "Unifica y consolida. De múltiples fragmentos o versiones, crea documento único coherente. Elimina redundancias, resuelve contradicciones, asegura flujo narrativo.", [], tail=("idioma",))
add("/v", "V · Validar veracidad", "Marca OK / requiere confirmación / potencialmente incorrecto.",
    "Valida veracidad y consistencia. Marca cada afirmación: OK / Requiere confirmación / Potencialmente incorrecto. Sugiere correcciones donde aplique.", [], tail=("salida",))
add("/w", "W · What if", "3 escenarios con condiciones de activación e impacto.",
    "What if. Genera [[n]] escenarios: optimista, pesimista, más probable. Cada uno con: condiciones de activación, impacto esperado, acciones recomendadas.",
    [ip("n","Escenarios",[("3","3","3"),("2 (mejor/peor)","2","2: mejor y peor caso")])], tail=("evid",))
add("/x", "X · Extraer datos", "Extrae nombres, fechas, cifras y compromisos en formato estructurado.",
    "Extrae datos clave en formato estructurado. Nombres, fechas, cifras, métricas, compromisos, decisiones. Presenta en [[salida_x]].",
    [ip("salida_x","Formato",[("tabla o JSON según sea más útil","auto","tabla o JSON según sea más útil"),("tabla","tabla","tabla"),("JSON","JSON","JSON")])], tail=())
add("/y", "Y · Revisión final", "Revisión pre-entrega: completitud, formato, parámetros resueltos.",
    "Ya casi — revisión final pre-entrega. Verifica: completitud, consistencia, formato, ortografía, parámetros resueltos, listo para uso inmediato.", [], tail=("tono",))
add("/z", "Z · Zoom out", "Perspectiva estratégica: panorama, implicaciones sistémicas.",
    "Zoom out. Perspectiva estratégica. Conecta con el panorama general: objetivos de largo plazo, implicaciones sistémicas, qué estamos pasando por alto.", [], tail=("ext",))

# ---------- criterio de aceptación + límite/caso borde por comando ----------
# crit = qué debe cumplir la salida para ser buena. edge = cómo manejar ambigüedad/falta de datos / qué NO hacer.
CE = {
"/0": ("Reformulas rol, objetivo y restricciones sin que yo corrija; las preguntas son bloqueantes, no cosméticas.", "Ante ambigüedad pregunta, no asumas. No ejecutes nada en este paso."),
"/1": ("La frase Qué + Para Qué + Para Quién es aprobable sin edición.", "Si la idea es vaga, marca qué falta antes de validar; no la completes inventando."),
"/2": ("El SPEC es ejecutable por un tercero sin contexto extra.", "Si un campo S/P/E/C queda supuesto, decláralo explícito en vez de rellenarlo."),
"/3": ("Cada fase tiene entrada, salida y criterio de hecho; dependencias y riesgos visibles.", "No planifiques sobre supuestos no confirmados; márcalos como riesgo."),
"/4": ("Draft completo, sin secciones vacías; pendientes marcados, no omitidos.", "Si falta un dato usa [PENDIENTE] y continúa; no inventes para rellenar."),
"/5": ("Cada dato con fuente o marcado como estimación; ejemplos verificables.", "No agregues longitud sin sustancia; si no hay fuente, dilo."),
"/6": ("El output es más corto que el input sin perder lo esencial.", "No elimines matices que cambian la decisión."),
"/7": ("Cada punto del checklist con veredicto y evidencia; las fallas se enrutan a 5/6.", "No marques OK por defecto: criterio que no aplica, justifícalo."),
"/8": ("Usable sin edición por la audiencia destino; formato del Criterio aplicado.", "Si el Criterio (C) no se definió, pídelo antes de cerrar."),
"/9": ("Los 2 prompts reproducen el resultado de hoy en 1 paso.", "Si el historial es insuficiente, indica qué falta para reusarlo."),
"/compara": ("Scoring justificado por celda; la recomendación se deriva de los totales, no de preferencia.", "Opción sin dato en un criterio: márcala, no asumas 0 implícito."),
"/prioriza": ("El #1 es defendible ante un escéptico; cada ítem con un porqué accionable.", "Si faltan datos para puntuar, pídelos o marca el supuesto; no inventes prioridad."),
"/reformula": ("Mismo significado, mejor forma; cero cambios de fondo sin señalar.", "Si detectas un error de fondo, sepáralo de la reescritura."),
"/debate": ("Cada postura con su mejor argumento; la síntesis no es un empate tibio.", "No fuerces equidistancia si la evidencia inclina a un lado."),
"/investiga": ("Cada hallazgo con [FUENTE]; gaps explícitos; cero afirmación sin soporte.", "Sin fuente fiable, dilo; no rellenes con datos plausibles."),
"/documenta": ("Estructura navegable, metadata completa, archivable sin edición.", "Datos faltantes en metadata: marcados, no inventados."),
"/diagrama": ("Sintaxis válida y renderizable; relaciones correctas.", "Si el concepto no es diagramable, propón el tipo más fiel y dilo."),
"/evalua": ("Cada dimensión puntuada con razón; total y recomendación coherentes.", "Criterio sin evidencia: declara la confianza, no inventes el número."),
"/optimiza": ("Cada mejora con impacto estimado y costo; ordenadas por ratio beneficio/esfuerzo.", "No propongas optimización sin un cuello de botella identificado."),
"/automatiza": ("Por oportunidad: herramienta, ROI en h/semana y complejidad.", "Si un paso exige juicio humano, no lo marques automatizable."),
"/desafia": ("Ataca supuestos, no estilo; cada riesgo con cómo se manifiesta.", "Implacable con la idea, no con la persona."),
"/calibra": ("El registro coincide con la audiencia sin perder exactitud.", "Si la audiencia no está clara, pregúntala antes de calibrar."),
"/resume": ("Conclusión accionable primero; nada esencial omitido.", "No introduzcas información ausente del original."),
"/traduce": ("Preserva intención, tono y términos técnicos; suena nativo.", "Término sin equivalente: mantenlo y aclara entre paréntesis."),
"/profundiza": ("Aporta capas no obvias: datos, casos, contraposturas.", "No infles con generalidades; cada párrafo agrega algo nuevo."),
"/simplifica": ("Más corto que el input, idea intacta.", "No simplifiques al punto de volverlo incorrecto."),
"/contextualiza": ("Conecta antecedentes y por qué importa ahora, sin perder foco.", "No derives en historia irrelevante; ata todo al caso."),
"/cuantifica": ("Cada cualitativo con número, rango u orden de magnitud y su base.", "Sin dato: estimación fundamentada y marcada, no cifra inventada."),
"/visualiza": ("Tipo, layout y jerarquía suficientes para producir el visual.", "Si los datos no soportan el gráfico, propón otro."),
"/personaliza": ("Cada recomendación referencia rol, sector o restricción real.", "Falta contexto del usuario: pídelo, no generalices."),
"/estructura": ("Pirámide MECE: sin solapes ni huecos; conclusión arriba.", "Si los elementos no son MECE, reagrupa y dilo."),
"/argumenta": ("Tesis + soporte con evidencia + contraargumento anticipado.", "No afirmes sin dato o razonamiento explícito."),
"/predice": ("Cada escenario con condiciones, probabilidad e implicación.", "Extrapola con base; sin señal, dilo, no adivines."),
"/mapea": ("Nodos, relaciones y jerarquías completos; sintaxis válida.", "Relación incierta: márcala como hipótesis."),
"/pareto": ("El 20% identificado con justificación de su peso.", "Si la distribución no es 80/20, repórtalo, no la fuerces."),
"/verifica": ("Cada afirmación etiquetada (verificado/duda/incorrecto) + confianza.", "No marques verificado sin fuente; lo dudoso se separa."),
"/operacionaliza": ("Quién, qué, cuándo y cómo se mide por acción; ejecutable mañana.", "Acción sin responsable o métrica está incompleta: márcala."),
"/sintetiza": ("1 documento; contradicciones resueltas; esencia intacta.", "Conflicto entre fuentes: decláralo y resuélvelo, no lo ocultes."),
"/segmenta": ("Segmentos con entregable parcial y dependencias claras.", "No crees dependencias circulares entre segmentos."),
"/escenarios": ("Conservador, base y agresivo con supuestos y probabilidad.", "Supuestos explícitos; sin ellos el escenario no sirve."),
"/prototipa": ("MVP que valida la hipótesis nombrada; dice qué NO valida.", "No sobre-construyas; descartable por diseño."),
"/escala": ("Qué se rompe a 10x y qué cambiar/automatizar, por capa.", "No asumas que lo actual escala lineal."),
"/aterriza": ("Cada concepto a acción, fecha, responsable y entregable medible.", "Generalidad sin dueño no está aterrizada."),
"/conecta": ("Conexiones no obvias con el porqué de la relación.", "No fuerces vínculos espurios; calidad sobre cantidad."),
"/auditoria": ("Cada elemento completo/faltante/incorrecto + severidad + fix.", "Hallazgo sin evidencia: bájalo a observación."),
"/narrativa": ("Arco situación-tensión-resolución fiel a los datos.", "La historia no distorsiona el dato; emoción sin manipular."),
"/benchmark": ("Métrica > tu estado > mejor práctica > gap > acción, con fuente.", "Compara contra un benchmark aplicable, no contra uno inaplicable."),
"/diagnostica": ("Síntomas y causas separados; la prescripción se liga a la causa.", "No confundas síntoma con causa raíz."),
"/estrategia": ("Objetivo, palancas, trade-offs y riesgos atados a recursos reales.", "Sin restricciones reales no es estrategia, es deseo."),
"/feedback": ("SBI con hechos observables; pedido de cambio concreto.", "Describe comportamiento, no etiquetas de carácter."),
"/reversa": ("Priming + SPEC que reproducen el resultado en 1 paso.", "Historial insuficiente: indica qué falta."),
"/defiende": ("Cada objeción con respuesta fundamentada y evidencia.", "Anticipa la objeción más fuerte, no la más fácil."),
"/a": ("Confirmas los insights clave antes de pasar a lo operativo.", "Si algo del plan es dudoso, señálalo antes de proceder."),
"/b": ("Briefing con fuentes recientes y perspectivas alternas.", "Sin fuente fiable, dilo; no rellenes."),
"/c": ("Versión limpia; ambigüedades resueltas a favor de la claridad.", "Cambio de fondo (no de forma): sepáralo y avísame."),
"/d": ("Componentes con definición, relevancia y dependencias.", "Parte incierta: márcala, no la fuerces."),
"/e": ("Rúbrica de 10 aplicada; iteras hasta la meta; entregas solo la versión final.", "No entregues borradores intermedios."),
"/f": ("Escaneable y ejecutivo en 5 segundos; jerarquía clara.", "No cambies el contenido al formatear."),
"/g": ("Alternativas distintas con ventaja y trade-off, en tabla.", "Variantes reales, no la misma idea reescrita."),
"/h": ("Ítems accionables, verificables, ordenados por impacto.", "Ítem no verificable: reformúlalo."),
"/i": ("Objetivo, decisiones, abiertos, supuestos y próximos pasos.", "Marca lo que no quedó claro en la sesión."),
"/j": ("Cada afirmación con dato, fuente, marco o razonamiento.", "Sin soporte: márcalo como supuesto."),
"/k": ("Cada insight con su implicación y acción.", "Takeaway sin acción es observación, no clave."),
"/l": ("Ventajas y desventajas ponderadas + recomendación.", "No omitas el contra incómodo."),
"/m": ("Eleva profundidad, estructura y precisión; solo la versión final.", "No degrades lo que ya funcionaba."),
"/n": ("La acción inmediata de mayor palanca, con qué, quién y cuándo.", "Una sola acción, no una lista."),
"/o": ("Timeline con hitos, dependencias y fechas.", "Fecha incierta: estímala y márcala."),
"/p": ("Detalle experto con ejemplos y matices nuevos.", "No repitas lo dicho con más palabras."),
"/q": ("Preguntas críticas no formuladas que cambian conclusiones.", "Prioriza las bloqueantes sobre las cosméticas."),
"/r": ("Conclusión + evidencia + próximos pasos en 3 párrafos.", "No agregues información nueva."),
"/s": ("Mejor solución integrando fortalezas y mitigando debilidades.", "Si las opciones son incompatibles, dilo y elige."),
"/t": ("Tono e intención preservados; suena nativo.", "Término sin equivalente: mantén y aclara."),
"/u": ("Documento único coherente; contradicciones resueltas.", "Conflicto entre fuentes: resuélvelo explícito."),
"/v": ("OK/confirmar/incorrecto por afirmación + corrección.", "No marques OK sin base."),
"/w": ("3 escenarios con activación, impacto y acción.", "Supuestos explícitos por escenario."),
"/x": ("Datos estructurados (tabla/JSON) completos y fieles.", "Dato ausente: vacío marcado, no inventado."),
"/y": ("Completitud, consistencia y formato listos para uso.", "Si algo bloquea la entrega, detente y señálalo."),
"/z": ("Conexión con objetivos de largo plazo e implicaciones sistémicas.", "No pierdas el caso concreto al abstraer."),
}
CE_DEFAULT = ("Salida accionable, completa y sin afirmaciones sin respaldo.",
              "Ante ambigüedad o falta de datos, pregunta o marca el supuesto; no inventes.")

# ---------- render + scaffolds ----------
def render(body, params):
    """Sustituye [[key]] por el texto del default -> prosa limpia (sin tokens)."""
    out = body
    for p in params:
        txt = next((o[2] for o in p["opts"] if o[0] == p["def"]), "")
        out = out.replace("[[%s]]" % p["key"], txt)
    return re.sub(r'[ \t]{2,}', ' ', re.sub(r'[ \t]+\n', '\n', out)).strip()

def val_of(p):
    """Valor de default a mostrar en la versión 'parámetros' (texto inyectado o etiqueta)."""
    o = next((o for o in p["opts"] if o[0] == p["def"]), p["opts"][0])
    return o[2] if o[2] else o[1]

def alt_labels(p):
    return [o[1] for o in p["opts"] if o[0] != p["def"]]

def clean_params(params):
    """Quita tokens de presentación; opts solo informan la versión 'parámetros' y la explicación UI."""
    out = []
    for p in params:
        out.append({"key": p["key"], "label": p["label"], "def": p["def"],
                    "opts": [[o[0], o[1]] for o in p["opts"]]})  # opts ligeros (v,label) para UI
    return out

def mk_natural(body, params, crit, edge):
    return "%s\n\nCriterio: %s\nEvita: %s\n\n%s" % (render(body, params), crit, edge, PROTO)

def mk_parametros(desc, params, crit, edge):
    lines = ["PARÁMETROS (edita los valores a tu caso):"]
    for p in params:
        alts = alt_labels(p)
        extra = ("   ·alt: " + " | ".join(alts)) if alts else ""
        lines.append("· %s: %s%s" % (p["label"], val_of(p), extra))
    return ("%s\n\n%s\n\nEjecuta usando exactamente esos parámetros.\n\n"
            "Criterio de aceptación: %s\nLímites: %s\n\n%s") % (desc, "\n".join(lines), crit, edge, PROTO)

def mk_spec(desc, body, params, crit, edge):
    fmt = next((p for p in params if p["key"] in ("formato", "salida")), None)
    fmt_txt = (val_of(fmt) + "; ") if fmt else ""
    return ("[S] Situación: el contenido o la tarea que te comparto.\n"
            "[P] Pedido: %s\n"
            "[E] Ejecución: %s Evita: %s\n"
            "[C] Criterio: %s%s\n\n%s") % (desc, render(body, params), edge, fmt_txt, crit, PROTO)

def mk_dupla(title, body, params, crit, edge):
    return {
        "system": ("Eres un asistente experto de MetodologIA para «%s». Aplicas el método con criterios explícitos. "
                   "Guardrail: %s\n\n%s") % (title, edge, PROTO),
        "user": "%s\n\nCriterio: %s" % (render(body, params), crit)
    }

def main():
    data = json.load(open(DATA, encoding='utf-8'))
    bycmd = {r.get('command'): r for r in data}
    miss = [c for c in S if c not in bycmd]
    if miss:
        print("WARN comandos no encontrados:", miss)
    n = 0
    fillers = [P_idioma, P_tono, P_ext, P_evid]   # garantiza 2–4 parámetros
    for cmd, (title, desc, body, params) in S.items():
        r = bycmd.get(cmd)
        if not r:
            continue
        params = list(params)
        keys = {p["key"] for p in params}
        fi = 0
        while len(params) < 2 and fi < len(fillers):
            p = fillers[fi](); fi += 1
            if p["key"] in keys:
                continue
            keys.add(p["key"]); params.append(p); body += "[[%s]]" % p["key"]
        crit, edge = CE.get(cmd, CE_DEFAULT)
        r['title'] = title
        r['desc'] = desc
        r['params'] = clean_params(params)                                  # metadato de explicación (read-only)
        r['crit'] = crit; r['edge'] = edge                                  # trazabilidad: criterio + límite
        r['formats']['natural'] = mk_natural(body, params, crit, edge)      # prosa lista para pegar
        r['formats']['natural_params'] = mk_parametros(desc, params, crit, edge)  # parámetros explícitos
        r['formats']['spec'] = mk_spec(desc, body, params, crit, edge)      # andamiaje S·P·E·C
        r['formats']['dupla'] = mk_dupla(title, body, params, crit, edge)   # system/user con guardrail
        n += 1
    if not os.path.exists(DATA + '.bak'):
        shutil.copy(DATA, DATA + '.bak')   # preserva el original (no sobrescribir en re-runs)
    json.dump(data, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print("Actualizados %d/%d prompts. Backup: biblioteca-data.json.bak" % (n, len(S)))

if __name__ == '__main__':
    main()
