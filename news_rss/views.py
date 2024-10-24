from django.shortcuts import render
import feedparser


########################
'''News Feedparser'''
########################
def get_news():
    feed_url = "https://jogja.antaranews.com/rss/pariwisata-budaya.xml"
    try:
        response = requests.get(feed_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return []
    
    feed = feedparser.parse(response.content)
    return feed.get('entries', [])

def news_view(request):
    articles = get_news()
    return render(request, 'news_.html', {'articles': articles})
    ########################