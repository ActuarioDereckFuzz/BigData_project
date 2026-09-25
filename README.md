# Proyecto Big Data: aprendizaje con PySpark y Docker

Este repositorio documenta un recorrido práctico para aprender fundamentos de ingeniería de datos y Big Data. El entorno será reproducible con Docker y el primer objetivo es trabajar correctamente en una sola máquina antes de pasar a un clúster.

## Objetivo

Construir, entender y documentar un flujo de datos con Python y PySpark. Al final, el repositorio debe poder servir como pieza de portafolio en GitHub: claro para una persona que aprende y verificable para quien lo revise.

## Tecnología base

| Componente | Versión o decisión |
| --- | --- |
| Sistema anfitrión | Windows 11 + WSL2 (Ubuntu) |
| Entorno reproducible | Docker / Docker Compose |
| Java | JDK 17 |
| Apache Spark | 4.1.3 |
| PySpark | 4.1.3 |
| Hadoop | 3.4.2 |
| Lenguaje de práctica | Python |

## Cómo está organizado

```text
.
├── src/                 # Código Python reutilizable
├── notebooks/           # Experimentos y ejercicios explicados
├── data/
│   ├── raw/             # Datos originales (no se versionan si son grandes)
│   ├── processed/       # Datos generados por los procesos
│   └── samples/         # Muestras pequeñas, seguras para Git
├── docs/                # Notas, guías y diagramas
├── docker/              # Archivos para construir el entorno
├── README.md            # Entrada al proyecto
├── PROJECT_STATE.md     # Estado actual y siguiente paso
├── ROADMAP.md           # Ruta de aprendizaje
└── DECISIONS.md         # Decisiones técnicas y su motivo
```

## Primeros pasos

1. Instala y habilita Docker Desktop con integración para WSL2.
2. Desde la raíz del repositorio, construye el entorno:

   ```bash
   docker compose build
   ```

3. Abre una consola de PySpark:

   ```bash
   docker compose run --rm spark pyspark
   ```

4. Consulta [PROJECT_STATE.md](PROJECT_STATE.md) para continuar desde el punto real del proyecto, no desde suposiciones.

> Aún no hay un clúster ni un flujo de producción. Esta etapa prioriza entender Spark local, el modelo de ejecución y transformaciones antes de añadir complejidad.

## Forma de trabajo

- Cada sesión que cambie el avance actualiza `PROJECT_STATE.md`.
- Cada decisión técnica relevante se registra en `DECISIONS.md`.
- Los notebooks sirven para aprender; el código que se reutilice pasa a `src/`.
- No se suben datos sensibles ni archivos grandes a Git.

## Próximo paso

Validar que el contenedor inicia PySpark y ejecutar un ejemplo mínimo de lectura, transformación y escritura con un archivo de muestra.
