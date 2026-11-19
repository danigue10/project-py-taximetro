# 🚕 TaxiTech Solutions SL — Taxímetro Digital (`TTX-247`)

> **Autor:** Daniel Zamorano García  
> **Formación:** Bootcamp de Inteligencia Artificial — Factoría F5  
> **Cliente / Unidad:** TaxiTech Solutions SL (`TTX-247`)
> **Fecha de entrega:** 19 de noviembre de 2026 
> **Repositorio:** [https://github.com/danigue10/project-py-taximetro](https://github.com/danigue10/project-py-taximetro)
> **Tablero Kanban:** [https://github.com/users/danigue10/projects/1/views/1](https://github.com/users/danigue10/projects/1/views/1)

---

## 1. Contexto y Propósito del Proyecto

El proyecto responde a la necesidad de digitalizar el cálculo de tarifas de un servicio de taxi urbano en Madrid mediante una solución fiable, transparente y fácil de operar en cabina. El sistema contabiliza el tiempo transcurrido en cada estado del trayecto y aplica de forma exacta dos tarifas base por segundo:

| Estado del trayecto | Tarifa por segundo | Equivalencia por minuto |
| :--- | :---: | :---: |
| **Vehículo detenido (espera)** | `0,02 €/s` | `1,20 €/min` |
| **Vehículo en movimiento (en ruta)** | `0,05 €/s` | `3,00 €/min` |

Más allá del núcleo funcional inicial en consola (CLI), la solución se ha estructurado de forma incremental hasta incorporar una interfaz web interactiva para el conductor, una API REST documentada y persistencia relacional en base de datos.

---

## 2. Planificación Ágil y Priorización MoSCoW

El desarrollo se organizó mediante un tablero Kanban aplicando el método MoSCoW para asegurar primero un Producto Mínimo Viable (MVP) plenamente operativo antes de abordar mejoras complementarias:

| Prioridad | Historia | Alcance y Estado de Implementación |
| :--- | :--- | :--- |
| **Must Have** | `US-01` MVP CLI<br>`US-02` Tarifas<br>`US-03` Logs<br>`US-04` Tests | Núcleo de cálculo en Python con cambio dinámico entre `0,02 €/s` y `0,05 €/s`, registro de eventos en archivo de log, persistencia inicial en JSON y pruebas unitarias automatizadas para validar los importes. |
| **Should Have** | `US-05` Interfaz Web<br>`US-06` API y BBDD | Desarrollo de la interfaz visual para el conductor en Streamlit (`app.py`) con controles directos de inicio, cambio de estado, pausa y emisión de ticket final.<br>Implementación de endpoints REST con FastAPI (`main.py`) y base de datos SQLite con SQLAlchemy (`database.py`. |
| **Could Have** | `US-07` Docker | Archivos `Dockerfile` y `docker-compose.yml` preparados en el repositorio. |
| **Won't Have** | `US-08` GPS/TPV | Integración con GPS físico en tiempo real y pasarela de pago con tarjeta (TPV), descartadas conscientemente en esta fase para proteger la estabilidad del MVP. |

---

## 3. Arquitectura del Sistema y Capas

Siguiendo el principio de separación de responsabilidades, el proyecto divide la lógica de presentación, los servicios web y el almacenamiento de datos en módulos independientes:

| Capa / Archivo | Tecnología | Responsabilidad Técnica |
| :--- | :--- | :--- |
| **Interfaz de Conductor** (`app.py`) | Python · Streamlit | Panel operativo en tiempo real con cronómetro en vivo, conmutación entre espera y movimiento, cálculo acumulado y generación de resumen final de carrera. |
| **Backend y API REST** (`main.py`) | FastAPI · Uvicorn | Exposición de endpoints HTTP para consulta y registro de trayectos, con validación de esquemas y documentación interactiva automática en Swagger (`/docs`). |
| **Persistencia de Datos** (`database.py`) | SQLite · SQLAlchemy | Definición del modelo relacional y gestión de sesiones sobre la base de datos local `taxitech_prod.db` para conservar el historial de servicios. |
| **Infraestructura** (`Dockerfile` / `docker-compose.yml`) | Docker | Definición declarativa del entorno y servicios preparada en el repositorio para despliegue aislado *(pendiente de ejecución local por compatibilidad con la versión de macOS)*. |

---

## 4. Fundamentos de Programación Aplicados

La implementación consolida los cuatro pilares fundamentales del desarrollo en Python aplicados a un caso real:

* **Variables y Constantes:** Definición explícita de las tarifas base (`0.02` y `0.05`), identificadores de servicio y acumuladores dinámicos de segundos e importe total[.
* **Estructuras Condicionales (`if / elif / else`):** Control de las transiciones de estado del taxímetro (iniciado, detenido en espera, circulando en ruta, pausado o finalizado) para determinar la tarifa aplicable en cada instante.
* **Bucles y Gestión de Estado en Vivo:** Uso de `st.session_state` y cálculo diferencial de tiempo real en `app.py` para actualizar los contadores segundo a segundo sin pérdida de memoria entre refrescos.
* **Descomposición de Problemas:** División de un sistema completo en piezas pequeñas y verificables: interfaz de usuario (`app.py`), lógica de API (`main.py`), persistencia relacional (`database.py`) y batería de pruebas unitarias.

---

## 5. Decisiones de Diseño (UI) y Calidad

* **Criterio de simplicidad operativa:** Durante el desarrollo se exploraron enriquecimientos visuales en la interfaz de usuario; sin embargo, añadir elementos decorativos innecesarios dificultaba la lectura rápida y comprometía la estabilidad en directo. Se decidió rectificar a tiempo y volver a una interfaz limpia y minimalista, priorizando la claridad visual y la fiabilidad funcional durante el uso.
* **Control de versiones y aprendizaje guiado:** El desarrollo se apoyó en un flujo riguroso de control de versiones con Git y GitHub (`git status`, `git add`, `git commit`, `git push`), manteniendo un historial trazable de cada hito y utilizando herramientas de inteligencia artificial como apoyo pedagógico para comprender la lógica paso a paso y validar cada bloque de código.

---

## 6. Conclusiones y Próximos Pasos

El proyecto ha permitido dar los primeros pasos prácticos en Python, arquitectura modular y control de versiones con GitHub, comprobando la importancia de afianzar primero una base técnica sólida antes de refinar la capa visual. Como evolución natural tras esta entrega, el sistema queda preparado para integrar autenticación de conductores, conexión directa en tiempo real entre el panel de Streamlit y los endpoints de FastAPI, y despliegue en contenedor.
- [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/) — formato de mensajes de commit

### Solución
[Solución proyecto](https://github.com/Factoria-F5-madrid/stn-taximetro)
