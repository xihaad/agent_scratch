"""Styling constants for the digital twin Gradio app."""

import gradio as gr

ACCENT = "#14b8a6"     # teal: buttons, focus rings, title bar
USER = "#4f46e5"       # indigo: user message bubbles
HIGHLIGHT = "#a78bfa"  # violet: assistant stripe, scrollbar hover

THEME = gr.themes.Base(
    primary_hue="teal",
    secondary_hue="indigo",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
)

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

HEADER = """
<div class="twin-header">
  <h1>Digital Twin of Ahmed Rafi Hasan</h1>
  <p>Ask my AI twin about my career, research, skills and experience.</p>
</div>
"""

PROFILE = """
<div class="twin-profile">
  <div class="twin-avatar">AR</div>
  <div class="twin-name">Ahmed Rafi Hasan</div>
  <div class="twin-role">Machine Learning Engineer · Pivotly</div>
  <div class="twin-tags">
    <span>Deep RL</span><span>Multimodal ML</span><span>LLM Agents</span>
  </div>
  <div class="twin-links">
    <a href="https://xihaad.github.io/ahmed_rafi_hasan/" target="_blank">Website</a>
    <a href="https://github.com/xihaad" target="_blank">GitHub</a>
    <a href="https://www.linkedin.com/in/xihaad" target="_blank">LinkedIn</a>
    <a href="https://scholar.google.com/citations?user=rLjCUF4AAAAJ" target="_blank">Scholar</a>
  </div>
</div>
"""

KEY_HELP = """
Get a key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
Your key is only used for your own chat session.
Tick **Save** only when running on your own computer.
"""

