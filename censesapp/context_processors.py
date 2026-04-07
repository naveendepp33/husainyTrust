from .models import News

def news_context(request):
    news = News.objects.first()
    return {"site_news": news}