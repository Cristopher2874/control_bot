# 2026-11-21: Diagnóstico y arquitectura

- **Rama:** `claude/local-models-harness-architecture-035d14` (worktree de Claude; solo documentación)
- **Fase:** 0 (diseño)

## Objetivo

Entender el estado del proyecto `pei_control_bot` y definir la estrategia y la arquitectura para reiniciarlo como un harness de modelos locales.

## Qué se hizo

### 1. Diagnóstico del código existente

El flujo real era: Telegram → `orchestrator.handle_message` → `LLMRouter` (Needle) → tool `write_essay` → `LLMService` (LangChain + Ollama, sin tools) → `.md`/`.pdf` en `llm_gens/`.

Problemas encontrados:

1. Dos stacks de agente compitiendo (Needle + LangChain), con un import circular esquivado por un import diferido.
2. Singletons instanciados al importar, uno de ellos cargando el modelo Needle.
3. `commands_service` acoplado a los tipos de Telegram.
4. Modelo activo global aunque la documentación decía "por chat"; bug en `chat_id_var.set(trace_id_var)`.
5. README y `FEATURES.md` describían archivos inexistentes (`config.py`, `bot_commands.py`, `features/`).
6. Código muerto o de laboratorio mezclado: `app/mcp.py`, `lab/`, `response.json`, salidas en `llm_gens/` versionadas, `AgentLoggingHandler` duplicado.
7. Riesgos menores: `topic` usado como nombre de archivo, rutas fijas al escritorio en `word_tools`, `docx` y `python-docx` juntos en las dependencias, `psutil` sin declarar.

Hardware detectado (por `llm_gens/quality control`): solo CPU, nivel medio-bajo.

### 2. Preguntas de diseño y respuestas

| Pregunta | Respuesta |
|---|---|
| Tareas prioritarias | Computer use primero, luego chat. Además, un lab permanente para probar ideas con los recursos del harness |
| Interfaz principal | CLI primero, Telegram después |
| Rol de la nube | Según la tarea y la privacidad: lo privado (p. ej. ubicación) local; preguntas generales o tareas pesadas, cloud |
| Ciclo de agente | Propio |

Más tarde se añadió el requisito de que el sistema sea modular para sumar API calls y control de hardware.

### 3. Arquitectura resultante

- [Visión general y capas](../architecture/overview.md)
- [Capabilities](../architecture/capabilities.md)
- [Enrutamiento por privacidad](../architecture/privacy-routing.md)
- [Lab y producción](../architecture/lab.md)
- [Computer use](../architecture/computer-use.md)

## Decisiones

- [ADR-0001](../decisions/0001-reiniciar-como-harness.md) Reiniciar como harness modular
- [ADR-0002](../decisions/0002-ciclo-de-agente-propio.md) Ciclo de agente propio
- [ADR-0003](../decisions/0003-enrutamiento-por-privacidad.md) Enrutamiento por privacidad
- [ADR-0004](../decisions/0004-capabilities-como-plugins.md) Capabilities como plugins
- [ADR-0005](../decisions/0005-lab-y-produccion-en-mismo-repo.md) Lab y producción en el mismo repo
- [ADR-0006](../decisions/0006-cli-primero.md) CLI primero

## Problemas y aprendizajes

- La sesión corrió en un worktree de Claude; el trabajo de implementación seguirá en `master` desde una sesión nueva sin worktree.

## Pendiente

- [x] Llevar esta documentación a `master` (commit `5a2093a`)
- [ ] Abrir sesión nueva sobre `master` e iniciar la [Fase 1](../roadmap.md#fase-1-base-y-cli)
- [ ] Resolver las preguntas abiertas de [capabilities](../architecture/capabilities.md#preguntas-abiertas)
