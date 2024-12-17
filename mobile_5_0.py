import hashlib
from time import sleep


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = age

    @staticmethod
    def _hash_password(password):
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)


class Video:
    def __init__(self, title, duration, time_now=0, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        password_hash = User._hash_password(password)
        for user in self.users:
            if user.nickname == nickname and user.password == password_hash:
                self.current_user = user
                print(f"Пользователь {nickname} успешно вошел.")
                break
        else:
            print("Неверный логин или пароль.")

    def register(self, nickname, password, age):
        new_user = User(nickname, password, age)
        if any(user.nickname == nickname for user in self.users):
            print(f"Пользователь {nickname} уже существует.")
        else:
            self.users.append(new_user)
            self.log_in(nickname, password)
            print(f"Пользователь {nickname} зарегистрирован и выполнен вход.")

    def log_out(self):
        if self.current_user is not None:
            self.current_user = None
            print("Вы вышли из аккаунта.")
        else:
            print("Нет активного пользователя.")

    def add(self, *new_videos):
        for video in new_videos:
            if any(existing_video.title == video.title for existing_video in self.videos):
                continue
            self.videos.append(video)

    def get_videos(self, search_word):
        search_word = search_word.lower()
        matching_titles = [
            video.title for video in self.videos
            if search_word in video.title.lower()
        ]
        return matching_titles

    def watch_video(self, title):
        if self.current_user is None:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return

                # Воспроизведение видео
                for second in range(video.time_now, video.duration + 1):
                    print(f"Воспроизведение: {second} секунда")
                    sleep(1)

                video.time_now = 0
                print("Конец видео")
                return

        print("Видео не найдено.")




if __name__ == "__main__":
    ur = UrTube()

    v1 = Video('Лучший язык программирования 2024 года', 200)
    v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

    # Добавление видео
    ur.add(v1, v2)

    # Проверка поиска
    print(ur.get_videos('лучший'))  # ['Лучший язык программирования 2024 года']
    print(ur.get_videos('ПРОГ'))  # ['Лучший язык программирования 2024 года']

    # Проверка на вход пользователя и возрастное ограничение
    ur.watch_video('Для чего девушкам парень программист?')  # Войдите в аккаунт, чтобы смотреть видео

    ur.register('vasya_pupkin', 'lolkekcheburek', 13)
    ur.watch_video('Для чего девушкам парень программист?')  # Вам нет 18 лет, пожалуйста покиньте страницу

    ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
    ur.watch_video('Для чего девушкам парень программист?')  # Воспроизведение: 0 секунда ... Конец видео
