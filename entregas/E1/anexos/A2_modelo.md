# Anexo A2 · Detalle de estructuras

## OLTP · tablas y claves

| Tabla | PK | FK | Columnas principales | Modelo | Por qué |
|---|---|---|---|---|---|
| `usuario` | `author_id` | — | nombre, tz preferida | Relacional | Punto de integridad de la app |
| `receta` | `recipe_id` | `author_id` (autor del catálogo) | name, category, times ISO-8601, calories, macros, servings, keywords[], ingredients[], instructions[] | Relacional + JSON en columnas de listas | Lookup por id; listas no merecen 3FN en E1 |
| `resena` | `review_id` | `recipe_id`, `author_id` | rating 0–5, texto, submitted, modified | Relacional | Unique `(author_id, recipe_id)` |
| `dispositivo` | `device_id` | `author_id` | modelo, vinculación, desvinculación, tz | Relacional | Unique parcial: un activo por usuario |
| `comida` | `comida_id` | `author_id`, `recipe_id` | fecha_hora, porciones | Relacional | Escritura frecuente desde la app |
| `sesion` | `session_id` | `device_id` | tipo, inicio, fin, distancia_km, calorias | Relacional | Evento acotado; 4,8 k en el extracto |
| `medicion` (fuera del OLTP caliente) | `(device_id, ts_medicion)` | `device_id` | ts_recepcion, fc, pasos, kcal, fuente_modelo | Series temporales | 15,5 M filas append-only |
| `acumulado_usuario_dia` | `(author_id, fecha)` | `author_id` | kcal_in, kcal_out, pasos, n_sesiones | Relacional (resumen) | Sirve Q4 sin tocar series |

Listas de receta (`Keywords`, `RecipeIngredientParts`, `RecipeInstructions`, `Images`) se guardan como JSON/array: schema-on-write de la ficha, schema-on-read si más adelante se explota un ingrediente.

## Integridad que exige transacción

1. **Un reloj activo por usuario** (Q2).
2. **Una reseña por usuario y receta** (`UNIQUE (author_id, recipe_id)`).
3. **Comida con receta existente y porciones > 0** (Q1): FK + CHECK en la misma unidad de trabajo que el acumulado del día.

## OLAP · estrella

**Hecho `hecho_usuario_dia`** — granularidad: *una fila por usuario y día calendario (UTC, luego local con `zona_horaria`)*.

Medidas: `kcal_ingeridas`, `kcal_gastadas_medicion`, `kcal_gastadas_sesion`, `pasos`, `minutos_actividad`, `n_comidas`, `n_sesiones`, `fc_media`, `deficit_kcal`.

Claves: `fecha` → `dim_fecha`; `author_id` → `dim_usuario`; `tipo_actividad_principal` → `dim_actividad`; `recipe_id_modal` → `dim_receta` (la más repetida ese día; opcional).

**Hecho `hecho_comida`** — granularidad: *una fila por receta preparada*.

Medidas: `porciones`, `kcal_ingesta`, `proteina_g`, `pasos_3h_previas`, `kcal_gastadas_3h_previas` (ventana para E3), `minutos_desde_ultima_sesion`.

Dimensiones: `dim_fecha`, `dim_usuario`, `dim_receta` (categoría, macros, rating agregado, tiempo total), `dim_actividad` (si hubo sesión en ventana).

`dim_fecha`: fecha, semana, mes, fin_de_semana, hora_local no aplica a este grano diario.

`dim_usuario`: author_id, tz, modelo_actual, fecha_alta_reloj.

`dim_receta`: SCD tipo 1 en E1 (el catálogo histórico de Kaggle no versiona cambios).

## Ubicación y formato

| Capa | Dónde | Formato | Organización |
|---|---|---|---|
| Crudo | Data lake (objetos) | Parquet Food.com tal cual; CSV/JSONL.gz wearable | Carpetas `foodcom/`, `wearable/mediciones/fecha_recepcion/hora/` |
| Operacional | Base OLTP | filas (heap/índices B-tree) | Por PK |
| Silver/Gold | Lakehouse (tablas) | Parquet o Delta/Iceberg | Columnar; gold particionado por `fecha` |

Consultas que se benefician de la partición: Q5 y Q6 (filtro de día o rango). Q7 también si se predica `c.fecha`. Un índice B-tree no aporta en el scan columnar de 18 k días-usuario; sí la poda de directorios.
