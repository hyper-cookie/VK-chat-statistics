from VKStats.VKBot import *


class Collector:
    def __init__(self):
        self.create_vk_connector_object()
        self.create_vk_chat_object()
        self.create_vk_bot_object()

    def create_vk_connector_object(self):
        self.vk_connector_object = VKConnector()
        self.longpoll = self.vk_connector_object.get_longpoll()
        self.session = self.vk_connector_object.get_session()

    def create_vk_chat_object(self):
        self.vk_chat_object = VKChatConnector(self.longpoll)
        self.chat_id = self.vk_chat_object.get_chat_id()
        self.scan_id = self.vk_chat_object.get_scan_id()
        self.borders = self.vk_chat_object.get_borders()

    def create_vk_bot_object(self):
        self.vk_bot_object = VKBot(self.session, self.longpoll, self.chat_id, self.scan_id, self.borders)


Test_launch = Collector()
