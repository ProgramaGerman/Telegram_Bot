import json
import os
from difflib import SequenceMatcher
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

DB_FILE = "aprendizaje.json"
TOKEN_FILE = "token.txt"
SIMILARITY_THRESHOLD = 0.7  # Umbral de similitud para considerar una pregunta parecida

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        conocimiento = json.load(f)
else:
    conocimiento = {}

esperando_respuesta = {}

def encontrar_pregunta_parecida(texto):
    """Busca la pregunta aprendida más parecida al texto dado."""
    mejor_pregunta = None
    mejor_similitud = 0.0
    for pregunta in conocimiento:
        similitud = SequenceMatcher(None, texto.lower(), pregunta.lower()).ratio()
        if similitud > mejor_similitud:
            mejor_similitud = similitud
            mejor_pregunta = pregunta
    if mejor_similitud >= SIMILARITY_THRESHOLD:
        return mejor_pregunta
    return None

async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy un bot que aprende de ti y reconoce patrones similares. Hazme una pregunta y si no sé la respuesta, ¡enséñamela!")

async def responder(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    texto = update.message.text.strip()

    if esperando_respuesta.get(user_id):
        pregunta = esperando_respuesta[user_id]
        conocimiento[pregunta] = texto
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(conocimiento, f, ensure_ascii=False, indent=2)
        await update.message.reply_text(f"¡Gracias! He aprendido la respuesta para: '{pregunta}'")
        esperando_respuesta.pop(user_id)
        return

    pregunta_parecida = encontrar_pregunta_parecida(texto)
    if pregunta_parecida:
        await update.message.reply_text(conocimiento[pregunta_parecida])
    else:
        await update.message.reply_text("No sé la respuesta a eso. ¿Puedes enseñarme cuál sería la respuesta correcta?")
        esperando_respuesta[user_id] = texto

def obtener_token():
    """Lee el token del archivo token.txt"""
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(f"No se encontró el archivo {TOKEN_FILE}")
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

if __name__ == '__main__':
    token = obtener_token()
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    application.run_polling()
