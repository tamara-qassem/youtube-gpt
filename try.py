import openai
import streamlit as st
from llama_index import GPTVectorStoreIndex
from llama_hub.youtube_transcript import YoutubeTranscriptReader

st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
openai.api_key = "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"

# Load data and create index (replace this with your actual code)
loader = YoutubeTranscriptReader()

# Accept user input for YouTube link
yt_link = st.text_input("Enter YouTube link:")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.empty():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Create a column layout for better organization
col1, col2 = st.columns([1, 3])

# Accept user input in a fixed position
with col1:
    if yt_link:
        documents = loader.load_data(ytlinks=[yt_link])
        index = GPTVectorStoreIndex(documents)
        query_engine = index.as_query_engine()

        # User input
        if prompt := st.text_input("You:", key="user_input"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(f"You: {prompt}")
            # Display assistant response in chat message container
            with st.spinner("Thinking..."):
                try:
                    response = query_engine.query(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    with st.chat_message("assistant"):
                        st.markdown(f"Assistant: {response}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Store chat history in Streamlit session state
    st.session_state.messages = st.session_state.messages[-10:]  # Limit to the last 10 messages