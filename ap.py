import streamlit as st
import pandas as pd
import plotly.express as px
import glob


# Page configuration
st.set_page_config(
    page_title="Ransomware Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Ransomware Attacks Dashboard")
st.write("Analysis of Ransomware Attacks Data")


# Load dataset
@st.cache_data
def load_data():

    files = glob.glob("data/*.csv")

    if len(files) == 0:
        st.error("❌ No CSV file found inside the data folder.")
        st.stop()

    df = pd.read_csv(files[0])

    return df


# IMPORTANT: Load data here
df = load_data()
# Clean column names
df.columns = df.columns.str.strip()

# Sidebar filters
st.sidebar.header("🔎 Filters")

if "sector" in df.columns:
    sectors = st.sidebar.multiselect(
        "Select Sector",
        options=df["sector"].dropna().unique()
    )

    if sectors:
        df = df[df["sector"].isin(sectors)]

# Sidebar
st.sidebar.header("📊 Dashboard")
st.sidebar.write(f"Rows: {df.shape[0]}")
st.sidebar.write(f"Columns: {df.shape[1]}")


# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("📋 Total Records", len(df))

st.divider()
st.subheader("📊 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Attacks", len(df))

if "Target" in df.columns:
    col2.metric("Targets", df["Target"].nunique())

if "sector" in df.columns:
    col3.metric("Sectors", df["sector"].nunique())

col4.metric("Dataset Columns", len(df.columns))

# Dataset preview
st.subheader("📋 Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)
if "cost" in df.columns:

    numeric_cost = pd.to_numeric(
        df["cost"],
        errors="coerce"
    )

    valid_cost = numeric_cost.dropna()

    if not valid_cost.empty:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Average Cost",
            f"{valid_cost.mean():,.2f}"
        )

        col2.metric(
            "📈 Maximum Cost",
            f"{valid_cost.max():,.2f}"
        )

        col3.metric(
            "📉 Minimum Cost",
            f"{valid_cost.min():,.2f}"
        )
# Attacks by Sector
if "sector" in df.columns:

    st.divider()

    st.subheader("📊 Ransomware Attacks by Sector")

    sector_counts = (
        df["sector"]
        .dropna()
        .replace("None", pd.NA)
        .dropna()
        .value_counts()
        .reset_index()
    )

    sector_counts.columns = ["Sector", "Number of Attacks"]

    fig = px.bar(
        sector_counts,
        x="Sector",
        y="Number of Attacks",
        title="Number of Attacks by Sector"
    )

    st.plotly_chart(fig, use_container_width=True)
    
# Organisation Size
if "organisation size 1,5,10,25,100,300" in df.columns:

    st.subheader("🏢 Attacks by Organisation Size")

    size_counts = (
        df["organisation size 1,5,10,25,100,300"]
        .value_counts()
        .reset_index()
    )

    size_counts.columns = ["Organisation Size", "Number of Attacks"]

    fig2 = px.pie(
        size_counts,
        names="Organisation Size",
        values="Number of Attacks",
        title="Distribution of Targeted Organisation Sizes"
    )

    st.plotly_chart(fig2, use_container_width=True)
# Show columns for now
st.subheader("🔎 Dataset Columns")
st.write(list(df.columns))
if "sector" in df.columns:

    st.subheader("🏢 Attacks by Sector")

    sector_counts = (
        df["sector"]
        .value_counts()
        .reset_index()
    )

    sector_counts.columns = [
        "Sector",
        "Number of Attacks"
    ]

    fig = px.bar(
        sector_counts,
        x="Sector",
        y="Number of Attacks",
        title="Number of Ransomware Attacks by Sector"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    st.subheader("🏆 Top 10 Targeted Sectors")

top_sectors = (
    df["sector"]
    .dropna()
    .replace("None", pd.NA)
    .dropna()
    .value_counts()
    .head(10)
    .reset_index()
)

top_sectors.columns = ["Sector", "Number of Attacks"]

fig = px.bar(
    top_sectors,
    x="Number of Attacks",
    y="Sector",
    orientation="h",
    title="Top 10 Most Targeted Sectors"
)
st.plotly_chart(fig, use_container_width=True)
if "cost" in df.columns:

    cost_data = df.copy()

    cost_data["cost_numeric"] = pd.to_numeric(
        cost_data["cost"],
        errors="coerce"
    )

    cost_data = cost_data.dropna(
        subset=["cost_numeric"]
    )

    if not cost_data.empty:

        st.subheader("💰 Ransomware Attack Cost Analysis")
if "cost" in df.columns:

    cost_numeric = pd.to_numeric(
        df["cost"],
        errors="coerce"
    ).dropna()

    if not cost_numeric.empty:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Average Cost",
            f"{cost_numeric.mean():,.2f}"
        )

        col2.metric(
            "📈 Maximum Cost",
            f"{cost_numeric.max():,.2f}"
        )

        col3.metric(
            "📉 Minimum Cost",
            f"{cost_numeric.min():,.2f}"
        )
        fig4 = px.histogram(
            cost_data,
            x="cost_numeric",
            nbins=20,
            title="Distribution of Ransomware Attack Costs"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )
         