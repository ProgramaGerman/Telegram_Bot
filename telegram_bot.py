import json
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Archivo donde se guardan las preguntas y respuestas aprendidas
DB_FILE = "aprendizaje.json"

# Cargar base de datos o crear una nueva
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        conocimiento = json.load(f)
else:
    conocimiento = {}

# Diccionario para saber si el bot espera una respuesta de aprendizaje
esperando_respuesta = {}

async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy un bot que aprende de ti. Hazme una pregunta y si no sé la respuesta, ¡enséñamela!")

async def responder(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    texto = update.message.text.strip()

    # Si el bot espera una respuesta de aprendizaje
    if esperando_respuesta.get(user_id):
        pregunta = esperando_respuesta[user_id]
        conocimiento[pregunta] = texto
        # Guardar en archivo
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(conocimiento, f, ensure_ascii=False, indent=2)
        await update.message.reply_text("¡Gracias! He aprendido la respuesta para: '" + pregunta + "'")
        esperando_respuesta.pop(user_id)
        return

    # Si ya conoce la respuesta
    if texto in conocimiento:
        await update.message.reply_text(conocimiento[texto])
    else:
        await update.message.reply_text("No sé la respuesta a eso. ¿Puedes enseñarme cuál sería la respuesta correcta?")
        esperando_respuesta[user_id] = texto

if __name__ == '__main__':
    application = ApplicationBuilder().token('8000399373:AAF6qzXmBsscoEcj5g8F943HemOM2bxpgMA').build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    application.run_polling()
