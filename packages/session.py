import os
import json
import shutil


class Session(object):
    def create_user_folder(self):
        os.makedirs(os.getcwd() + "/session/" + str(self.username), exist_ok=True)
        return str(os.getcwd() + "/session/" + str(self.username))

    def __init__(self):
        self.username = "default"
        self.user_file_path = (
            os.getcwd()
            + "/session/"
            + str(self.username)
            + "/"
            + str(self.username)
            + ".json"
        )

        if os.path.exists(self.user_file_path):
            self.user_folder = os.getcwd() + "/session/" + str(self.username)
            self.user_info = self.get_session_details()
            self.save_user_info()
        else:
            # self.user_info = {
            #     "current_photo_name": username
            # }
            self.user_info = {}
            self.user_folder = self.create_user_folder()
            self.save_user_info()

    def get_session_details(self):
        user_session_path = self.user_folder + "/{}.json".format(self.username)
        with open(user_session_path) as json_file:
            data = json.load(json_file)
            return data

    def save_user_info(self):
        # self.update_last_action()
        # self.save_to_user_history()
        with open(
            self.user_folder + "/{}.json".format(self.username), "w", encoding="utf-8"
        ) as f:
            json.dump(self.user_info, f, ensure_ascii=False, indent=4)

    def store_photo(self, photo_name):
        # TODO fix this for multiplyuser
        """ """
        self.user_info["current_photo_to_save"] = photo_name
        self.save_user_info()

    def get_photo_name(self):
        pic = self.user_info["current_photo_to_save"]
        self.store_photo('')

    def photo_not_exist(self):
        session_exist = os.path.exists(self.user_file_path) and not self.user_info.get("current_photo_to_save") 
        return session_exist

    

    #     self.username = username
    #     self.password = password
    #     self.cur_chat = chat
    #     self.message_id = message_id
    #     # check_folder
    #     # exists load
    #     # else create
    #

    # def update_user_info(self, value, condition):
    #     self.user_info[value] = condition
    #     self.save_user_info()

    # def update_state_user(self, state, value, password=False):
    #     self.update_last_action()
    #     self.user_info["state"][state] = value
    #     if password:
    #         self.user_info["password"] = password
    #     self.save_user_info()

    # def update_user_creditails(self, place, check_place, value_for_place):
    #     self.update_last_action()
    #     self.user_info[place][check_place] = value_for_place
    #     self.save_user_info()

    # def reset_login_session(self):
    #     # reset all and back to login menu
    #     self.user_info["on_check_photos"] = False
    #     self.user_info["changer"]["old_password"] = False
    #     self.user_info["changer"]["new_password"] = False
    #     self.user_info["photo_position"]["latitude"] = False
    #     self.user_info["photo_position"]["longitude"] = False
    #     self.update_state_user("upload", False)
    #     self.update_state_user("change_password", False)
    #     self.update_state_user("change_time_check_updates", False)
    #     self.update_state_user("login", True)
    #     self.save_user_info()

    # def get_user_info_value(self, value):
    #     self.update_last_action()
    #     return self.user_info[value]

    # def clean_session(self):
    #     shutil.rmtree(self.user_folder, ignore_errors=True)
