from __future__ import annotations

from fractions import Fraction
from typing import Dict, List, Tuple

from Core.matrix_operations import clone_matrix, is_zero, normalize_small_values, shape


Number = Fraction | float | int
Step = Dict[str, object]


def eliminate(
	matrix: List[List[Number]],
	method: str = "gauss-jordan",
	tol: float = 1e-10,
	record_steps: bool = True,
) -> Tuple[List[List[Number]], List[int], List[Step]]:
	"""Reduce an augmented matrix [A | b].

	The last column is treated as the right-hand side vector and is never used
	as a pivot column. ``method`` may be ``gauss`` (row echelon form) or
	``gauss-jordan`` (reduced row echelon form).
	"""

	if method not in {"gauss", "gauss-jordan"}:
		raise ValueError("method must be 'gauss' or 'gauss-jordan'")

	work = clone_matrix(matrix)
	rows, cols = shape(work)
	if rows == 0 or cols < 2:
		return work, [], []

	n_vars = cols - 1
	pivot_cols: List[int] = []
	steps: List[Step] = []

	pivot_row = 0
	for col in range(n_vars):
		if pivot_row >= rows:
			break

		found = _find_pivot_row(work, pivot_row, col, tol)
		if found is None:
			continue

		if found != pivot_row:
			work[pivot_row], work[found] = work[found], work[pivot_row]
			_record(
				steps,
				record_steps,
				{
					"kind": "swap",
					"row": pivot_row,
					"other": found,
					"label": f"R{pivot_row + 1} \u2194 R{found + 1}",
				},
				work,
			)

		pivot_value = work[pivot_row][col]

		if method == "gauss-jordan":
			if not _is_one(pivot_value):
				work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
				_record(
					steps,
					record_steps,
					{
						"kind": "scale",
						"row": pivot_row,
						"pivot_col": col,
						"factor": pivot_value,
						"label": f"R{pivot_row + 1} \u2190 R{pivot_row + 1} \u00f7 ({_fmt(pivot_value)})",
					},
					work,
				)

			for r in range(rows):
				if r == pivot_row:
					continue
				factor = work[r][col]
				if is_zero(factor, tol):
					continue
				work[r] = [value - factor * pivot for value, pivot in zip(work[r], work[pivot_row])]
				_record(
					steps,
					record_steps,
					{
						"kind": "eliminate",
						"row": r,
						"pivot_row": pivot_row,
						"pivot_col": col,
						"factor": factor,
						"label": _eliminate_label(r, pivot_row, factor),
					},
					work,
				)
		else:
			for r in range(pivot_row + 1, rows):
				factor = work[r][col] / pivot_value
				if is_zero(factor, tol):
					continue
				work[r] = [value - factor * pivot for value, pivot in zip(work[r], work[pivot_row])]
				_record(
					steps,
					record_steps,
					{
						"kind": "eliminate",
						"row": r,
						"pivot_row": pivot_row,
						"pivot_col": col,
						"factor": factor,
						"label": _eliminate_label(r, pivot_row, factor),
					},
					work,
				)

		pivot_cols.append(col)
		pivot_row += 1

	normalize_small_values(work, tol)
	return work, pivot_cols, steps


def rref(
	matrix: List[List[Number]],
	tol: float = 1e-10,
	record_steps: bool = True,
) -> Tuple[List[List[Number]], List[int], List[Step]]:
	"""Convenience wrapper that reduces a matrix to RREF."""

	return eliminate(matrix, method="gauss-jordan", tol=tol, record_steps=record_steps)


def _find_pivot_row(matrix: List[List[Number]], start_row: int, col: int, tol: float) -> int | None:
	best_row: int | None = None
	best_value = 0.0

	for row in range(start_row, len(matrix)):
		value = matrix[row][col]
		if is_zero(value, tol):
			continue
		if isinstance(value, Fraction):
			return row
		magnitude = abs(float(value))
		if magnitude > best_value:
			best_value = magnitude
			best_row = row

	return best_row


def _is_one(value: Number) -> bool:
	if isinstance(value, Fraction):
		return value == 1
	return abs(float(value) - 1.0) <= 1e-12


def _fmt(value: Number) -> str:
	if isinstance(value, Fraction):
		if value.denominator == 1:
			return str(value.numerator)
		return f"{value.numerator}/{value.denominator}"
	text = f"{float(value):.6f}".rstrip("0").rstrip(".")
	return "0" if text in {"-0", ""} else text


def _eliminate_label(row: int, pivot_row: int, factor: Number) -> str:
	operator = "+" if factor < 0 else "\u2212"
	magnitude = -factor if factor < 0 else factor
	return f"R{row + 1} \u2190 R{row + 1} {operator} ({_fmt(magnitude)}) \u00b7 R{pivot_row + 1}"


def _record(steps: List[Step], enabled: bool, step: Step, matrix: List[List[Number]]) -> None:
	if not enabled:
		return
	payload = dict(step)
	payload["matrix"] = clone_matrix(matrix)
	steps.append(payload)
