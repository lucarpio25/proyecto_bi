# Proyecto Final — Análisis de la demanda y el gasto de las prestaciones de salud del sector privado peruano

**Curso:** Business Intelligence

**Integrantes**

- Luciana Carpio
- Sofía Briceño
- Gustavo Barrantes
- Adriano Raffo

## 1. Marco teórico

### 1.1. Business Intelligence

El Business Intelligence (BI), o inteligencia empresarial, comprende un conjunto de procesos y herramientas tecnológicas que permiten recopilar, integrar y analizar datos para convertirlos en información útil, la cual se emplea en la toma de decisiones. Su propósito es facilitar que las organizaciones entiendan mejor su desempeño, identifiquen patrones y detecten problemas u oportunidades a partir de datos confiables.

La implementación de BI permite elaborar reportes, indicadores y visualizaciones que presentan información y facilitan su interpretación. Así, los responsables de una empresa pueden tomar decisiones fundamentadas en evidencia y no únicamente en percepciones o experiencias previas. BI permite realizar un seguimiento del comportamiento histórico de las operaciones y comparar sus resultados entre diferentes periodos, áreas o categorías.

En el sector salud, Business Intelligence puede utilizarse para analizar grandes volúmenes de información relacionada con pacientes, establecimientos, aseguradoras, diagnósticos, coberturas, prestaciones y gastos. A partir de este análisis, las organizaciones pueden identificar los tipos de atención con mayor demanda, los diagnósticos y establecimientos que concentran mayores gastos, así como diferencias según ubicación, cobertura o características de los pacientes. Por lo tanto, la aplicación de BI contribuye a convertir los registros de prestaciones de salud en información relevante para mejorar la planificación y apoyar la toma de decisiones en el sector.

### 1.2. Data warehouse

Un data warehouse o almacén de datos es un sistema diseñado para recopilar, integrar y almacenar información proveniente de distintas fuentes con el propósito de facilitar su análisis. A diferencia de una base de datos operacional, que registra las actividades diarias de una organización, un data warehouse conserva información histórica y se orienta a la elaboración de reportes y al apoyo en la toma de decisiones.

Algunas de sus características son las siguientes: está orientado a temas, porque organiza los datos según áreas relevantes; es integrado, ya que reúne información con formatos consistentes; es variante en el tiempo, porque permite analizar datos históricos; y es no volátil, debido a que la información almacenada se mantiene estable para su consulta.

### 1.3. Data mart

Un Data Mart es una base de datos analítica orientada a un área, proceso o tema específico de una organización. A diferencia de un data warehouse, que puede integrar información de distintas áreas empresariales, un Data Mart contiene un conjunto más delimitado de datos y busca responder necesidades concretas de análisis. Esta especialización facilita el acceso a la información relevante y permite realizar consultas enfocadas en un determinado proceso de negocio.

Un Data Mart puede obtener sus datos de un data warehouse, pero también puede construirse directamente a partir de fuentes internas o externas. Su información suele organizarse mediante un modelo dimensional compuesto por una tabla de hechos y distintas tablas de dimensiones, lo que permite analizar las medidas desde diferentes perspectivas.

### 1.4. Modelamiento multidimensional

El modelamiento multidimensional es una técnica utilizada para organizar los datos de forma que puedan ser consultados y analizados con facilidad. Su diseño parte de un proceso de negocio y separa la información en hechos, que representan eventos o métricas de negocio, y dimensiones, que proporcionan el contexto necesario para analizarlos, como el tiempo, la ubicación o la empresa involucrada.

Para elaborar un modelo multidimensional, primero se selecciona el proceso de negocio, luego se define la granularidad, es decir, qué representa cada fila de la tabla de hechos. Después se identifican las dimensiones y las medidas asociadas al proceso. Esta organización permite filtrar, agrupar y resumir grandes cantidades de datos desde distintas perspectivas. A continuación, se describen el modelo estrella y los elementos principales del modelamiento multidimensional:

#### 1.4.1. Modelo estrella

Está conformado por una tabla de hechos central conectada directamente con diferentes tablas de dimensiones, lo cual forma una figura similar a una estrella. La tabla central almacena los eventos y medidas del proceso analizado, mientras que las dimensiones contienen la información descriptiva empleada para filtrar y agrupar los resultados. Su diseño facilita la comprensión del modelo, reduce la complejidad de las consultas y permite analizar las medidas desde distintas perspectivas. Además, las dimensiones suelen estar desnormalizadas, es decir, sus atributos se conservan en una misma tabla para simplificar el análisis.

#### 1.4.2. Tabla de hechos y granularidad

La tabla de hechos es la tabla central de un modelo estrella. En ella se registran los eventos correspondientes a un proceso de negocio y las medidas que se desean analizar, como cantidades, importes, costos o duraciones. También contiene claves foráneas que permiten relacionar cada evento con sus respectivas dimensiones.

La granularidad define exactamente qué representa cada fila de la tabla de hechos. Por ejemplo, una fila podría representar una venta completa o un producto individual dentro de una venta. Esta definición debe realizarse antes de seleccionar las dimensiones y medidas, ya que todos los datos de la tabla deben corresponder al mismo nivel de detalle. Una granularidad correctamente definida permite interpretar las medidas de manera consistente y evita combinar información perteneciente a distintos niveles de análisis.

#### 1.4.3. Tablas de dimensiones

Las tablas de dimensiones almacenan la información descriptiva que permite interpretar y analizar los registros de la tabla de hechos. Sus atributos responden preguntas como quién, qué, cuándo, dónde y cómo ocurrió un evento. Estas tablas se utilizan para filtrar, clasificar y agrupar las medidas. Además, pueden contener jerarquías que permiten analizar la información con distintos niveles de detalle mediante atributos organizados en niveles, como año, trimestre y mes.

Cada dimensión posee una clave que identifica de manera única sus registros y que se conecta con la tabla de hechos. En los modelos dimensionales suelen utilizarse claves sustitutas, generadas específicamente para el data warehouse, en lugar de depender únicamente de los identificadores de los sistemas de origen.

