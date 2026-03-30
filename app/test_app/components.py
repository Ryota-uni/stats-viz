import streamlit as st
import plotly.express as px
import pandas as pd
# Components for the app - reusable UI elements and functions

#-----------------------------
# Data source rendering
#-----------------------------
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

#-----------------------------
# Page setup
#-----------------------------
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

#-----------------------------
# Time series section rendering 
#-----------------------------
def render_timeseries_section(df_plot, variable, growth_col, indicator_info):
    st.subheader(indicator_info["label"])

    tab_names = ["Level"]

    if indicator_info["log_allowed"]:
        tab_names.append("Log Scale")

    if indicator_info["growth_allowed"]:
        tab_names.append("Growth Rate")

    tabs = st.tabs(tab_names)
    tab_index = 0

    hover_level = (
        "Country: %{fullData.name}<br>"
        "Year: %{x}<br>"
        f"{indicator_info['hover_label']}: "
        f"%{{y{indicator_info['value_format']}}}<br>"
        "<extra></extra>"
    )

    hover_growth = (
        "Country: %{fullData.name}<br>"
        "Year: %{x}<br>"
        "Growth rate: %{y:.2f}%<br>"
        "<extra></extra>"
    )

    # Level
    with tabs[tab_index]:
        fig = px.line(
            df_plot,
            x="year",
            y=variable,
            color="area",
            markers=True,
            title=f"{indicator_info['label']} ({indicator_info['unit']})",
        )
        fig.update_traces(hovertemplate=hover_level)
        fig.update_xaxes(
            title="Year",
            showline=True,
            linewidth=1,
            linecolor="white",
            showgrid=False,
        )
        fig.update_yaxes(
            title=f"{indicator_info['label']} ({indicator_info['unit']})",
            showline=True,
            linewidth=1,
            linecolor="white",
            showgrid=True,
            gridcolor="#E5E5E5",
            gridwidth=1,
            type="linear",
        )
        st.plotly_chart(fig, use_container_width=True)

    tab_index += 1

    # Log Scale
    if indicator_info["log_allowed"]:
        with tabs[tab_index]:
            positive_df = df_plot[df_plot[variable] > 0].copy()

            if positive_df.empty:
                st.info("Log scale is not available because there are no positive values.")
            else:
                fig = px.line(
                    positive_df,
                    x="year",
                    y=variable,
                    color="area",
                    markers=True,
                    title=f"{indicator_info['label']} (log scale)",
                )
                fig.update_traces(hovertemplate=hover_level)
                fig.update_xaxes(
                    title="Year",
                    showline=True,
                    linewidth=1,
                    linecolor="white",
                    showgrid=False,
                )
                fig.update_yaxes(
                    title=f"{indicator_info['label']} (log scale)",
                    showline=True,
                    linewidth=1,
                    linecolor="white",
                    showgrid=True,
                    gridcolor="#E5E5E5",
                    gridwidth=1,
                    type="log",
                )
                st.plotly_chart(fig, use_container_width=True)

        tab_index += 1

    # Growth Rate
    if indicator_info["growth_allowed"]:
        with tabs[tab_index]:
            fig = px.line(
                df_plot,
                x="year",
                y=growth_col,
                color="area",
                markers=True,
                title=f"{indicator_info['label']} Growth Rate (%)",
            )
            fig.update_traces(hovertemplate=hover_growth)
            fig.update_xaxes(
                title="Year",
                showline=True,
                linewidth=1,
                linecolor="white",
                showgrid=False,
            )
            fig.update_yaxes(
                title="Growth rate (%)",
                showline=True,
                linewidth=1,
                linecolor="white",
                showgrid=True,
                gridcolor="#E5E5E5",
                gridwidth=1,
            )
            st.plotly_chart(fig, use_container_width=True)

