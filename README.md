# Proyecto Final: Análisis del desempeño operativo de los vuelos domésticos de American Airlines, con énfasis en retrasos, cancelaciones y desvíos

**Curso:** Business Intelligence

## Integrantes

- Luciana Carpio
- Sofía Briceño
- Gustavo Barrantes
- Adriano Raffo

---

## 1. Marco teórico

### 1.1. Business Intelligence

El Business Intelligence (BI), o inteligencia empresarial, comprende un conjunto de procesos y herramientas tecnológicas que permiten recopilar, integrar y analizar datos para convertirlos en información útil, la cual se emplea en la toma de decisiones. Su propósito es facilitar que las organizaciones entiendan mejor su desempeño, identifiquen patrones y detecten problemas u oportunidades a partir de datos confiables (IBM, s. f.).

La implementación de BI permite elaborar reportes, indicadores y visualizaciones que presentan información y facilitan su interpretación. Así, los responsables de una empresa pueden tomar decisiones fundamentadas en evidencia y no únicamente en percepciones o experiencias previas. Además, BI permite realizar un seguimiento del comportamiento histórico de las operaciones y comparar sus resultados entre diferentes periodos, áreas o categorías.

En el sector aéreo, Business Intelligence puede utilizarse para analizar grandes volúmenes de información relacionada con vuelos, rutas, aeropuertos, horarios, retrasos y cancelaciones. A partir de este análisis, una aerolínea puede identificar las rutas con mayores problemas de puntualidad, los horarios en los que se producen más demoras y las causas que afectan con mayor frecuencia sus operaciones. Por lo tanto, la aplicación de BI contribuye a convertir los registros operativos de los vuelos en información relevante para mejorar la planificación y apoyar la toma de decisiones.

### 1.2. Data warehouse

Un data warehouse o almacén de datos es un sistema diseñado para recopilar, integrar y almacenar información proveniente de distintas fuentes con el propósito de facilitar su análisis. A diferencia de una base de datos operacional, que registra las actividades diarias de una organización, un data warehouse conserva información histórica y se orienta a la elaboración de reportes y al apoyo en la toma de decisiones (IBM, s. f.; Oracle, 2023).

Entre sus principales características se encuentra su orientación a temas, porque organiza los datos según áreas relevantes para la organización; su integración, debido a que reúne información de diferentes fuentes utilizando formatos consistentes; su variación en el tiempo, porque conserva datos históricos; y su carácter no volátil, ya que la información almacenada se mantiene estable para su consulta y análisis.

### 1.3. Data Mart

Un Data Mart es una base de datos analítica orientada a un área, proceso o tema específico de una organización. A diferencia de un data warehouse, que puede integrar información de distintas áreas empresariales, un Data Mart contiene un conjunto más delimitado de datos y busca responder necesidades concretas de análisis. Esta especialización facilita el acceso a la información relevante y permite realizar consultas enfocadas en un determinado proceso de negocio (IBM, s. f.).

Un Data Mart puede obtener sus datos de un data warehouse, pero también puede construirse directamente a partir de fuentes internas o externas. Su información suele organizarse mediante un modelo dimensional compuesto por una tabla de hechos y distintas tablas de dimensiones, lo que permite analizar las medidas desde diferentes perspectivas.

### 1.4. Modelamiento multidimensional

El modelamiento multidimensional es una técnica utilizada para organizar los datos de forma que puedan ser consultados y analizados con facilidad. Su diseño parte de un proceso de negocio y separa la información en hechos, que representan eventos o métricas de negocio, y dimensiones, que proporcionan el contexto necesario para analizarlos, como el tiempo, la ubicación o la organización involucrada (Kimball Group, s. f.).

Para elaborar un modelo multidimensional, primero se selecciona el proceso de negocio y luego se define la granularidad, es decir, qué representa cada fila de la tabla de hechos. Después se identifican las dimensiones y las medidas asociadas al proceso. Esta organización permite filtrar, agrupar y resumir grandes cantidades de datos desde distintas perspectivas.

#### 1.4.1. Modelo estrella

El modelo estrella está conformado por una tabla de hechos central conectada directamente con diferentes tablas de dimensiones, por lo que sus relaciones adoptan una forma similar a una estrella. La tabla central almacena los eventos y medidas del proceso analizado, mientras que las dimensiones contienen la información descriptiva empleada para filtrar y agrupar los resultados.

Este diseño facilita la comprensión del modelo, reduce la complejidad de las consultas y permite analizar las medidas desde distintas perspectivas. Además, las dimensiones suelen estar desnormalizadas, lo que significa que sus atributos descriptivos se conservan en una misma tabla para simplificar las consultas analíticas (Microsoft, s. f.).

#### 1.4.2. Tabla de hechos y granularidad

La tabla de hechos es la tabla central de un modelo estrella. En ella se registran los eventos correspondientes a un proceso de negocio y las medidas que se desean analizar, como cantidades, importes, costos o duraciones. También contiene claves foráneas que permiten relacionar cada evento con sus respectivas dimensiones (Kimball, 2008).

