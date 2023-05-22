import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """
        Инициализирует объект Video.
        Args:
            video_id (str): Идентификатор видео.
        """
        self.video_id = video_id
        try:
            response = self.youtube.videos().list(part="snippet,statistics", id=self.video_id).execute()
            snippet = response['items'][0]['snippet']
            statistics = response['items'][0]['statistics']
            self.title = snippet['title']
            self.link = f"https://www.youtube.com/watch?v={self.video_id}"
            self.views = statistics['viewCount']
            self.likes = statistics['likeCount'] or statistics['favoriteCount']
        except Exception as e:
            print(f'Error retrieving video information: {e}')

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Video.
        Returns:
            str: Заголовок видео.
        """
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, pl_id: str) -> None:
        """
        Инициализирует объект PLVideo.
        Args:
            video_id (str): Идентификатор видео.
            pl_id (str): Идентификатор плейлиста.
        """
        super().__init__(video_id)
        self.playlist_id = pl_id
