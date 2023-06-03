import os
import datetime

from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []

    def __init__(self, playlist_id: str) -> None:
        """
        Инициализирует объект PlayList.
        Args:
            playlist_id (str): Идентификатор плейлиста.
        """
        self.playlist_id = playlist_id
        response = self.youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=self.playlist_id
        ).execute()
        video_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]
        videos_response = self.youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(video_ids)
        ).execute()
        for item in videos_response['items']:
            if 'contentDetails' not in item:
                continue
            video = {
                'link': f"https://www.youtube.com/watch?v={item['id']}",
                'likes': int(item['statistics']['likeCount']),
                'duration': self.parse_duration(item['contentDetails']['duration'])
            }
            self.videos.append(video)

        response = self.youtube.playlists().list(part="snippet", id=self.playlist_id).execute()
        snippet = response['items'][0]['snippet']
        self.title = snippet['title']
        self.link = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @staticmethod
    def parse_duration(duration_str: str) -> datetime.timedelta:
        """
        Преобразует строку длительности в объект timedelta.
        Args:
            duration_str (str): Строка длительности в формате ISO 8601.
        Returns:
            timedelta: Объект timedelta, представляющий длительность.
        """
        parts = duration_str.split('T')
        time_parts = parts[1].split('H')
        hours = int(time_parts[0]) if len(time_parts) > 1 else 0
        time_parts = time_parts[-1].split('M')
        minutes = int(time_parts[0]) if len(time_parts) > 1 else 0
        time_parts = time_parts[-1].split('S')
        seconds = int(time_parts[0]) if len(time_parts) > 1 else 0
        return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    @property
    def total_duration(self) -> datetime.timedelta:
        """
        Возвращает общую длительность плейлиста.
        Returns:
            timedelta: Общая длительность плейлиста.
        """
        total_duration = datetime.timedelta()
        for video in self.videos:
            total_duration += video['duration']
        return total_duration

    def show_best_video(self) -> str:
        """
        Возвращает ссылку на видео с наибольшим количеством лайков.
        Returns:
            str: Ссылка на видео с наибольшим количеством лайков.
        """
        if not self.videos:
            return None
        best_video = max(self.videos, key=lambda video: video['likes'])
        return best_video['link']
