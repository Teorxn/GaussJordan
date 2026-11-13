from __future__ import annotations

from typing import List

import streamlit as st


def render_vector_plot(vectors: List[List[float]]) -> None:
	if not vectors:
		return
	dim = len(vectors[0])
	if dim not in {2, 3}:
		st.info("Vector plot is available only for 2D or 3D data")
		return
	st.info("Vector plot not implemented yet")
