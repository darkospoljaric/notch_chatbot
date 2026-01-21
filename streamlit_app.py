"""Streamlit UI for Notch Chatbot."""

import asyncio
import logging
import os
import sys

import streamlit as st
from dotenv import load_dotenv

from src.notch_chatbot.agent import create_notch_agent
from src.notch_chatbot.knowledge_base import load_knowledge_base

# Configure logging to show in terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Application starting...")

# Page config
st.set_page_config(
    page_title="Notch Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main {
        max-width: 800px;
        margin: 0 auto;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    h1 {
        text-align: center;
        color: #1f1f1f;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_chatbot():
    """Load knowledge base and create agent (cached)."""
    logger.info("Loading knowledge base from data/ directory...")
    kb = load_knowledge_base()
    logger.info(
        f"Knowledge base loaded: {len(kb.services)} services, {len(kb.case_studies)} case studies"
    )

    logger.info("Creating Notch agent...")
    agent = create_notch_agent(kb)
    logger.info("Agent created successfully")

    return agent, kb


def get_api_key():
    """Get API key from environment or Streamlit secrets."""
    # Try environment variable first
    api_key = os.getenv("OPENAI_API_KEY")

    # Try Streamlit secrets (for deployment)
    if not api_key and hasattr(st, "secrets"):
        try:
            api_key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            pass

    return api_key


async def stream_response(agent, kb, user_message, message_history):
    """Stream response from agent."""
    async with agent.run_stream(
        user_message, deps=kb, message_history=message_history
    ) as response:
        async for chunk in response.stream_text(delta=True):
            yield chunk

        # Store updated history
        st.session_state.pydantic_history = response.new_messages()


def main():
    """Main Streamlit app."""
    # Header
    st.title("💬 Notch Chatbot")
    st.markdown(
        '<p class="subtitle">Your AI assistant for Notch software development services</p>',
        unsafe_allow_html=True,
    )

    # Check for API key
    api_key = get_api_key()
    if not api_key:
        logger.error("OpenAI API key not found")
        st.error(
            "⚠️ OpenAI API key not found. Please set the `OPENAI_API_KEY` "
            "environment variable or add it to Streamlit secrets."
        )
        st.info(
            "For local development: Create a `.env` file with `OPENAI_API_KEY=your-key`\n\n"
            "For Streamlit Cloud: Add the API key in your app's secrets settings."
        )
        st.stop()

    logger.info("OpenAI API key found")

    # Set API key in environment for the agent
    os.environ["OPENAI_API_KEY"] = api_key

    # Check for SendGrid API key (optional)
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    if sendgrid_key:
        logger.info("SendGrid API key found - email proposals enabled")
    else:
        logger.warning(
            "SendGrid API key not found - email proposals disabled (this is optional)"
        )

    # Load agent and knowledge base
    try:
        logger.info("Loading knowledge base and agent...")
        with st.spinner("Loading Notch knowledge base..."):
            agent, kb = load_chatbot()
        logger.info("Chatbot loaded successfully")
    except Exception as e:
        logger.exception(f"Failed to load chatbot: {e}")
        st.error(f"Failed to load chatbot: {str(e)}")
        st.stop()

    # Initialize session state for chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.pydantic_history = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about Notch's services, case studies, or capabilities..."):
        logger.info(f"User message received: {prompt[:100]}...")  # Log first 100 chars

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Stream the response
            try:
                logger.info("Starting agent response stream...")

                # Create async generator and run it
                async def collect_response():
                    response_text = ""
                    async for chunk in stream_response(
                        agent, kb, prompt, st.session_state.pydantic_history
                    ):
                        response_text += chunk
                        message_placeholder.markdown(response_text + "▌")
                    message_placeholder.markdown(response_text)
                    return response_text

                # Run async function and get final response
                full_response = asyncio.run(collect_response())
                logger.info(
                    f"Agent response complete ({len(full_response)} chars): {full_response[:100]}..."
                )

                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

            except Exception as e:
                logger.exception(f"Error generating response: {e}")
                st.error(f"Error generating response: {str(e)}")

    # Sidebar with info
    with st.sidebar:
        st.header("About")
        st.markdown(
            """
            This chatbot helps you learn about:

            - 🔧 **Services**: Custom software, AI systems, MVPs, team extension
            - 📊 **Case Studies**: Real client success stories
            - 🏢 **Industries**: Fintech, healthcare, manufacturing, and more
            - 🤖 **AI Capabilities**: Agentic AI, machine learning integration

            **Features:**
            - 💬 Concise, conversational responses
            - 🧠 Maintains conversation context
            - 📚 Knowledge of 11 services, 7 case studies
            - ⚡ Real-time streaming
            """
        )

        st.divider()

        st.markdown("**Stats:**")
        st.metric("Messages", len(st.session_state.messages))

        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.session_state.pydantic_history = []
            st.rerun()

        st.divider()

        st.markdown(
            """
            <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            Built with ❤️ for <a href='https://www.wearenotch.com' target='_blank'>Notch</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
