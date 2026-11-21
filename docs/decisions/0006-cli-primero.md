# ADR-0006: CLI primero, Telegram como adaptador

- **Estado:** Aceptado
- **Fecha:** 2026-11-21
- **Sesión:** [2026-11-21 diagnóstico y arquitectura](../sessions/2026-11-21-diagnostico-y-arquitectura.md)

## Contexto

El bot anterior solo se podía usar y probar por Telegram, lo que hacía lenta la depuración y acoplaba la lógica a la interfaz.

## Decisión

La CLI es la interfaz principal durante el desarrollo. Telegram llega en la Fase 5 como un adaptador delgado sobre el runtime y el bus de eventos.

## Alternativas consideradas

- **Telegram desde el inicio:** útil desde el celular, pero frena la iteración.
- **API HTTP:** innecesaria por ahora; puede agregarse como otra interfaz.

## Consecuencias

- Iteración rápida y trazas visibles en la terminal.
- El núcleo queda libre de dependencias de interfaz desde el principio.
