# Lab y producción

> Estado: propuesto (2026-11-21). Decisión en [ADR-0005](../decisions/0005-lab-y-produccion-en-mismo-repo.md).

Tengo ideas continuamente. El lab es donde se prueban usando los mismos recursos que producción, sin poder romperla.

## Reglas

1. **Dependencias en un solo sentido.** `lab/` y `apps/` importan `harness`; `harness` nunca importa nada de `lab/`.
2. **Mismos recursos.** El lab usa el mismo cliente de Ollama, perfiles de modelos, telemetría y runner de evals. `lab/sandbox.py` los deja listos en una línea.
3. **Probar sin promover.** Un experimento puede registrar tools o workflows con `channel: lab`. El harness real los ejecuta solo con `harness --lab`.

## Anatomía de un experimento

```
lab/experiments/2026-11-voice-commands/
  README.md   # hipótesis, estado, resultados, decisión
  run.py      # usa harness como librería
```

Plantilla del README:

```markdown
# <Nombre del experimento>
- Estado: idea | probando | candidato | promovido | descartado
- Hipótesis: …
- Cómo se prueba: …
- Resultados: (tabla de evals, latencia, notas)
- Decisión: por qué se promovió o se descartó
```

## Checklist para promover a producción

- [ ] El código se movió a `packages/` y no depende de nada en `lab/`
- [ ] Tiene tests
- [ ] Tiene una eval con resultados aceptables en mis modelos
- [ ] Cada tool tiene nivel de permiso y sensibilidad declarados
- [ ] El README del experimento registra la decisión
- [ ] Hay un ADR si la promoción cambia el diseño
