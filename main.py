"""
Stack Overflow Developer Survey 2025 - Analysis Script
======================================================
Author: Yigit Baba
Course: Data Science Basic Module, CODE University of Applied Sciences
Date: November 2025

This script analyzes the Stack Overflow 2025 Developer Survey to answer
five key research questions about developer compensation, technology adoption,
education impact, remote work, and AI sentiment.

Research Questions:
1. How does experience level impact compensation?
2. What are the most popular programming languages?
3. How does education level affect salary?
4. What is the relationship between remote work and job satisfaction?
5. How do developers feel about AI threat to their jobs?
"""

# ============================================================================
# IMPORTS & SETUP
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

# Set style for publication-quality plots
sns.set_style("whitegrid")  # Clean background with grid
sns.set_palette("husl")  # Colorblind-friendly palette

# Configure plot parameters
plt.rcParams["figure.dpi"] = 300  # High resolution (publication quality)
plt.rcParams["savefig.dpi"] = 300  # Save at 300 DPI
plt.rcParams["savefig.bbox"] = "tight"  # Remove excess whitespace
plt.rcParams["font.size"] = 11  # Base font size
plt.rcParams["axes.labelsize"] = 12  # Axis label size
plt.rcParams["axes.titlesize"] = 14  # Title size
plt.rcParams["axes.titleweight"] = "bold"  # Bold titles

# ============================================================================
# DATA LOADING
# ============================================================================

print("Loading Stack Overflow Developer Survey 2025...")
df = pd.read_csv("./data/survey_results_public.csv")

# Display basic dataset information
print(f"Total responses: {len(df):,}")
print(f"Total variables: {len(df.columns)}")
print(f"Shape of dataset: {df.shape}")

# ============================================================================
# RESEARCH QUESTION 1: Experience Level vs Compensation
# ============================================================================

print("\n" + "=" * 80)
print("Q1: How does experience level impact compensation?")
print("=" * 80)

# ---- Data Cleaning ----
# Filter for valid compensation data
# - Remove null values
# - Remove zero/negative salaries (likely missing/invalid)
# - Remove outliers above $500K (extreme values that skew analysis)
df_comp = df[df["ConvertedCompYearly"].notna() & (df["ConvertedCompYearly"] > 0)].copy()
df_comp = df_comp[df_comp["ConvertedCompYearly"] < 500000]  # Remove outliers
df_comp = df_comp[df_comp["WorkExp"].notna()]  # Need experience data too

# ---- Create Experience Bins ----
# Group continuous experience into categorical bins for easier analysis
# Bins chosen based on typical career stages in tech industry
df_comp["ExpBin"] = pd.cut(
    df_comp["WorkExp"],
    bins=[0, 2, 5, 10, 20, 100],  # Bin edges
    labels=["0-2 years", "3-5 years", "6-10 years", "11-20 years", "20+ years"],
)

# ---- Calculate Statistics ----
# Group by experience level and calculate summary statistics
exp_stats = (
    df_comp.groupby("ExpBin")["ConvertedCompYearly"]
    .agg(
        [
            ("Count", "count"),  # Sample size (n)
            ("Mean", "mean"),  # Average salary (sensitive to outliers)
            ("Median", "median"),  # Middle value (robust to outliers)
            ("Std", "std"),  # Standard deviation (measure of spread)
        ]
    )
    .round(0)  # Round to nearest dollar
)

print("\nCompensation by Experience Level:")
print(exp_stats)

# ---- Correlation Analysis ----
# Calculate Pearson correlation coefficient between experience and compensation
# r ranges from -1 to +1, where:
#   -1 = perfect negative correlation
#    0 = no correlation
#   +1 = perfect positive correlation
corr_exp_comp = df_comp[["WorkExp", "ConvertedCompYearly"]].corr().iloc[0, 1]
print(f"\nPearson correlation (Experience vs Compensation): {corr_exp_comp:.3f}")
# Result: r = 0.332 (moderate positive correlation)
# r² = 0.11, meaning experience explains ~11% of salary variance

