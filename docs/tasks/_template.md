# T<fase>.<n>: <Título>

- **Fase:** <n>
- **Estado:** Pendiente | En curso | En revisión | Hecha
- **Depende de:** <IDs o —>

## Objetivo

Qué debe existir al terminar, en una o dos frases.

## Contexto mínimo

Solo lo necesario para implementar sin leer otros documentos: decisiones que aplican, nombres, formatos, restricciones.

## Alcance

**Incluye:**
- …

**Fuera de alcance:**
- …

## Archivos y carpetas

- `ruta/` (crear | modificar | mover)

## Pasos de implementación

1. …

## Output esperado

Lo que el usuario puede ver o ejecutar al final.

## Tests mínimos

Los tests que el agente escribe (el usuario los corre). Sin Ollama ni Windows real salvo que se marque `@pytest.mark.ollama`.

- `tests/...::test_...`: qué comprueba.

## Verificación (la corre el usuario)

```powershell
uv run pytest
```

## Criterios de aceptación

- [ ] …

## Telemetría

Eventos que esta tarea agrega y qué no se debe registrar. "Ninguna" si no aplica.

## Seguridad

Solo si aplica.

## Decisiones abiertas

Preguntas para el usuario antes de implementar esa parte. "Ninguna" si no hay.

## Referencias (solo si hay dudas)

- [doc](../../architecture/...)

## Notas de implementación

La rellena el agente al dejar la tarea En revisión: qué hizo, qué decidió fuera de lo previsto, qué quedó pendiente.
