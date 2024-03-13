from pytube import YouTube
import windowMessage, interface


class Download:
    url_video = ""

    def __init__(self, url, progress_callback):
        if url == "":
            return
        else:
            self.progress_callback = progress_callback
            url_video = url
            try:
                self.yt = YouTube(url_video,
                                  on_progress_callback=self.on_progress,
                                  on_complete_callback=self.on_complete,
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
            is_download = self.yt.streams.get_highest_resolution().download("videos")
            return is_download
        except Exception as e:
            windowMessage.open_window_error(f"Failed to upload video: {e}")


    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_callback(int(percentage))
        print(f"Downloaded: {percentage: .2f}%")


    # @staticmethod
    def on_complete(self, stream, path_file):
        windowMessage.show_message_link("Download is complete", path_file)
        print("complete_callback")