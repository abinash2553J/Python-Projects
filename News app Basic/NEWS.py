import requests # pip install requests

query = input("What type of news are you interested in today? ")
api = "197e5982c77a497ea92817bde45c472b"

url = f"https://newsapi.org/v2/everything?q={query}&from=2025-05-20&sortBy=publishedAt&apiKey={api}"

print(url)
r =  requests.get(url)

data = r.json()
articles = data["articles"]

for index, article in enumerate(articles):
    print(index + 1, article["title"], article["url"])
    print("\n****************************************\n")
