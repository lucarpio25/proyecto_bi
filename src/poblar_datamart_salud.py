# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:11:34 2026

@author: lu

Carga inicial: ejecutar con las tablas del datamart vacías.
Si ya contienen registros, el script se detiene sin borrarlos.
Configurar SERVIDOR y dejar junto al script estos tres archivos:
BD_pagos.xlsx, TB_UBIGEOS.csv y CIE10_MINSA_OFICIAL.xlsx.
Las descripciones de subtipos de cobertura quedan pendientes del catálogo TEDEF.
"""

# ==========================
# %% IMPORTACIONES
# ==========================

from pathlib import Path
import pandas as pd
import pyodbc
from decimal import Decimal, InvalidOperation

# ==========================
# %% CONEXIÓN AL DATA MART
# ==========================

SERVIDOR = r"Laptop_Lu\SQLEXPRESS"
BASE_DATOS = "ProyectoDatamart"


def get_connection_destino():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SERVIDOR};"
        f"DATABASE={BASE_DATOS};"
        "Trusted_Connection=yes;",
        autocommit=False
    )

    print("Conexión al datamart exitosa")
    return conn

# ==========================
# %% CREAR EL DATA MART
# ==========================

def crear_base_datos():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SERVIDOR};"
        "DATABASE=master;"
        "Trusted_Connection=yes;",
        autocommit=True
    )

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT DB_ID(?)",
            BASE_DATOS
        )

        if cursor.fetchone()[0] is None:
            nombre_base = BASE_DATOS.replace("]", "]]")

            cursor.execute(
                f"CREATE DATABASE [{nombre_base}]"
            )

            print(f"Base de datos {BASE_DATOS} creada")
        else:
            print(f"La base de datos {BASE_DATOS} ya existe")

    finally:
        cursor.close()
        conn.close()


def crear_tablas_datamart(conn):
    cursor = conn.cursor()

    script = """
    IF OBJECT_ID('dbo.DimFecha', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimFecha (
            FechaKey INT NOT NULL PRIMARY KEY,
            Fecha DATE NULL,
            Anio SMALLINT NULL,
            Trimestre TINYINT NULL,
            Mes TINYINT NULL,
            NombreMes VARCHAR(15) NULL,
            Dia TINYINT NULL,
            DiaSemana TINYINT NULL,
            NombreDiaSemana VARCHAR(15) NULL,
            TipoRegistroFecha VARCHAR(20) NOT NULL
        );
    END;

    IF OBJECT_ID('dbo.DimIAFAS', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimIAFAS (
            IafasKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            CodigoIafasAnonimizado VARCHAR(64) NOT NULL
        );
    END;

    IF OBJECT_ID('dbo.DimIPRESS', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimIPRESS (
            IpressKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            CodigoIpressAnonimizado VARCHAR(64) NOT NULL
        );
    END;

    IF OBJECT_ID('dbo.DimPaciente', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimPaciente (
            PacienteKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            TipoDocumentoIdentidad VARCHAR(10) NOT NULL,
            PacienteAnonimizado VARCHAR(64) NOT NULL,
            FechaNacimiento DATE NOT NULL,
            CodigoSexo VARCHAR(10) NOT NULL,
            DescripcionSexo VARCHAR(20) NULL,
            DescripcionTipoDocumentoIdentidad VARCHAR(100) NULL
        );
    END;

    IF OBJECT_ID('dbo.DimAfiliacion', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimAfiliacion (
            AfiliacionKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            CodigoTipoAfiliacion VARCHAR(10) NOT NULL,
            CodigoFiliacionPaciente VARCHAR(10) NOT NULL,
            DescripcionTipoAfiliacion VARCHAR(100) NULL,
            DescripcionFiliacionPaciente VARCHAR(100) NULL
        );
    END;

    IF OBJECT_ID('dbo.DimCobertura', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimCobertura (
            CoberturaKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            CodigoTipoCobertura VARCHAR(10) NOT NULL,
            CodigoSubtipoCobertura VARCHAR(10) NOT NULL,
            DescripcionTipoCobertura VARCHAR(100) NULL
        );
    END;

    IF OBJECT_ID('dbo.DimDiagnostico', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimDiagnostico (
            DiagnosticoKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            CodigoDiagnosticoCIE10 VARCHAR(10) NOT NULL,
            DescripcionDiagnostico VARCHAR(500) NULL
        );
    END;

    IF OBJECT_ID('dbo.DimTipoProfesional', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimTipoProfesional (
            TipoProfesionalKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            CodigoTipoProfesional VARCHAR(10) NULL,
            DescripcionTipoProfesional VARCHAR(100) NULL
        );
    END;

    IF OBJECT_ID('dbo.DimHospitalizacion', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimHospitalizacion (
            HospitalizacionKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            CodigoTipoHospitalizacion VARCHAR(10) NULL,
            CodigoTipoEgreso VARCHAR(10) NULL,
            DescripcionTipoHospitalizacion VARCHAR(100) NULL,
            DescripcionTipoEgreso VARCHAR(100) NULL
        );
    END;

    IF OBJECT_ID('dbo.DimUbicacion', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DimUbicacion (
            UbicacionKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            Ubigeo CHAR(6) NULL,
            Departamento VARCHAR(100) NULL,
            Provincia VARCHAR(100) NULL,
            Distrito VARCHAR(100) NULL
        );
    END;

    IF OBJECT_ID('dbo.FactPrestacionSalud', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.FactPrestacionSalud (
            PrestacionKey BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,

            FechaPrestacionKey INT NOT NULL,
            FechaIngresoKey INT NOT NULL,
            FechaEgresoKey INT NOT NULL,
            FechaRecepcionKey INT NOT NULL,
            IafasKey INT NOT NULL,
            IpressKey INT NOT NULL,
            PacienteKey INT NOT NULL,
            AfiliacionKey INT NOT NULL,
            CoberturaKey INT NOT NULL,
            DiagnosticoKey INT NOT NULL,
            TipoProfesionalKey INT NOT NULL,
            HospitalizacionKey INT NOT NULL,
            UbicacionIpressKey INT NOT NULL,
            UbicacionAfiliadoKey INT NOT NULL,

            TipoDocumentoPago VARCHAR(10) NULL,
            DocumentoPagoAnonimizado VARCHAR(64) NULL,
            CorrelativoPrestacion INT NULL,
            CantidadPrestaciones TINYINT NULL,
            DiasEstanciaFacturable INT NULL,

            GastoHonorariosProcedimientos DECIMAL(18,2) NULL,
            GastoOdontologia DECIMAL(18,2) NULL,
            GastoHoteleriaServicioClinicoTopico DECIMAL(18,2) NULL,
            GastoLaboratorio DECIMAL(18,2) NULL,
            GastoImagenes DECIMAL(18,2) NULL,
            GastoFarmaciaInsumos DECIMAL(18,2) NULL,
            GastoProtesis DECIMAL(18,2) NULL,
            GastoExoneradoIGV DECIMAL(18,2) NULL,
            OtrosGastos DECIMAL(18,2) NULL,
            CopagoFijoAfectoSinIGV DECIMAL(18,2) NULL,
            CopagoFijoExonerado DECIMAL(18,2) NULL,
            CopagoVariableAfectoSinIGV DECIMAL(18,2) NULL,
            CopagoVariableExonerado DECIMAL(18,2) NULL,
            TotalGastosCubiertosSinIGV DECIMAL(18,2) NULL,
            TotalLiquidadoIAFAS DECIMAL(18,2) NULL,

            FOREIGN KEY (FechaPrestacionKey)
                REFERENCES dbo.DimFecha(FechaKey),

            FOREIGN KEY (FechaIngresoKey)
                REFERENCES dbo.DimFecha(FechaKey),

            FOREIGN KEY (FechaEgresoKey)
                REFERENCES dbo.DimFecha(FechaKey),

            FOREIGN KEY (FechaRecepcionKey)
                REFERENCES dbo.DimFecha(FechaKey),

            FOREIGN KEY (IafasKey)
                REFERENCES dbo.DimIAFAS(IafasKey),

            FOREIGN KEY (IpressKey)
                REFERENCES dbo.DimIPRESS(IpressKey),

            FOREIGN KEY (PacienteKey)
                REFERENCES dbo.DimPaciente(PacienteKey),

            FOREIGN KEY (AfiliacionKey)
                REFERENCES dbo.DimAfiliacion(AfiliacionKey),

            FOREIGN KEY (CoberturaKey)
                REFERENCES dbo.DimCobertura(CoberturaKey),

            FOREIGN KEY (DiagnosticoKey)
                REFERENCES dbo.DimDiagnostico(DiagnosticoKey),

            FOREIGN KEY (TipoProfesionalKey)
                REFERENCES dbo.DimTipoProfesional(TipoProfesionalKey),

            FOREIGN KEY (HospitalizacionKey)
                REFERENCES dbo.DimHospitalizacion(HospitalizacionKey),

            FOREIGN KEY (UbicacionIpressKey)
                REFERENCES dbo.DimUbicacion(UbicacionKey),

            FOREIGN KEY (UbicacionAfiliadoKey)
                REFERENCES dbo.DimUbicacion(UbicacionKey)
        );
    END;
    """

    try:
        cursor.execute(script)
        conn.commit()

        print("Tablas del datamart disponibles")

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        
        
carpeta = Path(__file__).resolve().parent.parent

ruta_datos = carpeta / "datos" / "BD_pagos.xlsx"

ruta_ubigeos = (
    carpeta / "datos" / "auxiliares" / "TB_UBIGEOS.csv"
)

ruta_diagnosticos = (
    carpeta / "datos" / "auxiliares" / "CIE10_MINSA_OFICIAL.xlsx"
)

for ruta_archivo in [
    ruta_datos,
    ruta_ubigeos,
    ruta_diagnosticos
]:
    if not ruta_archivo.is_file():
        raise FileNotFoundError(
            f"Falta el archivo requerido: {ruta_archivo}"
        )
        
crear_base_datos()

dest_conn = get_connection_destino()

crear_tablas_datamart(dest_conn)

# Comprobar todas las tablas antes de iniciar una carga inicial
cursor_revision = dest_conn.cursor()

try:
    tablas_con_datos = []

    for tabla in [
        "DimFecha", "DimIAFAS", "DimIPRESS", "DimPaciente",
        "DimAfiliacion", "DimCobertura", "DimDiagnostico",
        "DimTipoProfesional", "DimHospitalizacion", "DimUbicacion",
        "FactPrestacionSalud"
    ]:
        cursor_revision.execute(f"SELECT COUNT_BIG(*) FROM dbo.[{tabla}]")
        if cursor_revision.fetchone()[0] > 0:
            tablas_con_datos.append(tabla)

    if tablas_con_datos:
        raise ValueError(
            "Esta es una carga inicial y ya hay registros en: "
            + ", ".join(tablas_con_datos)
            + ". No se borró ni se recargó ninguna tabla."
        )

except Exception:
    dest_conn.rollback()
    cursor_revision.close()
    dest_conn.close()
    raise

else:
    cursor_revision.close()

# ==========================
# %% LEER LA FUENTE DE DATOS
# ==========================

df_origen = pd.read_excel(
    ruta_datos,
    dtype=str
)

# ==========================
# %% RENOMBRAR COLUMNAS
# ==========================

nombres_columnas = {
    "VCODIAFAS_FAC": "CodigoIafasAnonimizado",
    "VCODIPRESS_FAC": "CodigoIpressAnonimizado",
    "VTDOCPAGO_FAC": "TipoDocumentoPago",
    "VNDOCPAGO_FAC": "DocumentoPagoAnonimizado",
    "VCORRPRESTA_ATE": "CorrelativoPrestacion",
    "VTAFILPAC_ATE": "CodigoTipoAfiliacion",
    "VTDOCIDEN_ATE": "TipoDocumentoIdentidad",
    "VNUMDOCIDEN_ATE": "PacienteAnonimizado",
    "VTIPOCOBERT_ATE": "CodigoTipoCobertura",
    "VSUBTIPCOBERT_ATE": "CodigoSubtipoCobertura",
    "VPRIDIAGCIE_ATE": "CodigoDiagnosticoCIE10",
    "VFECPRES_ATE": "FechaPrestacion",
    "VTITPRORESPRES_ATE": "CodigoTipoProfesional",
    "VTIPOHOSPI_ATE": "CodigoTipoHospitalizacion",
    "VFECINGRHOSP_ATE": "FechaIngresoHospitalario",
    "VFECEGRHOSP_ATE": "FechaEgresoHospitalario",
    "VTIPEGREHOSP_ATE": "CodigoTipoEgreso",
    "VDIASESTFAC_ATE": "DiasEstanciaFacturable",
    "VFECNACPAC_ATE": "FechaNacimiento",
    "VSEXOPAC_ATE": "CodigoSexo",
    "VFILIAPAC_ATE": "CodigoFiliacionPaciente",
    "VUBIGEOIPRESS_ATE": "UbigeoIPRESS",
    "DFECRECEP_PQ": "FechaRecepcion",
    "UBIGEO_AFILIADO": "UbigeoAfiliado"
}

columnas_faltantes = [
    columna
    for columna in nombres_columnas
    if columna not in df_origen.columns
]

if columnas_faltantes:
    raise ValueError(
        f"Faltan columnas en el archivo: {columnas_faltantes}"
    )

df = df_origen.rename(columns=nombres_columnas).copy()

# para los campos monetarios
nombres_montos = {
    "VGASTHONPROSIGV_ATE": "GastoHonorariosProcedimientos",
    "VGASTPRODOSIGV_ATE": "GastoOdontologia",
    "VGASTHTSCLITOPSIGV_ATE": "GastoHoteleriaServicioClinicoTopico",
    "VGASTEXAUXLABSIGV_ATE": "GastoLaboratorio",
    "VGASTEXAUXIMGSIGV_ATE": "GastoImagenes",
    "VGASTFARINSSIGV_ATE": "GastoFarmaciaInsumos",
    "VGASTPROTSIGV_ATE": "GastoProtesis",
    "VGASTMEDEXOIGV_ATE": "GastoExoneradoIGV",
    "VOGPRESSLDSIGV_ATE": "OtrosGastos",
    "VCOPAGOFIJOSIGV_ATE": "CopagoFijoAfectoSinIGV",
    "VCPAGOFIJOEXIGV_ATE": "CopagoFijoExonerado",
    "VCOPAGOVARSIGV_ATE": "CopagoVariableAfectoSinIGV",
    "VCPAGOVAREXIGV_ATE": "CopagoVariableExonerado",
    "VTOTGASTCUBSIGV_ATE": "TotalGastosCubiertosSinIGV",
    "VTOTLIQIAFAS_ATE": "TotalLiquidadoIAFAS"
}

columnas_faltantes = [
    columna
    for columna in nombres_montos
    if columna not in df.columns
]

if columnas_faltantes:
    raise ValueError(
        f"Faltan campos monetarios: {columnas_faltantes}"
    )

df = df.rename(columns=nombres_montos)

columnas_montos = list(nombres_montos.values())

# ==========================
# %% CONVERTIR CAMPOS AL TIPO DE DATO ADECUADO
# ==========================

# valores monetarios
def convertir_monto(valor):
    if pd.isna(valor):
        return None

    try:
        monto = Decimal(str(valor).strip())

        if monto.is_finite():
            return monto

        return None

    except InvalidOperation:
        return None


for columna in columnas_montos:
    valores_originales = (
        df[columna]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    valores_convertidos = valores_originales.map(convertir_monto)

    valores_invalidos = (
        valores_originales.notna()
        & valores_convertidos.isna()
    )

    if valores_invalidos.any():
        ejemplos = (
            valores_originales[valores_invalidos]
            .drop_duplicates()
            .head(5)
            .tolist()
        )

        raise ValueError(
            f"Hay montos con formato inválido en {columna}: {ejemplos}"
        )

    df[columna] = valores_convertidos

# fechas
columnas_fechas = [
    "FechaPrestacion",
    "FechaNacimiento",
    "FechaIngresoHospitalario",
    "FechaEgresoHospitalario"
]

resumen_fechas = []

for columna in columnas_fechas:
    valores_originales = (
        df[columna]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    fechas_convertidas = pd.to_datetime(
        valores_originales,
        format="%Y%m%d",
        errors="coerce"
    )

    valores_invalidos = (
        valores_originales.notna()
        & fechas_convertidas.isna()
    )

    resumen_fechas.append({
        "Campo": columna,
        "Vacias": int(valores_originales.isna().sum()),
        "Invalidas": int(valores_invalidos.sum())
    })

    if valores_invalidos.any():
        print(f"\nEjemplos de fechas inválidas en {columna}:")
        print(
            valores_originales[valores_invalidos]
            .drop_duplicates()
            .head(5)
            .tolist()
        )

        raise ValueError(
            f"Hay fechas con formato inválido en {columna}. "
            "Revisar los ejemplos antes de cargar."
        )

    df[columna] = fechas_convertidas

# fechas con hora
recepcion_original = (
    df["FechaRecepcion"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
)

recepcion_convertida = pd.to_datetime(
    recepcion_original,
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
)

recepcion_invalida = (
    recepcion_original.notna()
    & recepcion_convertida.isna()
)

if recepcion_invalida.any():
    ejemplos = (
        recepcion_original[recepcion_invalida]
        .drop_duplicates()
        .head(5)
        .tolist()
    )

    raise ValueError(
        f"Hay fechas de recepción con formato inválido: {ejemplos}"
    )

df["FechaRecepcion"] = recepcion_convertida

if df.empty:
    raise ValueError("La fuente no contiene prestaciones.")

if df[["FechaPrestacion", "FechaNacimiento", "FechaRecepcion"]].isna().any().any():
    raise ValueError("Faltan fechas obligatorias de prestación, nacimiento o recepción.")

prestacion_posterior_recepcion = (
    df["FechaPrestacion"].dt.normalize()
    > df["FechaRecepcion"].dt.normalize()
)

if prestacion_posterior_recepcion.any():
    raise ValueError(
        "Hay prestaciones posteriores a su fecha de recepción. Revisar la fuente."
    )

# ==========================
# %% LIMPIAR CÓDIGOS E IDENTIFICADORES
# ==========================

columnas_codigos = [
    "CodigoIafasAnonimizado",
    "CodigoIpressAnonimizado",
    "TipoDocumentoPago",
    "DocumentoPagoAnonimizado",
    "TipoDocumentoIdentidad",
    "PacienteAnonimizado",
    "CodigoTipoAfiliacion",
    "CodigoFiliacionPaciente",
    "CodigoTipoCobertura",
    "CodigoSubtipoCobertura",
    "CodigoDiagnosticoCIE10",
    "CodigoTipoProfesional",
    "CodigoTipoHospitalizacion",
    "CodigoTipoEgreso",
    "UbigeoIPRESS",
    "UbigeoAfiliado"
]

for columna in columnas_codigos:
    df[columna] = (
        df[columna]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

# Normalizar los ubigeos de la fuente sin convertirlos a números
for columna in ["UbigeoIPRESS", "UbigeoAfiliado"]:
    formato_invalido = (
        df[columna].notna()
        & ~df[columna].str.fullmatch(r"[0-9]{1,6}", na=False)
    )

    if formato_invalido.any():
        ejemplos = df.loc[formato_invalido, columna].drop_duplicates().head(10).tolist()
        raise ValueError(f"Ubigeos con formato inválido en {columna}: {ejemplos}")

    df[columna] = df[columna].str.zfill(6)

# Verificar campos obligatorios antes de preparar las dimensiones
columnas_obligatorias = [
    "CodigoIafasAnonimizado", "CodigoIpressAnonimizado",
    "TipoDocumentoPago", "DocumentoPagoAnonimizado",
    "TipoDocumentoIdentidad", "PacienteAnonimizado",
    "CodigoTipoAfiliacion", "CodigoFiliacionPaciente",
    "CodigoTipoCobertura", "CodigoSubtipoCobertura",
    "CodigoDiagnosticoCIE10", "CodigoSexo", "UbigeoIPRESS"
]

faltantes_obligatorios = df[columnas_obligatorias].isna().sum()

if faltantes_obligatorios.gt(0).any():
    raise ValueError(
        "Hay campos obligatorios vacíos:\n"
        + faltantes_obligatorios[faltantes_obligatorios.gt(0)].to_string()
    )

# Comprobar la coherencia de los datos hospitalarios
es_hospitalizacion_fuente = df["CodigoTipoHospitalizacion"].isin(["C", "Q"])
tipo_hospitalizacion_invalido = (
    df["CodigoTipoHospitalizacion"].notna()
    & ~df["CodigoTipoHospitalizacion"].isin(["C", "Q", "N"])
)

if tipo_hospitalizacion_invalido.any():
    raise ValueError("Hay tipos de hospitalización no contemplados en el catálogo.")

datos_hospitalarios = [
    "FechaIngresoHospitalario", "FechaEgresoHospitalario", "CodigoTipoEgreso"
]

if df.loc[es_hospitalizacion_fuente, datos_hospitalarios].isna().any().any():
    raise ValueError("Hay hospitalizaciones con fechas o tipo de egreso ausentes.")

if df.loc[~es_hospitalizacion_fuente, datos_hospitalarios].notna().any().any():
    raise ValueError("Hay datos hospitalarios en prestaciones sin hospitalización.")

egreso_anterior_ingreso = (
    df["FechaIngresoHospitalario"].notna()
    & df["FechaEgresoHospitalario"].notna()
    & (df["FechaEgresoHospitalario"] < df["FechaIngresoHospitalario"])
)

if egreso_anterior_ingreso.any():
    raise ValueError("Hay fechas de egreso anteriores al ingreso hospitalario.")

# ==========================
# %% PREPARAR DATOS DE DIAGNÓSTICOS
# ==========================

catalogo_original = pd.read_excel(
    ruta_diagnosticos,
    sheet_name="VOLUMEN VIGENTE",
    header=None,
    dtype="string",
    usecols=[0]
)

texto_diagnosticos = (
    catalogo_original.iloc[:, 0]
    .str.strip()
)

catalogo_diagnosticos = texto_diagnosticos.str.extract(
    r"^([A-Z][0-9]{2}(?:\.?[0-9A-Z]{1,4})?)\s*[-–—]\s*(.+)$"
)

catalogo_diagnosticos.columns = [
    "CodigoDiagnosticoCatalogo",
    "DescripcionDiagnostico"
]

catalogo_diagnosticos = (
    catalogo_diagnosticos
    .dropna(subset=[
        "CodigoDiagnosticoCatalogo",
        "DescripcionDiagnostico"
    ])
    .drop_duplicates()
    .reset_index(drop=True)
)

if catalogo_diagnosticos["CodigoDiagnosticoCatalogo"].duplicated().any():
    raise ValueError(
        "El catálogo contiene códigos con varias descripciones."
    )

# Conservar los códigos originales utilizados en las prestaciones
df_diagnostico = (
    df[["CodigoDiagnosticoCIE10"]]
    .drop_duplicates()
    .sort_values("CodigoDiagnosticoCIE10")
    .reset_index(drop=True)
)

catalogo_busqueda = catalogo_diagnosticos.copy()

# Preparar un código auxiliar para comparar ambos archivos
# Se ignoran diferencias de mayúsculas y puntos
df_diagnostico["CodigoBusqueda"] = (
    df_diagnostico["CodigoDiagnosticoCIE10"]
    .str.strip()
    .str.upper()
    .str.replace(".", "", regex=False)
)

catalogo_busqueda["CodigoBusqueda"] = (
    catalogo_busqueda["CodigoDiagnosticoCatalogo"]
    .str.strip()
    .str.upper()
    .str.replace(".", "", regex=False)
)

# Verificar que cada código de búsqueda tenga una sola descripción
catalogo_busqueda = (
    catalogo_busqueda[
        ["CodigoBusqueda", "DescripcionDiagnostico"]
    ]
    .drop_duplicates()
)

if catalogo_busqueda["CodigoBusqueda"].duplicated().any():
    raise ValueError(
        "Un código de diagnóstico tiene varias descripciones "
        "en el catálogo. Revisar antes de continuar."
    )

# ==========================
# %% PREPARAR DATOS DE UBICACION
# ==========================

df_ubigeos = pd.read_csv(
    ruta_ubigeos,
    sep=";",
    encoding="utf-8-sig",
    dtype="string",
    usecols=[
        "ubigeo_reniec",
        "ubigeo_inei",
        "departamento",
        "provincia",
        "distrito"
    ]
)

for columna in df_ubigeos.columns:
    df_ubigeos[columna] = (
        df_ubigeos[columna]
        .str.strip()
        .replace("", pd.NA)
    )

for columna in ["ubigeo_reniec", "ubigeo_inei"]:
    df_ubigeos[columna] = (
        df_ubigeos[columna].str.zfill(6)
    )

# completar y clasificar equivalencias

# Incorporar la equivalencia verificada de Alto Trujillo
if not df_ubigeos["ubigeo_reniec"].eq("120113").any():
    alto_trujillo = pd.DataFrame({
        "ubigeo_reniec": ["120113"],
        "ubigeo_inei": ["130112"],
        "departamento": ["LA LIBERTAD"],
        "provincia": ["TRUJILLO"],
        "distrito": ["ALTO TRUJILLO"]
    }).astype("string")

    df_ubigeos = pd.concat(
        [df_ubigeos, alto_trujillo],
        ignore_index=True
    )

equivalencias_reniec = (
    df_ubigeos[["ubigeo_reniec", "ubigeo_inei"]]
    .dropna(subset=["ubigeo_reniec"])
    .drop_duplicates()
)

if equivalencias_reniec["ubigeo_reniec"].duplicated().any():
    raise ValueError("Hay códigos RENIEC con varias equivalencias.")

reniec_a_inei = equivalencias_reniec.set_index(
    "ubigeo_reniec"
)["ubigeo_inei"]

df["UbigeoAfiliadoINEI"] = (
    df["UbigeoAfiliado"]
    .map(reniec_a_inei)
    .astype("string")
)

df["EstadoUbigeoAfiliado"] = "Con equivalencia INEI"

df.loc[
    df["UbigeoAfiliado"].isna(),
    "EstadoUbigeoAfiliado"
] = "Sin dato"

sin_equivalencia = (
    df["UbigeoAfiliado"].notna()
    & df["UbigeoAfiliadoINEI"].isna()
)

df.loc[
    sin_equivalencia,
    "EstadoUbigeoAfiliado"
] = "Sin equivalencia en catálogo"

pendientes_ubigeo = (
    df.loc[sin_equivalencia, "UbigeoAfiliado"]
    .value_counts()
    .rename_axis("CodigoRENIEC")
    .reset_index(name="CantidadPrestaciones")
)

# validar ubicaciones de ipress

codigos_inei_catalogo = (
    df_ubigeos["ubigeo_inei"]
    .dropna()
    .unique()
)

ipress_sin_correspondencia = (
    df["UbigeoIPRESS"].notna()
    & ~df["UbigeoIPRESS"].isin(codigos_inei_catalogo)
)


if ipress_sin_correspondencia.any():
    ejemplos = (
        df.loc[ipress_sin_correspondencia, "UbigeoIPRESS"]
        .drop_duplicates().head(10).tolist()
    )
    raise ValueError(f"Ubigeos de IPRESS sin correspondencia: {ejemplos}")

# preparar dim ubicacion

ubigeos_utilizados = pd.concat(
    [
        df["UbigeoIPRESS"],
        df["UbigeoAfiliadoINEI"]
    ],
    ignore_index=True
).dropna().unique()

df_ubicacion = (
    df_ubigeos[[
        "ubigeo_inei",
        "departamento",
        "provincia",
        "distrito"
    ]]
    .rename(columns={
        "ubigeo_inei": "Ubigeo",
        "departamento": "Departamento",
        "provincia": "Provincia",
        "distrito": "Distrito"
    })
    .dropna(subset=["Ubigeo"])
    .drop_duplicates()
)

if df_ubicacion["Ubigeo"].duplicated().any():
    raise ValueError(
        "Un código INEI tiene varias descripciones en el catálogo."
    )

df_ubicacion = (
    df_ubicacion[
        df_ubicacion["Ubigeo"].isin(ubigeos_utilizados)
    ]
    .sort_values("Ubigeo")
    .reset_index(drop=True)
)

ubicacion_desconocida = pd.DataFrame({
    "Ubigeo": [None],
    "Departamento": ["Desconocido"],
    "Provincia": ["Desconocido"],
    "Distrito": ["Desconocido"]
})

df_ubicacion = pd.concat(
    [ubicacion_desconocida, df_ubicacion],
    ignore_index=True
)

print("\nEstado de ubicación del afiliado:")
print(df["EstadoUbigeoAfiliado"].value_counts())

print(
    "\nPrestaciones con ubicación de IPRESS sin correspondencia:",
    int(ipress_sin_correspondencia.sum())
)

print(
    "\nRegistros preparados para DimUbicacion:",
    len(df_ubicacion)
)

# ==========================
# %% PREPARAR DIMENSIONES
# ==========================

# DimIAFAS

df_iafas = (
    df[["CodigoIafasAnonimizado"]]
    .drop_duplicates()
    .sort_values("CodigoIafasAnonimizado")
    .reset_index(drop=True)
)

# DimIPRESS

df_ipress = (
    df[["CodigoIpressAnonimizado"]]
    .drop_duplicates()
    .sort_values("CodigoIpressAnonimizado")
    .reset_index(drop=True)
)

# DimPaciente

columnas_paciente = [
    "TipoDocumentoIdentidad",
    "PacienteAnonimizado",
    "FechaNacimiento",
    "CodigoSexo"
]

if df[columnas_paciente].isna().any().any():
    raise ValueError(
        "Hay datos faltantes en los campos obligatorios de DimPaciente."
    )

df_paciente = (
    df[columnas_paciente]
    .drop_duplicates()
    .sort_values(columnas_paciente)
    .reset_index(drop=True)
)

cantidad_identificadores = (
    df_paciente[[
        "TipoDocumentoIdentidad",
        "PacienteAnonimizado"
    ]]
    .drop_duplicates()
    .shape[0]
)

# DimAfiliacion

columnas_afiliacion = [
    "CodigoTipoAfiliacion",
    "CodigoFiliacionPaciente"
]

df_afiliacion = (
    df[columnas_afiliacion]
    .drop_duplicates()
    .sort_values(columnas_afiliacion)
    .reset_index(drop=True)
)

# DimCobertura

columnas_cobertura = [
    "CodigoTipoCobertura",
    "CodigoSubtipoCobertura"
]

df_cobertura = (
    df[columnas_cobertura]
    .drop_duplicates()
    .sort_values(columnas_cobertura)
    .reset_index(drop=True)
)

# DimTipoProfesional

df_tipo_profesional = (
    df[["CodigoTipoProfesional"]]
    .drop_duplicates()
    .sort_values("CodigoTipoProfesional")
    .reset_index(drop=True)
)

# DimHospitalizacion

columnas_hospitalizacion = [
    "CodigoTipoHospitalizacion",
    "CodigoTipoEgreso"
]

df_hospitalizacion = (
    df[columnas_hospitalizacion]
    .drop_duplicates()
    .sort_values(
        columnas_hospitalizacion,
        na_position="first"
    )
    .reset_index(drop=True)
)

# Revisar y conservar incidencias de fechas hospitalarias

recepcion_dia = df["FechaRecepcion"].dt.normalize()

df["IngresoPosteriorRecepcion"] = (
    df["FechaIngresoHospitalario"].notna()
    & recepcion_dia.notna()
    & (
        df["FechaIngresoHospitalario"].dt.normalize()
        > recepcion_dia
    )
)

df["EgresoPosteriorRecepcion"] = (
    df["FechaEgresoHospitalario"].notna()
    & recepcion_dia.notna()
    & (
        df["FechaEgresoHospitalario"].dt.normalize()
        > recepcion_dia
    )
)

df["FechaIngresoAnalisis"] = (
    df["FechaIngresoHospitalario"]
    .mask(df["IngresoPosteriorRecepcion"])
)

df["FechaEgresoAnalisis"] = (
    df["FechaEgresoHospitalario"]
    .mask(df["EgresoPosteriorRecepcion"])
)

columnas_incidencias = [
    "DocumentoPagoAnonimizado",
    "CorrelativoPrestacion",
    "CodigoIafasAnonimizado",
    "CodigoIpressAnonimizado",
    "FechaPrestacion",
    "FechaIngresoHospitalario",
    "FechaEgresoHospitalario",
    "FechaRecepcion",
    "IngresoPosteriorRecepcion",
    "EgresoPosteriorRecepcion"
]

if "Source.Name" in df.columns:
    columnas_incidencias = ["Source.Name"] + columnas_incidencias

incidencias_fechas_hospitalarias = df.loc[
    df["IngresoPosteriorRecepcion"]
    | df["EgresoPosteriorRecepcion"],
    columnas_incidencias
].copy()

print(
    "\nPrestaciones con fechas hospitalarias pendientes de validación:",
    len(incidencias_fechas_hospitalarias)
)


# DimFecha

columnas_fecha_dimension = [
    "FechaPrestacion",
    "FechaIngresoAnalisis",
    "FechaEgresoAnalisis",
    "FechaRecepcion"
]

fechas_validas = pd.concat(
    [
        df[columna].dt.normalize()
        for columna in columnas_fecha_dimension
    ],
    ignore_index=True
).dropna()

if fechas_validas.empty:
    raise ValueError(
        "No hay fechas válidas para preparar DimFecha."
    )

calendario = pd.date_range(
    start=fechas_validas.min(),
    end=fechas_validas.max(),
    freq="D"
)

df_fecha = pd.DataFrame({
    "Fecha": calendario
})

meses = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

dias_semana = {
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado",
    7: "Domingo"
}

df_fecha["FechaKey"] = (
    df_fecha["Fecha"].dt.strftime("%Y%m%d").astype(int)
)

df_fecha["Anio"] = df_fecha["Fecha"].dt.year
df_fecha["Trimestre"] = df_fecha["Fecha"].dt.quarter
df_fecha["Mes"] = df_fecha["Fecha"].dt.month
df_fecha["NombreMes"] = df_fecha["Mes"].map(meses)
df_fecha["Dia"] = df_fecha["Fecha"].dt.day
df_fecha["DiaSemana"] = df_fecha["Fecha"].dt.dayofweek + 1

df_fecha["NombreDiaSemana"] = (
    df_fecha["DiaSemana"].map(dias_semana)
)

df_fecha["TipoRegistroFecha"] = "Fecha válida"

fechas_especiales = pd.DataFrame([
    {
        "FechaKey": -1,
        "Fecha": pd.NaT,
        "TipoRegistroFecha": "No aplica"
    },
    {
        "FechaKey": 0,
        "Fecha": pd.NaT,
        "TipoRegistroFecha": "Desconocido"
    }
]).reindex(columns=df_fecha.columns)

df_fecha = pd.concat(
    [fechas_especiales, df_fecha],
    ignore_index=True
)

columnas_enteras_fecha = [
    "FechaKey",
    "Anio",
    "Trimestre",
    "Mes",
    "Dia",
    "DiaSemana"
]

for columna in columnas_enteras_fecha:
    df_fecha[columna] = df_fecha[columna].astype("Int64")
    
# dim diagnostico

df_diagnostico = df_diagnostico.merge(
    catalogo_busqueda,
    on="CodigoBusqueda",
    how="left",
    validate="many_to_one"
)

df_diagnostico = df_diagnostico.drop(
    columns="CodigoBusqueda"
)

# Identificar diagnósticos sin descripción
diagnosticos_sin_descripcion = df_diagnostico.loc[
    df_diagnostico["DescripcionDiagnostico"].isna(),
    "CodigoDiagnosticoCIE10"
]

pendientes_diagnostico = (
    df.loc[
        df["CodigoDiagnosticoCIE10"].isin(
            diagnosticos_sin_descripcion
        ),
        "CodigoDiagnosticoCIE10"
    ]
    .value_counts()
    .rename_axis("CodigoDiagnosticoCIE10")
    .reset_index(name="CantidadPrestaciones")
)

# ==========================
# %% PREPARAR CAMPOS ENTEROS DE LA TABLA DE HECHOS
# ==========================

columnas_enteras = [
    "CorrelativoPrestacion",
    "DiasEstanciaFacturable"
]

for columna in columnas_enteras:

    valores_originales = (
        df[columna]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    valores_numericos = pd.to_numeric(
        valores_originales,
        errors="coerce"
    )

    # Validar números enteros no negativos dentro del rango de INT
    valores_invalidos = (
        valores_originales.notna()
        & (
            valores_numericos.isna()
            | (valores_numericos < 0)
            | (valores_numericos > 2147483647)
            | (valores_numericos % 1 != 0)
        )
    )

    if valores_invalidos.any():
        ejemplos = (
            valores_originales[valores_invalidos]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            f"El campo {columna} contiene valores inválidos: "
            f"{ejemplos}"
        )

    df[columna] = valores_numericos.astype("Int64")

# validar precision de montos

limite_monto = Decimal("9999999999999999.99")
dos_decimales = Decimal("0.01")


def monto_valido_sql(monto):

    if pd.isna(monto):
        return True

    if not monto.is_finite():
        return False

    if abs(monto) > limite_monto:
        return False

    return monto == monto.quantize(dos_decimales)


for columna in columnas_montos:

    montos_invalidos = ~df[columna].map(monto_valido_sql)

    if montos_invalidos.any():
        ejemplos = (
            df.loc[montos_invalidos, columna]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            f"El campo {columna} contiene montos que no "
            f"pueden almacenarse exactamente en DECIMAL(18,2): "
            f"{ejemplos}"
        )

# ==========================
# %% VALIDAR IDENTIFICACIÓN DE LAS PRESTACIONES
# ==========================

columnas_identificacion = [
    "CodigoIafasAnonimizado",
    "CodigoIpressAnonimizado",
    "TipoDocumentoPago",
    "DocumentoPagoAnonimizado",
    "CorrelativoPrestacion"
]

if df[columnas_identificacion].isna().any().any():
    raise ValueError("Hay campos vacíos en la identificación de las prestaciones.")

identificacion_repetida = df.duplicated(
    subset=columnas_identificacion,
    keep=False
)

if identificacion_repetida.any():
    ejemplos = df.loc[identificacion_repetida, columnas_identificacion].head(10)
    raise ValueError(
        "Hay prestaciones con identificación repetida. No se eliminaron registros:\n"
        + ejemplos.to_string(index=False)
    )

print("\nIdentificación completa y sin repeticiones:", len(df))


def validar_montos_cargados(conexion, datos):
    expresiones_sql = []

    for columna in columnas_montos:
        expresiones_sql.extend([
            f"SUM([{columna}])",
            f"COUNT_BIG([{columna}])"
        ])

    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT " + ", ".join(expresiones_sql)
            + " FROM dbo.FactPrestacionSalud"
        )
        resultados_sql = cursor.fetchone()
    finally:
        cursor.close()

    comparacion = []

    for posicion, columna in enumerate(columnas_montos):
        valores = datos[columna].dropna()
        total_python = sum(valores, Decimal("0")) if len(valores) else None
        total_sql = resultados_sql[posicion * 2]
        cantidad_sql = resultados_sql[posicion * 2 + 1]

        comparacion.append({
            "Campo": columna,
            "TotalPython": total_python,
            "TotalSQL": total_sql,
            "InformadosPython": len(valores),
            "InformadosSQL": cantidad_sql,
            "Coincide": total_python == total_sql and len(valores) == cantidad_sql
        })

    validacion = pd.DataFrame(comparacion)
    print("\nComparación monetaria:")
    print(validacion.to_string(index=False))

    if not validacion["Coincide"].all():
        raise ValueError("Los montos o la cantidad de valores informados no coinciden.")

    return validacion

# ==========================
# %% CARGAR DIMENSIONES EN SQL SERVER
# ==========================

def cargar_dimension(conexion, tabla, datos, columnas):

    cursor = conexion.cursor()

    try:
        # Comprobar que la dimensión esté vacía
        cursor.execute(
            f"SELECT COUNT(*) FROM dbo.[{tabla}]"
        )

        cantidad_actual = cursor.fetchone()[0]

        if cantidad_actual > 0:
            raise ValueError(
                f"La tabla {tabla} ya contiene "
                f"{cantidad_actual} registros. "
                "No se realizará una nueva carga."
            )

        campos_sql = ", ".join(
            f"[{columna}]" for columna in columnas
        )

        parametros = ", ".join(
            "?" for columna in columnas
        )

        consulta = (
            f"INSERT INTO dbo.[{tabla}] ({campos_sql}) "
            f"VALUES ({parametros})"
        )

        cursor.fast_executemany = True

        # Insertar en lotes para no enviar todas las filas juntas
        for inicio in range(0, len(datos), 5000):

            lote = (
                datos.iloc[inicio:inicio + 5000][columnas]
                .astype(object)
            )

            # Convertir los valores faltantes a NULL de SQL
            lote = lote.where(pd.notna(lote), None)

            registros = [
                tuple(
                    valor.to_pydatetime()
                    if isinstance(valor, pd.Timestamp)
                    else valor
                    for valor in fila
                )
                for fila in lote.itertuples(
                    index=False,
                    name=None
                )
            ]

            cursor.executemany(consulta, registros)

        print(
            f"{tabla}: {len(datos)} registros insertados "
            "(pendientes de confirmar)."
        )

    finally:
        cursor.close()


dimensiones_carga = [
    (
        "DimFecha",
        df_fecha,
        [
            "FechaKey",
            "Fecha",
            "Anio",
            "Trimestre",
            "Mes",
            "NombreMes",
            "Dia",
            "DiaSemana",
            "NombreDiaSemana",
            "TipoRegistroFecha"
        ]
    ),
    (
        "DimIAFAS",
        df_iafas,
        ["CodigoIafasAnonimizado"]
    ),
    (
        "DimIPRESS",
        df_ipress,
        ["CodigoIpressAnonimizado"]
    ),
    (
        "DimPaciente",
        df_paciente,
        [
            "TipoDocumentoIdentidad",
            "PacienteAnonimizado",
            "FechaNacimiento",
            "CodigoSexo"
        ]
    ),
    (
        "DimAfiliacion",
        df_afiliacion,
        [
            "CodigoTipoAfiliacion",
            "CodigoFiliacionPaciente"
        ]
    ),
    (
        "DimCobertura",
        df_cobertura,
        [
            "CodigoTipoCobertura",
            "CodigoSubtipoCobertura"
        ]
    ),
    (
        "DimDiagnostico",
        df_diagnostico,
        [
            "CodigoDiagnosticoCIE10",
            "DescripcionDiagnostico"
        ]
    ),
    (
        "DimTipoProfesional",
        df_tipo_profesional,
        ["CodigoTipoProfesional"]
    ),
    (
        "DimHospitalizacion",
        df_hospitalizacion,
        [
            "CodigoTipoHospitalizacion",
            "CodigoTipoEgreso"
        ]
    ),
    (
        "DimUbicacion",
        df_ubicacion,
        [
            "Ubigeo",
            "Departamento",
            "Provincia",
            "Distrito"
        ]
    )
]


# Validar los campos de texto según las longitudes del destino
limites_texto_dimensiones = {
    "CodigoIafasAnonimizado": 64,
    "CodigoIpressAnonimizado": 64,
    "TipoDocumentoIdentidad": 10,
    "PacienteAnonimizado": 64,
    "CodigoSexo": 10,
    "CodigoTipoAfiliacion": 10,
    "CodigoFiliacionPaciente": 10,
    "CodigoTipoCobertura": 10,
    "CodigoSubtipoCobertura": 10,
    "CodigoDiagnosticoCIE10": 10,
    "DescripcionDiagnostico": 500,
    "CodigoTipoProfesional": 10,
    "CodigoTipoHospitalizacion": 10,
    "CodigoTipoEgreso": 10,
    "Ubigeo": 6,
    "Departamento": 100,
    "Provincia": 100,
    "Distrito": 100
}

for tabla, datos, columnas in dimensiones_carga:
    for columna in columnas:
        if columna in limites_texto_dimensiones:
            limite = limites_texto_dimensiones[columna]
            excede = datos[columna].astype("string").str.len().gt(limite).fillna(False)
            if excede.any():
                raise ValueError(f"{tabla}.{columna} supera {limite} caracteres.")

try:
    for tabla, datos, columnas in dimensiones_carga:
        cargar_dimension(
            dest_conn,
            tabla,
            datos,
            columnas
        )

    dest_conn.commit()

    print("\nCarga de todas las dimensiones confirmada.")

except Exception:
    dest_conn.rollback()

    print(
        "\nLa carga no se completó. "
        "Se revirtieron las inserciones de este bloque."
    )

    raise
    
# ==========================
# %% RECUPERAR CLAVES DE LAS DIMENSIONES
# ==========================

def leer_dimension(conexion, tabla, columnas):

    cursor = conexion.cursor()

    try:
        campos_sql = ", ".join(
            f"[{columna}]" for columna in columnas
        )

        cursor.execute(
            f"SELECT {campos_sql} FROM dbo.[{tabla}]"
        )

        registros = [
            tuple(fila)
            for fila in cursor.fetchall()
        ]

        return pd.DataFrame.from_records(
            registros,
            columns=columnas
        )

    finally:
        cursor.close()


claves_dimensiones = {
    "DimFecha": "FechaKey",
    "DimIAFAS": "IafasKey",
    "DimIPRESS": "IpressKey",
    "DimPaciente": "PacienteKey",
    "DimAfiliacion": "AfiliacionKey",
    "DimCobertura": "CoberturaKey",
    "DimDiagnostico": "DiagnosticoKey",
    "DimTipoProfesional": "TipoProfesionalKey",
    "DimHospitalizacion": "HospitalizacionKey",
    "DimUbicacion": "UbicacionKey"
}

dimensiones_sql = {}

for tabla, datos, columnas in dimensiones_carga:

    clave = claves_dimensiones[tabla]

    # Incluir la clave una sola vez
    columnas_consulta = [clave] + [
        columna
        for columna in columnas
        if columna != clave
    ]

    dimension = leer_dimension(
        dest_conn,
        tabla,
        columnas_consulta
    )

    # Comprobar que se recuperaron todos los registros
    if len(dimension) != len(datos):
        raise ValueError(
            f"La cantidad de registros de {tabla} "
            "no coincide con la dimensión preparada."
        )

    if (
        dimension[clave].isna().any()
        or dimension[clave].duplicated().any()
    ):
        raise ValueError(
            f"La tabla {tabla} contiene claves "
            "vacías o repetidas."
        )

    dimensiones_sql[tabla] = dimension

    print(
        f"{tabla}: {len(dimension)} registros recuperados."
    )

print("\nEjemplo de claves de diagnóstico:")
print(
    dimensiones_sql["DimDiagnostico"]
    .head()
    .to_string(index=False)
)

# ==========================
# %% ASIGNAR CLAVES DIMENSIONALES A LAS PRESTACIONES
# ==========================

df_fact = df.copy().reset_index(drop=True)


def asignar_clave_dimension(
    datos,
    tabla,
    columnas_union,
    clave
):

    dimension = dimensiones_sql[tabla][
        columnas_union + [clave]
    ].copy()

    datos = datos.copy()

    # Mantener el mismo tipo de dato en los códigos
    for columna in columnas_union:
        datos[columna] = datos[columna].astype("string")
        dimension[columna] = dimension[columna].astype("string")

    cantidad_inicial = len(datos)

    resultado = datos.merge(
        dimension,
        on=columnas_union,
        how="left",
        validate="many_to_one"
    )

    if len(resultado) != cantidad_inicial:
        raise ValueError(
            f"La unión con {tabla} modificó "
            "la cantidad de prestaciones."
        )

    sin_clave = resultado[clave].isna()

    if sin_clave.any():
        ejemplos = (
            resultado.loc[sin_clave, columnas_union]
            .drop_duplicates()
            .head(10)
        )

        raise ValueError(
            f"Hay {int(sin_clave.sum())} prestaciones "
            f"sin correspondencia en {tabla}:\n"
            f"{ejemplos.to_string(index=False)}"
        )

    resultado[clave] = resultado[clave].astype("Int64")

    print(
        f"{clave}: asignada a las "
        f"{len(resultado)} prestaciones."
    )

    return resultado


dimensiones_por_asignar = [
    (
        "DimIAFAS",
        ["CodigoIafasAnonimizado"],
        "IafasKey"
    ),
    (
        "DimIPRESS",
        ["CodigoIpressAnonimizado"],
        "IpressKey"
    ),
    (
        "DimAfiliacion",
        [
            "CodigoTipoAfiliacion",
            "CodigoFiliacionPaciente"
        ],
        "AfiliacionKey"
    ),
    (
        "DimCobertura",
        [
            "CodigoTipoCobertura",
            "CodigoSubtipoCobertura"
        ],
        "CoberturaKey"
    ),
    (
        "DimDiagnostico",
        ["CodigoDiagnosticoCIE10"],
        "DiagnosticoKey"
    ),
    (
        "DimTipoProfesional",
        ["CodigoTipoProfesional"],
        "TipoProfesionalKey"
    ),
    (
        "DimHospitalizacion",
        [
            "CodigoTipoHospitalizacion",
            "CodigoTipoEgreso"
        ],
        "HospitalizacionKey"
    )
]


for tabla, columnas_union, clave in dimensiones_por_asignar:

    df_fact = asignar_clave_dimension(
        df_fact,
        tabla,
        columnas_union,
        clave
    )
    
# ==========================
# %% ASIGNAR CLAVE DE PACIENTE
# ==========================

columnas_paciente = [
    "TipoDocumentoIdentidad",
    "PacienteAnonimizado",
    "FechaNacimiento",
    "CodigoSexo"
]

pacientes_sql = dimensiones_sql["DimPaciente"][
    columnas_paciente + ["PacienteKey"]
].copy()

# Igualar el formato de los códigos en ambos DataFrames
for columna in [
    "TipoDocumentoIdentidad",
    "PacienteAnonimizado",
    "CodigoSexo"
]:
    df_fact[columna] = df_fact[columna].astype("string")
    pacientes_sql[columna] = pacientes_sql[columna].astype("string")

# Igualar el formato de la fecha de nacimiento
df_fact["FechaNacimiento"] = pd.to_datetime(
    df_fact["FechaNacimiento"],
    errors="raise"
).dt.normalize()

pacientes_sql["FechaNacimiento"] = pd.to_datetime(
    pacientes_sql["FechaNacimiento"],
    errors="raise"
).dt.normalize()

cantidad_inicial = len(df_fact)

# Buscar la clave utilizando el perfil completo
df_fact = df_fact.merge(
    pacientes_sql,
    on=columnas_paciente,
    how="left",
    validate="many_to_one"
)

if len(df_fact) != cantidad_inicial:
    raise ValueError(
        "La unión con DimPaciente modificó "
        "la cantidad de prestaciones."
    )

sin_clave_paciente = df_fact["PacienteKey"].isna()

if sin_clave_paciente.any():
    ejemplos = (
        df_fact.loc[sin_clave_paciente, columnas_paciente]
        .drop_duplicates()
        .head(10)
    )

    raise ValueError(
        f"Hay {int(sin_clave_paciente.sum())} prestaciones "
        "sin correspondencia en DimPaciente:\n"
        f"{ejemplos.to_string(index=False)}"
    )

df_fact["PacienteKey"] = df_fact["PacienteKey"].astype("Int64")

# ==========================
# %% ASIGNAR CLAVES DE UBICACIÓN
# ==========================

ubicaciones_sql = dimensiones_sql["DimUbicacion"][
    ["UbicacionKey", "Ubigeo"]
].copy()

ubicaciones_sql["Ubigeo"] = (
    ubicaciones_sql["Ubigeo"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
)

# Recuperar la clave de la ubicación desconocida
ubicacion_desconocida_sql = ubicaciones_sql.loc[
    ubicaciones_sql["Ubigeo"].isna(),
    "UbicacionKey"
]

if len(ubicacion_desconocida_sql) != 1:
    raise ValueError(
        "DimUbicacion debe contener exactamente "
        "un registro de ubicación desconocida."
    )

clave_ubicacion_desconocida = int(
    ubicacion_desconocida_sql.iloc[0]
)

# Preparar la búsqueda por código INEI
ubicaciones_con_codigo = ubicaciones_sql.dropna(
    subset=["Ubigeo"]
)

if ubicaciones_con_codigo["Ubigeo"].duplicated().any():
    raise ValueError(
        "Hay códigos INEI repetidos en DimUbicacion."
    )

mapa_ubicaciones = ubicaciones_con_codigo.set_index(
    "Ubigeo"
)["UbicacionKey"]

ubicaciones_por_asignar = [
    ("UbigeoIPRESS", "UbicacionIpressKey"),
    ("UbigeoAfiliadoINEI", "UbicacionAfiliadoKey")
]

for columna_ubigeo, columna_clave in ubicaciones_por_asignar:

    codigos = (
        df_fact[columna_ubigeo]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    claves = codigos.map(mapa_ubicaciones)

    # Los códigos INEI informados deben existir en la dimensión
    sin_correspondencia = codigos.notna() & claves.isna()

    if sin_correspondencia.any():
        ejemplos = (
            codigos[sin_correspondencia]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            f"Hay códigos de {columna_ubigeo} "
            f"sin correspondencia en DimUbicacion: {ejemplos}"
        )

    # Usar la ubicación desconocida cuando no hay código INEI
    df_fact[columna_clave] = (
        claves
        .fillna(clave_ubicacion_desconocida)
        .astype("Int64")
    )

# ==========================
# %% ASIGNAR CLAVES DE FECHA
# ==========================

fechas_sql = dimensiones_sql["DimFecha"][
    ["FechaKey", "Fecha"]
].copy()

fechas_sql["Fecha"] = pd.to_datetime(
    fechas_sql["Fecha"],
    errors="raise"
).dt.normalize()

# Comprobar que existen los registros especiales
claves_especiales = set(fechas_sql["FechaKey"])

if not {0, -1}.issubset(claves_especiales):
    raise ValueError(
        "DimFecha debe contener las claves "
        "0 (Desconocido) y -1 (No aplica)."
    )

fechas_con_valor = fechas_sql.dropna(subset=["Fecha"])

if fechas_con_valor["Fecha"].duplicated().any():
    raise ValueError(
        "Hay fechas repetidas en DimFecha."
    )

mapa_fechas = fechas_con_valor.set_index(
    "Fecha"
)["FechaKey"]

es_hospitalizacion = (
    df_fact["CodigoTipoHospitalizacion"].isin(["C", "Q"])
)

fechas_por_asignar = [
    ("FechaPrestacion", "FechaPrestacionKey", False),
    ("FechaIngresoAnalisis", "FechaIngresoKey", True),
    ("FechaEgresoAnalisis", "FechaEgresoKey", True),
    ("FechaRecepcion", "FechaRecepcionKey", False)
]

for columna_fecha, columna_clave, fecha_hospitalaria in fechas_por_asignar:

    fechas = pd.to_datetime(
        df_fact[columna_fecha],
        errors="raise"
    ).dt.normalize()

    claves = fechas.map(mapa_fechas)

    # Toda fecha informada debe existir en el calendario
    sin_correspondencia = fechas.notna() & claves.isna()

    if sin_correspondencia.any():
        ejemplos = (
            fechas[sin_correspondencia]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            f"Hay fechas de {columna_fecha} "
            f"que no existen en DimFecha: {ejemplos}"
        )

    # Fecha ausente o pendiente de validación: Desconocido
    claves = claves.fillna(0).astype("Int64")

    # Las fechas hospitalarias no aplican a otras prestaciones
    if fecha_hospitalaria:
        claves = claves.mask(~es_hospitalizacion, -1)

    df_fact[columna_clave] = claves

# ==========================
# %% CARGAR TABLA DE HECHOS
# ==========================

# Cada registro representa una prestación
df_fact["CantidadPrestaciones"] = 1

columnas_claves_fact = [
    "FechaPrestacionKey",
    "FechaIngresoKey",
    "FechaEgresoKey",
    "FechaRecepcionKey",
    "IafasKey",
    "IpressKey",
    "PacienteKey",
    "AfiliacionKey",
    "CoberturaKey",
    "DiagnosticoKey",
    "TipoProfesionalKey",
    "HospitalizacionKey",
    "UbicacionIpressKey",
    "UbicacionAfiliadoKey"
]

columnas_carga_fact = (
    columnas_claves_fact
    + [
        "TipoDocumentoPago",
        "DocumentoPagoAnonimizado",
        "CorrelativoPrestacion",
        "CantidadPrestaciones",
        "DiasEstanciaFacturable"
    ]
    + columnas_montos
)

# Seleccionar únicamente los campos del destino
df_carga_fact = df_fact[columnas_carga_fact].copy()

# Verificar que se conservan todas las prestaciones
if len(df_carga_fact) != len(df):
    raise ValueError(
        "La cantidad de prestaciones preparada "
        "no coincide con la fuente."
    )

# Las claves foráneas no deben quedar vacías
claves_vacias = (
    df_carga_fact[columnas_claves_fact]
    .isna()
    .sum()
)

if claves_vacias.gt(0).any():
    raise ValueError(
        "Hay claves dimensionales vacías:\n"
        f"{claves_vacias[claves_vacias.gt(0)].to_string()}"
    )

# Validar la longitud de los campos de texto
limites_texto_fact = {
    "TipoDocumentoPago": 10,
    "DocumentoPagoAnonimizado": 64
}

for columna, limite in limites_texto_fact.items():

    excede_longitud = (
        df_carga_fact[columna]
        .astype("string")
        .str.len()
        .gt(limite)
        .fillna(False)
    )

    if excede_longitud.any():
        raise ValueError(
            f"El campo {columna} contiene valores "
            f"que superan los {limite} caracteres."
        )

# cargar la fact

if dest_conn.autocommit:
    raise ValueError(
        "La conexión debe tener autocommit desactivado "
        "para poder revertir la carga si ocurre un error."
    )

cursor_fact = dest_conn.cursor()

try:
    # Evitar cargar nuevamente las mismas prestaciones
    cursor_fact.execute(
        "SELECT COUNT_BIG(*) FROM dbo.FactPrestacionSalud"
    )

    registros_actuales = cursor_fact.fetchone()[0]

    if registros_actuales > 0:
        raise ValueError(
            "FactPrestacionSalud ya contiene "
            f"{registros_actuales} registros. "
            "No se realizará una nueva carga."
        )

    campos_sql = ", ".join(
        f"[{columna}]"
        for columna in columnas_carga_fact
    )

    parametros = ", ".join(
        "?" for columna in columnas_carga_fact
    )

    consulta_fact = (
        f"INSERT INTO dbo.FactPrestacionSalud ({campos_sql}) "
        f"VALUES ({parametros})"
    )

    cursor_fact.fast_executemany = True

    total_prestaciones = len(df_carga_fact)

    for inicio in range(0, total_prestaciones, 5000):

        lote = (
            df_carga_fact
            .iloc[inicio:inicio + 5000]
            .astype(object)
        )

        # Convertir los valores faltantes a NULL
        lote = lote.where(pd.notna(lote), None)

        registros = list(
            lote.itertuples(index=False, name=None)
        )

        cursor_fact.executemany(
            consulta_fact,
            registros
        )

        procesados = inicio + len(lote)

        if (
            procesados % 50000 == 0
            or procesados == total_prestaciones
        ):
            print(
                f"Prestaciones insertadas: "
                f"{procesados:,} de {total_prestaciones:,} "
                "(pendientes de confirmar)."
            )

    # Verificar la carga antes de confirmarla
    cursor_fact.execute("""
        SELECT
            COUNT_BIG(*),
            SUM(CAST(CantidadPrestaciones AS BIGINT))
        FROM dbo.FactPrestacionSalud
    """)

    filas_sql, contador_sql = cursor_fact.fetchone()

    if (
        filas_sql != total_prestaciones
        or contador_sql != total_prestaciones
    ):
        raise ValueError(
            "La cantidad cargada en SQL Server "
            "no coincide con las prestaciones preparadas."
        )

    # Consumir el resultado anterior antes de abrir otro cursor
    cursor_fact.fetchall()

    # Comparar los 15 montos y sus nulos antes de confirmar la carga
    validacion_montos = validar_montos_cargados(dest_conn, df_carga_fact)

    dest_conn.commit()

    print("\nCarga de FactPrestacionSalud confirmada.")
    print("Registros cargados:", filas_sql)
    print("Total del contador de prestaciones:", contador_sql)

except Exception:
    dest_conn.rollback()

    print(
        "\nLa carga de hechos no se completó. "
        "Se revirtieron las inserciones de este bloque."
    )

    raise

finally:
    cursor_fact.close()

# agregar valores a los codigos de cada dimension
# ==========================
# %% AGREGAR DESCRIPCIÓN DEL TIPO DE PROFESIONAL
# ==========================

cursor_auxiliar = dest_conn.cursor()

try:
    cursor_auxiliar.execute("""
        IF COL_LENGTH(
            'dbo.DimTipoProfesional',
            'DescripcionTipoProfesional'
        ) IS NULL
        BEGIN
            ALTER TABLE dbo.DimTipoProfesional
            ADD DescripcionTipoProfesional VARCHAR(100) NULL;
        END
    """)

    dest_conn.commit()

    print("Columna DescripcionTipoProfesional disponible.")

    # Consultar los códigos que debemos describir
    cursor_auxiliar.execute("""
        SELECT
            TipoProfesionalKey,
            CodigoTipoProfesional,
            DescripcionTipoProfesional
        FROM dbo.DimTipoProfesional
        ORDER BY CodigoTipoProfesional;
    """)

    for fila in cursor_auxiliar.fetchall():
        print(tuple(fila))

except Exception:
    dest_conn.rollback()
    raise

finally:
    cursor_auxiliar.close()

# Etiquetas basadas en el diccionario oficial de SUSALUD
catalogo_tipo_profesional = {
    "00": "Profesional sin colegiatura",
    "01": "Médico",
    "02": "Químico farmacéutico",
    "03": "Odontólogo",
    "04": "Biólogo",
    "05": "Obstetra",
    "06": "Enfermero",
    "07": "Trabajador social",
    "08": "Psicólogo",
    "09": "Tecnólogo médico",
    "10": "Nutricionista",
    "91": "Licenciado en Educación Especial"
}

cursor_auxiliar = dest_conn.cursor()

try:
    cursor_auxiliar.execute("""
        SELECT
            TipoProfesionalKey,
            CodigoTipoProfesional
        FROM dbo.DimTipoProfesional;
    """)

    profesionales = cursor_auxiliar.fetchall()

    actualizaciones = []

    for clave, codigo in profesionales:

        # Normalizar solo para buscar la equivalencia
        codigo_busqueda = str(codigo).strip().zfill(2)

        if codigo_busqueda not in catalogo_tipo_profesional:
            raise ValueError(
                f"El código de profesional {codigo} "
                "no tiene equivalencia en el catálogo."
            )

        descripcion = catalogo_tipo_profesional[codigo_busqueda]

        actualizaciones.append(
            (descripcion, clave)
        )

    cursor_auxiliar.executemany("""
        UPDATE dbo.DimTipoProfesional
        SET DescripcionTipoProfesional = ?
        WHERE TipoProfesionalKey = ?;
    """, actualizaciones)

    cursor_auxiliar.execute("""
        SELECT
            CodigoTipoProfesional,
            DescripcionTipoProfesional
        FROM dbo.DimTipoProfesional
        ORDER BY TRY_CONVERT(INT, CodigoTipoProfesional);
    """)

    resultado = cursor_auxiliar.fetchall()

    if any(descripcion is None for codigo, descripcion in resultado):
        raise ValueError(
            "Quedaron tipos de profesional sin descripción."
        )

    dest_conn.commit()

    print("\nTipos de profesional actualizados:", len(resultado))

    for fila in resultado:
        print(tuple(fila))

except Exception:
    dest_conn.rollback()
    raise

finally:
    cursor_auxiliar.close()
# ==========================
# %% COMPLETAR DESCRIPCIONES DE HOSPITALIZACIÓN
# ==========================

catalogo_hospitalizacion = {
    "C": "Hospitalización clínica",
    "Q": "Hospitalización quirúrgica",
    "N": "No aplica"
}

catalogo_egreso = {
    "01": "Alta médica",
    "02": "Alta voluntaria",
    "03": "Transferencia a otro establecimiento de IAFAS",
    "04": "Transferencia a EsSalud",
    "05": "Fuga o abandono",
    "06": "Defunción",
    "07": "Egreso de facturación (continúa hospitalizado)"
}

cursor_auxiliar = dest_conn.cursor()

try:
    # Agregar las columnas si todavía no existen
    cursor_auxiliar.execute("""
        IF COL_LENGTH(
            'dbo.DimHospitalizacion',
            'DescripcionTipoHospitalizacion'
        ) IS NULL
        BEGIN
            ALTER TABLE dbo.DimHospitalizacion
            ADD DescripcionTipoHospitalizacion VARCHAR(100) NULL;
        END
    """)

    cursor_auxiliar.execute("""
        IF COL_LENGTH(
            'dbo.DimHospitalizacion',
            'DescripcionTipoEgreso'
        ) IS NULL
        BEGIN
            ALTER TABLE dbo.DimHospitalizacion
            ADD DescripcionTipoEgreso VARCHAR(100) NULL;
        END
    """)

    cursor_auxiliar.execute("""
        SELECT
            HospitalizacionKey,
            CodigoTipoHospitalizacion,
            CodigoTipoEgreso
        FROM dbo.DimHospitalizacion;
    """)

    hospitalizaciones = cursor_auxiliar.fetchall()

    actualizaciones = []

    for clave, tipo, egreso in hospitalizaciones:

        tipo_busqueda = (
            str(tipo).strip().upper()
            if tipo is not None
            else None
        )

        egreso_busqueda = (
            str(egreso).strip().zfill(2)
            if egreso is not None
            else None
        )

        # Combinación sin hospitalización, validada previamente
        if (
            tipo_busqueda in (None, "N")
            and egreso_busqueda is None
        ):
            descripcion_tipo = "No aplica"
            descripcion_egreso = "No aplica"

        else:
            if tipo_busqueda not in catalogo_hospitalizacion:
                raise ValueError(
                    f"Tipo de hospitalización sin equivalencia: {tipo}"
                )

            if egreso_busqueda not in catalogo_egreso:
                raise ValueError(
                    f"Tipo de egreso sin equivalencia: {egreso}"
                )

            descripcion_tipo = (
                catalogo_hospitalizacion[tipo_busqueda]
            )

            descripcion_egreso = catalogo_egreso[egreso_busqueda]

        actualizaciones.append(
            (descripcion_tipo, descripcion_egreso, clave)
        )

    cursor_auxiliar.executemany("""
        UPDATE dbo.DimHospitalizacion
        SET
            DescripcionTipoHospitalizacion = ?,
            DescripcionTipoEgreso = ?
        WHERE HospitalizacionKey = ?;
    """, actualizaciones)

    cursor_auxiliar.execute("""
        SELECT
            CodigoTipoHospitalizacion,
            CodigoTipoEgreso,
            DescripcionTipoHospitalizacion,
            DescripcionTipoEgreso
        FROM dbo.DimHospitalizacion
        ORDER BY
            CodigoTipoHospitalizacion,
            CodigoTipoEgreso;
    """)

    resultado = cursor_auxiliar.fetchall()

    dest_conn.commit()

    print("\nCombinaciones actualizadas:", len(resultado))

    for fila in resultado:
        print(tuple(fila))

except Exception:
    dest_conn.rollback()
    raise

finally:
    cursor_auxiliar.close()

# ==========================
# %% COMPLETAR DESCRIPCIONES DE AFILIACIÓN
# ==========================

catalogo_afiliacion = {
    "01": "Regular",
    "02": "SCTR",
    "03": "Potestativo (independiente)",
    "04": "SCTR independiente",
    "05": "Otros contributivos y complementario",
    "06": "SOAT",
    "07": "AFOCAT",
    "08": "SIS subsidiado",
    "09": "Semicontributivo"
}

catalogo_filiacion = {
    "01": "Titular",
    "02": "Cónyuge",
    "03": "Concubino(a)",
    "04": "Madre gestante de hijo extramatrimonial",
    "05": "Hijo no incapacitado",
    "06": "Hijo incapacitado",
    "07": "Padres",
    "08": "Hermano(a)",
    "09": "Abuelo(a)",
    "10": "Tío(a)",
    "11": "Nieto(a)",
    "12": "Sobrino(a)",
    "13": "Primo(a)",
    "14": "Padres del cónyuge o concubino(a)",
    "15": "Hijo(a) del cónyuge o concubino(a)",
    "16": "Viudo(a)",
    "17": "Otros"
}

cursor_auxiliar = dest_conn.cursor()

try:
    # Agregar las columnas descriptivas
    for columna in [
        "DescripcionTipoAfiliacion",
        "DescripcionFiliacionPaciente"
    ]:
        cursor_auxiliar.execute(f"""
            IF COL_LENGTH(
                'dbo.DimAfiliacion',
                '{columna}'
            ) IS NULL
            BEGIN
                ALTER TABLE dbo.DimAfiliacion
                ADD [{columna}] VARCHAR(100) NULL;
            END
        """)

    cursor_auxiliar.execute("""
        SELECT
            AfiliacionKey,
            CodigoTipoAfiliacion,
            CodigoFiliacionPaciente
        FROM dbo.DimAfiliacion;
    """)

    afiliaciones = cursor_auxiliar.fetchall()

    actualizaciones = []

    for clave, afiliacion, filiacion in afiliaciones:

        codigo_afiliacion = (
            str(afiliacion).strip().zfill(2)
        )

        codigo_filiacion = (
            str(filiacion).strip().zfill(2)
        )

        if codigo_afiliacion not in catalogo_afiliacion:
            raise ValueError(
                "Tipo de afiliación sin equivalencia: "
                f"{afiliacion}"
            )

        if codigo_filiacion not in catalogo_filiacion:
            raise ValueError(
                "Filiación del paciente sin equivalencia: "
                f"{filiacion}"
            )

        actualizaciones.append((
            catalogo_afiliacion[codigo_afiliacion],
            catalogo_filiacion[codigo_filiacion],
            clave
        ))

    cursor_auxiliar.executemany("""
        UPDATE dbo.DimAfiliacion
        SET
            DescripcionTipoAfiliacion = ?,
            DescripcionFiliacionPaciente = ?
        WHERE AfiliacionKey = ?;
    """, actualizaciones)

    cursor_auxiliar.execute("""
        SELECT
            CodigoTipoAfiliacion,
            DescripcionTipoAfiliacion,
            CodigoFiliacionPaciente,
            DescripcionFiliacionPaciente
        FROM dbo.DimAfiliacion
        ORDER BY
            TRY_CONVERT(INT, CodigoTipoAfiliacion),
            TRY_CONVERT(INT, CodigoFiliacionPaciente);
    """)

    resultado = cursor_auxiliar.fetchall()

    dest_conn.commit()

    print("\nCombinaciones actualizadas:", len(resultado))

    for fila in resultado:
        print(tuple(fila))

except Exception:
    dest_conn.rollback()
    raise

finally:
    cursor_auxiliar.close()
    
# ==========================
# %% COMPLETAR DESCRIPCIÓN DEL TIPO DE COBERTURA
# ==========================

catalogo_cobertura = {
    "00": "No aplica",
    "01": "Extrahospitalaria",
    "02": "Médico en planta",
    "03": "Medicinas alternativas",
    "04": "Ambulatoria",
    "05": "Hospitalaria",
    "06": "Emergencia",
    "08": "Integral (exclusivo para el SIS)",
    "09": "Otros"
}

cursor_auxiliar = dest_conn.cursor()

try:
    cursor_auxiliar.execute("""
        IF COL_LENGTH(
            'dbo.DimCobertura',
            'DescripcionTipoCobertura'
        ) IS NULL
        BEGIN
            ALTER TABLE dbo.DimCobertura
            ADD DescripcionTipoCobertura VARCHAR(100) NULL;
        END
    """)

    cursor_auxiliar.execute("""
        SELECT
            CoberturaKey,
            CodigoTipoCobertura
        FROM dbo.DimCobertura;
    """)

    coberturas = cursor_auxiliar.fetchall()

    actualizaciones = []

    for clave, codigo in coberturas:

        codigo_busqueda = str(codigo).strip().zfill(2)

        if codigo_busqueda not in catalogo_cobertura:
            raise ValueError(
                f"Tipo de cobertura sin equivalencia: {codigo}"
            )

        actualizaciones.append((
            catalogo_cobertura[codigo_busqueda],
            clave
        ))

    cursor_auxiliar.executemany("""
        UPDATE dbo.DimCobertura
        SET DescripcionTipoCobertura = ?
        WHERE CoberturaKey = ?;
    """, actualizaciones)

    cursor_auxiliar.execute("""
        SELECT DISTINCT
            CodigoTipoCobertura,
            DescripcionTipoCobertura
        FROM dbo.DimCobertura
        ORDER BY CodigoTipoCobertura;
    """)

    resultado = cursor_auxiliar.fetchall()

    dest_conn.commit()

    print(
        "\nCombinaciones de cobertura actualizadas:",
        len(actualizaciones)
    )

    print("\nTipos de cobertura:")

    for fila in resultado:
        print(tuple(fila))

except Exception:
    dest_conn.rollback()
    raise

finally:
    cursor_auxiliar.close()

# ==========================
# %% COMPLETAR DESCRIPCIÓN DEL SEXO
# ==========================

catalogo_sexo = {
    "01": "Masculino",
    "02": "Femenino"
}

cursor_auxiliar = dest_conn.cursor()

try:
    cursor_auxiliar.execute("""
        IF COL_LENGTH(
            'dbo.DimPaciente',
            'DescripcionSexo'
        ) IS NULL
        BEGIN
            ALTER TABLE dbo.DimPaciente
            ADD DescripcionSexo VARCHAR(20) NULL;
        END
    """)

    # Consultar los códigos distintos, no todos los perfiles
    cursor_auxiliar.execute("""
        SELECT DISTINCT CodigoSexo
        FROM dbo.DimPaciente;
    """)

    codigos = cursor_auxiliar.fetchall()

    actualizaciones = []

    for fila in codigos:

        codigo_original = fila[0]
        codigo_busqueda = str(codigo_original).strip().zfill(2)

        if codigo_busqueda not in catalogo_sexo:
            raise ValueError(
                f"Código de sexo sin equivalencia: {codigo_original}"
            )

        actualizaciones.append((
            catalogo_sexo[codigo_busqueda],
            codigo_original
        ))

    # Cada actualización completa todos los perfiles de ese código
    cursor_auxiliar.executemany("""
        UPDATE dbo.DimPaciente
        SET DescripcionSexo = ?
        WHERE CodigoSexo = ?;
    """, actualizaciones)

    cursor_auxiliar.execute("""
        SELECT
            CodigoSexo,
            DescripcionSexo,
            COUNT_BIG(*) AS CantidadPerfiles
        FROM dbo.DimPaciente
        GROUP BY CodigoSexo, DescripcionSexo
        ORDER BY CodigoSexo;
    """)

    resultado = cursor_auxiliar.fetchall()

    dest_conn.commit()

    print("\nDescripción del sexo completada:")

    for fila in resultado:
        print(tuple(fila))

except Exception:
    dest_conn.rollback()
    raise

finally:
    cursor_auxiliar.close()
# ==========================
# %% COMPLETAR DESCRIPCIÓN DEL DOCUMENTO DE IDENTIDAD
# ==========================

catalogo_documento_identidad = {
    "01": "DNI",
    "02": "Carné de extranjería",
    "03": "Pasaporte",
    "04": "Documento de identidad extranjero",
    "05": "Código Único de Identificación (CUI)",
    "06": "Código de Nacido Vivo (CNV)",
    "07": "Sin documento de identidad",
    "A": "Permiso Temporal de Permanencia"
}

cursor_auxiliar = dest_conn.cursor()

try:
    cursor_auxiliar.execute("""
        IF COL_LENGTH(
            'dbo.DimPaciente',
            'DescripcionTipoDocumentoIdentidad'
        ) IS NULL
        BEGIN
            ALTER TABLE dbo.DimPaciente
            ADD DescripcionTipoDocumentoIdentidad VARCHAR(100) NULL;
        END
    """)

    cursor_auxiliar.execute("""
        SELECT DISTINCT TipoDocumentoIdentidad
        FROM dbo.DimPaciente;
    """)

    codigos = cursor_auxiliar.fetchall()

    actualizaciones = []

    for fila in codigos:

        codigo_original = fila[0]

        codigo_busqueda = (
            str(codigo_original).strip().upper()
        )

        # Completar el cero inicial solo en códigos numéricos
        if codigo_busqueda.isdigit():
            codigo_busqueda = codigo_busqueda.zfill(2)

        if codigo_busqueda not in catalogo_documento_identidad:
            raise ValueError(
                "Tipo de documento de identidad sin equivalencia: "
                f"{codigo_original}"
            )

        actualizaciones.append((
            catalogo_documento_identidad[codigo_busqueda],
            codigo_original
        ))

    cursor_auxiliar.executemany("""
        UPDATE dbo.DimPaciente
        SET DescripcionTipoDocumentoIdentidad = ?
        WHERE TipoDocumentoIdentidad = ?;
    """, actualizaciones)

    cursor_auxiliar.execute("""
        SELECT
            TipoDocumentoIdentidad,
            DescripcionTipoDocumentoIdentidad,
            COUNT_BIG(*) AS CantidadPerfiles
        FROM dbo.DimPaciente
        GROUP BY
            TipoDocumentoIdentidad,
            DescripcionTipoDocumentoIdentidad
        ORDER BY TipoDocumentoIdentidad;
    """)

    resultado = cursor_auxiliar.fetchall()

    dest_conn.commit()

    print("\nTipos de documento de identidad completados:")

    for fila in resultado:
        print(tuple(fila))

except Exception:
    dest_conn.rollback()
    raise

finally:
    cursor_auxiliar.close()
    
# ==========================
# ==========================
# %% CREAR VISTA PARA EL ANÁLISIS
# ==========================

cursor_auxiliar = dest_conn.cursor()

try:
    cursor_auxiliar.execute("""
        CREATE OR ALTER VIEW dbo.vwPrestacionSalud
        AS
        SELECT
            f.*,

            -- Fechas
            fp.Fecha AS FechaPrestacion,
            fi.Fecha AS FechaIngresoHospitalario,
            fe.Fecha AS FechaEgresoHospitalario,
            fr.Fecha AS FechaRecepcion,
            fp.Anio,
            fp.Trimestre,
            fp.Mes,
            fp.NombreMes,
            fp.DiaSemana,
            fp.NombreDiaSemana,

            -- Instituciones anonimizadas
            ia.CodigoIafasAnonimizado,
            ip.CodigoIpressAnonimizado,

            -- Perfil del paciente
            p.TipoDocumentoIdentidad,
            p.DescripcionTipoDocumentoIdentidad,
            p.PacienteAnonimizado,
            p.FechaNacimiento,
            p.CodigoSexo,
            p.DescripcionSexo,

            -- Afiliación
            af.CodigoTipoAfiliacion,
            af.DescripcionTipoAfiliacion,
            af.CodigoFiliacionPaciente,
            af.DescripcionFiliacionPaciente,

            -- Cobertura
            c.CodigoTipoCobertura,
            c.DescripcionTipoCobertura,
            c.CodigoSubtipoCobertura,

            -- Diagnóstico
            d.CodigoDiagnosticoCIE10,
            d.DescripcionDiagnostico,

            -- Profesional
            tp.CodigoTipoProfesional,
            tp.DescripcionTipoProfesional,

            -- Hospitalización
            h.CodigoTipoHospitalizacion,
            h.DescripcionTipoHospitalizacion,
            h.CodigoTipoEgreso,
            h.DescripcionTipoEgreso,

            -- Ubicación de la IPRESS
            ui.Ubigeo AS UbigeoIPRESS,
            ui.Departamento AS DepartamentoIPRESS,
            ui.Provincia AS ProvinciaIPRESS,
            ui.Distrito AS DistritoIPRESS,

            -- Ubicación del afiliado, en códigos INEI
            ua.Ubigeo AS UbigeoAfiliadoINEI,
            ua.Departamento AS DepartamentoAfiliado,
            ua.Provincia AS ProvinciaAfiliado,
            ua.Distrito AS DistritoAfiliado,

            -- Documento de pago
            CASE TRY_CONVERT(INT, f.TipoDocumentoPago)
                WHEN 1 THEN 'Factura'
                WHEN 2 THEN 'Recibo por honorarios'
                WHEN 3 THEN 'Boleta de venta'
                WHEN 4 THEN 'Liquidación de compra'
                WHEN 5 THEN 'Boleto de aviación comercial'
                WHEN 9 THEN 'Ticket o cinta de máquina registradora'
                WHEN 99 THEN 'Otros documentos autorizados por SUNAT'
                ELSE
                    CASE
                        WHEN NULLIF(
                            LTRIM(RTRIM(f.TipoDocumentoPago)), ''
                        ) IS NULL
                        THEN 'Sin dato'
                        ELSE 'Sin equivalencia'
                    END
            END AS DescripcionTipoDocumentoPago

        FROM dbo.FactPrestacionSalud AS f

        LEFT JOIN dbo.DimFecha AS fp
            ON f.FechaPrestacionKey = fp.FechaKey

        LEFT JOIN dbo.DimFecha AS fi
            ON f.FechaIngresoKey = fi.FechaKey

        LEFT JOIN dbo.DimFecha AS fe
            ON f.FechaEgresoKey = fe.FechaKey

        LEFT JOIN dbo.DimFecha AS fr
            ON f.FechaRecepcionKey = fr.FechaKey

        LEFT JOIN dbo.DimIAFAS AS ia
            ON f.IafasKey = ia.IafasKey

        LEFT JOIN dbo.DimIPRESS AS ip
            ON f.IpressKey = ip.IpressKey

        LEFT JOIN dbo.DimPaciente AS p
            ON f.PacienteKey = p.PacienteKey

        LEFT JOIN dbo.DimAfiliacion AS af
            ON f.AfiliacionKey = af.AfiliacionKey

        LEFT JOIN dbo.DimCobertura AS c
            ON f.CoberturaKey = c.CoberturaKey

        LEFT JOIN dbo.DimDiagnostico AS d
            ON f.DiagnosticoKey = d.DiagnosticoKey

        LEFT JOIN dbo.DimTipoProfesional AS tp
            ON f.TipoProfesionalKey = tp.TipoProfesionalKey

        LEFT JOIN dbo.DimHospitalizacion AS h
            ON f.HospitalizacionKey = h.HospitalizacionKey

        LEFT JOIN dbo.DimUbicacion AS ui
            ON f.UbicacionIpressKey = ui.UbicacionKey

        LEFT JOIN dbo.DimUbicacion AS ua
            ON f.UbicacionAfiliadoKey = ua.UbicacionKey;
    """)

    # Verificar que la vista conserva una fila por prestación
    cursor_auxiliar.execute("""
        SELECT
            COUNT_BIG(*),
            COUNT_BIG(DISTINCT PrestacionKey)
        FROM dbo.vwPrestacionSalud;
    """)

    filas_vista, prestaciones_distintas = (
        cursor_auxiliar.fetchone()
    )

    cursor_auxiliar.execute("""
        SELECT COUNT_BIG(*)
        FROM dbo.FactPrestacionSalud;
    """)

    filas_fact = cursor_auxiliar.fetchone()[0]

    if (
        filas_vista != filas_fact
        or prestaciones_distintas != filas_fact
    ):
        raise ValueError(
            "La vista no conserva una fila por prestación."
        )

    dest_conn.commit()

    print("\nVista de análisis actualizada.")
    print("Filas en la tabla de hechos:", filas_fact)
    print("Filas en la vista:", filas_vista)
    print("Claves de prestación distintas:", prestaciones_distintas)

except Exception:
    dest_conn.rollback()
    raise

finally:
    cursor_auxiliar.close()
    

# ==========================
# %% GUARDAR INCIDENCIAS
# ==========================

carpeta_incidencias = carpeta / "validaciones"

carpeta_incidencias.mkdir(
    parents=True,
    exist_ok=True
)

# Resumen del estado de ubicación del afiliado
resumen_ubicacion = (
    df["EstadoUbigeoAfiliado"]
    .value_counts()
    .rename_axis("EstadoUbigeoAfiliado")
    .reset_index(name="CantidadPrestaciones")
)

resumen_ubicacion.to_csv(
    carpeta_incidencias / "resumen_ubicacion_afiliado.csv",
    sep=";",
    encoding="utf-8-sig",
    index=False
)

# Códigos RENIEC informados que no tienen equivalencia
pendientes_ubigeo.to_csv(
    carpeta_incidencias / "ubigeos_sin_equivalencia.csv",
    sep=";",
    encoding="utf-8-sig",
    index=False
)

# Prestaciones con fechas hospitalarias posteriores a la recepción
incidencias_fechas_hospitalarias.to_csv(
    carpeta_incidencias / "incidencias_fechas_hospitalarias.csv",
    sep=";",
    encoding="utf-8-sig",
    index=False
)

print("\nArchivos de control guardados en:")
print(carpeta_incidencias)

print("\nResumen de ubicación:")
print(resumen_ubicacion.to_string(index=False))

print(
    "\nCódigos de ubigeo sin equivalencia:",
    len(pendientes_ubigeo)
)

print(
    "Prestaciones con fechas hospitalarias por revisar:",
    len(incidencias_fechas_hospitalarias)
)

columnas_identificador_paciente = [
    "TipoDocumentoIdentidad",
    "PacienteAnonimizado"
]

# Contar las fechas de nacimiento y códigos de sexo
# asociados a cada identificador
resumen_pacientes = (
    df.groupby(
        columnas_identificador_paciente,
        dropna=False
    )
    .agg(
        CantidadFechasNacimiento=("FechaNacimiento", "nunique"),
        CantidadCodigosSexo=("CodigoSexo", "nunique"),
        CantidadPrestaciones=("PacienteAnonimizado", "size")
    )
    .reset_index()
)

pacientes_inconsistentes = resumen_pacientes.loc[
    (resumen_pacientes["CantidadFechasNacimiento"] > 1)
    | (resumen_pacientes["CantidadCodigosSexo"] > 1)
].copy()

# Conservar cada perfil observado y su frecuencia
versiones_pacientes = (
    df.groupby(
        columnas_identificador_paciente
        + ["FechaNacimiento", "CodigoSexo"],
        dropna=False
    )
    .size()
    .reset_index(name="CantidadPrestacionesPerfil")
)

versiones_pacientes = versiones_pacientes.merge(
    pacientes_inconsistentes[columnas_identificador_paciente],
    on=columnas_identificador_paciente,
    how="inner",
    validate="many_to_one"
)

versiones_pacientes = versiones_pacientes.sort_values(
    columnas_identificador_paciente
    + ["FechaNacimiento", "CodigoSexo"]
)

# Guardar el resumen de identificadores afectados
pacientes_inconsistentes.to_csv(
    carpeta_incidencias / "resumen_inconsistencias_pacientes.csv",
    sep=";",
    encoding="utf-8-sig",
    index=False
)

# Guardar las versiones demográficas encontradas
versiones_pacientes.to_csv(
    carpeta_incidencias / "versiones_pacientes_inconsistentes.csv",
    sep=";",
    encoding="utf-8-sig",
    index=False
)

print(
    "\nIdentificadores con inconsistencias:",
    len(pacientes_inconsistentes)
)

print(
    "Con distintas fechas de nacimiento:",
    int(
        pacientes_inconsistentes["CantidadFechasNacimiento"]
        .gt(1)
        .sum()
    )
)

print(
    "Con distintos códigos de sexo:",
    int(
        pacientes_inconsistentes["CantidadCodigosSexo"]
        .gt(1)
        .sum()
    )
)

print("\nArchivos de incidencias de pacientes guardados.")

# Conservar también la evidencia de las validaciones y catálogos pendientes
validacion_montos.to_csv(
    carpeta_incidencias / "validacion_montos.csv",
    sep=";", encoding="utf-8-sig", index=False
)

pd.DataFrame(resumen_fechas).to_csv(
    carpeta_incidencias / "resumen_conversion_fechas.csv",
    sep=";", encoding="utf-8-sig", index=False
)

pendientes_diagnostico.to_csv(
    carpeta_incidencias / "diagnosticos_sin_descripcion.csv",
    sep=";", encoding="utf-8-sig", index=False
)

(carpeta_incidencias / "catalogo_pendiente.txt").write_text(
    "Se conserva CodigoSubtipoCobertura sin descripción. "
    "Su equivalencia queda pendiente del catálogo oficial de TEDEF.\n",
    encoding="utf-8"
)

# ==========================
# %% CERRAR CONEXIÓN
# ==========================

dest_conn.close()
print("\nETL finalizado y conexión cerrada.")