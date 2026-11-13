from __future__ import annotations

from typing import Dict

import streamlit as st

from utils.explanations import get_explanation
from utils.formatter import format_number, system_latex
from visualizations.matrix_display import render_augmented


def render_classroom(results: Dict[str, object], options: Dict[str, object]) -> None:
	st.markdown(
		'<div class="section-head"><div class="section-title">Procedimiento</div></div>',
		unsafe_allow_html=True,
	)

	method = str(results["method"])
	method_title = "Eliminación gaussiana" if method == "gauss" else "Eliminación de Gauss-Jordan"

	st.markdown(
		f'<div class="callout note"><b>{method_title}.</b> {get_explanation(method)}</div>',
		unsafe_allow_html=True,
	)

	with st.expander("1. Planteamiento", expanded=True):
		st.markdown(
			"Escribimos el sistema y lo llevamos a la matriz aumentada $[A \\mid b]$."
		)
		st.latex(system_latex(results["matrix"]))
		render_augmented(results["matrix"])
		st.markdown(
			f'<div class="panel-note">El sistema tiene <b>{results["n_equations"]}</b> '
			f'ecuaciones y <b>{results["n_vars"]}</b> incógnitas. Las primeras columnas '
			f'forman <b>A</b> y la última es el término independiente <b>b</b>.</div>',
			unsafe_allow_html=True,
		)

	with st.expander(f"2. {method_title}", expanded=True):
		steps = results.get("steps") or []
		if not options.get("show_steps", True):
			st.markdown(
				'<div class="callout note">Los pasos están desactivados. Activa '
				'<b>Registrar pasos</b> en la entrada y vuelve a resolver.</div>',
				unsafe_allow_html=True,
			)
		elif steps:
			st.markdown(f"Se registraron **{len(steps)}** operaciones elementales por filas.")
			for index, step in enumerate(steps, start=1):
				st.markdown(
					f'<div class="step-head">Paso {index} '
					f'<span class="step-op">{step["label"]}</span></div>',
					unsafe_allow_html=True,
				)
				st.markdown(f'<div class="step-note">{_explain_step(step)}</div>', unsafe_allow_html=True)

				matrix_col, equation_col = st.columns([1, 1.25], gap="large")
				with matrix_col:
					render_augmented(step["matrix"])
				with equation_col:
					st.latex(system_latex(step["matrix"]))
		else:
			st.markdown(
				'<div class="callout">La matriz ya estaba en la forma buscada: no se '
				'requirieron operaciones elementales.</div>',
				unsafe_allow_html=True,
			)

		st.markdown('<div class="mini-title">Matriz final</div>', unsafe_allow_html=True)
		render_augmented(results["final_matrix"])

		pivots = list(results["pivot_cols"])
		free_cols = list(results["free_cols"])
		pivot_text = ", ".join(str(col + 1) for col in pivots) if pivots else "—"
		free_text = ", ".join(str(col + 1) for col in free_cols) if free_cols else "ninguna"
		st.markdown(
			f'<div class="panel-note"><b>Pivotes:</b> {pivot_text} &nbsp;·&nbsp; '
			f'<b>Columnas libres:</b> {free_text} &nbsp;·&nbsp; '
			f'<b>Rango:</b> {results["rank"]}</div>',
			unsafe_allow_html=True,
		)


def _explain_step(step: Dict[str, object]) -> str:
	kind = str(step.get("kind", ""))

	if kind == "swap":
		return (
			f"Intercambiamos la fila **{int(step['row']) + 1}** con la fila "
			f"**{int(step['other']) + 1}** para colocar un pivote no nulo en la posición adecuada."
		)

	if kind == "scale":
		factor = format_number(step.get("factor", 0))
		return (
			f"Dividimos la fila **{int(step['row']) + 1}** entre **{factor}** para que el "
			f"pivote de la columna {int(step['pivot_col']) + 1} sea 1."
		)

	if kind == "eliminate":
		factor = step.get("factor", 0)
		is_negative = factor < 0
		magnitude = -factor if is_negative else factor
		action = "Sumamos" if is_negative else "Restamos"
		return (
			f"{action} **{format_number(magnitude)}** veces la fila **{int(step['pivot_row']) + 1}** a la fila "
			f"**{int(step['row']) + 1}** para anular el coeficiente de la columna "
			f"{int(step['pivot_col']) + 1}."
		)

	return "Aplicamos una operación elemental por filas."
