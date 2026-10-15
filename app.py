import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================
# PAGE SETTINGS
# =========================
st.set_page_config(
    page_title="Netflix Analytics",
    page_icon="🎬",
    layout="wide"
)

# =========================
# PROJECT PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "netflix_titles.csv"
POSTER_DIR = BASE_DIR / "posters"

# =========================
# NETFLIX-INSPIRED DESIGN
# =========================
st.markdown("""
<style>
.stApp {
    background: #101010;
    color: #F5F5F1;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1 {
    color: #E50914 !important;
    font-weight: 900 !important;
    letter-spacing: 2px;
}

h2, h3 {
    color: #F5F5F1 !important;
    font-weight: 650 !important;
}

section[data-testid="stSidebar"] {
    background: #181818;
    border-right: 1px solid #333333;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #242424, #191919);
    padding: 22px 20px;
    border: 1px solid #383838;
    border-bottom: 3px solid #E50914;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #BDBDBD !important;
    font-size: 14px !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 30px !important;
    font-weight: 750 !important;
}

.stTextInput input {
    background: #222222;
    color: white;
    border: 1px solid #444444;
    border-radius: 8px;
}

hr {
    border-color: #333333;
}

[data-testid="stDataFrame"] {
    border: 1px solid #333333;
    border-radius: 10px;
}

[data-testid="stMultiSelect"] {
    padding-bottom: 8px;
}

.stCaption {
    color: #BDBDBD;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #383838;
    border-radius: 12px;
}

.stDownloadButton button {
    background-color: #E50914;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stDownloadButton button:hover {
    background-color: #B20710;
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# =========================
# LOAD DATASET
# =========================
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    data["release_year"] = pd.to_numeric(
        data["release_year"],
        errors="coerce"
    )

    return data


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "Could not find netflix_titles.csv. "
        "Place it in the same folder as app.py."
    )
    st.stop()

# =========================
# DASHBOARD HEADING
# =========================
st.markdown(
    """
    <h1 style="
        color: #E50914;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 0;
    ">
        NETFLIX
    </h1>
    <h3 style="
        color: #F5F5F1;
        font-size: 23px;
        margin-top: 0;
    ">
        Content Analytics Dashboard
    </h3>
    <p style="
        color: #BDBDBD;
        font-size: 16px;
    ">
        Explore content trends, audience ratings, genres,
        and movies across the Netflix catalogue.
    </p>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filter Content")

content_types = st.sidebar.multiselect(
    "Content Type",
    options=sorted(df["type"].dropna().unique()),
    default=sorted(df["type"].dropna().unique())
)

countries = sorted(
    df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .unique()
)

selected_countries = st.sidebar.multiselect(
    "Country",
    options=countries,
    default=[]
)

ratings = sorted(df["rating"].dropna().unique())

selected_ratings = st.sidebar.multiselect(
    "Rating",
    options=ratings,
    default=[]
)

years = sorted(
    df["release_year"].dropna().astype(int).unique(),
    reverse=True
)

selected_years = st.sidebar.multiselect(
    "Release Year",
    options=years,
    default=[]
)

genres = sorted(
    df["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
    .unique()
)

selected_genres = st.sidebar.multiselect(
    "Genre",
    options=genres,
    default=[]
)


# =========================
# APPLY FILTERS
# =========================
filtered = df[df["type"].isin(content_types)].copy()

if selected_years:
    filtered = filtered[
        filtered["release_year"].isin(selected_years)
    ]

if selected_genres:
    filtered = filtered[
        filtered["listed_in"].fillna("").apply(
            lambda value: any(
                genre in value.split(", ")
                for genre in selected_genres
            )
        )
    ]

if selected_countries:
    filtered = filtered[
        filtered["country"].fillna("").apply(
            lambda value: any(
                country in value.split(", ")
                for country in selected_countries
            )
        )
    ]

if selected_ratings:
    filtered = filtered[
        filtered["rating"].isin(selected_ratings)
    ]


# =========================
# KPI METRICS
# =========================
st.markdown(
    """
    <h2 style="
        color: #FFFFFF;
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    ">
        Netflix Overview
    </h2>
    <p style="
        color: #BDBDBD;
        font-size: 14px;
        margin-top: -10px;
    ">
        A quick snapshot of the titles in your selected dataset.
    </p>
    """,
    unsafe_allow_html=True
)

total_titles = len(filtered)

movies_count = (filtered["type"] == "Movie").sum()
shows_count = (filtered["type"] == "TV Show").sum()

country_count = (
    filtered["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .nunique()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Titles", f"{total_titles:,}")
col2.metric("Movies", f"{movies_count:,}")
col3.metric("TV Shows", f"{shows_count:,}")
col4.metric("Countries", f"{country_count:,}")

st.divider()

# =========================
# KEY INSIGHTS
# =========================
st.subheader("Key Insights")

rating_counts = filtered["rating"].dropna().value_counts()

genre_counts = (
    filtered["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
)

country_counts = (
    filtered["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
)

insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown("**Most Common Rating**")
    if not rating_counts.empty:
        st.metric("Rating", rating_counts.index[0])
        st.caption(f"{rating_counts.iloc[0]:,} titles")
    else:
        st.info("No rating data available.")

with insight2:
    st.markdown("**Most Common Genre**")
    if not genre_counts.empty:
        st.metric("Genre", genre_counts.index[0])
        st.caption(f"{genre_counts.iloc[0]:,} titles")
    else:
        st.info("No genre data available.")

with insight3:
    st.markdown("**Leading Country**")
    if not country_counts.empty:
        st.metric("Country", country_counts.index[0])
        st.caption(f"{country_counts.iloc[0]:,} titles")
    else:
        st.info("No country data available.")

st.divider()


# =========================
# CHART 1: MOVIES VS TV SHOWS
# =========================
left, right = st.columns(2)

with left:
    st.subheader("Movies vs TV Shows")

    type_data = (
        filtered["type"]
        .value_counts()
        .rename_axis("Type")
        .reset_index(name="Count")
    )

    fig_type = px.pie(
        type_data,
        names="Type",
        values="Count",
        hole=0.55,
        color_discrete_sequence=["#E50914", "#777777"]
    )

    fig_type.update_layout(
        paper_bgcolor="#181818",
        plot_bgcolor="#181818",
        font_color="#F5F5F1",
        margin=dict(t=35, b=25, l=25, r=25),
        legend_title_text="Content Type",
        title_font_size=18,
        legend=dict(
             bgcolor="rgba(0,0,0,0)",
             font=dict(size=13)
        )
    )
    st.plotly_chart(fig_type, use_container_width=True)


# =========================
# CHART 2: TITLES BY YEAR
# =========================
with right:
    st.subheader("Titles Released by Year")

    year_data = (
        filtered.dropna(subset=["release_year"])
        .groupby("release_year")
        .size()
        .reset_index(name="Titles")
    )

    fig_year = px.line(
        year_data,
        x="release_year",
        y="Titles",
        markers=True
    )

    fig_year.update_traces(
        line_color="#E50914",
        marker_color="#E50914"
    )

    fig_year.update_layout(
        paper_bgcolor="#181818",
        plot_bgcolor="#181818",
        font_color="#F5F5F1",
        title_font_size=18,
        xaxis_title="Release Year",
        yaxis_title="Number of Titles",
        margin=dict(t=35, b=40, l=25, r=25),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            zeroline=False
        )
    )

    st.plotly_chart(fig_year, use_container_width=True)     


# =========================
# CHART 6: MOVIE VS TV SHOW TRENDS
# =========================
st.divider()
st.subheader("Movie vs TV Show Trends Over Time")

trend_data = (
    filtered.dropna(subset=["release_year"])
    .groupby(["release_year", "type"])
    .size()
    .reset_index(name="Titles")
)

if not trend_data.empty:
    fig_trend = px.line(
        trend_data,
        x="release_year",
        y="Titles",
        color="type",
        markers=True,
        color_discrete_map={
            "Movie": "#E50914",
            "TV Show": "#AAAAAA"
        },
        labels={
            "release_year": "Release Year",
            "Titles": "Number of Titles",
            "type": "Content Type"
        }
    )

    fig_trend.update_layout(
        paper_bgcolor="#141414",
        plot_bgcolor="#141414",
        font_color="white",
        xaxis_title="Release Year",
        yaxis_title="Number of Titles",
        legend_title_text="Content Type",
        margin=dict(t=30, b=40, l=20, r=20)
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )
else:
    st.info("No release-year data is available for the selected filters.")

# =========================
# CHART 3: TOP 10 COUNTRIES
# =========================
left, right = st.columns(2)

with left:
    st.subheader("Top 10 Countries")

    country_data = (
        filtered.dropna(subset=["country"])
        .assign(
            country=lambda data: data["country"].str.split(", ")
        )
        .explode("country")
        .groupby("country")
        .size()
        .nlargest(10)
        .sort_values()
        .reset_index(name="Titles")
    )

    fig_country = px.bar(
        country_data,
        x="Titles",
        y="country",
        orientation="h",
        color="Titles",
        color_continuous_scale=["#5A0000", "#E50914"]
    )

    fig_country.update_layout(
        paper_bgcolor="#181818",
        plot_bgcolor="#181818",
        font_color="#F5F5F1",
        coloraxis_showscale=False,
        xaxis_title="Number of Titles",
        yaxis_title="Country",
        margin=dict(t=35, b=35, l=20, r=30),
        xaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        )
    )

    fig_country.update_traces(
        marker_line_color="#181818",
        marker_line_width=1
    )

    st.plotly_chart(fig_country, use_container_width=True)


# =========================
# CHART 4: TOP 10 GENRES
# =========================
with right:
    st.subheader("Top 10 Genres")

    genre_data = (
        filtered.dropna(subset=["listed_in"])
        .assign(
            Genre=lambda data: data["listed_in"].str.split(", ")
        )
        .explode("Genre")
        .groupby("Genre")
        .size()
        .nlargest(10)
        .sort_values()
        .reset_index(name="Titles")
    )

    fig_genre = px.bar(
        genre_data,
        x="Titles",
        y="Genre",
        orientation="h",
        color="Titles",
        color_continuous_scale=["#5A0000", "#E50914"]
    )

    fig_genre.update_layout(
        paper_bgcolor="#181818",
        plot_bgcolor="#181818",
        font_color="#F5F5F1",
        coloraxis_showscale=False,
        xaxis_title="Number of Titles",
        yaxis_title="Genre",
        margin=dict(t=35, b=35, l=20, r=30),
        xaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        )
    )

    fig_genre.update_traces(
        marker_line_color="#181818",
        marker_line_width=1
    )

    st.plotly_chart(fig_genre, use_container_width=True)


# =========================
# DATASET EXPLORER
# =========================
st.divider()
st.markdown(
    """
    <h2 style="
        color: #FFFFFF;
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    ">
        Explore the Netflix Dataset
    </h2>
    <p style="
        color: #BDBDBD;
        font-size: 14px;
        margin-top: -10px;
    ">
        Search, explore, and export titles from your filtered dataset.
    </p>
    """,
    unsafe_allow_html=True
)

search = st.text_input(
    "Search titles by name",
    placeholder="Enter a movie or TV show title..."
)

table_data = filtered.copy()

if search:
    table_data = table_data[
        table_data["title"].str.contains(
            search,
            case=False,
            na=False,
            regex=False
        )
    ]

columns = [
    "title",
    "type",
    "release_year",
    "rating",
    "duration",
    "listed_in",
    "country"
]

st.caption(f"Showing {len(table_data):,} titles")

st.dataframe(
    table_data[columns],
    use_container_width=True,
    hide_index=True
)

# =========================
# DOWNLOAD FILTERED DATA
# =========================
st.markdown("### Export Your Data")

st.caption(
    "Download the dataset using your selected filters and title search."
)

csv_data = table_data[columns].to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv_data,
    file_name="netflix_filtered_data.csv",
    mime="text/csv",
    key="download_filtered_csv"
)

# =========================
# CHART 5: CONTENT RATINGS
# =========================
st.divider()
st.subheader("Content Rating Distribution")

rating_data = (
    filtered.dropna(subset=["rating"])
    .groupby("rating")
    .size()
    .reset_index(name="Titles")
    .sort_values("Titles", ascending=False)
)

if not rating_data.empty:
    fig_rating = px.bar(
        rating_data,
        x="rating",
        y="Titles",
        text="Titles",
        color="Titles",
        color_continuous_scale=["#5A0000", "#E50914"],
        labels={
            "rating": "Audience Rating",
            "Titles": "Number of Titles"
        }
    )

    fig_rating.update_traces(
        textposition="outside"
    )

    fig_rating.update_layout(
        paper_bgcolor="#181818",
        plot_bgcolor="#181818",
        font_color="#F5F5F1",
        title_font_size=18,
        xaxis_title="Content Rating",
        yaxis_title="Number of Titles",
        margin=dict(t=35, b=40, l=25, r=25),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            zeroline=False
        )
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )
else:
    st.info("No rating data is available for the selected filters.")

