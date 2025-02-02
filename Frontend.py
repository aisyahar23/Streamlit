# Generate a streamlit app for your chatbot application created in Project 4
# Import load_model from chatbot
from chatbotBackend import load_model, bot_respond
# Import streamlit package
import streamlit as st

# Insert title 'My Chatbot App'
st.title('My Chatbot App')

# Sidebar
# Insert a sidebar title 'Sidebar'
st.sidebar.title('Sidebar')
# Insert a sidebar subheader 'Pages'
st.sidebar.subheader('Pages')
# Insert a sidebar selectbox 'Select a page' with options 'Home' and 'Chatbot' and assign it to variable 'app_mode'
app_mode = st.sidebar.selectbox('Select a page', ['Home', 'Chatbot'])

# If app_mode is 'Home'
if app_mode == 'Home':
    # Display 'Chat with me if you feel bored' using st.markdown
    st.markdown('Chat with me if you feel bored')
    # Display any video from youtube using st.video
    st.video('https://youtu.be/Kn1HF3oD19c')
# Else if app_mode is 'Chatbot'
elif app_mode == 'Chatbot':
    # Display 'Please talk to me' using st.text
    st.text('Please talk to me')
    # Call load_model
    load_model()
    # Insert a text input 'You:' and assign it to variable 'text'
    text = st.text_input('You:')
    # If text is not empty
    if text:
        # Display 'Chatbot:' using st.write
        st.write('Chatbot:')
        # While the response is loading, display 'Loading...' using st.spinner
        with st.spinner('Loading...'):
            # Display the response from bot_respond(text) using st.write
            st.write(bot_respond(text))

# Run the app:
# py -m streamlit run 6-Advanced1-Chatbot.py
