"""Shared chart colours and Plotly defaults, so every page looks like one app.

Colour rules:
- Use colours by the job they do. Categorical slots go in this fixed order, never cycled.
- One series that matters + context: the matter series gets SERIES[0], context gets CONTEXT grey.
- Projections are dashed, actual data is solid. Nothing else is dashed (not gridlines).
- Never two y-axes on one chart. Index to a common base instead.
- The first three slots pass colourblind checks against each other. Past three, fold into "Other".
"""

import plotly.graph_objects as go

# Categorical slots (validated light-mode palette).
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
CONTEXT = "#b4b2a9"  # de-emphasised series ("everything else")

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'


def style(
    fig: go.Figure,
    *,
    height: int = 420,
    x_title: str | None = None,
    y_title: str | None = None,
    legend_title: str | None = None,
    legend: bool = True,
) -> go.Figure:
    """Apply the shared look to a Plotly figure and return it.

    Rubric: every axis and legend needs a label with units, so pass x_title, y_title and (for two or more
    series) legend_title, for example style(fig, x_title="Year", y_title="TWh per year",
    legend_title="Region (TWh per year)").
    """
    fig.update_layout(
        height=height,
        font=dict(family=FONT, size=14, color=INK_2),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=SURFACE,
        margin=dict(l=10, r=30, t=30, b=10),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", font=dict(family=FONT, color=INK)),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    title=dict(text=legend_title, font=dict(color=INK_2)) if legend_title else None),
    )
    fig.update_xaxes(title=x_title, showgrid=False, linecolor=AXIS, ticks="outside", tickcolor=AXIS, color=MUTED)
    fig.update_yaxes(
        title=y_title, gridcolor=GRID, gridwidth=1, zeroline=True, zerolinecolor=AXIS, color=MUTED, rangemode="tozero"
    )
    return fig


# Pass to st.plotly_chart(..., config=PLOTLY_CONFIG) to hide the busy toolbar.
PLOTLY_CONFIG = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"]}
