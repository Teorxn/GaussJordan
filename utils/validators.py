from __future__ import annotations

import re
from fractions import Fraction
from typing import List, Tuple


Number = Fraction | float | int


def parse_augmented_matrix(text: str, exact: bool = False) -> Tuple[List[List[Number]] | None, str | None]:
	"""Parse rows of an augmented matrix [A | b].

	Rows may be separated by line breaks or semicolons. Values may be separated
	by spaces, commas or a vertical bar. Fractions such as ``1/2`` are accepted
	in both modes.
	"""

	if not text or not text.strip():
		return None, "Escribe al menos una fila de la matriz aumentada."

	clean_text = text.replace(";", "\n").replace("|", " ")
	lines = [line.strip() for line in clean_text.splitlines() if line.strip()]

	matrix: List[List[Number]] = []
	expected_len: int | None = None

	for line_number, line in enumerate(lines, start=1):
		line = line.strip().strip("[]()").replace("\t", " ")
		tokens = [token for token in re.split(r"[,\s]+", line) if token]
		if not tokens:
			continue

		try:
			row = [parse_number(token, exact) for token in tokens]
		except ValueError as exc:
			return None, f"Fila {line_number}: número inválido ({exc})."

		if expected_len is None:
			expected_len = len(row)
		elif len(row) != expected_len:
			return None, "Todas las filas deben tener la misma cantidad de columnas."

		matrix.append(row)

	if not matrix:
		return None, "No se encontraron valores válidos."

	if expected_len is not None and expected_len < 2:
		return None, "La matriz debe tener al menos una incógnita y el término independiente."

	return matrix, None


def parse_number(token: str, exact: bool) -> Number:
	cleaned = token.replace("−", "-").strip()
	try:
		if exact:
			return Fraction(cleaned)
		if "/" in cleaned:
			return float(Fraction(cleaned))
		if re.fullmatch(r"[+-]?\d+", cleaned):
			return Fraction(int(cleaned))
		return float(cleaned)
	except (ValueError, ZeroDivisionError):
		raise ValueError(f"'{token}' no es un número válido") from None