La granularidad define exactamente qué representa cada fila de la tabla de hechos. Por ejemplo, una fila podría representar una venta completa o un producto individual dentro de una venta. Esta definición debe realizarse antes de seleccionar las dimensiones y las medidas, ya que todos los datos de la tabla de hechos deben corresponder al mismo nivel de detalle.

Una granularidad correctamente definida permite interpretar las medidas de manera consistente y evita combinar información perteneciente a distintos niveles de análisis.

#### 1.4.3. Tablas de dimensiones

Las tablas de dimensiones almacenan la información descriptiva que permite interpretar y analizar los registros de la tabla de hechos. Sus atributos responden preguntas como quién, qué, cuándo, dónde y cómo ocurrió un evento. Estas tablas se utilizan para filtrar, clasificar y agrupar las medidas.

Las dimensiones también pueden contener jerarquías que permiten analizar la información con distintos niveles de detalle. Por ejemplo, una dimensión de fecha podría incluir la jerarquía año, trimestre, mes y día, permitiendo pasar de una visión general a una más detallada.

Cada dimensión posee una clave que identifica de manera única sus registros y que se conecta con la tabla de hechos. En los modelos dimensionales suelen utilizarse claves sustitutas, generadas específicamente para el data warehouse o Data Mart, en lugar de depender únicamente de los identificadores de los sistemas de origen (Kimball Group, s. f.).

### 1.5. Proceso ETL

El proceso ETL comprende las etapas de extracción, transformación y carga de datos. En la extracción se obtiene la información desde las fuentes originales; durante la transformación, los datos se limpian, organizan, integran y adaptan a la estructura requerida; finalmente, en la carga, la información procesada se almacena en un data warehouse, Data Mart u otro repositorio de destino (IBM, s. f.).

Este proceso permite convertir datos provenientes de diferentes archivos o sistemas en información consistente y preparada para el análisis. Durante la transformación pueden realizarse actividades como la corrección de formatos, el tratamiento de valores nulos, la eliminación de duplicados, la validación de registros y la creación de campos derivados. De esta manera, ETL contribuye a mejorar la calidad y uniformidad de los datos utilizados en una solución de Business Intelligence.

### 1.6. Procesamiento analítico OLAP

El procesamiento analítico en línea u OLAP es una tecnología que permite analizar grandes volúmenes de información desde diferentes perspectivas. Se utiliza principalmente con datos almacenados en un data warehouse y facilita la ejecución rápida de consultas, comparaciones y cálculos complejos (IBM, 2021).

La información suele organizarse en estructuras multidimensionales conocidas como cubos OLAP. Estos contienen medidas numéricas y dimensiones que permiten observar un mismo resultado según diferentes criterios, como tiempo, ubicación o categoría.

OLAP también permite modificar el nivel de detalle del análisis. Por ejemplo, se puede pasar de una visión anual a una mensual, filtrar una categoría específica o comparar diferentes grupos. De esta manera, los usuarios pueden explorar la información e identificar tendencias o patrones que apoyen la toma de decisiones.

### 1.7. Indicadores de desempeño de vuelos

Los indicadores de desempeño de vuelos permiten medir la eficiencia y puntualidad de las operaciones aéreas. Entre los principales se encuentran el porcentaje de vuelos puntuales, los minutos promedio de retraso, la tasa de cancelación y la proporción de vuelos desviados.

El Bureau of Transportation Statistics considera que un vuelo presenta retraso cuando llega o sale 15 minutos o más después del horario programado. Asimismo, clasifica las causas de demora en cinco categorías: factores atribuibles a la aerolínea, clima extremo, Sistema Nacional de Aviación, llegada tardía de la aeronave anterior y seguridad (Bureau of Transportation Statistics, s. f.).

Estos indicadores permiten comparar el desempeño entre periodos, rutas, aeropuertos y aerolíneas. Su análisis facilita la identificación de patrones y factores que afectan la puntualidad, proporcionando información relevante para mejorar la planificación y la toma de decisiones operativas.

### 1.8. Aplicación de BI al análisis de operaciones aéreas

Las aerolíneas generan grandes cantidades de datos relacionados con vuelos, horarios, rutas, aeropuertos, retrasos, cancelaciones y desvíos. Business Intelligence permite integrar y analizar esta información para convertirla en indicadores que faciliten la evaluación del desempeño operativo y la toma de decisiones.

Mediante reportes y visualizaciones, es posible comparar la puntualidad entre periodos, identificar rutas o aeropuertos con retrasos frecuentes y analizar las principales causas de demora. El Bureau of Transportation Statistics recopila este tipo de información, incluyendo horarios programados y reales, cancelaciones, desvíos y minutos de retraso según su causa (Bureau of Transportation Statistics, s. f.).

De esta manera, la aplicación de BI en el transporte aéreo facilita la identificación de patrones y problemas recurrentes. La información obtenida puede apoyar la planificación de horarios, la asignación de recursos y el seguimiento del desempeño operativo de los vuelos.

## 2. Descripción de la empresa y problemática

### 2.1. Descripción de la empresa
La empresa elegida para desarrollar el proyecto es American Airlines, cuya principal actividad consiste en proveer servicios de transporte aéreo comercial de pasajeros y carga a nivel nacional e internacional. La compañía cuenta con una extensa red de destinos y complementa sus operaciones con servicios como el programa de fidelización AAdvantage, las salas Admirals Club y su división logística American Airlines Cargo. Asimismo, forma parte de la alianza internacional oneworld. 

