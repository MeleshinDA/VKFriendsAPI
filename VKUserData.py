import requests
import sys

request_pattern = "https://api.vk.com/method/{0}?{1}&access_token={2}&v=5.131"


class VKUserData:
    def __init__(self, user, token):
        self.user = user
        self.token = token
        self.friends = self.__get_all_friends()

    def __get_friends_from_req(self):
        request = requests.get(request_pattern.format("friends.get", f"user_id={self.user}&order=random", self.token))
        return requests.get(
            request_pattern.format("users.get", f"user_ids={(request.json()['response'])['items']}&fields=city",
                                   self.token))

    def __get_all_friends(self):
        try:
            friends = []
            for friend_info in self.__get_friends_from_req().json()['response']:
                city = friend_info.get("city").get("title") if friend_info.get("city") else "неуказанного города"
                friends.append(friend_info['first_name'] + " " + friend_info['last_name'] + ". Из " + city)

            friends.sort()
            return friends

        except KeyError:
            sys.exit("Error parameters.")

        except requests.exceptions.ConnectionError:
            sys.exit("Connection to Internet error.")

    def print_user_info(self):
        user_data = requests.get(
            request_pattern.format("users.get", f"user_ids={self.user}&fields=city,bdate,counters", self.token)).json()[
            'response'][0]

        general_info = f"Информация о пользователе {self.user}:\n"
        general_info += "Имя: " + str(user_data["first_name"]) + "\n"
        general_info += "Фамилия: " + str(user_data["last_name"]) + "\n"
        general_info += "Дата рождения: " + user_data["bdate"] + "\n"
        general_info += "Город: "
        general_info += user_data["city"]["title"] + "\n" if user_data.get("city") else "не указан \n"
        general_info += "Количество аудио: " + str(user_data["counters"]["audios"]) + "\n"
        general_info += "Количество видео: " + str(user_data["counters"]["videos"]) + "\n"
        general_info += "Количество фотографий : " + str(user_data["counters"]["photos"]) + "\n"
        general_info += "Количество подарков : " + str(user_data["counters"]["gifts"]) + "\n"

        print(general_info)
        print("Друзья: ")
        for friend in self.friends:
            print(friend)


