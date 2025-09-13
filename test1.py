import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

def load_data(file_path='imdb_top_1000.csv'):
    try:
        df = pd.read_csv(file_path)
        df['combined_features'] = df['Genre'].fillna('') + ' ' + df['Overview'].fillna('')
        return df
    except FileNotFoundError:
        print(Fore.RED + f"Error: The file '{file_path}' was not found.")
        exit()

movies_df = load_data()

def list_genres(df):
    return sorted(set(
        genre.strip()
        for sublist in df['Genre'].dropna().str.split(', ')
        for genre in sublist
    ))
genres = list_genres(movies_df)

print(genres)

# Recommend movies based on filters (genre, mood, rating)
def recommend_movies(genre=None, mood=None, rating=None, top_n=5):
    filtered_df = movies_df
    if genre:
        filtered_df = filtered_df[filtered_df['Genre'].str.contains(genre, case=False, na=False)]
    if rating:
        filtered_df = filtered_df[filtered_df['IMDB_Rating'] >= rating]

    filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)  # Randomize the order

    recommendations = []
    for idx, row in filtered_df.iterrows():
        overview = row['Overview']
        if pd.isna(overview):
            continue
        polarity = TextBlob(overview).sentiment.polarity
        if (mood and ((TextBlob(mood).sentiment.polarity < 0 and polarity > 0) or polarity >= 0)) or not mood:
            recommendations.append((row['Series_Title'], polarity))
        if len(recommendations) == top_n:
            break

    return recommendations if recommendations else "No suitable movie recommendations found."



recs = recommend_movies(genre="Adventure", mood="positive", rating=8, top_n=5)


for item in recs:
 (title,sentiment) = item
 print(f"{title} - {sentiment}")
