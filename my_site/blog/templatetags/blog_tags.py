from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag("blog/post/latest_post.html")
def latest_posts(count = 3):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest': latest_posts}

@register.simple_tag
def get_most_commented(count = 3):
    return Post.published.annotate(
        total_comments = Count('commetns')
    ).order_by('-total_comments')[:count]
