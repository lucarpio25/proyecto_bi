# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 19:34:32 2026

@author: lunya
"""

import pyodbc
from collections import Counter
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from textwrap import shorten, wrap
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State

# ==========================
# CARGAR LA MUESTRA
# ==========================

# La fuente actual es la vista del datamart; se conserva el encabezado original.
SERVIDOR = r"Laptop_Lu\SQLEXPRESS"
BASE_DATOS = "ProyectoDatamart"


def load_data():
    conexion = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SERVIDOR};"
        f"DATABASE={BASE_DATOS};"
        "Trusted_Connection=yes;",
        autocommit=True
    )

    cursor = None

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                PrestacionKey,
                FechaPrestacion,
                FechaRecepcion,
                TipoDocumentoIdentidad,
                PacienteAnonimizado,
                FechaNacimiento,
                CodigoDiagnosticoCIE10,
                DescripcionDiagnostico,
                CodigoTipoCobertura,
                DescripcionTipoCobertura,
                CodigoSexo,
                DescripcionSexo,
                CodigoTipoHospitalizacion,
                DescripcionTipoHospitalizacion,
                DiasEstanciaFacturable,
                CodigoIpressAnonimizado,
                CodigoIafasAnonimizado,
                UbigeoIPRESS,
                DepartamentoIPRESS,
                ProvinciaIPRESS,
                DistritoIPRESS,
                UbigeoAfiliadoINEI,
                DepartamentoAfiliado,
                ProvinciaAfiliado,
                DistritoAfiliado,
                TotalLiquidadoIAFAS,
                CopagoFijoAfectoSinIGV,
                CopagoFijoExonerado,
                CopagoVariableAfectoSinIGV,
                CopagoVariableExonerado,
                GastoHonorariosProcedimientos,
                GastoOdontologia,
                GastoHoteleriaServicioClinicoTopico,
                GastoLaboratorio,
                GastoImagenes,
                GastoFarmaciaInsumos,
                GastoProtesis,
                GastoExoneradoIGV,
                OtrosGastos
            FROM dbo.vwPrestacionSalud;
        """)

        columnas = [columna[0] for columna in cursor.description]
        bloques = []

        while True:
            filas = cursor.fetchmany(50000)
            if not filas:
                break

            bloques.append(pd.DataFrame.from_records(
                [tuple(fila) for fila in filas],
                columns=columnas
            ))

        if not bloques:
            raise ValueError("La vista del datamart no contiene prestaciones.")

        datos = pd.concat(bloques, ignore_index=True)

        if (
            datos["PrestacionKey"].isna().any()
            or datos["PrestacionKey"].duplicated().any()
        ):
            raise ValueError("La vista debe contener una fila por prestación.")

        return datos

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()

# Cargar los datos
df_full = load_data()

# ==========================
# %% TRANSFORMACIONES Y GRUPOS
# ==========================

# renombrar columnas

# SQL Server ya entrega los nombres definidos en el modelo dimensional.
columnas_codigo = [
    "TipoDocumentoIdentidad", "PacienteAnonimizado",
    "CodigoDiagnosticoCIE10", "CodigoTipoCobertura", "CodigoSexo",
    "CodigoTipoHospitalizacion", "CodigoIpressAnonimizado",
    "CodigoIafasAnonimizado", "UbigeoIPRESS", "UbigeoAfiliadoINEI"
]

for columna in columnas_codigo:
    df_full[columna] = (
        df_full[columna].astype("string").str.strip().replace("", pd.NA)
    )

nombres_montos = {
    "VTOTLIQIAFAS_ATE": "TotalLiquidadoIAFAS",
    "VCOPAGOFIJOSIGV_ATE": "CopagoFijoAfectoSinIGV",
    "VCPAGOFIJOEXIGV_ATE": "CopagoFijoExonerado",
    "VCOPAGOVARSIGV_ATE": "CopagoVariableAfectoSinIGV",
    "VCPAGOVAREXIGV_ATE": "CopagoVariableExonerado"
}


nombres_gastos = {
    "VGASTHONPROSIGV_ATE": "GastoHonorariosProcedimientos",
    "VGASTPRODOSIGV_ATE": "GastoOdontologia",
    "VGASTHTSCLITOPSIGV_ATE": "GastoHoteleriaServicioClinicoTopico",
    "VGASTEXAUXLABSIGV_ATE": "GastoLaboratorio",
    "VGASTEXAUXIMGSIGV_ATE": "GastoImagenes",
    "VGASTFARINSSIGV_ATE": "GastoFarmaciaInsumos",
    "VGASTPROTSIGV_ATE": "GastoProtesis",
    "VGASTMEDEXOIGV_ATE": "GastoExoneradoIGV",
    "VOGPRESSLDSIGV_ATE": "OtrosGastos"
}


columnas_gastos = list(nombres_gastos.values())

for columna in columnas_gastos:
    df_full[columna] = pd.to_numeric(
        df_full[columna],
        errors="raise"
    )

# cambiar formato de datos numericos

columnas_montos = list(nombres_montos.values())

for columna in columnas_montos:
    df_full[columna] = pd.to_numeric(
        df_full[columna],
        errors="raise"
    )

# cambiar el formato de las fechas

df_full["FechaPrestacion"] = pd.to_datetime(
    df_full["FechaPrestacion"],
    errors="raise"
)

df_full["FechaNacimiento"] = pd.to_datetime(
    df_full["FechaNacimiento"],
    errors="raise"
)

df_full["FechaRecepcion"] = pd.to_datetime(
    df_full["FechaRecepcion"], errors="raise"
).dt.normalize()

if df_full["FechaRecepcion"].isna().any():
    raise ValueError("Hay prestaciones sin fecha de recepción en la vista.")

df_full["AntiguedadDias"] = (
    df_full["FechaRecepcion"] - df_full["FechaPrestacion"].dt.normalize()
).dt.days

if df_full["AntiguedadDias"].lt(0).any():
    raise ValueError("Hay prestaciones posteriores a su recepción. Revisar el ETL.")

RANGOS_ANTIGUEDAD = ["0–30 días", "31–60 días", "61–90 días", "91–180 días", "Más de 180 días"]
df_full["RangoAntiguedad"] = pd.cut(
    df_full["AntiguedadDias"], bins=[-1, 30, 60, 90, 180, np.inf],
    labels=RANGOS_ANTIGUEDAD
)

# calcular la edad de los pacientes

fecha = df_full["FechaPrestacion"]
nacimiento = df_full["FechaNacimiento"]

cumpleanios_pendiente = (
    (fecha.dt.month < nacimiento.dt.month)
    | (
        (fecha.dt.month == nacimiento.dt.month)
        & (fecha.dt.day < nacimiento.dt.day)
    )
)

df_full["Edad"] = (
    fecha.dt.year
    - nacimiento.dt.year
    - cumpleanios_pendiente.astype(int)
).astype("Int64")

df_full.loc[
    fecha.isna() | nacimiento.isna() | (fecha < nacimiento),
    "Edad"
] = pd.NA


# añadir columna de grupos etarios

df_full["GrupoEtario"] = pd.cut(
    df_full["Edad"],
    bins=[0, 12, 18, 30, 45, 60, float("inf")],
    labels=["0–11", "12–17", "18–29", "30–44", "45–59", "60 o más"],
    right=False
)

# preparar campos de hospitalizacion

columnas_hospitalizacion = [
    "CodigoTipoHospitalizacion"
]

for columna in columnas_hospitalizacion:
    df_full[columna] = (
        df_full[columna].str.strip().replace("", pd.NA)
    )

df_full["DiasEstanciaFacturable"] = pd.to_numeric(
    df_full["DiasEstanciaFacturable"],
    errors="coerce"
)

# ==========================
# %% INDICADORES
# ==========================

# indicadores de utilización de servicios

def calcular_indicadores_utilizacion(datos):
    columnas_paciente = [
        "TipoDocumentoIdentidad",
        "PacienteAnonimizado"
    ]

    datos_paciente = datos[columnas_paciente].apply(
        lambda columna: columna.str.strip()
    ).replace("", pd.NA)

    pacientes_validos = datos_paciente.dropna(
        subset=columnas_paciente
    )

    total_prestaciones = len(datos)
    total_pacientes = len(pacientes_validos.drop_duplicates())

    promedio_prestaciones = (
        len(pacientes_validos) / total_pacientes
        if total_pacientes > 0
        else None
    )

    return {
        "TotalPrestaciones": total_prestaciones,
        "IdentificadoresDistintos": total_pacientes,
        "PrestacionesPorIdentificador": promedio_prestaciones
    }


indicadores_utilizacion = calcular_indicadores_utilizacion(df_full)

# indicadores de gastos y copagos

def calcular_indicadores_gastos(datos):
    montos_liquidados = datos["TotalLiquidadoIAFAS"]

    columnas_copago = [
        "CopagoFijoAfectoSinIGV",
        "CopagoFijoExonerado",
        "CopagoVariableAfectoSinIGV",
        "CopagoVariableExonerado"
    ]

    copago_por_prestacion = datos[columnas_copago].sum(
        axis=1,
        min_count=4
    )

    return {
        "MontoTotalLiquidado": montos_liquidados.sum(min_count=1),
        "MontoPromedioLiquidado": montos_liquidados.mean(),
        "CopagoTotal": copago_por_prestacion.sum(min_count=1),
        "CopagoPromedio": copago_por_prestacion.mean()
    }


