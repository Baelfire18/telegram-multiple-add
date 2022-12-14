# Telegram: Add multiple members to a Group

This a a script that lets you add multiple participants to a Telegram Basic-Group. It also notify you the users who have privacy settings that don't allow them to be added to groups.

## Steps

### Create a Telegram App and Get Your Credentials

- Sign up for Telegram using any application.
- Log in to your Telegram core: https://my.telegram.org.

![](https://i2.wp.com/python.gotrained.com/wp-content/uploads/2019/01/login.png?resize=768%2C418&ssl=1)

- Click on **API development tools** and fill the required fields.

![](https://i1.wp.com/python.gotrained.com/wp-content/uploads/2019/01/desc.png?resize=768%2C479&ssl=1)


You can choose any name for your app. After submitting, you will get basic addresses as well as the `api_id` and `api_hash` parameters required for user authorization.

### Git clone

Git clone the repository

```bash
git clone https://github.com/Baelfire18/telegram-multiple-add.git
```

### Install the required libraries

```bash
pip install -r requirements.txt
```

### Configura the parameters

Create a file called `config.py` and add the following parameters (you can see an example in [config.example.py](config.example.py)):

- `api_id`: The id of the app we created in the previous step.
- `api_hash`: The hash of the app we created in the previous step.
- `phone`: The phone number with which we registered in Telegram.
- `group_link`: The link to join the target group.
- `admins_file_path`: The path of the file that contains the target group administrators.
- `members_file_path`: The path of the file that contains the users to be added to the target group.

### Run the script

```bash
python main.py
```
The first time you run the script, you will be asked to enter the code that Telegram will send to your phone. After entering the code, the script will start adding the users to the group.

## Inspired by

- https://core.telegram.org/methods
- https://python.gotrained.com/scraping-telegram-group-members-python-telethon/
- https://python.gotrained.com/adding-telegram-members-to-your-groups-telethon-python/
