# Digital Twin Agent

An AI "digital twin" chat app built with **OpenAI** and **Gradio**. It talks to visitors in the first person, as Ahmed Rafi Hasan, about his career, research, skills and experience. Its answers come from a LinkedIn profile export and a short written summary.

The agent can also:

- **search the web** (DuckDuckGo) for public info that isn't in its context, like new publications or talks,
- **record unanswered questions**, and
- **capture contact details** from visitors who want to get in touch.

The last two send a push notification to your phone through [Pushover](https://pushover.net/).

---

## Project structure

```
digital-twin-agent-scratch/
├── src/                     # The Digital Twin app
│   ├── app.py               # Entry point: Gradio UI, chat loop, API-key handling
│   ├── context.py           # Builds the system prompt from docs/linkedin.pdf + docs/summary.txt
│   ├── tools.py             # Tool definitions: web_search, record_user_details, record_unknown_question
│   ├── styles.py            # Theme, CSS, JS, header/profile HTML, example prompts
│   ├── docs/
│   │   ├── linkedin.pdf     # LinkedIn profile exported as PDF
│   │   └── summary.txt      # Short personal summary
│   ├── requirements.txt     # Dependencies for Hugging Face Spaces deployment
│   └── README.md            # Hugging Face Spaces config (front matter)
├── scripts/
│   └── fundamentals.py      # Standalone warm-up script: basic OpenAI calls
├── env.example              # Template for your .env file
├── pyproject.toml           # Project dependencies (managed with uv)
└── uv.lock
```

## How it works

1. `context.py` reads `docs/linkedin.pdf` (with `pypdf`) and `docs/summary.txt`, then puts them into a system prompt. That prompt sets the twin's persona, tone, rules and tool usage.
2. `app.py` sends the conversation to the OpenAI Chat Completions API (model `gpt-5.5`) with the tool definitions from `tools.py`.
3. When the model asks for a tool call (`finish_reason == "tool_calls"`), `handle_tool_calls` runs the matching Python function and sends the result back to the model. This repeats until the model returns a final answer.
4. Gradio shows the chat UI. The sidebar lets each visitor paste their own OpenAI API key. Keys are stored per browser session, so visitors never share a key.

| Tool                      | What it does                                                                 |
| ------------------------- | ---------------------------------------------------------------------------- |
| `web_search`              | Gets the top 5 DuckDuckGo results (via `ddgs`) for questions not covered by the docs |
| `record_unknown_question` | Sends you a Pushover notification with a question the twin couldn't answer  |
| `record_user_details`     | Sends you a Pushover notification with a visitor's email, name and notes    |

---

## Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** (recommended), or plain `pip`
- An **OpenAI API key**: <https://platform.openai.com/api-keys>
- *(Optional)* A **Pushover** account (user key + app token), for phone notifications

Install uv if you don't have it:

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url> digital-twin-agent-scratch
cd digital-twin-agent-scratch
```

### 2. Install dependencies

With **uv** (creates `.venv` and installs everything from `uv.lock`):

```bash
uv sync
```

Or with **pip**:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r src/requirements.txt
```

### 3. Configure environment variables

Copy the template to `.env` in the **project root**:

```powershell
# Windows (PowerShell)
Copy-Item env.example .env
```

```bash
# macOS / Linux / Git Bash
cp env.example .env
```

Then edit `.env`:

```dotenv
OPENAI_API_KEY=sk-...your-key...

# Optional: any OpenAI-compatible endpoint (e.g. OpenRouter). Leave unset for OpenAI.
# OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Optional: Pushover notifications for unknown questions and new contacts
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
```

| Variable          | Required | Purpose                                                              |
| ----------------- | -------- | -------------------------------------------------------------------- |
| `OPENAI_API_KEY`  | No*      | Default key for chatting. *If unset, each visitor enters a key in the UI. |
| `OPENAI_BASE_URL` | No       | Use an OpenAI-compatible provider instead of OpenAI                  |
| `PUSHOVER_USER`   | No       | Your Pushover user key                                               |
| `PUSHOVER_TOKEN`  | No       | Your Pushover application API token                                  |

> `.env` is git-ignored. Never commit real keys.

---

## Run the app

From the **project root**:

```bash
uv run src/app.py
```

Or, with an activated virtual environment:

```bash
python src/app.py
```

Then open **<http://127.0.0.1:7860>** in your browser.

In the UI:

1. If `OPENAI_API_KEY` is in `.env`, you can start chatting right away.
2. If not, paste a key in the left panel and click **Connect** (or press Enter). The app checks the key with OpenAI before using it.
3. Tick **Save key to my .env file** to keep the key for next time. Only do this on your own computer.
4. Try one of the example prompts, or ask anything about the person's background.

When the model uses a tool, the terminal prints `Tool called: <tool_name>`.

### Useful run options

Gradio reads these environment variables:

```powershell
# Windows (PowerShell): change the port, or listen on all interfaces
$env:GRADIO_SERVER_PORT = "8080"; uv run src/app.py
$env:GRADIO_SERVER_NAME = "0.0.0.0"; uv run src/app.py
```

```bash
# macOS / Linux
GRADIO_SERVER_PORT=8080 uv run src/app.py
GRADIO_SERVER_NAME=0.0.0.0 uv run src/app.py
```

For auto-reload while editing the UI, use Gradio's dev mode:

```bash
uv run gradio src/app.py
```

Stop the server with **Ctrl + C**.

### Run the fundamentals script

`scripts/fundamentals.py` is a small standalone exercise. It checks your API key, asks for a fun fact, then has one model write a hard IQ question, a second answer it, and a third grade the answer:

```bash
uv run scripts/fundamentals.py
```

---

## Deploy to Hugging Face Spaces

The `src/` folder is set up as a Gradio Space. `src/README.md` holds the Space config and `src/requirements.txt` lists its dependencies.

```bash
cd src
uv run gradio deploy
```

Follow the prompts (log in with a Hugging Face **write** token if asked). Then, in your Space go to **Settings → Variables and secrets** and add these as **secrets**:

- `OPENAI_API_KEY` (optional; without it, visitors bring their own key)
- `PUSHOVER_USER`, `PUSHOVER_TOKEN` (optional)

> Don't upload your `.env` file to the Space. Use Space secrets.

---

## Customize it for yourself

1. **Your data:** replace `src/docs/linkedin.pdf` with your own LinkedIn export (Profile → *More* → *Save to PDF*) and rewrite `src/docs/summary.txt`.
2. **UI text:** edit `HEADER`, `PROFILE` (name, role, tags, links), `EXAMPLES` and the colors in `src/styles.py`.
3. **Model:** change `MODEL_NAME` in `src/app.py`.
4. **Persona and rules:** edit `TWIN_SYSTEM_PROMPT` in `src/context.py`.
5. **New tools:** in `src/tools.py`, write a function and its JSON schema, then add it to `tools` and `tool_map`.

---

## Troubleshooting

| Problem | Fix |
| ------- | --- |
| `FileNotFoundError: .../docs/linkedin.pdf` | Make sure `src/docs/linkedin.pdf` and `src/docs/summary.txt` exist. |
| `ModuleNotFoundError: No module named 'ddgs'` (or `gradio`, `pypdf`) | Run `uv sync` (or `pip install -r src/requirements.txt`). |
| "Invalid key. OpenAI rejected this key." | Check the key at platform.openai.com and that your account has credit. |
| Model not found / access error | Change `MODEL_NAME` in `src/app.py` to a model your key can use. |
| No Pushover notifications | Check `PUSHOVER_USER` / `PUSHOVER_TOKEN` in `.env`. The chat still works without them. |
| Port 7860 already in use | Set `GRADIO_SERVER_PORT` to a different port (see above). |
| Web search returns "Web search failed" | DuckDuckGo may be rate-limiting you. Wait a moment and try again. |
