import streamlit as st
import numpy as np
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import time

st.title('Do You Want to Play Something Else?')
st.subheader('Board Game Recommendations')

with open('rec_df.pickle', 'rb') as f:
    df = pickle.load(f)

with open('exp_imp_dict.pickle', 'rb') as exp_imp_dict_pickle:
    exp_imp_dict = pickle.load(exp_imp_dict_pickle)

drop_cols = ['name','url','yr_pub','min_players','max_players','avg_play_time','min_play_time',\
                'max_play_time','min_age','complexity','avg_user_rating']

def make_clickable(url, text):
    return f'<a target="_blank" href="{url}">{text}</a>'

df['url'] = df['url'].apply(make_clickable, args = ('BGG Link',))

game_name = st.text_input("What's a game you like?",'Pandemic')
st.write('User searched for this game: ', game_name)
game_index = df[df['name']==game_name.title()].index.values
Y = df

filters = st.checkbox('Additional Filters',False)
if filters:
    st.sidebar.markdown('Additional Filters:')
    players = st.sidebar.number_input('Number of Players: ',
        0, 12000, 4)
    st.write('Players:', players)
    avg_play_time = st.sidebar.number_input('Playing Time (mins)', 0, 30000000, 60)
    st.write('Playing Time: ',avg_play_time)
    min_age = st.sidebar.number_input('Minimum Recommended Age: ', 0, 2017, 0)
    st.write('Minimum Age: ', min_age)
    Y = Y[(Y['min_players']<=players)&(Y['max_players']>=players)&(Y['avg_play_time']<=avg_play_time)&\
          (Y['min_age']<=min_age)]

exp_imp = st.checkbox('Remove Expansions/Implementations/Integrations/Compilations?',False)
if exp_imp:
    Y = Y[~Y['name'].isin(exp_imp_dict[game_name])]

num_results = st.slider('How many results?',1,20,5)

#@st.cache
#def recommendation(game_index=game_index,Y=Y):
#    try:
#        cos_sim = cosine_similarity(X=df.iloc[game_index].drop(drop_cols,axis=1),Y=Y.drop(drop_cols,axis=1),dense_output=False)
#        idxs = np.argsort(cos_sim)[:,-(num_results+1):-1]
#        result = (Y.iloc[idxs[0]][['name','url']].to_html(escape = False))
#        return result
#    except IndexError:
#        st.error('There are no games with the given parameters, please adjust your filters')
#    except ValueError:
#        st.error('We cannot find the game you entered, please try again or search which games are included below')

#rec = recommendation(game_index,Y)
#st.write(rec, unsafe_allow_html = True)
#try:
#    st.write(Y.iloc[rec[0]][['name','url']].to_html(escape = False), unsafe_allow_html = True)
#except IndexError:
#        st.error('There are no games with the given parameters, please adjust your filters')
#except ValueError:
#        st.error('We cannot find the game you entered, please try again or search which games are included below')

try:
    cos_sim = cosine_similarity(X=df.iloc[game_index].drop(drop_cols,axis=1),Y=Y.drop(drop_cols,axis=1),dense_output=False)
    idxs = np.argsort(cos_sim)[:,-(num_results+1):-1]
    for idx in idxs[::]:
        st.write(Y.iloc[idx][['name','url']].to_html(escape = False), unsafe_allow_html = True)
except IndexError:
    st.error('There are no games with the given parameters, please adjust your filters')
except ValueError:
    st.error('We cannot find the game you entered, please try again or search which games are included below')


with st.beta_expander("Search for game name"):
    game_search = st.text_input("Please enter your game search?",'Pandemic')
    search = df[df['name'].str.contains(game_search)]
    st.table(search['name'])