CSS = """
:root {
  --twin-accent: #14b8a6;
  --twin-accent-hover: #2dd4bf;
  --twin-user: #4f46e5;
  --twin-highlight: #a78bfa;
  --twin-link: #5eead4;
  --twin-bg: #0b1020;
  --twin-surface: #121933;
  --twin-surface-2: #18213f;
  --twin-border: #243056;
  --twin-border-strong: #34416d;
  --twin-text: #e6e9f5;
  --twin-muted: #8b93b5;
  --twin-radius: 12px;
}

/* Light mode: Gradio adds `.dark` to <body> when dark; absence = light.
   The neutral palette flips; links get darker so they stay readable on white. */
body:not(.dark) {
  --twin-link: #0f766e;
  --twin-bg: #f5f7fb;
  --twin-surface: #ffffff;
  --twin-surface-2: #eef1f8;
  --twin-border: #d9deeb;
  --twin-border-strong: #b5bdd3;
  --twin-text: #141a2e;
  --twin-muted: #5d6582;
}

footer, .built-with, .show-api, .api-docs { display: none !important; }

html, body, gradio-app { background: var(--twin-bg) !important; }

/* ---------- Stable layout ---------- */
.gradio-container {
  background: var(--twin-bg) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  width: 100% !important;
  max-width: 1200px !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 32px 24px 48px !important;
}
.gradio-container .main, .gradio-container .contain, .gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
}
.gradio-container * { min-width: 0; }

/* ---------- Title ---------- */
.gradio-container h1 {
  color: var(--twin-text) !important;
  font-size: 26px !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  border-left: 3px solid var(--twin-accent);
  padding-left: 12px !important;
  margin: 4px 0 8px !important;
  text-align: left !important;
}

/* ---------- Rounded corners on structural pieces ---------- */
.chatbot, .block, .form,
button, input, textarea,
.examples button {
  border-radius: var(--twin-radius) !important;
}

/* ---------- Block surfaces ---------- */
.block, .form { background: transparent !important; box-shadow: none !important; }

/* ---------- Hide the Chatbot label / header strip ---------- */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container {
  display: none !important;
}

/* ---------- Chatbot frame ---------- */
.chatbot, .chatbot.block {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  min-height: 460px !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18) !important;
}
.chatbot .placeholder, .chatbot .placeholder * { color: var(--twin-muted) !important; }

/* ---------- Message rows: strip parent backgrounds ---------- */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap, .bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* ---------- Reset borders on every bubble variant first ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  box-shadow: none !important;
  padding: 10px 14px !important;
  border-radius: 14px !important;
}

/* ---------- Bubble backgrounds (broad to cover Gradio variants) ---------- */
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: var(--twin-user) !important;
  color: #ffffff !important;
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--twin-surface-2) !important;
  color: var(--twin-text) !important;
}

/* ---------- Purple stripe ----------
   Apply to every common bubble class for assistant rows (we don't know which
   one the running Gradio uses), then suppress on any *nested* instance so the
   stripe lands on the outermost matching element only — exactly one stripe. */
.message-row.bot-row .message,
.message-row.bot-row .bubble,
.message-row.bot-row .message-bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .bubble,
.message-row[data-role="assistant"] .message-bubble {
  border-left: 3px solid var(--twin-highlight) !important;
}

.message-row.bot-row .message .message,
.message-row.bot-row .message .bubble,
.message-row.bot-row .message .message-bubble,
.message-row.bot-row .bubble .message,
.message-row.bot-row .bubble .bubble,
.message-row.bot-row .bubble .message-bubble,
.message-row.bot-row .message-bubble .message,
.message-row.bot-row .message-bubble .bubble,
.message-row.bot-row .message-bubble .message-bubble,
.message-row[data-role="assistant"] .message .message,
.message-row[data-role="assistant"] .message .bubble,
.message-row[data-role="assistant"] .message .message-bubble,
.message-row[data-role="assistant"] .bubble .message,
.message-row[data-role="assistant"] .bubble .bubble,
.message-row[data-role="assistant"] .bubble .message-bubble,
.message-row[data-role="assistant"] .message-bubble .message,
.message-row[data-role="assistant"] .message-bubble .bubble,
.message-row[data-role="assistant"] .message-bubble .message-bubble {
  border-left: 0 !important;
}

/* ---------- Uniform font size in bubbles ----------
   The "first paragraph different size" was caused by a leaky `.prose p:first-of-type`
   selector. Force every paragraph in a bubble to the same size. */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  font-size: 14px !important;
  line-height: 1.55 !important;
}
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 14px !important;
  line-height: 1.55 !important;
  margin: 0 0 8px !important;
  color: inherit !important;
}
.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child,
.message-row .prose p:last-child { margin-bottom: 0 !important; }

/* Strip stray internal borders/backgrounds from anything inside a bubble */
.message-row .message *,
.message-row .message-bubble *,
.message-row .bubble * {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: inherit !important;
}
.message-row .message a,
.message-row .message-bubble a {
  color: var(--twin-link) !important;
  text-decoration: underline;
}

/* ---------- Input row alignment ---------- */
.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"] { align-items: stretch !important; }

textarea, input[type="text"] {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 14px !important;
  padding: 12px 14px !important;
  line-height: 1.4 !important;
  min-height: 48px !important;
}
textarea:focus, input[type="text"]:focus {
  border-color: var(--twin-accent) !important;
  outline: none !important;
  box-shadow: 0 0 0 1px var(--twin-accent) !important;
}
textarea::placeholder, input::placeholder { color: var(--twin-muted) !important; }

/* ---------- Buttons ---------- */
button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  letter-spacing: 0.01em !important;
  text-transform: none !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  border: 1px solid var(--twin-border) !important;
  background: transparent !important;
  color: var(--twin-text) !important;
  padding: 0 16px !important;
  min-height: 48px !important;
  align-self: stretch !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer;
  transition: background 0.12s ease, color 0.12s ease, border-color 0.12s ease;
}
button:hover { border-color: var(--twin-accent) !important; color: var(--twin-accent) !important; }

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary {
  background: var(--twin-accent) !important;
  border: 1px solid var(--twin-accent) !important;
  color: #111111 !important;
  min-height: 48px !important;
  align-self: stretch !important;
  padding: 0 14px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover {
  background: var(--twin-accent-hover) !important;
  border-color: var(--twin-accent-hover) !important;
  color: #111111 !important;
}

/* ---------- Submit-button icon: center vertically and size correctly ---------- */
button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg {
  width: 18px !important;
  height: 18px !important;
  margin: 0 auto !important;
  display: block !important;
  align-self: center !important;
  color: #111111 !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* ---------- Examples ---------- */
.examples, .examples-holder, [data-testid="examples"] {
  background: transparent !important;
  padding: 0 !important;
  margin-top: 14px !important;
}
.examples table, .examples-table { background: transparent !important; border: 0 !important; }
.examples button, .example, .examples td button, [data-testid="examples"] button {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  color: var(--twin-text) !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  padding: 10px 14px !important;
  text-align: left !important;
  min-height: 0 !important;
  align-self: auto !important;
  display: inline-block !important;
}
.examples button:hover, .example:hover, [data-testid="examples"] button:hover {
  border-color: var(--twin-user) !important;
  color: var(--twin-user) !important;
  background: var(--twin-surface) !important;
}

/* ---------- Icon buttons (clear, retry, copy) ---------- */
.icon-button, .chatbot .icon-button {
  color: var(--twin-muted) !important;
  background: transparent !important;
  border: 0 !important;
  min-height: 0 !important;
  align-self: auto !important;
  padding: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.icon-button:hover, .chatbot .icon-button:hover { color: var(--twin-accent) !important; }

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--twin-bg); }
::-webkit-scrollbar-thumb { background: var(--twin-border-strong); }
::-webkit-scrollbar-thumb:hover { background: var(--twin-highlight); }

/* ---------- Selection ---------- */
::selection { background: var(--twin-accent); color: #111111; }

/* ---------- Header ---------- */
.twin-header { margin-bottom: 18px; }
.twin-header p { color: var(--twin-muted); font-size: 14px; margin: 0 0 0 15px; }

/* ---------- Left sidebar card ---------- */
.twin-sidebar {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: var(--twin-radius) !important;
  padding: 20px !important;
  gap: 14px !important;
  position: sticky;
  top: 24px;
  align-self: flex-start;
}
.twin-sidebar [data-testid="block-info"],
.twin-sidebar label > span {
  color: var(--twin-muted) !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
input[type="checkbox"] { border-radius: 4px !important; accent-color: var(--twin-accent); }

/* Profile */
.twin-profile { text-align: center; padding-bottom: 16px; border-bottom: 1px solid var(--twin-border); }
.twin-avatar {
  width: 64px; height: 64px; margin: 0 auto 10px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, var(--twin-accent), var(--twin-user));
  color: #ffffff; font-weight: 700; font-size: 20px;
}
.twin-name { color: var(--twin-text); font-size: 17px; font-weight: 700; }
.twin-role { color: var(--twin-muted); font-size: 13px; margin-top: 2px; }
.twin-tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px; margin-top: 12px; }
.twin-tags span {
  font-size: 11px; padding: 3px 9px; border-radius: 999px;
  border: 1px solid var(--twin-border-strong); color: var(--twin-text);
}
.twin-links { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 12px; }
.twin-links a { color: var(--twin-link) !important; font-size: 13px; text-decoration: none; }
.twin-links a:hover { text-decoration: underline; }

/* Status and help text */
.twin-status, .twin-status * { font-size: 13px !important; color: var(--twin-text) !important; }
.twin-note, .twin-note * { font-size: 12px !important; color: var(--twin-muted) !important; line-height: 1.5 !important; }
.twin-note a { color: var(--twin-link) !important; }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .gradio-container { padding: 22px 14px 36px !important; }
  .gradio-container h1 { font-size: 22px !important; }
  .twin-sidebar { position: static; }
}
"""

JS = """
() => {
  document.title = 'Digital Twin';

  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  // Re-focus the message field whenever Gradio re-enables it
  // (i.e. after the assistant finishes responding).
  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""
