# Anexos de la E1

No cuentan en el máximo de 3 páginas del informe.

| Archivo | Contenido |
|---|---|
| [`A1_consultas.sql.md`](A1_consultas.sql.md) | SQL aproximado de Q1–Q6 (y Q7 extra) |
| [`A2_modelo.md`](A2_modelo.md) | Detalle OLTP/OLAP, integridad, formatos |
| [`A3_diagramas.pdf`](A3_diagramas.pdf) | ER, estrella analítica y arquitectura |
| `er_oltp.png`, `estrella_olap.png`, `arquitectura.png` | Figuras usadas en el PDF |
| `generar_pdf_e1.py` | Script que regenera `informe.pdf` y `A3_diagramas.pdf` |

Para regenerar los PDF (opcional):

```bash
pip install reportlab matplotlib
python entregas/E1/anexos/generar_pdf_e1.py
```
