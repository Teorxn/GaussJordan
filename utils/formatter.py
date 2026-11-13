from __future__ import annotations

from fractions import Fraction
from typing import Iterable, List, Tuple


Number = Fraction | float | int


def format_number(value: Number, precision: int = 6) -> str:
	if isinstance(value, Fraction):
		if value.denominator == 1:
			return str(value.numerator)
		return f"{value.numerator}/{value.denominator}"

	text = f"{float(value):.{precision}f}".rstrip("0").rstrip(".")
	if text in {"-0", "-0.0", ""}:
		return "0"
	return text


def latex_number(value: Number, precision: int = 6) -> str:
	if isinstance(value, Fraction):
		if value.denominator == 1:
			return str(value.numerator)
		sign = "-" if value.numerator < 0 else ""
		return f"{sign}\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"
	return format_number(value, precision)


def format_matrix(matrix: List[List[Number]], precision: int = 6) -> List[List[str]]:
	return [[format_number(value, precision) for value in row] for row in matrix]


def format_vector_list(vectors: List[List[Number]], precision: int = 6) -> str:
	lines = []
	for vector in vectors:
		values = ", ".join(format_number(value, precision) for value in vector)
		lines.append(f"[{values}]")
	return "\n".join(lines)


def vectors_to_text(vectors: List[List[Number]], precision: int = 6) -> str:
	return "\n".join(", ".join(format_number(value, precision) for value in vector) for vector in vectors)


def variable_latex(index: int) -> str:
	return f"x_{{{index + 1}}}"


def augmented_matrix_latex(matrix: List[List[Number]], precision: int = 6) -> str:
	if not matrix:
		return "\\left[\\;\\right]"

	cols = len(matrix[0])
	column_spec = "c" * (cols - 1) + "|c"
	lines = []
	for row in matrix:
		lines.append(" & ".join(latex_number(value, precision) for value in row))
	body = " \\\\ ".join(lines)
	return f"\\left[\\begin{{array}}{{{column_spec}}}{body}\\end{{array}}\\right]"


def matrix_latex(matrix: List[List[Number]], precision: int = 6) -> str:
	if not matrix:
		return "\\left[\\;\\right]"
	lines = [" & ".join(latex_number(value, precision) for value in row) for row in matrix]
	body = " \\\\ ".join(lines)
	return f"\\begin{{bmatrix}}{body}\\end{{bmatrix}}"


def system_latex(matrix: List[List[Number]], precision: int = 6) -> str:
	"""Render an augmented matrix as a linear system of equations."""

	if not matrix:
		return ""

	n_vars = len(matrix[0]) - 1
	lines = []
	for row in matrix:
		terms: List[str] = []
		for col in range(n_vars):
			term = _linear_term(row[col], variable_latex(col), not terms)
			if term:
				terms.append(term)
		left = "".join(terms) if terms else "0"
		right = latex_number(row[n_vars], precision)
		lines.append(f"{left} &= {right}")
	return "\\begin{aligned}" + " \\\\ ".join(lines) + "\\end{aligned}"


def solution_vector_latex(solution: Iterable[Number], precision: int = 6) -> str:
	values = " \\\\ ".join(latex_number(value, precision) for value in solution)
	return f"\\begin{{bmatrix}}{values}\\end{{bmatrix}}"


def parametric_latex(entry: dict, precision: int = 6) -> str:
	"""Render one parametric equation such as x_1 = 2 - 3t."""

	left = variable_latex(int(entry["col"]))
	right = _expression_latex(entry.get("const", 0), entry.get("terms", []), precision)
	return f"{left} &= {right}"


def parametric_system_latex(entries: List[dict], precision: int = 6) -> str:
	lines = [parametric_latex(entry, precision) for entry in entries]
	return "\\begin{aligned}" + " \\\\ ".join(lines) + "\\end{aligned}"


def _linear_term(coefficient: Number, variable: str, first: bool) -> str:
	coefficient_text = latex_number(coefficient)
	if coefficient_text == "0":
		return ""
	if coefficient_text == "1":
		body = variable
	elif coefficient_text == "-1":
		body = f"-{variable}"
	else:
		body = f"{coefficient_text}{variable}"

	if first:
		return body
	if body.startswith("-"):
		return f" - {body[1:]}"
	return f" + {body}"


def _expression_latex(constant: Number, terms: List[Tuple[Number, str]], precision: int = 6) -> str:
	parts: List[str] = []

	if not isinstance(constant, Fraction) and abs(float(constant)) <= 1e-12:
		constant_text = "0"
	else:
		constant_text = latex_number(constant, precision)

	if constant_text != "0":
		parts.append(constant_text)

	for coefficient, name in terms:
		coefficient_text = latex_number(coefficient, precision)
		if coefficient_text == "0":
			continue
		if coefficient_text == "1":
			body = name
		elif coefficient_text == "-1":
			body = f"-{name}"
		else:
			body = f"{coefficient_text}{name}"
		if not parts:
			parts.append(body)
		elif body.startswith("-"):
			parts.append(f" - {body[1:]}")
		else:
			parts.append(f" + {body}")

	if not parts:
		return "0"
	return "".join(parts)
