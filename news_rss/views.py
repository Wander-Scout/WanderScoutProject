from django.shortcuts import render
import feedparser


########################
'''News Feedparser'''
########################
def get_news():
    feed_url = "https://jogja.antaranews.com/rss/pariwisata-budaya.xml"
    feed = feedparser.parse(feed_url)
    return feed.entries

def news_view(request):
    articles = get_news()
    return render(request, 'news_.html', {'articles': articles})
    ########################