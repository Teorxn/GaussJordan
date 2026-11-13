from __future__ import annotations

from typing import Dict, List

import streamlit as st

from utils.explanations import get_explanation
from utils.formatter import (
	format_number,
	parametric_system_latex,
	solution_vector_latex,
	system_latex,
)
from visualizations.matrix_display import render_augmented


STATUS_INFO = {
	"unique": {
		"eyebrow": "Sistema compatible determinado",
		"title": "Solución única",
		"class": "status-good",
	},
	"infinite": {
		"eyebrow": "Sistema compatible indeterminado",
		"title": "Infinitas soluciones",
		"class": "status-warn",
	},
	"inconsistent": {
		"eyebrow": "Sistema incompatible",
		"title": "Sin solución",
		"class": "status-bad",
	},
}


def render_results(results: Dict[str, object], options: Dict[str, object]) -> None:
	st.markdown(
		'<div class="section-head"><div class="section-title">Resultados</div></div>',
		unsafe_allow_html=True,
	)

	status = str(results["status"])
	info = STATUS_INFO[status]

	st.markdown(
		f"""
		<div class="status-panel {info['class']}">
			<div class="status-eyebrow">{info['eyebrow']}</div>
			<div class="status-title">{info['title']}</div>
			<div class="status-body">{get_explanation(status)}</div>
		</div>
		""",
		unsafe_allow_html=True,
	)

	metric_cols = st.columns(4, gap="medium")
	metrics = [
		("Ecuaciones", str(results["n_equations"]), "Filas de la matriz."),
		("Incógnitas", str(results["n_vars"]), "Variables del sistema."),
		("Rango de A", str(results["rank"]), "Pivotes de la matriz de coeficientes."),
		("Rango de [A | b]", str(results["rank_augmented"]), "Pivotes de la matriz ampliada."),
	]
	for column, (label, value, caption) in zip(metric_cols, metrics):
		with column:
			st.markdown(
				f"""
				<div class="stat-card">
					<div class="stat-label">{label}</div>
					<div class="stat-value">{value}</div>
					<div class="stat-caption">{caption}</div>
				</div>
				""",
				unsafe_allow_html=True,
			)

	method = str(results["method"])
	pivot_cols = list(results["pivot_cols"])
	pivot_text = ", ".join(str(col + 1) for col in pivot_cols) if pivot_cols else "ninguna"
	st.markdown(
		f'<div class="panel-note"><b>Método:</b> {options.get("method_label", method)}. '
		f'<b>Columnas pivote:</b> {pivot_text}.</div>',
		unsafe_allow_html=True,
	)

	st.markdown('<div class="mini-title">Matriz y forma final</div>', unsafe_allow_html=True)
	left, right = st.columns(2, gap="large")

	with left:
		render_augmented(results["matrix"])
		st.caption("Matriz aumentada inicial [A | b]")

	with right:
		final_title = "Forma escalonada" if method == "gauss" else "Forma escalonada reducida (RREF)"
		render_augmented(results["final_matrix"])
		st.caption(final_title)

	with st.expander("Ver sistemas de ecuaciones", expanded=False):
		equation_left, equation_right = st.columns(2, gap="large")
		with equation_left:
			st.markdown('<div class="mini-title">Sistema original</div>', unsafe_allow_html=True)
			st.latex(system_latex(results["matrix"]))
		with equation_right:
			st.markdown('<div class="mini-title">Sistema equivalente</div>', unsafe_allow_html=True)
			st.latex(system_latex(results["final_matrix"]))

	st.markdown(
		'<div class="section-head"><div class="section-title">Solución</div></div>',
		unsafe_allow_html=True,
	)
	_render_solution(results)

	st.markdown(
		'<div class="section-head"><div class="section-title">Comprobación</div></div>',
		unsafe_allow_html=True,
	)
	_render_verification(results)


