# Estado del Proyecto Big Data

> Este archivo es la fuente de verdad operativa del proyecto. Actualízalo al cerrar una sesión de trabajo para que cualquier chat pueda retomar el avance.

## Objetivo del proyecto

Aprender de forma profunda los fundamentos de Big Data y construir un proyecto demostrable con Python, PySpark y Docker. Se empezará en modo local/single-node y solo después se explorarán componentes distribuidos y un clúster.

## Estado actual

- **Fase:** 0 — Preparación y estructura.
- **Entorno objetivo:** Windows 11 + WSL2 Ubuntu + Docker.
- **Repositorio:** estructura y documentación inicial creadas.
- **Validación pendiente:** construir la imagen y confirmar que `pyspark` inicia dentro del contenedor.

## Configuración acordada

- JDK 17
- Spark y PySpark 4.1.3
- Hadoop 3.4.2
- Docker como entorno reproducible
- Ejecución inicial: Spark local, un solo nodo

## Siguiente acción concreta

Construir el contenedor y ejecutar una sesión de PySpark. Después, crear un notebook o script mínimo que lea datos de `data/samples/`, haga una transformación sencilla y escriba el resultado en `data/processed/`.

## Última actualización

- Fecha: 2026-09-24
- Cambio: se creó la estructura base del repositorio y la documentación de continuidad.

## Bitácora breve

| Fecha | Cambio | Resultado |
| --- | --- | --- |
| 2026-09-24 | Inicialización del espacio de trabajo | Pendiente validar Docker y PySpark |

## Bloqueos o preguntas abiertas

- Confirmar que Docker Desktop y la integración con WSL2 están disponibles.
- Elegir un conjunto de datos pequeño y público para el primer ejercicio.
