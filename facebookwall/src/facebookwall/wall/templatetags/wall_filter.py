from django import template

register = template.Library()


@register.filter(name='is_liked')
def is_liked(all_likes, user):
    liked = all_likes.filter(liker=user)
    return liked
