import streamlit as st
from llm import ask_llm
from prompt import system_prompt


def clear_chat_history():

    # Clear conversation history
    if "conversation_history" in st.session_state:
        st.session_state.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]  # Added the missing closing bracket here
    
    # Also clear the displayed messages if you're storing them separately
    if "messages" in st.session_state:
        st.session_state.messages = []

with st.sidebar:
    
    openai_api_key = st.text_input("API Key", key="chatbot_api_key", type="password")
    model_option = st.selectbox(
        "Models",
        ["gpt-4o-2024-08-06", "anthropic/claude-3-opus", "google/gemini-pro"],
        index=0
    )


     # Add clear chat button
    st.button("Clear Chat History", on_click=clear_chat_history, key="clear_chat")

     # Add some helpful information
    st.markdown("---")
    st.markdown("### About")
    st.markdown("NBA Player Q&A Assistant can answer questions about NBA players, teams, games and statistics.")

# Main content
st.title("🏀 NBA player Q&A assistant")
st.caption("Ask any question about NBA players")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your NBA questions?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    st.chat_message("user").write(prompt)
    with st.spinner("Thinking..."):
        msg = ask_llm(prompt, model_option, openai_api_key)
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)