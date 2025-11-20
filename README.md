# Stack Overflow Developer Survey 2025 - Data Analysis

## Project Overview

This project analyzes the **Stack Overflow Developer Survey 2025** dataset, containing **49,123 responses** from developers across **177 countries**. The analysis explores key trends in developer compensation, technology adoption, education impact, remote work preferences, and AI sentiment.

## Research Questions

This analysis addresses five key research questions:

1. **Q1: Experience & Compensation** - How does work experience impact developer salaries?
2. **Q2: Programming Languages** - What are the most popular languages in 2025?
3. **Q3: Education Impact** - How does education level affect compensation?
4. **Q4: Remote Work** - What's the relationship between remote work and job satisfaction?
5. **Q5: AI Sentiment** - How do developers perceive AI as a threat to their jobs?

## Project Structure

```
stackoverflow-survey-analysis/
├── data/
│   ├── survey_results_public.csv    # Main survey data
│   └── survey_results_schema.csv    # Data dictionary/schema
├── plots/
│   ├── plot1_compensation_experience.png
│   ├── plot2_top_languages.png
│   ├── plot3_education_compensation.png
│   ├── plot4_remote_satisfaction_heatmap.png
│   ├── plot5_ai_threat_experience.png
│   └── plot6_correlation_matrix.png
├── main.py                           # Main analysis script
├── pyproject.toml                    # Project dependencies
├── README.md                         # This file
└── .gitignore                        # Git ignore rules
```

## Installation & Setup

### Prerequisites

- Python 3.13 or higher
- pip or uv package manager

### Install Dependencies

Using pip:

```bash
pip install pandas numpy scipy seaborn matplotlib
```

Using uv (recommended):

```bash
uv sync
```

### Data Setup

1. Download the Stack Overflow 2025 survey data from [survey.stackoverflow.co](https://survey.stackoverflow.co/)
2. Place `survey_results_public.csv` and `survey_results_schema.csv` in the `data/` directory

## 🚀 Running the Analysis

### Basic Execution

```bash
python main.py
```

or

```bash
uv run main.py
```

### Expected Output

The script will:

1. Load and validate the dataset
2. Perform statistical analysis for each research question
3. Generate 6 plots (saved to `plots/` directory)
4. Print summary statistics to console

## Key Findings

### Q1: Experience Impact on Compensation

- **Strong positive correlation**: r = 0.332
- **Salary progression**:
  - 0-2 years: $22,632 median
  - 20+ years: $108,913 median (480% increase!)
- **Steepest growth**: 69% increase between years 5-10

### Q2: Programming Language Popularity

- **Top 5 Languages**:
  1. JavaScript: 20,986 developers
  2. HTML/CSS: 19,681 developers
  3. SQL: 18,617 developers
  4. Python: 18,388 developers
  5. Bash/Shell: 15,486 developers

### Q3: Education Level Impact

- **PhD/Professional**: $87,011 median salary
- **Surprising finding**: "Other" category (bootcamps/self-taught) earns $76,512 median
- **Key insight**: Multiple paths to high compensation in tech

### Q4: Remote Work & Satisfaction

- **Highest satisfaction**: Flexible workers (7.43/10 average)
- **Lowest satisfaction**: In-person workers (6.99/10 average)
- **Conclusion**: Autonomy drives developer happiness

### Q5: AI Threat Perception

- **Not threatened**: 63.6% of developers
- **Uncertain**: 21.3%
- **Threatened**: 15.0%
- **Trend**: Senior developers (20+ years) slightly less concerned

## Methodology

### Data Processing

1. **Data Cleaning**:

   - Removed compensation outliers (>$500K)
   - Handled missing values using `.notna()` filtering
   - Created categorical bins for continuous variables

2. **Statistical Methods**:

   - Pearson correlation coefficients
   - Descriptive statistics (mean, median, std)
   - Pivot tables and cross-tabulations
   - Categorical data binning

3. **Visualization Techniques**:
   - Box plots for distribution analysis
   - Horizontal bar charts for rankings
   - Violin plots for density distributions
   - Heatmaps for cross-tabulations
   - Stacked bar charts for categorical comparisons
   - Correlation matrices for relationship analysis

### Tools & Libraries

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical operations
- **matplotlib**: Base plotting library
- **seaborn**: Statistical visualizations
- **scipy**: Statistical tests and correlations

## Code Structure Explanation

### Main Script (`main.py`)

#### 0. Module Docstring (lines 1-18)

- Script metadata (author, institution, dates)
- Analysis overview and research questions

#### 1. Setup & Configuration (lines 20-49)

- Import libraries
- Configure plot styles (DPI, fonts, colors)
- Set publication-quality defaults

#### 2. Data Loading (lines 51-61)

- Load CSV with pandas
- Validate dataset dimensions

#### 3. Q1: Experience Analysis (lines 63-135)

- Filter compensation data
- Create experience bins
- Calculate correlation (r=0.332)
- Generate box plot

#### 4. Q2: Language Popularity (lines 137-178)

- Parse semicolon-separated languages
- Count occurrences
- Rank top 15 languages
- Create horizontal bar chart

#### 5. Q3: Education Analysis (lines 180-246)

- Map education levels to categories
- Group by education level
- Calculate statistics
- Generate violin plot

#### 6. Q4: Remote Work Analysis (lines 248-302)

- Create pivot table (crosstab)
- Calculate satisfaction scores
- Generate heatmap

#### 7. Q5: AI Threat Analysis (lines 304-358)

- Count threat perceptions
- Cross-tabulate with experience
- Create stacked bar chart

#### 8. Bonus: Correlation Matrix (lines 360-412)

- Select numeric variables
- Calculate correlation matrix
- Visualize with masked heatmap

#### 9. Summary Statistics (lines 414-447)

- Calculate dataset-wide metrics
- Print summary to console

## Visualization Details

All plots are configured with:

- **Resolution**: 300 DPI (publication quality)
- **Format**: PNG with tight bounding boxes
- **Style**: Clean whitegrid background
- **Colors**: Colorblind-friendly palettes
- **Labels**: Bold, readable fonts

### Plot Specifications

| Plot | Type               | Purpose                        | Key Feature            |
| ---- | ------------------ | ------------------------------ | ---------------------- |
| 1    | Box Plot           | Show compensation distribution | Quartiles + outliers   |
| 2    | Horizontal Bar     | Rank languages                 | Value labels           |
| 3    | Violin Plot        | Education salary density       | Distribution shape     |
| 4    | Heatmap            | Remote work patterns           | Percentage annotations |
| 5    | Stacked Bar        | AI sentiment by experience     | 100% stacked           |
| 6    | Correlation Matrix | Variable relationships         | Masked upper triangle  |

## References

- **Data Source**: Stack Overflow Developer Survey 2025
- **Official Site**: https://survey.stackoverflow.co/

## Author

Yigit Baba
Course: Data Science Basic Module
Date: November 2025

## License

This project is for educational purposes. The underlying Stack Overflow survey data is licensed under ODbL.
