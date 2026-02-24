## Deep Research Agent (OpenAI SDK)

This project is a small, end‑to‑end **deep research agent** built on top of the **OpenAI Python SDK**, exposed through a simple Gradio UI and a set of modular agents (planner, searcher, writer, and emailer).

The core idea is to use the SDK to define **specialized agents with clear instructions and typed outputs**, then orchestrate them into a multi‑step workflow inside `ResearchManager`.

---

### High‑level architecture

- **UI layer (`deep_research.py`)**  
  - Uses `gradio.Blocks` to expose a single text box (`query_textbox`) and a **streaming** `run` function.  
  - `run(query)` delegates all work to `ResearchManager().run(query)` and yields status updates and the final markdown report back into the Gradio `Markdown` component.

- **Orchestrator (`research_manager.py`)**  
  - `ResearchManager.run` wires together four agent steps, each of which runs through a common `Runner` abstraction on top of the OpenAI SDK:
    - **Planner agent** (`planner_agent`): turns the original query into a structured `WebSearchPlan` (a list of `WebSearchItem` objects).  
    - **Search agent** (`search_agent`): executes each planned search using a web search tool and summarizes the results.  
    - **Writer agent** (`writer_agent`): takes the original query plus search summaries and produces a long‑form markdown `ReportData` object (short summary, full report, follow‑up questions).  
    - **Email agent** (`email_agent`): converts the markdown report into a well‑formatted HTML email and sends it via SMTP using a tool function.
  - Uses `trace` and `gen_trace_id` from `agents` to send trace metadata to the OpenAI platform, making it easy to inspect each step at `https://platform.openai.com/traces`.

- **Agent definitions (`planner_agent.py`, `search_agent.py`, `writer_agent.py`, `email_agent.py`)**  
  - Each file defines an `Agent` instance from the local `agents` module, which internally wraps the **OpenAI SDK client**:
    - **Model configuration**: all agents are configured with `model="gpt-4o-mini"` (or similar OpenAI models).  
    - **Instructions**: rich, role‑specific instructions guide the model’s behavior (planner, researcher, writer, email composer/sender).  
    - **Tools**:
      - `search_agent` attaches a `WebSearchTool` tool and uses `ModelSettings(tool_choice="required")` so the SDK enforces tool calling for web search.  
      - `email_agent` exposes a `send_html_email(subject, html_body)` function‑tool (decorated with `@function_tool`) that sends the final report as HTML through Gmail’s SMTP server.
    - **Typed outputs**: `planner_agent` and `writer_agent` specify `output_type` as Pydantic models (`WebSearchPlan`, `ReportData`), letting the SDK responses be parsed into strongly‑typed Python objects instead of raw text.

---

### Running the app

From the `deep-research-agent-SDK` directory:

```bash
pip install -r requirements.txt  # or install gradio, python-dotenv, pydantic, openai, etc.

# Make sure your OpenAI API key and any search API keys are in your .env
export OPENAI_API_KEY=...

python deep_research.py
```

This will open the Gradio interface in your browser. Enter a research query, and the app will:

1. Plan several web searches using the planner agent (OpenAI SDK + structured output).  
2. Run those searches through the search agent using tool calling.  
3. Generate a long‑form markdown report via the writer agent.  
4. Convert it into an email via the email agent.  
5. Stream progress and the final report back to the UI, while recording a full trace in the OpenAI dashboard.

---

### Summary

In short, this project demonstrates how to:

- Wrap the **OpenAI Python SDK** in a lightweight `Agent` / `Runner` layer.  
- Combine **tool calling**, **structured outputs (Pydantic models)**, and **tracing** to build a robust multi‑step deep research workflow.  
- Surface the whole experience behind a simple, user‑friendly Gradio interface.

