import os
from dotenv import load_dotenv
# Load .env variables
load_dotenv()


from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from src.agents.psycologist import Psycologist
from dotenv import load_dotenv
from src.utils import send_telegram_message, download_telegram_audio, transcribe_audio_with_deepgram
import os
import requests
from fastapi import FastAPI, Request
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

app = FastAPI()

# Models
#model = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
#model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
#model = ChatOpenAI(
#    model="deepseek-chat", 
#    api_key=DEEPSEEK_API_KEY, 
#    base_url="https://api.deepseek.com",
#    temperature=0.7
#)

model = ChatOpenAI(model='gpt-4o-mini', temperature=0.1)

telegram_assistant = Psycologist(model)


@app.post("/")
async def telegram_message_receiver(request: Request):
    #TOKEN = os.getenv("TELEGRAM_TOKEN")
    #url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        response = await request.json()
        print(f"Data received: {response}")

        if "message" in response:
            message = response["message"]
            user_id = message["from"]["id"]
            
            timestamp = message["date"]
            chat_id = message['chat']['id']

            if "text" in message:
                text = message.get("text", "")

                print(f"Message received: {text} from {user_id} at {timestamp}")

            elif "voice" in message:
                voice = message["voice"]
                file_id = voice["file_id"]

                print("Downlading audio...")
                audio_path = download_telegram_audio(file_id)

                print("Transcribing audio...")
                text = await transcribe_audio_with_deepgram(audio_path)

                print(f"Message transcribed: {text} from {user_id} at {timestamp}")

            sent_message = (f"Message: {text}\n"
                            f"Current Date/time: {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')}")
            user_config = {"configurable": {"thread_id": user_id}}
            answer = telegram_assistant.invoke(sent_message, user_config)
            send_telegram_message(answer, chat_id)
        
        return {"status": "success"}
    except Exception as e:
        print("Erro ao processar mensagem:", e)
        return {"status": "error", "message": str(e)}

        

#if __name__ == "__main__":
#    print("Telegram Assistant Manager is running")
#    #config = {"configurable": {"thread_id": 200}}
#    initial_timestamp = int(time.time())
#    monitor_bot(initial_timestamp)