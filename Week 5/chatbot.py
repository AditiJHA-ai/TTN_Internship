"""
Week 5  Simple CLI Chatbot
Demonstrates: conversation history, system prompt, temperature tuning,
token awareness, and a /reset command to clear context.
"""
 
from openai import OpenAI
 
client = OpenAI()
 
SYSTEM_PROMPT = """
You are Aria, a helpful assistant for software engineers.
You are concise, friendly, and technically precise.
When writing code, always include brief inline comments.
If you don't know something, say so clearly instead of guessing.
Keep responses under 150 words unless the user explicitly asks for more detail.
"""
 
MODEL     = "gpt-4o-mini"
MAX_HIST  = 10     # keep last N message pairs to manage context window
TEMP      = 0.7    # balanced creativity vs. consistency
 
 
def chat(history: list[dict], user_input: str) -> str:
    """Send message with full history, return assistant reply."""
    history.append({"role": "user", "content": user_input})
 
    response = client.chat.completions.create(
        model=MODEL,
        temperature=TEMP,
        max_tokens=400,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history
    )
 
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
 
    # Trim history to avoid blowing the context window
    if len(history) > MAX_HIST * 2:
        history[:] = history[-(MAX_HIST * 2):]
 
    return reply
 
 
def count_approx_tokens(history: list[dict]) -> int:
    """Rough token estimate: ~4 chars per token."""
    total = sum(len(m["content"]) for m in history)
    return total // 4
 
 
def main():
    history = []
 
    print("Aria — AI Assistant  (type /help for commands)")
    print("-" * 45)
 
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break
 
        if not user_input:
            continue
 
        # Commands
        if user_input == "/quit":
            print("Goodbye.")
            break
        elif user_input == "/reset":
            history.clear()
            print("  [Context cleared. Starting fresh.]")
            continue
        elif user_input == "/history":
            if not history:
                print("  [No history yet.]")
            for i, msg in enumerate(history):
                role = "You" if msg["role"] == "user" else "Aria"
                print(f"  [{i+1}] {role}: {msg['content'][:80]}...")
            continue
        elif user_input == "/tokens":
            print(f"  [Approx tokens in context: {count_approx_tokens(history)}]")
            continue
        elif user_input == "/help":
            print("  Commands:")
            print("    /reset    — clear conversation history")
            print("    /history  — show conversation so far")
            print("    /tokens   — show approximate token count")
            print("    /quit     — exit")
            continue
 
        reply = chat(history, user_input)
        print(f"\nAria: {reply}")
 
 
if __name__ == "__main__":
    main()
