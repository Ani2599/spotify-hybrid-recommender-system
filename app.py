import streamlit as st
import pandas as pd
from content_based_filtering import recommend
from scipy.sparse import load_npz


# transformed data path
transformed_data_path = "data/transformed_data.npz"

# clean data path
cleaned_data_path = "data/cleaned_data.csv"

# load the data
data = pd.read_csv(cleaned_data_path)

# load the transformed data
transformed_data = load_npz(transformed_data_path)

# Title
st.title("Welcome to Spotify Song Recommender")

# Subheader
st.write('### Enter the name of a song and the recommender will suggest similar songs 🎵🎧')

# Text Input
song_name = st.text_input('Enter a song name:')
st.write('You entered:', song_name)
# lower case the input
song_name = song_name.lower()

# k recommndations
k = st.selectbox('How many recommendations do you want?', [5,10,15,20], index=1)

if st.button('Get Recommendations'):
    if (data["name"].str.lower() == song_name).any():
        st.write('Recommendations for', f"**{song_name}**")
        recommendations = recommend(song_name, data, transformed_data, k)  # Removed artist name
        
        if recommendations.empty or not all(col in recommendations.columns for col in ['name', 'artist', 'spotify_preview_url']):
            st.write("No valid recommendations found. Please try another song.")
        else:
            for idx, (_, recommendation) in enumerate(recommendations.iterrows()):
                song_name = recommendation['name'].title()
                artist_name = recommendation['artist'].title()
                
                if idx == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{song_name}** by **{artist_name}**")
                elif idx == 1:
                    st.markdown("### Next Up 🎵")
                    st.markdown(f"#### {idx}. **{song_name}** by **{artist_name}**")
                else:
                    st.markdown(f"#### {idx}. **{song_name}** by **{artist_name}**")
                
                if pd.notna(recommendation['spotify_preview_url']):
                    st.audio(recommendation['spotify_preview_url'])
                else:
                    st.write("Preview not available for this song.")
                st.write('---')
    else:
        st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")