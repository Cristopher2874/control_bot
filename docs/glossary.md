# Glosario

| Término | Significado |
|---|---|
| **Harness** | El sistema completo: orquesta modelos locales (y en la nube) para completar tareas. |
| **Capability** | Un módulo enchufable (plugin) que agrega una familia de habilidades: computer use, chat, APIs, hardware. Ver [capabilities](architecture/capabilities.md). |
| **Manifest** | La declaración de una capability: nombre, versión, canal, permisos de cada tool y sensibilidad de sus datos. |
| **Tool** | Una acción tipada que el modelo puede pedir (`open_app(name)`). Es lo único de una capability que ve el modelo. |
| **Workflow** | Una receta determinista para una tarea conocida; el LLM solo rellena pasos concretos. |
| **Driver** | El código que toca el mundo real (pywinauto, PowerShell, HTTP, serial). Va detrás de una interfaz para poder simularlo. |
| **Registry** | El componente del motor que descubre, valida y expone las capabilities. |
| **Run** | Una ejecución completa de una petición, de principio a fin, con su traza. |
| **Evento** | Algo que ocurre durante un run (`model_call`, `tool_call`, `final`…). Las interfaces y la telemetría se suscriben a ellos. |
| **Perfil de modelo** | La configuración de un modelo: nombre en Ollama, `locality`, `num_ctx`, temperatura, si soporta tools. |
| **Locality** | `local` o `cloud`: dónde se ejecuta un modelo. |
| **Sensibilidad** | `private` o `public`: la clasificación de un dato o de un run. |
| **Contexto contaminado** | Un run que ya contiene datos privados; queda fijado a modelos locales hasta el final. |
| **Canal** | `stable` (producción) o `lab` (experimental, solo con `--lab`). |
| **Nivel de permiso** | `read` (sin preguntar), `act` (se audita) o `dangerous` (siempre pide confirmación). |
