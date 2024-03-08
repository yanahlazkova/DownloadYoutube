from pytube import YouTube
import windowMessage


class Download:
    url_video = ""

    def __init__(self, url):
        if url == "":
            return
        else:
            url_video = url
            try:
                self.yt = YouTube(url_video) #, use_oauth=True, allow_oauth_cache=True)
            except Exception as e:
                windowMessage.open_window_error(e)

    def get_data_video(self):
        try:
            title = self.yt.title
            author = self.yt.author
            image = self.yt.thumbnail_url
            video_data = {"title": title, "author": author, "image": image}

            return video_data
        except:
            windowMessage.open_window_error("YouTube link is invalid")

    def download_video(self):
        try:
            is_download = self.yt.streams.get_highest_resolution().download("videos")
            print("download_video: ", is_download)
            return is_download
        except Exception as e:
            windowMessage.open_window_error(f"Failed to upload video: {e}")
