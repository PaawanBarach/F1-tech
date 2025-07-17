from fastapi import FastAPI, UploadFile, File
import gradio as gr
import threading, time
import os

from agents_enhanced import answer_question
from ingestion import run_full_ingest
from articles import generate_technical_article
from vectorstore import STORE, upsert_texts

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "alive"}

@app.get("/")
def root():
    return {"message": "F1 Technical Analyst API", "status": "running"}

def chat_fn(user, history):
    thinking, answer, sources, imgs = answer_question(user)
    # hide thinking until clicked
    display = f"<details><summary>🤔 Show reasoning</summary>\n\n{thinking}\n\n</details>\n\n" \
              + answer + "\n\n**Sources:**\n" \
              + "\n".join(f"- {s}" for s in sources)
    history.append((user, display))
    return history, imgs

def ingest_upload(file: UploadFile):
    content = file.file.read().decode(errors="ignore")
    upsert_texts([f"Uploaded: {file.filename}\n\n{content}"])
    return f"✅ Ingested `{file.filename}`"

def launch_ui():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🏎️ F1 Technical Analyst")

        with gr.Tabs():
            # Chat
            with gr.Tab("🤖 Chat"):
                chat = gr.Chatbot()
                msg  = gr.Textbox(placeholder="Ask about F1 tech…")
                imgs = gr.Gallery(label="Charts", columns=2)
                msg.submit(chat_fn, [msg, chat], [chat, imgs])
                msg.submit(lambda: "", None, msg)

            # Ingestion
            with gr.Tab("📥 Ingest Data"):
                gr.Markdown("**Manual ingestion** or **upload PDF/text** to KB")
                ing_btn = gr.Button("Run Full Ingest")
                status = gr.Textbox(interactive=False)
                upload = gr.File(label="Upload PDF or TXT", file_types=[".pdf",".txt"])
                ing_btn.click(lambda: f"🔄 Added {run_full_ingest()} items", None, status)
                upload.upload(ingest_upload, upload, status)

            # Articles
            with gr.Tab("📝 Articles"):
                art_list = gr.Dropdown(choices=os.listdir("articles") if os.path.isdir("articles") else [], label="Saved Articles")
                art_view = gr.Markdown()
                btn = gr.Button("Generate New Article")
                btn.click(lambda: generate_technical_article()[1], None, art_view)
                art_list.change(lambda fn: open(f"articles/{fn}","r",encoding="utf-8").read(), art_list, art_view)

        demo.launch(server_name="0.0.0.0", server_port=7860, prevent_thread_lock=True)

if __name__ == "__main__":
    threading.Thread(target=launch_ui, daemon=True).start()
    time.sleep(2)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