### 1.5. Proceso ETL

El proceso ETL comprende las etapas de extracción, transformación y carga de datos. En la extracción se obtiene la información desde las fuentes originales; durante la transformación, los datos se limpian, organizan, integran y adaptan a la estructura requerida; finalmente, en la carga, la información procesada se almacena en un data warehouse, Data Mart u otro repositorio de destino.

Este proceso permite convertir datos provenientes de diferentes archivos o sistemas en información consistente y preparada para el análisis. Durante la transformación pueden realizarse actividades como la corrección de formatos, el tratamiento de valores nulos, la eliminación de duplicados, la validación de registros y la creación de campos derivados. De esta manera, ETL contribuye a mejorar la calidad y uniformidad de los datos utilizados en una solución de Business Intelligence.

### 1.6. Procesamiento analítico OLAP

El procesamiento analítico en línea u OLAP es una tecnología que permite analizar grandes volúmenes de información desde diferentes perspectivas. Se utiliza principalmente con datos almacenados en un data warehouse y facilita la ejecución rápida de consultas, comparaciones y cálculos complejos.

La información suele organizarse en estructuras multidimensionales conocidas como cubos OLAP. Estos contienen medidas numéricas y dimensiones que permiten observar un mismo resultado según diferentes criterios, como tiempo, ubicación o categoría.

OLAP también permite cambiar el nivel de detalle del análisis. Por ejemplo, se puede pasar de una visión anual a una mensual, filtrar una categoría específica o comparar diferentes grupos. De esta manera, los usuarios pueden explorar la información e identificar tendencias o patrones que apoyen la toma de decisiones.

### 1.7. Indicadores de prestaciones y gastos de salud

Los indicadores de prestaciones y gastos de salud permiten analizar la demanda de servicios y la distribución de los recursos económicos asociados con la atención de los pacientes. Entre los principales indicadores se encuentran la cantidad de prestaciones realizadas, el monto total liquidado por las IAFAS, el monto promedio liquidado por prestación, el promedio de días de estancia facturable por prestación hospitalaria y la participación de cada componente en la suma de los gastos registrados, como honorarios, farmacia, laboratorio, imágenes, hotelería y prótesis. Los copagos se analizarán por separado para distinguir los gastos de la atención de la participación económica del paciente.

Estos indicadores permiten comparar los resultados entre periodos, establecimientos de salud, aseguradoras, diagnósticos, tipos de cobertura y ubicaciones geográficas. Su análisis facilita la identificación de prestaciones con mayor demanda, componentes que concentran los gastos y diferencias en la utilización de los servicios, proporcionando información relevante para mejorar la planificación y apoyar la toma de decisiones en el sector salud.

### 1.8. Aplicación de BI al análisis de prestaciones de salud

Las organizaciones del sector salud generan grandes cantidades de datos relacionados con pacientes, establecimientos, aseguradoras, diagnósticos, coberturas, hospitalizaciones y gastos. Business Intelligence permite integrar y analizar esta información para convertirla en indicadores que faciliten la evaluación de la demanda de servicios y la toma de decisiones. Mediante reportes y visualizaciones, es posible comparar la cantidad de prestaciones entre periodos, identificar los diagnósticos y establecimientos que concentran mayores gastos y analizar la composición de estos según conceptos como honorarios, farmacia, laboratorio, imágenes y hotelería.

SUSALUD recopila información de las prestaciones realizadas por establecimientos privados, incluyendo características de la atención, datos demográficos anonimizados y montos asociados. De esta manera, la aplicación de BI permite identificar patrones de utilización y gasto. La información obtenida puede apoyar la planificación de recursos, el seguimiento de las prestaciones y la supervisión del sector privado de salud.

## 2. Descripción de la institución y problemática

### 2.1. Descripción de la institución

La institución seleccionada para el desarrollo del proyecto es la Superintendencia Nacional de Salud (SUSALUD), entidad del Estado peruano encargada de promover, proteger y restituir los derechos en salud de las personas. Su labor comprende la supervisión de los establecimientos y aseguradoras de salud, con la finalidad de contribuir a que los servicios sean brindados con calidad, oportunidad, disponibilidad y aceptabilidad (Superintendencia Nacional de Salud [SUSALUD], s. f.).

SUSALUD tiene competencia sobre las Instituciones Prestadoras de Servicios de Salud (IPRESS) y las Instituciones Administradoras de Fondos de Aseguramiento en Salud (IAFAS), tanto públicas como privadas y mixtas. Las IPRESS corresponden a los establecimientos y servicios médicos que realizan actividades de prevención, diagnóstico, tratamiento o rehabilitación, mientras que las IAFAS se encargan de administrar los fondos destinados al aseguramiento y a la cobertura de las prestaciones de salud.

Como parte de sus funciones de supervisión, SUSALUD recopila y publica información sobre las prestaciones realizadas en establecimientos privados. Los registros contienen datos anonimizados sobre aseguradoras, establecimientos, pacientes, diagnósticos, coberturas, hospitalizaciones, ubicación y diferentes componentes del gasto. Por ello, esta información resulta apropiada para la aplicación de herramientas de Business Intelligence que permitan analizar la demanda de prestaciones, la distribución de los gastos y las diferencias entre establecimientos, coberturas y grupos de pacientes.

El presente proyecto analizará únicamente las prestaciones reportadas por las IPRESS privadas registradas en SUSALUD que, durante el año anterior a la presentación de la información, registraron una facturación mensual promedio igual o superior a veinte Unidades Impositivas Tributarias. Esta delimitación responde al alcance de los archivos publicados por SUSALUD y significa que los resultados no representan necesariamente a todos los establecimientos privados de salud del Perú (SUSALUD, 2025).

### 2.2. Problemática

El sector salud genera grandes volúmenes de información sobre pacientes, establecimientos, aseguradoras, diagnósticos, coberturas, hospitalizaciones y gastos. El análisis de estos datos es importante para conocer cómo se utilizan los servicios, qué prestaciones concentran la mayor demanda registrada y cómo se distribuyen los recursos económicos entre los distintos componentes de la atención. En el Perú, SUSALUD supervisa a las Instituciones Prestadoras de Servicios de Salud (IPRESS) y a las Instituciones Administradoras de Fondos de Aseguramiento en Salud (IAFAS), incluyendo sus aspectos sanitarios, administrativos y financieros (Superintendencia Nacional de Salud [SUSALUD], s. f.).