# =========================
# CHART 7: MOVIE DURATION ANALYSIS
# =========================
st.divider()
st.subheader("Movie Duration Analysis")

movie_data = filtered[
    (filtered["type"] == "Movie")
    & filtered["duration"].notna()
].copy()

movie_data["duration_minutes"] = pd.to_numeric(
    movie_data["duration"]
    .astype(str)
    .str.extract(r"(\d+)")[0],
    errors="coerce"
)

movie_data = movie_data.dropna(
    subset=["duration_minutes"]
)

if not movie_data.empty:
    fig_duration = px.histogram(
        movie_data,
        x="duration_minutes",
        nbins=25,
        color_discrete_sequence=["#E50914"],
        labels={
            "duration_minutes": "Movie Duration (minutes)",
            "count": "Number of Movies"
        }
    )

    fig_duration.update_layout(
        paper_bgcolor="#181818",
        plot_bgcolor="#181818",
        font_color="#F5F5F1",
        title_font_size=18,
        xaxis_title="Movie Duration (minutes)",
        yaxis_title="Number of Movies",
        margin=dict(t=35, b=40, l=25, r=25),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            zeroline=False
        )
    )

    median_duration = movie_data[
        "duration_minutes"
    ].median()

    average_duration = movie_data[
        "duration_minutes"
    ].mean()

    metric1, metric2 = st.columns(2)

    metric1.metric(
        "Average Movie Duration",
        f"{average_duration:.0f} min"
    )

    metric2.metric(
        "Median Movie Duration",
        f"{median_duration:.0f} min"
    )

    st.plotly_chart(
        fig_duration,
        use_container_width=True
    )
