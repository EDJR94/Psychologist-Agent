import os
import requests
from datetime import datetime
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

# Initialize Deepgram client
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
deepgram = DeepgramClient(api_key=DEEPGRAM_API_KEY)

TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}"

def print_agent_output(output):
    for message in output['messages']:
        message.pretty_print()

def send_telegram_message(text, chat_id):
    #CHAT_ID = os.getenv("CHAT_ID")
    print(f"Sending message... with token: {TOKEN}")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}&amp;parse_mode=MarkdownV2"
    response = requests.get(url).json()
    print(f"Response: {response}")
    if not response["ok"]:
        return "Error sending message"
    
def download_telegram_audio(file_id):
    """Download audio file from Telegram using file_id."""
    file_info_url = f"{TELEGRAM_URL}/getFile?file_id={file_id}"
    file_info = requests.get(file_info_url).json()

    if file_info.get("ok"):
        file_path = file_info["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

        # Download the file
        audio_response = requests.get(file_url)
        audio_file_path = f"/tmp/{file_path.split('/')[-1]}"  # Save in temp directory

        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(audio_response.content)

        return audio_file_path
    else:
        raise Exception("Failed to get file info from Telegram.")

async def transcribe_audio_with_deepgram(file_path):
    """Send audio file to Deepgram for transcription."""
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient()

        with open(file_path, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            language="pt-BR"
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

        transcription_text = response["results"]["channels"][0]["alternatives"][0]["transcript"]

        # STEP 4: Print the response
        #print(response.to_json(indent=4))

        return transcription_text

    except Exception as e:
        print(f"Exception: {e}")
    
#def telegram_message_receiver(after_timestamp):
#    TOKEN = os.getenv("TELEGRAM_TOKEN")
#    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
#    response = requests.get(url).json()
#    if not response["result"]:
#        return []
#    
#    new_messages = []
#    for update in response['result']:
#        if "message" in update:
#            message = update["message"]
#            if message["date"] > after_timestamp: # only get new messages
#                new_messages.append({
#                    "user_id": message["from"]["id"], # save the user for persistence
#                    "text": message["text"],
#                    "date": datetime.fromtimestamp(message["date"]).strftime("%Y-%m-%d %H:%M")
#                })
#    return new_messages