indicadores_gastos = calcular_indicadores_gastos(df_full)


# porcentaje de representacion de componentes

def calcular_composicion(datos, columnas):
    registros_completos = datos.dropna(subset=columnas)

    totales = registros_completos[columnas].sum()
    gasto_total = totales.sum()

    resultado = totales.reset_index()
    resultado.columns = ["Componente", "Monto"]

    if gasto_total > 0:
        resultado["Porcentaje"] = (
            resultado["Monto"] / gasto_total * 100
        )
    else:
        resultado["Porcentaje"] = float("nan")

    return resultado


composicion_gasto = calcular_composicion(
    df_full,
    columnas_gastos
)

# indicadores de hospitalizacion

def calcular_indicadores_hospitalizacion(datos):
    hospitalarias = datos[
        datos["CodigoTipoHospitalizacion"].isin(["C", "Q"])
    ].copy()

    dias = hospitalarias["DiasEstanciaFacturable"]
    dias_validos = dias[dias >= 0]

    return {
        "PrestacionesHospitalarias": len(hospitalarias),
        "PrestacionesConDiasValidos": dias_validos.count(),
        "PromedioDiasEstancia": dias_validos.mean(),
        "MontoPromedioHospitalario":
            hospitalarias["TotalLiquidadoIAFAS"].mean()
    }


indicadores_hospitalizacion = (
    calcular_indicadores_hospitalizacion(df_full)
)

# ==========================
# %% PREPARACION DE DATOS
# ==========================


if df_full["FechaPrestacion"].isna().any():
    raise ValueError("Hay prestaciones sin fecha; revisar el datamart.")


def obtener_descripciones(columna_codigo, columna_descripcion):
    pares = df_full[[columna_codigo, columna_descripcion]].drop_duplicates()

    if pares[columna_codigo].duplicated().any():
        raise ValueError(
            f"Un código de {columna_codigo} tiene varias descripciones."
        )

    return {
        codigo: descripcion if pd.notna(descripcion) else str(codigo)
        for codigo, descripcion in pares.itertuples(index=False, name=None)
        if pd.notna(codigo)
    }


nombres_coberturas = obtener_descripciones(
    "CodigoTipoCobertura", "DescripcionTipoCobertura"
)
nombres_sexos = obtener_descripciones("CodigoSexo", "DescripcionSexo")
nombres_diagnosticos = obtener_descripciones(
    "CodigoDiagnosticoCIE10", "DescripcionDiagnostico"
)

MINIMO_PRESTACIONES = 10
MAXIMO_DIAGNOSTICOS = 15
RANGOS_ESTANCIA = ["0–1", "2–3", "4–7", "8–14", "15–30", "Más de 30"]

# Abreviar por longitud sin inventar equivalencias clínicas; el hover conserva el nombre completo.
etiquetas_diagnosticos = {
    codigo: shorten(" ".join(str(nombre).split()).capitalize(), width=42, placeholder="…")
    for codigo, nombre in nombres_diagnosticos.items()
}
repeticiones_etiquetas = Counter(etiquetas_diagnosticos.values())
etiquetas_diagnosticos = {
    codigo: f"{etiqueta} [{codigo}]" if repeticiones_etiquetas[etiqueta] > 1 else etiqueta
    for codigo, etiqueta in etiquetas_diagnosticos.items()
}


def filtrar_recepcion(datos, inicio, fin):
    if inicio:
        datos = datos[datos["FechaRecepcion"] >= pd.to_datetime(inicio)]
    if fin:
        datos = datos[datos["FechaRecepcion"] < pd.to_datetime(fin) + pd.Timedelta(days=1)]
    return datos


def opciones_diagnosticos_frecuentes(datos, seleccion):
    frecuencias = datos["CodigoDiagnosticoCIE10"].value_counts()
    frecuencias = frecuencias[frecuencias >= MINIMO_PRESTACIONES].head(MAXIMO_DIAGNOSTICOS)
    opciones = [
        {"label": f"{etiquetas_diagnosticos.get(codigo, codigo)} · n={cantidad:,}", "value": codigo}
        for codigo, cantidad in frecuencias.items()
    ]
    return opciones, seleccion if seleccion in frecuencias.index else None


def mostrar_nombres_diagnosticos(figura, codigos):
    figura.update_yaxes(
        tickmode="array", tickvals=list(codigos),
        ticktext=["<br>".join(wrap(etiquetas_diagnosticos.get(codigo, str(codigo)), 25)) for codigo in codigos],
        title_text="Diagnóstico", automargin=True
    )
    figura.update_layout(margin=dict(l=190))


def figura_sin_datos(titulo, mensaje):
    figura = go.Figure()
    figura.update_layout(title=titulo)
    figura.add_annotation(text=mensaje, x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
    formato_grafico(figura)
    return figura


# Las descripciones se usan en filtros y ayudas; los códigos siguen siendo las claves de búsqueda.
opciones_coberturas = [
    {"label": f"{codigo} · {descripcion}", "value": codigo}
    for codigo, descripcion in sorted(nombres_coberturas.items())
]
opciones_sexos = [
    {"label": descripcion, "value": codigo}
    for codigo, descripcion in sorted(nombres_sexos.items())
]
opciones_diagnosticos = [
    {"label": f"{codigo} · {descripcion}", "value": codigo}
    for codigo, descripcion in sorted(nombres_diagnosticos.items())
]

coberturas = sorted(
    df_full["CodigoTipoCobertura"].dropna().unique()
)

sexos = sorted(
    df_full["CodigoSexo"].dropna().unique()
)

grupos_etarios = (
    df_full["GrupoEtario"].cat.categories.tolist()
)

fecha_minima = df_full["FechaRecepcion"].min()
fecha_maxima = df_full["FechaRecepcion"].max()

diagnosticos = sorted(
    df_full["CodigoDiagnosticoCIE10"].dropna().unique()
)

codigos_ipress = sorted(
    df_full["CodigoIpressAnonimizado"].dropna().unique()
)

etiquetas_ipress = {
    codigo: f"IPRESS {numero}"
    for numero, codigo in enumerate(codigos_ipress, start=1)
}

df_full["EtiquetaIPRESS"] = (
    df_full["CodigoIpressAnonimizado"].map(etiquetas_ipress)
)

codigos_iafas = sorted(
    df_full["CodigoIafasAnonimizado"].dropna().unique()
)

etiquetas_iafas = {
    codigo: f"IAFAS {numero}"
    for numero, codigo in enumerate(codigos_iafas, start=1)
}

df_full["EtiquetaIAFAS"] = (
    df_full["CodigoIafasAnonimizado"].map(etiquetas_iafas)
)

# ==========================
# COMPARAR CODIFICACIONES DE UBIGEO
# ==========================
# ==========================
# CORREGIR UBICACIÓN DEL AFILIADO: RENIEC
# ==========================
# Normalizar el código original sin cambiar su significado
# Preparar la equivalencia RENIEC -> INEI y nombres geográficos
# Retirar las descripciones de la unión anterior
# Incorporar las descripciones utilizando RENIEC
# Normalizar el ubigeo de la IPRESS
# Preparar el catálogo de ubicaciones de IPRESS
# Excluir claves vacías del catálogo
# Evitar columnas repetidas al realizar la unión
# Incorporar los nombres geográficos mediante el código INEI

# Las operaciones descritas arriba ya se realizaron en el ETL.
# La vista entrega ambas ubicaciones en INEI y sus nombres; aquí no se vuelve a cruzar RENIEC.
for columna in ["UbigeoIPRESS", "UbigeoAfiliadoINEI"]:
    codigos = df_full[columna].astype("string").str.strip().replace("", pd.NA)
    invalidos = codigos.notna() & ~codigos.str.fullmatch(r"[0-9]{1,6}", na=False)
    if invalidos.any():
        raise ValueError(f"Hay códigos INEI mal formados en {columna}.")
    df_full[columna] = codigos.str.zfill(6)

if df_full.columns.duplicated().any():
    raise ValueError("La consulta devolvió columnas repetidas.")

# Reducir memoria en las descripciones que se repiten en muchas prestaciones.
for columna in [
    "DescripcionDiagnostico", "DescripcionTipoCobertura", "DescripcionSexo",
    "DescripcionTipoHospitalizacion", "DepartamentoIPRESS", "ProvinciaIPRESS",
    "DistritoIPRESS", "DepartamentoAfiliado", "ProvinciaAfiliado", "DistritoAfiliado"
]:
    df_full[columna] = df_full[columna].astype("category")

# ==========================
# %% INICIALIZAR APLICACIÓN DASH
# ==========================

app = dash.Dash(__name__, title="Prestaciones de salud")


# Estilo visual
COLORES_SALUD = ["#16786F", "#70B8A5", "#375B70", "#A5CFC0", "#CA9E59",
                 "#8A839D", "#4E9EB0", "#B37A71", "#768C5D"]
px.defaults.color_discrete_sequence = COLORES_SALUD
COLORES_SEXO = {nombres_sexos.get(codigo, codigo): COLORES_SALUD[i % len(COLORES_SALUD)]
               for i, codigo in enumerate(sexos)}
COLORES_SEXO["Sin información"] = "#A3AAA7"
ETIQUETAS_GASTOS = {
    "GastoHonorariosProcedimientos": "Honorarios y procedimientos",
    "GastoOdontologia": "Odontología",
    "GastoHoteleriaServicioClinicoTopico": "Hotelería y servicios clínicos",
    "GastoLaboratorio": "Laboratorio",
    "GastoImagenes": "Imágenes",
    "GastoFarmaciaInsumos": "Farmacia e insumos",
    "GastoProtesis": "Prótesis",
    "GastoExoneradoIGV": "Exonerados de IGV",
    "OtrosGastos": "Otros gastos"
}
COLORES_GASTO = dict(zip(ETIQUETAS_GASTOS.values(), COLORES_SALUD))

def formato_grafico(figura, colores=None):
    from textwrap import wrap

    titulo = figura.layout.title.text or ""
    partes = []
    for parte in titulo.split("<br>"):
        es_subtitulo = "<sup>" in parte
        texto = parte.replace("<sup>", "").replace("</sup>", "")
        texto = "<br>".join(wrap(texto, width=85 if es_subtitulo else 56))
        partes.append(f"<sup>{texto}</sup>" if es_subtitulo else texto)
    figura.update_layout(
        font=dict(family="Segoe UI, Calibri, sans-serif", size=13, color="#304B48"),
        title=dict(text="<br>".join(partes), x=0.04, xanchor="left",
                   font=dict(family="Georgia, serif", size=17, color="#214F49")),
        paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=70, r=30, t=110 if len(partes) > 1 else 85, b=55),
        legend=dict(font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="white", font=dict(size=12)),
        bargap=0.3
    )
    figura.update_xaxes(automargin=True, gridcolor="#EDF1ED", zeroline=False,
                        title_font=dict(size=12), tickfont=dict(size=11))
    figura.update_yaxes(automargin=True, gridcolor="#EDF1ED", zeroline=False,
                        title_font=dict(size=12), tickfont=dict(size=11))
    figura.update_traces(line=dict(width=2.5), marker=dict(size=7),
                          selector=dict(type="scatter", mode="lines+markers"))
    figura.update_traces(cliponaxis=False, selector=dict(type="bar"))
    if colores:
        for traza in figura.data:
            if traza.name in colores:
                traza.marker.color = colores[traza.name]

