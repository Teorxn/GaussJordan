from __future__ import annotations

from fractions import Fraction
from typing import List, Tuple


Number = Fraction | float | int


def shape(matrix: List[List[Number]]) -> Tuple[int, int]:
	if not matrix:
		return 0, 0
	return len(matrix), len(matrix[0])


def clone_matrix(matrix: List[List[Number]]) -> List[List[Number]]:
	return [row[:] for row in matrix]


def transpose(matrix: List[List[Number]]) -> List[List[Number]]:
	if not matrix:
		return []
	rows, cols = shape(matrix)
	return [[matrix[r][c] for r in range(rows)] for c in range(cols)]


def is_zero(value: Number, tol: float = 1e-10) -> bool:
	if isinstance(value, Fraction):
		return value == 0
	return abs(float(value)) <= tol


def normalize_small_values(matrix: List[List[Number]], tol: float = 1e-10) -> None:
	for r, row in enumerate(matrix):
		for c, value in enumerate(row):
			if not isinstance(value, Fraction) and abs(float(value)) <= tol:
				matrix[r][c] = 0.0


def row_is_zero(row: List[Number], tol: float = 1e-10) -> bool:
	return all(is_zero(value, tol) for value in row)
