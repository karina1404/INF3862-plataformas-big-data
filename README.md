# INF3862 — Plataformas Big Data para Data Science

Proyecto individual: **plataforma de datos para recetas y wearables**.

## Caso de uso

Recomendar la **próxima comida** a usuarios que vinculan un reloj y registran recetas preparadas, usando el **balance energético del día** (kcal ingeridas desde Food.com vs. kcal gastadas en el wearable) y el **tipo de actividad** (más proteína después de correr o fuerza).

## Entregables

| Entrega | Plazo | Dónde está |
|---|---|---|
| **E1** Diseño de datos | 16-nov-2026 | [`entregas/E1/informe.pdf`](entregas/E1/informe.pdf) · [anexos](entregas/E1/anexos/) |
| E2 Ingesta y procesamiento | 30-nov-2026 | `entregas/E2/` (pendiente) |
| E3 Datos para ML y arquitectura | 14-dic-2026 | `entregas/E3/` (pendiente) |

Registro de decisiones (todo el curso): [`decisiones.md`](decisiones.md).

Cómo obtener los datos (no están en este repo): [`datos/README.md`](datos/README.md).

Repositorio público: https://github.com/karina1404/INF3862-plataformas-big-data

Si el PDF aún dice “completar nombre”, regenerarlo o editar la portada; el informe actual usa **Karina**. Si tu apellido debe ir, dímelo y lo actualizamos.

## Cómo publicar este repositorio en GitHub

Este proyecto se entrega en un **repositorio público**. Desde la carpeta del proyecto, en PowerShell o Git Bash:

```bash
git init
git add README.md .gitignore datos/README.md decisiones.md entregas/
git status
git commit -m "E1: diseño de datos para recomendación de próxima comida"
```

En GitHub (github.com): **New repository** → nombre p. ej. `INF3862-plataformas-big-data` → **Public** → **no** agregue README, .gitignore ni licencia (ya existen) → Create.

```bash
git branch -M main
git remote add origin https://github.com/karina1404/INF3862-plataformas-big-data.git
git push -u origin main
```

Luego pegar la URL en el Excel de registro de repositorios del curso.

**No suba** `datos_proyecto_INF3862/` ni los `.parquet` (`.gitignore` ya los excluye).

## Entorno (a partir de E2)

El enunciado pide `uv`. Cuando corresponda:

```bash
uv sync
uv run jupyter notebook
```