else:
    st.info(
        "No movie duration data is available. "
        "Select Movies in the Content Type filter."
    )

# =========================
# CHART 8: TOP DIRECTORS
# =========================
st.divider()
st.subheader("Top 10 Directors")

director_data = (
    filtered.dropna(subset=["director"])
    .assign(
        director=lambda data: data["director"].str.split(", ")
    )
    .explode("director")
)

director_data = (
    director_data[
        director_data["director"].str.strip() != ""
    ]
    .groupby("director")
    .size()
    .nlargest(10)
    .sort_values()
    .reset_index(name="Titles")
)

if not director_data.empty:
    fig_directors = px.bar(
        director_data,
        x="Titles",
        y="director",
        orientation="h",
        text="Titles",
        color="Titles",
        color_continuous_scale=["#5A0000", "#E50914"],
        labels={
            "director": "Director",
            "Titles": "Number of Titles"
        }
    )

    fig_directors.update_traces(
        textposition="outside"
    )

    fig_directors.update_layout(
        paper_bgcolor="#181818",
        plot_bgcolor="#181818",
        font_color="#F5F5F1",
        title_font_size=18,
        xaxis_title="Number of Titles",
        yaxis_title="Director",
        margin=dict(t=35, b=35, l=20, r=30),
        xaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        )
    )

    st.plotly_chart(
        fig_directors,
        use_container_width=True
    )
