# A/B Testing Framework for Product Feature Optimization

AB Testing Framework for Feature Optimization is a data-driven solution that automates the evaluation of new product features using robust statistical analysis, such as **t-tests**, **chi-squared** tests, and effect size measurements. 
Leveraging an LLM API (Gemini 2.0 Flash) for report generation, it translates complex analytic results into clear, actionable insights. This framework not only simulates realistic user behavior with synthetic data but also provides interactive visualizations to support informed decision-making.


---

## Features

- **Fake Data Generation:**  
  Automatically generates synthetic data including `user_id`, `group`, `converted`, `clicks`, `views`, and more.

- **Statistical Analysis:**  
  Uses statistical tests to analyze the results:
  - **T-Test:** Evaluates differences in mean conversion rates.
  - **Chi-Squared Test:** Checks for significant differences in conversion proportions.
  - **Effect Size:** Computes Cohen's d to gauge the practical significance of the differences.

- **Metrics Calculation:**  
  Calculates critical metrics:
  - `total_users`: Count of users.
  - `total_converted`: Sum of converted users.
  - `conversion_rate`: Mean conversion rate.
  - `avg_clicks`: Average number of clicks.
  - `avg_views`: Average number of views.

- **Google Gemini Integration:**  
  Connects to the Google Gemini 2.0 Flash API to create a detailed report on the experiment.

- **Interactive Visualizations:**  
  Creates several plots for better interactivity and insight:
  - **Conversion Rates with Confidence Intervals**
  - **Daily Conversion Rates Over Time**
  - **Cumulative Conversion Rates Over Time**
  - **User Funnel from Views to Conversions**
  - **Distributions of Clicks and Views**

- **PDF Report Generation:**  
  Combines reports and plots into a single PDF file.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ab-testing-framework.git
   cd ab-testing-framework

2. **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
---

## Usage

**Data management in this project has not been fully optimized yet. To use it effectively, your data structure must align with the predefined format.**

1. Save the data in the 'data/raw' path.
2. **Run:**
    ```bash
    python3 main.py
---

## 🧾 Dataset Description

This dataset simulates user interaction data for an A/B testing experiment conducted in a fintech mobile app. It contains behavioral and conversion data for both control and test groups.

### 1. `user_id`
- **Type:** Integer  
- **Description:** A unique identifier for each user in the dataset.  
- **Example Value:** `1`, `2`, `3`, etc.  
- **Purpose:** Used to uniquely identify each user in the experiment.

### 2. `group`
- **Type:** Categorical (`'control'` or `'test'`)  
- **Description:** Indicates whether the user is in the control group (old app experience) or test group (with the new feature).  
- **Example Value:** `'control'`, `'test'`  
- **Purpose:** Differentiates users into two experiment groups for analysis.

### 3. `converted`
- **Type:** Binary (`0` or `1`)  
- **Description:** Whether the user completed the target action, such as making a transaction or clicking a key feature.  
- **Example Value:** `0` (did not convert), `1` (converted)  
- **Purpose:** Core performance metric for evaluating the success of the tested feature.

### 4. `timestamp`
- **Type:** DateTime  
- **Description:** The date and time the user's interaction was recorded.  
- **Example Value:** `2025-01-01 00:01:00`  
- **Purpose:** Enables time-based analysis and helps detect any patterns or seasonality in behavior or conversion.

### 5. `clicks`
- **Type:** Integer  
- **Description:** The number of clicks the user made within the app during the test period.  
- **Example Value:** `3`, `5`, `7`, etc.  
- **Purpose:** Measures user interaction level and engagement with the app.

### 6. `views`
- **Type:** Integer  
- **Description:** Number of pages or screens the user viewed during the test period.  
- **Example Value:** `6`, `8`, `10`, etc.  
- **Purpose:** Represents overall user activity and helps analyze general engagement across app features.

---

## Contributing

**Contributions are welcome!** Please fork the repository and submit your pull requests. For major changes, open an issue first to discuss what you'd like to change.

