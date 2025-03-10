#from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Post
from django.utils import timezone
from django.http import HttpRequest, HttpResponse

def homepage(request):

    #posts = Post.objects.filter(is_published=True).order_by('-published_at')
    posts = Post.objects.all()[0:2]


    return render(request, 'blog/home.html', {'posts': posts})

def add_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        is_published = request.POST.get('is_published', 'on') == 'on'
        post = Post(title=title, content=content, is_published=is_published, published_at=timezone.now(),poster=request.FILES["poster"])
        post.save()
        return redirect('blog:homepage')
    
    return render(request, 'blog/add_post.html')



def details(request:HttpRequest, blog_id:int):

    post = Post.objects.get(pk=blog_id)

    return render(request, 'blog/details.html', {"post" : post})


def update(request:HttpRequest, blog_id:int):

    post = Post.objects.get(pk=blog_id)

    if request.method == "POST":
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.is_published = request.POST["is_published"]
        if "poster" in request.FILES: post.poster = request.FILES["poster"]



        post.save()


        return redirect("blog:details", blog_id=post.id)


    
    return render(request, 'blog/update.html', {"post" : post})

def delete(request:HttpRequest, blog_id:int):

    post = Post.objects.get(pk=blog_id)
    post.delete()

    return redirect("blog:homepage")

def all_publisher(request):

   # posts = Post.objects.filter(title__contains="about")
    posts = Post.objects.filter(is_published=True).order_by('-published_at')

    #posts = Post.objects.all()
    print(posts.count())

    return render(request, 'blog/all_publisher.html', {'posts': posts})
