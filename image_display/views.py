import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from .models import RSSItem

#No HTTP required since it is called on a seperate page
def fetch_and_store_rss_items():
    url = "https://jogja.antaranews.com/rss/photo.xml"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        namespaces = {
            'media': 'http://search.yahoo.com/mrss/',
        }

        channel = root.find('channel')
        items = channel.findall('item')

        for item in items:
            title = item.find('title').text
            description = item.find('description').text
            pub_date_str = item.find('pubDate').text
            pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')

            # Find the media:content element using namespaces
            media_content = item.find('media:content', namespaces)
            if media_content is not None:
                image_url = media_content.get('url')
            else:
                image_url = None

            # Update or create the RSSItem object
            RSSItem.objects.update_or_create(
                title=title,
                defaults={
                    'description': description,
                    'pub_date': pub_date,
                    'image_url': image_url,
                }
            )
    else:
        print(f"Failed to fetch RSS feed. Status code: {response.status_code}")
