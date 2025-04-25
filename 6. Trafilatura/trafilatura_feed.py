from trafilatura import feeds, fetch_url, extract

feed_url = "https://www.mk.co.kr/rss/30200030/"

feed_list = feeds.find_feed_urls(feed_url)

for num, feed in enumerate(feed_list,1):
    html = fetch_url(feed)
    text = extract(html)
    print(f"<<<<<{num}>>>>>")
    print(text)
    print()
    
