from interface import Interface



# create main GUI window
myApp = Interface(title="YouTube Downloader", width=430, height=730)
myApp.create_widgets()
myApp.place_widgets()
myApp.app.mainloop()
