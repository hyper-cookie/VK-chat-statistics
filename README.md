# VK-chat-statistics
The project collects statistics of messages in russian social network "VK" (VKontakte) chats.
If you want to know the top of words which were used in your chats, the top of users who were chatting more or the activity per day, then you can use this program!

---
Which modules to start:
- vk_api - pip install vk-api
- matplotlib - pip install matplotlib
- numpy - pip install numpy
- sqlite3 (already installed with your python)

---
What you need to start:
- Create a group in VK, make the settings of the group to bot-group, set the highest longpoll version and give all permission to the bot.
- Create a token of the group.
- Open the "VKConfig.py" file, fill variables "GROUP_TOKEN" and "GROUP_ID" with your group-token and ID of your bot-group.
- Then add the group-bot to your CHAT (not dialogue, chat!) and give access to all messages.
- Launch "Collector.py" file and you are ready to start!

---
There are many ways to launch the analysis:
- If you want to analysis ALL history of your messages, then just write "Start Analysis" (you should write directions in the chat where your bot has been added), like here:
![image](https://user-images.githubusercontent.com/62260405/114281015-aa447980-9a44-11eb-8fc6-2765d45dfa30.png)
- If you want to set date-borders of analysis, then you must write firstly "Start Analysis" and then add "from *year/month/day hours:minuts* to *year/month/day hours:minuts*", like here:
![image](https://user-images.githubusercontent.com/62260405/114281058-e1b32600-9a44-11eb-9090-3a22a88b78b1.png)
- If you want to set date-borders FROM start of the chat or TO end of the chat, then add "from *year/month/day hours:minuts*" or "to *year/month/day hours:minuts*" to your firstly "Start Analysis", like here:
![image](https://user-images.githubusercontent.com/62260405/114281100-17f0a580-9a45-11eb-8904-3859a24410be.png)
- It is not necessary to set the time for date-border, so you can write only date, like here:
![image](https://user-images.githubusercontent.com/62260405/114281400-d8c35400-9a46-11eb-8469-f622fc1b12e7.png)

Remember, words "Start Analysis" must be written firstly!

---
Results:
![7FKHnSWhaIU](https://user-images.githubusercontent.com/62260405/114281291-3dca7a00-9a46-11eb-9221-43793ede88e1.jpg)
![AzSZW3Cz4l8](https://user-images.githubusercontent.com/62260405/114281314-4e7af000-9a46-11eb-8a63-81814773cc94.jpg)
![pkvR-cON_TI](https://user-images.githubusercontent.com/62260405/114281317-5044b380-9a46-11eb-9a80-4ac20ac82e45.jpg)

---
I would be very thanksfull if you can help to improve my code or give me some advices. Pleasant use for you!
