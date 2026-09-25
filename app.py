import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Global Happiness Report Analysis",
    page_icon="🌍",
    layout="wide"
)

# ==========================================
# GLOBAL HAPPINESS REPORT ANALYSIS
# ==========================================

st.title("🌍 Global Happiness Report Analysis")
st.write("World Happiness Report - 2019")

# ------------------------------------------
# 1. Load Dataset
# ------------------------------------------

file_path = "2019.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("2019.csv not found. Upload 2019.csv to the same GitHub folder as app.py.")
    st.stop()

df.columns = df.columns.str.strip()

st.success("Dataset Loaded Successfully!")

# ------------------------------------------
# Sidebar
# ------------------------------------------

st.sidebar.title("📌 Analysis Menu")

choice = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Dataset",
        "Top & Bottom Countries",
        "Correlation Analysis",
        "Happiness Factors",
        "Average Values"
    ]
)

# ------------------------------------------
# Clean Data
# ------------------------------------------

df = df.dropna()

# ------------------------------------------
# Dashboard
# ------------------------------------------

if choice == "Dashboard":

    st.header("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Countries", df.shape[0])
    col2.metric("Average Happiness", round(df["Score"].mean(), 2))
    col3.metric("Highest Score", round(df["Score"].max(), 2))
    col4.metric("Lowest Score", round(df["Score"].min(), 2))

    st.subheader("📋 Dataset Summary")

    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    st.subheader("🏆 Top 10 Happiest Countries")

    top_10 = df.sort_values(
        by="Score",
        ascending=False
    ).head(10)

    st.dataframe(
        top_10[["Country or region", "Score"]],
        use_container_width=True,
        hide_index=True
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=top_10,
        x="Score",
        y="Country or region",
        ax=ax
    )

    ax.set_title("Top 10 Happiest Countries")
    ax.set_xlabel("Happiness Score")
    ax.set_ylabel("Country")

    st.pyplot(fig)

# ------------------------------------------
# Dataset
# ------------------------------------------

elif choice == "Dataset":

    st.header("📋 Dataset")

    st.subheader("First 5 Records")
    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.subheader("Complete Dataset")
    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    col1.metric("Number of Rows", df.shape[0])
    col2.metric("Number of Columns", df.shape[1])

    st.subheader("Missing Values")

    missing = df.isnull().sum()

    st.dataframe(
        missing.to_frame("Missing Values"),
        use_container_width=True
    )

    st.subheader("Basic Statistics")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )

# ------------------------------------------
# Top and Bottom Countries
# ------------------------------------------

elif choice == "Top & Bottom Countries":

    st.header("🏆 Country Happiness Ranking")

    top_10 = df.sort_values(
        by="Score",
        ascending=False
    ).head(10)

    bottom_10 = df.sort_values(
        by="Score",
        ascending=True
    ).head(10)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Happiest Countries")

        st.dataframe(
            top_10[["Country or region", "Score"]],
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.subheader("10 Lowest Happiness Countries")

        st.dataframe(
            bottom_10[["Country or region", "Score"]],
            use_container_width=True,
            hide_index=True
        )

# ------------------------------------------
# Correlation Analysis
# ------------------------------------------

elif choice == "Correlation Analysis":

    st.header("🔥 Correlation Analysis")

    columns = [
        "Score",
        "GDP per capita",
        "Social support",
        "Healthy life expectancy",
        "Freedom to make life choices",
        "Generosity",
        "Perceptions of corruption"
    ]

    correlation = df[columns].corr()

    st.subheader("Correlation Table")

    st.dataframe(
        correlation.round(2),
        use_container_width=True
    )

    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots(figsize=(10, 7))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax
    )

    ax.set_title("Correlation Between Happiness Factors")

    st.pyplot(fig)

    st.subheader("Individual Correlations")

    col1, col2 = st.columns(2)

    gdp_corr = df["Score"].corr(
        df["GDP per capita"]
    )

    social_corr = df["Score"].corr(
        df["Social support"]
    )

    life_corr = df["Score"].corr(
        df["Healthy life expectancy"]
    )

    freedom_corr = df["Score"].corr(
        df["Freedom to make life choices"]
    )

    col1.metric(
        "Happiness ↔ GDP",
        round(gdp_corr, 2)
    )

    col2.metric(
        "Happiness ↔ Social Support",
        round(social_corr, 2)
    )

    col1.metric(
        "Happiness ↔ Life Expectancy",
        round(life_corr, 2)
    )

    col2.metric(
        "Happiness ↔ Freedom",
        round(freedom_corr, 2)
    )

# ------------------------------------------
# Happiness Factors
# ------------------------------------------

elif choice == "Happiness Factors":

    st.header("📈 Happiness Factor Analysis")

    factor_names = {
        "GDP per capita": "GDP per Capita",
        "Social support": "Social Support",
        "Healthy life expectancy": "Life Expectancy",
        "Freedom to make life choices": "Freedom",
        "Generosity": "Generosity",
        "Perceptions of corruption": "Perceptions of Corruption"
    }

    factor = st.selectbox(
        "Select Happiness Factor",
        list(factor_names.keys())
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    sns.scatterplot(
        data=df,
        x=factor,
        y="Score",
        ax=ax
    )

    ax.set_title(
        f"{factor_names[factor]} vs Happiness Score"
    )

    ax.set_xlabel(factor_names[factor])
    ax.set_ylabel("Happiness Score")

    st.pyplot(fig)

    correlation = df["Score"].corr(
        df[factor]
    )

    st.info(
        f"Correlation between Happiness and "
        f"{factor_names[factor]}: {correlation:.2f}"
    )

# ------------------------------------------
# Average Values
# ------------------------------------------

elif choice == "Average Values":

    st.header("📊 Average Values")

    col1, col2 = st.columns(2)

    col1.metric(
        "Average Happiness",
        round(df["Score"].mean(), 2)
    )

    col2.metric(
        "Average GDP",
        round(df["GDP per capita"].mean(), 2)
    )

    col1.metric(
        "Average Social Support",
        round(df["Social support"].mean(), 2)
    )

    col2.metric(
        "Average Life Expectancy",
        round(df["Healthy life expectancy"].mean(), 2)
    )

    col1.metric(
        "Average Freedom",
        round(df["Freedom to make life choices"].mean(), 2)
    )

    col2.metric(
        "Average Generosity",
        round(df["Generosity"].mean(), 2)
    )

    st.subheader("Average Factor Values")

    average_data = pd.DataFrame({
        "Factor": [
            "Happiness",
            "GDP",
            "Social Support",
            "Life Expectancy",
            "Freedom",
            "Generosity"
        ],
        "Average Value": [
            df["Score"].mean(),
            df["GDP per capita"].mean(),
            df["Social support"].mean(),
            df["Healthy life expectancy"].mean(),
            df["Freedom to make life choices"].mean(),
            df["Generosity"].mean()
        ]
    })

    st.dataframe(
        average_data.round(2),
        use_container_width=True,
        hide_index=True
    )

# ------------------------------------------
# Footer
# ------------------------------------------

st.sidebar.markdown("---")
st.sidebar.info("Global Happiness Report Analysis | 2019")
