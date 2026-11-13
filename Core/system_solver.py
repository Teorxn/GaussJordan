from __future__ import annotations

from fractions import Fraction
from typing import Dict, List, Tuple

from Core.gaussian_elimination import eliminate
from Core.matrix_operations import clone_matrix, is_zero, shape


Number = Fraction | float | int
PARAM_NAMES = ["t", "s", "r", "u", "w", "v", "z"]


def solve_system(
	matrix: List[List[Number]],
	method: str = "gauss-jordan",
	tol: float = 1e-10,
	exact: bool = False,
	record_steps: bool = True,
) -> Dict[str, object]:
	"""Solve an augmented system [A | b] using Gaussian elimination."""

	rows, cols = shape(matrix)
	if rows == 0:
		raise ValueError("La matriz aumentada está vacía.")
	if cols < 2:
		raise ValueError("La matriz debe incluir al menos una incógnita y el término independiente.")
	if any(len(row) != cols for row in matrix):
		raise ValueError("Todas las filas deben tener la misma cantidad de columnas.")

	n_vars = cols - 1
	working = _coerce_matrix(matrix, exact)

	echelon, pivot_cols, steps = eliminate(
		working,
		method=method,
		tol=tol,
		record_steps=record_steps,
	)

	if method == "gauss-jordan":
		rref_matrix = clone_matrix(echelon)
	else:
		rref_matrix, _, _ = eliminate(echelon, method="gauss-jordan", tol=tol, record_steps=False)

	contradiction_row = _find_contradiction(echelon, n_vars, tol)
	rank = len(pivot_cols)
	rank_augmented = rank + (1 if contradiction_row is not None else 0)
	free_cols = [col for col in range(n_vars) if col not in pivot_cols]
	param_names = _parameter_names(len(free_cols))

	if contradiction_row is not None:
		status = "inconsistent"
	elif free_cols:
		status = "infinite"
	else:
		status = "unique"

	solution: List[Number] | None = None
	parametric: List[Dict[str, object]] = []
	example_solution: List[Number] | None = None
	back_substitution: List[Dict[str, object]] = []

	if status == "unique":
		solution = [0] * n_vars
		for row_index, pivot_col in enumerate(pivot_cols):
			solution[pivot_col] = rref_matrix[row_index][n_vars]
		if method == "gauss":
			solution, back_substitution = _back_substitution(echelon, pivot_cols, n_vars, tol)
		solution = [_clean(value, tol) for value in solution]
	elif status == "infinite":
		parametric = _parametric_solution(rref_matrix, pivot_cols, free_cols, param_names, n_vars, tol)
		example_solution = [0] * n_vars
		for entry in parametric:
			value = entry["const"]
			for coefficient, _param in entry["terms"]:
				value += coefficient
			example_solution[int(entry["col"])] = value
		example_solution = [_clean(value, tol) for value in example_solution]

	verification_solution = solution if solution is not None else example_solution
	verification = _verify(matrix, verification_solution, n_vars, tol) if verification_solution else []
	concrete_solution = verification_solution

	return {
		"method": method,
		"matrix": clone_matrix(matrix),
		"echelon": echelon,
		"rref": rref_matrix,
		"final_matrix": echelon if method == "gauss" else rref_matrix,
		"steps": steps,
		"pivot_cols": pivot_cols,
		"rank": rank,
		"rank_augmented": rank_augmented,
		"n_vars": n_vars,
		"n_equations": rows,
		"free_cols": free_cols,
		"param_names": param_names,
		"status": status,
		"solution": solution,
		"example_solution": example_solution,
		"concrete_solution": concrete_solution,
		"parametric": parametric,
		"back_substitution": back_substitution,
		"contradiction_row": contradiction_row,
		"verification": verification,
		"exact": exact,
	}


def _find_contradiction(matrix: List[List[Number]], n_vars: int, tol: float) -> int | None:
	for row_index, row in enumerate(matrix):
		coefficients_zero = all(is_zero(value, tol) for value in row[:n_vars])
		if coefficients_zero and not is_zero(row[n_vars], tol):
			return row_index
	return None


