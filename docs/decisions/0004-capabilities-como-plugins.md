# ADR-0004: Capabilities como plugins con contrato común

- **Estado:** Aceptado
- **Fecha:** 2026-11-21
- **Sesión:** [2026-11-21 diagnóstico y arquitectura](../sessions/2026-11-21-diagnostico-y-arquitectura.md)

## Contexto

El harness empieza con computer use, pero después tendrá chat, APIs externas y control de hardware. Agregar cada una no debe obligar a modificar el motor.

## Decisión

Toda habilidad se agrega como capability: manifest + tools + workflows + drivers. Un registry las descubre y valida; el router y el agent loop solo conocen el contrato. Detalle en [capabilities](../architecture/capabilities.md).

## Alternativas consideradas

- **Tools sueltas registradas a mano:** es lo que hacía el bot anterior; sin permisos ni metadatos de privacidad.
- **Servidores MCP para todo:** útil como adaptador futuro, pero agrega procesos y latencia para lo que corre en la misma máquina.

## Consecuencias

- Capabilities nuevas sin tocar el núcleo, y el lab usa el mismo mecanismo.
- Permisos y sensibilidad quedan declarados y se pueden auditar.
- MCP puede entrar después como un tipo de driver o capability adaptadora.
