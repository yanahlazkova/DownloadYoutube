from pytube import YouTube
import windowMessage
# import threading


class Downloader:
    """ download video, display video data """
    url_video = ""
    widgets = {}

    # to review: it seems like too complicated logic for a simple constuctor
    # check, if you really need it
    def __init__(self, url, widgets): # progressbar, percentage):
        self.widgets = widgets
        self.progressbar = self.widgets["Progressbar"]
        self.label_percentage = self.widgets["Labels"]["percentage_label"]
        self.url_video = url


    def check_video_access(self):
        try:
            self.yt = YouTube(self.url_video,
                              on_progress_callback=self.on_progress,
                              on_complete_callback=self.on_complete
                              ) #, use_oauth=True, allow_oauth_cache=True)
            return True
        except Exception as e:
            windowMessage.open_window_error("Create object Youtube" + str(e))
            return False


        # self.percentage = percentage

        # self.url_video = self.widgets["Combobox_url"].get()


    def __init__(self, url, progress_callback):
        self.progress_callback = progress_callback
        self.url_video = url
        try:
            self.yt = YouTube(self.url_video,
                              on_progress_callback=self.on_progress,
                              on_complete_callback=self.on_complete
                              ) #, use_oauth=True, allow_oauth_cache=True)
        except Exception as e:
            windowMessage.open_window_error(e)


    def get_data_video(self):
        print("Url: ", self.url_video)
        try:
            title = self.yt.title
            author = self.yt.author
            image = self.yt.thumbnail_url
            video_data = {"title": title, "author": author, "image": image}
            return video_data
        except:
            windowMessage.open_window_error("YouTube link is invalid")
            # return None


    def download_video(self):
        try:
            stream = self.yt.streams.get_highest_resolution()
            is_download = stream.download("videos")
            return is_download
        except Exception as e:
            windowMessage.open_window_error(f"Failed to upload video: {e}")

    # todo: you progress bar is not filled correctly, see videos 1 and 3
    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        # self.progress_callback(int(percentage))
        # print(f"Downloaded: {percentage: .2f}%")
        print("%: ", percentage)
        self.percentage.configure(text=f"Downloaded: {percentage} %")
        self.progressbar.set(percentage / 100)
        self.percentage.update()


    # @staticmethod
    def on_complete(self, stream, path_file):
        # windowMessage.show_message_link("Download is completed", path_file)
        windowMessage.open_window_message("Downloaded", "Download is completed")
        print("path: ", path_file)
        # print("stream: ", stream)