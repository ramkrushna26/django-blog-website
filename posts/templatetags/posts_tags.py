from django import template
from ..models import Post
import requests
import lxml
from bs4 import BeautifulSoup

register = template.Library() 

@register.inclusion_tag('posts/snippets/recent_posts.html')
def recent_posts():
    return {
        # This is just an example query, your actual models may vary
        'post_list': Post.objects.all().order_by("-posted_on")[:3]
    }


@register.inclusion_tag('posts/snippets/rss_medium.html')
def rss_medium():
    url = 'https://levelup.gitconnected.com/feed'
    responce = requests.get(url)
    soup = BeautifulSoup(responce.content, features='xml')
    items = []
    for item in soup.findAll('item')[:5]:
        items.append({'title':item.title.text, 'link':item.link.text})
    return {
        'items': items
    }