Para sostener esta amplia cobertura, American Airlines basa su estructura logística en un modelo de red de centros de conexión (Hub and Spoke), mediante la cual coordina miles de despegues diarios desde aeropuertos estratégicos. Entre ellos se encuentran Dallas/Fort Worth, Charlotte, Chicago, Miami, Nueva York, Los Ángeles, Filadelfia, Phoenix y Washington. La dimensión de estas operaciones permite mantener una amplia cobertura, pero también genera una elevada interdependencia entre vuelos, aeronaves, aeropuertos y horarios. 

Así, debido a esta elevada magnitud de operaciones, la compañía genera grandes volúmenes de datos relacionados con vuelos, rutas, aeropuertos, horarios, retrasos y cancelaciones. Esta información resulta adecuada para aplicar herramientas de Business Intelligence que permitan evaluar el desempeño operativo e identificar patrones asociados con problemas de puntualidad. Aunque American Airlines realiza vuelos nacionales e internacionales, el presente proyecto analizará únicamente sus operaciones domésticas dentro de Estados Unidos, debido a que la fuente seleccionada corresponde a los registros publicados por el Bureau of Transportation Statistics. 

### 2.2. Problemática
El sector aeronáutico presenta una alta sensibilidad al tiempo, por lo cual la puntualidad constituye un aspecto importante del desempeño de una aerolínea. Los retrasos, las cancelaciones y los desvíos pueden alterar la programación de aeronaves y tripulaciones, afectar el uso de la infraestructura aeroportuaria y generar inconvenientes para los pasajeros. Según el Bureau of Transportation Statistics, un vuelo se considera retrasado cuando llega o sale 15 minutos o más después del horario programado. 

- **Impacto en la eficiencia operativa:** Las demoras durante la salida, el vuelo o la llegada pueden incrementar el tiempo total de una operación y afectar la utilización de aeronaves y tripulaciones. Asimismo, las cancelaciones y los retrasos prolongados pueden requerir ajustes en la programación y generar gastos adicionales para la aerolínea. Aunque la base empleada no contiene los costos monetarios ocasionados por estas situaciones, sí permite analizar variables operativas como el tiempo de taxi, la duración del vuelo, los minutos de retraso y el número de cancelaciones.
- **Impacto en la puntualidad:** Las interrupciones en el servicio pueden generar un efecto dominó. Por ejemplo, un retraso inicial causado por la llegada tardía de una aeronave puede afectar los vuelos posteriores programados para ese avión y sus respectivas tripulaciones. El Bureau of Transportation Statistics clasifica las causas de demora en cinco categorías generales: factores atribuibles a la aerolínea, clima extremo, Sistema Nacional de Aviación, seguridad y llegada tardía de la aeronave anterior.
- **Impacto en los pasajeros:** Los retrasos y las cancelaciones prolongan el tiempo de espera, pueden ocasionar la pérdida de conexiones y obligar a modificar los itinerarios de los pasajeros. Estas situaciones pueden afectar negativamente su experiencia de viaje. Sin embargo, debido a que la base seleccionada no contiene encuestas de satisfacción ni información individual de los pasajeros, este impacto será considerado como una consecuencia de la problemática y no como una variable medida directamente en el proyecto. 

American Airlines realiza una gran cantidad de vuelos domésticos en Estados Unidos, cuyo desempeño operativo puede verse afectado por retrasos, cancelaciones y desvíos. Estos eventos varían según factores como la fecha, el horario, la ruta, los aeropuertos involucrados y las causas de demora. Debido al elevado volumen de registros y a la diversidad de variables operativas, resulta difícil identificar patrones y determinar qué factores concentran los mayores problemas mediante consultas convencionales.

Por ello, existe la necesidad de integrar y organizar esta información mediante una solución de Business Intelligence que permita analizar el desempeño operativo de los vuelos domésticos de American Airlines. La solución facilitará el seguimiento de indicadores de puntualidad, retrasos, cancelaciones y desvíos, así como la identificación de los periodos, rutas, aeropuertos y causas que presentan mayores incidencias. De esta manera, se proporcionará información que pueda apoyar la planificación y la toma de decisiones operativas.

### 2.3. Objetivo general
Diseñar e implementar una solución de Business Intelligence para analizar el proceso operativo de la aerolínea American Airlines, estructurada mediante un modelo en estrella e integrada con los registros del Bureau of Transportation Statistics, con el fin de transformar grandes volúmenes de datos operativos en información analítica que permita identificar patrones de retraso, rutas y aeropuertos críticos, franjas horarias con mayor incidencia y causas de interrupción, apoyando la toma de decisiones orientadas a mejorar la puntualidad y la eficiencia operativa. 

