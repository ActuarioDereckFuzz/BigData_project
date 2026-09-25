# Decisiones técnicas

Este registro conserva el contexto de decisiones que no debe perderse entre sesiones. Para cada decisión, anota el motivo y las consecuencias prácticas.

## D-001 — Docker como entorno principal

- **Fecha:** 2026-09-24
- **Decisión:** usar Docker y Docker Compose para ejecutar el entorno de Spark.
- **Motivo:** reduce diferencias entre equipos, facilita repetir ejercicios y deja una base portable para el portafolio.
- **Consecuencia:** la instalación local directa no será el camino principal; Docker Desktop y WSL2 deben estar operativos.

## D-002 — Empezar con Spark local/single-node

- **Fecha:** 2026-09-24
- **Decisión:** aprender y validar PySpark en una única máquina antes de crear un clúster.
- **Motivo:** permite aislar conceptos fundamentales y depurar con menos componentes.
- **Consecuencia:** no se introducirá configuración de varios nodos hasta que el flujo local esté comprendido y documentado.

## D-003 — Versiones base

- **Fecha:** 2026-09-24
- **Decisión:** JDK 17, Spark/PySpark 4.1.3 y Hadoop 3.4.2.
- **Motivo:** son las versiones definidas para este proyecto.
- **Consecuencia:** cualquier incompatibilidad encontrada se documentará aquí antes de cambiar una versión.

## D-004 — Separar exploración y código reutilizable

- **Fecha:** 2026-09-24
- **Decisión:** usar `notebooks/` para aprendizaje y `src/` para lógica que se reutilice.
- **Motivo:** conserva el razonamiento didáctico sin convertir el proyecto en una colección de notebooks difíciles de mantener.
- **Consecuencia:** cuando un notebook estabilice un proceso, se extrae a un módulo o script en `src/`.
