import os
import time
import base64
import configparser

config = configparser.ConfigParser()


def base64encode(s):
    return str(base64.b64encode(bytes(s, encoding="utf-8")), encoding="utf-8").rstrip("=")


def base64decode(s):
    if len(s) % 4 != 0:
        s += "=" * (4 - len(s) % 4)
    return str(base64.b64decode(bytes(s, encoding="utf-8")), encoding="utf-8")


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def rename(file_dir, filename, s):
    os.rename(file_dir + "/" + filename, file_dir + "/" + s)


def encode_files(file_dir):
    log = "Encoding...\n"
    files = file_name(file_dir)
    for i in files:
        log += "Filename: {}, Base64: {}\n".format(i, base64encode(i))
        rename(file_dir, i, base64encode(i))
    log += "Done."
    create_log(log)


def decode_files(file_dir):
    log = "Decoding...\n"
    files = file_name(file_dir)
    for i in files:
        log += "Base64: {}, Filename: {}\n".format(i, base64decode(i))
        rename(file_dir, i, base64decode(i))
    log += "Done."
    create_log(log)


def create_log(s):
    localtime = time.localtime(time.time())
    user_dir = os.path.join(os.path.expanduser("~"), 'Documents') + "/HideMyFiles/log"
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    filename = "{}/log-{}-{}-{}-{}-{}-{}.txt".format(user_dir, localtime.tm_year, localtime.tm_mon, localtime.tm_mday,
                                                     localtime.tm_hour, localtime.tm_min, localtime.tm_sec)
    offset = 0
    if not os.path.exists(filename):
        file = open(filename, "w+")
    else:
        while os.path.exists(filename + "-{}".format(offset)):
            offset += 1
        file = open(filename + "-{}".format(offset), "w+")
    file.writelines(s)


def create_config(username, password, path):
    user_dir = os.path.join(os.path.expanduser("~"), 'Documents') + "/HideMyFiles"
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    file_dir = user_dir + "/config.ini"
    config.read(file_dir)
    try:
        config.add_section("Settings")
    except configparser.DuplicateSectionError:
        print("Section 'Settings' already exists")
    config.set("Settings", "Username", base64encode(username))
    config.set("Settings", "Password", base64encode(password))
    config.set("Settings", "Path", base64encode(path))
    config.write(open(file_dir, "w"))


def update_config(section, name, rule):
    if check_config():
        user_dir = os.path.join(os.path.expanduser("~"), 'Documents') + "/HideMyFiles"
        file_dir = user_dir + "/config.ini"
        config.read(file_dir)
        try:
            config.add_section(section)
        except configparser.DuplicateSectionError:
            print("Section '{}' already exists".format(section))
        config.set(section, name, rule)
        config.write(open(file_dir, "w"))


def read_config():
    user_dir = os.path.join(os.path.expanduser("~"), 'Documents') + "/HideMyFiles"
    file_dir = user_dir + "/config.ini"
    config.read(file_dir)
    username = base64decode(config.get("Settings", "Username"))
    password = config.get("Settings", "Password")
    path = base64decode(config.get("Settings", "Path"))
    try:
        status = base64decode(config.get("Status", "Hide"))
    except:
        status = "False"
    try:
        language = base64decode(config.get("Settings", "Language"))
    except:
        language = "English"
    return username, password, path, status, language


def check_config():
    user_dir = os.path.join(os.path.expanduser("~"), 'Documents') + "/HideMyFiles"
    if os.path.exists(user_dir + "/config.ini"):
        if os.path.getsize(user_dir + "/config.ini") > 0:
            return True
    return False
