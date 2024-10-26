import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from .models import RSSItem, ImageModel
from datetime import datetime
from django.views.decorators.http import require_http_methods


def strip_namespaces(root):
    for elem in root.iter():
        elem.tag = elem.tag.split('}')[-1]
        elem.attrib = {key.split('}')[-1]: val for key, val in elem.attrib.items()}


@require_http_methods(["GET"])
def fetch_rss_items(request):
    url = "https://jogja.antaranews.com/rss/photo.xml"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        strip_namespaces(root) 

        channel = root.find('channel')
        items = channel.findall('item')

        for item in items:
            title = item.find('title').text
            description = item.find('description').text
            pub_date_str = item.find('pubDate').text
            pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')

            media_content = item.find('content')
            if media_content is not None:
                image_url = media_content.get('url')
            else:
                image_url = None

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

    rss_items = RSSItem.objects.all().order_by('-pub_date')

    return render(request, 'rss_carousel.html', {'items': rss_items})
