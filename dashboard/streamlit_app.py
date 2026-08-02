# ==========================================================
# Intelligent Surveillance Analytics Dashboard
# ==========================================================

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from components import (
    dashboard_header,
    metric_card,
    live_camera,
    snapshot_gallery,
    section,
)

from charts import (
    object_distribution,
    category_share,
    detection_timeline,
    top_objects,
    hourly_activity,
    system_health,
    intrusion_chart,
)


from styles import load_css

# ==========================================================
# Load Glass CSS
# ==========================================================

load_css()

from utils import (
    BASE_DIR,
    load_tracking_data,
    dashboard_stats,
    get_class_distribution,
    camera_status,
    snapshot_count,
    database_size,
)

from components import (
    dashboard_header,
    metric_card,
)

from charts import (
    object_distribution,
    category_share,
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Surveillance AI Analytics",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# Auto Refresh Every 5 Seconds
# ==========================================================

st_autorefresh(
    interval=5000,
    key="dashboard_refresh",
)



# ==========================================================
# Header
# ==========================================================

dashboard_header()

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/security-checked.png",
        width=70,
    )

    st.title("AI Surveillance")

    st.markdown("---")

    st.success(f"Camera Status : {camera_status()}")

    st.metric(
        "Snapshots",
        snapshot_count()
    )

    st.metric(
        "Database",
        database_size()
    )

    st.markdown("---")

    auto = st.checkbox(
        "Auto Refresh",
        value=True
    )

    if st.button("Refresh Now"):
        st.rerun()

    st.markdown("---")

    st.subheader("About")

    st.caption(
        """
Real-Time Surveillance Analytics Platform

YOLOv8 • ByteTrack • OpenCV

SQLite • Streamlit • Plotly
"""
    )

# ==========================================================
# Load Tracking Data
# ==========================================================

df = load_tracking_data()

if df.empty:

    st.warning("No tracking data found.")

    st.info(
        "Run\n\n"
        "python main.py\n\n"
        "to generate detections."
    )

    st.stop()

# ==========================================================
# Dashboard Statistics
# ==========================================================

stats = dashboard_stats(df)

total_detections = stats["detections"]

unique_objects = stats["unique_objects"]

active_class = stats["active_class"]

intrusions = stats["intrusions"]

# ==========================================================
# KPI Cards
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:

    metric_card(
        "Total Detections",
        total_detections
    )

with c2:

    metric_card(
        "Unique Objects",
        unique_objects
    )

with c3:

    metric_card(
        "Most Active",
        active_class.upper()
    )

