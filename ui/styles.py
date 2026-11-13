import streamlit as st


STUDENT_NAME = "Daniely Fernández Pérez"


def inject_css() -> None:
	st.markdown(
		"""
		<style>
		:root {
			--paper: #f7f6f2;
			--surface: #ffffff;
			--ink: #1f2328;
			--muted: #5d646d;
			--line: #d7d4cc;
			--line-soft: #e8e5de;
			--accent: #24425f;
			--accent-hover: #1a3148;
			--good: #2f6b4f;
			--good-soft: #f0f7f2;
			--warn: #8a5d0a;
			--warn-soft: #fbf5e8;
			--bad: #9b2c2c;
			--bad-soft: #fbf0ef;
		}

		html, body, [class*="css"] {
			font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif !important;
		}

		.stApp {
			background: var(--paper);
		}

		.stApp, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"] {
			color: var(--ink);
		}

		p, span, li, label, td, th {
			color: var(--ink);
		}

		.block-container {
			max-width: 980px !important;
			padding-top: 1.8rem !important;
			padding-bottom: 3rem !important;
		}

		/* ── Encabezado ── */
		.page-head {
			border-bottom: 2px solid var(--accent);
			padding-bottom: 1rem;
			margin-bottom: 1.8rem;
		}

		.page-kicker {
			font-size: 0.72rem;
			letter-spacing: 0.14em;
			text-transform: uppercase;
			color: var(--muted);
		}

		.page-title {
			font-family: Georgia, "Times New Roman", serif !important;
			font-size: 1.95rem;
			font-weight: 600;
			line-height: 1.2;
			margin: 0.35rem 0 0.4rem 0;
			color: var(--ink);
		}

		.page-sub {
			font-size: 0.92rem;
			color: var(--muted);
			margin: 0;
			line-height: 1.5;
		}

		.page-meta {
			margin-top: 0.9rem;
			font-size: 0.82rem;
			color: var(--ink);
		}

		.page-meta b {
			font-weight: 600;
		}

		/* ── Secciones ── */
		.section-head {
			border-bottom: 1px solid var(--line);
			padding-bottom: 0.35rem;
			margin: 1.9rem 0 0.9rem 0;
		}

		.section-title {
			font-family: Georgia, "Times New Roman", serif;
			font-size: 1.2rem;
			font-weight: 600;
			color: var(--ink);
		}

		.mini-title {
			font-size: 0.78rem;
			font-weight: 600;
			color: var(--ink);
			margin: 1rem 0 0.35rem 0;
		}

		.panel-note {
			font-size: 0.82rem;
			color: var(--muted);
			line-height: 1.5;
			margin-top: 0.4rem;
		}

		/* ── Diagnóstico ── */
		.status-panel {
			border: 1px solid var(--line);
			border-left: 4px solid var(--accent);
			border-radius: 4px;
			padding: 0.95rem 1.1rem;
			background: var(--surface);
			margin-bottom: 1rem;
		}

		.status-good {
			border-left-color: var(--good);
			background: var(--good-soft);
		}

		.status-warn {
			border-left-color: var(--warn);
			background: var(--warn-soft);
		}

		.status-bad {
			border-left-color: var(--bad);
			background: var(--bad-soft);
		}

		.status-eyebrow {
			font-size: 0.72rem;
			letter-spacing: 0.06em;
			text-transform: uppercase;
			color: var(--muted);
			margin-bottom: 0.2rem;
		}

		.status-title {
			font-family: Georgia, "Times New Roman", serif;
			font-size: 1.25rem;
			font-weight: 600;
			margin-bottom: 0.25rem;
			color: var(--ink);
		}

		.status-body {
			font-size: 0.86rem;
			color: var(--muted);
			line-height: 1.55;
		}

		/* ── Resumen numérico ── */
		.stat-card {
			border-top: 1px solid var(--line);
			padding: 0.55rem 0 0 0;
			background: transparent;
		}

		.stat-label {
			font-size: 0.72rem;
			letter-spacing: 0.04em;
			text-transform: uppercase;
			color: var(--muted);
			margin-bottom: 0.15rem;
		}

		.stat-value {
			font-family: Georgia, "Times New Roman", serif;
			font-size: 1.35rem;
			font-weight: 600;
			color: var(--ink);
			margin-bottom: 0.1rem;
		}

		.stat-caption {
			font-size: 0.72rem;
			color: var(--muted);
			line-height: 1.4;
		}

		/* ── Avisos ── */
		.callout {
			border: 1px solid var(--line);
			border-left: 3px solid var(--accent);
			border-radius: 3px;
			padding: 0.75rem 0.9rem;
			background: var(--surface);
			font-size: 0.84rem;
			color: var(--ink);
			line-height: 1.55;
			margin: 0.5rem 0;
		}

		.callout.good {
			border-left-color: var(--good);
			background: var(--good-soft);
		}

		.callout.warn {
			border-left-color: var(--warn);
			background: var(--warn-soft);
		}

		.callout.note {
			border-left-color: var(--accent);
			background: #f4f6f8;
		}

		.empty-state {
			border: 1px solid var(--line);
			border-radius: 4px;
			padding: 1.2rem;
			background: var(--surface);
			margin-top: 1rem;
		}

		.empty-title {
			font-family: Georgia, "Times New Roman", serif;
			font-size: 1.05rem;
			font-weight: 600;
			margin-bottom: 0.25rem;
		}

		.empty-body {
			font-size: 0.85rem;
			color: var(--muted);
			line-height: 1.5;
		}

		/* ── Pasos ── */
		.step-head {
			font-size: 0.86rem;
			font-weight: 600;
			color: var(--ink);
			margin: 0.9rem 0 0.2rem 0;
		}

		.step-op {
			font-family: Consolas, "Courier New", monospace;
			font-size: 0.78rem;
			font-weight: 400;
			color: var(--accent);
			margin-left: 0.35rem;
		}

		.step-note {
			font-size: 0.82rem;
			color: var(--muted);
			line-height: 1.5;
			margin-bottom: 0.3rem;
		}

		/* ── Formulario ── */
		[data-testid="stForm"] {
			border: 1px solid var(--line) !important;
			border-radius: 4px !important;
			padding: 1.1rem !important;
			background: var(--surface) !important;
		}

		textarea, input, select {
			border: 1px solid #bfc4ca !important;
			border-radius: 3px !important;
			background: #ffffff !important;
			color: var(--ink) !important;
		}

		textarea:focus, input:focus {
			border-color: var(--accent) !important;
			box-shadow: 0 0 0 2px rgba(36, 66, 95, 0.12) !important;
		}

		textarea::placeholder,
		input::placeholder {
			color: #9aa0a6 !important;
			opacity: 1 !important;
		}

		.stTextArea textarea,
		.stNumberInput input {
			font-family: Consolas, "Courier New", monospace !important;
			font-size: 0.85rem !important;
		}

		div[data-baseweb="select"] > div {
			border: 1px solid #bfc4ca !important;
			border-radius: 3px !important;
			background: #ffffff !important;
		}

		div[data-baseweb="select"] span {
			color: var(--ink) !important;
		}

		label,
		.stCheckbox label,
		.stRadio label,
		.stSelectbox label,
		.stTextArea label,
		.stNumberInput label {
			color: var(--ink) !important;
			font-size: 0.84rem !important;
			font-weight: 600 !important;
		}

		.stCheckbox label span,
		.stRadio label span,
		.stCheckbox [data-testid="stMarkdownContainer"],
		.stRadio [data-testid="stMarkdownContainer"] {
			color: var(--ink) !important;
			font-weight: 400 !important;
			opacity: 1 !important;
		}

		/* ── Botones ── */
		div[data-testid="stFormSubmitButton"],
		.stButton {
			margin-top: 0.4rem;
		}

		div[data-testid="stFormSubmitButton"] button,
		button[data-testid="baseButton-secondaryFormSubmit"],
		button[data-testid="baseButton-primaryFormSubmit"],
		.stButton > button {
			background: var(--accent) !important;
			background-color: var(--accent) !important;
			color: #ffffff !important;
			border: 1px solid var(--accent) !important;
			border-radius: 3px !important;
			box-shadow: none !important;
			padding: 0.55rem 1.25rem !important;
			min-width: 170px !important;
			font-family: "Segoe UI", Arial, sans-serif !important;
			font-size: 0.88rem !important;
			font-weight: 600 !important;
			letter-spacing: 0 !important;
			text-transform: none !important;
		}

		div[data-testid="stFormSubmitButton"] button *,
		button[data-testid="baseButton-secondaryFormSubmit"] *,
		button[data-testid="baseButton-primaryFormSubmit"] *,
		.stButton > button * {
			color: #ffffff !important;
			opacity: 1 !important;
			font-family: "Segoe UI", Arial, sans-serif !important;
			font-size: 0.88rem !important;
			font-weight: 600 !important;
			letter-spacing: 0 !important;
			text-transform: none !important;
		}

		div[data-testid="stFormSubmitButton"] button:hover,
		button[data-testid="baseButton-secondaryFormSubmit"]:hover,
		button[data-testid="baseButton-primaryFormSubmit"]:hover,
		.stButton > button:hover {
			background: var(--accent-hover) !important;
			background-color: var(--accent-hover) !important;
			border-color: var(--accent-hover) !important;
			color: #ffffff !important;
		}

		div[data-testid="stFormSubmitButton"] button:hover *,
		button[data-testid="baseButton-secondaryFormSubmit"]:hover *,
		button[data-testid="baseButton-primaryFormSubmit"]:hover *,
		.stButton > button:hover * {
			color: #ffffff !important;
		}

		div[data-testid="stFormSubmitButton"] button:focus,
		button[data-testid="baseButton-secondaryFormSubmit"]:focus,
		button[data-testid="baseButton-primaryFormSubmit"]:focus,
		.stButton > button:focus {
			background: var(--accent) !important;
			border-color: var(--accent) !important;
			color: #ffffff !important;
			box-shadow: 0 0 0 2px rgba(36, 66, 95, 0.25) !important;
		}

		/* ── Expansores ── */
		[data-testid="stExpander"] {
			border: 1px solid var(--line) !important;
			border-radius: 4px !important;
			background: var(--surface) !important;
			margin-bottom: 0.5rem !important;
		}

		[data-testid="stExpander"] details {
			border: none !important;
		}

		[data-testid="stExpander"] summary {
			font-weight: 600 !important;
			color: var(--ink) !important;
		}

		/* ── Bloques de código ── */
		[data-testid="stCode"],
		.stCode,
		pre {
			border-radius: 3px !important;
			border: 1px solid var(--line) !important;
			background: #f3f2ee !important;
		}

		[data-testid="stCode"] code,
		[data-testid="stCode"] *,
		[data-testid="stCode"] span,
		[data-testid="stCode"] div,
		[data-testid="stCode"] pre,
		[data-testid="stCode"] [class],
		[data-testid="stCode"] [class*="css"],
		.stCode code,
		.stCode *,
		.stCode span,
		.stCode div,
		.stCode [class],
		.stCode [class*="css"],
		pre,
		pre *,
		pre code,
		pre span,
		pre div,
		pre [class],
		pre [class*="css"] {
			font-family: Consolas, "Courier New", monospace !important;
			font-size: 0.84rem !important;
			line-height: 1.5 !important;
			color: var(--ink) !important;
		}

		/* ── Matemáticas ── */
		[data-testid="stLatex"] {
			overflow-x: auto;
			padding: 0.1rem 0;
		}

		hr {
			border: none;
			border-top: 1px solid var(--line);
			margin: 1.4rem 0;
		}

		/* ── Ocultar elementos de Streamlit ── */
		#MainMenu {visibility: hidden;}
		footer {visibility: hidden;}
		header {visibility: hidden;}

		::-webkit-scrollbar {
			width: 8px;
			height: 8px;
		}
		::-webkit-scrollbar-track {
			background: transparent;
		}
		::-webkit-scrollbar-thumb {
			background: #c9c6be;
			border-radius: 4px;
		}
		</style>
		""",
		unsafe_allow_html=True,
	)


def render_header() -> None:
	st.markdown(
		f"""
		<div class="page-head">
			<div class="page-kicker">Álgebra lineal</div>
			<div class="page-title">Eliminación de Gauss y Gauss-Jordan</div>
			<div class="page-sub">
				Resolución de sistemas de ecuaciones lineales con matriz aumentada.
			</div>
			<div class="page-meta">Estudiante: <b>{STUDENT_NAME}</b></div>
		</div>
		""",
		unsafe_allow_html=True,
	)
