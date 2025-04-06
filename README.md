# A/B Testing Framework for Product Feature Optimization

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
