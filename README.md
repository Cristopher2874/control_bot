# PEI Harness

Harness modular en Python para usar modelos locales de Ollama (solo CPU, hardware medio-bajo) en tareas concretas: computer use en Windows, chat con memoria y, más adelante, APIs y hardware. Lo privado se queda en local; las capacidades se agregan como plugins.

El código del bot anterior está en `legacy/`, solo como referencia.

## Instalación

```powershell
uv sync
```

## Objetivo de la Fase 1

```powershell
uv run harness chat "hola"
```

Responde con un modelo local y deja una traza JSONL del run (todavía no implementado, ver T1.3).

## Documentación

- [Tareas](docs/tasks/README.md): punto de entrada para trabajar en el repo.
- [Arquitectura](docs/architecture/overview.md)
