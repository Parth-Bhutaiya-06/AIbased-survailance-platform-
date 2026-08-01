# dashboard/streamlit_app.py
import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# Load environment variables if dotenv is present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Set page configuration
st.set_page_config(
    page_title="Surveillance AI Analytics Dashboard",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom css for aesthetics
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #374151;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎥 Intelligent Surveillance Analytics Dashboard")
st.markdown("Real-time monitoring metrics, detection analytics, and persistent object tracking.")

# Resolve database path dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "tracking.db")

# Sidebar
st.sidebar.header("Navigation & Options")
st.sidebar.markdown("This dashboard displays analytics compiled by the Surveillance AI tracking system.")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

st.sidebar.info("💡 Run `python main.py` in the workspace root to log new data.")

def load_data():
    """
    Loads tracking logs dynamically. Connects to Cloud PostgreSQL if DATABASE_URL is defined,
    otherwise falls back to Local SQLite.
    """
    db_url = os.environ.get("DATABASE_URL")
    
    if db_url:
        try:
            import psycopg2
            conn = psycopg2.connect(db_url)
            
            # Auto-create the table in the cloud if it does not exist yet to prevent query errors
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracking_logs(
                id SERIAL PRIMARY KEY,
                timestamp VARCHAR(50) NOT NULL,
                object_id INTEGER NOT NULL,
                object_class VARCHAR(50) NOT NULL,
                is_intrusion INTEGER DEFAULT 0
            )
            """)
            conn.commit()
            cursor.close()
            
            query = "SELECT * FROM tracking_logs ORDER BY id DESC"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df, "Cloud PostgreSQL"
        except Exception as e:
            st.sidebar.warning(f"Cloud Database connection failed: {e}. Trying local fallback.")

    # Local SQLite
    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame(), None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        query = "SELECT * FROM tracking_logs ORDER BY id DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, "Local SQLite"
    except Exception as e:
        st.error(f"Failed to read local SQLite: {e}")
        return pd.DataFrame(), None

# Fetch Logs
df, db_source = load_data()

# Show Connection Status in Sidebar
if db_source:
    st.sidebar.success(f"🌐 Connected to: {db_source}")
else:
    st.sidebar.warning("⚠️ No data source found!")

# Check database contents
if df.empty:
    st.warning("⚠️ Database not found or empty!")
    st.info("Please run the tracking system first with: `python main.py` to create the database.")
else:
    try:
        # Parse timestamps
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # Metrics Row
        total_detections = len(df)
        unique_objects = df['object_id'].nunique()
        most_active_class = df['object_class'].mode()[0] if not df['object_class'].empty else 'N/A'

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Detections Logged", total_detections)
        with col2:
            st.metric("Total Unique Tracked", unique_objects)
        with col3:
            st.metric("Most Active Category", most_active_class.upper())

        st.markdown("---")

        # Visualizations Section
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📊 Object Class Distribution")
            # Group by unique objects to find the primary class of each object ID
            obj_unique = df.drop_duplicates(subset=['object_id'])
            class_counts = obj_unique['object_class'].value_counts().reset_index()
            class_counts.columns = ['Object Class', 'Count']

            fig_class = px.bar(
                class_counts,
                x='Object Class',
                y='Count',
                color='Object Class',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                text_auto=True
            )
            fig_class.update_layout(showlegend=False, template="plotly_dark")
            st.plotly_chart(fig_class, use_container_width=True)

        with col_right:
            st.subheader("🍰 Object Category Share")
            fig_pie = px.pie(
                class_counts,
                names='Object Class',
                values='Count',
                color='Object Class',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4
            )
            fig_pie.update_layout(template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # Activity Timeline
        st.subheader("📈 Detection Frequency Timeline")
        df_timeline = df.copy()
        df_timeline.set_index('timestamp', inplace=True)
        df_timeline_grouped = df_timeline.resample('10s').size().reset_index(name='Detections')

        fig_timeline = px.area(
            df_timeline_grouped,
            x='timestamp',
            y='Detections',
            labels={'timestamp': 'Time', 'Detections': 'Detections / 10s'},
            color_discrete_sequence=['#3B82F6']
        )
        fig_timeline.update_layout(template="plotly_dark")
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.markdown("---")

        # Detailed Logs - Full width
        st.subheader("📝 Live Tracking Log (Last 100 entries)")
        df_display = df.copy()
        # Drop the is_intrusion column from display to keep it clean
        if 'is_intrusion' in df_display.columns:
            df_display = df_display.drop(columns=['is_intrusion'])
        df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(df_display.head(100), use_container_width=True)

    except Exception as e:
        st.error(f"Error rendering dashboard: {e}")