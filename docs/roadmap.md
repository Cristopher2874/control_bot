# Roadmap

Cada fase deja algo que ya se puede ejecutar. Marca las casillas al avanzar y enlaza la bitácora de la sesión donde se cerró.

| Fase | Estado | Sesión de cierre |
|---|---|---|
| 1. Base + CLI | Pendiente | |
| 2. Agent loop + computer use | Pendiente | |
| 3. Política de privacidad | Pendiente | |
| 4. Chat con memoria | Pendiente | |
| 5. Telegram + cola de jobs | Pendiente | |
| Continuo. Evals en el lab | Pendiente | |

## Fase 1: base y CLI

- [ ] Workspace de uv: `packages/harness`, `apps/cli`, `lab/`
- [ ] Código viejo movido a `legacy/`
- [ ] ruff, pytest y pyright configurados
- [ ] `core`: dataclasses Task, Message, ToolCall, Run, Event
- [ ] Proveedor Ollama detrás de `Protocol`, con perfiles local/cloud en `models.yaml`
- [ ] Telemetría: trazas JSONL por run, redacción de secretos
- [ ] Contrato de capabilities y registry (vacío)
- [ ] `lab/sandbox.py`

**Terminado cuando:** `uv run pytest` pasa y `uv run harness chat "hola"` responde con un modelo local y deja su traza.

## Fase 2: agent loop y computer use

- [ ] Ciclo de agente con tool calls, reintentos y salida estructurada
- [ ] Permisos `read` / `act` / `dangerous`, confirmación en CLI y auditoría
- [ ] Dry-run y kill switch
- [ ] 4 o 5 tools de computer use ([diseño](architecture/computer-use.md))

**Terminado cuando:** "Abre Spotify y sube el volumen" funciona con confirmación donde corresponde.

## Fase 3: política de privacidad

- [ ] Reglas de sensibilidad + clasificador local
- [ ] Contexto contaminado
- [ ] `policy.yaml` y razón de enrutamiento en cada traza

**Terminado cuando:** hay tests que demuestran que nada privado llega a un modelo cloud.

## Fase 4: chat con memoria

- [ ] Conversaciones en SQLite con etiquetas de sensibilidad
- [ ] Armado de contexto que respeta la política

**Terminado cuando:** las conversaciones persisten entre ejecuciones y respetan la política.

## Fase 5: Telegram y cola de jobs

- [ ] Adaptador de Telegram sobre runtime y eventos
- [ ] Confirmaciones con botones
- [ ] Cola de jobs de un solo worker

**Terminado cuando:** lo mismo que la CLI funciona desde el celular.

## Continuo: evals en el lab

- [ ] Runner de evals con tareas en YAML y verificadores
- [ ] Tabla por modelo: precisión, latencia, tokens/s
