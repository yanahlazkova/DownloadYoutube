import tkinter as tk
import customtkinter
import listUrls


class DL:
  app = tk.Tk()
  
  def __init__(self) -> None:
    list_urls = [url["url"] for url in listUrls.list_urls]
    self.url_var = tk.StringVar(value="Enter url")
    comboBox = customtkinter.CTkComboBox(self.app, variable=self.url_var, values=list_urls, command=self.Click)
    comboBox.pack()
    
  def Click(self, selected_value):
    print("Selected value:", selected_value)
    

wind = DL()
wind.app.mainloop()




