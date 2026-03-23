import streamlit as st
import plotly.express as px

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
    fig = px.scatter(
        df,
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