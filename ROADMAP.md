# Roadmap — Proyecto Big Data con PySpark y Docker

**Última actualización:** 2026-10-15  
**Estado:** en desarrollo  
**Avance global estimado:** **55 %** (estimación orientativa por esfuerzo y entregables)

## Objetivo

Desarrollar un flujo de ingeniería de datos reproducible con **Docker y PySpark** para ingerir, validar, limpiar, integrar y analizar los viajes **NYC Taxi 2024** junto con información meteorológica de **NOAA**. Completar el proyecto con mediciones de rendimiento, ejecución reproducible de extremo a extremo y documentación para portafolio.

## Fases

| Fase | Alcance | Estado | Entregable principal |
|---|---|---|---|
| 00 | Planeación y seguimiento | Continuo | `ROADMAP.md`, `PROJECT_STATE.md` y registro de decisiones |
| 01 | Docker y entorno reproducible | ✅ Completada | Imagen Docker funcional y smoke tests de Spark |
| 02 | Fundamentos PySpark / Spark | ✅ Completada | Notebooks de DataFrames, SQL, joins, ventanas, particiones y ETL didáctico |
| 03 | Ingesta y exploración de datos | ✅ Completada | Ingesta, profiling y EDA de Taxi 2024 y NOAA |
| 04 | Limpieza, transformación e integración | ✅ Completada | Datos limpios e integrados, escritos en Parquet y validados |
| 05 | Optimización y rendimiento | ⏭️ Siguiente | Benchmarks, análisis de planes y mejoras justificadas |
| 06 | Persistencia y formatos Big Data | 🟡 Parcial | Consolidar organización, particionamiento y estrategia de escritura/lectura |
| 07 | Pipeline ETL reproducible | 🟡 Parcial | Orquestar el flujo completo fuera de notebooks exploratorios |
| 08 | Escalamiento / arquitectura distribuida | ⬜ Pendiente | Experimentos o documentación verificable de escalamiento |
| 09 | Documentación final y portafolio | ⬜ Pendiente | README, guía de ejecución, resultados y repositorio presentable |

> **Nota:** las fases 06 y 07 ya tienen componentes desarrollados, pero todavía no cumplen sus criterios de cierre. Los porcentajes no deben calcularse contando fases por igual.

## Hitos alcanzados

- [x] **Entorno:** Docker con Python 3.11, Java 17 y PySpark/Spark 4.1.3; lectura y escritura Parquet verificadas.
- [x] **Fundamentos:** notebooks prácticos sobre ejecución Spark, DataFrames, joins, SQL, I/O, particiones y pipeline ETL introductorio.
- [x] **Datos fuente:** 12 archivos Parquet de NYC Taxi 2024 (**41,169,720** registros originales, 19 columnas) y NOAA Central Park (**1,826** observaciones meteorológicas por variable/fecha).
- [x] **Calidad inicial:** identificados **56** registros Taxi fuera de 2024 y **420** con discrepancia entre mes del archivo y mes del viaje.
- [x] **Transformación e integración:** **41,169,664** viajes dentro de 2024 integrados con información meteorológica; **366** fechas de referencia NOAA.
- [x] **Nulos explicados:** se preservó `AWND` faltante para **428,126** viajes, sin imputación arbitraria.
- [x] **Persistencia y controles:** datasets transformados almacenados en Parquet y **7/7** controles finales de validación reportados como exitosos.

## Próxima fase — 05: Optimización y rendimiento

1. Definir una **línea base**: tiempos, volumen procesado, número/tamaño de particiones y configuración Spark.
2. Revisar los planes de ejecución (`explain`) e identificar **shuffles, joins y escrituras** costosas.
3. Comparar alternativas controladas (`broadcast`, particionamiento, ajustes de shuffle, caché cuando corresponda).
4. Registrar resultados **antes/después**, reproducibilidad, uso de recursos y decisiones técnicas.
5. Conservar la solución más simple que muestre mejoras reales y no degrade la integridad de los datos.

### Criterio de cierre de la fase 05

Benchmark reproducible con configuración explícita, métricas comparables, evidencia de planes de ejecución y conclusiones sobre los cambios que aportan valor.

## Pendientes posteriores

- **06:** fijar convenciones de rutas y particiones, formatos y políticas de reescritura; verificar lectura/escritura sobre distintos volúmenes.
- **07:** ejecutar el ETL completo mediante scripts/módulos reutilizables, con verificaciones y manejo de errores; documentar el comando de ejecución.
- **08:** evaluar si hace falta un entorno multinodo real o basta con experimentos controlados y documentación arquitectónica; no afirmar escalamiento no probado.
- **09:** depurar dependencias, documentar arquitectura, instrucciones, decisiones, benchmarks, limitaciones y resultados del proyecto.

## Alcance y límites

El proyecto **ya demuestra ingesta, transformación, integración y validación de datos a gran escala en PySpark**. Aún no se considera un pipeline de producción completamente automatizado ni se han demostrado mejoras de rendimiento o ejecución multinodo: esos son los próximos entregables.

**Fuente de detalle operativo:** [`PROJECT_STATE.md`](PROJECT_STATE.md).