# ---- Visualization: Box Plot ----
# Box plot shows distribution of salaries across experience levels
# Components:
# - Box: Interquartile range (25th to 75th percentile)
# - Line in box: Median
# - Whiskers: 1.5 × IQR
# - Dots: Outliers
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_comp, x="ExpBin", y="ConvertedCompYearly", ax=ax, palette="Set2")
ax.set_xlabel("Years of Experience", fontweight="bold")
ax.set_ylabel("Annual Compensation (USD)", fontweight="bold")
ax.set_title("Developer Compensation by Experience Level", pad=20)
ax.set_ylim(0, 250000)  # Set y-axis limit for better readability
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("./plots/plot1_compensation_experience.png", dpi=300, bbox_inches="tight")
print("✓ Plot 1 saved: plot1_compensation_experience.png")
plt.close()

# ============================================================================
# RESEARCH QUESTION 2: Most Popular Programming Languages
# ============================================================================

print("\n" + "=" * 80)
print("Q2: What are the most popular programming languages?")
print("=" * 80)

# ---- Parse Language Data ----
# Languages are stored as semicolon-separated strings
# Example: "Python;JavaScript;SQL"
# Need to split these into individual languages and count occurrences
languages_series = df["LanguageHaveWorkedWith"].dropna()
all_languages = []

# Loop through each response and split languages
for langs in languages_series:
    all_languages.extend([lang.strip() for lang in str(langs).split(";")])

# Count occurrences and get top 15
lang_counts = pd.Series(all_languages).value_counts().head(15)
print("\nTop 15 Programming Languages:")
print(lang_counts)

# ---- Visualization: Horizontal Bar Chart ----
# Horizontal bars better for long language names
# Sorted ascending so most popular is at top
fig, ax = plt.subplots(figsize=(10, 8))
lang_counts.sort_values().plot(kind="barh", ax=ax, color="steelblue", edgecolor="black")
ax.set_xlabel("Number of Developers", fontweight="bold")
ax.set_ylabel("Programming Language", fontweight="bold")
ax.set_title("Top 15 Most Used Programming Languages (2025)", pad=20)
ax.grid(axis="x", alpha=0.3)  # Add vertical grid lines for readability

