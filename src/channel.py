import os
import googleapiclient.discovery


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    channel_id: str = os.getenv('YT_CHANNEL_ID')
    youtube: googleapiclient.discovery.Resource = None

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала и api-ключом.
        Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=self.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(
            part="snippet,statistics",
            id=self.channel_id
        ).execute()

        snippet = response['items'][0]['snippet']
        statistics = response['items'][0]['statistics']

        print(f"Title: {snippet['title']}")
        print(f"Description: {snippet['description']}")
        print(f"Custom URL: {snippet['customUrl']}")
        print(f"Published At: {snippet['publishedAt']}")
        print(f"View Count: {statistics['viewCount']}")
        print(f"Subscriber Count: {statistics['subscriberCount']}")
        print(f"Video Count: {statistics['videoCount']}")


if __name__ == '__main__':
    vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    vdud.print_info()

