import time
from hashlib import md5
import requests as rq
import json
import math
import pandas as pd

def get_characters(i,j):

    public_key = 'the public key you generated'
    private_key = 'the private key you generated'

    ts = str(time.time())
    hash_str = md5(f"{ts}{private_key}{public_key}".encode("utf8")).hexdigest()

    # print(hash_str)

    params = {
        "apikey": public_key,
        "ts": ts,
        "hash": hash_str,
        "orderBy": "name",
        "limit": i, #variable i to set the limit
        "offset": j} #variable j to set the offset

    try:
        r = rq.get('https://gateway.marvel.com:443/v1/public/characters', params=params)
    except Exception as e:
        return False, e
    else:
        return r.json()

r = get_characters(100, 0) #get initial data of the first 100 characters

total_char = r['data']['total'] #total number of characters

df = pd.DataFrame(r["data"]["results"]) # initialization of the dataframe
df1 = pd.concat([df['name'], pd.DataFrame(list(df['comics']))['available']], axis=1)
# listing elements of the dictionnary into columns of data frame
# and concatenating the column of names with column of comics count

#we use loop to bypass the limit of 100 set by marvel api
for i in range(1, math.ceil(total_char / 100)):
    r = get_characters(100, i * 100)
    df = pd.DataFrame(r["data"]["results"])
    df2 = pd.concat([df['name'], pd.DataFrame(list(df['comics']))['available']], axis=1)
    df1 = pd.concat([df1, df2]) #recursive concatination to add new data

#df1 dataframe contain the complete set of characters with the according comics count
print(df1.head(50)) #displaying first 50 elements of df1