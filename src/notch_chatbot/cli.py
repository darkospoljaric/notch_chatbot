"""CLI interface for the Notch chatbot."""

import asyncio
import sys
from dotenv import load_dotenv

from .agent import create_notch_agent
from .knowledge_base import load_knowledge_base


async def async_main() -> None:
    """Async main function for streaming support."""
    # Load knowledge base
    print("Loading Notch knowledge base...", file=sys.stderr)
    kb = load_knowledge_base()
    print(
        f"Loaded {len(kb.services)} services, {len(kb.case_studies)} case studies, "
        f"and {len(kb.use_cases)} use cases.\n",
        file=sys.stderr,
    )

    # Create agent
    agent = create_notch_agent(kb)

    # Initialize conversation history
    message_history = []

    # Print welcome message
    print("=" * 60)
    print("Welcome to Notch Chatbot!")
    print("=" * 60)
    print(
        "\nI'm here to help you learn about Notch's software development services."
    )
    print("Ask me about our capabilities, case studies, or how we can help you.\n")
    print('Type "exit" or press Ctrl+C to quit.\n')

    # Interactive loop with streaming
    while True:
        try:
            # Get user input (running in executor to avoid blocking)
            loop = asyncio.get_event_loop()
            user_input = await loop.run_in_executor(None, lambda: input("You: ").strip())

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nThank you for chatting! Visit www.wearenotch.com for more information.")
                break

            print("Notch: ", end="", flush=True)

            # Run agent with streaming, passing conversation history
            async with agent.run_stream(
                user_input, deps=kb, message_history=message_history
            ) as response:
                async for chunk in response.stream_text(delta=True):
                    print(chunk, end="", flush=True)

            print()  # Add newline after response

            # Update message history with the new messages from this turn
            message_history = response.new_messages()

        except KeyboardInterrupt:
            print("\n\nGoodbye!", file=sys.stderr)
            break
        except Exception as e:
            print(f"\nError: {e}", file=sys.stderr)
            print("Let's try again.\n")
            continue


def main() -> None:
    """Run the Notch chatbot CLI."""
    # Load environment variables from .env file
    load_dotenv()

    try:
        # Run the async main function
        asyncio.run(async_main())
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(
            "Make sure the data directory exists with all required JSON files.",
            file=sys.stderr,
        )
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGoodbye!", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