CSS_SALUD = """
* { box-sizing: border-box; }
body { margin:0; background:#F7F9F5; color:#29443F; font-family:"Segoe UI",Calibri,sans-serif; }
.app-salud { max-width:1480px; margin:0 auto; padding:28px 38px 48px !important; font-family:"Segoe UI",Calibri,sans-serif !important; }
.cabecera-salud { display:flex; align-items:center; gap:18px; margin:-28px -38px 25px; padding:30px 38px; background:#164B43; color:#FFFFFF; }
.cruz-salud { color:#99D5BD; font-size:45px; line-height:1; font-weight:300; }
.cabecera-salud strong { display:block; font-family:Georgia,"Times New Roman",serif; font-size:30px; font-weight:400; letter-spacing:-0.5px; }
.cabecera-salud small { display:block; color:#C4E2D4; font-size:12px; letter-spacing:1px; margin-top:7px; }
.pagina-salud > h1, .pagina-salud > h2 {
    background:#E5F1E9; border-left:5px solid #329784;
    color:#204E46; margin:24px 0 12px; padding:23px 25px;
    font-family:Georgia,"Times New Roman",serif; font-size:30px; font-weight:400; letter-spacing:-0.5px; line-height:1.25;
}
.pagina-salud > p { color:#6C7D73; margin:0 0 20px; font-size:14px; font-style:italic; }
.pagina-salud > h3 { font-family:Georgia,"Times New Roman",serif; font-size:23px; font-weight:400; margin:30px 0 15px; }
.filtros-salud { display:grid; grid-template-columns:repeat(4,minmax(0,1fr));
    gap:16px; padding:15px 0 23px; border-bottom:1px solid #DCE6DF;
    margin-bottom:20px; max-width:none !important; }
.filtros-salud.tres { grid-template-columns:repeat(3,minmax(0,1fr)); }
.filtros-salud.uno { grid-template-columns:minmax(240px,440px); padding:10px 0 14px;
    border:0; margin-bottom:12px; }
.campo-salud { min-width:0; }
.campo-salud > label { display:block; color:#4D695B; font-size:14px; font-weight:600; margin-bottom:8px; }
.campo-salud .DateRangePicker { width:100%; }
.DateRangePickerInput { border-color:#D4DFD7; border-radius:3px; width:100%; }
.DateInput { width:43%; background:transparent; }
.DateInput_input { font-size:13px; padding:9px 8px; color:#29443F; }
.DateRangePickerInput_arrow { width:8%; }
.Select-control { border-color:#D4DFD7; border-radius:3px; }
.Select-menu-outer { z-index:1000; }
.kpis-salud { display:grid !important; grid-template-columns:repeat(3,minmax(0,1fr));
    gap:0 !important; background:#FFF; margin:22px 0 28px !important;
    border-top:2px solid #6AB29D; border-bottom:1px solid #E0E7DF; }
.kpi-salud { background:transparent !important; border-radius:0 !important;
    padding:20px 25px !important; min-width:0; border-right:1px solid #E4EBE5; }
.kpi-salud:last-child { border-right:0; }
.kpi-salud h3, .kpi-salud h4 { font-size:16px; font-weight:600; color:#4E685C;
    margin:0 0 11px; line-height:1.45; }
.kpi-salud h2 { color:#236655; font-family:Georgia,"Times New Roman",serif; font-size:40px; font-weight:400; line-height:1.15; margin:0; font-variant-numeric:lining-nums tabular-nums; overflow-wrap:anywhere; }
.fila-salud { display:grid; grid-template-columns:minmax(0,1fr); gap:22px; margin:0 0 22px; }
.grafico-salud { min-width:0; height:460px; overflow:hidden; background:#FFF;
    border:1px solid #E2E9E1; border-radius:3px; padding:4px; }
.tabla-salud { background:#FFF; border:1px solid #E2E9E1; padding:8px 12px; margin:10px 0 26px; }
@media(min-width:1200px) { .fila-salud.doble { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media(max-width:1000px) { .filtros-salud,.filtros-salud.tres { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media(max-width:640px) {
    .app-salud { padding:18px 14px 35px !important; }
    .cabecera-salud { margin:-18px -14px 22px; padding:25px 20px; gap:12px; }
    .cabecera-salud strong { font-size:25px; }
    .cabecera-salud small { font-size:11px; letter-spacing:0.5px; }
    .kpi-salud h2 { font-size:36px; }
    .pagina-salud > h1,.pagina-salud > h2 { font-size:23px; padding:18px; }
    .filtros-salud,.filtros-salud.tres,.filtros-salud.uno { grid-template-columns:minmax(0,1fr); }
    .kpis-salud { grid-template-columns:minmax(0,1fr); }
    .kpi-salud { border-right:0; border-bottom:1px solid #E4EBE5; padding:16px 20px !important; }
    .grafico-salud { height:480px !important; }
}
"""

app.index_string = """<!DOCTYPE html>
<html lang="es"><head>{%metas%}<title>{%title%}</title>{%favicon%}{%css%}
<style>""" + CSS_SALUD + """</style></head><body>{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>"""

ESTILO_TAB = {"padding":"15px 12px", "border":"none", "borderBottom":"2px solid #DCE6DF",
              "backgroundColor":"transparent", "color":"#718177", "fontSize":"14px", "fontFamily":"Segoe UI, Calibri, sans-serif"}
ESTILO_TAB_ACTIVA = {**ESTILO_TAB, "borderBottom":"2px solid #238374",
                     "color":"#1E6759", "fontWeight":"600"}