else:
    st.info(
        "No director information is available "
        "for the selected filters."
    )

# =========================
# CONTENT DISCOVERY WITH POSTERS
# =========================
st.divider()
st.subheader("Discover Netflix Titles")
st.caption("Browse titles from your filtered Netflix dataset.")

if not filtered.empty:
    discovery_data = filtered.copy()

    discovery_data["title"] = (
        discovery_data["title"].fillna("Untitled")
    )

    discovery_data = discovery_data.sort_values(
        by="release_year",
        ascending=False,
        na_position="last"
    )

    number_to_show = st.selectbox(
        "Titles to display",
        options=[6, 9, 12],
        index=0,
        key="discovery_count"
    )

    discovery_data = discovery_data.head(number_to_show)

    cards = st.columns(3)

    for index, (_, item) in enumerate(
        discovery_data.iterrows()
    ):
        with cards[index % 3]:
            with st.container(border=True):

                title_name = str(item["title"]).strip()

                poster_files = {
                    "stranger things": "stranger_things.jpg"
                }

                poster_filename = poster_files.get(
                    title_name.lower()
                )

                if poster_filename:
                    poster_path = POSTER_DIR / poster_filename

                    if poster_path.is_file():
                        st.image(
                            str(poster_path),
                            use_container_width=True
                        )
                    else:
                        st.info(
                            "Poster not found. Check the posters folder."
                        )

                st.markdown(f"### {title_name}")

                release_year = (
                    int(item["release_year"])
                    if pd.notna(item["release_year"])
                    else "Year unknown"
                )

                st.caption(
                    f"{item['type']} · {release_year}"
                )

                rating_value = (
                    item["rating"]
                    if pd.notna(item["rating"])
                    else "Not rated"
                )

                genre_value = (
                    item["listed_in"]
                    if pd.notna(item["listed_in"])
                    else "Not available"
                )

                st.write(f"**Rating:** {rating_value}")
                st.write(f"**Genre:** {genre_value}")

                description = item.get(
                    "description",
                    "No description available."
                )

                if pd.isna(description):
                    description = "No description available."

                st.write(str(description))

