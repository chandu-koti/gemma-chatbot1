import streamlit as st
from ollama import chat
from ollama import ChatResponse

# Streamlit app configuration
st.set_page_config(
    page_title="Gemma2 Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# App title and description
st.title("🤖 Gemma2 Chat Assistant")
st.markdown("Ask any question and get responses from Gemma2 AI model via Ollama")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response from Gemma2
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response: ChatResponse = chat(
                    model='gemma2:2b', 
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt,
                        },
                    ]
                )
                
                # Get the response content
                assistant_response = response.message.content
                
                # Display the response
                st.markdown(assistant_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                
            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ Information")
    st.markdown("""
    **Model:** Gemma2 2B
    
    **Features:**
    - Real-time chat interface
    - Chat history preservation
    - Error handling
    
    **Requirements:**
    - Ollama running locally
    - Gemma2 model downloaded
    """)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()