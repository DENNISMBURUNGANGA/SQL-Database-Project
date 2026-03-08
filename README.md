# EPL SQL Database Project
**Course:*** MSc Data Mining and Discovery | 
**University:** University of Hertfordshire  
**Author:** Dennis Mburu Nganga

## 📌 Project Overview
This project fulfills the requirements for the Database Systems assignment by generating a sophisticated, relational synthetic database for English Premier League (EPL) analytics using Python and SQLite.

## 📊 Database Architecture
The database is designed with **Normalization** in mind to reduce redundancy. It utilizes:
* **Primary & Foreign Keys:** Enforced via `PRAGMA foreign_keys = ON`.
* **Compound Primary Key:** Implemented in the `Match_Performances` table `(match_id, player_id)` to ensure data integrity (one performance record per player, per match).



## 📈 Statistical Data Types
1. **Nominal:** `team_name`, `position` (Categorical labels).
2. **Ordinal:** `performance_rating` (Ranked: Poor < Fair < Good < Excellent).
3. **Interval:** `temperature_celsius` (Quantitative, where 0 is arbitrary).
4. **Ratio:** `distance_covered_km`, `goals_scored` (Quantitative with a meaningful absolute zero).

## 🛠️ Tech Stack & Generation
* **Language:** Python 3.x
* **Database Engine:** SQLite3
* **Generation Method:** Weighted randomization using the `random` library to ensure realistic distributions (e.g., forwards score more frequently than defenders).

## 📂 File Structure
* `SQL_Database_Project.py`: The Python source code used to build the schema and populate 4,400+ rows.
* `epl_synthetic_analytics.db`: The generated SQLite database file.
* `Technical Report...pdf`: Documentation covering methodology, schema justification, and ethical considerations.

## ⚖️ Ethics & Privacy
All player data is **synthetic**. Names are generated from a randomized pool to ensure no real-world Personal Identifiable Information (PII) is used, adhering to GDPR principles for synthetic data generation.
