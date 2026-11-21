# ADR-0002: Ciclo de agente propio sobre Ollama

- **Estado:** Aceptado
- **Fecha:** 2026-11-21
- **Sesión:** [2026-11-21 diagnóstico y arquitectura](../sessions/2026-11-21-diagnostico-y-arquitectura.md)

## Contexto

Con modelos chicos (1 a 8B) en CPU, las fallas más comunes son tool calls mal formadas, JSON inválido y bucles. Hace falta controlar el prompt, el parseo, los reintentos y la salida estructurada. Ollama ya ofrece `tools` y `format` (JSON schema que restringe la salida) en su API nativa.

## Decisión

Escribir un ciclo de agente propio (~150 líneas) sobre la API nativa de Ollama, con Pydantic para los schemas. No usar LangChain ni LangGraph.

## Alternativas consideradas

- **LangGraph:** ya se usaba; mucha abstracción que oculta por qué falla un modelo chico.
- **PydanticAI:** ligero y tipado; razonable, pero con menos control sobre el ciclo.

## Consecuencias

- Control total y depuración directa con las trazas.
- Hay que mantener el ciclo, el parseo de tool calls y la lógica de reintentos.
- El proveedor queda detrás de un `Protocol`, así que se puede agregar un adaptador OpenAI-compatible (llama.cpp, LM Studio) sin tocar el ciclo.
