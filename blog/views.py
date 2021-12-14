from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView,DetailView
from . models import Post,Comment
from . forms import CommentsForm
from django.views import View
# 
class StartPageView(ListView):
    template_name="blog/index.html"
    model=Post
    ordering=["-date"]
    context_object_name="posts"
    def get_queryset(self):
        queryset= super().get_queryset()
        latest_post=queryset[:3]
        return latest_post

    

class AllPostsView(ListView):
    template_name="blog/all-posts.html"
    model=Post
    context_object_name="all_posts"
    ordering=["date"]

class PostDetailView(View):
    def is_stored_post(self,request,post_id):
        stored_post=request.session.get("stored_post")
        if stored_post is not None:
            is_read_later=post_id in stored_post
        else:
            is_read_later=False
        return is_read_later
    def get(self,request,slug):
        identified_post=Post.objects.get(slug=slug)
        
        form=CommentsForm()
        return render(request,"blog/post-details.html",{
            "post":identified_post,
            "tags":identified_post.tag.all(),
            "form":form,
            "comments":identified_post.comments.all().order_by("-id"),
            "is_read_later":self.is_stored_post(request,identified_post.id)
        })

    def post(self,request,slug):
        form=CommentsForm(request.POST)
        identified_post=Post.objects.get(slug=slug)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=identified_post
            comment.save()

            return HttpResponseRedirect("/posts/"+slug)
        return render(request,"blog/post-details.html",{
            "post":identified_post,
            "tags":identified_post.tag.all(),
            "form":form,
            "comments":identified_post.comments.all().order_by("-id"),
            "is_read_later":self.is_stored_post(request,identified_post.id)
        })
    # template_name="blog/post-details.html"
    # model=Post
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     identified_object=self.object
    #     context["tags"] = identified_object.tag.all()
    #     context["form"]=CommentsForm()
    #     return context
    

# def post_details(request,slug):
#     identified_post=get_object_or_404(Post,slug=slug)
#     return render(request,"blog/post-details.html",{
#         "post":identified_post,
#         "tags":identified_post.tag.all()
#     })

class ReadLaterView(View):
    def post(self,request):
        stored_post=request.session.get("stored_post")
        post_id=int(request.POST["read_later"])
        if stored_post==None:
            stored_post=[]
        if post_id not in stored_post:
            stored_post.append(post_id)
            request.session["stored_post"]=stored_post
        else:
            stored_post.remove(post_id)
            request.session["stored_post"]=stored_post
        return HttpResponseRedirect("/")

    def get(self,request):
        stored_posts=request.session.get("stored_post")
        context={}
        if(stored_posts==None or len(stored_posts)==0):
            context["posts"]=None
            context["has_posts"]=False
        else:
            posts=Post.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context["has_posts"]=True
        return render(request,"blog/read_later.html",context)

