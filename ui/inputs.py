from __future__ import annotations

from typing import Dict

import streamlit as st

from utils.validators import parse_augmented_matrix


PRESETS: Dict[str, Dict[str, object]] = {
	"Sistema 3×3 · solución única": {
		"matrix": "1, 2, 0, 5\n0, 1, 0, 2\n1, 0, 1, 4",
		"exact": True,
		"note": "Coeficientes enteros y pivotes iguales a 1: el proceso no produce fracciones.",
	},
	"Sistema 3×3 · infinitas soluciones": {
		"matrix": "1, 1, 0, 3\n0, 1, 1, 4\n1, 2, 1, 7",
		"exact": True,
		"note": "La tercera ecuación es la suma de las dos primeras: queda una variable libre.",
	},
	"Sistema 3×3 · incompatible": {
		"matrix": "1, 2, 3, 4\n0, 1, 1, 2\n1, 3, 4, 7",
		"exact": True,
		"note": "La tercera ecuación contradice a las dos primeras: aparece 0 = 1.",
	},
	"Sistema 2×2 · solución única": {
		"matrix": "1, 2, 5\n2, 5, 9",
		"exact": True,
		"note": "Sistema pequeño con solución entera y pivotes iguales a 1.",
	},
	"Sistema 4×4 · coeficientes enteros": {
		"matrix": "1, 2, 0, 0, 5\n0, 1, 3, 0, 11\n0, 0, 1, 0, 3\n1, 0, 0, 1, 5",
		"exact": True,
		"note": "Pivotes iguales a 1 y resultados enteros en todos los pasos.",
	},
}
CUSTOM_LABEL = "Personalizado"
METHOD_LABELS = {
	"Gauss (forma escalonada)": "gauss",
	"Gauss-Jordan (RREF)": "gauss-jordan",
}
DEFAULT_PRESET = "Sistema 3×3 · solución única"


def render_input_panel() -> Dict[str, object] | None:
	st.markdown(
		'<div class="section-head"><div class="section-title">Sistema de ecuaciones</div></div>',
		unsafe_allow_html=True,
	)
	st.markdown(
		'<div class="panel-note">Escribe la matriz aumentada [A | b] y elige el método.</div>',
		unsafe_allow_html=True,
	)

	_initialize_state()

	setup_left, setup_right = st.columns([1.15, 1], gap="large")
	with setup_left:
		st.selectbox(
			"Ejemplo guiado",
			list(PRESETS.keys()) + [CUSTOM_LABEL],
			key="preset_label",
			on_change=_apply_preset,
			help="Carga un sistema de prueba o escribe el tuyo con la opción Personalizado.",
		)
		preset = PRESETS.get(st.session_state.get("preset_label"))
		if preset:
			st.caption(str(preset["note"]))

	with setup_right:
		method_label = st.radio(
			"Método",
			list(METHOD_LABELS.keys()),
			key="method_choice",
			horizontal=True,
		)

	method = METHOD_LABELS[method_label]
	description = (
		"Reduce la matriz a forma escalonada y resuelve por sustitución regresiva."
		if method == "gauss"
		else "Reduce la matriz hasta la forma escalonada reducida (RREF) y lee la solución directamente."
	)
	st.markdown(
		f'<div class="panel-note"><b>{method_label}</b>: {description}</div>',
		unsafe_allow_html=True,
	)

	with st.form("system_form"):
		body_left, body_right = st.columns([1.7, 1], gap="large")

		with body_left:
			st.text_area(
				"Matriz aumentada (una fila por línea)",
				key="matrix_text",
				height=190,
				placeholder="2, 1, -1, 8\n-3, -1, 2, -11\n-2, 1, 2, -3",
			)
			st.markdown(
				'<div class="panel-note">Separa los valores con comas o espacios. La última columna corresponde a <b>b</b>. '
				'Puedes usar <code>1/2</code> para fracciones.</div>',
				unsafe_allow_html=True,
			)

		with body_right:
			st.markdown('<div class="mini-title">Opciones</div>', unsafe_allow_html=True)
			st.checkbox("Fracciones exactas", key="exact_mode")
			st.checkbox("Registrar pasos", key="show_steps")

		submitted = st.form_submit_button("Resolver")

	if not submitted:
		return None

	exact = bool(st.session_state.get("exact_mode", False))
	matrix, error = parse_augmented_matrix(st.session_state.get("matrix_text", ""), exact=exact)
	if error:
		st.error(f"✗ {error}")
		return None

	options = {
		"show_steps": bool(st.session_state.get("show_steps", True)),
		"method_label": method_label,
	}

	return {
		"matrix": matrix,
		"method": method,
		"exact": exact,
		"options": options,
	}


def _initialize_state() -> None:
	if "matrix_text" not in st.session_state:
		st.session_state["matrix_text"] = PRESETS[DEFAULT_PRESET]["matrix"]
	if "preset_label" not in st.session_state:
		st.session_state["preset_label"] = DEFAULT_PRESET
	if "exact_mode" not in st.session_state:
		st.session_state["exact_mode"] = bool(PRESETS[DEFAULT_PRESET]["exact"])
	if "method_choice" not in st.session_state:
		st.session_state["method_choice"] = "Gauss-Jordan (RREF)"
	if "show_steps" not in st.session_state:
		st.session_state["show_steps"] = True


def _apply_preset() -> None:
	preset = PRESETS.get(st.session_state.get("preset_label"))
	if not preset:
		return
	st.session_state["matrix_text"] = preset["matrix"]
	st.session_state["exact_mode"] = bool(preset["exact"])