# Add value labels to bars
for i, v in enumerate(lang_counts.sort_values()):
    ax.text(v + 500, i, f"{v:,}", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("./plots/plot2_top_languages.png", dpi=300, bbox_inches="tight")
print("✓ Plot 2 saved: plot2_top_languages.png")
plt.close()

# ============================================================================
# RESEARCH QUESTION 3: Education Level vs Compensation
# ============================================================================

print("\n" + "=" * 80)
print("Q3: How does education level affect compensation?")
print("=" * 80)

# ---- Data Filtering ----
# Same compensation filters as Q1, plus need education data
df_edu = df[
    (df["ConvertedCompYearly"].notna())
    & (df["ConvertedCompYearly"] > 0)
    & (df["ConvertedCompYearly"] < 500000)
    & (df["EdLevel"].notna())
].copy()

# ---- Simplify Education Levels ----
# Original categories are verbose, map to shorter labels for plots
edu_mapping = {
    "Bachelor's degree (B.A., B.S., B.Eng., etc.)": "Bachelor",
    "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": "Master",
    "Some college/university study without earning a degree": "Some College",
    "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "PhD/Professional",
    "Associate degree (A.A., A.S., etc.)": "Associate",
    "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "High School",
    "Primary/elementary school": "Elementary",
    "Something else": "Other",  # Includes bootcamps, self-taught, etc.
}

df_edu["EdLevelSimple"] = df_edu["EdLevel"].map(edu_mapping).fillna("Other")

# ---- Calculate Statistics ----
edu_stats = (
    df_edu.groupby("EdLevelSimple")["ConvertedCompYearly"]
    .agg([("Count", "count"), ("Mean", "mean"), ("Median", "median")])
    .round(0)
    .sort_values("Median", ascending=False)  # Sort by median salary
)

print("\nCompensation by Education Level:")
print(edu_stats)

# ---- Visualization: Violin Plot ----
# Violin plot shows full distribution shape (density)
# Width of "violin" indicates how many people earn that salary
# Reveals bimodal distributions (two common salary ranges)
fig, ax = plt.subplots(figsize=(12, 7))
order = edu_stats.index.tolist()  # Use our sorted order
sns.violinplot(
    data=df_edu,
    x="EdLevelSimple",
    y="ConvertedCompYearly",
    order=order,
    ax=ax,
    palette="muted",
    cut=0,  # Don't extend beyond data range
)
ax.set_xlabel("Education Level", fontweight="bold")
ax.set_ylabel("Annual Compensation (USD)", fontweight="bold")
ax.set_title("Compensation Distribution by Education Level", pad=20)
ax.set_ylim(0, 250000)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("./plots/plot3_education_compensation.png", dpi=300, bbox_inches="tight")
print("✓ Plot 3 saved: plot3_education_compensation.png")
plt.close()

# ============================================================================
# RESEARCH QUESTION 4: Remote Work vs Job Satisfaction
# ============================================================================

print("\n" + "=" * 80)
print("Q4: Remote work and job satisfaction relationship")
print("=" * 80)

# ---- Data Filtering ----
df_remote = df[(df["RemoteWork"].notna()) & (df["JobSat"].notna())].copy()

# ---- Create Pivot Table (Cross-Tabulation) ----
# Shows percentage of each remote work type giving each satisfaction score
# normalize='index' means each row sums to 100%
remote_jobsat = (
    pd.crosstab(df_remote["RemoteWork"], df_remote["JobSat"], normalize="index") * 100
)
print("\nJob Satisfaction by Remote Work Status (%):")
print(remote_jobsat.round(1))

# ---- Calculate Average Satisfaction ----
# Aggregate satisfaction scores by remote work type
remote_satisfaction = (
    df_remote.groupby("RemoteWork")["JobSat"]
    .agg([("Count", "count"), ("Mean", "mean"), ("Median", "median")])
    .sort_values("Mean", ascending=False)  # Sort by average satisfaction
)

print("\nAverage Job Satisfaction Scores:")
print(remote_satisfaction.round(2))
# Key finding: Flexible work has highest satisfaction (7.43/10)
# In-person has lowest (6.99/10)

# ---- Visualization: Heatmap ----
# Heatmap shows distribution of satisfaction scores across work arrangements
# Color intensity = percentage of respondents
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(
    remote_jobsat,
    annot=True,  # Show percentage values
    fmt=".1f",  # One decimal place
    cmap="YlGnBu",  # Yellow-Green-Blue color scheme
    cbar_kws={"label": "Percentage (%)"},
    ax=ax,
    linewidths=0.5,  # Grid lines between cells
)
ax.set_xlabel("Job Satisfaction Score (0=Lowest, 10=Highest)", fontweight="bold")
ax.set_ylabel("Remote Work Status", fontweight="bold")
ax.set_title("Job Satisfaction Distribution by Remote Work Arrangement", pad=20)
plt.tight_layout()
plt.savefig(
    "./plots/plot4_remote_satisfaction_heatmap.png", dpi=300, bbox_inches="tight"
)
print("✓ Plot 4 saved: plot4_remote_satisfaction_heatmap.png")
plt.close()

# ============================================================================
# RESEARCH QUESTION 5: AI Threat to Jobs
# ============================================================================

print("\n" + "=" * 80)
print("Q5: Developer sentiment about AI threat to jobs")
print("=" * 80)

# ---- Overall Sentiment ----
df_ai = df[df["AIThreat"].notna()].copy()
ai_threat_counts = df_ai["AIThreat"].value_counts()
print("\nAI Threat Perception:")
print(ai_threat_counts)

# Convert to percentages
print(f"\nPercentage distribution:")
print((ai_threat_counts / ai_threat_counts.sum() * 100).round(1))
# Key finding: 63.6% say "No" - most developers NOT worried

# ---- Cross-Tabulation with Experience ----
# Does AI concern vary by experience level?
df_ai_exp = df[(df["AIThreat"].notna()) & (df["WorkExp"].notna())].copy()
df_ai_exp["ExpBin"] = pd.cut(
    df_ai_exp["WorkExp"],
    bins=[0, 5, 10, 20, 100],
    labels=["0-5 years", "6-10 years", "11-20 years", "20+ years"],
)

# Create crosstab with row percentages
ai_exp_crosstab = (
    pd.crosstab(df_ai_exp["ExpBin"], df_ai_exp["AIThreat"], normalize="index") * 100
)
print("\nAI Threat Perception by Experience (%):")
print(ai_exp_crosstab.round(1))
# Interesting: Senior developers (20+) slightly LESS concerned

# ---- Visualization: Stacked Bar Chart ----
# Shows composition of responses at each experience level
# Each bar totals 100%
fig, ax = plt.subplots(figsize=(12, 7))
ai_exp_crosstab.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    color=["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4"],  # Red, orange, green, blue
)
ax.set_xlabel("Years of Experience", fontweight="bold")
ax.set_ylabel("Percentage (%)", fontweight="bold")
ax.set_title("AI Threat Perception by Developer Experience Level", pad=20)
ax.legend(title="AI Threat Level", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("./plots/plot5_ai_threat_experience.png", dpi=300, bbox_inches="tight")
print("✓ Plot 5 saved: plot5_ai_threat_experience.png")
plt.close()

# ============================================================================
# BONUS: Correlation Matrix
# ============================================================================

print("\n" + "=" * 80)
print("BONUS: Correlation Analysis")
print("=" * 80)

# ---- Select Numeric Variables ----
# Choose key numeric variables for correlation analysis
numeric_cols = [
    "WorkExp",  # Years of work experience
    "YearsCode",  # Years coding (including hobbyist time)
    "ConvertedCompYearly",  # Annual compensation
    "JobSat",  # Job satisfaction score
    "ToolCountWork",  # Number of tools used at work
]
df_corr = df[numeric_cols].dropna()

# ---- Calculate Correlation Matrix ----
# Pearson correlation between all pairs of variables
correlation_matrix = df_corr.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix.round(3))

