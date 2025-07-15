# Telegram Bot de Aprendizaje Supervisado

Este proyecto es un bot de Telegram que aprende de las respuestas que le enseñan los usuarios. Utiliza un sistema de aprendizaje supervisado simple y es capaz de reconocer preguntas similares para responder de manera flexible.

## Características
- Aprende nuevas respuestas a partir de la interacción con los usuarios.
- Reconoce patrones similares en las preguntas usando similitud de texto.
- Guarda el conocimiento adquirido en un archivo JSON para que el aprendizaje sea persistente.
- El token del bot se almacena de forma segura en un archivo externo (`token.txt`).

## ¿Cómo funciona?
1. Cuando el bot recibe una pregunta, busca en su base de datos si ya conoce una respuesta para una pregunta similar.
2. Si encuentra una pregunta parecida, responde con la respuesta aprendida.
3. Si no la conoce, pide al usuario que le enseñe la respuesta correcta.
4. El usuario responde y el bot almacena la nueva pareja pregunta-respuesta para futuras ocasiones.

## Archivos principales
- `telegram_bot.py`: Código principal del bot.
- `aprendizaje.json`: Base de datos donde se guardan las preguntas y respuestas aprendidas.
- `token.txt`: Archivo donde se debe colocar el token del bot de Telegram (una sola línea).

## Instalación y uso
1. Instala las dependencias necesarias:
   ```bash
   pip install python-telegram-bot
   ```
2. Coloca tu token de bot de Telegram en un archivo llamado `token.txt` en la misma carpeta del proyecto.
3. Ejecuta el bot:
   ```bash
   python telegram_bot.py
   ```

## Ejemplo de interacción
```
Usuario: hola
Bot: No sé la respuesta a eso. ¿Puedes enseñarme cuál sería la respuesta correcta?
Usuario: ¡Hola! ¿Cómo estás?
Bot: ¡Gracias! He aprendido la respuesta para: 'hola'
Usuario: hola
Bot: ¡Hola! ¿Cómo estás?
```

## Notas
- El bot reconoce preguntas similares, no solo iguales, gracias a un sistema de similitud de texto.
- El aprendizaje es persistente: lo que aprende se guarda en `aprendizaje.json`.

---

Desarrollado como ejemplo de bot de aprendizaje supervisado en Python.
