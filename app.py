import streamlit as st

from Core.system_solver import solve_system
from ui.classroom import render_classroom
from ui.inputs import render_input_panel
from ui.results import render_results, render_results_placeholder
from ui.styles import inject_css, render_header


def main() -> None:
	st.set_page_config(
		page_title="Eliminación Gaussiana · Daniely Fernández Pérez",
		layout="wide",
	)

	inject_css()
	render_header()

	input_data = render_input_panel()

	if input_data is not None:
		try:
			results = solve_system(
				input_data["matrix"],
				method=input_data["method"],
				exact=input_data["exact"],
				record_steps=input_data["options"]["show_steps"],
			)
			st.session_state["system_payload"] = {
				"results": results,
				"options": input_data["options"],
			}
		except Exception as exc:  # pragma: no cover - defensa de la interfaz
			st.error(f"No se pudo resolver el sistema: {exc}")

	payload = st.session_state.get("system_payload")

	if payload:
		render_results(payload["results"], payload["options"])
		render_classroom(payload["results"], payload["options"])
	else:
		render_results_placeholder()


if __name__ == "__main__":
	main()
