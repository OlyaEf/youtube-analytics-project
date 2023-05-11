import json
import os
import googleapiclient.discovery


class Channel:
    """
    Класс для представления YouTube-канала.
    """
    api_key: str = os.getenv('YT_API_KEY')
    channel_id: str = os.getenv('YT_CHANNEL_ID')
    youtube: googleapiclient.discovery.Resource = None

    def __init__(self, channel_id: str) -> None:
        """
        Инициализирует экземпляр класса Channel.
        Args:
            channel_id (str): Идентификатор YouTube-канала.
        Returns:
            None
        """
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=self.api_key)
        self.channel_id = channel_id
        response = self.youtube.channels().list(part="snippet,statistics", id=self.channel_id).execute()
        snippet = response['items'][0]['snippet']
        statistics = response['items'][0]['statistics']
        self.id = self.channel_id
        self.title = snippet['title']
        self.description = snippet['description']
        self.url = f"https://www.youtube.com/channel/{snippet['customUrl']}" if 'customUrl' in snippet \
            else f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscribers_count = statistics['subscriberCount']
        self.video_count = statistics['videoCount']
        self.view_count = statistics['viewCount']

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Channel.
        Returns:
            str: Строковое представление объекта Channel.
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other) -> int:
        """
        Выполняет операцию сложения двух объектов Channel.
        Args:
            other (Channel): Другой объект Channel.
        Returns:
            int: Сумма количества подписчиков двух каналов.
        """
        return int(self.subscribers_count) + int(other.subscribers_count)

    def __sub__(self, other) -> int:
        """
        Выполняет операцию вычитания двух объектов Channel.
        Args:
            other (Channel): Другой объект Channel.
        Returns:
            int: Разность количества подписчиков двух каналов.
        """
        return int(self.subscribers_count) - int(other.subscribers_count)

    def __lt__(self, other) -> bool:
        """
        Выполняет операцию "меньше чем" для двух объектов Channel.
        Args:
            other (Channel): Другой объект Channel.
        Returns:
            bool: Результат сравнения по количеству подписчиков.
        """
        return self.subscribers_count < other.subscribers_count

    def __le__(self, other) -> bool:
        """
        Выполняет операцию "меньше или равно" для двух объектов Channel.
        """
        return self.subscribers_count <= other.subscribers_count

    def __gt__(self, other) -> bool:
        """
        Выполняет операцию "больше чем" для двух объектов Channel.
        """
        return self.subscribers_count > other.subscribers_count

    def __ge__(self, other) -> bool:
        """
        Выполняет операцию "больше или равно" для двух объектов Channel.
        """

        return self.subscribers_count >= other.subscribers_count

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        Returns:
            None
        """
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Custom URL: {self.url}")
        print(f"Subscriber Count: {self.subscribers_count}")
        print(f"Video Count: {self.video_count}")
        print(f"View Count: {self.view_count}")

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        Returns:
            googleapiclient.discovery.Resource: Объект для работы с YouTube API.
        """
        return googleapiclient.discovery.build("youtube", "v3", developerKey=cls.api_key)

    def to_json(self, filename: str) -> None:
        """
        Сохраняет значения атрибутов экземпляра Channel в файл JSON.
        Args:
            filename (str): Имя файла для сохранения.
        Returns:
            None
        """
        data = {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscribers_count': self.subscribers_count,
            'videos_count': self.video_count,
            'views_count': self.view_count,
        }

        with open(filename, 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    vdud.print_info()
    print(vdud.__str__())
