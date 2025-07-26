# ✅ Install pustaka jika belum tersedia
!pip install requests pandas

# ✅ Import library
import requests
import pandas as pd
import time

# ✅ Masukkan Bearer Token milikmu di sini
BEARER_TOKEN = 'MASUKKAN_TOKEN_KAMU_DI_SINI'

# ✅ Fungsi untuk ambil user_id dari username
def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()['data']['id']

# ✅ Fungsi untuk ambil followers (dengan pagination)
def get_all_followers(user_id, max_followers=10000):
    url = f"https://api.twitter.com/2/users/{user_id}/followers"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "max_results": 1000,
        "user.fields": "username,name"
    }
    followers = []
    next_token = None

    while True:
        if next_token:
            params['pagination_token'] = next_token

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error:", response.text)
            break

        data = response.json()
        followers.extend(data.get('data', []))

        meta = data.get('meta', {})
        next_token = meta.get('next_token')

        print(f"Fetched {len(followers)} followers...")

        if not next_token or len(followers) >= max_followers:
            break

        time.sleep(1)  # Hindari rate limit

    return followers

# ✅ Jalankan semua fungsi
username = "add_infofi"
user_id = get_user_id(username)
followers_data = get_all_followers(user_id)

# ✅ Simpan ke CSV
df = pd.DataFrame(followers_data)
df.to_csv(f"{username}_followers.csv", index=False)

print(f"✅ Selesai! Total follower yang disimpan: {len(df)}")
