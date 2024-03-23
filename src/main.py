from interface import Interface



# create main GUI window
myApp = Interface(title="YouTube Downloader", width=400, height=700)
myApp.create_widgets()
myApp.place_widgets()
myApp.app.mainloop()
