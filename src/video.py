import os

from googleapiclient.discovery import build

from helper.youtube_api_manual import playlist_id


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
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
        return self.title


if __name__ == '__main__':
    # Создаем два экземпляра класса
    video1 = Video('9lO06Zxhu88')  # '9lO06Zxhu88' - это id видео из ютуб
    print()

    assert str(video1) == 'Как устроена IT-столица мира / Russian Silicon Valley (English subs)'


class PLVideo(Video):
    def __init__(self, video_id: str, pl_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = pl_id