Como parte de esta labor, SUSALUD publica mensualmente registros detallados de las prestaciones realizadas por determinadas IPRESS privadas. Estos datos incluyen características de la atención, información anonimizada de los pacientes, diagnósticos, tipos de cobertura, hospitalizaciones, ubicación y diversos componentes del gasto. Sin embargo, debido al elevado volumen de registros y a la variedad de campos disponibles, resulta complejo obtener una visión consolidada que permita comparar el comportamiento de las prestaciones entre periodos, establecimientos, aseguradoras, diagnósticos y grupos de pacientes mediante consultas convencionales.

- **Impacto en la gestión de los gastos:** Cada prestación puede contener diferentes componentes económicos. El análisis separado de estos campos dificulta conocer qué conceptos concentran la mayor proporción del gasto y cómo varían según el diagnóstico, la cobertura, el establecimiento o la aseguradora. Al integrar la información se pueden identificar patrones de gasto elevado que requieran un análisis más detallado, sin asumir necesariamente que representan ineficiencias o cobros inadecuados.

- **Impacto en la planificación de las prestaciones:** La cantidad y características de las atenciones pueden variar según el periodo, el diagnóstico u otros factores. Sin una estructura analítica que permita relacionar estas variables, resulta difícil identificar los servicios con mayor utilización, los grupos que concentran determinadas prestaciones y los periodos en los que se registra una mayor demanda. Esta información es relevante para orientar la planificación y el seguimiento de los servicios de salud.

- **Impacto en la gestión de la información:** Los datos se publican en archivos mensuales y contienen diferentes fechas, códigos anonimizados, categorías de atención y medidas monetarias. Para analizarlos de manera conjunta es necesario consolidarlos, estandarizar sus formatos y organizarlos bajo un nivel de detalle común. Para el alcance de este proyecto, se requiere un modelo analítico que permita elaborar indicadores consistentes y comparar los resultados entre las distintas perspectivas de análisis.

Por ello, existe la necesidad de integrar y organizar los registros de prestaciones de salud privadas mediante una solución de Business Intelligence. Esta solución permitirá realizar el seguimiento de indicadores como la cantidad de prestaciones, el monto total y promedio liquidado, la composición del gasto y los días de estancia facturable. Asimismo, facilitará la identificación de patrones según periodo, IAFAS, IPRESS, diagnóstico, cobertura, ubicación y características del paciente, proporcionando información que pueda apoyar la supervisión y la toma de decisiones basada en datos.

El análisis estará limitado a las IPRESS privadas incluidas en los archivos publicados por SUSALUD, las cuales corresponden a establecimientos que alcanzaron el nivel de facturación establecido para el reporte. Además, debido a que la fuente no contiene información completa sobre resultados clínicos, capacidad instalada o satisfacción del paciente, el proyecto no evaluará la calidad médica, la necesidad clínica de las prestaciones ni la rentabilidad de los establecimientos. Su alcance se concentrará en la utilización registrada y en la distribución de los gastos asociados (SUSALUD, 2025).

**Pregunta general de la problemática:**

> ¿Cómo puede una solución de Business Intelligence integrar y analizar los registros de prestaciones de salud del sector privado publicados por SUSALUD para identificar patrones de utilización y gasto que apoyen la planificación, supervisión y toma de decisiones?

### 2.3. Objetivo general

Diseñar e implementar una solución de Business Intelligence para analizar las prestaciones de salud del sector privado registradas por SUSALUD, estructurada mediante un modelo en estrella e integrada con los archivos publicados en la Plataforma Nacional de Datos Abiertos, con el fin de transformar grandes volúmenes de registros en información analítica que permita identificar patrones de utilización y gasto según periodo, IAFAS, IPRESS, diagnóstico, cobertura, ubicación y características del paciente, apoyando la planificación, la supervisión y la toma de decisiones basada en datos.

### 2.4. Objetivos específicos

1. **Consolidar y preparar la fuente de datos:** Extraer, integrar, limpiar y transformar los archivos mensuales publicados por SUSALUD para construir una base de datos analítica estandarizada, validando formatos, registros duplicados, valores faltantes y consistencia de los montos.

2. **Analizar los patrones de utilización de las prestaciones:** Identificar los periodos, diagnósticos, tipos de cobertura y subtipos de prestación que concentran la mayor cantidad de atenciones registradas.

3. **Evaluar la distribución de las prestaciones:** Comparar la cantidad de atenciones y los gastos asociados según IAFAS, IPRESS, ubicación geográfica y características demográficas de los pacientes, como sexo y grupo etario.

4. **Analizar la composición de los gastos:** Determinar la participación de los honorarios, procedimientos, farmacia, laboratorio, imágenes, hotelería, prótesis y otros conceptos en la suma de los componentes del gasto registrados, y analizar por separado los copagos, identificando los componentes y categorías que concentran los mayores montos.

5. **Diseñar el data mart multidimensional y los tableros de control:** Construir un modelo dimensional en estrella con al menos ocho dimensiones y desarrollar tableros interactivos que faciliten el seguimiento de la utilización, los gastos y las estancias hospitalarias, apoyando la planificación, supervisión y toma de decisiones.

### 2.5. Preguntas de negocio

#### Análisis temporal de las prestaciones

- ¿Cómo varían mensualmente la cantidad de prestaciones registradas y el monto total liquidado por las IAFAS?

- ¿En qué periodos se observa el mayor monto promedio liquidado por prestación?

#### Análisis por diagnósticos y coberturas

- ¿Qué diagnósticos y tipos de cobertura concentran la mayor cantidad de prestaciones?

- ¿Qué diagnósticos presentan los mayores montos totales y promedios liquidados por prestación?

#### Análisis por establecimientos, aseguradoras y ubicación