def _coerce_matrix(matrix: List[List[Number]], exact: bool) -> List[List[Number]]:
	if exact:
		return [[value if isinstance(value, Fraction) else Fraction(value) for value in row] for row in matrix]

	# Keep whole numbers exact even outside "Fracciones exactas"; this avoids
	# rounding artifacts and unnecessary fractions in integer systems.
	converted: List[List[Number]] = []
	for row in matrix:
		new_row: List[Number] = []
		for value in row:
			if isinstance(value, Fraction) and value.denominator == 1:
				new_row.append(value)
			elif isinstance(value, int):
				new_row.append(Fraction(value))
			else:
				new_row.append(float(value))
		converted.append(new_row)
	return converted


def _clean(value: Number, tol: float) -> Number:
	if isinstance(value, Fraction):
		return value
	number = float(value)
	nearest = round(number)
	if abs(number - nearest) <= tol * max(1.0, abs(number)):
		return int(nearest)
	return number


def _parameter_names(count: int) -> List[str]:
	names: List[str] = []
	for index in range(count):
		names.append(PARAM_NAMES[index] if index < len(PARAM_NAMES) else f"t_{{{index + 1}}}")
	return names


def _parametric_solution(
	rref_matrix: List[List[Number]],
	pivot_cols: List[int],
	free_cols: List[int],
	param_names: List[str],
	n_vars: int,
	tol: float,
) -> List[Dict[str, object]]:
	entries: List[Dict[str, object]] = []

	for col in range(n_vars):
		if col in free_cols:
			param_index = free_cols.index(col)
			entries.append(
				{
					"col": col,
					"free": True,
					"const": 0,
					"terms": [(1, param_names[param_index])],
				}
			)
			continue

		row_index = pivot_cols.index(col)
		constant = _clean(rref_matrix[row_index][n_vars], tol)
		terms: List[Tuple[Number, str]] = []
		for free_col in free_cols:
			coefficient = _clean(-rref_matrix[row_index][free_col], tol)
			if not is_zero(coefficient, tol):
				terms.append((coefficient, param_names[free_cols.index(free_col)]))

		entries.append(
			{
				"col": col,
				"free": False,
				"const": constant,
				"terms": terms,
			}
		)

	return entries


def _back_substitution(
	echelon: List[List[Number]],
	pivot_cols: List[int],
	n_vars: int,
	tol: float,
) -> Tuple[List[Number], List[Dict[str, object]]]:
	solution: List[Number] = [0] * n_vars
	steps: List[Dict[str, object]] = []

	for row_index in range(len(pivot_cols) - 1, -1, -1):
		pivot_col = pivot_cols[row_index]
		rhs = echelon[row_index][n_vars]
		subtotal: Number = 0
		for col in range(pivot_col + 1, n_vars):
			subtotal += echelon[row_index][col] * solution[col]
		pivot_coefficient = echelon[row_index][pivot_col]
		value = (rhs - subtotal) / pivot_coefficient
		value = _clean(value, tol)
		solution[pivot_col] = value
		steps.append(
			{
				"var": pivot_col,
				"value": value,
				"rhs": rhs,
				"subtotal": subtotal,
				"pivot": pivot_coefficient,
			}
		)

	return solution, steps


def _verify(
	matrix: List[List[Number]],
	solution: List[Number],
	n_vars: int,
	tol: float,
) -> List[Dict[str, object]]:
	checks: List[Dict[str, object]] = []
	for row_index, row in enumerate(matrix):
		lhs: Number = 0
		for col in range(n_vars):
			lhs += row[col] * solution[col]
		rhs = row[n_vars]
		residual = lhs - rhs
		checks.append(
			{
				"row": row_index,
				"lhs": lhs,
				"rhs": rhs,
				"residual": 0 if is_zero(residual, tol) else residual,
				"ok": is_zero(residual, tol),
			}
		)
	return checks
