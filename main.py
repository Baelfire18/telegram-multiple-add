from telethon.sync import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest, EditChatAdminRequest
from telethon.errors.rpcerrorlist import (
    PeerFloodError,
    UserPrivacyRestrictedError,
    UserAlreadyParticipantError,
)

from config import api_id, api_hash, phone, group_link, admins_file_path, members_file_path


class TelegramBot(TelegramClient):
    def __init__(self, phone: str, api_id: int, api_hash: str) -> None:
        super().__init__(phone, api_id, api_hash)
        self.__usernames_files_paths = []
        self.connect()

        if not self.is_user_authorized():
            self.send_code_request(phone)
            self.sign_in(phone, input("Enter the code: "))

    def add_group(self, group_link: str) -> None:
        self.__group_link = group_link
        self.__group_name = self.__group_link.strip("https://t.me/")
        self.__group_entity = self.get_input_entity(group_link)

    def add_users(self, usernames_file_path: str, make_them_admins: bool = False) -> None:
        self.__usernames_files_paths.append(usernames_file_path)
        with open(self.__usernames_files_paths[-1], "r") as f:
            usernames = f.read().splitlines()

        for username in usernames:
            user_entity = self.get_input_entity(username)
            try:
                self(AddChatUserRequest(self.__group_entity.chat_id, user_entity.user_id, 100))
                # channel
                # self(InviteToChannelRequest(self.__group_entity, [user_entity]))
                # self(EditChatAdminRequest(self.__group_entity.channel_id, user_entity, True))
            except UserAlreadyParticipantError:
                pass
            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now.")
                print(f"Left in {username}:=")
                print("Please try again after some time.")
                break
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping")
                print(f"{username}:=")
                continue
            except:
                print("Unexpected Error")
                print(f"{username}:=")
                break
            print(username)
            if make_them_admins:
                self(EditChatAdminRequest(self.__group_entity.chat_id, user_entity.user_id, True))

    def fetching_members(self) -> None:
        all_participants = self.get_participants(self.__group_entity, aggressive=True)
        all_participants_usernames = [f"@{user.username}" for user in all_participants]
        with open(f"{self.__group_name}_participants_usernames.txt", "w") as f:
            [f.write(username + "\n") for username in all_participants_usernames]

        usernames = []
        for file in self.__usernames_files_paths:
            with open(file, "r") as f:
                usernames += f.read().splitlines()
        request_members = set(usernames)
        actual_participants = set(all_participants_usernames)
        missing_participants = list(request_members - actual_participants)
        if missing_participants:
            with open(f"{self.__group_name}_missing_participants.txt", "w") as f:
                [f.write(username + "\n") for username in missing_participants]

    def disconnect(self) -> None:
        super().disconnect()


client = TelegramBot(phone, api_id, api_hash)
client.add_group(group_link)
client.add_users(admins_file_path, True)
client.add_users(members_file_path)
client.fetching_members()
client.disconnect()
