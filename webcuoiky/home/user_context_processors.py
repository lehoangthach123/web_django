from .models import *


def loadBaseItems(request):
    categories = Category.objects.all()
    web = WebsiteState.objects.first()


    return {
        'categories': categories,
        'title': web.title,
    }
