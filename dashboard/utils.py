# dashboard/utils.py

import os
import glob
import sqlite3
import pandas as pd


# ==========================================================
# Paths
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "tracking.db"
)

SNAPSHOT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "snapshots"
)

VIDEO_PATH = os.path.join(
    BASE_DIR,
    "outputs",
    "tracked_output.mp4"
)


# ==========================================================
# Load SQLite Data
# ==========================================================

def load_tracking_data():

    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame()

    try:

        conn = sqlite3.connect(DATABASE_PATH)

        df = pd.read_sql_query(
            """
            SELECT *
            FROM tracking_logs
            ORDER BY id DESC
            """,
            conn,
        )

        conn.close()

        if not df.empty:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                errors="coerce",
            )

        return df

    except Exception as e:

        print(e)

        return pd.DataFrame()


# ==========================================================
# Database Statistics
# ==========================================================

def dashboard_stats(df):

    if df.empty:

        return {
            "detections": 0,
            "unique_objects": 0,
            "active_class": "N/A",
            "intrusions": 0,
        }

    return {

        "detections":
            len(df),

        "unique_objects":
            df["object_id"].nunique(),

        "active_class":
            df["object_class"].mode()[0],

        "intrusions":
            df["is_intrusion"].sum()
            if "is_intrusion" in df.columns
            else 0,

    }


# ==========================================================
# Class Counts
# ==========================================================

def get_class_distribution(df):

    if df.empty:

        return pd.DataFrame(
            columns=[
                "Object Class",
                "Count",
            ]
        )

    unique_objects = df.drop_duplicates(
        subset=["object_id"]
    )

    counts = (

        unique_objects

        ["object_class"]

        .value_counts()

        .reset_index()

    )

    counts.columns = [

        "Object Class",

        "Count",

    ]

    return counts


# ==========================================================
# Recent Logs
# ==========================================================

def latest_logs(df, limit=100):

    if df.empty:

        return df

    logs = df.copy()

    if "timestamp" in logs.columns:

        logs["timestamp"] = logs["timestamp"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    if "is_intrusion" in logs.columns:

        logs = logs.drop(
            columns=["is_intrusion"]
        )

    return logs.head(limit)


# ==========================================================
# Snapshot Gallery
# ==========================================================

def latest_snapshots(limit=12):

    if not os.path.exists(SNAPSHOT_DIR):

        return []

    images = glob.glob(

        os.path.join(

            SNAPSHOT_DIR,

            "**",

            "*.jpg",

        ),

        recursive=True,

    )

    images = sorted(

        images,

        key=os.path.getmtime,

        reverse=True,

    )

    return images[:limit]


# ==========================================================
# Latest Snapshot
# ==========================================================

def latest_snapshot():

    images = latest_snapshots(1)

    if len(images):

        return images[0]

    return None


# ==========================================================
# Video Exists
# ==========================================================

def has_video():

    return os.path.exists(VIDEO_PATH)


# ==========================================================
# Recent Objects
# ==========================================================

def latest_objects(df, limit=10):

    if df.empty:

        return pd.DataFrame()

    return (

        df

        [["object_id", "object_class", "timestamp"]]

        .drop_duplicates(
            subset=["object_id"]
        )

        .head(limit)

    )


# ==========================================================
# Active Objects
# ==========================================================

def active_objects(df):

    if df.empty:

        return []

    return (

        df

        ["object_class"]

        .unique()

        .tolist()

    )


# ==========================================================
# Camera Status
# ==========================================================

def camera_status():

    if os.path.exists(VIDEO_PATH):

        return "ONLINE"

    return "OFFLINE"


# ==========================================================
# Storage Usage
# ==========================================================

def snapshot_count():

    return len(

        latest_snapshots(
            99999
        )

    )


# ==========================================================
# Database Size
# ==========================================================

def database_size():

    if not os.path.exists(DATABASE_PATH):

        return "0 KB"

    size = os.path.getsize(
        DATABASE_PATH
    )

    if size < 1024:

        return f"{size} B"

    if size < 1024 * 1024:

        return f"{size/1024:.1f} KB"

    return f"{size/(1024*1024):.2f} MB"