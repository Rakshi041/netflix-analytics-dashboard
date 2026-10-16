 Netflix Analytics Dashboard

An interactive data analytics dashboard built with Python, Pandas, Plotly Express, and Streamlit to explore Netflix movies and TV shows.

Live Demo

**Try the dashboard:** [Open Netflix Analytics Dashboard](https://netflix-analytics-dashboard-vmcpm8zrkasugbnobnvcdb.streamlit.app/)

Project Overview

This project explores a Netflix titles dataset to understand content distribution, ratings, release trends, genres, countries, and directors. The dashboard allows users to interact with the data through filters and visualisations.

 Features

- Interactive filters for content type, country, rating, release year, and genre.
- Key performance indicators (KPIs) for total titles, movies, TV shows, and countries.
- Visualisations for content distribution, release-year trends, genres, countries, directors, and ratings.
- Movie-duration analysis.
- Title search and detailed title descriptions.
- CSV download for filtered data.
- Dynamic key insights based on selected filters.

Technologies Used

- **Python** — application logic and data processing
- **Pandas** — data manipulation and analysis
- **Plotly Express** — interactive data visualisations
- **Streamlit** — dashboard development and deployment
- **Google Colab** — exploratory data analysis

📊 Dataset

The project uses a Netflix titles dataset containing information such as title, content type, director, cast, country, release year, rating, duration, genre, and description.

💻 Run Locally

1. Clone the repository:

   ```bash
   git clone PASTE_YOUR_GITHUB_REPOSITORY_URL_HERE
   ```

2. Open the project directory:

   ```bash
   cd netflix-analytics-dashboard
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure the dataset file, `netflix_titles.csv`, is available in the project directory.

5. Run the dashboard:

   ```bash
   streamlit run app.py
   ```

project Goals

- Practise exploratory data analysis.
- Build interactive data visualisations.
- Learn to develop and deploy a data analytics application.
- Present data insights through a user-friendly interface.

Future Improvements

- Add more detailed comparisons and insights.
- Include additional title posters.
- Expand the dashboard with more advanced analytics.

Author

Developed as a personal data analytics project to practise Python, data analysis, visualisation, and dashboard development.
