# Documentación técnica del harness

Documentación viva del proyecto. Se escribe poco a poco: cada sesión de trabajo, cada decisión y cada cambio de diseño deja su rastro aquí.

## Estructura

| Carpeta / archivo | Qué contiene | Cuándo se actualiza |
|---|---|---|
| [tasks/](tasks/) | **Punto de entrada para implementar.** Tareas por fase, tipo ticket, autocontenidas | Al planear una fase y al cerrar cada tarea |
| [architecture/](architecture/) | Cómo está diseñado el sistema **hoy** | Cuando cambia el diseño o se construye una pieza nueva |
| [decisions/](decisions/) | ADRs: una decisión por archivo, con contexto y alternativas | Cada vez que se toma una decisión no obvia |
| [sessions/](sessions/) | Bitácora: qué se hizo en cada sesión y qué quedó pendiente | Al cerrar cada sesión de trabajo |
| [roadmap.md](roadmap.md) | Fases, estado y criterio de terminado | Al avanzar o replanear una fase |
| [glossary.md](glossary.md) | Términos del proyecto (capability, run, lab…) | Cuando aparece un término nuevo |

## Índice de arquitectura

- [Visión general y capas](architecture/overview.md)
- [Capabilities (plugins)](architecture/capabilities.md)
- [Enrutamiento por privacidad](architecture/privacy-routing.md)
- [Lab y producción](architecture/lab.md)
- [Computer use](architecture/computer-use.md)

## Reglas para escribir docs

1. **`architecture/` describe el presente.** Si algo cambia, se edita el documento; el porqué del cambio va en un ADR nuevo.
2. **Los ADRs no se reescriben.** Si una decisión cambia, se crea un ADR nuevo que la reemplaza y el viejo se marca `Reemplazado por ADR-XXXX`.
3. **Cada sesión deja una bitácora** en `sessions/AAAA-MM-DD-tema.md` usando la [plantilla](sessions/_template.md).
4. **Lo que todavía no existe se marca.** Usa `> Estado: propuesto`, `> Estado: en construcción` o `> Estado: implementado` al inicio de cada documento de arquitectura.
5. **Una tarea no obliga a leer el resto de docs.** Su "Contexto mínimo" resume lo necesario; las referencias son para dudas. Las reglas de trabajo de los agentes están en [AGENTS.md](../AGENTS.md).
6. Los diagramas van en Mermaid dentro del Markdown, así se versionan con el código.
