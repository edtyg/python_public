import os
from typing import Final
from telethon import TelegramClient, events

api_id: Final = "27367864"
api_hash: Final = "cf33b4b9f3746649fb1e8079d1fab16f"

# phone = 'your_telegram_number' # replace with your telegram number

client = TelegramClient("Lyou", api_id, api_hash)

full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"

# Load keywords from file
with open(save_path + "keywords.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

part_a_keywords = [word.strip() for word in lines[0].split(":")[1].split(",")]
part_b_keywords = [word.strip() for word in lines[1].split(":")[1].split(",")]


@client.on(
    events.NewMessage(chats=("wublock", "unfolded", "theblockbeats", "foresightnews"))
)
# @client.on(events.NewMessage(chats=('miyanohash_bot')))
async def my_event_handler(event):
    print("New message: ", event.message.text)

    # Convert the message to lowercase
    message_text = event.message.text or ""
    message_words = message_text.lower().split()
    print(message_words)

    # Only forward the message if it contains at least one keyword from both Part A and Part B
    if any(keyword in message_words for keyword in part_a_keywords) and any(
        keyword in message_words for keyword in part_b_keywords
    ):
        # Forward the message to another chat
        await client.forward_messages(-990460215, event.message)


with client:
    client.run_until_disconnected()
