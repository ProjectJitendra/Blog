from django.conf import settings as dj_settings
from django.db.models import Count
from web.models import Category, Post


def all_category(request):
    popular_posts = Post.objects.annotate(likes_count=Count('likes')).filter(likes_count__gt=2).order_by('-created_at')[:5]

    return {'categories': Category.objects.all(),
            'popular_blog': popular_posts,
            'category':Category.objects.all()[:5]
            }

def settings(request):
	return {'settings': dj_settings}
