import streamlit as st


def load_css():
    st.markdown(
        """
<style>

/* ================================
   Google Font
================================ */

html,
body,
.stApp,
[class*="css"] {
    font-family: "Inter", sans-serif;
}


/* ================================
   Main Background
================================ */

.stApp{
    background:
    radial-gradient(circle at top left,#0f172a,#020617 70%);
    color:white;
}

/* Remove Streamlit header */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* ================================
   Main Container
================================ */

.block-container{
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
    max-width:1600px;
}

/* ================================
   Sidebar
================================ */

section[data-testid="stSidebar"]{
    background:rgba(15,23,42,.75);
    backdrop-filter:blur(20px);
    border-right:1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* ================================
   KPI Cards
================================ */

.metric-card{

    background:rgba(255,255,255,.08);

    backdrop-filter:blur(18px);

    border:1px solid rgba(255,255,255,.12);

    border-radius:18px;

    padding:25px;

    transition:.35s;

    box-shadow:
    0 8px 32px rgba(0,0,0,.30);

}

.metric-card:hover{

    transform:translateY(-5px);

    box-shadow:
    0 10px 40px rgba(0,229,255,.15);

}

.metric-title{

    color:#94a3b8;

    font-size:14px;

    letter-spacing:1px;

    text-transform:uppercase;

}

.metric-value{

    font-size:42px;

    font-weight:700;

    color:white;

    margin-top:10px;

}

/* ================================
   Glass Container
================================ */

.glass{

    background:rgba(255,255,255,.06);

    backdrop-filter:blur(16px);

    border:1px solid rgba(255,255,255,.08);

    border-radius:20px;

    padding:20px;

    margin-bottom:25px;

    box-shadow:
    0 8px 24px rgba(0,0,0,.25);

}

/* ================================
   Charts
================================ */

.js-plotly-plot{

    border-radius:18px;

    overflow:hidden;

}

/* ================================
   Dataframe
================================ */

div[data-testid="stDataFrame"]{

    background:rgba(255,255,255,.05);

    border-radius:18px;

    border:1px solid rgba(255,255,255,.08);

    overflow:hidden;

}

/* ================================
   Buttons
================================ */

.stButton>button{

    width:100%;

    border:none;

    border-radius:12px;

    padding:12px;

    color:white;

    background:linear-gradient(
        135deg,
        #2563eb,
        #06b6d4
    );

    transition:.3s;

    font-weight:600;

}

.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:
    0 8px 25px rgba(37,99,235,.45);

}

/* ================================
   Metrics
================================ */

div[data-testid="metric-container"]{

    background:rgba(255,255,255,.08);

    border-radius:18px;

    padding:20px;

    border:1px solid rgba(255,255,255,.08);

    backdrop-filter:blur(20px);

    transition:.3s;

}

div[data-testid="metric-container"]:hover{

    transform:translateY(-5px);

}

/* ================================
   Images
================================ */

img{

    border-radius:18px;

}

/* ================================
   Scrollbar
================================ */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-track{

    background:#111827;

}

::-webkit-scrollbar-thumb{

    background:#3b82f6;

    border-radius:20px;

}

/* ================================
   Title
================================ */

.dashboard-title{

    font-size:42px;

    font-weight:700;

    color:white;

}

.dashboard-subtitle{

    color:#94a3b8;

    font-size:18px;

}

/* ================================
   Status Badge
================================ */

.badge{

    display:inline-block;

    padding:6px 12px;

    border-radius:30px;

    background:#00c853;

    color:white;

    font-size:13px;

    font-weight:600;

}

/* ================================
   Snapshot Cards
================================ */

.snapshot{

    background:rgba(255,255,255,.06);

    border-radius:18px;

    padding:15px;

    border:1px solid rgba(255,255,255,.08);

}

/* ================================
   Tables
================================ */

table{

    border-radius:15px;

    overflow:hidden;

}

/* ================================
   Animations
================================ */

@keyframes fadeIn{

from{

opacity:0;
transform:translateY(20px);

}

to{

opacity:1;
transform:translateY(0px);

}

}

.glass,
.metric-card,
div[data-testid="metric-container"]{

animation:fadeIn .6s ease;

}

</style>
""",
        unsafe_allow_html=True,
    )