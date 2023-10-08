# mysql
mysql_host = 'localhost'
mysql_port = 3306
mysql_user = 'root'
mysql_pass = 'root'
mysql_database = 'osu'
mysql_url = f'mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_database}?charset=utf8mb4'

# redis
redis_host = 'localhost'
redis_port = 6379
redis_pass = 'omoi'
redis_db = 0
redis_subscribe = f'__keyevent@{redis_db}__:expired'

# kook bot token
bot_token = '1/MTA2MDQ=/HWm7zympOUBjWpRxEK5EHw=='

# osu api token
client_id = 6587
client_secret = "ULY2zz2uUqdkxZ7u65M7trUZfpamZZV6E1wxtwox"

# admin
admin_id = ('565510950',)

# playing status
playing_game_id = 5883  # osu!

# emoji guild
emoji_guild = '9325863522261945'

# channel for user's osu homepage url, when catch osu homepage url will register automatically
user_channel = ('8896430597770990', '4272896228850685',)

# osu guild
osu_guild = '5107224330983339'
osu_guild_role = {'osu': 197862, 'taiko': 197869, 'fruits': 197870, 'mania': 197865}