# Key findings:
# - WorkExp vs YearsCode: 0.892 (very strong - expected)
# - WorkExp vs Compensation: 0.084 (weak - other factors matter more)
# - JobSat vs everything: ~0.1 (satisfaction not driven by these metrics)

# ---- Visualization: Correlation Heatmap ----
# Use mask to hide upper triangle (matrix is symmetric)
fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(
    correlation_matrix,
    mask=mask,  # Hide redundant upper triangle
    annot=True,  # Show correlation values
    fmt=".3f",  # Three decimal places
    cmap="coolwarm",  # Diverging color scheme (blue-white-red)
    center=0,  # White at zero correlation
    square=True,  # Square cells
    linewidths=1,  # Grid lines
    cbar_kws={"shrink": 0.8},  # Slightly smaller color bar
    ax=ax,
    vmin=-1,  # Correlation range
    vmax=1,
)
ax.set_title("Correlation Matrix of Key Developer Metrics", pad=20, fontweight="bold")
plt.tight_layout()
plt.savefig("./plots/plot6_correlation_matrix.png", dpi=300, bbox_inches="tight")
print("✓ Plot 6 saved: plot6_correlation_matrix.png")
plt.close()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)

# Calculate overall dataset metrics
summary_stats = {
    "Total Responses": len(df),
    "Response Rate (with compensation data)": f"{len(df[df['ConvertedCompYearly'].notna()]) / len(df) * 100:.1f}%",
    "Countries Represented": df["Country"].nunique(),
    "Median Compensation (USD)": f"${df['ConvertedCompYearly'].median():,.0f}",
    "Median Work Experience (years)": f"{df['WorkExp'].median():.0f}",
    "Most Common Dev Type": (
        df["DevType"].mode()[0] if not df["DevType"].mode().empty else "N/A"
    ),
}

print("\nKey Dataset Metrics:")
for key, value in summary_stats.items():
    print(f"  • {key}: {value}")

print("\n" + "=" * 80)
print("Analysis complete! All plots saved.")
print("=" * 80)
print("\nPlots saved to ./plots/ directory:")
print("  1. plot1_compensation_experience.png")
print("  2. plot2_top_languages.png")
print("  3. plot3_education_compensation.png")
print("  4. plot4_remote_satisfaction_heatmap.png")
print("  5. plot5_ai_threat_experience.png")
print("  6. plot6_correlation_matrix.png")