### 2.4. Objetivos específicos
- **Consolidar y preparar la fuente de datos operativa:** Extraer, limpiar y transformar los registros de vuelos del Bureau of Transportation Statistics para construir una base de datos analítica estandarizada, validando posibles inconsistencias y valores faltantes.
- **Analizar los patrones temporales de demoras:** Identificar las franjas horarias del día y los días de la semana con mayor promedio de retrasos y mayor frecuencia de vuelos demorados por más de 15 minutos.
- **Evaluar el comportamiento operativo por rutas y aeropuertos:** Determinar las rutas de origen a destino y los aeropuertos que concentran el mayor tiempo promedio de retraso en las llegadas y la mayor tasa de cancelaciones de vuelos.
- **Analizar las causas de las interrupciones:** Clasificar los minutos de demora según causas atribuibles a la aerolínea, clima, Sistema Nacional de Aviación, seguridad o llegada tardía de aeronaves, evaluando la participación de esta última causa en los retrasos registrados por la compañía.
- **Diseñar el Data Mart multidimensional y los tableros de control:** Construir un modelo dimensional en estrella con al menos ocho dimensiones y desarrollar tableros de control interactivos que faciliten el monitoreo del desempeño operativo y la puntualidad para apoyar la toma de decisiones.

### 2.5. Preguntas de negocio

#### Análisis por tiempo y horarios
- ¿Cuáles son las franjas horarias del día en las que se registran los mayores minutos promedio de demora en la salida?
- ¿En qué días de la semana se concentra la mayor cantidad de vuelos retrasados por más de 15 minutos?

#### Análisis por ubicación y rutas
- ¿Qué rutas presentan el mayor tiempo promedio de retraso en la llegada?
- ¿Qué aeropuertos de origen registran la mayor proporción de vuelos cancelados respecto del total de salidas programadas?

#### Análisis por causas de demora
- ¿Qué causa acumula el mayor volumen de minutos de retraso entre factores atribuibles a la aerolínea, clima, Sistema Nacional de Aviación, seguridad y llegada tardía de aeronaves?
- ¿Qué proporción del total de minutos de demora clasificados por causa corresponde a la llegada tardía de la aeronave anterior?

#### Análisis de cancelaciones y desvíos
- ¿Cuáles son las causas de cancelación más frecuentes?
- ¿En qué rutas, aeropuertos y periodos se registra la mayor proporción de vuelos desviados?

# 3. Modelamiento de Datos Dimensional

## 3.1. Fuente de datos