else:
    st.info(
        "No titles available. Change your sidebar filters."
    )


# =========================
# TITLE DETAILS VIEWER
# =========================
st.divider()
st.subheader("Explore a Title")

if not table_data.empty:
    title_options = sorted(
        table_data["title"].dropna().unique()
    )

    selected_title = st.selectbox(
        "Choose a movie or TV show",
        options=title_options,
        key="title_details_selector"
    )

    if selected_title:
        title_info = table_data[
            table_data["title"] == selected_title
        ].iloc[0]

        st.markdown(f"### {title_info['title']}")

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:
            st.write(f"**Type:** {title_info['type']}")

            release_year = (
                int(title_info["release_year"])
                if pd.notna(title_info["release_year"])
                else "Unknown"
            )
            st.write(f"**Release year:** {release_year}")

            rating_value = (
                title_info["rating"]
                if pd.notna(title_info["rating"])
                else "Not available"
            )
            st.write(f"**Rating:** {rating_value}")

            duration_value = (
                title_info["duration"]
                if pd.notna(title_info["duration"])
                else "Not available"
            )
            st.write(f"**Duration:** {duration_value}")

        with detail_col2:
            for field in ["director", "cast", "listed_in", "country"]:
                value = title_info.get(field)

                if pd.isna(value) or not value:
                    value = "Not available"

                label = {
                    "listed_in": "Genre",
                    "director": "Director",
                    "cast": "Cast",
                    "country": "Country"
                }[field]

                st.write(f"**{label}:** {value}")

        st.markdown("**Synopsis**")

        description = title_info["description"]

        st.write(
            description
            if pd.notna(description)
            else "No description available."
        )

else:
    st.info(
        "No titles match your current filters or search. "
        "Adjust your filters to explore titles."
    )


# =========================
# FOOTER
# =========================
st.divider()
st.caption(
    "Built with Python, Pandas, Plotly and Streamlit."
)