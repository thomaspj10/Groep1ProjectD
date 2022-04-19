import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def create_simple_line_chart():
    data = [[2, 4], [4, 16], [8, 25], [16, 49], [32, 81]]

    st.line_chart(data)
    
def create_simple_diagrams():
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["a", "b", "c"]
    )
    
    st.area_chart(chart_data)
    
    bar_chart_data = pd.DataFrame({
        "a": ["a", "b", "c", "d", "e"],
        "b": [28, 55, 43, 91, 81]
    })
    
    chart = alt.Chart(bar_chart_data).mark_bar().encode(
        x="a",
        y="b"
    )
    st.altair_chart(chart, use_container_width=True)
    