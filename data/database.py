#!/usr/bin/python3
import sqlite3

DATABASE = '/root/jiyoonbot/data/data.db'

def query(command, parameters=()):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(command, parameters)
    data = cursor.fetchall()
    db.close
    return data

def execute(command, parameters=()):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(command, parameters)
    db.commit()
    db.close()

# twitter cog queries

def channel_exists(channel_id):
    data = query("SELECT channel_id FROM follow_list WHERE channel_id=?", (channel_id,))
    return data

def is_followed(channel_id, twitter_id):
    data = query("SELECT * FROM follow_list WHERE channel_id=? and twitter_user_id=?", (channel_id, twitter_id,))
    return data

def follow_site(channel_id, twitter_id):
    execute("REPLACE INTO follow_list(channel_id, twitter_user_id) VALUES(?, ?)", 
    (channel_id, twitter_id,))

def remove_site(channel_id, twitter_id):
    execute("DELETE FROM follow_list WHERE channel_id=? and twitter_user_id=?", 
    (channel_id, twitter_id,))

def check_site(channel_id):
    data = query("SELECT twitter_user_id FROM follow_list WHERE channel_id=?", (channel_id,))
    return data

def get_sites():
    data = query("SELECT DISTINCT twitter_user_id FROM follow_list")
    sites = []
    for site in data:
	    sites.append(str(site[0]))
    return sites

def get_channels(twitter_id):
    data = query("SELECT channel_id FROM follow_list WHERE twitter_user_id=?", (twitter_id,))
    channels = []
    for channel in data:
        channels.append(int(channel[0]))
    return channels

# spotify cog queries

def add_temp(code):
    execute("INSERT INTO code_temp(code) VALUES(?)", (code,))

def rtv_temp():
    data = query("SELECT code FROM code_temp WHERE rowid = (SELECT max(rowid) from code_temp)")
    data = data[0][0]
    return data

def remove_temp():
    execute("DELETE FROM code_temp WHERE rowid = (SELECT max(rowid) from code_temp)")

def add_spt_user(user_id, refresh_token):
    execute("REPLACE INTO spt_users(user_id, refresh_token) VALUES(?, ?)",
    (user_id, refresh_token,))

def rtv_refresh_token(user_id):
    data = query("SELECT refresh_token FROM spt_users WHERE user_id=?", (user_id,))
    return data

def delete_spt_user(user_id):
    execute("DELETE FROM spt_users WHERE user_id=?", (user_id,))

# cookies

def nommer_exists(nommer_id):
    data = query("SELECT * FROM cookies WHERE nommer_id=?", (nommer_id,))
    if data:
        return data[0]
    else:
        return None

def grab_cookies(nommer_id, last_grabbed, total_cookies, total_cookies_grabbed, total_cookies_gifted, total_grab_attempts, total_cookies_received):
    execute("REPLACE INTO cookies(nommer_id, last_grabbed, total_cookies, total_cookies_grabbed, total_cookies_gifted, total_grab_attempts, total_cookies_received) VALUES(?, ?, ?, ?, ?, ?, ?)", 
    (nommer_id, last_grabbed, total_cookies, total_cookies_grabbed, total_cookies_gifted, total_grab_attempts, total_cookies_received,))

# prefixes

def replace_prefix(guild_id, prefix):
    execute("REPLACE INTO prefixes(guild_id, prefix) VALUES(?, ?)", (guild_id, prefix,))

def get_prefix(guild_id):
    data = query("SELECT prefix FROM prefixes WHERE guild_id=?", (guild_id,))
    return data[0][0]

def new_guild_prefix(guild_id):
    execute("INSERT INTO prefixes(guild_id, prefix) VALUES(?, ?)", (guild_id, "$",))

def remove_guild_prefix(guild_id):
    execute("DELETE FROM prefixes WHERE guild_id=?", (guild_id,))