with c4:

    metric_card(
        "Intrusions",
        intrusions
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Prepare Data For Charts
# ==========================================================

class_counts = get_class_distribution(df)

# ==========================================================
# First Row Charts
# ==========================================================

left, right = st.columns(2)

with left:

    st.plotly_chart(
        object_distribution(class_counts),
        use_container_width=True
    )

with right:

    st.plotly_chart(
        category_share(class_counts),
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ========= END OF PART 1 =========

# ==========================================================
# ANALYTICS SECTION
# ==========================================================

section("Analytics Overview")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        detection_timeline(df),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with col2:

    st.plotly_chart(
        top_objects(df),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ==========================================================
# SECOND ROW
# ==========================================================

col3, col4 = st.columns(2)

with col3:

    st.plotly_chart(
        hourly_activity(df),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with col4:

    st.plotly_chart(
        system_health(unique_objects),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ==========================================================
# INTRUSION CHART
# ==========================================================

intrusion_fig = intrusion_chart(df)

if intrusion_fig is not None:

    section("Intrusion Analytics")

    st.plotly_chart(
        intrusion_fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ==========================================================
# LIVE CAMERA + SNAPSHOTS
# ==========================================================

section("Live Monitoring")

left, right = st.columns([2, 1])

with left:

    live_camera(BASE_DIR)

with right:

    st.markdown(
        """
        <div class="glass">
            <h4>System Status</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success("Camera Online")

    st.info(f"Unique Objects : {unique_objects}")

    st.info(f"Total Detections : {total_detections}")

    st.info(f"Most Active : {active_class.upper()}")

    st.info(f"Intrusions : {intrusions}")


# ==========================================================
# SNAPSHOT GALLERY
# ==========================================================

section("Automatic Snapshot Gallery")

snapshot_gallery(BASE_DIR)

st.markdown("<br>", unsafe_allow_html=True)

# ================= END PART 2 =====================

# ==========================================================
# DETECTION LOGS
# ==========================================================

section("Recent Detection Logs")

search = st.text_input(
    "🔍 Search by Object Class or ID",
    placeholder="Example: person, bottle, 3",
)

logs = df.copy()

# Remove unwanted column
if "is_intrusion" in logs.columns:
    logs = logs.drop(columns=["is_intrusion"])

# Search
if search:

    search = search.lower()

    logs = logs[
        logs.astype(str)
        .apply(lambda x: x.str.lower())
        .apply(lambda x: x.str.contains(search))
        .any(axis=1)
    ]

# Format timestamp
logs["timestamp"] = logs["timestamp"].dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)

st.dataframe(
    logs.head(100),
    use_container_width=True,
    height=450,
)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# RECENT OBJECTS
# ==========================================================

section("Latest Unique Objects")

latest = (
    df.sort_values("timestamp", ascending=False)
      .drop_duplicates(subset=["object_id"])
      .head(10)
)

latest["timestamp"] = latest["timestamp"].dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)

st.dataframe(
    latest,
    use_container_width=True,
)


# ==========================================================
# QUICK SUMMARY
# ==========================================================

section("Dashboard Summary")

c1, c2, c3 = st.columns(3)

with c1:

    st.success(
        f"""
### Objects Detected

**{total_detections}**
"""
    )

with c2:

    st.info(
        f"""
### Active Categories

**{df['object_class'].nunique()}**
"""
    )

with c3:

    st.warning(
        f"""
### Latest Object

**{active_class.upper()}**
"""
    )


# ==========================================================
# AUTO REFRESH STATUS
# ==========================================================

section("Dashboard Status")

left, right = st.columns(2)

with left:

    st.success("Dashboard Connected")

    st.write("SQLite Database")

    st.write("Automatic Refresh Enabled")

    st.write("Detection Logs Loaded")

with right:

    st.metric(
        "Rows Loaded",
        len(df)
    )

    st.metric(
        "Snapshot Images",
        snapshot_count()
    )

    st.metric(
        "Database Size",
        database_size()
    )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
<div style='
background:rgba(255,255,255,.06);
padding:25px;
border-radius:18px;
border:1px solid rgba(255,255,255,.08);
text-align:center;
'>

<h3 style="margin-bottom:5px;">
Intelligent Surveillance Analytics Platform
</h3>

<p style="color:#94a3b8;">
Real-Time AI Surveillance using
YOLOv8 • ByteTrack • OpenCV • Streamlit
</p>

<hr>

<div style="display:flex;justify-content:center;gap:40px;flex-wrap:wrap;">

<div>

<b>Computer Vision</b><br>

YOLOv8

</div>

<div>

<b>Tracking</b><br>

ByteTrack

</div>

<div>

<b>Database</b><br>

SQLite

</div>

<div>

<b>Dashboard</b><br>

Streamlit

</div>

</div>

<br>

<p style="font-size:14px;color:#64748b;">
Built for AI Surveillance Analytics
</p>

</div>
""",
unsafe_allow_html=True,
)


# ==========================================================
# SIDEBAR FOOTER
# ==========================================================

st.sidebar.markdown("---")

st.sidebar.caption("Version 1.0")

st.sidebar.caption("AI Surveillance Dashboard")

st.sidebar.caption("Auto Refresh: Every 5 Seconds")