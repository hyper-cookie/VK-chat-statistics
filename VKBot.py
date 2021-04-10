import re
import datetime
import vk_api
import os
from vk_api import VkApi as VkBotConnect
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from sys import exit as sys_exit
from VKStats.VKConfig import *
from VKStats.DataBase import *
from VKStats.DataAnalyst import *


class VKConnector:
    def __init__(self):
        self._create_connection()

    def _create_connection(self):
        try:
            self.VK_session = VkBotConnect(token=GROUP_TOKEN)
            self.longpoll = VkBotLongPoll(self.VK_session, GROUP_ID)
        except vk_api.exceptions.ApiError:
            print("- VK connection ERROR. Wrong token or group ID -")
            sys_exit()

    def get_session(self):
        return self.VK_session

    def get_longpoll(self):
        return self.longpoll


class BorderDefiner:
    def __init__(self):
        self.time_reg_exp = re.compile("(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])")
        self.date_reg_exp = re.compile(r"\d{4}[-/]\d{2}[-/]\d{2}")

        self.first_border_text = ''
        self.second_border_text = ''
        self.borders = []

    def define_borders(self, user_message):
        is_from = user_message.find('from')
        is_to = user_message.find('to')

        if is_from != -1 and is_to != -1:
            self.first_border_text = user_message[is_from:is_to - 1]
            self.second_border_text = user_message[user_message.find('to'):]
        elif is_from != -1 and is_to == -1:
            self.first_border_text = user_message[is_from:]
        elif is_from == -1 and is_to != -1:
            self.second_border_text = user_message[user_message.find('to'):]

        for border in [self.first_border_text, self.second_border_text]:
            self.borders.append(self.date_reg_exp.findall(border))
            self.borders.append(self.time_reg_exp.findall(border))

        for border_num in range(len(self.borders)):
            if len(self.borders[border_num]) == 0 and border_num == 1:
                self.borders[border_num] = ["00:00"]
            if len(self.borders[border_num]) == 0 and border_num == 3:
                self.borders[border_num] = ["23:59"]

    def get_borders(self):
        return self.borders


class VKChatConnector:
    def __init__(self, longpoll):
        self.border_object = BorderDefiner()

        self.VK_connection = longpoll
        self.actual_chat_ID = None
        self.scan_ID = None
        self.borders = None

        self.find_chat()

    def find_chat(self):
        for event in self.VK_connection.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object.message["text"][0:14].lower() == "start analysis":
                self.actual_chat_ID = event.chat_id
                self.scan_ID = event.object.message["conversation_message_id"]
                self.border_object.define_borders(event.object.message["text"])
                self.borders = self.border_object.get_borders()
                break

    def get_chat_id(self):
        return self.actual_chat_ID

    def get_scan_id(self):
        return self.scan_ID

    def get_borders(self):
        return self.borders


class VKBot:
    def __init__(self, session, longpoll, chat_id, scan_id, borders):
        if os.path.exists("VKMessages.db"): # if last DB file exists (from another launch) - then delete it
            os.remove("VKMessages.db")

        self.db_object = DataBase()
        self.analyst_object = DataAnalyst()

        self.VK_session = session
        self.VK_longpoll = longpoll

        self.actual_chat_id = chat_id
        self.actual_message_id = 1
        self.actual_message_value = None
        self.actual_message_date = None
        self.scan_ID = scan_id
        self.find_borders = borders

        self.start_date = None
        self.end_date = None

        self.find_borders_dates()
        self.get_all_messages()
        self.launch_data_analysis()
        self.send_graphs_in_chat()

    def get_message_by_id(self, message_number):
        self.actual_message_value = self.VK_session.method("messages.getByConversationMessageId",
                                                           {"peer_id": 2000000000 + self.actual_chat_id,
                                                            "conversation_message_ids": message_number,
                                                            "extended": 1})

    def find_borders_dates(self):
        while self.actual_message_id <= self.scan_ID:
            self.get_message_by_id(self.actual_message_id)
            if len(self.actual_message_value["items"]) != 0:
                self.start_date = self.actual_message_value["items"][0]["date"]
                break
            self.actual_message_id += 1

        self.get_message_by_id(self.scan_ID)
        self.end_date = self.actual_message_value["items"][0]["date"]

        if len(self.find_borders[0]) == 0:
            timestamp = datetime.datetime.fromtimestamp(self.start_date)
            self.find_borders[0] = [timestamp.strftime("%Y/%m/%d")]
        if len(self.find_borders[2]) == 0:
            timestamp = datetime.datetime.fromtimestamp(self.end_date)
            self.find_borders[2] = [timestamp.strftime("%Y/%m/%d")]

        self.actual_message_id = 1

    def get_all_messages(self):
        while self.actual_message_id <= self.scan_ID:
            self.get_message_by_id(self.actual_message_id)

            # if message is not system-message
            if len(self.actual_message_value["items"]) != 0:
                self.actual_message_date = self.actual_message_value["items"][0]["date"]
                timestamp = datetime.datetime.fromtimestamp(self.actual_message_date)
                self.actual_message_date = timestamp.strftime("%Y/%m/%d %H:%M")

                # if len of message's text isn't 0 and message is sent by user and the date of message in the user range
                if "profiles" in self.actual_message_value:
                    if len(self.actual_message_value["items"][0]["text"]) != 0:
                        if self.actual_message_date >= self.find_borders[0][0] + " " + self.find_borders[1][0] \
                                and self.actual_message_date <= self.find_borders[2][0] + " " + self.find_borders[3][0]:
                            self.db_object.insert_data(self.actual_message_value["items"][0]["text"],
                                                       self.actual_message_value["profiles"][0]["first_name"] + " " +
                                                       self.actual_message_value["profiles"][0]["last_name"],
                                                       self.actual_message_date)

                        if self.actual_message_date > self.find_borders[2][0] + " " + self.find_borders[3][0]:
                            break

            self.actual_message_id += 1

    def launch_data_analysis(self):
        self.analyst_object.find_words_quantity()
        self.analyst_object.find_users_quantity()
        self.analyst_object.find_messages_per_day()

        self.analyst_object.build_graph_top_words()
        self.analyst_object.build_graph_top_users()
        self.analyst_object.build_graph_messages_per_day()

    def send_graphs_in_chat(self):
        photo_names = ["Graphs\\top_words.png", "Graphs\\top_users.png", "Graphs\\messages_per_day.png"]

        for photo_name in photo_names:
            upload = vk_api.VkUpload(self.VK_session)
            photo = upload.photo_messages(photo_name)
            owner_id = photo[0]["owner_id"]
            photo_id = photo[0]["id"]
            access_key = photo[0]["access_key"]
            attachment = f"photo{owner_id}_{photo_id}_{access_key}"
            self.VK_session.method("messages.send",
                                   {"peer_id": 2000000000 + self.actual_chat_id,
                                    "attachment": attachment,
                                    "random_id": 0})
