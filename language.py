import os


class Language:
    def __init__(self, words):
        self.name = words[0]
        self.title = words[1]
        self.set = words[2]
        self.username = words[3]
        self.password = words[4]
        self.submit = words[5]
        self.path_to_hide = words[6]
        self.success = words[7]
        self.failed = words[8]
        self.hello = words[9]
        self.hide = words[10]
        self.show = words[11]
        self.pro = words[12]
        self.normal = words[13]
        self.settings = words[14]
        self.try_again = words[15]
        self.path_not_exist = words[16]
        self.hided = words[17]
        self.showed = words[18]
        self.language = words[19]
        self.save = words[20]
        self.back = words[21]
        self.saved = words[22]


def load_languages():
    languages = {}
    user_dir = os.path.join(os.path.expanduser("~"), 'Documents') + "/HideMyFiles/lang"
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    if not os.path.exists(user_dir + "/language.txt"):
        file = open(user_dir + "/language.txt", "w+")
        language = "English,Hide My Files,Set Username and Password,Username,Password,Submit,Path to Hide,Success,Failed,Hello {},Hide,Show,Pro Mode,Normal Mode,Settings,Try again,Path Not Exist,Files Hided,Files Showed,Language,Save Path,Back,Path Saved\n"
        language += "中文,隐藏文件,初次设置,用户名,密码,提交,要隐藏的目录,成功,失败,你好 {},隐藏,显示,高级模式,普通模式,设置,重试,目录不存在,文件已隐藏,文件已显示,语言,保存目录,返回,目录已保存\n"
        file.write(language)
    file = open(user_dir + "/language.txt", "r")
    for line in file:
        languages[line.split(",")[0]] = Language(line.split(","))
    return languages
