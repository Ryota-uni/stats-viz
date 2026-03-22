import streamlit as st


def render_data_sources() -> None:
    st.subheader("Data Sources")

    with st.container(horizontal=True):
        st.link_button(
            label="FAOSTAT",
            url="https://www.fao.org/faostat/en/#home",
            icon="➡",
            icon_position="right",
        )
        st.link_button(
            label="WDI",
            url="https://databank.worldbank.org/source/world-development-indicators",
            icon="➡",
            icon_position="right",
        )