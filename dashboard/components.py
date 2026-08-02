import os
import glob
import streamlit as st
from PIL import Image


# ============================================================
# Dashboard Header
# ============================================================

def dashboard_header():
    st.markdown(
        f"""
<div class="glass">
    <div class="dashboard-title">
        Intelligent Surveillance Analytics
    </div>

    
</div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# KPI Card
# ============================================================

def metric_card(title, value):

    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-title">{title}</div>
    <div class="metric-value">{value}</div>
</div>
""",
        unsafe_allow_html=True,
    )
# ============================================================
# Section Title
# ============================================================

def section(title):

    st.markdown(
        f"""
        <br>

        <div class="glass">

        <h3 style="margin-bottom:0px;">
        {title}
        </h3>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Latest Camera Output
# ============================================================

def live_camera(project_root):

    st.markdown(
        """
        <div class="glass">
        <h4>Live Camera Output</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    video = os.path.join(
        project_root,
        "outputs",
        "tracked_output.mp4",
    )

    if os.path.exists(video):

        st.video(video)

    else:

        st.info("Tracked output video not found.")


# ============================================================
# Snapshot Gallery
# ============================================================

def snapshot_gallery(project_root):

    st.markdown(
        """
        <div class="glass">
        <h4>Latest Snapshots</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    snapshot_dir = os.path.join(
        project_root,
        "outputs",
        "snapshots",
    )

    if not os.path.exists(snapshot_dir):

        st.warning("Snapshot folder not found.")
        return

    images = sorted(

        glob.glob(
            os.path.join(
                snapshot_dir,
                "**",
                "*.jpg",
            ),
            recursive=True,
        ),

        key=os.path.getmtime,
        reverse=True,

    )

    if len(images) == 0:

        st.info("No snapshots captured yet.")
        return

    cols = st.columns(4)

    for i, img in enumerate(images[:12]):

        with cols[i % 4]:

            image = Image.open(img)

            st.image(
                image,
                use_container_width=True,
            )

            st.caption(
                os.path.basename(img)
            )


# ============================================================
# Detection Summary
# ============================================================

def summary_box(df):

    st.markdown(
        """
        <div class="glass">
        <h4>Detection Summary</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:

        st.info("No data available.")
        return

    st.write("Latest Detection")

    latest = df.iloc[0]

    st.success(

        f"""

Object ID : {latest['object_id']}

Class : {latest['object_class']}

Time : {latest['timestamp']}

"""

    )


# ============================================================
# Footer
# ============================================================

def footer():

    st.markdown(
        """
        <br><br>

        <hr>

        <center>

        Surveillance AI Analytics Platform

        <br>

        Built using
        Python • OpenCV • YOLOv8 • Streamlit

        </center>

        """,
        unsafe_allow_html=True,
    )