- ¿Qué IPRESS e IAFAS concentran la mayor cantidad de prestaciones y los mayores montos liquidados?

- ¿Cómo varían los montos promedio por prestación entre IPRESS para un mismo diagnóstico y tipo de cobertura?

- ¿Cómo se distribuyen las prestaciones y los gastos registrados según la ubicación del establecimiento y la residencia del afiliado?

#### Análisis de la composición del gasto y los copagos

- ¿Qué proporción de la suma de los componentes de gasto registrados corresponde a farmacia, honorarios y procedimientos, laboratorio, imágenes, hotelería y otros conceptos?

- ¿Cómo varían los copagos promedio por prestación según la IAFAS y el tipo de cobertura?

#### Análisis por características de los pacientes

- ¿Qué grupos etarios y sexos concentran la mayor cantidad de prestaciones y los mayores montos liquidados?

- ¿Cuáles son los diagnósticos más frecuentes entre las prestaciones registradas para cada grupo etario?

#### Análisis de hospitalización

Entre las prestaciones hospitalarias, ¿qué diagnósticos y tipos de hospitalización presentan el mayor promedio de días de estancia facturable?

- ¿Cómo varía el monto promedio liquidado por prestación hospitalaria según los días de estancia facturable y el diagnóstico?

## 3. Modelamiento dimensional de datos

### 3.1. Fuente de datos

La fuente principal del proyecto es el conjunto de datos Registro de datos de atenciones de la cobertura prestacional de salud del sector privado, publicado por la Superintendencia Nacional de Salud (SUSALUD) en la Plataforma Nacional de Datos Abiertos. La base contiene información de prestaciones realizadas por determinadas Instituciones Prestadoras de Servicios de Salud (IPRESS) privadas registradas en SUSALUD. Incluye campos sobre aseguradoras (IAFAS), establecimientos (IPRESS), diagnósticos, cobertura, fechas de atención, hospitalización, datos demográficos anonimizados y componentes del gasto asociado a las prestaciones (SUSALUD, 2025).

Para el proyecto se descargaron los archivos mensuales correspondientes a enero, febrero y marzo de 2026. Los tres archivos fueron consolidados en una sola base mediante Power Query. El conjunto resultante contiene 781,556 registros y 40 campos, por lo que supera el requisito mínimo de 500,000 registros. Se conservó el campo `Source.Name` para identificar el archivo mensual del que proviene cada registro.

Los meses señalados corresponden a los archivos de publicación descargados y pueden incluir prestaciones realizadas en fechas anteriores. El análisis temporal de las atenciones utilizará la fecha de prestación.

La información incluye montos de honorarios y procedimientos, farmacia, laboratorio, imágenes, hotelería, prótesis, copagos, total de gastos cubiertos y monto liquidado por las IAFAS. Estos campos permitirán analizar la cantidad y distribución de las prestaciones, así como la composición de los gastos según periodo, diagnóstico, cobertura, aseguradora, establecimiento y ubicación. Los códigos anonimizados de pacientes, IAFAS e IPRESS se conservarán como identificadores analíticos, sin intentar identificar a las personas o instituciones.

