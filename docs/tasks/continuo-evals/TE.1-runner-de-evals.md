# TE.1: Runner de evals

- **Fase:** continua (no bloquea fases)
- **Estado:** Pendiente
- **Depende de:** T1.3

## Objetivo

Un comando que corre una suite de casos contra varios perfiles y produce una tabla de precisión y latencia, para decidir con datos qué modelo hace qué tarea.

## Contexto mínimo

- **Evals ≠ tests.** Los tests comprueban que el código funciona (sin Ollama). Las evals miden qué tan bien resuelve un modelo real una tarea. Son lentas, las corre el usuario a mano y sus resultados no hacen fallar el build.
- **Suite en YAML** (`evals/<suite>.yaml`):

  ```yaml
  name: saludo
  kind: chat            # chat | structured | tool_call
  cases:
    - input: "hola"
      check: { type: contains_any, values: ["hola", "Hola"] }
    - input: "responde solo con el número: 2+2"
      check: { type: equals, value: "4" }
  ```

  Verificadores iniciales: `equals`, `contains_any`, `json_field` (para `structured`) y `tool_called` (para `tool_call`). Agregar más solo cuando una suite los necesite.
- **Métricas** por perfil: aciertos/total, latencia p50 y máxima, tokens/s de salida.
- **Resultados:** `.harness/evals/<suite>-<fecha>.jsonl` (detalle por caso) y una tabla Markdown en la terminal, lista para pegar en el README de un experimento del lab.
- **Privacidad:** las evals respetan el router. Un caso privado nunca se evalúa contra un perfil cloud: se marca `skipped`.

## Alcance

**Incluye:** `harness.evals` (carga de suites, verificadores, runner), `harness eval <suite> [--profiles a,b,c]`, una suite de ejemplo (`saludo`).

**Fuera de alcance:** las suites reales (TE.2), gráficas, comparación histórica.

## Archivos y carpetas

- `packages/harness/src/harness/evals/{__init__,suite,checks,runner}.py` (crear)
- `evals/saludo.yaml` (crear)
- `apps/cli/src/harness_cli/main.py` (subcomando `eval`)
- `tests/test_evals.py` (crear)

## Pasos de implementación

1. Modelos Pydantic de suite y caso.
2. Verificadores.
3. Runner por perfil, secuencial (un solo modelo a la vez en CPU).
4. Tabla de salida.

## Output esperado

```text
> uv run harness eval saludo --profiles light,standard,fast
perfil    aciertos  p50     máx     tok/s
light     2/2       1.1 s   1.4 s   18.2
standard  2/2       2.3 s   2.9 s   9.7
fast      1/2       3.0 s   3.8 s   7.1
```

## Tests mínimos

- `test_evals.py::test_runner_con_fake`: con `FakeProvider`, una suite de 2 casos produce 1 acierto y 1 fallo esperados y una tabla con las columnas correctas.

## Verificación (la corre el usuario)

```powershell
uv run pytest tests/test_evals.py
```

```powershell
uv run harness eval saludo --profiles light,standard,fast
```

## Criterios de aceptación

- [ ] El comando corre contra perfiles reales y produce la tabla.
- [ ] Los casos privados no se mandan a perfiles cloud.

## Telemetría

- Cada caso es un run con su `trace_id`, marcado `eval: <suite>` en `run_started`.

## Seguridad

- Las suites versionadas no llevan datos personales reales; usar datos inventados.

## Decisiones abiertas

Ninguna.

## Referencias (solo si hay dudas)

- [Principios: medir antes de opinar](../../architecture/overview.md#principios)
- [Lab y producción](../../architecture/lab.md)

## Notas de implementación

