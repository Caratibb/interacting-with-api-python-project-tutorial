import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

# Load environment variables from .env file
load_dotenv()

# Fetch credentials from environment variables
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

# Verify library versions
print(f"Pandas version: {pd.__version__}, NumPy version: {np.__version__}")

# Initialize Spotipy with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-library-read"
))

# Artist ID to fetch top tracks
artist_id = "378dH6EszOLFShpRzAQkVM"

try:
    # Fetch the artist's top tracks
    top_tracks = sp.artist_top_tracks(artist_id)

    # Extract track details
    track_data = []
    for track in top_tracks['tracks']:
        track_data.append({
            'Track Name': track['name'],
            'Popularity': track['popularity'],
            'Duration (min)': track['duration_ms'] / (1000 * 60),
            'Duration (sec)': (track['duration_ms'] / 1000) % 60
        })

    # Convert to DataFrame
    df = pd.DataFrame(track_data)
    print("Top Tracks Data:")
    print(df)

    # Scatterplot of popularity vs duration
    scatter_plot = sns.scatterplot(data=df, x="Popularity", y="Duration (min)")
    fig = scatter_plot.get_figure()
    fig.savefig("scatter_plot.png")

except spotipy.exceptions.SpotifyException as e:
    print(f"An error occurred: {e}")

# Use client credentials for additional API calls
sp_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                  client_secret=client_secret))

# Fetch the same artist's top tracks for comparison
response = sp_client.artist_top_tracks(artist_id)

if response:
    # Extract relevant track details
    tracks = [
        {
            'Track Name': track['name'],
            'Popularity': track['popularity'],
            'Duration (min)': track['duration_ms'] / (1000 * 60)
        }
        for track in response["tracks"]
    ]

    # Convert to DataFrame and sort by popularity
    tracks_df = pd.DataFrame(tracks)
    tracks_df.sort_values(by="Popularity", ascending=False, inplace=True)

    # Display the top 3 tracks
    print("Top 3 Tracks by Popularity:")
    print(tracks_df.head(3))

    # Scatterplot for duration and popularity
    scatter_plot = sns.scatterplot(data=tracks_df, x="Popularity", y="Duration (min)")
    fig = scatter_plot.get_figure()
    fig.savefig("scatter_plot_comparison.png")
