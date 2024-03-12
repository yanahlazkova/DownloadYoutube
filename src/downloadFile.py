from pytube import YouTube
import windowMessage, interface


class Download:
    url_video = ""

    def __init__(self, url):
        if url == "":
            return
        else:
            url_video = url
            try:
                self.yt = YouTube(url_video,
                                  on_progress_callback=self.on_progress,
                                  # on_complete_callback=self.on_complete,
                                  ) #, use_oauth=True, allow_oauth_cache=True)
            except Exception as e:
                windowMessage.open_window_error(e)

    def get_data_video(self):
        try:
            title = self.yt.title
            author = self.yt.author
            image = self.yt.thumbnail_url
            video_data = {"title": title, "author": author, "image": image}
            print(self.yt.vid_info)

            return video_data
        except:
            windowMessage.open_window_error("YouTube link is invalid")

    def download_video(self):
        try:
            self.stream = self.yt.streams.get_highest_resolution()
            is_download = self.stream.download("videos")
            print("download_video: ", dir(is_download))
            return is_download
        except Exception as e:
            windowMessage.open_window_error(f"Failed to upload video: {e}")

    # def get_info_video(self):
    #     return self.yt.streams.stream, self.yt.bytes_remaining
    def on_progress(self):
        total_size = self.stream.filesize
        bytes_downloaded = total_size - self.stream.bytes_remaining
        percentage_of_compeletion = bytes_downloaded / total_size * 100
        per = str(int(percentage_of_compeletion))
        print("%: ", per)

    @staticmethod
    def on_complete():

        print("complete_callback")