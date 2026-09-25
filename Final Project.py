import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Global Happiness Report Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Happiness Report Analysis")
st.write("Analysis of the 2015 World Happiness dataset")

# -------------------- LOAD DATA --------------------

file_path = "2015.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("2015.csv not found. Put 2015.csv in the same folder as this app.py file.")
    st.stop()

df.columns = df.columns.str.strip()

# -------------------- RENAME COLUMNS --------------------

column_mapping = {}

for col in df.columns:
    clean_col = col.lower().strip()

    if "happiness score" in clean_col:
        column_mapping[col] = "Happiness_Score"
    elif "economy" in clean_col and "gdp" in clean_col:
        column_mapping[col] = "Economy_GDP"
    elif "family" in clean_col:
        column_mapping[col] = "Family"
    elif "health" in clean_col and "life" in clean_col:
        column_mapping[col] = "Health_Life_Expectancy"
    elif "freedom" in clean_col:
        column_mapping[col] = "Freedom"
    elif "trust" in clean_col or "government corruption" in clean_col:
        column_mapping[col] = "Trust_Government_Corruption"
    elif "generosity" in clean_col:
        column_mapping[col] = "Generosity"
    elif "region" in clean_col:
        column_mapping[col] = "Region"
    elif clean_col == "country":
        column_mapping[col] = "Country"

df.rename(columns=column_mapping, inplace=True)

numeric_columns = [
    "Happiness_Score",
    "Economy_GDP",
    "Family",
    "Health_Life_Expectancy",
    "Freedom",
    "Trust_Government_Corruption",
    "Generosity"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

required_columns = [
    column for column in numeric_columns
    if column in df.columns
]

df = df.dropna(subset=["Happiness_Score"])

# -------------------- SIDEBAR --------------------

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Choose Analysis",
    [
        "Dashboard",
        "Dataset",
        "Happiness Factors",
        "Country Analysis",
        "Regional Analysis",
        "Correlation Heatmap"
    ]
)

# -------------------- DASHBOARD --------------------

if page == "Dashboard":

    st.subheader("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Countries",
        len(df)
    )

    col2.metric(
        "Average Happiness",
        round(df["Happiness_Score"].mean(), 2)
    )

    col3.metric(
        "Highest Score",
        round(df["Happiness_Score"].max(), 2)
    )

    col4.metric(
        "Lowest Score",
        round(df["Happiness_Score"].min(), 2)
    )

    st.success("Dataset loaded successfully!")

    st.subheader("🏆 Top 10 Happiest Countries")

    if "Country" in df.columns:
        top10 = df.nlargest(10, "Happiness_Score")

        st.dataframe(
            top10[
                [
                    col for col in
                    ["Country", "Region", "Happiness_Score"]
                    if col in top10.columns
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.subheader("📈 Happiness Score Distribution")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        df["Happiness_Score"],
        bins=15
    )

    ax.set_title("Distribution of Happiness Scores - 2015")
    ax.set_xlabel("Happiness Score")
    ax.set_ylabel("Number of Countries")

    st.pyplot(fig)

# -------------------- DATASET --------------------

elif page == "Dataset":

    st.subheader("📋 Dataset Overview")

    col1, col2 = st.columns(2)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.write("### Dataset")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.write("### Missing Values")

    missing = df.isnull().sum()

    st.dataframe(
        missing.to_frame("Missing Values"),
        use_container_width=True
    )

# -------------------- HAPPINESS FACTORS --------------------

elif page == "Happiness Factors":

    st.subheader("📈 Happiness Factor Analysis")

    available_factors = [
        column for column in
        [
            "Economy_GDP",
            "Family",
            "Health_Life_Expectancy",
            "Freedom",
            "Trust_Government_Corruption",
            "Generosity"
        ]
        if column in df.columns
    ]

    if not available_factors:
        st.warning("No happiness factor columns were found.")
        st.stop()

    factor = st.selectbox(
        "Select Factor",
        available_factors
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.regplot(
        data=df,
        x=factor,
        y="Happiness_Score",
        scatter_kws={"alpha": 0.6},
        ax=ax
    )

    ax.set_title(
        f"{factor} vs Happiness Score"
    )

    ax.set_xlabel(factor)
    ax.set_ylabel("Happiness Score")

    st.pyplot(fig)

    correlation = df[[factor, "Happiness_Score"]].corr().iloc[0, 1]

    st.info(
        f"Correlation between {factor} and Happiness Score: "
        f"{correlation:.2f}"
    )

# -------------------- COUNTRY ANALYSIS --------------------

elif page == "Country Analysis":

    st.subheader("🌍 Country Analysis")

    if "Country" not in df.columns:
        st.warning("Country column was not found.")
        st.stop()

    country = st.selectbox(
        "Select Country",
        sorted(df["Country"].dropna().unique())
    )

    country_data = df[df["Country"] == country].iloc[0]

    st.write(f"### {country}")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Happiness Score",
        round(country_data["Happiness_Score"], 2)
    )

    if "Economy_GDP" in df.columns:
        col2.metric(
            "Economy / GDP",
            round(country_data["Economy_GDP"], 2)
        )

    if "Freedom" in df.columns:
        col3.metric(
            "Freedom",
            round(country_data["Freedom"], 2)
        )

    factor_values = {}

    for factor in [
        "Economy_GDP",
        "Family",
        "Health_Life_Expectancy",
        "Freedom",
        "Trust_Government_Corruption",
        "Generosity"
    ]:
        if factor in df.columns:
            factor_values[factor] = country_data[factor]

    if factor_values:
        chart_data = pd.DataFrame(
            {
                "Factor": list(factor_values.keys()),
                "Value": list(factor_values.values())
            }
        )

        st.bar_chart(
            chart_data.set_index("Factor")
        )

# -------------------- REGIONAL ANALYSIS --------------------

elif page == "Regional Analysis":

    st.subheader("🗺️ Regional Happiness Analysis")

    if "Region" not in df.columns:
        st.warning("Region column was not found.")
        st.stop()

    region_data = (
        df.groupby("Region")["Happiness_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    st.write("### Average Happiness Score by Region")

    st.bar_chart(region_data)

    st.write("### Regional Distribution")

    fig, ax = plt.subplots(figsize=(12, 7))

    sns.boxplot(
        data=df,
        x="Happiness_Score",
        y="Region",
        ax=ax
    )

    ax.set_title(
        "Happiness Score Distribution by Region - 2015"
    )

    ax.set_xlabel("Happiness Score")
    ax.set_ylabel("Region")

    st.pyplot(fig)

# -------------------- HEATMAP --------------------

elif page == "Correlation Heatmap":

    st.subheader("🔥 Correlation Heatmap")

    heatmap_columns = [
        column for column in numeric_columns
        if column in df.columns
    ]

    correlation = df[heatmap_columns].corr()

    fig, ax = plt.subplots(figsize=(10, 7))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.5,
        ax=ax
    )

    ax.set_title(
        "Correlation Heatmap of Happiness Factors - 2015"
    )

    st.pyplot(fig)

# -------------------- FOOTER --------------------

st.sidebar.markdown("---")
st.sidebar.info("Global Happiness Report Analysis | 2015")
