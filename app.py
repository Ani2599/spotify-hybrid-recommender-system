import streamlit as st
import pandas as pd
from content_based_filtering import content_recommendation
from scipy.sparse import load_npz
from numpy import load
from collaborative_filtering import collaborative_recommendation
from hybrid_recommendations import HybridRecommenderSystem as hrs

# load the data
cleaned_data_path = "data/cleaned_data.csv"
songs_data = pd.read_csv(cleaned_data_path)

# load the transformed data
transformed_data_path = "data/transformed_data.npz"
transformed_data = load_npz(transformed_data_path)

# load the track ids
track_ids_path = "data/track_ids.npy"
track_ids = load(track_ids_path,allow_pickle=True)

# load the filtered songs data
filtered_data_path = "data/collab_filtered_data.csv"
filtered_data = pd.read_csv(filtered_data_path)

# load the interaction matrix
interaction_matrix_path = "data/interaction_matrix.npz"
interaction_matrix = load_npz(interaction_matrix_path)

# load the transformed hybrid data
transformed_hybrid_data_path = "data/transformed_hybrid_data.npz"
transformed_hybrid_data = load_npz(transformed_hybrid_data_path)

# Title
st.title("Welcome to Spotify Song Recommender")

# Subheader
st.write('### Enter the name of a song and the recommender will suggest similar songs 🎵🎧')

# Text Inputs with unique keys
song_name = st.text_input('Enter a song name:', key='song_input')
st.write('You entered:', song_name)
artist_name = st.text_input('Enter the artist name:', key='artist_input')
st.write('You entered:', artist_name)

# lowercase the input
song_name = song_name.lower() if song_name else ""
artist_name = artist_name.lower() if artist_name else ""

# k recommendations with unique key
k = st.selectbox('How many recommendations do you want?', 
                 [5,10,15,20], 
                 index=1,
                 key='k_select')

# type of filtering with unique key
filtering_type = st.selectbox(label= 'Select the type of filtering:', 
                               options= ['Content-Based Filtering', 
                                         'Collaborative Filtering',
                                         "Hybrid Recommender System"],
                               index= 2)

# Button
if filtering_type == 'Content-Based Filtering':
     if st.button('Get Recommendations'):
         if ((songs_data["name"] == song_name) & (songs_data['artist'] == artist_name)).any():
             st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
             recommendations = content_recommendation(song_name=song_name,
                                                      artist_name=artist_name,
                                                      songs_data=songs_data,
                                                      transformed_data=transformed_data,
                                                      k=k)
             
             # Display Recommendations
             for ind , recommendation in recommendations.iterrows():
                 song_name = recommendation['name'].title()
                 artist_name = recommendation['artist'].title()
                 
                 if ind == 0:
                     st.markdown("## Currently Playing")
                     st.markdown(f"#### **{song_name}** by **{artist_name}**")
                     st.audio(recommendation['spotify_preview_url'])
                     st.write('---')
                 elif ind == 1:   
                     st.markdown("### Next Up 🎵")
                     st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                     st.audio(recommendation['spotify_preview_url'])
                     st.write('---')
                 else:
                     st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                     st.audio(recommendation['spotify_preview_url'])
                     st.write('---')
         else:
             st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")
             
elif filtering_type == 'Collaborative Filtering':
     if st.button('Get Recommendations'):
         if ((filtered_data["name"] == song_name) & (filtered_data["artist"] == artist_name)).any():
             st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
             recommendations = collaborative_recommendation(song_name=song_name,
                                                            artist_name=artist_name,
                                                            track_ids=track_ids,
                                                            songs_data=filtered_data,
                                                            interaction_matrix=interaction_matrix,
                                                            k=k)
             # Display Recommendations
             for ind , recommendation in recommendations.iterrows():
                 song_name = recommendation['name'].title()
                 artist_name = recommendation['artist'].title()
                 
                 if ind == 0:
                     st.markdown("## Currently Playing")
                     st.markdown(f"#### **{song_name}** by **{artist_name}**")
                     st.audio(recommendation['spotify_preview_url'])
                     st.write('---')
                 elif ind == 1:   
                     st.markdown("### Next Up 🎵")
                     st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                     st.audio(recommendation['spotify_preview_url'])
                     st.write('---')
                 else:
                     st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                     st.audio(recommendation['spotify_preview_url'])
                     st.write('---')
         else:
             st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")

elif filtering_type == "Hybrid Recommender System":
    if st.button('Get Recommendations'):
        if ((filtered_data["name"].str.strip().str.lower() == song_name.strip()) & 
            (filtered_data["artist"].str.strip().str.lower() == artist_name.strip())).any():
            
            st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
            
            # Call the Hybrid Recommender System
            recommender = hrs(
                song_name=song_name,
                artist_name=artist_name,
                number_of_recommendations=k,
                weight_content_based=0.3,
                weight_collaborative=0.7,
                songs_data=filtered_data,
                transformed_matrix=transformed_hybrid_data,
                track_ids=track_ids,
                interaction_matrix=interaction_matrix
            )
            
            # Assuming `get_recommendations()` returns a DataFrame
            recommendations = recommender.give_recommendations()
            
            # Display Recommendations
            for ind, recommendation in recommendations.iterrows():
                current_song = recommendation['name'].title()
                current_artist = recommendation['artist'].title()
                
                if ind == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{current_song}** by **{current_artist}**")
                    if pd.notna(recommendation['spotify_preview_url']):
                        st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
                elif ind == 1:
                    st.markdown("### Next Up 🎵")
                    st.markdown(f"#### {ind}. **{current_song}** by **{current_artist}**")
                    if pd.notna(recommendation['spotify_preview_url']):
                        st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
                else:
                    st.markdown(f"#### {ind}. **{current_song}** by **{current_artist}**")
                    if pd.notna(recommendation['spotify_preview_url']):
                        st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
        else:
            st.error(f"Sorry, we couldn't find '{song_name}' by '{artist_name}' in our database. Please try another song.")             