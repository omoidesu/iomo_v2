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

# iomo url
iomo_url = ''

# kook bot token
bot_token = ''

# osu oauth
oauth_url = ''

# osu api token
client_id = 0
client_secret = ''

osu_tools_path = r''

# admin
admin_id = ('',)

# playing status
playing_game_id = 5883  # osu!

# emoji guild
emoji_guild = ''

# channel for user's osu homepage url, when catch osu homepage url will register automatically
user_channel = ('')

# osu guild
osu_guild = ''
osu_guild_role = {'osu': 0, 'taiko': 0, 'fruits': 0, 'mania': 0}
