# ADR-0003: Enrutamiento local/cloud por privacidad

- **Estado:** Aceptado
- **Fecha:** 2026-11-21
- **Sesión:** [2026-11-21 diagnóstico y arquitectura](../sessions/2026-11-21-diagnostico-y-arquitectura.md)

## Contexto

Quiero usar modelos en la nube (por ejemplo `gemma4:31b-cloud`) para preguntas generales y tareas pesadas, pero mis datos personales (ubicación, archivos, lo que hay en mi PC) no deben salir de la máquina.

## Decisión

El destino de cada paso depende de la sensibilidad de los datos: lo privado va solo a modelos locales, lo público puede ir a la nube si la tarea es pesada. Un run que recibe datos privados queda fijado a local hasta el final (contexto contaminado). Ante la duda, local. Detalle en [privacy-routing](../architecture/privacy-routing.md).

## Alternativas consideradas

- **Solo local:** más simple, pero desperdicia la nube para tareas que la necesitan.
- **Respaldo opcional manual:** depende de que yo recuerde qué es privado.

## Consecuencias

- Las tools y capabilities deben declarar la sensibilidad de lo que devuelven.
- Hace falta un clasificador y tests específicos que demuestren que no hay fugas.
- Computer use siempre corre en local.
