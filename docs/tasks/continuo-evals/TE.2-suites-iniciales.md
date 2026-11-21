# TE.2: Suites iniciales

- **Fase:** continua
- **Estado:** Pendiente
- **Depende de:** TE.1, T3.2 (y T2.4 para la suite de computer use)

## Objetivo

Tener suites para las tres decisiones que dependen del modelo, una línea base medida en el hardware real y, con esos datos, ajustar qué perfil usa cada paso.

## Contexto mínimo

- **Suites:**

  | Suite | Tipo | Qué mide | Perfiles a comparar |
  |---|---|---|---|
  | `sensibilidad` | structured | Clasificador `private/public` (T3.2). ~30 casos, mitad y mitad, con frases ambiguas | light, standard |
  | `seleccion_workflow` | structured | Selector de workflows y los Fill de computer use (T2.4). ~15 peticiones | light, standard, fast |
  | `tool_calls` | tool_call | Si el modelo pide la tool correcta con argumentos válidos (T2.1). ~10 casos | standard, fast |

- **Lo más importante es la suite de sensibilidad:** un falso `public` es una fuga posible. Se reporta aparte la tasa de falsos `public` y debe ser 0 para aceptar un perfil como clasificador.
- **Resultados** en un experimento del lab: `lab/experiments/<fecha>-evals-linea-base/README.md` con la tabla de cada suite y la decisión.
- **Si los resultados piden cambiar perfiles** (por ejemplo, que el clasificador use `standard` en vez de `light`), el cambio en `config/models.yaml` o `policy.yaml` se propone al usuario y no se aplica solo.

## Alcance

**Incluye:** las tres suites, la corrida de línea base (la hace el usuario) y el README del experimento.

**Fuera de alcance:** evals de chat o de calidad de redacción, evals automáticas en CI.

## Archivos y carpetas

- `evals/sensibilidad.yaml`, `evals/seleccion_workflow.yaml`, `evals/tool_calls.yaml` (crear)
- `lab/experiments/<fecha>-evals-linea-base/README.md` (crear)
- `packages/harness/src/harness/evals/` (solo si hace falta un verificador nuevo, por ejemplo la tasa de falsos `public`)

## Pasos de implementación

1. Escribir los casos con datos inventados.
2. Agregar al reporte de la suite `sensibilidad` la tasa de falsos `public`.
3. El usuario corre las suites y pega los resultados. El agente redacta la decisión en el README.

## Output esperado

Tres tablas en el README del experimento y una recomendación de perfil por paso.

## Tests mínimos

Ninguno nuevo, salvo que se agregue un verificador (un test para él).

## Verificación (la corre el usuario)

```powershell
uv run harness eval sensibilidad --profiles light,standard
```

```powershell
uv run harness eval seleccion_workflow --profiles light,standard,fast
```

```powershell
uv run harness eval tool_calls --profiles standard,fast
```

## Criterios de aceptación

- [ ] Las tres suites corren y tienen resultados registrados en el lab.
- [ ] La tasa de falsos `public` está reportada por perfil.
- [ ] Hay una recomendación explícita de perfiles, aprobada o rechazada por el usuario.

## Telemetría

Ninguna nueva.

## Seguridad

- Ningún caso usa datos personales reales.

## Decisiones abiertas

Ninguna.

## Referencias (solo si hay dudas)

- [Lab: anatomía de un experimento](../../architecture/lab.md#anatomía-de-un-experimento)

## Notas de implementación

