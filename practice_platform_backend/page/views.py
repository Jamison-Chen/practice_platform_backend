import json

from django.http import JsonResponse, HttpResponseNotFound
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import article as Article
from .models import paragraph as Parapraph


@csrf_exempt
@require_POST
def create_article(request):
    """
    "fake-domain-name": string,
    "article-title": string,
    "article-subtitle": string,
    "article-body": {
        "text": string,
        "image-url": string,
    }[]
    """
    res = {"error-message": "", "status": "", "article-id": ""}
    if request.user:
        title = request.POST.get("article-title", "")
        subtitle = request.POST.get("article-subtitle", "")
        body = json.loads(request.POST.get("article-body", ""))
        if title != "":
            a = Article.objects.create(title=title, subtitle=subtitle)
            for idx, eachParagraph in enumerate(body):
                if eachParagraph["image"] != None:
                    p.image = eachParagraph["image"]
                    p.save()
                else:
                    p = Parapraph.objects.create(
                        article=a,
                        order_number=idx,
                        text=eachParagraph["text"],
                    )
            res["article-id"] = a.pk
            res["status"] = "succeeded"
        else:
            res["error-message"] = "Please provide article title."
            res["status"] = "failed"
    else:
        res["error-message"] = "Please log in."
        res["status"] = "failed"
    return JsonResponse(res)
    """
    "error-message": string,
    "status": string,
    "article-id": string
    """


@csrf_exempt
@require_POST
def search_article_by_title(request):
    """
    "fake-domain-name": string,
    "article-title": string
    """
    res = {"error-message": "", "articles": [], "status": ""}
    if request.user:
        try:
            a = Article.objects.filter(
                title=request.POST.get("article-title")
            ).order_by("-updated_at")
            for eachArticle in a:
                anArticle = {
                    "id": eachArticle.pk,
                    "title": eachArticle.title,
                    "subtitle": eachArticle.subtitle,
                    "body": [],
                }
                p = eachArticle.paragraphs.order_by("order_number")
                for each in p:
                    anArticle["body"].append(
                        {
                            "text": each.text or "",
                            "image-url": settings.MEDIA_URL + str(each.image)
                            if each.image
                            else "",
                        }
                    )
                res["articles"].append(anArticle)
            res["status"] = "succeeded"
        except Exception as e:
            res["error-message"] = str(e)
            res["status"] = "failed"
    else:
        res["error-message"] = "Please log in."
        res["status"] = "failed"
    return JsonResponse(res)
    """
    "error-message": string,
    "status": string,
    "articles": {
        "id": string,
        "title": string,
        "subtitle": string,
        "body": {
            "text": string,
            "image-url": string,
        }[]
    }[]
    """


@csrf_exempt
@require_POST
def read_article(request):
    """
    "fake-domain-name": string,
    "article-id": string
    """
    res = {
        "error-message": "",
        "article": {"id": "", "title": "", "subtitle": "", "body": []},
        "status": "",
    }
    if request.user:
        try:
            a = Article.objects.get(pk=request.POST.get("article-id"))
            res["article"]["id"] = a.pk
            res["article"]["title"] = a.title
            res["article"]["subtitle"] = a.subtitle

            p = a.paragraphs.order_by("order_number")
            for each in p:
                res["article"]["body"].append(
                    {
                        "text": each.text or "",
                        "image-url": settings.MEDIA_URL + str(each.image)
                        if each.image
                        else "",
                    }
                )
            res["status"] = "succeeded"
        except Exception as e:
            res["error-message"] = str(e)
            res["status"] = "failed"
    else:
        res["error-message"] = "Please log in."
        res["status"] = "failed"
    return JsonResponse(res)
    """
    "error-message": string,
    "status": string,
    "article": {
        "id": string,
        "title": string,
        "subtitle": string,
        "body": {
            "text": string,
            "image-url": string,
        }[]
    }
    """


@csrf_exempt
@require_POST
def update_article(request):
    """
    "fake-domain-name": string,
    "article-id": string,
    "article-title": string,
    "article-subtitle": string,
    "article-body": {
        "text": string,
        "image-url": string,
    }[]
    """
    res = {
        "error-message": "",
        "article": {"id": "", "title": "", "subtitle": "", "body": []},
        "status": "",
    }
    if request.user:
        title = request.POST.get("article-title", "")
        subtitle = request.POST.get("article-subtitle", "")
        body = json.loads(request.POST.get("article-body", ""))
        try:
            a = Article.objects.get(pk=request.POST.get("article-id"))
            a.title = title
            a.subtitle = subtitle
            a.save()
            a.paragraphs.all().delete()
            for idx, eachParagraph in enumerate(body):
                if eachParagraph["image"] != None:
                    p.image = eachParagraph["image"]
                    p.save()
                else:
                    p = Parapraph.objects.create(
                        article=a,
                        order_number=idx,
                        text=eachParagraph["text"],
                    )

            res["article"]["id"] = a.pk
            res["article"]["title"] = title
            res["article"]["subtitle"] = subtitle

            p = a.paragraphs.order_by("order_number")
            for each in p:
                res["article"]["body"].append(
                    {
                        "text": each.text or "",
                        "image-url": settings.MEDIA_URL + str(each.image)
                        if each.image
                        else "",
                    }
                )
            res["status"] = "succeeded"
        except Exception as e:
            res["error-message"] = str(e)
            res["status"] = "failed"
    else:
        res["error-message"] = "Please log in."
        res["status"] = "failed"
    return JsonResponse(res)
    """
    "error-message": string,
    "status": string,
    "article": {
        "id": string,
        "title": string,
        "subtitle": string,
        "body": {
            "text": string,
            "image-url": string,
        }[]
    }
    """


@csrf_exempt
@require_POST
def delete_article(request):
    """
    fake-domain-name: string,
    article-id: string
    """
    res = {"error-message": "", "status": ""}
    if request.user:
        try:
            Article.objects.filter(pk=request.POST.get("article-id")).delete()
            res["status"] = "succeeded"
        except Exception as e:
            res["error-message"] = str(e)
            res["status"] = "failed"
    else:
        res["error-message"] = "Please log in."
        res["status"] = "failed"
    return JsonResponse(res)
    """
    "error-message": string,
    "status": string,
    """