app.layout = html.Div([
    html.Div([
        html.Span("+", className="cruz-salud", **{"aria-hidden":"true"}),
        html.Div([
            html.Strong("Prestaciones de salud"),
            html.Small("SUSALUD  /  Business Intelligence")
        ])
    ], className="cabecera-salud"),
    
    dcc.Tabs(
    id="selector-dashboard",
    value="utilizacion",
    children=[
        dcc.Tab(
            label="Utilización de prestaciones",
            value="utilizacion"
        , style=ESTILO_TAB, selected_style=ESTILO_TAB_ACTIVA),
        dcc.Tab(
            label="Gastos y copagos",
            value="gastos"
        , style=ESTILO_TAB, selected_style=ESTILO_TAB_ACTIVA),
        dcc.Tab(
            label="Distribución y hospitalización",
            value="hospitalizacion"
        , style=ESTILO_TAB, selected_style=ESTILO_TAB_ACTIVA)
        ]
    , style={"backgroundColor":"transparent"}),
    #primer dashboard
    html.Div([
        html.H1("Utilización de prestaciones de salud"),

        html.P(
            f"Datamart SUSALUD · {len(df_full):,} prestaciones",
            title="Los filtros temporales utilizan la fecha de recepción de información en TEDEF."
        ),
        
        html.Div([
        html.Div([
            html.Label("Fecha de recepción:"),
            dcc.DatePickerRange(
                id="filtro-fechas",
                min_date_allowed=fecha_minima.date(),
                max_date_allowed=fecha_maxima.date(),
                start_date=fecha_minima.date(),
                end_date=fecha_maxima.date()
            , display_format="DD/MM/YYYY")
        ], className="campo-salud"),
    
        html.Div([
            html.Label("Cobertura:"),
            dcc.Dropdown(
                id="filtro-cobertura",
                options=[{"label": "Todas", "value": "Todos"}]
                + opciones_coberturas,
                value="Todos",
                clearable=False
            )
        ], className="campo-salud"),
    
        html.Div([
            html.Label("Sexo:"),
            dcc.Dropdown(
                id="filtro-sexo",
                options=[{"label": "Todos", "value": "Todos"}]
                + opciones_sexos,
                value="Todos",
                clearable=False
            )
        ], className="campo-salud"),
    
        html.Div([
            html.Label("Grupo etario:"),
            dcc.Dropdown(
                id="filtro-grupo-etario",
                options=[{"label": "Todos", "value": "Todos"}]
                + [{"label": g, "value": g} for g in grupos_etarios],
                value="Todos",
                clearable=False
            )
        ], className="campo-salud")
        ], style={"maxWidth": "600px"}, className="filtros-salud"),

        # Tarjetas de indicadores
        
        html.Div([
            html.Div([
                html.H3("Prestaciones"),
                html.H2(id="indicador-prestaciones")
            ], style={"flex": "1", "backgroundColor": "#f0f4f8",
                      "padding": "20px", "borderRadius": "8px"}, className="kpi-salud"),
        
            html.Div([
                html.H3(
                    "Identificadores distintos",
                    title="Tipo de documento e identificador anonimizado. No equivale a personas únicas verificadas."
                ),
                html.H2(id="indicador-pacientes")
            ], style={"flex": "1", "backgroundColor": "#f0f4f8",
                      "padding": "20px", "borderRadius": "8px"}, className="kpi-salud"),
        
            html.Div([
                html.H3("Prestaciones por identificador"),
                html.H2(id="indicador-promedio")
            ], style={"flex": "1", "backgroundColor": "#f0f4f8",
                      "padding": "20px", "borderRadius": "8px"}, className="kpi-salud")
        ], style={"display": "flex", "gap": "15px", "marginTop": "25px"}, className="kpis-salud"),
              
        # Graficos
        
        html.Div([
            dcc.Graph(id="grafico-evolucion", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False}),
            dcc.Graph(id="grafico-diagnosticos", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False})
        ], className="fila-salud doble"),
        html.Div([
            dcc.Graph(id="grafico-cobertura-sexo", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False}),
            dcc.Graph(id="grafico-mapa-calor", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False})
        ], className="fila-salud doble")
        
    ], id="pagina-utilizacion", className="pagina-salud"),
    # segundo dashboard
    html.Div([
        html.H2("Gastos y copagos"),
        
        html.Div([
            html.Div([
                html.Label("Fecha de recepción:"),
                dcc.DatePickerRange(
                    id="filtro-fechas-gastos",
                    min_date_allowed=fecha_minima.date(),
                    max_date_allowed=fecha_maxima.date(),
                    start_date=fecha_minima.date(),
                    end_date=fecha_maxima.date()
                , display_format="DD/MM/YYYY")
            ], className="campo-salud"),

            html.Div([
                html.Label("Cobertura:"),
                dcc.Dropdown(
                    id="filtro-cobertura-gastos",
                    options=[{"label": "Todas", "value": "Todos"}]
                    + opciones_coberturas,
                    value="Todos",
                    clearable=False
                )
            ], className="campo-salud")
        ], className="filtros-salud tres"),
        
        html.Div([
            html.Div([
                html.H3("Monto total liquidado"),
                html.H2(id="indicador-monto-total")
            ], className="kpi-salud"),
        
            html.Div([
                html.H3("Monto promedio por prestación"),
                html.H2(id="indicador-monto-promedio")
            ], className="kpi-salud"),
        
            html.Div([
                html.H3("Copago promedio por prestación"),
                html.H2(id="indicador-copago-promedio")
            ], className="kpi-salud")
        ], className="kpis-salud"),

        html.Div([
            html.Div([
                html.Label("Medida a visualizar:"),
                dcc.Dropdown(
                    id="selector-monto",
                    options=[
                        {"label": "Monto total liquidado", "value": "total"},
                        {"label": "Monto promedio por prestación", "value": "promedio"}
                    ],
                    value="total",
                    clearable=False
                )
            ], className="campo-salud")
        ], className="filtros-salud uno"),

        html.Div([
            dcc.Graph(id="grafico-monto-mensual", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False}),
            dcc.Graph(id="grafico-monto-diagnostico", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False})
        ], className="fila-salud doble"),
        html.Div([
            dcc.Graph(id="grafico-composicion-gasto", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False})
        ], className="fila-salud"),
        html.Div([
            html.Div([
                html.Label("Cobertura para comparar IPRESS:"),
                dcc.Dropdown(id="filtro-cobertura-ipress", options=opciones_coberturas,
                             value=None, placeholder="Selecciona una cobertura", clearable=False)
            ], className="campo-salud"),
            html.Div([
                html.Label("Diagnóstico frecuente:"),
                dcc.Dropdown(id="filtro-diagnostico-gastos", options=[], value=None,
                             placeholder="Selecciona un diagnóstico", clearable=False)
            ], className="campo-salud"),
            html.Div([
                html.Label("Rango de montos:"),
                dcc.RadioItems(id="rango-montos-ipress", options=[
                    {"label": "Vista central (P95)", "value": "central"},
                    {"label": "Rango completo", "value": "completo"}
                ], value="central", inline=True)
            ], className="campo-salud")
        ], className="filtros-salud tres"),
        html.Div([
            dcc.Graph(id="grafico-distribucion-ipress", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False})
        ], className="fila-salud"),
        
        html.H3("Copagos por IAFAS y cobertura"),

        html.Div([
            dash_table.DataTable(
                id="tabla-copagos",
                columns=[
                    {"name": "IAFAS", "id": "IAFAS"},
                    {"name": "Cobertura", "id": "Cobertura"},
                    {"name": "Prestaciones", "id": "Prestaciones"},
                    {
                        "name": "Prestaciones con copago informado",
                        "id": "PrestacionesConCopago"
                    },
                    {
                        "name": "Copago promedio",
                        "id": "CopagoPromedio",
                        "type": "numeric"
                    }
                ],
                page_size=10,
                sort_action="native"
            , style_table={"overflowX":"auto"},
                style_header={"backgroundColor":"#E8F1E9", "color":"#245A4D", "fontWeight":"600",
                              "border":"none", "padding":"12px", "whiteSpace":"normal", "height":"auto"},
                style_cell={"fontFamily":"Segoe UI, Calibri, sans-serif", "fontSize":"13px", "textAlign":"left",
                            "padding":"11px 12px", "border":"none", "borderBottom":"1px solid #EDF1EB",
                            "minWidth":"105px", "whiteSpace":"normal", "height":"auto"},
                style_data_conditional=[{"if":{"row_index":"odd"}, "backgroundColor":"#FAFCF8"}],
                style_cell_conditional=[{"if":{"column_id": c}, "textAlign":"right"}
                                        for c in ["Prestaciones","PrestacionesConCopago","CopagoPromedio","MontoTotal","MontoPromedio"]])
        ], className="tabla-salud")
        
    ], id="pagina-gastos", style={"display": "none"}, className="pagina-salud"),
    # tercer dashboard
    html.Div([
        html.H2("Distribución geográfica y hospitalización"),

        html.Div([
            html.Div([
                html.Label("Fecha de recepción:"),
                dcc.DatePickerRange(
                    id="filtro-fechas-hospitalizacion",
                    min_date_allowed=fecha_minima.date(),
                    max_date_allowed=fecha_maxima.date(),
                    start_date=fecha_minima.date(),
                    end_date=fecha_maxima.date()
                , display_format="DD/MM/YYYY")
            ], className="campo-salud")
        ], className="filtros-salud uno"),
        
        html.H3("Distribución geográfica"),

        html.Div([
            dcc.Dropdown(
                id="selector-ubicacion",
                options=[
                    {"label": "Ubicación de la IPRESS", "value": "IPRESS"},
                    {"label": "Ubicación del afiliado", "value": "Afiliado"}
                ],
                value="IPRESS",
                clearable=False
            )
        ], className="filtros-salud uno"),

        html.Div([
            dash_table.DataTable(
                id="tabla-geografica",
                columns=[
                    {"name": "Ubigeo INEI", "id": "Ubigeo"},
                    {"name": "Departamento", "id": "Departamento"},
                    {"name": "Provincia", "id": "Provincia"},
                    {"name": "Distrito", "id": "Distrito"},
                    {
                        "name": "Prestaciones",
                        "id": "Prestaciones",
                        "type": "numeric"
                    },
                    {
                        "name": "Monto total liquidado",
                        "id": "MontoTotal",
                        "type": "numeric"
                    },
                    {
                        "name": "Monto promedio liquidado",
                        "id": "MontoPromedio",
                        "type": "numeric"
                    }
                ],
                page_size=10,
                sort_action="native"
            , style_table={"overflowX":"auto"},
                style_header={"backgroundColor":"#E8F1E9", "color":"#245A4D", "fontWeight":"600",
                              "border":"none", "padding":"12px", "whiteSpace":"normal", "height":"auto"},
                style_cell={"fontFamily":"Segoe UI, Calibri, sans-serif", "fontSize":"13px", "textAlign":"left",
                            "padding":"11px 12px", "border":"none", "borderBottom":"1px solid #EDF1EB",
                            "minWidth":"105px", "whiteSpace":"normal", "height":"auto"},
                style_data_conditional=[{"if":{"row_index":"odd"}, "backgroundColor":"#FAFCF8"}],
                style_cell_conditional=[{"if":{"column_id": c}, "textAlign":"right"}
                                        for c in ["Prestaciones","PrestacionesConCopago","CopagoPromedio","MontoTotal","MontoPromedio"]])
        ], className="tabla-salud"),
        
        html.H3("Prestaciones hospitalarias"),

        html.Div([
            html.Div([
                html.H4("Prestaciones hospitalarias"),
                html.H2(id="indicador-hospitalarias")
            ], className="kpi-salud"),

            html.Div([
                html.H4("Promedio de días de estancia facturable"),
                html.H2(id="indicador-dias-estancia")
            ], className="kpi-salud"),

            html.Div([
                html.H4("Monto promedio por prestación hospitalaria"),
                html.H2(id="indicador-monto-hospitalario")
            ], className="kpi-salud")
        ], className="kpis-salud"),

        html.Div([
            dcc.Graph(id="grafico-estancia-diagnostico", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False})
        ], className="fila-salud"),
        html.Div([
            html.Div([
                html.Label("Diagnóstico hospitalario frecuente:"),
                dcc.Dropdown(id="filtro-diagnostico-hospitalizacion", options=[], value=None,
                             placeholder="Selecciona un diagnóstico", clearable=False)
            ], className="campo-salud")
        ], className="filtros-salud uno"),
        html.Div([
            dcc.Graph(id="grafico-estancia-tipo", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False})
        ], className="fila-salud"),
        html.Div([
            html.Div([
                html.Label("Diagnóstico hospitalario frecuente:"),
                dcc.Dropdown(id="filtro-diagnostico-relacion", options=[], value=None,
                             placeholder="Selecciona un diagnóstico", clearable=False)
            ], className="campo-salud")
        ], className="filtros-salud uno"),
        html.Div([
            dcc.Graph(id="grafico-estancia-monto", className="grafico-salud", responsive=True, style={"height": "460px", "minWidth": 0}, config={"displaylogo": False})
        ], className="fila-salud")

    ], id="pagina-hospitalizacion", style={"display": "none"}, className="pagina-salud"),


], style={"padding": "25px", "fontFamily": "Arial"}, className="app-salud")

