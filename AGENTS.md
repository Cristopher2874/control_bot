# AGENTS.md

Instrucciones para cualquier agente (Claude Code u otro) que trabaje en este repo. Son reglas de trabajo, no de arquitectura: el diseño vive en `docs/`.

## Qué es este proyecto

Un harness modular en Python para usar modelos locales de Ollama (solo CPU, hardware medio-bajo) en tareas: computer use en Windows, chat con memoria y, más adelante, APIs y hardware. Workspace de uv: `packages/harness` (librería), `apps/` (interfaces), `lab/` (experimentos). El código del bot anterior está en `legacy/` (o todavía en la raíz si la tarea T1.1 no se ha hecho).

## Cómo se trabaja: una tarea a la vez

1. **Empieza por la tarea, no por la documentación.** El usuario te indica una tarea de `docs/tasks/` (por ejemplo `T1.2`). Lee **solo** ese archivo. Contiene el objetivo, el contexto mínimo, los archivos a tocar y los criterios de aceptación.
2. **No leas toda la carpeta `docs/` al iniciar.** Abre un documento de `docs/architecture/` o `docs/decisions/` solo si la tarea lo enlaza y de verdad tienes una duda que la tarea no resuelve. Lee la sección que necesitas, no el archivo completo si es largo. No leas `docs/sessions/` salvo que el usuario lo pida.
3. **Quédate dentro del alcance.** Si algo queda fuera de la sección "Fuera de alcance" o no está en la lista de archivos, no lo hagas: anótalo como nota al cerrar la tarea. Si la tarea tiene "Decisiones abiertas", pregúntalas al usuario antes de implementar esa parte.
4. **No ejecutes los tests por defecto.** Escribe el código y los tests que pide la tarea y detente. El usuario corre los comandos de "Verificación" y te trae los resultados. Solo ejecuta tests, `ruff` o `pyright` si el usuario lo aprueba explícitamente en esa sesión. Comandos baratos que no son tests (por ejemplo `uv sync` o `uv run python -c "import harness"`) se pueden correr si hacen falta para avanzar.
5. **Cierra la tarea en estado "En revisión".** Al terminar: cambia el estado en el archivo de la tarea a `En revisión`, rellena su sección "Notas de implementación" (qué hiciste, qué decidiste fuera de lo previsto, qué quedó pendiente) y dale al usuario la lista de comandos de verificación. La tarea pasa a `Hecha` solo cuando el usuario lo aprueba.
6. **Si el usuario trae fallas**, corrígelas dentro del alcance de la misma tarea. Si la causa está en otra tarea, dilo antes de tocarla.
7. **Commits:** pequeños, en `master`, solo cuando el usuario lo pida. Un commit por tarea aprobada es lo normal.

## Sin sobreingeniería

- **Tests mínimos.** Prueban que la funcionalidad sirve, no la forma del código. Un test por comportamiento importante o riesgo real (fuga de privacidad, permiso ignorado, parseo de tool calls). Nada de tests de getters, de dataclasses triviales ni de formato.
- **Los tests no necesitan Ollama ni tocar Windows.** Usa el proveedor falso y los drivers simulados. Lo que requiere el modelo real se marca `@pytest.mark.ollama` y el usuario lo corre aparte.
- **Construye solo lo que pide la tarea actual.** Nada de abstracciones "por si acaso", hooks, configuraciones o capas que ninguna tarea usa todavía.
- **Dependencias:** solo las que la tarea lista. Si necesitas otra, pregunta.

## Telemetría

- Crece con las tareas: cada tarea dice qué eventos agrega. No construyas telemetría por adelantado.
- **Nunca registres:** tokens o API keys, contenido de `.env`, prompts o respuestas completas con datos privados, ni salidas crudas de tools del PC. Registra metadatos (modelo, perfil, latencia, tokens contados, motivo de enrutamiento, nombre de la tool, resultado ok/error) y pasa todo por la redacción de secretos.
- La telemetría (trazas JSONL para entender un run) y los tests (comprobar que el código funciona) son cosas distintas. No uses los tests para inspeccionar trazas ni las trazas como sustituto de un test.

## Seguridad

Hoy todo es local y por CLI, así que basta con lo básico. Ten presente lo que viene después.

- **Ahora:** secretos solo por variables de entorno o `.env` (nunca en el código, en YAML versionado ni en prompts). `.env`, trazas y bases de datos locales no se versionan. Lo privado no sale a un perfil `cloud` (ver la política de privacidad). Las tools de computer use son acciones tipadas con allowlists, nunca shell libre.
- **Después (Telegram, APIs, hardware):** allowlist de usuarios de Telegram, credenciales de APIs desde la config, límites físicos en drivers de hardware, revisión de qué datos manda cada capability fuera de la máquina. Las tareas de esas fases lo detallan.

## Comandos del proyecto

Los corre el usuario salvo aprobación (ver regla 4):

```powershell
uv run pytest
```

```powershell
uv run ruff check .
```

```powershell
uv run pyright
```

## Mapa de la documentación (consultar solo si hace falta)

- `docs/tasks/`: tareas por fase. **Punto de entrada.**
- `docs/architecture/`: cómo es el sistema. `docs/decisions/`: por qué (ADRs).
- `docs/roadmap.md`: fases. `docs/glossary.md`: términos.
- Reglas para escribir docs: `docs/README.md`.
