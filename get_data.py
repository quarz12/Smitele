from typing import List

import requests
import json
import sqlite3 as sql
from pipe import select
import pprint
base_url="https://cms.smitegame.com/wp-json/smite-api/"

def make_url(s,lang_id:int=1):
    return base_url+s+"/"+str(lang_id)

def get_gods()->List[dict]:
    return json.loads(requests.get(make_url("all-gods")).content.decode("utf-8"))

def get_skins(god_id:int):
    return json.loads(requests.get(make_url(f"god-skin/{god_id}")).content.decode("utf-8"))

def update():
    conn=sql.connect("gods.db")
    gods=get_gods()
    for god in gods:
        god.pop("free")
        god.pop("new")
        god.pop("pantheon_EN")
        god.pop("role_EN")
        god.pop("god_name_EN")
    with conn:
        conn.executemany("insert or ignore into GODS(id,name,title,pantheon,pros,type,role,card) values(?,?,?,?,?,?,?,?)",list(gods|select(lambda x:list(x.values()))))

update()
