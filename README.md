# 🌍 World Happiness Report (2015) — Exploratory Data Analysis & Visualizations

---

## 📖 Project Overview

The **World Happiness Report** measures global wellbeing based on key economic, social, and institutional factors. This repository provides an automated pipeline designed to:
1. Normalize varied raw column naming conventions.
2. Handle null/missing records and enforce numeric data integrity.
3. Compute a correlation matrix across happiness drivers.
4. Render high-resolution regression models, boxplots, and heatmaps.
5. Compute key descriptive statistics (highest/lowest scoring nations, global averages).

---

## ⚡ Key Features

* **Dynamic Column Normalization**: Automatically maps heterogeneous raw headers (e.g., `"Economy (GDP per Capita)"` $\rightarrow$ `"Economy_GDP"`).
* **Automated Data Cleaning**: Coerces non-numeric anomalies to NaN, isolates required metrics, and removes incomplete observations.
* **Multivariate Visualizations**: Generates regression plots and distribution charts using Seaborn and Matplotlib.
* **Geographical Insights**: Sorts regions hierarchically by median happiness scores.

---

## 📊 Dataset Architecture & Mapping

The pipeline extracts and standardizes the following continuous metrics from `2015.csv`:

| Standardized Column Name | Target Metric Description |
| :--- | :--- |
| `Happiness_Score` | National score based on the Cantril Ladder survey response |
| `Economy_GDP` | Extent to which GDP per capita contributes to calculation |
| `Family` | Social support and family cohesion network strength |
| `Health_Life_Expectancy` | Healthy life expectancy at birth |
| `Freedom` | Perceived freedom of citizens to make life choices |
| `Trust_Government_Corruption` | Public trust and perceived absence of institutional corruption |
| `Generosity` | Public charitable donations and societal altruism |
| `Region` | Geographic classification of surveyed nations |

---

## 📈 Visualizations & Analytical Insights

The analysis script generates five key figures:

### 1. Correlation Matrix Heatmap
* **Type**: Annotated Heatmap (`coolwarm` palette, 2-decimal precision)
* **Purpose**: Evaluates linear correlation ($r$) between all seven standardized continuous drivers.
* **Key Finding**: Demonstrates strong positive collinearity between `Happiness_Score`, `Economy_GDP`, and `Health_Life_Expectancy`.

### 2. Economic Prosperity vs. Happiness
* **Type**: Linear Regression Plot (`Economy_GDP` vs. `Happiness_Score`)
* **Purpose**: Identifies the correlation between national economic output and overall life satisfaction.

### 3. Social Support & Family Dynamics
* **Type**: Linear Regression Plot (`Family` vs. `Happiness_Score`)
* **Purpose**: Measures how strong family structures and social safety nets correlate with happiness.

### 4. Health & Life Expectancy Impact
* **Type**: Linear Regression Plot (`Health_Life_Expectancy` vs. `Happiness_Score`)
* **Purpose**: Evaluates how access to healthcare and long-term vitality correlate with national scores.

### 5. Freedom of Choice vs. Happiness
* **Type**: Linear Regression Plot (`Freedom` vs. `Happiness_Score`)
* **Purpose**: Examines the relationship between personal autonomy/civil liberties and national morale.

### 6. Regional Happiness Distribution
* **Type**: Ordered Horizontal Boxplot
* **Purpose**: Displays the spread, median, and interquartile range (IQR) across global regions (e.g., Western Europe, Sub-Saharan Africa, Latin America).

---