# ==========================
# %% CALLBACK: ACTUALIZACIONES
# ==========================

# para el dashboard de utilizacion

@app.callback(
    [
        Output("indicador-prestaciones", "children"),
        Output("indicador-pacientes", "children"),
        Output("indicador-promedio", "children"),
        Output("grafico-evolucion", "figure"),
        Output("grafico-diagnosticos", "figure"),
        Output("grafico-cobertura-sexo", "figure"),
        Output("grafico-mapa-calor", "figure")
    ],
    [
        Input("filtro-fechas", "start_date"),
        Input("filtro-fechas", "end_date"),
        Input("filtro-cobertura", "value"),
        Input("filtro-sexo", "value"),
        Input("filtro-grupo-etario", "value")
    ]
)

def update_dashboard(inicio, fin, cobertura, sexo, grupo_etario):
    df = df_full[['FechaRecepcion', 'RangoAntiguedad', 'CodigoTipoCobertura', 'CodigoSexo', 'GrupoEtario', 'TipoDocumentoIdentidad', 'PacienteAnonimizado', 'CodigoDiagnosticoCIE10']].copy()

    # Aplicar filtros
    if inicio:
        df = df[df["FechaRecepcion"] >= pd.to_datetime(inicio)]

    if fin:
        df = df[
            df["FechaRecepcion"] < pd.to_datetime(fin) + pd.Timedelta(days=1)
        ]

    if cobertura != "Todos":
        df = df[df["CodigoTipoCobertura"] == cobertura]

    if sexo != "Todos":
        df = df[df["CodigoSexo"] == sexo]

    if grupo_etario != "Todos":
        df = df[df["GrupoEtario"] == grupo_etario]

    # Calcular indicadores sobre los datos filtrados
    indicadores = calcular_indicadores_utilizacion(df)

    promedio = indicadores["PrestacionesPorIdentificador"]

    texto_promedio = (
        f"{promedio:.2f}" if promedio is not None else "No disponible"
    )
    
    # Agrupar las prestaciones filtradas por mes
    # La serie histórica se sustituye por antigüedad dentro de la ventana de recepción.
    datos_linea = (
        df["RangoAntiguedad"].value_counts(sort=False)
        .reindex(RANGOS_ANTIGUEDAD, fill_value=0)
        .rename_axis("Antiguedad").reset_index(name="CantidadPrestaciones")
    )
    total = datos_linea["CantidadPrestaciones"].sum()
    datos_linea["Porcentaje"] = datos_linea["CantidadPrestaciones"] / total * 100 if total else 0

    # Crear el gráfico de lineas
    # Se utilizan barras porque se comparan intervalos de antigüedad.
    fig_evolucion = px.bar(
        datos_linea, x="Antiguedad", y="CantidadPrestaciones", text="CantidadPrestaciones",
        hover_data={"Porcentaje": ":.1f"},
        title="Antigüedad de las prestaciones al recibirse",
        labels={"Antiguedad": "Días entre prestación y recepción",
                "CantidadPrestaciones": "Prestaciones", "Porcentaje": "Participación (%)"},
        template="plotly_white"
    )

    # Contar prestaciones por diagnóstico
    datos_diagnosticos = (
        df["CodigoDiagnosticoCIE10"]
        .dropna()
        .value_counts()
        .head(10)
        .rename_axis("Diagnostico")
        .reset_index(name="CantidadPrestaciones")
    )

    datos_diagnosticos["DescripcionDiagnostico"] = (
        datos_diagnosticos["Diagnostico"].map(nombres_diagnosticos)
    )

    # Crear el gráfico de barras horizontales
    fig_diagnosticos = px.bar(
        datos_diagnosticos,
        x="CantidadPrestaciones",
        y="Diagnostico",
        orientation="h",
        text="CantidadPrestaciones",
        hover_data={"DescripcionDiagnostico": True},
        title="Diez diagnósticos con más prestaciones",
        labels={
            "CantidadPrestaciones": "Cantidad de prestaciones",
            "Diagnostico": "Diagnóstico CIE-10",
            "DescripcionDiagnostico": "Descripción"
        },
        template="plotly_white"
    )
    
    fig_diagnosticos.update_yaxes(
        type="category",
        categoryorder="total ascending"
    )
    
    # Preparar categorías sin información
    datos_cobertura = df[
        ["CodigoTipoCobertura", "CodigoSexo"]
    ].copy().fillna("Sin información")

    # Contar prestaciones por cobertura y sexo
    datos_cobertura = (
        datos_cobertura
        .groupby(["CodigoTipoCobertura", "CodigoSexo"])
        .size()
        .reset_index(name="CantidadPrestaciones")
    )

    datos_cobertura["Cobertura"] = (
        datos_cobertura["CodigoTipoCobertura"]
        .map(nombres_coberturas).fillna("Sin información")
    )
    datos_cobertura["Sexo"] = (
        datos_cobertura["CodigoSexo"]
        .map(nombres_sexos).fillna("Sin información")
    )

    # Crear las barras apiladas
    fig_cobertura = px.bar(
        datos_cobertura,
        x="Cobertura",
        y="CantidadPrestaciones",
        color="Sexo",
        barmode="stack",
        title="Prestaciones por cobertura y sexo",
        labels={
            "Cobertura": "Cobertura",
            "CantidadPrestaciones": "Cantidad de prestaciones",
            "Sexo": "Sexo"
        },
        template="plotly_white"
    )

    fig_cobertura.update_xaxes(type="category")
    
    # Seleccionar los diez diagnósticos más frecuentes
    top_diagnosticos = datos_diagnosticos["Diagnostico"].tolist()
    
    datos_calor = df[
        df["CodigoDiagnosticoCIE10"].isin(top_diagnosticos)
    ]
    
    # Contar prestaciones por diagnóstico y grupo etario
    matriz_calor = pd.crosstab(
        datos_calor["CodigoDiagnosticoCIE10"],
        datos_calor["GrupoEtario"]
    )
    
    matriz_calor = matriz_calor.reindex(
        index=top_diagnosticos,
        columns=grupos_etarios,
        fill_value=0
    )

    # Crear el mapa de calor
    fig_calor = px.imshow(
        matriz_calor,
        labels={
            "x": "Grupo etario",
            "y": "Diagnóstico CIE-10",
            "color": "Prestaciones"
        },
        title="Prestaciones por diagnóstico y grupo etario",
        color_continuous_scale="Blues",
        aspect="auto"
    )
    
    fig_calor.update_layout(template="plotly_white")
    fig_calor.update_traces(
        customdata=[
            [nombres_diagnosticos.get(codigo, str(codigo)) for _ in matriz_calor.columns]
            for codigo in matriz_calor.index
        ],
        hovertemplate=(
            "%{y}: %{customdata}<br>Grupo etario: %{x}"
            "<br>Prestaciones: %{z}<extra></extra>"
        )
    )

    formato_grafico(fig_evolucion)
    formato_grafico(fig_diagnosticos)
    formato_grafico(fig_cobertura, COLORES_SEXO)
    formato_grafico(fig_calor)
    mostrar_nombres_diagnosticos(fig_diagnosticos, datos_diagnosticos["Diagnostico"])
    mostrar_nombres_diagnosticos(fig_calor, top_diagnosticos)
    
    return (
        indicadores["TotalPrestaciones"],
        indicadores["IdentificadoresDistintos"],
        texto_promedio,
        fig_evolucion,
        fig_diagnosticos,
        fig_cobertura,
        fig_calor
    )

