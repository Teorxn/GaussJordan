from __future__ import annotations

from typing import List

import streamlit as st

from utils.formatter import augmented_matrix_latex, format_matrix


def render_matrix(matrix: List[List[object]], title: str | None = None) -> None:
	if title:
		st.caption(title)
	if not matrix:
		st.write("[]")
		return

	formatted = format_matrix(matrix)
	col_widths = _column_widths(formatted)
	lines = []
	for row in formatted:
		padded = [value.rjust(col_widths[i]) for i, value in enumerate(row)]
		lines.append("  ".join(padded))
	st.code("\n".join(lines))


def render_augmented(matrix: List[List[object]], title: str | None = None) -> None:
	if title:
		st.caption(title)
	if not matrix:
		st.write("[]")
		return
	st.latex(augmented_matrix_latex(matrix))


def _column_widths(matrix: List[List[str]]) -> List[int]:
	widths = [0] * len(matrix[0])
	for row in matrix:
		for index, value in enumerate(row):
			widths[index] = max(widths[index], len(value))
	return widths
