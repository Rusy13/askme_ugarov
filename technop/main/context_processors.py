from .models import Tag, Profile

def popular_tags_and_members(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    return {
        'popular_tags': popular_tags,
        'popular_members': popular_members,
    }
