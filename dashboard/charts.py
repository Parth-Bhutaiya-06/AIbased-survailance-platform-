# dashboard/charts.py

import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# Common Layout
# =====================================================

def apply_theme(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Inter",
            color="white",
            size=14
        ),

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),

        hoverlabel=dict(
            bgcolor="#111827",
            font_size=14
        )

    )

    fig.update_xaxes(

        showgrid=False,

        zeroline=False,

        showline=False

    )

    fig.update_yaxes(

        gridcolor="rgba(255,255,255,.08)",

        zeroline=False

    )

    return fig


# =====================================================
# Object Distribution
# =====================================================

def object_distribution(class_counts):

    fig = px.bar(

        class_counts,

        x="Object Class",

        y="Count",

        color="Object Class",

        text_auto=True,

        color_discrete_sequence=px.colors.qualitative.Bold,

    )

    fig.update_traces(

        marker_line_width=0,

        textposition="outside"

    )

    fig.update_layout(

        title="Object Distribution",

        showlegend=False

    )

    return apply_theme(fig)


# =====================================================
# Donut Chart
# =====================================================

def category_share(class_counts):

    fig = px.pie(

        class_counts,

        names="Object Class",

        values="Count",

        hole=.65,

        color="Object Class",

        color_discrete_sequence=px.colors.qualitative.Bold,

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    fig.update_layout(

        title="Category Share"

    )

    return apply_theme(fig)


# =====================================================
# Timeline
# =====================================================

def detection_timeline(df):

    timeline = df.copy()

    timeline = timeline.set_index("timestamp")

    timeline = (

        timeline

        .resample("10s")

        .size()

        .reset_index(name="Detections")

    )

    fig = px.area(

        timeline,

        x="timestamp",

        y="Detections",

    )

    fig.update_traces(

        line=dict(

            width=3,

            color="#00E5FF"

        )

    )

    fig.update_layout(

        title="Detection Timeline"

    )

    return apply_theme(fig)


# =====================================================
# Top Objects
# =====================================================

def top_objects(df):

    obj = (

        df

        .groupby("object_class")

        .size()

        .reset_index(name="Count")

        .sort_values(

            "Count",

            ascending=False

        )

    )

    fig = px.bar(

        obj,

        x="Count",

        y="object_class",

        orientation="h",

        color="Count",

        color_continuous_scale="Turbo",

        text_auto=True,

    )

    fig.update_layout(

        title="Top Detected Objects",

        coloraxis_showscale=False

    )

    return apply_theme(fig)


# =====================================================
# Hourly Activity
# =====================================================

def hourly_activity(df):

    hourly = df.copy()

    hourly["Hour"] = hourly["timestamp"].dt.hour

    hourly = (

        hourly

        .groupby("Hour")

        .size()

        .reset_index(name="Detections")

    )

    fig = px.line(

        hourly,

        x="Hour",

        y="Detections",

        markers=True

    )

    fig.update_traces(

        line=dict(

            width=4,

            color="#00FF9C"

        )

    )

    fig.update_layout(

        title="Hourly Activity"

    )

    return apply_theme(fig)


# =====================================================
# Intrusion Chart
# =====================================================

def intrusion_chart(df):

    if "is_intrusion" not in df.columns:

        return None

    intrusion = (

        df

        .groupby("is_intrusion")

        .size()

        .reset_index(name="Count")

    )

    intrusion["Status"] = intrusion["is_intrusion"].map({

        0: "Normal",

        1: "Intrusion"

    })

    fig = px.pie(

        intrusion,

        names="Status",

        values="Count",

        hole=.55,

        color="Status",

        color_discrete_map={

            "Normal": "#00FF9C",

            "Intrusion": "#FF4D6D"

        }

    )

    fig.update_layout(

        title="Intrusion Status"

    )

    return apply_theme(fig)


# =====================================================
# Gauge Chart
# =====================================================

def system_health(total_objects):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=total_objects,

            title={

                "text": "Objects Tracked"

            },

            gauge={

                "axis": {

                    "range": [0, 100]

                },

                "bar": {

                    "color": "#00E5FF"

                },

                "steps": [

                    {

                        "range": [0, 40],

                        "color": "#14532d"

                    },

                    {

                        "range": [40, 70],

                        "color": "#854d0e"

                    },

                    {

                        "range": [70, 100],

                        "color": "#7f1d1d"

                    }

                ]

            }

        )

    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(

            l=20,

            r=20,

            t=40,

            b=20

        )

    )

    return fig