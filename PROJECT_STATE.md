# Estado del proyecto — Big Data con PySpark y Docker

**Actualizado:** 2026-10-15  
**Fase actual:** **05 — Optimización y rendimiento (por iniciar)**  
**Último hito cerrado:** **04 — Limpieza, transformación e integración**  
**Avance global orientativo:** **55 %**  
**Estado general:** operativo en local mediante contenedor Docker; falta optimización, consolidación de automatización y cierre de portafolio.

## Resumen ejecutivo

El proyecto ya dispone de entorno Spark reproducible, formación práctica mediante notebooks, fuentes reales NYC Taxi y NOAA, procesos de limpieza e integración, persistencia Parquet y validaciones de calidad. La prioridad siguiente es **medir y optimizar** las operaciones costosas antes de consolidar la ejecución integral como pipeline reutilizable.

## Estado por fase

| Fase | Estado | Observación |
|---|---|---|
| 01. Docker y entorno | ✅ Terminada | Construcción de imagen y smoke tests funcionales |
| 02. Fundamentos Spark | ✅ Terminada | Notebooks didácticos y ETL inicial |
| 03. Ingesta y exploración | ✅ Terminada | NYC Taxi 2024 + NOAA, profiling y EDA |
| 04. Limpieza e integración | ✅ Terminada | Parquet procesado y controles de calidad |
| 05. Optimización | ⏭️ Siguiente | Definir línea base de rendimiento |
| 06. Persistencia avanzada | 🟡 Parcial | Parquet ya se utiliza; falta consolidar estrategia |
| 07. Pipeline final | 🟡 Parcial | Procesos desarrollados; falta orquestación integral reutilizable |
| 08. Escalamiento | ⬜ Pendiente | Sin evidencia de ejecución multinodo |
| 09. Documentación y portafolio | ⬜ Pendiente | README final, dependencias y resultados técnicos |

## Entorno técnico validado

- **Contenedor:** Docker, imagen `bigdata-spark:0.1`.
- **Runtime:** Python 3.11.16, OpenJDK 17, Spark/PySpark 4.1.3 y Hadoop 3.4.2.
- **Ejecución:** entorno Linux dentro de Docker, con archivos del repositorio montados desde el host.
- **Pruebas:** SparkSession, DataFrames y persistencia de Parquet confirmados.

## Datos y resultados confirmados en el seguimiento

| Indicador | Valor |
|---|---:|
| NYC Taxi 2024 — registros originales | 41,169,720 |
| NYC Taxi — columnas originales | 19 |
| Taxi — registros fuera de 2024 | 56 |
| Taxi — discrepancia mes de archivo/fecha | 420 |
| Taxi — registros 2024 tras filtro de fecha | **41,169,664** |
| NOAA Central Park — observaciones originales | 1,826 |
| NOAA — fechas de 2024 | 366 |
| Viajes integrados con meteorología | **41,169,664** |
| Viajes con `AWND` faltante | **428,126** |
| Controles de validación finales | **7/7 PASS** |

**Decisión de calidad:** los nulos de `AWND` se conservan porque provienen de fechas sin registro meteorológico; no se imputan sin justificar el método.

## Productos actuales

- Datos Taxi y NOAA ingeridos y explorados.
- Transformaciones y unión temporal Taxi–NOAA ejecutadas en PySpark.
- Datasets limpios e integrados persistidos en Parquet.
- Notebooks de las fases 01–04 y resultados de controles finales.
- Documentación de seguimiento: `ROADMAP.md`, `PROJECT_STATE.md` y demás archivos del repositorio.

## Próximas acciones — orden sugerido

1. **Abrir Fase 05** y fijar un conjunto de pruebas reproducible (dataset, equipo, configuración, operaciones y métricas).
2. Medir línea base de lecturas, limpieza, unión y escrituras; guardar planes `explain` y duración.
3. Optimizar únicamente los cuellos de botella demostrados y comparar contra la misma línea base.
4. Actualizar `ROADMAP.md` y este estado con resultados cuantitativos al cerrar la fase.
5. Seguir con consolidación de persistencia, pipeline automatizado, escalamiento y documentación de portafolio.

## Riesgos y decisiones abiertas

- **Rendimiento:** aún no hay una comparativa reproducible de tiempos y recursos antes/después.
- **Automatización:** el flujo no debe presentarse como pipeline de producción/orquestado hasta contar con un punto de entrada y pruebas integrales.
- **Escalamiento:** usar Spark en Docker/local no demuestra por sí solo un clúster multinodo.
- **Calidad:** conservar trazabilidad entre registros originales, exclusiones por fecha y valores meteorológicos faltantes.
- **Dependencias y documentación:** revisar `requirements.txt`, README y comandos de ejecución antes del cierre.

## Definición del siguiente hito

**Fase 05 cerrada** cuando exista un informe breve y reproducible con configuración Spark, mediciones base, cambios ensayados, resultados comparativos, planes físicos relevantes y conclusión técnica sustentada.

**Roadmap detallado:** [`ROADMAP.md`](ROADMAP.md).
