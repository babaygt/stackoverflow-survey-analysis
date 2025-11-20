# Analysis Methodology

## Overview

This document provides detailed technical documentation of the analysis methodology used in the Stack Overflow Developer Survey 2025 analysis project.

## Data Collection & Preparation

### Dataset Characteristics

- **Source**: Stack Overflow Annual Developer Survey 2025
- **Total Responses**: 49,123 developers
- **Variables**: 170 data points per respondent
- **Geographic Coverage**: 177 countries
- **Survey Method**: Online self-reported survey

### Data Loading

```python
df = pd.read_csv("./data/survey_results_public.csv")
```

**Rationale**: Used pandas for efficient DataFrame operations.

## Data Cleaning Process

### 1. Missing Value Handling

**Approach**: Filtering rather than imputation

```python
df_comp = df[df["ConvertedCompYearly"].notna() & (df["ConvertedCompYearly"] > 0)].copy()
```

**Rationale**:

- **Why not impute?** Salary data is highly contextual (location, role, experience). Imputing with mean/median would introduce systematic bias.
- **Trade-off**: Smaller sample size, but maintained data integrity

### 2. Outlier Removal

**Method**: Hard threshold at $500,000 annual compensation

```python
df_comp = df_comp[df_comp["ConvertedCompYearly"] < 500000]
```

**Rationale**:

- Salaries above $500K represent less than 1% of responses
- Could represent data entry errors or extreme outliers
- Would skew mean calculations and distort visualizations
- Median is robust to outliers, but box plots would become unreadable

### 3. Categorical Binning

**Experience Levels**:

```python
df_comp["ExpBin"] = pd.cut(
    df_comp["WorkExp"],
    bins=[0, 2, 5, 10, 20, 100],
    labels=["0-2 years", "3-5 years", "6-10 years", "11-20 years", "20+ years"]
)
```

**Rationale**:

- Bins chosen based on typical career stages in technology industry
- 0-2 years: Junior developers
- 3-5 years: Early-career professionals
- 6-10 years: Mid-level developers
- 11-20 years: Senior developers
- 20+ years: Veteran developers

## Statistical Methods

### 1. Descriptive Statistics

**Calculated for each group**:

- **Count**: Sample size (for statistical power assessment)
- **Mean**: Average value (sensitive to outliers)
- **Median**: Middle value (robust to outliers)
- **Standard Deviation**: Measure of spread

**Why both mean and median?**

- Mean: Useful for total/expected value calculations
- Median: Better for skewed distributions (like salary)
- Comparing them reveals distribution shape

### 2. Correlation Analysis

**Pearson Correlation Coefficient**:

```python
corr_exp_comp = df_comp[["WorkExp", "ConvertedCompYearly"]].corr().iloc[0, 1]
```

**Interpretation**:

- r = 0.332 (moderate positive correlation)
- r² = 0.110 (11% of variance explained)
- **Meaning**: Experience alone explains approximately 11% of salary variation
- Other 89%: Location, role, company, skills, etc.

**Why Pearson?**

- Measures linear relationships
- Assumes continuous variables
- Industry standard for this type of analysis

**Limitations**:

- Does not capture non-linear relationships
- Sensitive to outliers (addressed through outlier removal)

### 3. Cross-Tabulation (Pivot Tables)

**Remote Work × Job Satisfaction**:

```python
remote_jobsat = pd.crosstab(
    df_remote["RemoteWork"],
    df_remote["JobSat"],
    normalize="index"
) * 100
```

**Normalization**: `normalize="index"` converts counts to row percentages

- Each row sums to 100%
- Enables comparison across different group sizes
- Answers: "Of remote workers, what percentage gave each satisfaction score?"

## Visualization Choices

### Plot 1: Box Plot (Experience vs Compensation)

**Why box plot?**

- Shows distribution (quartiles, median, outliers)
- Easy comparison across groups
- Reveals data spread and skewness

**Key elements**:

- Box: IQR (25th-75th percentile)
- Line: Median
- Whiskers: 1.5 × IQR
- Dots: Outliers beyond whiskers

### Plot 2: Horizontal Bar Chart (Language Popularity)

**Why horizontal bars?**

- Language names are long (better horizontal orientation)
- Natural reading order (top = most popular)
- Easy to add value labels

**Design choices**:

- Sorted ascending (lowest at bottom)
- Added count labels for exact values
- Limited to top 15 for clarity

### Plot 3: Violin Plot (Education vs Compensation)

**Why violin plot over box plot?**

- Shows full distribution shape (density)
- Reveals bimodal distributions
- More informative than box plot alone

**Interpretation**:

- Width = density of data points at that value
- "Bumps" = common salary ranges
- Thinner = fewer people at that salary

### Plot 4: Heatmap (Remote Work vs Satisfaction)

**Why heatmap?**

- Two categorical variables
- Shows percentage distribution
- Color intensity = frequency

**Color choice**: YlGnBu (yellow-green-blue)

- Sequential palette (low to high)
- Colorblind-friendly
- Professional appearance

### Plot 5: Stacked Bar Chart (AI Threat by Experience)

**Why stacked?**

- Shows composition (each bar = 100%)
- Easy comparison of proportions across groups
- Highlights trends with experience

### Plot 6: Correlation Matrix (Heatmap with Mask)

**Why mask upper triangle?**

```python
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
```

- Correlation matrix is symmetric (redundant information)
- Diagonal is always 1.0 (not informative)
- Cleaner presentation

**Color scheme**: Coolwarm (diverging)

- Blue = negative correlation
- White = zero correlation
- Red = positive correlation

## Plot Configuration

### Publication Quality Settings

```python
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["savefig.bbox"] = "tight"
```

**Why 300 DPI?**

- Standard for publication/printing
- 72-96 DPI: Screen display
- 150 DPI: Basic printing
- 300 DPI: Professional printing
- 600+ DPI: High-end publishing (unnecessary for this context)

**"tight" bbox**:

- Removes excess whitespace
- Ensures all labels are visible
- Professional appearance

## Key Calculations Explained

### 1. Language Parsing

```python
all_languages = []
for langs in languages_series:
    all_languages.extend([lang.strip() for lang in str(langs).split(";")])
```

**Why this approach?**

- Stack Overflow stores multiple languages as "Python;JavaScript;SQL"
- Need to split and count individually
- `.strip()` removes whitespace
- Creates flat list for counting

### 2. Education Mapping

```python
edu_mapping = {
    "Bachelor's degree (B.A., B.S., B.Eng., etc.)": "Bachelor",
    # ...
}
df_edu["EdLevelSimple"] = df_edu["EdLevel"].map(edu_mapping).fillna("Other")
```

**Why simplify?**

- Original categories too verbose for plots
- Easier comparison with short labels
- Groups similar education levels

### 3. Percentage Calculation

```python
ai_threat_counts / ai_threat_counts.sum() * 100
```

**Formula**: (Count / Total) × 100

- Converts absolute numbers to percentages
- Easier to interpret and compare
- Standard for reporting categorical data