La fuente fue seleccionada porque es oficial, contiene información detallada sobre prestaciones y gastos, y permite construir indicadores útiles para analizar su utilización y distribución. El conjunto de datos y su diccionario se encuentran en la [página oficial de SUSALUD](https://www.datosabiertos.gob.pe/dataset/registro-de-datos-de-atenciones-de-la-cobertura-prestacional-de-salud-del-sector-privado).

### 3.2. Descripción general de los datos

Cada fila contiene el registro de una prestación de salud reportada por una IPRESS privada. La base incluye códigos anonimizados de la IAFAS, la IPRESS y el paciente; el diagnóstico principal; el tipo y subtipo de cobertura; la fecha de prestación; características del paciente y, cuando corresponde, información sobre la hospitalización.

Los campos monetarios detallan gastos por honorarios y procedimientos, farmacia, laboratorio, imágenes, hotelería, prótesis y otros conceptos. También se registran copagos, el total de gastos cubiertos y el monto liquidado por la IAFAS. Los días de estancia facturable se expresan como una duración, mientras que las fechas de prestación, ingreso y egreso permiten ubicar las atenciones en el tiempo.

### 3.3. Diccionario de datos de la fuente

El diccionario de la fuente describe los campos originales utilizados durante la preparación de los datos. Posteriormente, los diccionarios de la tabla de hechos y de las dimensiones describen la estructura propuesta para el Data Mart. Por lo tanto, algunos campos de la fuente se transforman, se separan entre diferentes tablas o se excluyen del modelo analítico.

Los tipos de datos y la columna «Nulos» corresponden a la propuesta de almacenamiento; no representan una validación exhaustiva de todos los registros. Las fechas en formato AAAAMMDD se convertirán a `DATE` y los ubigeos se prepararán como texto de seis caracteres.

| Nombre del campo | Tipo de dato propuesto | Descripción del campo | Nulos |
| --- | --- | --- | --- |
| `Source.Name` | `VARCHAR(255)` | Nombre del archivo mensual de origen. | No |
| `VCODIAFAS_FAC` | `VARCHAR(64)` | Código anonimizado de la Institución Administradora de Fondos de Aseguramiento en Salud (IAFAS). | No |
| `VCODIPRESS_FAC` | `VARCHAR(64)` | Código anonimizado de la Institución Prestadora de Servicios de Salud (IPRESS). | No |
| `VTDOCPAGO_FAC` | `VARCHAR(10)` | Código del tipo de documento de pago. | No |
| `VNDOCPAGO_FAC` | `VARCHAR(64)` | Número anonimizado del documento de pago. | No |
| `VCORRPRESTA_ATE` | `INT` | Correlativo de la prestación dentro del documento de pago. | No |
| `VTAFILPAC_ATE` | `VARCHAR(10)` | Código del tipo de afiliación del paciente. | No |
| `VTDOCIDEN_ATE` | `VARCHAR(10)` | Código del tipo de documento de identidad del paciente. | No |
| `VNUMDOCIDEN_ATE` | `VARCHAR(64)` | Número anonimizado del documento de identidad del paciente. | No |
| `VTIPOCOBERT_ATE` | `VARCHAR(10)` | Código del tipo de cobertura o prestación de salud. | No |
| `VSUBTIPCOBERT_ATE` | `VARCHAR(10)` | Código del subtipo de cobertura de la prestación. | No |
| `VPRIDIAGCIE_ATE` | `VARCHAR(10)` | Código del primer diagnóstico registrado, según la clasificación CIE-10. | No |
| `VFECPRES_ATE` | `DATE` | Fecha en que se realizó la prestación de salud. | No |
| `VTITPRORESPRES_ATE` | `VARCHAR(10)` | Código del tipo de profesional responsable de la prestación. | No |
| `VTIPOHOSPI_ATE` | `VARCHAR(10)` | Código del tipo de hospitalización, cuando corresponde. | Sí |
| `VFECINGRHOSP_ATE` | `DATE` | Fecha de ingreso hospitalario. | Sí |
| `VFECEGRHOSP_ATE` | `DATE` | Fecha de egreso hospitalario. | Sí |
| `VTIPEGREHOSP_ATE` | `VARCHAR(10)` | Código del tipo de egreso hospitalario. | Sí |
| `VDIASESTFAC_ATE` | `INT` | Cantidad de días de estancia facturable. | Sí |
| `VFECNACPAC_ATE` | `DATE` | Fecha de nacimiento del paciente. | No |
| `VSEXOPAC_ATE` | `VARCHAR(10)` | Código del sexo del paciente. | No |
| `VFILIAPAC_ATE` | `VARCHAR(10)` | Código de filiación del paciente. | No |
| `VUBIGEOIPRESS_ATE` | `CHAR(6)` | Código de ubicación geográfica de la IPRESS, según el INEI. | No |
| `VGASTHONPROSIGV_ATE` | `DECIMAL(18,2)` | Gasto por honorarios y procedimientos, sin IGV. | No |
| `VGASTPRODOSIGV_ATE` | `DECIMAL(18,2)` | Gasto por procedimientos odontológicos, sin IGV. | No |
| `VGASTHTSCLITOPSIGV_ATE` | `DECIMAL(18,2)` | Gasto presentado por hotelería, servicio clínico y tópico, sin IGV. | No |
| `VGASTEXAUXLABSIGV_ATE` | `DECIMAL(18,2)` | Gasto por exámenes auxiliares de laboratorio, sin IGV. | No |
| `VGASTEXAUXIMGSIGV_ATE` | `DECIMAL(18,2)` | Gasto por exámenes auxiliares por imágenes, sin IGV. | No |
| `VGASTFARINSSIGV_ATE` | `DECIMAL(18,2)` | Gasto por farmacia e insumos, sin IGV. | No |
| `VGASTPROTSIGV_ATE` | `DECIMAL(18,2)` | Gasto en prótesis, sin IGV. | No |
| `VGASTMEDEXOIGV_ATE` | `DECIMAL(18,2)` | Gasto en productos, servicios o medicamentos exonerados de IGV. | No |
| `VOGPRESSLDSIGV_ATE` | `DECIMAL(18,2)` | Otros gastos por prestaciones de salud, sin IGV. | No |
| `VCOPAGOFIJOSIGV_ATE` | `DECIMAL(18,2)` | Copago fijo correspondiente a conceptos afectos a IGV, expresado sin IGV. | No |
| `VCPAGOFIJOEXIGV_ATE` | `DECIMAL(18,2)` | Copago fijo correspondiente a conceptos exonerados de IGV. | No |
| `VCOPAGOVARSIGV_ATE` | `DECIMAL(18,2)` | Copago variable correspondiente a conceptos afectos a IGV, expresado sin IGV. | No |
| `VCPAGOVAREXIGV_ATE` | `DECIMAL(18,2)` | Copago variable correspondiente a conceptos exonerados de IGV. | No |
| `VTOTGASTCUBSIGV_ATE` | `DECIMAL(18,2)` | Total de gastos cubiertos, sin IGV. | No |
| `VTOTLIQIAFAS_ATE` | `DECIMAL(18,2)` | Monto total liquidado por la IAFAS. | No |
| `DFECRECEP_PQ` | `DATETIME2(0)` | Fecha y hora de recepción de la información en el TEDEF. | No |
| `UBIGEO_AFILIADO` | `CHAR(6)` | Código de ubicación geográfica del afiliado. | Sí |

### 3.4. Proceso de negocio

El proceso de negocio analizado es la prestación de servicios de salud en las IPRESS privadas incluidas en los registros publicados por SUSALUD, considerando la atención brindada al paciente y los gastos asociados. Cada prestación se relaciona con un paciente, un establecimiento, una IAFAS, un diagnóstico y una cobertura, e incluye información sobre hospitalización cuando corresponde.

El análisis permitirá evaluar la cantidad de prestaciones, la composición de los gastos, los montos liquidados por las IAFAS, los copagos y los días de estancia facturable. Asimismo, permitirá comparar estos resultados según fecha, establecimiento, aseguradora, diagnóstico, cobertura, ubicación y características del paciente. La información obtenida facilitará la identificación de patrones de utilización y concentración del gasto para apoyar la planificación y supervisión de las prestaciones registradas.

### 3.5. Granularidad

La granularidad de la tabla de hechos corresponde a una prestación de salud registrada, asociada con un paciente, una IPRESS, una IAFAS y un documento de pago, dentro del cual se identifica mediante un correlativo.

Por lo tanto, cada fila de `FactPrestacionSalud` representa una prestación e incluye sus respectivas claves dimensionales, componentes del gasto, copagos y monto liquidado por la IAFAS. Las prestaciones que no implican hospitalización también se conservan, aunque las fechas de ingreso y egreso de la fuente pueden estar vacías. En el modelo, sus claves se vincularán con registros especiales de «No aplica», mientras que los días de estancia facturable podrán permanecer como `NULL`.

La granularidad puede expresarse de la siguiente manera:

> Una fila por cada prestación de salud registrada dentro de un documento de pago, vinculada con un paciente, un establecimiento de salud y una entidad financiadora.

Esta definición asegura que las medidas económicas y los días de estancia facturable correspondan al mismo nivel de detalle. Un paciente o un documento de pago pueden estar asociados con varias prestaciones, por lo que una fila no equivale necesariamente a un paciente único, una factura completa o una hospitalización completa.

### 3.6. Tabla de hechos

La tabla `FactPrestacionSalud` constituye la tabla central del modelo dimensional. Cada registro representa una prestación de salud registrada dentro de un documento de pago, vinculada con un paciente, una IPRESS y una IAFAS, e identificada dentro del documento mediante un correlativo.

Esta tabla contiene las claves foráneas que relacionan cada prestación con sus dimensiones y las medidas utilizadas para analizar la cantidad de prestaciones, los componentes del gasto, los copagos, los montos liquidados y los días de estancia facturable. También conserva los identificadores del documento de pago y el correlativo para facilitar la trazabilidad y la validación de los registros.

Los campos se presentan con nombres más comprensibles, manteniendo su correspondencia con las variables de la fuente original.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `PrestacionKey` | `BIGINT` | Clave sustituta que identifica de manera única cada registro de la tabla de hechos. | No |
| `FechaPrestacionKey` | `INT` | Clave foránea que relaciona la prestación con su fecha de atención en `DimFecha`. | No |
| `FechaIngresoKey` | `INT` | Clave foránea que relaciona la prestación con su fecha de ingreso hospitalario en `DimFecha`. | No |
| `FechaEgresoKey` | `INT` | Clave foránea que relaciona la prestación con su fecha de egreso hospitalario en `DimFecha`. | No |
| `FechaRecepcionKey` | `INT` | Clave foránea que relaciona la prestación con la fecha de recepción de la información en el TEDEF, mediante `DimFecha`. | No |
| `IafasKey` | `INT` | Clave foránea que identifica la entidad financiadora en `DimIAFAS`. | No |
| `IpressKey` | `INT` | Clave foránea que identifica el establecimiento de salud en `DimIPRESS`. | No |
| `PacienteKey` | `INT` | Clave foránea que relaciona la prestación con el paciente anonimizado en `DimPaciente`. | No |
| `AfiliacionKey` | `INT` | Clave foránea que relaciona la prestación con las condiciones de afiliación del paciente en `DimAfiliacion`. | No |
| `CoberturaKey` | `INT` | Clave foránea que identifica el tipo y subtipo de cobertura en `DimCobertura`. | No |
| `DiagnosticoKey` | `INT` | Clave foránea que identifica el diagnóstico principal registrado en `DimDiagnostico`. | No |
| `TipoProfesionalKey` | `INT` | Clave foránea que identifica la categoría del profesional responsable en `DimTipoProfesional`. | No |
| `HospitalizacionKey` | `INT` | Clave foránea que identifica el tipo de hospitalización y de egreso en `DimHospitalizacion`. | No |
| `UbicacionIpressKey` | `INT` | Clave foránea que identifica la ubicación del establecimiento de salud en `DimUbicacion`. | No |
| `UbicacionAfiliadoKey` | `INT` | Clave foránea que identifica la ubicación del afiliado en `DimUbicacion`. | No |
| `TipoDocumentoPago` | `VARCHAR(10)` | Código del tipo de documento de pago asociado con la prestación. | No |
| `DocumentoPagoAnonimizado` | `VARCHAR(64)` | Número anonimizado del documento de pago asociado con la prestación. | No |
| `CorrelativoPrestacion` | `INT` | Correlativo que identifica la prestación dentro del documento de pago. | No |
| `CantidadPrestaciones` | `TINYINT` | Contador de prestaciones. Toma el valor 1 por cada registro. | No |
| `DiasEstanciaFacturable` | `INT` | Cantidad de días de estancia facturable registrados para la prestación, cuando corresponde. | Sí |
| `GastoHonorariosProcedimientos` | `DECIMAL(18,2)` | Gasto por honorarios y procedimientos, sin IGV. | No |
| `GastoOdontologia` | `DECIMAL(18,2)` | Gasto por procedimientos odontológicos, sin IGV. | No |
| `GastoHoteleriaServicioClinicoTopico` | `DECIMAL(18,2)` | Gasto presentado por hotelería, servicio clínico y tópico, sin IGV. | No |
| `GastoLaboratorio` | `DECIMAL(18,2)` | Gasto por exámenes auxiliares de laboratorio, sin IGV. | No |
| `GastoImagenes` | `DECIMAL(18,2)` | Gasto por exámenes auxiliares por imágenes, sin IGV. | No |
| `GastoFarmaciaInsumos` | `DECIMAL(18,2)` | Gasto por farmacia e insumos, sin IGV. | No |
| `GastoProtesis` | `DECIMAL(18,2)` | Gasto en prótesis, sin IGV. | No |
| `GastoExoneradoIGV` | `DECIMAL(18,2)` | Gasto en productos, servicios o medicamentos exonerados de IGV. | No |
| `OtrosGastos` | `DECIMAL(18,2)` | Otros gastos por prestaciones de salud, sin IGV. | No |
| `CopagoFijoAfectoSinIGV` | `DECIMAL(18,2)` | Copago fijo correspondiente a conceptos afectos a IGV, expresado sin IGV. | No |
| `CopagoFijoExonerado` | `DECIMAL(18,2)` | Copago fijo correspondiente a conceptos exonerados de IGV. | No |
| `CopagoVariableAfectoSinIGV` | `DECIMAL(18,2)` | Copago variable correspondiente a conceptos afectos a IGV, expresado sin IGV. | No |
| `CopagoVariableExonerado` | `DECIMAL(18,2)` | Copago variable correspondiente a conceptos exonerados de IGV. | No |
| `TotalGastosCubiertosSinIGV` | `DECIMAL(18,2)` | Total de gastos cubiertos, sin IGV, registrado para la prestación. | No |
| `TotalLiquidadoIAFAS` | `DECIMAL(18,2)` | Monto total liquidado por la IAFAS para la prestación. | No |

Las claves foráneas no admitirán valores nulos. Para las prestaciones sin hospitalización se utilizarán registros especiales de «No aplica» en las dimensiones correspondientes. Cuando un dato no esté informado, como la ubicación del afiliado, se utilizará un registro de «Desconocido». Los días de estancia facturable permanecerán como `NULL` cuando no correspondan, evitando incorporarlos como ceros en los promedios de estancia.

Los componentes del gasto, los copagos y los totales se analizarán según su significado. No se sumarán todos estos campos para obtener un nuevo total, porque algunos representan componentes o diferentes formas de distribución de un mismo importe. Asimismo, los días de estancia facturable no se interpretarán automáticamente como días únicos de hospitalización de un paciente.

### 3.7. Tablas de dimensiones

Las tablas de dimensiones almacenan la información descriptiva que permite analizar las medidas de `FactPrestacionSalud` desde diferentes perspectivas. El modelo cuenta con diez dimensiones: fecha, IAFAS, IPRESS, paciente, afiliación, cobertura, diagnóstico, tipo de profesional, hospitalización y ubicación.

`DimFecha` y `DimUbicacion` cumplen varias funciones dentro del modelo. `DimFecha` representa las fechas de prestación, ingreso hospitalario, egreso hospitalario y recepción de la información. Por su parte, `DimUbicacion` representa la ubicación de la IPRESS y la del afiliado.

#### DimFecha

Permite analizar las prestaciones y sus gastos según diferentes periodos y niveles de detalle temporal. Se relaciona cuatro veces con la tabla de hechos, de acuerdo con la función de cada fecha.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `FechaKey` | `INT` | Clave primaria de la dimensión. Utiliza el formato AAAAMMDD para fechas válidas y valores reservados para registros especiales. | No |
| `Fecha` | `DATE` | Fecha completa. | Sí |
| `Anio` | `SMALLINT` | Año de la fecha. | Sí |
| `Trimestre` | `TINYINT` | Trimestre del año, con valores del 1 al 4. | Sí |
| `Mes` | `TINYINT` | Número del mes, con valores del 1 al 12. | Sí |
| `NombreMes` | `VARCHAR(15)` | Nombre del mes. | Sí |
| `Dia` | `TINYINT` | Día del mes, con valores del 1 al 31. | Sí |
| `DiaSemana` | `TINYINT` | Día de la semana: 1 = lunes y 7 = domingo. | Sí |
| `NombreDiaSemana` | `VARCHAR(15)` | Nombre del día de la semana. | Sí |
| `TipoRegistroFecha` | `VARCHAR(20)` | Clasifica el registro como fecha válida, no aplica o desconocida. | No |

Los atributos temporales admitirán valores nulos únicamente en los registros especiales de «No aplica» y «Desconocido». Esto permite conservar claves foráneas no nulas en la tabla de hechos sin asignar fechas ficticias a las prestaciones.

#### DimIAFAS

Identifica a la entidad que administra los fondos de aseguramiento vinculados con la prestación. Permite comparar la cantidad de prestaciones, los gastos, los copagos y los montos liquidados entre entidades.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `IafasKey` | `INT` | Clave sustituta de la dimensión IAFAS. | No |
| `CodigoIafasAnonimizado` | `VARCHAR(64)` | Código anonimizado de la IAFAS, procedente de `VCODIAFAS_FAC`. | No |

La fuente contiene códigos anonimizados, por lo que no permite identificar el nombre real de cada IAFAS.

#### DimIPRESS

Identifica al establecimiento de salud asociado con la prestación. Permite comparar la utilización y los gastos registrados entre establecimientos.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `IpressKey` | `INT` | Clave sustituta de la dimensión IPRESS. | No |
| `CodigoIpressAnonimizado` | `VARCHAR(64)` | Código anonimizado de la IPRESS, procedente de `VCODIPRESS_FAC`. | No |

La ubicación del establecimiento se relaciona directamente con la tabla de hechos mediante `UbicacionIpressKey`. El código anonimizado no permite conocer el nombre real del establecimiento.

#### DimPaciente

Contiene el identificador anonimizado del paciente y sus características demográficas. Permite analizar las prestaciones según sexo y calcular la edad del paciente en la fecha de atención.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `PacienteKey` | `INT` | Clave sustituta de la dimensión paciente. | No |
| `TipoDocumentoIdentidad` | `VARCHAR(10)` | Código del tipo de documento de identidad del paciente, procedente de `VTDOCIDEN_ATE`. | No |
| `PacienteAnonimizado` | `VARCHAR(64)` | Número anonimizado del documento de identidad del paciente, procedente de `VNUMDOCIDEN_ATE`. | No |
| `FechaNacimiento` | `DATE` | Fecha de nacimiento del paciente, procedente de `VFECNACPAC_ATE`. | No |
| `CodigoSexo` | `VARCHAR(10)` | Código del sexo del paciente, procedente de `VSEXOPAC_ATE`. | No |

La edad y el grupo etario se calcularán utilizando la fecha de nacimiento y la fecha de prestación. Así, la clasificación reflejará la edad que tenía el paciente cuando recibió la atención.

#### DimAfiliacion

Describe el tipo de afiliación y la filiación del paciente registrados para cada prestación. Se mantiene separada de `DimPaciente` porque estas condiciones pueden variar entre atenciones.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `AfiliacionKey` | `INT` | Clave sustituta de la dimensión afiliación. | No |
| `CodigoTipoAfiliacion` | `VARCHAR(10)` | Código del tipo de afiliación del paciente, procedente de `VTAFILPAC_ATE`. | No |
| `CodigoFiliacionPaciente` | `VARCHAR(10)` | Código de filiación del paciente, procedente de `VFILIAPAC_ATE`. | No |

#### DimCobertura

Permite clasificar las prestaciones según el tipo y subtipo de cobertura, y comparar su cantidad, gastos y copagos.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `CoberturaKey` | `INT` | Clave sustituta de la dimensión cobertura. | No |
| `CodigoTipoCobertura` | `VARCHAR(10)` | Código del tipo de cobertura o prestación de salud, procedente de `VTIPOCOBERT_ATE`. | No |
| `CodigoSubtipoCobertura` | `VARCHAR(10)` | Código del subtipo de cobertura, procedente de `VSUBTIPCOBERT_ATE`. | No |

#### DimDiagnostico

Permite analizar la cantidad de prestaciones, los gastos y las estancias facturables según el diagnóstico principal registrado.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `DiagnosticoKey` | `INT` | Clave sustituta de la dimensión diagnóstico. | No |
| `CodigoDiagnosticoCIE10` | `VARCHAR(10)` | Código del primer diagnóstico registrado, procedente de `VPRIDIAGCIE_ATE`. | No |
| `DescripcionDiagnostico` | `VARCHAR(500)` | Descripción del diagnóstico, obtenida de un catálogo oficial CIE-10 compatible con la fuente. | Sí |

La descripción se incorporará mediante una tabla auxiliar. Los códigos que no encuentren correspondencia se conservarán y quedarán pendientes de revisión.

#### DimTipoProfesional

Permite analizar las prestaciones según la categoría del profesional responsable. Representa tipos de profesionales, dado que la fuente no identifica individualmente a cada profesional.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `TipoProfesionalKey` | `INT` | Clave sustituta de la dimensión tipo de profesional. | No |
| `CodigoTipoProfesional` | `VARCHAR(10)` | Código del tipo de profesional responsable de la prestación, procedente de `VTITPRORESPRES_ATE`. | No |

#### DimHospitalizacion

Clasifica las prestaciones según el tipo de hospitalización y el tipo de egreso. Las fechas de ingreso y egreso y los días de estancia facturable se mantienen relacionados con la tabla de hechos.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `HospitalizacionKey` | `INT` | Clave sustituta de la dimensión hospitalización. | No |
| `CodigoTipoHospitalizacion` | `VARCHAR(10)` | Código del tipo de hospitalización, procedente de `VTIPOHOSPI_ATE`. | Sí |
| `CodigoTipoEgreso` | `VARCHAR(10)` | Código del tipo de egreso hospitalario, procedente de `VTIPEGREHOSP_ATE`. | Sí |

Se incluirá un registro especial de «No aplica» para las prestaciones sin hospitalización. Los datos faltantes en prestaciones hospitalarias se distinguirán mediante un registro de «Desconocido».

#### DimUbicacion

Contiene la información geográfica que permite analizar la distribución territorial de las prestaciones y los gastos. Se relaciona dos veces con la tabla de hechos: como ubicación de la IPRESS y como ubicación del afiliado. Los códigos de ubigeo proceden de los campos `VUBIGEOIPRESS_ATE` y `UBIGEO_AFILIADO` de la fuente principal. Para incorporar los nombres de departamento, provincia y distrito, se utilizará una tabla auxiliar oficial de ubigeos del INEI, vinculada mediante el código geográfico de seis caracteres.

| Campo | Tipo de dato | Descripción | Nulos |
| --- | --- | --- | --- |
| `UbicacionKey` | `INT` | Clave sustituta de la dimensión ubicación. | No |
| `Ubigeo` | `CHAR(6)` | Código geográfico procedente de `VUBIGEOIPRESS_ATE` o `UBIGEO_AFILIADO`. | Sí |
| `Departamento` | `VARCHAR(100)` | Nombre del departamento, obtenido mediante un catálogo oficial del INEI. | Sí |
| `Provincia` | `VARCHAR(100)` | Nombre de la provincia, obtenido mediante un catálogo oficial del INEI. | Sí |
| `Distrito` | `VARCHAR(100)` | Nombre del distrito, obtenido mediante un catálogo oficial del INEI. | Sí |

Los ubigeos se almacenarán como texto de seis caracteres para conservar sus ceros iniciales. Se incluirá un registro de «Desconocido» para ubicaciones no informadas; los códigos disponibles que no encuentren correspondencia en el catálogo se conservarán para su revisión.

## Bibliografía

IBM. (2021, 30 de julio). *What is OLAP?* https://www.ibm.com/think/topics/olap

IBM. (s. f.). *¿Qué es Business Intelligence (BI)?* https://www.ibm.com/mx-es/think/topics/business-intelligence

IBM. (s. f.). *¿Qué es un mercado de datos?* https://www.ibm.com/mx-es/think/topics/data-mart

IBM. (s. f.). *What is a data warehouse?* https://www.ibm.com/think/topics/data-warehouse

IBM. (s. f.). *What is ETL (extract, transform, load)?* https://www.ibm.com/think/topics/etl

Instituto Nacional de Estadística e Informática. (s. f.). *Ubigeos (códigos de ubicación geográfica)*. Plataforma Nacional de Datos Abiertos. https://www.datosabiertos.gob.pe/dataset/ubigeos-c%C3%B3digos-de-ubicaci%C3%B3n-geogr%C3%A1fica-instituto-nacional-de-estad%C3%ADstica-e-inform%C3%A1tica-inei

Kimball Group. (s. f.). *Dimensional modeling techniques*. https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/

Kimball, R. (2008, 5 de noviembre). *Fact tables*. Kimball Group. https://www.kimballgroup.com/2008/11/fact-tables/

Microsoft. (s. f.). *Understand star schema and the importance for Power BI*. Microsoft Learn. https://learn.microsoft.com/en-us/power-bi/guidance/star-schema

Oracle. (2023, 8 de junio). *What is a data warehouse?* https://www.oracle.com/database/what-is-a-data-warehouse/

Superintendencia Nacional de Salud. (2025). *Registro de datos de atenciones de la cobertura prestacional de salud del sector privado*. Plataforma Nacional de Datos Abiertos. https://www.datosabiertos.gob.pe/dataset/registro-de-datos-de-atenciones-de-la-cobertura-prestacional-de-salud-del-sector-privado

Superintendencia Nacional de Salud. (s. f.). *Información institucional*. Plataforma Digital Única del Estado Peruano. https://www.gob.pe/institucion/susalud/institucional

