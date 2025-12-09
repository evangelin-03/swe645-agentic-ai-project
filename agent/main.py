import os
from dotenv import load_dotenv
load_dotenv()

# Try to import Google Gemini client
client = None
try:
    from google import genai
    API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if API_KEY:
        try:
            client = genai.Client(api_key=API_KEY)
        except Exception as e:
            print("Warning: could not create genai.Client():", e)
            client = None
    else:
        print("Note: GEMINI_API_KEY not set -> running in SIMULATION mode.")
except Exception:
    print("Note: google-genai package not installed -> running in SIMULATION mode.")
    client = None

from agent.langgraph_config import build_agent_graph
from agent.memory.faiss_store import FaissMemory

def run_cli():
    graph = build_agent_graph(client=client)
    memory = FaissMemory()
    print("Agent ready. Type 'exit' or 'quit' to stop. Use 'retrieve: <text>' to search memory.")

    session_history = []

    while True:
        q = input("\nUser> ").strip()
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        # retrieval command
        if q.lower().startswith("retrieve:"):
            query_text = q.split(":", 1)[1].strip()
            results = memory.search(query_text, top_k=5)
            if not results:
                print("No documents found in long-term memory.")
            else:
                print("\n--- Memory Results ---")
                for r in results:
                    print(f"- ID: {r['id']}  Score: {r['score']:.4f}")
                    print(f"  Text: {r['text'][:300]}")
            continue

        # short-term memory
        session_history.append({"role": "user", "content": q})
        recent_context = "\n".join([f"{m['role']}: {m['content']}" for m in session_history[-5:]])

        # build prompt for the agent
        state = {
            "prompt": f"Context:\n{recent_context}\n\nUser: {q}"
        }

        # run the agent plan
        result = graph.run(state)
        plan = result.get("plan", "(no plan returned)")

        print("\n=== AGENT PLAN ===\n")
        print(plan)

        # human confirmation
        conf = input("\nExecute plan? (y/n) > ").strip().lower()
        if not conf.startswith("y"):
            print("Execution aborted by human.")
            session_history.append({"role": "assistant", "content": "(plan aborted)"})
            continue

        # execute the plan
        if client is None:
            exec_result_text = "(simulated) " + plan.splitlines()[0]
            print("Result:", exec_result_text)
        else:
            try:
                exec_resp = client.models.generate_content(
                    model=graph.model,
                    contents=f"Execute the plan:\n{plan}"
                )
                if hasattr(exec_resp, "text") and exec_resp.text:
                    exec_result_text = exec_resp.text
                else:
                    exec_result_text = str(exec_resp)
                print("Result:", exec_result_text)
            except Exception as e:
                exec_result_text = f"(Gemini execution failed: {e})"
                print(exec_result_text)

        # save to long-term memory
        import time, hashlib
        doc_id = hashlib.sha1(f"{time.time()}-{q}".encode("utf8")).hexdigest()[:12]
        doc_text = f"User: {q}\nAgent: {exec_result_text}"

        if memory.store_document(doc_id, doc_text, {"source": "agent_run"}):
            print(f"Saved to memory with id {doc_id}")
        else:
            print("Failed to save to memory.")

        # store result in short-term memory
        session_history.append({"role": "assistant", "content": exec_result_text})


if __name__ == "__main__":
    run_cli()