La fuente principal del proyecto es la base **Reporting Carrier On-Time Performance**, publicada por el *Bureau of Transportation Statistics* (BTS) del Departamento de Transporte de los Estados Unidos. Esta base contiene registros reales sobre los vuelos domésticos realizados por las aerolíneas estadounidenses y se encuentra disponible en el portal oficial [TranStats](https://www.transtats.bts.gov/).

Para el proyecto se descargaron archivos mensuales correspondientes al periodo de **enero a julio de 2025**. Debido a que el análisis se enfoca en las operaciones de **American Airlines**, los registros fueron filtrados mediante el campo `OP_UNIQUE_CARRIER`, seleccionando el código `AA`. Posteriormente, los siete archivos fueron consolidados mediante **Power Query** para formar una sola fuente de datos.

Además, se utilizará la tabla auxiliar de causas de cancelación de la misma plataforma para asociar los valores del campo `CANCELLATION_CODE` con una descripción comprensible de cada motivo de cancelación.

La base contiene información relacionada con:
- Fecha del vuelo, aerolínea, número de vuelo y aeronave
- Aeropuertos de origen y destino
- Horarios programados y reales
- Retrasos, cancelaciones y desvíos
- Duración y distancia recorrida
- Minutos de demora atribuidos a distintas causas (aerolínea, clima, Sistema Nacional de Aviación, seguridad y llegada tardía de la aeronave anterior)

Además de los registros principales, se descargaron **tablas auxiliares** proporcionadas por el BTS que permiten interpretar determinados códigos presentes en la base, como los correspondientes a aerolíneas, aeropuertos y causas de cancelación.

La fuente fue seleccionada porque contiene datos oficiales, reales y suficientemente detallados para analizar el desempeño operativo de los vuelos domésticos de American Airlines, incluyendo su puntualidad, cancelaciones y desvíos. Asimismo, el conjunto consolidado supera el requisito mínimo de **500 000 registros** establecido para el proyecto.

## 3.2. Descripción general de los datos

Cada registro corresponde a un vuelo doméstico programado de American Airlines e incluye datos como la fecha, aeronave, aeropuertos de origen y destino, horarios programados y reales, duración, tiempo de rodaje y distancia recorrida. También indica si el vuelo fue cancelado o desviado y, cuando corresponda, el motivo de la cancelación.

Para los vuelos que cumplen los criterios de demora establecidos por el BTS, se registran los minutos de retraso según su causa. Las horas se expresan en formato `HHMM`, mientras que las duraciones y los retrasos se encuentran expresados en minutos y las distancias en millas.

Los datos fueron consolidados a partir de **siete archivos mensuales**, correspondientes al periodo de enero a julio de 2025. La base consolidada contiene:

- **569 156 registros**
- **53 campos**, de los cuales 52 proceden de la fuente original y uno, `Source.Name`, fue generado durante la consolidación en Power Query

> El campo `Source.Name` se utilizará únicamente para identificar el archivo mensual de procedencia durante la preparación de los datos y no formará parte del modelo dimensional final.

Se seleccionó un **modelo en estrella** porque el análisis se concentra en un único proceso de negocio: la operación de vuelos domésticos programados. La tabla `FactOperacionVuelo` almacena las medidas operativas, mientras que las dimensiones proporcionan el contexto temporal, geográfico y descriptivo necesario para analizarlas. Este diseño facilita la comprensión del modelo y reduce la complejidad de las consultas analíticas.

Debido a que la fuente fue filtrada previamente para incluir únicamente American Airlines, no se incorporó una dimensión de aerolínea. En su lugar, se incluyó `DimCausaCancelacion`, debido a que permite analizar uno de los eventos considerados en las preguntas de negocio.

## 3.3. Diccionario de datos de la fuente

El diccionario de la fuente describe los campos originales utilizados durante la preparación de los datos. Posteriormente, los diccionarios de la tabla de hechos y de las dimensiones describen la estructura propuesta para el Data Mart. Por lo tanto, algunos campos de la fuente se transforman, se separan entre diferentes tablas o se excluyen del modelo analítico.

### Campos de la tabla

| Nombre del campo | Tipo de dato propuesto | Descripción del campo | Nulos |
|---|---|---|---|
| `Source.Name` | varchar(255) | Nombre del archivo de origen | No |
| `YEAR` | SMALLINT | Año del vuelo | No |
| `MONTH` | TINYINT | Mes del vuelo | No |
| `QUARTER` | TINYINT | Trimestre del año (1–4) | No |
| `DAY_OF_MONTH` | TINYINT | Día del mes (1–31) | No |
| `DAY_OF_WEEK` | TINYINT | Día de la semana (1 = lunes, 7 = domingo) | No |
| `FL_DATE` | DATE | Fecha del vuelo | No |
| `OP_UNIQUE_CARRIER` | VARCHAR(10) | Código único de la aerolínea que opera el vuelo | No |
| `OP_CARRIER_AIRLINE_ID` | INT | ID numérico de la aerolínea asignado por el DOT | No |
| `TAIL_NUM` | VARCHAR(10) | Matrícula de la aeronave | Sí |
| `OP_CARRIER_FL_NUM` | INT | Número de vuelo | No |
| `ORIGIN_AIRPORT_ID` | INT | ID único del aeropuerto de origen | No |
| `ORIGIN` | CHAR(3) | Código IATA del aeropuerto de origen | No |
| `ORIGIN_CITY_NAME` | VARCHAR(100) | Ciudad de origen | No |
| `ORIGIN_STATE_ABR` | CHAR(2) | Abreviatura del estado de origen | No |
| `ORIGIN_STATE_NM` | VARCHAR(50) | Nombre del estado de origen | No |
| `DEST_AIRPORT_ID` | INT | ID único del aeropuerto de destino | No |
| `DEST` | CHAR(3) | Código IATA del aeropuerto de destino | No |
| `DEST_CITY_NAME` | VARCHAR(100) | Ciudad de destino | No |
| `DEST_STATE_ABR` | CHAR(2) | Abreviatura del estado de destino | No |
| `DEST_STATE_NM` | VARCHAR(50) | Nombre del estado de destino | No |
| `CRS_DEP_TIME` | CHAR(4) | Hora de salida programada, en hora local (hhmm) | No |
| `DEP_TIME` | CHAR(4) | Hora de salida real, en hora local (hhmm) | Sí |
| `DEP_DELAY` | SMALLINT | Minutos de diferencia entre la salida real y la programada (un valor negativo indica que salió antes) | Sí |
| `DEP_DELAY_NEW` | SMALLINT | Minutos de retraso en la salida, con los valores negativos reemplazados por 0 | Sí |
| `DEP_DEL15` | BIT | Indicador de retraso en la salida de 15 minutos o más (1 = sí, 0 = no) | Sí |
| `DEP_DELAY_GROUP` | SMALLINT | Rango de retraso en la salida en intervalos de 15 minutos (-2 a 12) | Sí |
| `DEP_TIME_BLK` | VARCHAR(9) | Franja horaria de la salida programada (ej. 0600-0659) | No |
| `TAXI_OUT` | SMALLINT | Minutos entre la puerta y el despegue | Sí |
| `WHEELS_OFF` | CHAR(4) | Hora de despegue, en hora local (HHMM) | Sí |
| `WHEELS_ON` | CHAR(4) | Hora de aterrizaje, en hora local (HHMM) | Sí |
| `TAXI_IN` | SMALLINT | Minutos entre el aterrizaje y la llegada a la puerta | Sí |
| `CRS_ARR_TIME` | CHAR(4) | Hora de llegada programada, en hora local (HHMM) | No |
| `ARR_TIME` | CHAR(4) | Hora de llegada real, en hora local (HHMM) | Sí |
| `ARR_DELAY` | SMALLINT | Minutos de diferencia entre la llegada real y la programada (un valor negativo significa que llegó antes) | No |
| `ARR_DELAY_NEW` | SMALLINT | Minutos de retraso en la llegada, con los valores negativos reemplazados por 0 | Sí |
| `ARR_DEL15` | BIT | Indicador de retraso en la llegada de 15 minutos o más (1 = sí, 0 = no) | Sí |
| `ARR_DELAY_GROUP` | SMALLINT | Rango de retraso en la llegada en intervalos de 15 minutos (-2 a 12) | Sí |
| `ARR_TIME_BLK` | VARCHAR(9) | Franja horaria de la llegada programada | No |
| `CANCELLED` | BIT | Indicador de vuelo cancelado | No |
| `CANCELLATION_CODE` | CHAR(1) | Motivo de la cancelación (A, B, C, D) | Sí |
| `DIVERTED` | BIT | Indicador de vuelo desviado | No |
| `CRS_ELAPSED_TIME` | SMALLINT | Duración programada del vuelo en minutos, de puerta a puerta | No |
| `ACTUAL_ELAPSED_TIME` | SMALLINT | Duración real del vuelo en minutos, de puerta a puerta | Sí |
| `AIR_TIME` | SMALLINT | Minutos en el aire, del despegue al aterrizaje | Sí |
| `FLIGHTS` | TINYINT | Cantidad de vuelos (contador con valor 1 por cada registro) | No |
| `DISTANCE` | SMALLINT | Distancia entre aeropuertos, en millas | No |
| `DISTANCE_GROUP` | TINYINT | Rango de distancia en intervalos de 250 millas | No |
| `CARRIER_DELAY` | SMALLINT | Minutos de retraso atribuibles a la aerolínea | Sí |
| `WEATHER_DELAY` | SMALLINT | Minutos de retraso por clima extremo | Sí |
| `NAS_DELAY` | SMALLINT | Minutos de retraso por el sistema nacional de aviación | Sí |
| `SECURITY_DELAY` | SMALLINT | Minutos de retraso por motivos de seguridad | Sí |
| `LATE_AIRCRAFT_DELAY` | SMALLINT | Minutos de retraso porque la aeronave llegó tarde de su vuelo anterior | Sí |

## 3.4. Diseño del Datamart

A partir de los campos identificados en la fuente de datos se diseñó el Datamart que será utilizado como estructura de destino para el proceso ETL. El modelo organiza la información operacional de los vuelos mediante una tabla de hechos central y ocho dimensiones relacionadas directamente con ella.

La granularidad definida es de **un registro por cada vuelo programado**. Por lo tanto, cada fila de `FactOperacionVuelo` representa una operación de vuelo individual y contiene tanto las claves que permiten relacionarla con sus dimensiones como las medidas necesarias para analizar su desempeño.

Para las dimensiones se utilizan claves sustitutas generadas dentro del Datamart. Estas claves permiten identificar de forma única cada registro dimensional sin depender directamente de las claves utilizadas en la fuente de origen.

### 3.4.1. Diagrama del Datamart

La estructura final del Datamart se presenta en el siguiente diagrama:

![Diagrama del Datamart](datamart.png)

El modelo está compuesto por la tabla de hechos `FactOperacionVuelo` y las siguientes ocho dimensiones:

1. `DimFecha`
2. `DimHora`
3. `DimAeropuerto`
4. `DimRuta`
5. `DimAvion`
6. `DimVuelo`
7. `DimEstadoOperacion`
8. `DimCausaCancelacion`

Todas las dimensiones se relacionan directamente con `FactOperacionVuelo`, manteniendo la estructura de un esquema estrella.

`DimHora` desempeña dos roles dentro del modelo, ya que se utiliza para representar la hora programada de salida y la hora programada de llegada. De manera similar, `DimAeropuerto` se utiliza tanto para el aeropuerto de origen como para el aeropuerto de destino. Por este motivo, la tabla de hechos contiene dos claves foráneas hacia cada una de estas dimensiones.

---

### 3.4.2. FactOperacionVuelo

`FactOperacionVuelo` constituye la tabla central del Datamart. Su granularidad corresponde a un vuelo programado y concentra las claves foráneas de las dimensiones junto con las medidas operativas utilizadas para el análisis de retrasos, cancelaciones, desvíos, tiempos y distancias.

| Campo | Tipo | Descripción |
|---|---|---|
| `OperacionVueloKey` | BIGINT | Clave primaria sustituta de la tabla de hechos. |
| `FechaKey` | INT | Clave foránea hacia `DimFecha`. |
| `HoraSalidaProgramadaKey` | INT | Clave foránea hacia `DimHora` para la hora programada de salida. |
| `HoraLlegadaProgramadaKey` | INT | Clave foránea hacia `DimHora` para la hora programada de llegada. |
| `AeropuertoOrigenKey` | INT | Clave foránea hacia `DimAeropuerto` para el aeropuerto de origen. |
| `AeropuertoDestinoKey` | INT | Clave foránea hacia `DimAeropuerto` para el aeropuerto de destino. |
| `RutaKey` | INT | Clave foránea hacia `DimRuta`. |
| `AvionKey` | INT | Clave foránea hacia `DimAvion`. |
| `VueloKey` | INT | Clave foránea hacia `DimVuelo`. |
| `EstadoOperacionKey` | INT | Clave foránea hacia `DimEstadoOperacion`. |
| `CausaCancelacionKey` | INT | Clave foránea hacia `DimCausaCancelacion`. Puede ser nula cuando el vuelo no fue cancelado. |
| `DEP_DELAY` | SMALLINT | Diferencia en minutos entre la salida real y la programada. |
| `DEP_DELAY_NEW` | SMALLINT | Minutos de retraso en salida, considerando como cero los valores negativos. |
| `DEP_DEL15` | BIT | Indica si el retraso de salida fue de 15 minutos o más. |
| `DEP_DELAY_GROUP` | SMALLINT | Agrupación del retraso de salida en intervalos de 15 minutos. |
| `ARR_DELAY` | SMALLINT | Diferencia en minutos entre la llegada real y la programada. |
| `ARR_DELAY_NEW` | SMALLINT | Minutos de retraso en llegada, considerando como cero los valores negativos. |
| `ARR_DEL15` | BIT | Indica si el retraso de llegada fue de 15 minutos o más. |
| `ARR_DELAY_GROUP` | SMALLINT | Agrupación del retraso de llegada en intervalos de 15 minutos. |
| `TAXI_OUT` | SMALLINT | Minutos transcurridos desde la salida de la puerta hasta el despegue. |
| `TAXI_IN` | SMALLINT | Minutos transcurridos desde el aterrizaje hasta la llegada a la puerta. |
| `CRS_ELAPSED_TIME` | SMALLINT | Duración programada del vuelo en minutos. |
| `ACTUAL_ELAPSED_TIME` | SMALLINT | Duración real del vuelo en minutos. |
| `AIR_TIME` | SMALLINT | Tiempo efectivo de vuelo en minutos. |
| `FLIGHTS` | TINYINT | Contador de vuelos; toma el valor 1 por cada operación. |
| `DISTANCE` | SMALLINT | Distancia de la operación en millas. |
| `CARRIER_DELAY` | SMALLINT | Minutos de demora atribuibles a la aerolínea. |
| `WEATHER_DELAY` | SMALLINT | Minutos de demora asociados al clima extremo. |
| `NAS_DELAY` | SMALLINT | Minutos de demora asociados al Sistema Nacional de Aviación. |
| `SECURITY_DELAY` | SMALLINT | Minutos de demora asociados a seguridad. |
| `LATE_AIRCRAFT_DELAY` | SMALLINT | Minutos de demora ocasionados por la llegada tardía de la aeronave anterior. |
| `DEP_TIME` | CHAR(4) | Hora real de salida. |
| `WHEELS_OFF` | CHAR(4) | Hora de despegue. |
| `WHEELS_ON` | CHAR(4) | Hora de aterrizaje. |
| `ARR_TIME` | CHAR(4) | Hora real de llegada. |
| `CANCELLED` | BIT | Indica si el vuelo fue cancelado. |
| `DIVERTED` | BIT | Indica si el vuelo fue desviado. |

---

### 3.4.3. DimFecha

`DimFecha` proporciona el contexto temporal de cada operación y permite realizar análisis por año, trimestre, mes, día del mes y día de la semana.

| Campo | Tipo | Descripción |
|---|---|---|
| `FechaKey` | INT | Clave primaria sustituta de la dimensión. |
| `FL_DATE` | DATE | Fecha completa del vuelo. |
| `YEAR` | SMALLINT | Año correspondiente al vuelo. |
| `QUARTER` | TINYINT | Trimestre del año. |
| `MONTH` | TINYINT | Mes del año. |
| `DAY_OF_MONTH` | TINYINT | Día del mes. |
| `DAY_OF_WEEK` | TINYINT | Día de la semana. |

La dimensión permite establecer una jerarquía temporal de año → trimestre → mes → día.

---

### 3.4.4. DimHora

`DimHora` permite analizar las operaciones según la hora y la franja horaria en la que fueron programadas.

| Campo | Tipo | Descripción |
|---|---|---|
| `HoraKey` | INT | Clave primaria sustituta de la dimensión. |
| `HoraCompleta` | CHAR(4) | Hora completa en formato HHMM. |
| `Hora` | TINYINT | Componente correspondiente a la hora. |
| `Minuto` | TINYINT | Componente correspondiente a los minutos. |
| `FranjaHoraria` | NVARCHAR(50) | Franja horaria utilizada para agrupar las operaciones. |

Esta dimensión se utiliza dos veces desde `FactOperacionVuelo`: `HoraSalidaProgramadaKey` representa la salida programada y `HoraLlegadaProgramadaKey` representa la llegada programada.

---

### 3.4.5. DimAeropuerto

`DimAeropuerto` almacena los atributos descriptivos de los aeropuertos involucrados en las operaciones.

| Campo | Tipo | Descripción |
|---|---|---|
| `AeropuertoKey` | INT | Clave primaria sustituta de la dimensión. |
| `AIRPORT_ID` | INT | Identificador del aeropuerto proveniente de la fuente. |
| `AIRPORT_CODE` | NCHAR(10) | Código del aeropuerto. |
| `CITY_NAME` | NVARCHAR(100) | Ciudad donde se encuentra el aeropuerto. |
| `STATE_ABR` | NCHAR(10) | Abreviatura del estado. |
| `STATE_NM` | NVARCHAR(50) | Nombre del estado. |

La dimensión cumple dos roles dentro del modelo. `AeropuertoOrigenKey` identifica el aeropuerto desde el cual parte el vuelo y `AeropuertoDestinoKey` identifica el aeropuerto al cual se dirige.

---

### 3.4.6. DimRuta

`DimRuta` representa la combinación de origen y destino correspondiente a una operación y permite realizar análisis a nivel de ruta.

| Campo | Tipo | Descripción |
|---|---|---|
| `RutaKey` | INT | Clave primaria sustituta de la dimensión. |
| `RUTA` | NVARCHAR(50) | Identificación de la ruta del vuelo. |
| `DISTANCE_GROUP` | SMALLINT | Grupo de distancia de la ruta. |

La distancia exacta se conserva como medida en `FactOperacionVuelo`, mientras que `DISTANCE_GROUP` permite clasificar las rutas según rangos de distancia.

---

### 3.4.7. DimAvion

`DimAvion` identifica la aeronave utilizada en cada operación.

| Campo | Tipo | Descripción |
|---|---|---|
| `AvionKey` | INT | Clave primaria sustituta de la dimensión. |
| `TAIL_NUM` | NVARCHAR(50) | Matrícula de la aeronave. |

`TAIL_NUM` puede presentar valores nulos en la fuente de datos.

---

### 3.4.8. DimVuelo

`DimVuelo` representa el número de vuelo asignado por la aerolínea.

| Campo | Tipo | Descripción |
|---|---|---|
| `VueloKey` | INT | Clave primaria sustituta de la dimensión. |
| `OP_CARRIER_FL_NUM` | INT | Número de vuelo de la operación. |

---

### 3.4.9. DimEstadoOperacion

`DimEstadoOperacion` permite clasificar el resultado general de la operación del vuelo.

| Campo | Tipo | Descripción |
|---|---|---|
| `EstadoOperacionKey` | INT | Clave primaria sustituta de la dimensión. |
| `EstadoOperacion` | NVARCHAR(50) | Estado correspondiente a la operación del vuelo. |

Esta dimensión permite distinguir las diferentes situaciones operativas definidas durante la transformación de los datos.

---

### 3.4.10. DimCausaCancelacion

`DimCausaCancelacion` permite incorporar una descripción comprensible del motivo por el cual un vuelo fue cancelado.

| Campo | Tipo | Descripción |
|---|---|---|
| `CausaCancelacionKey` | INT | Clave primaria sustituta de la dimensión. |
| `CANCELLATION_CODE` | CHAR(1) | Código de la causa de cancelación proveniente de la fuente. |
| `DescripcionCancelacion` | NVARCHAR(20) | Descripción asociada a la causa de cancelación. |

La relación con esta dimensión es opcional, ya que solamente los vuelos cancelados presentan una causa de cancelación.

---

### 3.4.11. Relaciones del modelo

Todas las dimensiones se relacionan directamente con `FactOperacionVuelo` mediante relaciones de uno a muchos (1:N). Un registro de una dimensión puede estar asociado a múltiples operaciones de vuelo, mientras que cada clave foránea de la tabla de hechos identifica un registro específico de su dimensión correspondiente.

Dos dimensiones cumplen más de un rol:

- `DimHora` se relaciona mediante `HoraSalidaProgramadaKey` y `HoraLlegadaProgramadaKey`.
- `DimAeropuerto` se relaciona mediante `AeropuertoOrigenKey` y `AeropuertoDestinoKey`.

## Bibliografía

Bureau of Transportation Statistics. (s. f.). *Reporting carrier on-time performance (1987–present)*. U.S. Department of Transportation. [https://www.transtats.bts.gov/DL_SelectFields.aspx?QO_fu146_anzr=b0-gvzr&gnoyr_VQ=FGJ](https://www.transtats.bts.gov/DL_SelectFields.aspx?QO_fu146_anzr=b0-gvzr&gnoyr_VQ=FGJ)

IBM. (s. f.). *¿Qué es Business Intelligence (BI)?* [https://www.ibm.com/mx-es/think/topics/business-intelligence](https://www.ibm.com/mx-es/think/topics/business-intelligence)

IBM. (s. f.). *What is a data warehouse?* [https://www.ibm.com/think/topics/data-warehouse](https://www.ibm.com/think/topics/data-warehouse)

IBM. (2021, 30 de julio). *What is OLAP?* [https://www.ibm.com/think/topics/olap](https://www.ibm.com/think/topics/olap)

Kimball Group. (s. f.). *Dimensional modeling techniques*. [https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

Kimball, R. (2008, 5 de noviembre). *Fact tables*. Kimball Group. [https://www.kimballgroup.com/2008/11/fact-tables/](https://www.kimballgroup.com/2008/11/fact-tables/)

Microsoft. (s. f.). *Understand star schema and the importance for Power BI*. Microsoft Learn. [https://learn.microsoft.com/en-us/power-bi/guidance/star-schema](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)

Oracle. (2023, 8 de junio). *What is a data warehouse?* [https://www.oracle.com/database/what-is-a-data-warehouse/](https://www.oracle.com/database/what-is-a-data-warehouse/)

Link de la base de datos completa (drive): https://drive.google.com/file/d/1UJ-2yC9uMcpQJi6i4bS0GQAZNirMcL3X/view?usp=sharing
