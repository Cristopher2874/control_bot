# ADR-0005: Lab y producción en el mismo repo

- **Estado:** Aceptado
- **Fecha:** 2026-11-21
- **Sesión:** [2026-11-21 diagnóstico y arquitectura](../sessions/2026-11-21-diagnostico-y-arquitectura.md)

## Contexto

Tengo ideas que quiero probar constantemente usando los recursos del harness (Ollama, config, telemetría), y algunas acabarán en producción. En el proyecto anterior el lab y el código real estaban mezclados.

## Decisión

Un workspace de uv con `packages/harness` (librería), `apps/` (producción) y `lab/` (experimentos). El lab importa el harness, nunca al revés. Los experimentos pueden registrarse con `channel: lab` y activarse con `--lab`. Hay una checklist explícita para promover. Detalle en [lab](../architecture/lab.md).

## Alternativas consideradas

- **Repo separado para el lab:** duplicaría config y obligaría a publicar el harness como paquete.
- **Ramas de git por experimento:** se pierden de vista y no comparten mejoras del núcleo.

## Consecuencias

- Experimentar cuesta pocas líneas y no rompe producción.
- Hay que respetar la regla de dependencias (conviene un test o lint que lo verifique).