# para elegir el dashboard

@app.callback(
    [
        Output("pagina-utilizacion", "style"),
        Output("pagina-gastos", "style"),
        Output("pagina-hospitalizacion", "style")
    ],
    [Input("selector-dashboard", "value")]
)

def cambiar_pagina(pagina):
    visible = {"display": "block"}
    oculto = {"display": "none"}

    return (
        visible if pagina == "utilizacion" else oculto,
        visible if pagina == "gastos" else oculto,
        visible if pagina == "hospitalizacion" else oculto
    )

# para el dashboard de gastos

@app.callback(
    [
        Output("indicador-monto-total", "children"),
        Output("indicador-monto-promedio", "children"),
        Output("indicador-copago-promedio", "children"),
        Output("grafico-monto-mensual", "figure"),
        Output("grafico-monto-diagnostico", "figure"),
        Output("grafico-composicion-gasto", "figure"),
        Output("tabla-copagos", "data")
    ],
    [
        Input("selector-monto", "value"),
        Input("filtro-cobertura-gastos", "value"),
        Input("filtro-fechas-gastos", "start_date"),
        Input("filtro-fechas-gastos", "end_date")
    ]
)

def actualizar_gastos(medida, cobertura, inicio, fin):
    df = df_full[['FechaRecepcion', 'CodigoDiagnosticoCIE10', 'CodigoTipoCobertura', 'EtiquetaIPRESS', 'EtiquetaIAFAS'] + columnas_montos + columnas_gastos].copy()

    # Aplicar filtros
    if inicio:
        df = df[
            df["FechaRecepcion"] >= pd.to_datetime(inicio)
        ]

    if fin:
        df = df[
            df["FechaRecepcion"]
            < pd.to_datetime(fin) + pd.Timedelta(days=1)
        ]

    if cobertura != "Todos":
        df = df[df["CodigoTipoCobertura"] == cobertura]

    # Calcular indicadores con los datos filtrados
    indicadores = calcular_indicadores_gastos(df)

    texto_total = (
        f'{indicadores["MontoTotalLiquidado"]:,.2f}'
        if pd.notna(indicadores["MontoTotalLiquidado"])
        else "No disponible"
    )

    texto_promedio = (
        f'{indicadores["MontoPromedioLiquidado"]:,.2f}'
        if pd.notna(indicadores["MontoPromedioLiquidado"])
        else "No disponible"
    )

    texto_copago = (
        f'{indicadores["CopagoPromedio"]:,.2f}'
        if pd.notna(indicadores["CopagoPromedio"])
        else "No disponible"
    )

    # Preparar evolución mensual sin modificar df
    datos_temporales = df.dropna(
        subset=["FechaRecepcion"]
    ).copy()

    datos_temporales["Mes"] = (
        datos_temporales["FechaRecepcion"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    agrupacion = datos_temporales.groupby(
        "Mes"
    )["TotalLiquidadoIAFAS"]

    if medida == "total":
        datos_monto = agrupacion.sum(min_count=1)
        titulo = "Monto liquidado por mes de recepción"
        etiqueta = "Monto total liquidado"
    else:
        datos_monto = agrupacion.mean()
        titulo = "Monto promedio por prestación y mes de recepción"
        etiqueta = "Monto promedio liquidado"

    datos_monto = (
        datos_monto.reset_index(name="Monto")
        .sort_values("Mes")
    )

    fig_monto = px.bar(
        datos_monto,
        x="Mes",
        y="Monto",
        title=titulo,
        labels={
            "Mes": "Mes de recepción",
            "Monto": etiqueta
        },
        template="plotly_white"
    )

    # Agrupar montos por diagnóstico
    agrupacion_diagnostico = df.groupby(
        "CodigoDiagnosticoCIE10"
    )["TotalLiquidadoIAFAS"]

    if medida == "total":
        datos_diagnostico = agrupacion_diagnostico.sum(min_count=1)
        titulo_diagnostico = "Diez diagnósticos con mayor monto total liquidado"
        etiqueta_monto = "Monto total liquidado"
    else:
        datos_diagnostico = agrupacion_diagnostico.mean().where(
            agrupacion_diagnostico.count() >= MINIMO_PRESTACIONES
        )
        titulo_diagnostico = "Mayor monto promedio por diagnóstico (mín. 10 prestaciones)"
        etiqueta_monto = "Monto promedio por prestación"

    datos_diagnostico = (
        datos_diagnostico
        .dropna()
        .nlargest(10)
        .rename_axis("Diagnostico")
        .reset_index(name="Monto")
    )

    cantidades_diagnostico = agrupacion_diagnostico.count()

    datos_diagnostico["PrestacionesConMonto"] = (
        datos_diagnostico["Diagnostico"]
        .map(cantidades_diagnostico)
    )

    datos_diagnostico["DescripcionDiagnostico"] = (
        datos_diagnostico["Diagnostico"].map(nombres_diagnosticos)
    )

    fig_monto_diagnostico = px.bar(
        datos_diagnostico,
        x="Monto",
        y="Diagnostico",
        orientation="h",
        title=titulo_diagnostico + "",
        labels={
            "Diagnostico": "Diagnóstico CIE-10",
            "Monto": etiqueta_monto,
            "PrestacionesConMonto": "Prestaciones con monto informado",
            "DescripcionDiagnostico": "Descripción"
        },
        hover_data={
            "Monto": ":,.2f",
            "PrestacionesConMonto": True,
            "DescripcionDiagnostico": True
        },
        template="plotly_white"
    )

    fig_monto_diagnostico.update_yaxes(
        type="category",
        categoryorder="total ascending"
    )

    # Calcular la composición con los datos filtrados
    resultados_composicion = []

    for codigo_cobertura, grupo in df.groupby(
        "CodigoTipoCobertura",
        dropna=False
    ):
        composicion = calcular_composicion(
            grupo,
            columnas_gastos
        )

        composicion["Cobertura"] = (
            nombres_coberturas.get(codigo_cobertura, str(codigo_cobertura))
            if pd.notna(codigo_cobertura)
            else "Sin información"
        )

        resultados_composicion.append(composicion)

    if resultados_composicion:
        datos_composicion = pd.concat(
            resultados_composicion,
            ignore_index=True
        )
    else:
        datos_composicion = pd.DataFrame({
            "Componente": pd.Series(dtype="str"),
            "Monto": pd.Series(dtype="float"),
            "Porcentaje": pd.Series(dtype="float"),
            "Cobertura": pd.Series(dtype="str")
        })

    datos_composicion["Componente"] = (
        datos_composicion["Componente"].map(ETIQUETAS_GASTOS)
    )

    fig_composicion = px.bar(
        datos_composicion,
        x="Cobertura",
        y="Porcentaje",
        color="Componente",
        barmode="stack",
        title="Composición del gasto por cobertura",
        labels={
            "Cobertura": "Cobertura",
            "Porcentaje": "Participación del gasto (%)",
            "Componente": "Componente del gasto"
        },
        hover_data={"Monto": ":,.2f", "Porcentaje": ":.2f"},
        template="plotly_white"
    )

    fig_composicion.update_xaxes(type="category")
    fig_composicion.update_yaxes(range=[0, 100])

    # Mostrar un mensaje cuando la selección no tenga registros
    if df.empty:
        for figura in [
            fig_monto,
            fig_monto_diagnostico,
            fig_composicion
        ]:
            figura.add_annotation(
                text="Sin datos para la selección",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False
            )

    # Calcular copago por prestación
    columnas_copago = [
        "CopagoFijoAfectoSinIGV",
        "CopagoFijoExonerado",
        "CopagoVariableAfectoSinIGV",
        "CopagoVariableExonerado"
    ]

    datos_copagos = df.copy()

    datos_copagos["CopagoPrestacion"] = (
        datos_copagos[columnas_copago].sum(axis=1, min_count=4)
    )

    datos_copagos["IAFAS"] = (
        datos_copagos["EtiquetaIAFAS"].fillna("Sin información")
    )

    datos_copagos["Cobertura"] = (
        datos_copagos["CodigoTipoCobertura"]
        .map(nombres_coberturas).fillna("Sin información")
    )

    tabla_copagos = (
        datos_copagos.groupby(["IAFAS", "Cobertura"])
        .agg(
            Prestaciones=("CopagoPrestacion", "size"),
            PrestacionesConCopago=("CopagoPrestacion", "count"),
            CopagoPromedio=("CopagoPrestacion", "mean")
        )
        .reset_index()
    )

    tabla_copagos["CopagoPromedio"] = (
        tabla_copagos["CopagoPromedio"].round(2)
    )

    registros_copagos = (
        tabla_copagos.astype(object)
        .where(tabla_copagos.notna(), None)
        .to_dict("records")
    )

    formato_grafico(fig_monto)
    formato_grafico(fig_monto_diagnostico)
    formato_grafico(fig_composicion, COLORES_GASTO)
    mostrar_nombres_diagnosticos(fig_monto_diagnostico, datos_diagnostico["Diagnostico"])
    
    return (
        texto_total,
        texto_promedio,
        texto_copago,
        fig_monto,
        fig_monto_diagnostico,
        fig_composicion,
        registros_copagos
    )


@app.callback(
    [Output("filtro-cobertura-ipress", "options"), Output("filtro-cobertura-ipress", "value")],
    Input("filtro-cobertura-gastos", "value"),
    State("filtro-cobertura-ipress", "value")
)
def sincronizar_cobertura_ipress(cobertura_general, seleccion):
    if cobertura_general != "Todos":
        opciones = [o for o in opciones_coberturas if o["value"] == cobertura_general]
        return opciones, cobertura_general if opciones else None
    return opciones_coberturas, seleccion if seleccion in nombres_coberturas else None


@app.callback(
    [Output("filtro-diagnostico-gastos", "options"), Output("filtro-diagnostico-gastos", "value")],
    [Input("filtro-fechas-gastos", "start_date"), Input("filtro-fechas-gastos", "end_date"),
     Input("filtro-cobertura-ipress", "value")],
    State("filtro-diagnostico-gastos", "value")
)
def actualizar_opciones_ipress(inicio, fin, cobertura, seleccion):
    if cobertura is None:
        return [], None
    datos = filtrar_recepcion(df_full[["FechaRecepcion", "CodigoTipoCobertura",
                                      "CodigoDiagnosticoCIE10", "TotalLiquidadoIAFAS"]], inicio, fin)
    datos = datos[datos["CodigoTipoCobertura"] == cobertura].dropna(subset=["TotalLiquidadoIAFAS"])
    return opciones_diagnosticos_frecuentes(datos, seleccion)


@app.callback(
    Output("grafico-distribucion-ipress", "figure"),
    [Input("filtro-diagnostico-gastos", "value"), Input("filtro-cobertura-ipress", "value"),
     Input("rango-montos-ipress", "value"), Input("filtro-fechas-gastos", "start_date"),
     Input("filtro-fechas-gastos", "end_date")]
)
def actualizar_comparacion_ipress(diagnostico, cobertura, rango, inicio, fin):
    titulo = "Distribución de montos por IPRESS"
    if diagnostico is None or cobertura is None:
        return figura_sin_datos(titulo, "Selecciona una cobertura y un diagnóstico")

    datos_caja = filtrar_recepcion(df_full[["FechaRecepcion", "CodigoDiagnosticoCIE10",
        "CodigoTipoCobertura", "EtiquetaIPRESS", "TotalLiquidadoIAFAS"]], inicio, fin)
    datos_caja = datos_caja[
        (datos_caja["CodigoDiagnosticoCIE10"] == diagnostico)
        & (datos_caja["CodigoTipoCobertura"] == cobertura)
    ].dropna(subset=["EtiquetaIPRESS", "TotalLiquidadoIAFAS"])

    # Seleccionar prestaciones con IPRESS y monto informados
    # Limitar a las ocho IPRESS con más prestaciones
    cantidades = datos_caja["EtiquetaIPRESS"].value_counts()
    cantidades = cantidades[cantidades >= MINIMO_PRESTACIONES].head(8)
    principales_ipress = cantidades.index.tolist()
    datos_caja = datos_caja[datos_caja["EtiquetaIPRESS"].isin(principales_ipress)].copy()
    if datos_caja.empty:
        return figura_sin_datos(titulo, "Sin IPRESS con al menos 10 prestaciones para la selección")

    datos_caja["PrestacionesIPRESS"] = datos_caja["EtiquetaIPRESS"].map(cantidades)
    fig_caja = px.box(
        datos_caja, x="EtiquetaIPRESS", y="TotalLiquidadoIAFAS", points="outliers",
        category_orders={"EtiquetaIPRESS": principales_ipress},
        hover_data={"PrestacionesIPRESS": True}, title=titulo,
        labels={"EtiquetaIPRESS": "Establecimiento",
                "TotalLiquidadoIAFAS": "Monto liquidado por prestación (S/)",
                "PrestacionesIPRESS": "Prestaciones de la IPRESS"}, template="plotly_white"
    )
    formato_grafico(fig_caja)
    fig_caja.update_xaxes(tickmode="array", tickvals=principales_ipress,
        ticktext=[f"{codigo}<br>n={cantidades[codigo]:,}" for codigo in principales_ipress])

    if rango == "central":
        minimo = min(0, float(datos_caja["TotalLiquidadoIAFAS"].min()))
        limite = float(datos_caja["TotalLiquidadoIAFAS"].quantile(0.95))
        margen = max((limite - minimo) * 0.06, 1)
        fig_caja.update_yaxes(range=[minimo - margen, limite + margen])
        fig_caja.add_annotation(text=f"Vista central · P95: S/ {limite:,.2f}",
            x=1, y=1.07, xref="paper", yref="paper", showarrow=False, xanchor="right",
            font=dict(size=11))

    return fig_caja

# para el dashboard de hospitalizacion

# Incorporar etiquetas para los tipos de hospitalización
# Distribución de días por tipo de hospitalización
# Usar prestaciones con días válidos y monto informado
# Exigir un diagnóstico para mantener la comparación
@app.callback(
    [Output("indicador-hospitalarias", "children"), Output("indicador-dias-estancia", "children"),
     Output("indicador-monto-hospitalario", "children"), Output("grafico-estancia-diagnostico", "figure")],
    [Input("filtro-fechas-hospitalizacion", "start_date"), Input("filtro-fechas-hospitalizacion", "end_date")]
)
def actualizar_hospitalizacion(inicio, fin):
    df = filtrar_recepcion(df_full[["FechaRecepcion", "CodigoDiagnosticoCIE10", "CodigoTipoHospitalizacion",
        "DiasEstanciaFacturable", "TotalLiquidadoIAFAS"]], inicio, fin)
    # Calcular indicadores
    indicadores = calcular_indicadores_hospitalizacion(df)
    dias, monto = indicadores["PromedioDiasEstancia"], indicadores["MontoPromedioHospitalario"]
    texto_dias = f"{dias:.2f}" if pd.notna(dias) else "No disponible"
    texto_monto = f"{monto:,.2f}" if pd.notna(monto) else "No disponible"
    # Seleccionar prestaciones hospitalarias
    hospitalarias = df[df["CodigoTipoHospitalizacion"].isin(["C", "Q"])]
    # Seleccionar días informados y no negativos
    estancias_validas = hospitalarias[hospitalarias["DiasEstanciaFacturable"].notna()
                                     & hospitalarias["DiasEstanciaFacturable"].ge(0)]
    # Calcular promedio y cantidad por diagnóstico
    datos_estancia = estancias_validas.groupby("CodigoDiagnosticoCIE10").agg(
        PromedioDias=("DiasEstanciaFacturable", "mean"),
        PrestacionesConDias=("DiasEstanciaFacturable", "count")
    ).reset_index()
    datos_estancia = datos_estancia[datos_estancia["PrestacionesConDias"] >= MINIMO_PRESTACIONES].nlargest(10, "PromedioDias")
    datos_estancia["DescripcionDiagnostico"] = datos_estancia["CodigoDiagnosticoCIE10"].map(nombres_diagnosticos)
    fig_estancia = px.bar(datos_estancia, x="PromedioDias", y="CodigoDiagnosticoCIE10", orientation="h",
        hover_data={"PrestacionesConDias": True, "DescripcionDiagnostico": True},
        title="Mayor estancia promedio por diagnóstico (mín. 10 prestaciones)",
        labels={"PromedioDias": "Días facturables promedio", "CodigoDiagnosticoCIE10": "Diagnóstico",
                "PrestacionesConDias": "Prestaciones con días informados", "DescripcionDiagnostico": "Descripción"},
        template="plotly_white")
    fig_estancia.update_yaxes(type="category", categoryorder="total ascending")
    if datos_estancia.empty:
        fig_estancia.add_annotation(text="Sin diagnósticos con al menos 10 prestaciones", x=0.5, y=0.5,
            xref="paper", yref="paper", showarrow=False)
    formato_grafico(fig_estancia)
    mostrar_nombres_diagnosticos(fig_estancia, datos_estancia["CodigoDiagnosticoCIE10"])
    return indicadores["PrestacionesHospitalarias"], texto_dias, texto_monto, fig_estancia

def datos_hospitalarios(inicio, fin):
    datos = filtrar_recepcion(df_full[["FechaRecepcion", "CodigoDiagnosticoCIE10", "CodigoTipoHospitalizacion",
        "DescripcionTipoHospitalizacion", "DiasEstanciaFacturable", "TotalLiquidadoIAFAS"]], inicio, fin)
    return datos[datos["CodigoTipoHospitalizacion"].isin(["C", "Q"])
                 & datos["DiasEstanciaFacturable"].notna() & datos["DiasEstanciaFacturable"].ge(0)]


@app.callback(
    [Output("filtro-diagnostico-hospitalizacion", "options"), Output("filtro-diagnostico-hospitalizacion", "value"),
     Output("filtro-diagnostico-relacion", "options"), Output("filtro-diagnostico-relacion", "value")],
    [Input("filtro-fechas-hospitalizacion", "start_date"), Input("filtro-fechas-hospitalizacion", "end_date")],
    [State("filtro-diagnostico-hospitalizacion", "value"), State("filtro-diagnostico-relacion", "value")]
)
def actualizar_opciones_hospitalarias(inicio, fin, seleccion_estancia, seleccion_relacion):
    datos = datos_hospitalarios(inicio, fin)
    opciones_estancia, valor_estancia = opciones_diagnosticos_frecuentes(datos, seleccion_estancia)
    opciones_relacion, valor_relacion = opciones_diagnosticos_frecuentes(
        datos.dropna(subset=["TotalLiquidadoIAFAS"]), seleccion_relacion)
    return opciones_estancia, valor_estancia, opciones_relacion, valor_relacion


@app.callback(
    Output("grafico-estancia-tipo", "figure"),
    [Input("filtro-diagnostico-hospitalizacion", "value"), Input("filtro-fechas-hospitalizacion", "start_date"),
     Input("filtro-fechas-hospitalizacion", "end_date")]
)
def actualizar_distribucion_estancia(diagnostico, inicio, fin):
    titulo = "Distribución de la estancia facturable"
    if diagnostico is None:
        return figura_sin_datos(titulo, "Selecciona un diagnóstico hospitalario")
    datos = datos_hospitalarios(inicio, fin)
    datos = datos[datos["CodigoDiagnosticoCIE10"] == diagnostico].copy()
    if len(datos) < MINIMO_PRESTACIONES:
        return figura_sin_datos(titulo, "Se requieren al menos 10 prestaciones con días informados")
    # Incorporar etiquetas para los tipos de hospitalización
    datos["TipoHospitalizacion"] = datos["DescripcionTipoHospitalizacion"].astype("string")
    datos["RangoEstancia"] = pd.cut(datos["DiasEstanciaFacturable"],
        bins=[-1, 1, 3, 7, 14, 30, np.inf], labels=RANGOS_ESTANCIA)
    # Distribución de días por tipo de hospitalización
    distribucion = datos.groupby(["TipoHospitalizacion", "RangoEstancia"], observed=False).size().reset_index(name="Prestaciones")
    distribucion["TotalTipo"] = distribucion.groupby("TipoHospitalizacion")["Prestaciones"].transform("sum")
    distribucion["Porcentaje"] = distribucion["Prestaciones"] / distribucion["TotalTipo"] * 100
    figura = px.bar(distribucion, x="RangoEstancia", y="Porcentaje", color="TipoHospitalizacion", barmode="group",
        title=titulo, category_orders={"RangoEstancia": RANGOS_ESTANCIA},
        hover_data={"Prestaciones": True, "TotalTipo": True, "Porcentaje": ":.1f"},
        labels={"RangoEstancia": "Días de estancia facturable", "Porcentaje": "Prestaciones de cada tipo (%)",
                "TipoHospitalizacion": "Hospitalización", "TotalTipo": "Prestaciones del tipo"}, template="plotly_white")
    formato_grafico(figura)
    return figura


@app.callback(
    Output("grafico-estancia-monto", "figure"),
    [Input("filtro-diagnostico-relacion", "value"), Input("filtro-fechas-hospitalizacion", "start_date"),
     Input("filtro-fechas-hospitalizacion", "end_date")]
)
def actualizar_relacion_estancia(diagnostico, inicio, fin):
    titulo = "Estancia y monto promedio liquidado"
    if diagnostico is None:
        return figura_sin_datos(titulo, "Selecciona un diagnóstico hospitalario")
    # Usar prestaciones con días válidos y monto informado
    datos = datos_hospitalarios(inicio, fin)
    datos = datos[datos["CodigoDiagnosticoCIE10"] == diagnostico].dropna(subset=["TotalLiquidadoIAFAS"])
    if len(datos) < MINIMO_PRESTACIONES:
        return figura_sin_datos(titulo, "Se requieren al menos 10 prestaciones con días y monto")
    # Exigir un diagnóstico para mantener la comparación
    datos_relacion = datos.groupby("DiasEstanciaFacturable").agg(
        MontoPromedio=("TotalLiquidadoIAFAS", "mean"), CantidadPrestaciones=("TotalLiquidadoIAFAS", "count")
    ).reset_index()
    figura = px.scatter(datos_relacion, x="DiasEstanciaFacturable", y="MontoPromedio", size="CantidadPrestaciones",
        size_max=28, hover_data={"CantidadPrestaciones": True}, title=titulo,
        labels={"DiasEstanciaFacturable": "Días de estancia facturable", "MontoPromedio": "Monto promedio liquidado (S/)",
                "CantidadPrestaciones": "Prestaciones representadas"}, template="plotly_white")
    # Ajustar sobre las prestaciones individuales, no sobre promedios con el mismo peso.
    x = datos["DiasEstanciaFacturable"].to_numpy(dtype=float)
    y = datos["TotalLiquidadoIAFAS"].to_numpy(dtype=float)
    if np.unique(x).size >= 2:
        centrado = x - x.mean()
        pendiente = np.sum(centrado * (y - y.mean())) / np.sum(centrado ** 2)
        intercepto = y.mean() - pendiente * x.mean()
        extremos = np.array([x.min(), x.max()])
        figura.add_trace(go.Scatter(x=extremos, y=intercepto + pendiente * extremos, mode="lines",
            name="Tendencia lineal", line=dict(color="#CA9E59", dash="dash", width=2),
            hovertemplate="Tendencia descriptiva<extra></extra>"))
    else:
        figura.add_annotation(text="Sin variación de días para ajustar tendencia", x=0.5, y=1.04,
            xref="paper", yref="paper", showarrow=False, font=dict(size=11))
    formato_grafico(figura)
    return figura


@app.callback(
    Output("tabla-geografica", "data"),
    [
        Input("selector-ubicacion", "value"),
        Input("filtro-fechas-hospitalizacion", "start_date"),
        Input("filtro-fechas-hospitalizacion", "end_date")
    ]
)

def actualizar_geografia(origen, inicio, fin):
    if origen not in ["IPRESS", "Afiliado"]:
        raise ValueError("Selecciona la ubicación de la IPRESS o del afiliado.")

    columna_ubicacion = "UbigeoIPRESS" if origen == "IPRESS" else "UbigeoAfiliadoINEI"
    df = df_full[[
        "FechaRecepcion", columna_ubicacion,
        f"Departamento{origen}", f"Provincia{origen}", f"Distrito{origen}",
        "TotalLiquidadoIAFAS"
    ]].copy()

    if inicio:
        df = df[
            df["FechaRecepcion"] >= pd.to_datetime(inicio)
        ]

    if fin:
        df = df[
            df["FechaRecepcion"]
            < pd.to_datetime(fin) + pd.Timedelta(days=1)
        ]
    columna_ubigeo = (
        "UbigeoIPRESS"
        if origen == "IPRESS"
        else "UbigeoAfiliadoINEI"
    )

    columnas = [
        columna_ubigeo,
        f"Departamento{origen}",
        f"Provincia{origen}",
        f"Distrito{origen}",
        "TotalLiquidadoIAFAS"
    ]

    datos_geograficos = df[columnas].copy()

    datos_geograficos.columns = [
        "Ubigeo",
        "Departamento",
        "Provincia",
        "Distrito",
        "Monto"
    ]

    campos_ubicacion = [
        "Ubigeo", "Departamento", "Provincia", "Distrito"
    ]

    datos_geograficos[campos_ubicacion] = (
        datos_geograficos[campos_ubicacion]
        .astype("string")
        .fillna("Sin información")
    )

    tabla_geografica = (
        datos_geograficos.groupby(campos_ubicacion)
        .agg(
            Prestaciones=("Monto", "size"),
            MontoTotal=("Monto", lambda valores: valores.sum(min_count=1)),
            MontoPromedio=("Monto", "mean")
        )
        .reset_index()
        .sort_values("Prestaciones", ascending=False)
    )

    tabla_geografica[["MontoTotal", "MontoPromedio"]] = (
        tabla_geografica[["MontoTotal", "MontoPromedio"]].round(2)
    )

    return (
        tabla_geografica.astype(object)
        .where(tabla_geografica.notna(), None)
        .to_dict("records")
    )

# ==========================
# EJECUTAR LA APLICACIÓN
# ==========================

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
