from pytube import YouTube
from tkinter import messagebox
import windowMessage
import os, re


class Download:
    url_video = ""

    def __init__(self, url):
        self.url_video = url
        try:
            self.yt = YouTube(url)
        except Exception as e:
            windowMessage.open_window_error(e)

    def show_data_video(self):
        try:
            title = self.yt.title
            author = self.yt.author
            image = self.yt.thumbnail_url
            video_data = {"title": title, "author": author, "image": image}

            return video_data
        except:
            windowMessage.open_window_error("YouTube link is invalid")

    def download_video(self):
        self.yt.streams.get_highest_resolution().download("videos")