def _render_solution(results: Dict[str, object]) -> None:
	status = str(results["status"])

	if status == "unique":
		solution: List[object] = list(results["solution"])
		st.latex(f"\\mathbf{{x}} = {solution_vector_latex(solution)}")

		values = ", ".join(format_number(value) for value in solution)
		st.markdown(
			f'<div class="callout good">El sistema tiene solución única: '
			f'<b>({values})</b>.</div>',
			unsafe_allow_html=True,
		)

		back_substitution = results.get("back_substitution") or []
		if back_substitution:
			st.markdown('<div class="mini-title">Sustitución regresiva</div>', unsafe_allow_html=True)
			for step in back_substitution:
				var = int(step["var"]) + 1
				pivot = step["pivot"]
				numerator = step["rhs"] - step["subtotal"]
				if pivot == 1:
					st.latex(
						f"x_{{{var}}} = {format_number(numerator)} = "
						f"{format_number(step['value'])}"
					)
				elif pivot == -1:
					st.latex(
						f"x_{{{var}}} = -({format_number(numerator)}) = "
						f"{format_number(step['value'])}"
					)
				else:
					st.latex(
						f"x_{{{var}}} = \\frac{{{format_number(step['rhs'])} - "
						f"({format_number(step['subtotal'])})}}{{{format_number(pivot)}}} = "
						f"{format_number(step['value'])}"
					)
		return

	if status == "infinite":
		parametric = results.get("parametric") or []
		st.latex(parametric_system_latex(list(parametric)))

		param_names = list(results.get("param_names") or [])
		if param_names:
			st.markdown(
				f'<div class="callout note">Variables libres: '
				f'<b>{", ".join(param_names)}</b>. Cada valor de estos parámetros '
				f'produce una solución distinta.</div>',
				unsafe_allow_html=True,
			)

		example = results.get("example_solution") or []
		if example:
			values = ", ".join(format_number(value) for value in example)
			st.markdown(
				f'<div class="panel-note">Ejemplo con todos los parámetros iguales a 1: '
				f'({values}).</div>',
				unsafe_allow_html=True,
			)
		return

	row_index = results.get("contradiction_row")
	if row_index is not None:
		row = results["final_matrix"][int(row_index)]
		rhs = format_number(row[-1])
		st.markdown(
			f'<div class="callout warn">La fila {int(row_index) + 1} conduce a '
			f'<b>0 = {rhs}</b>, una igualdad imposible. El sistema no tiene solución.</div>',
			unsafe_allow_html=True,
		)
	else:
		st.markdown(
			'<div class="callout warn">El rango de A es menor que el rango de la matriz '
			'ampliada. El sistema no tiene solución.</div>',
			unsafe_allow_html=True,
		)


def _render_verification(results: Dict[str, object]) -> None:
	checks = results.get("verification") or []

	if not checks:
		st.markdown(
			'<div class="panel-note">No hay una solución que sustituir porque el sistema '
			'es incompatible.</div>',
			unsafe_allow_html=True,
		)
		return

	if str(results["status"]) == "infinite":
		st.markdown(
			'<div class="panel-note">Se comprueba el caso particular con todos los '
			'parámetros iguales a 1.</div>',
			unsafe_allow_html=True,
		)

	lines = []
	for check in checks:
		row = int(check["row"]) + 1
		lhs = format_number(check["lhs"])
		rhs = format_number(check["rhs"])
		mark = "correcto" if check["ok"] else "revisar"
		lines.append(f"E{row}:  {lhs} = {rhs}    [{mark}]")

	st.code("\n".join(lines))

	if all(bool(check["ok"]) for check in checks):
		st.markdown(
			'<div class="callout good">Todas las ecuaciones se satisfacen con el '
			'vector encontrado.</div>',
			unsafe_allow_html=True,
		)
	else:
		st.markdown(
			'<div class="callout warn">Alguna ecuación no se satisface. Revisa los '
			'datos o aumenta la precisión.</div>',
			unsafe_allow_html=True,
		)


def render_results_placeholder() -> None:
	st.markdown(
		"""
		<div class="section-head"><div class="section-title">Resultados</div></div>
		<div class="empty-state">
			<div class="empty-title">Sin resultados todavía</div>
			<div class="empty-body">
				Escribe una matriz aumentada y presiona <b>Resolver</b>.
			</div>
		</div>
		""",
		unsafe_allow_html=True,
	)
