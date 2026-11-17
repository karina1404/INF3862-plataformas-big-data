# Anexo A1 · Consultas E1 (SQL aproximado)

No se exige ejecución. Clasificación y justificación van en el informe.

## Q1 · OLTP · Registrar una comida (escritura + transacción)

Propósito: el usuario marca que preparó una receta. Usuario: la app.

```sql
BEGIN;
-- Unidad de trabajo: o queda la comida y el contador del día, o nada.
INSERT INTO comida (comida_id, author_id, recipe_id, fecha_hora, porciones)
VALUES (:id, :author_id, :recipe_id, :ts, :porciones);

-- Falla si la receta no existe (FK) o porciones <= 0 (CHECK).
UPDATE acumulado_usuario_dia
   SET kcal_ingeridas = kcal_ingeridas
       + (:porciones * r.calories / NULLIF(r.recipe_servings, 0))
  FROM receta r
 WHERE r.recipe_id = :recipe_id
   AND acumulado_usuario_dia.author_id = :author_id
   AND acumulado_usuario_dia.fecha = DATE(:ts);
COMMIT;
-- ROLLBACK si la receta no está en catálogo o el usuario no existe.
```

Sin transacción: la comida se inserta y el acumulado de “kcal de hoy” no se actualiza (o al revés). La app mostraría un balance falso.

## Q2 · OLTP · Vincular un reloj nuevo (un activo por usuario)

```sql
BEGIN;
UPDATE dispositivo
   SET fecha_desvinculacion = :ahora
 WHERE author_id = :author_id
   AND fecha_desvinculacion IS NULL;

INSERT INTO dispositivo (device_id, author_id, modelo, fecha_vinculacion, zona_horaria)
VALUES (:device_id, :author_id, :modelo, :ahora, :tz);
COMMIT;
```

Índice único parcial: `UNIQUE (author_id) WHERE fecha_desvinculacion IS NULL`.

## Q3 · OLTP · Ficha de receta al abrir el detalle

```sql
SELECT recipe_id, name, recipe_category, calories, protein_content,
       recipe_servings, total_time, recipe_ingredient_parts
  FROM receta
 WHERE recipe_id = :recipe_id;
```

Toca 1 fila por clave. Latencia < 50 ms. Índice PK.

## Q4 · Frontera OLTP/OLAP · “kcal de hoy” en la app

```sql
SELECT kcal_ingeridas, kcal_gastadas, pasos, n_sesiones
  FROM acumulado_usuario_dia
 WHERE author_id = :author_id
   AND fecha = CURRENT_DATE;
```

Clasificación: **se sirve como OLTP de lectura** sobre un resumen mantenido al ingerir lotes, no como OLAP ad hoc. Si se calculara con `SUM` sobre mediciones crudas, tocaría ~850 filas/usuario/día (y más en sesiones a 10 s) con alta concurrencia y competiría con la operación. Ejecutarla en el warehouse reintroduciría 1–3 s de latencia inaceptables en la home. Por eso vive en la base operacional como tabla de acumulados (o caché), alimentada por el pipeline, no por el analista.

## Q5 · OLAP · Ranking de próxima comida (objetivo 4.1)

```sql
WITH balance AS (
  SELECT author_id,
         kcal_ingeridas,
         kcal_gastadas,
         (kcal_gastadas - kcal_ingeridas) AS deficit,
         tipo_actividad_principal
    FROM hecho_usuario_dia
   WHERE fecha = :hoy
),
hist AS (
  SELECT author_id, recipe_id, COUNT(*) AS veces
    FROM hecho_comida
   GROUP BY 1, 2
)
SELECT r.recipe_id, r.name, r.calories, r.protein_content,
       b.deficit,
       CASE
         WHEN b.tipo_actividad_principal IN ('correr','fuerza')
          AND r.protein_content >= 20 THEN 1 ELSE 0
       END AS bonus_proteina
  FROM receta r
  JOIN balance b ON TRUE
  LEFT JOIN hist h
    ON h.author_id = b.author_id AND h.recipe_id = r.recipe_id
 WHERE r.calories BETWEEN GREATEST(b.deficit * 0.4, 150)
                      AND GREATEST(b.deficit * 1.2, 700)
 ORDER BY bonus_proteina DESC, h.veces DESC NULLS LAST, r.aggregated_rating DESC
 LIMIT 10;
```

Usuario: el servicio de recomendación / futuro modelo. Columnar + partición por `fecha` en el hecho; dimensión receta puede ir en parquet no particionado (522 k filas caben en memoria).

## Q6 · OLAP · Balance semanal por usuario (analista / producto)

```sql
SELECT u.author_id,
       d.semana,
       SUM(f.kcal_ingeridas) AS ing,
       SUM(f.kcal_gastadas)  AS gas,
       SUM(f.pasos)          AS pasos,
       SUM(f.minutos_actividad) AS min_act
  FROM hecho_usuario_dia f
  JOIN dim_fecha d   ON d.fecha = f.fecha
  JOIN dim_usuario u ON u.author_id = f.author_id
 WHERE d.fecha BETWEEN :desde AND :hasta
 GROUP BY u.author_id, d.semana;
```

Lee ~300 usuarios × 7 días en el extracto; a escala de todos los reseñadores con reloj, la partición por `fecha` evita un full scan.

## Q7 · OLAP (extra) · Proteína ingerida tras correr vs. días sedentarios

```sql
SELECT CASE WHEN f.tipo_actividad_principal = 'correr' THEN 'correr' ELSE 'otro' END AS grupo,
       AVG(c.proteina_g) AS proteina_media_comida,
       COUNT(*) AS n
  FROM hecho_comida c
  JOIN hecho_usuario_dia f
    ON f.author_id = c.author_id AND f.fecha = c.fecha
 WHERE c.fecha BETWEEN :desde AND :hasta
 GROUP BY 1;
```
