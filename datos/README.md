# Datos del proyecto · INF3862

Los datasets **no** van en GitHub (volumen y enunciado). Se descargan desde Canvas y se ubican en local.

## Cómo obtenerlos

1. En Canvas del curso INF3862, descargar el paquete `datos_proyecto_INF3862` (ZIP).
2. Descomprimirlo de modo que quede esta ruta relativa al repositorio:

```text
datos_proyecto_INF3862/datos_proyecto_INF3862/
  foodcom/
    recipes.parquet
    reviews.parquet
  wearable/
    dispositivos.csv
    comidas.csv
    sesiones.jsonl
    mediciones/AAAA-MM-DD/HH.jsonl.gz
    LEEME.md
  LEEME.md
```

3. Comprobar que existen `foodcom/recipes.parquet` y `wearable/dispositivos.csv`.

Fuente Food.com: [Food.com - Recipes and Reviews](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) (Kaggle, CC0). Wearable: datos sintéticos del equipo docente.

## Muestra sugerida (E2)

Para el pipeline mínimo, no hace falta cargar las 15,5 millones de mediciones ni las 522 mil recetas:

- **Usuarios:** los 300 `AuthorId` de `wearable/dispositivos.csv`.
- **Ventana temporal:** 14 días, por ejemplo `2008-01-01` a `2008-01-14` (carpeta `wearable/mediciones/`).
- **Recetas:** solo las que aparecen en `wearable/comidas.csv` (`RecipeId`) más un catálogo reducido para recomendar (p. ej. recetas con `Calories` y `ProteinContent` no nulos).
- **Reseñas:** filtrar a esos `AuthorId` (preferencias del usuario con reloj).

## Cómo se relacionan

| Cruce | Relación |
|---|---|
| `dispositivos.AuthorId` | usuario de `reviews.AuthorId` |
| `comidas.AuthorId` | mismo usuario de Food.com |
| `comidas.RecipeId` | receta de `recipes.RecipeId` |
| `recipes.AuthorId` | **autor de la receta**, no quien la cocina |

## Volúmenes observados (entrega E1)

| Archivo | Filas / lotes | Tamaño |
|---|---|---|
| `recipes.parquet` | 522.517 recetas | 170 MB |
| `reviews.parquet` | 1.401.982 reseñas; 271.907 usuarios | 166 MB |
| `dispositivos.csv` | 315 relojes / 300 usuarios | 19 KB |
| `comidas.csv` | 22.106 comidas | 983 KB |
| `sesiones.jsonl` | 4.840 sesiones | 761 KB |
| `mediciones/*.jsonl.gz` | 15.540.132 mediciones; 1.449 lotes; 61 días (2007-12-16 a 2008-02-14) | 110 MB comprimido |
