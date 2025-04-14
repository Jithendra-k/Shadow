from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from app.agent_levels import greet_agent
from app.query_parser import extract_info
from app.rule_engine import apply_rules
import logging
from datetime import datetime
from app.database import init_db, get_session
from app.models import Chat, ChatMessage
import uuid
from sqlmodel import select
from fastapi.responses import JSONResponse
from typing import Optional
from app.rag_searcher import search_rag



app = FastAPI()
# Setup query logger
log_path = "logs/queries.log"
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)
app.add_middleware(SessionMiddleware, secret_key="shadow-secure-key")  # 🔐 Change in prod
init_db()

templates = Jinja2Templates(directory="web/templates")

# Simulated login credentials
AGENTS = {
    "shadow1": {"password": "agent001", "level": 1},
    "phantom3": {"password": "agent003", "level": 3},
    "whisper5": {"password": "agent005", "level": 5},
}

def get_agent_level(session: dict):
    return session.get("agent_level", None)

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = AGENTS.get(username)
    if user and user["password"] == password:
        request.session["agent_username"] = username
        request.session["agent_level"] = user["level"]
        return RedirectResponse("/chat", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


@app.get("/terminal", response_class=HTMLResponse)
def terminal(request: Request):
    if "agent_username" not in request.session:
        return RedirectResponse("/", status_code=302)

    level = request.session["agent_level"]
    return templates.TemplateResponse("index.html", {"request": request, "level": level})


@app.post("/query", response_class=HTMLResponse)
def process_query(request: Request, query: str = Form(...)):
    level = get_agent_level(request.session)
    if not level:
        return RedirectResponse("/", status_code=302)

    greeting = greet_agent(str(level))
    query_data = extract_info(str(level), query)
    response = apply_rules(query_data)

    # Log the query
    username = request.session.get("agent_username", "unknown")
    log_msg = f"[{username} | Level {level}] Query: '{query}' → Response: '{response[:100]}...'"
    logging.info(log_msg)

    # Save to session history
    history = request.session.get("history", [])
    history.append({
        "query": query,
        "response": response,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    request.session["history"] = history  # store back

    return templates.TemplateResponse("result.html", {
        "request": request,
        "greeting": greeting,
        "query": query,
        "response": response,
        "history": history  # pass to template
    })



@app.get("/chat", response_class=HTMLResponse)
def get_chat(request: Request, chat_id: int = None):
    if "agent_username" not in request.session:
        return RedirectResponse("/", status_code=302)

    agent = request.session["agent_username"]
    level = request.session["agent_level"]
    greeting = greet_agent(str(level))

    with get_session() as session:
        chats = session.exec(select(Chat).where(Chat.agent == agent).order_by(Chat.created_at)).all()
        selected_chat = None
        messages = []

        if chat_id:
            selected_chat = session.get(Chat, chat_id)
            if selected_chat and selected_chat.agent == agent:
                messages = session.exec(select(ChatMessage).where(ChatMessage.chat_id == chat_id)).all()

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "greeting": greeting,
        "chats": chats,
        "selected_chat": selected_chat,
        "messages": messages
    })

@app.post("/chat", response_class=HTMLResponse)
def post_chat(request: Request, query: str = Form(...), chat_id: Optional[str] = Form(None)):
    if "agent_username" not in request.session:
        return RedirectResponse("/", status_code=302)

    agent = request.session["agent_username"]
    level = request.session["agent_level"]
    greeting = greet_agent(str(level))

    chat_id = int(chat_id) if chat_id and chat_id.isdigit() else None  # ✅ safely convert

    query_data = extract_info(str(level), query)
    rag_results = search_rag(query, level)
    if rag_results:
        response = rag_results[0]['content']  # take top match
    else:
        response = "No matching intel found in the archive."

    with get_session() as session:
        if chat_id:
            chat = session.get(Chat, chat_id)
            if not chat or chat.agent != agent:
                return RedirectResponse("/chat", status_code=302)
        else:
            chat = Chat(agent=agent, title=query[:40])
            session.add(chat)
            session.commit()
            session.refresh(chat)

        message = ChatMessage(chat_id=chat.id, query=query, response=response)
        session.add(message)
        session.commit()

        chats = session.exec(select(Chat).where(Chat.agent == agent).order_by(Chat.created_at)).all()
        messages = session.exec(select(ChatMessage).where(ChatMessage.chat_id == chat.id)).all()

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "greeting": greeting,
        "chats": chats,
        "selected_chat": chat,
        "messages": messages
    })

@app.get("/new-chat")
def new_chat(request: Request):
    if "agent_username" not in request.session:
        return RedirectResponse("/", status_code=302)

    return RedirectResponse("/chat", status_code=302)



@app.post("/rename-chat", response_class=JSONResponse)
def rename_chat(request: Request, chat_id: int = Form(...), new_title: str = Form(...)):
    with get_session() as session:
        chat = session.get(Chat, chat_id)
        if chat and chat.agent == request.session.get("agent_username"):
            chat.title = new_title
            session.add(chat)
            session.commit()
            return {"status": "renamed"}
    return {"status": "error", "message": "Chat not found"}

@app.post("/delete-chat", response_class=JSONResponse)
def delete_chat(request: Request, chat_id: int = Form(...)):
    with get_session() as session:
        chat = session.get(Chat, chat_id)
        if chat and chat.agent == request.session.get("agent_username"):
            messages = session.exec(select(ChatMessage).where(ChatMessage.chat_id == chat_id)).all()
            for m in messages:
                session.delete(m)
            session.delete(chat)
            session.commit()
            return {"status": "deleted"}
    return {"status": "error"}


@app.get("/search-chats", response_class=JSONResponse)
def search_chats(request: Request, q: str = ""):
    agent = request.session.get("agent_username")
    with get_session() as session:
        results = session.exec(
            select(Chat).where(Chat.agent == agent, Chat.title.ilike(f"%{q}%")).order_by(Chat.created_at)
        ).all()
        return [{"id": c.id, "title": c.title} for c in results]