def make_animated_scatter(
    df,
    x,
    y,
    x_label,
    y_label,
    x_format=".2f",
    y_format=".2f",
    log_x=False,
    log_y=False,
    color="sub_region",
    size=None,
    animation_frame="year",
    animation_group="area",
    hover_name="area",
    size_max=55,
    legend_title="Subregion",
):
    df_plot = df.copy()

    required_cols = [x, y, animation_frame, animation_group, hover_name]
    if color is not None:
        required_cols.append(color)
    if size is not None:
        required_cols.append(size)

    required_cols = list(dict.fromkeys(required_cols))
    df_plot = df_plot.dropna(subset=required_cols).copy()

    df_plot[animation_frame] = pd.to_numeric(df_plot[animation_frame], errors="coerce")
    df_plot = df_plot.dropna(subset=[animation_frame]).copy()
    df_plot[animation_frame] = df_plot[animation_frame].astype(int)

    df_plot = df_plot.sort_values([animation_frame, animation_group]).reset_index(drop=True)
    frame_order = sorted(df_plot[animation_frame].unique().tolist())

    fig = px.scatter(
        df_plot,
        x=x,
        y=y,
        animation_frame=animation_frame,
        animation_group=animation_group,
        hover_name=hover_name,
        color=color,
        size=size,
        log_x=log_x,
        log_y=log_y,
        size_max=size_max,
        category_orders={animation_frame: frame_order},
    )

    fig["layout"].pop("updatemenus", None)

    fig.update_layout(
        legend_title=legend_title,
    )

    fig.update_xaxes(
        title=x_label,
        showline=True,
        linewidth=1,
        linecolor="white",
        showgrid=False,
    )

    fig.update_yaxes(
        title=y_label,
        showline=True,
        linewidth=1,
        linecolor="white",
        showgrid=False,
        gridcolor="#E5E5E5",
        gridwidth=1,
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            f"{x_label}: %{{x:{x_format}}}<br>"
            f"{y_label}: %{{y:{y_format}}}<br>"
            "<extra></extra>"
        )
    )

    return fig


def render_scatter_panel(
    df,
    title,
    x,
    y,
    x_label,
    y_label,
    x_format,
    y_format,
    size,
    key_prefix,
):
    st.subheader(title)

    with st.container():
        log_x = st.toggle("Log X", value=True, key=f"{key_prefix}_log_x")
        log_y = st.toggle("Log Y", value=False, key=f"{key_prefix}_log_y")

    fig = make_animated_scatter(
        df=df,
        x=x,
        y=y,
        x_label=x_label,
        y_label=y_label,
        x_format=x_format,
        y_format=y_format,
        log_x=log_x,
        log_y=log_y,
        size=size,
    )

    st.plotly_chart(fig, use_container_width=True)

#-----------------------------
# Crop-specific components
#-----------------------------
def render_crop_timeseries_section(df_plot, crop_name):
    """
    Render crop-specific time series charts with three tabs:
    Yield, Production, and Area.

    Expected columns in df_plot:
    - year
    - area
    - yield_kg_per_ha
    - production_ton
    - harvested_area_ha
    """

    st.subheader(crop_name["label"])

    tab_yield, tab_production, tab_area = st.tabs(["Yield", "Production", "Area"])

    hover_yield = (
        "Country: %{fullData.name}<br>"
        "Year: %{x}<br>"
        "Yield: %{y:,.2f} kg/ha<br>"
        "<extra></extra>"
    )

    hover_production = (
        "Country: %{fullData.name}<br>"
        "Year: %{x}<br>"
        "Production: %{y:,.0f} ton<br>"
        "<extra></extra>"
    )

    hover_area = (
        "Country: %{fullData.name}<br>"
        "Year: %{x}<br>"
        "Area: %{y:,.0f} ha<br>"
        "<extra></extra>"
    )

    # Yield
    with tab_yield:
        fig = px.line(
            df_plot,
            x="year",
            y="yield_kg_per_ha",
            color="area",
            markers=True,
            title=f"{crop_name['label']} Yield",
        )
        fig.update_traces(hovertemplate=hover_yield)
        fig.update_xaxes(
            title="Year",
            showline=True,
            linewidth=1,
            linecolor="white",
            showgrid=False,
        )
        fig.update_yaxes(
            title="Yield (kg/ha)",
            showline=True,
            linewidth=1,
            linecolor="white",
            showgrid=True,
            gridcolor="#E5E5E5",
            gridwidth=1,
            type="linear",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Production
    with tab_production:
        fig = px.line(
            df_plot,
            x="year",
            y="production_ton",
            color="area",
            markers=True,
            title=f"{crop_name['label']} Production",
        )
        fig.update_traces(hovertemplate=hover_production)
        fig.update_xaxes(
            title="Year",
            showline=True,
            linewidth=1,
            linecolor="white",
            showgrid=False,
        )
        fig.update_yaxes(
            title="Production (ton)",
            showline=True,
            linewidth=1,
            linecolor="white",
            showgrid=True,
            gridcolor="#E5E5E5",
            gridwidth=1,
            type="linear",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Area
    with tab_area:
        fig = px.line(
            df_plot,
            x="year",
            y="area_harvested_ha",
            color="area",
            markers=True,
            title=f"{crop_name['label']} Area",
        )
        fig.update_traces(hovertemplate=hover_area)
        fig.update_xaxes(
            title="Year",
            showline=True,
            linewidth=1,
            linecolor="white",
            showgrid=False,
        )
        fig.update_yaxes(
            title="Area (ha)",
            showline=True,
            linewidth=1,
            linecolor="white",
            showgrid=True,
            gridcolor="#E5E5E5",
            gridwidth=1,
            type="linear",
        )
        st.plotly_chart(fig, use_container_width=True)