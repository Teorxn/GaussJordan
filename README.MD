# Eliminación de Gauss y Gauss-Jordan

Aplicación interactiva de álgebra lineal para resolver sistemas de ecuaciones
lineales con eliminación gaussiana o de Gauss-Jordan.

**Estudiante:** Daniely Fernández Pérez

## Funciones

- Entrada de la matriz aumentada `[A | b]`.
- Selección del método: Gauss (forma escalonada) o Gauss-Jordan (RREF).
- Diagnóstico automático: solución única, infinitas soluciones o sistema incompatible.
- Rango de `A` y de la matriz ampliada, columnas pivote y variables libres.
- Operaciones elementales por filas explicadas paso a paso.
- Solución paramétrica cuando hay variables libres.
- Comprobación por sustitución en las ecuaciones originales.
- Modo de fracciones exactas y ejemplos guiados.

## Ejecutar (Windows)

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Si `streamlit` no se reconoce, usa siempre `python -m streamlit`.

## Formato de entrada

- Una fila de la matriz aumentada por línea.
- La última columna corresponde al término independiente `b`.
- Separa los valores con comas o espacios.
- Las filas también pueden separarse con `;`.
- Se aceptan fracciones como `1/2` en modo exacto.

Ejemplo:

```text
2, 1, -1, 8
-3, -1, 2, -11
-2, 1, 2, -3
```

## Estructura

```text
app.py                      Punto de entrada de Streamlit
Core/
  gaussian_elimination.py   Operaciones elementales por filas
  system_solver.py          Clasificación y solución de sistemas
  matrix_operations.py      Utilidades de matrices
ui/                         Interfaz (entrada, resultados, procedimiento, estilos)
utils/                      Validación y formato de números/LaTeX
visualizations/             Representación de matrices
examples/                   Sistemas de ejemplo
```
