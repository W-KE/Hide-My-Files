from tkinter import *
from tkinter import messagebox
from utils import *
from language import *


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.language = "English"
        if check_config():
            self.username, self.password, self.path, self.status, self.language = read_config()
        self.mode = "Normal"
        self.languages = load_languages()
        self.language_list = [i for i in self.languages.keys()]
        self.createWidgets()

    def createWidgets(self):
        if check_config():
            self.space1 = Label(self)
        else:
            self.space1 = Label(self, text=self.languages[self.language].set)
        self.space1.grid(row=0)
        self.nameLabel = Label(self, text=self.languages[self.language].username)
        self.nameLabel.grid(row=1, column=0)
        self.nameInput = Entry(self)
        self.nameInput.grid(row=1, column=1)
        self.passwordLable = Label(self, text=self.languages[self.language].password)
        self.passwordLable.grid(row=2, column=0)
        self.passwordInput = Entry(self)
        self.passwordInput.grid(row=2, column=1)
        self.alertButton = Button(self, text=self.languages[self.language].submit, command=self.login)
        if check_config():
            self.alertButton.grid(row=3, columnspan=2)
            self.space2 = Label(self)
            self.space2.grid(row=4)
        else:
            self.alertButton.grid(row=4, columnspan=2)
            self.space2 = Label(self, text=self.languages[self.language].path_to_hide)
            self.space2.grid(row=3, column=0)
            self.pathInput = Entry(self)
            self.pathInput.grid(row=3, column=1)

    def login(self):
        if check_config():
            self.username, self.password, self.path, self.status, self.language = read_config()
            username_input = self.nameInput.get() or ""
            password_input = base64encode(self.passwordInput.get() or "")
            if self.username == username_input and self.password == password_input:
                messagebox.showinfo(self.languages[self.language].success,
                                    self.languages[self.language].hello.format(self.username))
                self.nameLabel.destroy()
                self.nameInput.destroy()
                self.passwordLable.destroy()
                self.passwordInput.destroy()
                self.alertButton.destroy()
                self.space1["text"] = ""
                self.space2["text"] = ""
                self.hideButton = Button(self, text=self.languages[self.language].hide, command=self.hide)
                self.hideButton.grid(row=1, column=0)
                self.showButton = Button(self, text=self.languages[self.language].show, command=self.show)
                self.showButton.grid(row=1, column=1)
                self.modeButton = Button(self, text=self.languages[self.language].pro, command=self.pro)
                self.modeButton.grid(row=2, column=0)
                self.settingButton = Button(self, text=self.languages[self.language].settings, command=self.setting)
                self.settingButton.grid(row=2, column=1)
            else:
                messagebox.showinfo(self.languages[self.language].failed, self.languages[self.language].try_again)
        else:
            if os.path.exists(self.pathInput.get()):
                create_config(self.nameInput.get(), self.passwordInput.get(), self.pathInput.get())
                self.pathInput.destroy()
                self.login()
            else:
                messagebox.showinfo(self.languages[self.language].failed, self.languages[self.language].path_not_exist)

    def hide(self):
        if self.status == "False" or self.mode == "Pro":
            self.status = "True"
            update_config("Status", "Hide", base64encode("True"))
            encode_files(self.path)
            messagebox.showinfo(self.languages[self.language].success, self.languages[self.language].hided)

    def show(self):
        if self.status == "True" or self.mode == "Pro":
            self.status = "False"
            update_config("Status", "Hide", base64encode("False"))
            decode_files(self.path)
            messagebox.showinfo(self.languages[self.language].success, self.languages[self.language].showed)

    def pro(self):
        if self.mode == "Normal":
            self.modeButton["text"] = self.languages[self.language].normal
            self.mode = "Pro"
        else:
            self.modeButton["text"] = self.languages[self.language].pro
            self.mode = "Normal"

    def setting(self):
        self.hideButton.destroy()
        self.showButton.destroy()
        self.modeButton.destroy()
        self.settingButton.destroy()
        self.langLabel = Label(self, text=self.languages[self.language].language)
        self.langLabel.grid(row=1, column=0)
        self.langButton = Button(self, text=self.language, command=self.change_language)
        self.langButton.grid(row=1, column=1)
        self.pathLabel = Label(self, text=self.languages[self.language].path_to_hide)
        self.pathLabel.grid(row=2, column=0)
        self.pathInput = Entry(self)
        self.pathInput.grid(row=2, column=1)
        self.pathButton = Button(self, text=self.languages[self.language].save, command=self.save)
        self.pathButton.grid(row=3, column=0)
        self.backButton = Button(self, text=self.languages[self.language].back, command=self.back)
        self.backButton.grid(row=3, column=1)
        self.space2["text"] = "by Ke Wang"

    def change_language(self):
        curr_language = self.language_list.index(self.langButton["text"])
        self.langButton["text"] = self.language_list[(curr_language + 1) % len(self.language_list)]
        self.language = self.langButton["text"]
        update_config("Settings", "Language", base64encode(self.language))
        self.back()
        self.setting()

    def back(self):
        self.langLabel.destroy()
        self.langButton.destroy()
        self.pathLabel.destroy()
        self.pathInput.destroy()
        self.pathButton.destroy()
        self.backButton.destroy()
        self.space2["text"] = ""
        self.hideButton = Button(self, text=self.languages[self.language].hide, command=self.hide)
        self.hideButton.grid(row=1, column=0)
        self.showButton = Button(self, text=self.languages[self.language].show, command=self.show)
        self.showButton.grid(row=1, column=1)
        self.modeButton = Button(self, text=self.languages[self.language].pro, command=self.pro)
        self.modeButton.grid(row=2, column=0)
        self.settingButton = Button(self, text=self.languages[self.language].settings, command=self.setting)
        self.settingButton.grid(row=2, column=1)

    def save(self):
        if os.path.exists(self.pathInput.get()):
            self.path = self.pathInput.get()
            update_config("Settings", "Path", base64encode(self.path))
            messagebox.showinfo(self.languages[self.language].success, self.languages[app.language].saved)
        else:
            messagebox.showinfo(self.languages[self.language].failed, self.languages[self.language].path_not_exist)


root = Tk()
root.geometry("320x128")
app = Application(root)
app.master.title(app.languages[app.language].title)
app.mainloop()
