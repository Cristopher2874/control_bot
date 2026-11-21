# ADR-0001: Reiniciar el proyecto como harness modular

- **Estado:** Aceptado
- **Fecha:** 2026-11-21
- **Sesión:** [2026-11-21 diagnóstico y arquitectura](../sessions/2026-11-21-diagnostico-y-arquitectura.md)

## Contexto

El proyecto era un bot de Telegram (`pei_control_bot`) que creció sin arquitectura:

- Dos stacks de agente compitiendo: Needle como router y LangChain/LangGraph como agente, este último sin tools (`self.tools = []`). La tool de Needle llamaba de vuelta al servicio de LangChain con un import diferido para esquivar un import circular.
- Singletons creados al importar (`LLMService()`, `LLMRouter()`, que además cargaba el modelo Needle), con efectos secundarios en tests e imports.
- Lógica de comandos acoplada a los tipos de Telegram.
- Estado de modelo global aunque la documentación decía "por chat", y un bug al fijar `chat_id_var` con el objeto ContextVar en lugar de un valor.
- Documentación que describía archivos inexistentes y código de laboratorio mezclado con el real.

El objetivo cambió: un harness para que mis modelos locales completen tareas, empezando por computer use y creciendo hacia APIs y hardware.

## Decisión

Empezar de cero con la arquitectura de [overview](../architecture/overview.md). El código viejo se mueve a `legacy/` para rescatar piezas y se borra cuando ya no haga falta.

Piezas a rescatar: conversión MD→PDF, `telegram_markdown`, ideas de telemetría (trace_id con ContextVar, redacción de secretos, allowlist de módulos), `word_tools` y los alias de modelos.

## Alternativas consideradas

- **Refactorizar sobre el código existente:** el acoplamiento y los dos stacks hacían que casi todo hubiera que reescribir igual.

## Consecuencias

- Diseño limpio desde el inicio, con documentación y decisiones registradas.
- Se pierde temporalmente la funcionalidad del bot de Telegram hasta la Fase 5.
