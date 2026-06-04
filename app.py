import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Food Classes Analytics Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.title {
    text-align: center;
    color: #ff4b4b;
    font-size: 40px;
    font-weight: bold;
}

.insight-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f1f5f9;
}

[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("classes.csv")
    return df

df = load_data()

# Rename first column
food_column = df.columns[0]
df.columns = ["Food"]

# ==========================================
# FEATURE ENGINEERING
# ==========================================

df["Food_Length"] = df["Food"].astype(str).str.len()
df["First_Letter"] = df["Food"].astype(str).str[0].str.upper()

# Word count
df["Word_Count"] = df["Food"].astype(str).str.split().str.len()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🍛 Food Explorer")

search_food = st.sidebar.text_input(
    "Search Food Item"
)

if search_food:
    df = df[
        df["Food"]
        .str.contains(
            search_food,
            case=False,
            na=False
        )
    ]

selected_letter = st.sidebar.multiselect(
    "Filter by First Letter",
    sorted(df["First_Letter"].unique())
)

if selected_letter:
    df = df[
        df["First_Letter"]
        .isin(selected_letter)
    ]

# ==========================================
# TITLE
# ==========================================

st.markdown(
    '<p class="title">🍽️ Food Classes Analytics Dashboard</p>',
    unsafe_allow_html=True
)

st.markdown("---")

# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Food Items",
        len(df)
    )

with col2:
    st.metric(
        "Unique Letters",
        df["First_Letter"].nunique()
    )

with col3:
    st.metric(
        "Avg Name Length",
        round(df["Food_Length"].mean(), 2)
    )

with col4:
    st.metric(
        "Avg Word Count",
        round(df["Word_Count"].mean(), 2)
    )

st.markdown("---")

# ==========================================
# CHARTS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    letter_counts = (
        df["First_Letter"]
        .value_counts()
        .reset_index()
    )

    letter_counts.columns = [
        "Letter",
        "Count"
    ]

    fig = px.bar(
        letter_counts,
        x="Letter",
        y="Count",
        title="Food Items by Starting Letter"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.histogram(
        df,
        x="Food_Length",
        nbins=15,
        title="Food Name Length Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# WORD COUNT ANALYSIS
# ==========================================

st.subheader("📊 Word Count Analysis")

word_counts = (
    df["Word_Count"]
    .value_counts()
    .reset_index()
)

word_counts.columns = [
    "Words",
    "Count"
]

fig = px.pie(
    word_counts,
    names="Words",
    values="Count",
    title="Single Word vs Multi-Word Foods"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# FOOD TABLE
# ==========================================

st.subheader("🍜 Food Items Dataset")

st.dataframe(
    df[[
        "Food",
        "Food_Length",
        "Word_Count",
        "First_Letter"
    ]],
    use_container_width=True
)

# ==========================================
# TOP INSIGHTS
# ==========================================

st.subheader("📌 Insights")

most_common_letter = (
    df["First_Letter"]
    .value_counts()
    .idxmax()
)

avg_length = round(
    df["Food_Length"].mean(),
    2
)

avg_words = round(
    df["Word_Count"].mean(),
    2
)

st.success(f"""
✔ Total Food Classes: {len(df)}

✔ Most Common Starting Letter: {most_common_letter}

✔ Average Food Name Length: {avg_length}

✔ Average Words per Food Name: {avg_words}

✔ Dataset contains multiple Indian food categories,
snacks, beverages, desserts, and meals.

✔ Food names can be used as labels for
food image classification projects.
""")

# ==========================================
# DOWNLOAD DATA
# ==========================================

csv = df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_food_classes.csv",
    mime="text/csv"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Built using Streamlit • Plotly • Pandas"
)
