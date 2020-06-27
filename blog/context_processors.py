from blog.models import TagType


def tag_type_processor(request):
    tag_types = TagType.objects.all()
    return {'tag_types': tag_types}