def get_html(session, url):
    with session.get(url) as resp:

        if resp.status_code != 200:
            print(f"Error: {resp.status_code}")
            return None

        return resp.text
