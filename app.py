
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Content Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("final_content_data.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# -----------------------------
# TITLE
# -----------------------------
st.title("📊 Content Analytics Dashboard")
st.markdown(
    "Analyze content performance, engagement, retention and viral potential."
)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

topics = st.sidebar.multiselect(
    "Topic",
    options=sorted(df["topic"].dropna().unique()),
    default=sorted(df["topic"].dropna().unique())
)

formats = st.sidebar.multiselect(
    "Format",
    options=sorted(df["format"].dropna().unique()),
    default=sorted(df["format"].dropna().unique())
)

viral_options = st.sidebar.multiselect(
    "Viral Category",
    options=sorted(df["viral_category"].dropna().unique()),
    default=sorted(df["viral_category"].dropna().unique())
)

filtered_df = df[
    (df["topic"].isin(topics)) &
    (df["format"].isin(formats)) &
    (df["viral_category"].isin(viral_options))
]

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Content",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Total Views",
        f"{filtered_df['views'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Avg Engagement Rate",
        f"{filtered_df['engagement_rate'].mean():.2f}%"
    )

with col4:
    st.metric(
        "Avg Retention Rate",
        f"{filtered_df['retention_rate'].mean():.2f}%"
    )

# -----------------------------
# SECOND KPI ROW
# -----------------------------
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Total Likes",
        f"{filtered_df['likes'].sum():,.0f}"
    )

with col6:
    st.metric(
        "Total Comments",
        f"{filtered_df['comments'].sum():,.0f}"
    )

with col7:
    st.metric(
        "Total Shares",
        f"{filtered_df['shares'].sum():,.0f}"
    )

with col8:
    st.metric(
        "Avg Viral Score",
        f"{filtered_df['viral_score'].mean():.2f}"
    )

# -----------------------------
# PERFORMANCE BY FORMAT
# -----------------------------
st.subheader("📈 Performance by Content Format")

format_perf = (
    filtered_df.groupby("format")
    .agg(
        views=("views", "sum"),
        engagement=("engagement_rate", "mean"),
        retention=("retention_rate", "mean")
    )
    .reset_index()
)

fig1 = px.bar(
    format_perf,
    x="format",
    y="views",
    title="Total Views by Content Format",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# ENGAGEMENT ANALYSIS
# -----------------------------
st.subheader("💬 Engagement Analysis")

col1, col2 = st.columns(2)

with col1:

    topic_engagement = (
        filtered_df.groupby("topic")["engagement_rate"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig2 = px.bar(
        topic_engagement,
        x="engagement_rate",
        y="topic",
        orientation="h",
        title="Average Engagement Rate by Topic",
        text_auto=".2f"
    )

    st.plotly_chart(fig2, use_container_width=True)

with col2:

    hook_engagement = (
        filtered_df.groupby("hook_type")["engagement_rate"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig3 = px.bar(
        hook_engagement,
        x="hook_type",
        y="engagement_rate",
        title="Engagement Rate by Hook Type",
        text_auto=".2f"
    )

    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# RETENTION ANALYSIS
# -----------------------------
st.subheader("🎥 Retention Analysis")

fig4 = px.scatter(
    filtered_df,
    x="video_length",
    y="retention_rate",
    size="views",
    color="format",
    hover_data=[
        "content_id",
        "topic",
        "engagement_rate"
    ],
    title="Video Length vs Retention Rate"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# VIRAL CONTENT
# -----------------------------
st.subheader("🔥 Viral Content Analysis")

col1, col2 = st.columns(2)

with col1:

    viral_counts = (
        filtered_df["viral_category"]
        .value_counts()
        .reset_index()
    )

    viral_counts.columns = ["viral_category", "count"]

    fig5 = px.pie(
        viral_counts,
        names="viral_category",
        values="count",
        title="Content Distribution by Viral Category"
    )

    st.plotly_chart(fig5, use_container_width=True)

with col2:

    viral_perf = (
        filtered_df.groupby("viral_category")["viral_score"]
        .mean()
        .reset_index()
        .sort_values("viral_score", ascending=False)
    )

    fig6 = px.bar(
        viral_perf,
        x="viral_category",
        y="viral_score",
        title="Average Viral Score by Category",
        text_auto=".2f"
    )

    st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# TOP CONTENT
# -----------------------------
st.subheader("🏆 Top Performing Content")

top_content = (
    filtered_df[
        [
            "content_id",
            "topic",
            "format",
            "views",
            "likes",
            "comments",
            "shares",
            "engagement_rate",
            "retention_rate",
            "viral_score"
        ]
    ]
    .sort_values("viral_score", ascending=False)
    .head(10)
)

st.dataframe(
    top_content,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# RECOMMENDATIONS
# -----------------------------
st.subheader("💡 Content Recommendations")

if len(filtered_df) > 0:

    best_format = (
        filtered_df.groupby("format")["engagement_rate"]
        .mean()
        .idxmax()
    )

    best_topic = (
        filtered_df.groupby("topic")["engagement_rate"]
        .mean()
        .idxmax()
    )

    best_hook = (
        filtered_df.groupby("hook_type")["engagement_rate"]
        .mean()
        .idxmax()
    )

    st.success(
        f"🎯 Best performing format: **{best_format}**"
    )

    st.info(
        f"🔥 Highest engagement topic: **{best_topic}**"
    )

    st.warning(
        f"🪝 Most effective hook type: **{best_hook}**"
    )

# -----------------------------
# DATASET
# -----------------------------
with st.expander("📋 View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "Content Analytics & A/B Testing Project"
)
