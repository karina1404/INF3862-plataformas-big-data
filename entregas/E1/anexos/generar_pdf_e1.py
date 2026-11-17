"""Genera entregas/E1/informe.pdf (3 páginas) y anexos/A3_diagramas.pdf."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[3]
E1 = ROOT / "entregas" / "E1"
ANEXOS = E1 / "anexos"
AZUL = colors.HexColor("#1F4E79")
AZUL_C = colors.HexColor("#D6E3F0")
GRIS = colors.HexColor("#F4F6F8")
LINEA = colors.HexColor("#8AA0B8")


def styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            "Cover",
            parent=s["Normal"],
            fontName="Times-Bold",
            fontSize=13,
            leading=16,
            alignment=TA_CENTER,
            textColor=AZUL,
            spaceAfter=2,
        )
    )
    s.add(
        ParagraphStyle(
            "Meta",
            parent=s["Normal"],
            fontName="Times-Italic",
            fontSize=8.5,
            leading=11,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            "H",
            parent=s["Normal"],
            fontName="Times-Bold",
            fontSize=10.5,
            leading=13,
            textColor=AZUL,
            spaceBefore=7,
            spaceAfter=3,
        )
    )
    s.add(
        ParagraphStyle(
            "H2",
            parent=s["Normal"],
            fontName="Times-Bold",
            fontSize=9.5,
            leading=12,
            textColor=AZUL,
            spaceBefore=4,
            spaceAfter=2,
        )
    )
    s.add(
        ParagraphStyle(
            "B",
            parent=s["Normal"],
            fontName="Times-Roman",
            fontSize=9,
            leading=11.4,
            alignment=TA_JUSTIFY,
            spaceAfter=3,
        )
    )
    s.add(
        ParagraphStyle(
            "N",
            parent=s["Normal"],
            fontName="Times-Roman",
            fontSize=7.4,
            leading=9.2,
            alignment=TA_LEFT,
        )
    )
    s.add(
        ParagraphStyle(
            "Nh",
            parent=s["Normal"],
            fontName="Times-Bold",
            fontSize=7.2,
            leading=9,
            alignment=TA_CENTER,
            textColor=colors.white,
        )
    )
    s.add(
        ParagraphStyle(
            "Cap",
            parent=s["Normal"],
            fontName="Times-Italic",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            "Foot",
            parent=s["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#555555"),
        )
    )
    return s


def P(text, st):
    return Paragraph(text, st)


def tabla(headers, rows, col_w, sty, header=True):
    data = [[P(h, sty["Nh"]) for h in headers]] + [
        [P(c, sty["N"]) if not isinstance(c, Paragraph) else c for c in row] for row in rows
    ]
    t = Table(data, colWidths=col_w, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("GRID", (0, 0), (-1, -1), 0.3, LINEA),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), GRIS))
    t.setStyle(TableStyle(cmds))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(1.6 * cm, 1.1 * cm, "INF3862 · E1 Diseño de datos · recetas y wearables")
    canvas.drawRightString(A4[0] - 1.6 * cm, 1.1 * cm, f"{doc.page}")
    canvas.restoreState()


def box(ax, x, y, w, h, title, body, fc="#1F4E79"):
    p = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.04",
        linewidth=1.1, edgecolor="#1F4E79", facecolor=fc,
    )
    ax.add_patch(p)
    ax.text(x + w / 2, y + h - 0.07, title, ha="center", va="top",
            fontsize=8, fontweight="bold", color="white" if fc == "#1F4E79" else "#1F4E79")
    ax.text(x + w / 2, y + 0.06, body, ha="center", va="bottom",
            fontsize=6.4, color="white" if fc == "#1F4E79" else "#333333", wrap=True)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=10,
            linewidth=1.1, color="#1F4E79",
        )
    )


def fig_arquitectura(path: Path):
    fig, ax = plt.subplots(figsize=(10.4, 6.2))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    def b(x, y, w, h, t, s, dark=True):
        fc = "#1F4E79" if dark else "#E8F0F7"
        tc = "white" if dark else "#1F4E79"
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
                           linewidth=1.2, edgecolor="#1F4E79", facecolor=fc)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h * 0.68, t, ha="center", va="center",
                fontsize=8.2, fontweight="bold", color=tc)
        ax.text(x + w / 2, y + h * 0.32, s, ha="center", va="center",
                fontsize=6.6, color=tc)

    ax.text(5.2, 5.95, "Arquitectura inicial (capacidades, sin productos)", ha="center",
            fontsize=11, fontweight="bold", color="#1F4E79")

    b(0.35, 4.55, 3.0, 0.90, "Food.com", "catalogo + resenas | batch Parquet", False)
    b(3.70, 4.55, 3.0, 0.90, "App recetas", "comidas, resenas, vinculo reloj", False)
    b(7.05, 4.55, 3.0, 0.90, "Relojes", "lotes JSONL.gz | Pulso S / FitBand 2", False)
    b(2.20, 3.25, 6.0, 0.80, "Recepcion", "transacciones en linea + micro-batch mediciones", True)
    b(0.35, 1.75, 4.7, 1.10, "Almacenamiento operacional (OLTP)",
      "usuarios, recetas, resenas, dispositivos\ncomidas, sesiones, acumulado del dia", True)
    b(5.35, 1.75, 4.7, 1.10, "Lake + analitico (OLAP)",
      "crudo en objetos (schema-on-read)\ngold Parquet/Delta, particion por fecha", True)
    b(0.35, 0.22, 3.0, 1.10, "App / home", "Q1-Q4  <200 ms\nkcal de hoy (resumen)", False)
    b(3.70, 0.22, 3.0, 1.10, "Recomendacion", "Q5 ranking proxima comida\n(objetivo del proyecto)", False)
    b(7.05, 0.22, 3.0, 1.10, "Analista / E3", "Q6 hechos usuario-dia\ny hecho comida", False)
    for x in (1.85, 5.20, 8.55):
        arrow(ax, x, 4.55, x, 4.05)
    arrow(ax, 5.20, 3.25, 2.70, 2.85)
    arrow(ax, 5.20, 3.25, 7.70, 2.85)
    arrow(ax, 2.70, 1.75, 1.85, 1.32)
    arrow(ax, 7.70, 1.75, 5.20, 1.32)
    arrow(ax, 7.70, 1.75, 8.55, 1.32)

    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_er(path: Path):
    fig, ax = plt.subplots(figsize=(10.6, 7.0))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 7.0)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(5.3, 6.70, "Modelo operacional (ER simplificado)", ha="center",
            fontsize=12, fontweight="bold", color="#1F4E79")
    ents = [
        (0.25, 4.70, 3.20, "USUARIO", "PK author_id\nnombre, zona horaria"),
        (3.70, 4.70, 3.20, "RECETA", "PK recipe_id\nFK author_id (autor catalogo)\nname, category, macros, JSON"),
        (7.15, 4.70, 3.20, "RESENA", "PK review_id\nFK author_id, recipe_id\nrating, texto\nUNIQUE (usuario, receta)"),
        (0.25, 2.65, 3.20, "DISPOSITIVO", "PK device_id  FK author_id\nmodelo, vinc/desvinc, tz\nUNIQUE: un activo por usuario"),
        (3.70, 2.65, 3.20, "COMIDA", "PK comida_id\nFK author_id, recipe_id\nfecha_hora, porciones"),
        (7.15, 2.65, 3.20, "SESION", "PK session_id  FK device_id\ntipo, inicio, fin, km, kcal"),
        (0.25, 0.55, 4.85, "MEDICION (serie temporal)", "PK (device_id, ts_medicion)\nfc, pasos, kcal, ts_recepcion\nfuera del OLTP caliente"),
        (5.40, 0.55, 4.95, "ACUMULADO_USUARIO_DIA", "PK (author_id, fecha)\nkcal_in, kcal_out, pasos\nconsulta frontera kcal de hoy"),
    ]
    for x, y, w, title, body in ents:
        h = 1.55
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
                           linewidth=1.15, edgecolor="#1F4E79", facecolor="#E8F0F7")
        ax.add_patch(p)
        ax.text(x + w / 2, y + h - 0.18, title, ha="center", va="top",
                fontsize=8, fontweight="bold", color="#1F4E79")
        ax.text(x + w / 2, y + 0.18, body, ha="center", va="bottom",
                fontsize=6.6, color="#1F2A3A")
    ax.text(5.3, 0.18, "1 usuario — N dispositivos (a lo mas 1 activo). 1 receta — N comidas y resenas.",
            ha="center", fontsize=7.2, color="#444444")
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_estrella(path: Path):
    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.text(5.1, 4.95, "Modelo analítico: dos hechos (usuario-día y comida)", ha="center",
            fontsize=11, fontweight="bold", color="#1F4E79")

    def d(x, y, t):
        p = FancyBboxPatch((x, y), 2.2, 1.05, boxstyle="round,pad=0.02,rounding_size=0.05",
                           linewidth=1.1, edgecolor="#1F4E79", facecolor="#E8F0F7")
        ax.add_patch(p)
        ax.text(x + 1.1, y + 0.52, t, ha="center", va="center", fontsize=7.4, color="#1F4E79")

    p = FancyBboxPatch((3.3, 1.85), 3.6, 1.5, boxstyle="round,pad=0.02,rounding_size=0.05",
                       linewidth=1.4, edgecolor="#1F4E79", facecolor="#1F4E79")
    ax.add_patch(p)
    ax.text(5.1, 2.85, "HECHO_USUARIO_DIA", ha="center", color="white", fontsize=8.5, fontweight="bold")
    ax.text(5.1, 2.35, "1 fila por usuario y día\nkcal in/out · pasos · min. act.\ndeficit · n_comidas · n_sesiones",
            ha="center", color="white", fontsize=6.6)

    p2 = FancyBboxPatch((3.3, 0.15), 3.6, 1.25, boxstyle="round,pad=0.02,rounding_size=0.05",
                        linewidth=1.4, edgecolor="#5B7C99", facecolor="#5B7C99")
    ax.add_patch(p2)
    ax.text(5.1, 0.95, "HECHO_COMIDA", ha="center", color="white", fontsize=8.2, fontweight="bold")
    ax.text(5.1, 0.5, "1 fila por receta preparada\nporciones · macros · ventana 3 h",
            ha="center", color="white", fontsize=6.6)

    d(0.3, 3.5, "DIM_FECHA\nfecha, semana, mes, WE")
    d(7.7, 3.5, "DIM_USUARIO\nauthor_id, tz, modelo")
    d(0.3, 1.95, "DIM_ACTIVIDAD\ntipo, con/sin distancia")
    d(7.7, 1.95, "DIM_RECETA\ncategoría, macros, rating")
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def build_informe(sty, img_arq, img_er):
    w = 18.0 * cm
    story = []
    story.append(P("INF3862 — Plataformas Big Data para Data Science", sty["Cover"]))
    story.append(P("Entrega 1 · Diseño de datos: objetivo, estructura y consultas", sty["Cover"]))
    story.append(
        P(
            "Estudiante: Karina Oportus · Magíster en Estadìstica. "
            "Caso: recomendación de la próxima comida según balance energético y tipo de actividad. "
            ,
            sty["Meta"],
        )
    )

    story.append(P("1. Objetivo", sty["H"]))
    story.append(
        P(
            "<b>Resultado.</b> Producto: un ranking de recetas candidatas para la <i>próxima comida</i> "
            "del usuario que vinculó su reloj. Destinatario: el usuario en la app (y, en E3, un modelo). "
            "La decisión que apoya es <b>qué cocinar ahora</b> para acercar kcal ingeridas y gastadas, "
            "y para subir proteína después de correr o de una sesión de fuerza. No es un dashboard de "
            "vanidad: cada sugerencia se ancla a un déficit (o superávit) medido ese día.",
            sty["B"],
        )
    )
    story.append(
        P(
            "<b>Datos.</b> Food.com: 522.517 recetas (170 MB Parquet, 28 columnas; listas en ingredientes, "
            "keywords, instrucciones e imágenes; 311 categorías; 35 % de <i>RecipeServings</i> nulo) y "
            "1.401.982 reseñas (166 MB; 271.907 usuarios; rating 0–5, 76 k con 0). Wearable (extracto de "
            "61 días, 2007-12-16 a 2008-02-14): 315 dispositivos / 300 usuarios; 22.106 comidas; 4.840 "
            "sesiones; <b>15.540.132 mediciones</b> en 1.449 lotes JSONL.gz (110 MB). Llegan por la app "
            "(comida, reseña, vinculación) y por sincronización en lotes (medición).",
            sty["B"],
        )
    )
    story.append(
        P(
            "<b>Operaciones.</b> Escribir comida y vincular reloj con integridad; leer ficha de receta; "
            "mostrar kcal del día; agregar gasto e ingesta por usuario-día; rankear recetas según déficit "
            "y tipo de actividad. Predecir (E3) con grano usuario-comida y una ventana de 3 h de actividad.",
            sty["B"],
        )
    )
    story.append(
        P(
            "<b>Exigencias.</b> Registrar comida y abrir ficha: &lt; 200 ms, error no tolerable en FK. "
            "Recomendación: 1–3 s es aceptable (no es un cobro). Error de kcal ±15–20 % por porciones y "
            "<i>servings</i> incompletos. No se tolera receta inexistente (hay 48 comidas cuyo "
            "<i>RecipeId</i> no está en el catálogo) ni doble conteo por reintentos de sync. "
            "<b>Recursos.</b> 1–2 personas; E2 en portátil (DuckDB). OLTP pequeño; lake de objetos + "
            "Parquet. Si operara, presupuesto de cientos de USD/mes — no miles — mientras el wearable "
            "siga en cientos de usuarios; a escala de los 272 k reseñadores el cuello sería el volumen "
            "de mediciones, no el catálogo.",
            sty["B"],
        )
    )

    story.append(P("2. Fuentes y recepción", sty["H"]))
    story.append(
        tabla(
            ["Fuente", "Un registro es…", "Tipo", "Volumen (entregado / crecimiento)", "Recepción, frecuencia, latencia", "Problemas y esquema"],
            [
                [
                    "Recetas Food.com",
                    "Una receta del catálogo (ficha + nutrición + listas).",
                    "Estructurado; listas = semi.",
                    "522.517 filas, 170 MB. Catálogo casi estático: decenas o cientos de altas/día si la app publicara.",
                    "Carga <b>batch</b> del extracto. En operación: batch diario del catálogo. Latencia de horas es aceptable.",
                    "Servings nulos (35 %), tiempos ISO-8601, listas. <b>Schema-on-write</b> en OLTP: la ficha se consulta por id.",
                ],
                [
                    "Reseñas Food.com",
                    "Una calificación/texto de un usuario a una receta.",
                    "Estructurado; texto semi.",
                    "1,40 M filas, 166 MB; 272 k autores. Crecimiento: reseñas nuevas en línea.",
                    "<b>Transacción en línea</b> desde la app. Latencia &lt; 200 ms. Batch solo para el histórico Kaggle.",
                    "Rating 0 ambiguo; única reseña por par usuario-receta. <b>Schema-on-write</b>.",
                ],
                [
                    "Dispositivos / comidas / sesiones",
                    "Reloj vinculado; receta preparada; actividad (caminar, correr, bici, fuerza).",
                    "Estructurado (CSV / JSONL).",
                    "315 / 22.106 / 4.840. ~1 comida/usuario/día; ~0,3 sesiones/usuario/día.",
                    "Comida y vínculo: <b>OLTP</b>. Sesión: evento al cerrar el deporte. Latencia segundos–minutos.",
                    "Recambio de reloj; 48 comidas huérfanas; distancia nula en fuerza. Schema-on-write.",
                ],
                [
                    "Mediciones wearable",
                    "Una muestra de FC/pasos/kcal de un reloj.",
                    "Semi-estructurado (JSONL, 2 esquemas).",
                    "15,54 M en 61 días (~255 k/día; ~850/usuario/día). ×N si hay más usuarios o sampling a 10 s.",
                    "<b>Micro-batch / eventos</b>: un archivo por hora de <i>recepción</i>. Latencia de horas si el lote llega tarde.",
                    "Atrasos (ts_recepcion mucho despues de ts_medicion), duplicados por retry, FC nula, Pulso S vs FitBand 2 (frecuencia_cardiaca vs fc). <b>Schema-on-read</b> en crudo: no se fuerza un esquema al aterrizar el lote.",
                ],
            ],
            [2.0 * cm, 2.6 * cm, 2.0 * cm, 3.6 * cm, 3.6 * cm, 4.2 * cm],
            sty,
        )
    )
    story.append(
        P(
            "Cruce: <i>dispositivos.AuthorId</i> y <i>comidas.AuthorId</i> son usuarios de reseñas; "
            "<i>comidas.RecipeId</i> apunta al catálogo. El <i>AuthorId</i> de la receta es el <b>autor</b>, no quien cocina.",
            sty["B"],
        )
    )

    story.append(P("3. Estructura de los datos", sty["H"]))
    story.append(P("3.1 Nivel operacional (OLTP)", sty["H2"]))
    story.append(
        P(
            "La app necesita lookups por clave, escrituras cortas y reglas de integridad, no scans de 15 M de puntos. "
            "Por eso el operacional es <b>relacional</b> para <i>usuario</i>, <i>receta</i> (listas en JSON), "
            "<i>resena</i>, <i>dispositivo</i>, <i>comida</i> y <i>sesion</i>. Las mediciones van a un almacén de "
            "<b>series temporales</b> (o tabla particionada fuera del OLTP caliente): patrón append-only, dos "
            "esquemas de fabricante y cardinalidad que rompería el SLA de la app. Un modelo documental único "
            "debilitaría la FK receta-comida; un grafo se reserva a E3 si se modela “usuarios que cocinan lo mismo”.",
            sty["B"],
        )
    )
    story.append(
        tabla(
            ["Tabla", "PK / FK", "Modelo y acceso"],
            [
                ["usuario", "PK author_id", "Relacional. Perfil; 300 en el extracto, 272 k potenciales."],
                ["receta", "PK recipe_id; FK autor del catálogo", "Relacional + JSON listas. Get by id (home, ficha)."],
                ["resena", "PK review_id; FK usuario, receta", "Relacional. Unique (author_id, recipe_id)."],
                ["dispositivo", "PK device_id; FK author_id", "Relacional. Unique parcial: un activo por usuario."],
                ["comida", "PK comida_id; FK usuario, receta", "Relacional. Insert desde la app."],
                ["sesion", "PK session_id; FK device_id", "Relacional. Evento acotado (inicio–fin)."],
                ["medicion", "PK (device_id, ts_medicion)", "Serie temporal. No comparte pool con comidas."],
                ["acumulado_usuario_dia", "PK (author_id, fecha)", "Relacional. Sirve “kcal de hoy” (consulta frontera)."],
            ],
            [3.3 * cm, 5.5 * cm, 9.2 * cm],
            sty,
        )
    )
    story.append(
        P(
            "<b>Integridad transaccional.</b> (1) Un solo reloj con <i>fecha_desvinculacion</i> nula por usuario "
            "(en el extracto, p. ej. el usuario 531811 cambia W00011 → W00012). Vincular y desvincular van en "
            "<i>BEGIN … COMMIT</i>: sin transacción quedarían dos activos y se duplicarían pasos y kcal. "
            "(2) Una reseña por par usuario-receta. (3) Comida con receta existente y porciones &gt; 0, actualizando "
            "el acumulado del día en la misma unidad de trabajo. Diagrama ER: figura al final y anexo A3.",
            sty["B"],
        )
    )

    story.append(P("3.2 Nivel analítico (OLAP), ubicación y formato", sty["H2"]))
    story.append(
        P(
            "<b>Hecho principal <i>hecho_usuario_dia</i></b>: una fila por usuario y día (UTC, con atributo de tz). "
            "Medidas: kcal ingeridas (comidas × calorías de receta / servings), kcal gastadas (medición y sesión), "
            "pasos, minutos de actividad, n_comidas, n_sesiones, fc media, déficit. Claves a <i>dim_fecha</i>, "
            "<i>dim_usuario</i>, <i>dim_actividad</i> (tipo principal del día) y, opcional, receta modal. "
            "<b>Hecho secundario <i>hecho_comida</i></b>: una fila por receta preparada; incluye ventana de 3 h "
            "de pasos/kcal previas (feature de E3) y macros de <i>dim_receta</i>.",
            sty["B"],
        )
    )
    story.append(
        P(
            "<b>Dónde viven.</b> <i>Lakehouse</i>, no warehouse puro ni lake puro. El <b>crudo</b> aterriza en "
            "almacenamiento de objetos tal como llega (Parquet Food.com, JSONL.gz de mediciones por hora de "
            "<b>recepción</b>): <b>schema-on-read</b>, porque Pulso S y FitBand 2 no comparten nombres de campo. "
            "El <b>gold</b> son tablas columnares Parquet (o Delta/Iceberg si más adelante hay upserts por lotes "
            "atrasados): <b>schema-on-write</b> una vez unificado <i>fc</i>/<i>frecuencia_cardiaca</i>. El OLTP "
            "queda fuera del lake. Un warehouse tipo Kimball desde el día 1 obligaría a modelar el JSON heterogéneo "
            "antes de verlo; dejar todo en JSONL haría caras Q5–Q6. Formato gold: Parquet columnar, no CSV.",
            sty["B"],
        )
    )
    story.append(
        P(
            "<b>Físico.</b> Columnas, no filas: Q5 y Q6 leen 6–10 medidas, no el texto de reseñas ni las instrucciones. "
            "Partición de gold por <i>fecha</i> (día). Beneficio: poda en “hoy” y en rangos semanales; un día son "
            "~300 filas de hecho, no 255 k mediciones. El crudo <b>no</b> se reescribe a partición por medición: "
            "la carpeta documenta la ingesta. En silver sí se reparte por <i>ts_medicion</i>.",
            sty["B"],
        )
    )

    story.append(P("4. Consultas de ejemplo", sty["H"]))
    story.append(
        P(
            "SQL completo en anexo A1. Criterios de Clase 1: volumen tocado, lectura/escritura, frecuencia, "
            "latencia y concurrencia.",
            sty["B"],
        )
    )
    story.append(
        tabla(
            ["#", "Propósito y usuario", "Clase", "Justificación (Clase 1)", "Qué la haría rápida"],
            [
                [
                    "Q1",
                    "Registrar comida (app). Escribe comida + acumulado del día. <b>BEGIN/COMMIT</b>. Sin transacción el home muestra un balance falso o queda una comida huérfana.",
                    "OLTP escribe",
                    "1–2 filas. Alta frecuencia (cada comida). Latencia &lt; 200 ms. Concurrencia por usuario, no global.",
                    "PK, FK receta, índice (author_id, fecha) en acumulado.",
                ],
                [
                    "Q2",
                    "Vincular reloj nuevo (app). Desvincula el activo e inserta el nuevo en una transacción (regla de un dispositivo activo).",
                    "OLTP escribe",
                    "1–2 filas. Rara. Crítica por integridad, no por QPS.",
                    "Índice único parcial WHERE desvinculación IS NULL.",
                ],
                [
                    "Q3",
                    "Abrir ficha de receta (cliente). Lookup de nutrición y nombre para pintar la card.",
                    "OLTP lee",
                    "1 fila por PK. Muy frecuente. Latencia &lt; 50 ms. Alta concurrencia de lectura.",
                    "PK; caché de fichas populares.",
                ],
                [
                    "Q4",
                    "<b>Frontera.</b> “kcal de hoy” en la home (cliente). Responde una pregunta analítica con exigencia operacional.",
                    "Frontera → se sirve OLTP",
                    "Si fuera SUM sobre mediciones: ~850 filas/usuario y pelearía con Q1. Frecuencia = cada apertura. Latencia de UI.",
                    "Tabla <i>acumulado_usuario_dia</i> (o caché) alimentada al ingerir el lote. No scan columnar en la app ni JSONL.",
                ],
                [
                    "Q5",
                    "<b>Objetivo 4.1.</b> Ranking de 10 recetas cuya kcal cubre el déficit del día, con bonus de proteína si el tipo principal es correr/fuerza (servicio de recomendación / futuro modelo).",
                    "OLAP",
                    "Lee 1 fila de hecho + catálogo (522 k, filtrado por rango de kcal). Baja frecuencia por usuario (pocas veces al día). Latencia 1–3 s. Poca concurrencia vs. Q3.",
                    "Hecho columnar particionado por fecha; receta en Parquet; no tocar mediciones crudas.",
                ],
                [
                    "Q6",
                    "Balance semanal kcal in vs out y minutos de actividad (analista de producto).",
                    "OLAP",
                    "Scan de ~300×7 filas de hecho (extracto), no 1,8 M mediciones/semana. Diaria o ad hoc. Latencia de segundos. Un usuario a la vez.",
                    "Partición por fecha + columnas de medidas; posible agregado precalculado semanal.",
                ],
            ],
            [1.1 * cm, 5.0 * cm, 2.2 * cm, 5.3 * cm, 4.4 * cm],
            sty,
        )
    )
    story.append(
        P(
            "Q4 se clasifica como frontera porque el <i>qué</i> es analítico (agregado del día) y el <i>cómo</i> "
            "debe ser transaccional (home, muchos usuarios a la vez). Ejecutarla en el warehouse competiría en "
            "latencia con la operación; calcularla sobre crudo competiría en I/O con la ingesta. El resumen "
            "operacional desacopla ambos mundos. Q5 es la única que responde de lleno el producto de 4.1 y por "
            "eso vive en gold, no en la base de la app.",
            sty["B"],
        )
    )

    story.append(P("5. Arquitectura inicial", sty["H"]))
    story.append(
        P(
            "Fuentes (Food.com batch, app OLTP, relojes en lotes) → recepción (transacciones + micro-batch) → "
            "dos almacenes: base operacional con integridad y lake/lakehouse para crudo y hechos. Consumo: app "
            "(Q1–Q4), ranking (Q5), analista (Q6). No se nombran productos: en E3 se eligen PostgreSQL vs. "
            "equivalente, objetos + Parquet/Delta, y el motor del ranking. Coherencia: todo lo que la app "
            "debe acertar en milisegundos y con transacción queda en OLTP; todo lo que cruza nutrición × "
            "actividad en el tiempo queda en columnar particionado por fecha. Detalle en figuras siguientes y anexos.",
            sty["B"],
        )
    )

    story.append(PageBreak())
    story.append(P("Diagramas", sty["H"]))
    story.append(Image(str(img_er), width=w, height=w * 0.58))
    story.append(P("Figura 1. ER operacional simplificado.", sty["Cap"]))
    story.append(Image(str(img_arq), width=w, height=w * 0.52))
    story.append(P("Figura 2. Fuentes → recepción → OLTP / lakehouse → consumo.", sty["Cap"]))
    return story


def build_anexo_diagramas(sty, img_arq, img_er, img_st):
    w = 18.0 * cm
    story = []
    story.append(P("Anexo A3 · Diagramas E1", sty["Cover"]))
    story.append(P("INF3862 · no sustituye al informe; lo complementa.", sty["Meta"]))
    story.append(Image(str(img_er), width=w, height=w * 0.60))
    story.append(P("Figura A3.1 ER operacional.", sty["Cap"]))
    story.append(Image(str(img_st), width=w, height=w * 0.48))
    story.append(P("Figura A3.2 Estrella analítica (dos granos).", sty["Cap"]))
    story.append(Image(str(img_arq), width=w, height=w * 0.52))
    story.append(P("Figura A3.3 Arquitectura de capacidades.", sty["Cap"]))
    return story


def main():
    ANEXOS.mkdir(parents=True, exist_ok=True)
    img_arq = ANEXOS / "arquitectura.png"
    img_er = ANEXOS / "er_oltp.png"
    img_st = ANEXOS / "estrella_olap.png"
    fig_arquitectura(img_arq)
    fig_er(img_er)
    fig_estrella(img_st)

    sty = styles()
    inf = E1 / "informe.pdf"
    doc = SimpleDocTemplate(
        str(inf),
        pagesize=A4,
        leftMargin=1.55 * cm,
        rightMargin=1.55 * cm,
        topMargin=1.25 * cm,
        bottomMargin=1.55 * cm,
        title="INF3862 E1 Diseño de datos",
        author="Proyecto recetas y wearables",
    )
    doc.build(build_informe(sty, img_arq, img_er), onFirstPage=footer, onLaterPages=footer)

    anexo = ANEXOS / "A3_diagramas.pdf"
    doc2 = SimpleDocTemplate(
        str(anexo),
        pagesize=A4,
        leftMargin=1.55 * cm,
        rightMargin=1.55 * cm,
        topMargin=1.25 * cm,
        bottomMargin=1.55 * cm,
        title="INF3862 E1 Anexos diagramas",
    )
    doc2.build(build_anexo_diagramas(sty, img_arq, img_er, img_st), onFirstPage=footer, onLaterPages=footer)
    print("OK", inf, "pages check separately")
    print(anexo)


if __name__ == "__main__":
    main()
