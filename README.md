# 🏏 IPL Analytics Dashboard

An interactive data analytics dashboard built with Python, Pandas, Plotly, and Streamlit to analyze Indian Premier League (IPL) match data.

## 📊 Features

- **Season Filter** — Filter all charts by IPL season
- **Top Metrics** — Total matches, teams, seasons, most winning team
- **Team Win Count** — Bar chart of wins by each team
- **Toss Decision Analysis** — Pie charts for bat vs field & toss impact on result
- **Top 10 Batsmen** — All-time run scorers horizontal bar chart
- **Season-wise Match Trend** — Line chart of matches per season
- **Win Margin Analysis** — Histograms for win by runs & wickets

## 🛠️ Tech Stack

- Python 3
- Pandas
- Plotly Express
- Streamlit

## 🚀 How to Run

1. Clone the repo:
```bash
git clone https://github.com/sayan-bhadra/ipl-dashboard.git
cd ipl-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the IPL dataset from Kaggle:
   - [IPL Dataset on Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)
   - Place `matches.csv` and `deliveries.csv` in the project folder

4. Run the app:
```bash
streamlit run ipl.py
```

## 📁 Project Structure

```
ipl-dashboard/
│
├── ipl.py              ← Main Streamlit app
├── matches.csv         ← IPL matches data (download from Kaggle)
├── deliveries.csv      ← Ball-by-ball data (download from Kaggle)
├── requirements.txt    ← Python dependencies
└── README.md
```

## 📸 Dashboard Preview

The dashboard has a dark cricket-themed UI with orange/red color scheme across all interactive charts.

## 👤 Author

**Sayan Bhadra**  
B.Sc Data Science — Techno India University  
GitHub: [@sayan-bhadra](https://github.com/sayan-bhadra)
# ipl-dashboard
