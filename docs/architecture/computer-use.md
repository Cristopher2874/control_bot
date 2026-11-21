# Computer use

> Estado: propuesto (2026-11-21). Se implementa en la Fase 2.

Primera capability del harness. Un modelo de 2 a 8B controlando el PC es la parte más delicada del sistema, así que el diseño empieza por la seguridad.

## Acciones tipadas, no shell libre

El modelo elige una acción y rellena argumentos validados; nunca escribe comandos de PowerShell.

| Tool | Permiso | Notas |
|---|---|---|
| `list_windows()` | read | |
| `focus_window(title)` | act | |
| `open_app(name)` | act | `name` contra una lista de apps conocidas |
| `set_volume(level)` | act | rango 0–100 |
| `run_script(name)` | dangerous | solo scripts de una allowlist |

> Lista inicial; se ajusta al implementar la Fase 2.

## Capas de interacción

Se usa la capa más estable que resuelva la acción:

1. **APIs y comandos del sistema** (PowerShell, Win32).
2. **UI Automation** con pywinauto: lee los controles reales de Windows.
3. **pyautogui** con coordenadas: último recurso. El bot anterior empezaba aquí, que es la capa más frágil.

## Protecciones

- **Dry-run:** muestra lo que haría sin ejecutarlo.
- **Kill switch:** una tecla o `/stop` cancela el run en curso.
- **Auditoría:** cada acción `act` o `dangerous` queda registrada con su run.
- **Confirmación:** todo lo `dangerous` pregunta antes.
- **Privacidad:** `data_sensitivity: private`, así que todo run de computer use es local.

## Criterio de terminado (Fase 2)

"Abre Spotify y sube el volumen" funciona desde la CLI, pide confirmación donde corresponde y deja traza y auditoría.
