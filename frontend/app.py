import streamlit as st
import requests
import json
import uuid
from typing import Dict, Any, Optional

# Configuration
API_URL = "http://127.0.0.1:8000"

def send_message_to_api(message: str, conversation_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Send message to the backend API"""
    try:
        payload = {
            "message": message,
            "conversation_id": conversation_id
        }
        
        response = requests.post(
            f"{API_URL}/api/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API returned status code {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Please make sure the backend server is running.")
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def initialize_session_state():
    """Initialize Streamlit session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())

def display_chat_messages():
    """Display chat messages in the UI"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_message(role: str, content: str):
    """Add a message to the chat history"""
    st.session_state.messages.append({"role": role, "content": content})

def main():
    """Main Streamlit application"""
    # Page configuration
    st.set_page_config(
        page_title="Vibe Coding Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 Vibe Coding Chatbot")
        st.markdown("---")
        
        # Conversation controls
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.session_state.conversation_id = str(uuid.uuid4())
            st.rerun()
        
        st.markdown("---")
        
        # API Status
        st.subheader("🔗 API Status")
        try:
            health_response = requests.get(f"{API_URL}/health", timeout=5)
            if health_response.status_code == 200:
                st.success("✅ API is online")
            else:
                st.error("❌ API is offline")
        except:
            st.error("❌ API is offline")
        
        st.markdown("---")
        
        # Instructions
        st.subheader("📋 Instructions")
        st.markdown("""
        1. Type your message in the chat input below
        2. The AI assistant can search the web for current information
        3. Use the clear button to start a new conversation
        """)
        
        # Conversation ID (for debugging)
        with st.expander("🔧 Debug Info"):
            st.text(f"Conversation ID: {st.session_state.conversation_id}")
            st.text(f"Messages: {len(st.session_state.messages)}")
    
    # Main chat interface
    st.title("💬 Chat with AI Assistant")
    st.markdown("Ask me anything! I can search the web for the latest information.")
    
    # Display chat messages
    display_chat_messages()
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        add_message("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = send_message_to_api(prompt, st.session_state.conversation_id)
                
                if response_data:
                    assistant_response = response_data.get("response", "I'm sorry, I couldn't process your request.")
                    
                    # Update conversation ID if provided
                    if "conversation_id" in response_data:
                        st.session_state.conversation_id = response_data["conversation_id"]
                else:
                    assistant_response = "I'm sorry, I couldn't connect to the backend service. Please try again later."
                
                # Display assistant response
                st.markdown(assistant_response)
                
                # Add assistant message to chat history
                add_message("assistant", assistant_response)

def run_app():
    """Alternative entry point for running the app"""
    main()

if __name__ == "__main__":
    main() 