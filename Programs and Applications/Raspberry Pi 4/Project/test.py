import json
from datetime import datetime


with open('message_1.json', encoding="utf8") as json_file:
    data = json.load(json_file)

messages = data['messages']

with open("message_1.csv", "w", encoding="utf8") as file:
    for m in messages:
        sender = m.get("sender_name")
        timestamp_ms = m.get("timestamp_ms")
        content = m.get("content")
        try:
            string1 = "Sender: " + str(sender.encode('ascii', 'ignore'))
            string2 = "Time: " + datetime.fromtimestamp(timestamp_ms/1000).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            string3 = "Content: " + str(content.encode('ascii', 'ignore'))
            file.write(string1 + "\n" + string2 + "\n" +string3 + "\n\n\n")
        except:
            pass
