import matplotlib.pyplot as plt
import numpy as np
from VKStats.DataBase import *


class DataAnalyst:
    def __init__(self):
        self.db_object = DataBase()

        self.words_quantity = {}
        self.users_quantity = {}
        self.messages_quantity = {}

        self.top25_words = {}
        self.top25_users = {}

    def find_words_quantity(self):
        for line in self.db_object.cursor.execute("SELECT message FROM messages"):
            for word in line[0].split():
                if word not in self.words_quantity:
                    self.words_quantity[word] = 1
                else:
                    self.words_quantity[word] += 1

        self.words_quantity = {k: v for k, v in sorted(self.words_quantity.items(), key=lambda item: item[1], reverse=True)}

        dict_item = 1
        for item in self.words_quantity.items():
            if dict_item <= 25:
                self.top25_words[item[0]] = item[1]
                dict_item += 1

    def find_users_quantity(self):
        for line in self.db_object.cursor.execute("SELECT user FROM messages"):
            if line[0] not in self.users_quantity:
                self.users_quantity[line[0]] = 1
            else:
                self.users_quantity[line[0]] += 1
        self.users_quantity = {k: v for k, v in sorted(self.users_quantity.items(), key=lambda item: item[1], reverse=True)}

        dict_item = 1
        for item in self.users_quantity.items():
            if dict_item <= 25:
                self.top25_users[item[0]] = item[1]
                dict_item += 1

    def find_messages_per_day(self):
        for line in self.db_object.cursor.execute("SELECT message, date FROM messages"):
            if line[1][0:-6] not in self.messages_quantity:
                self.messages_quantity[line[1][0:-6]] = 1
            else:
                self.messages_quantity[line[1][0:-6]] += 1

    def build_graph_top_words(self):
        plt.bar(self.top25_words.keys(), self.top25_words.values())
        plt.xticks(rotation=90)
        plt.grid(which="major", color="black")
        plt.minorticks_on()
        plt.grid(which="minor", color="gray", linestyle=":")

        plt.savefig("Graphs\\top_words.png", bbox_inches="tight", dpi=450)
        plt.close()

    def build_graph_top_users(self):
        plt.bar(self.top25_users.keys(), self.top25_users.values())
        plt.xticks(rotation=90)
        plt.grid(which="major", color="black")
        plt.minorticks_on()
        plt.grid(which="minor", color="gray", linestyle=":")

        plt.savefig("Graphs\\top_users.png", bbox_inches="tight", dpi=450)
        plt.close()

    def build_graph_messages_per_day(self):
        plt.plot(self.messages_quantity.keys(), self.messages_quantity.values(), "r--")
        plt.fill_between(list(self.messages_quantity.keys()), list(self.messages_quantity.values()),
                         np.zeros_like(list(self.messages_quantity.values())), color="pink")
        plt.xticks(rotation=90)
        plt.grid(which="major", color="black")
        plt.minorticks_on()
        plt.grid(which="minor", color="gray", linestyle=":")

        plt.savefig("Graphs\\messages_per_day.png", bbox_inches="tight", dpi=450)
        plt.close()
