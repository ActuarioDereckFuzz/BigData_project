# Roadmap de aprendizaje

El avance no consiste solo en “hacer que funcione”. Cada fase debe dejar una nota, ejercicio o resultado que explique qué se aprendió y cómo se verificó.

## Fase 0 — Entorno reproducible

- [x] Definir versiones y estructura del repositorio.
- [ ] Construir la imagen Docker.
- [ ] Iniciar una consola de PySpark dentro del contenedor.
- [ ] Ejecutar un trabajo mínimo con datos de muestra.

**Aprendizaje esperado:** qué aportan Java, Spark, PySpark, Docker y WSL2 al entorno local.

## Fase 1 — Fundamentos de Spark

- [ ] Crear una `SparkSession`.
- [ ] Entender driver, executors, jobs, stages y tasks.
- [ ] Practicar DataFrames, esquemas y tipos de datos.
- [ ] Diferenciar transformaciones de acciones.
- [ ] Observar ejecución con `explain()` y la interfaz de Spark cuando aplique.

**Entregable:** notebook de fundamentos con ejemplos reproducibles.

## Fase 2 — Procesamiento de datos

- [ ] Leer CSV y JSON con esquemas explícitos.
- [ ] Limpiar, filtrar, agrupar y unir datos.
- [ ] Escribir Parquet y comparar con CSV.
- [ ] Crear un pipeline pequeño de datos crudos a procesados.

**Entregable:** script en `src/` y datos de ejemplo documentados.

## Fase 3 — Rendimiento y buenas prácticas

- [ ] Comprender particiones y `shuffle`.
- [ ] Usar `cache`/`persist` con criterio.
- [ ] Comparar estrategias de joins.
- [ ] Medir una mejora y documentar la evidencia.

**Entregable:** nota técnica en `docs/` con antes/después.

## Fase 4 — Arquitectura Big Data

- [ ] Relacionar almacenamiento, procesamiento por lotes y orquestación.
- [ ] Introducir conceptos de HDFS/Hadoop sin confundirlos con Spark.
- [ ] Diseñar una arquitectura de referencia para el proyecto.

**Entregable:** diagrama y explicación de arquitectura.

## Fase 5 — Distribución y clúster

- [ ] Simular varios servicios/nodos con Docker Compose.
- [ ] Comprender modos local, standalone y cluster.
- [ ] Ejecutar un trabajo distribuido pequeño.

**Entregable:** guía de ejecución y limitaciones del entorno local.

## Fase 6 — Proyecto final y portafolio

- [ ] Elegir un problema y datos públicos.
- [ ] Construir pipeline reproducible de extremo a extremo.
- [ ] Agregar pruebas, documentación y resultados.
- [ ] Preparar README para GitHub.

**Entregable:** repositorio presentable, ejecutable y explicado.
