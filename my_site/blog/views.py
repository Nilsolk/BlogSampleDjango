from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage
from .models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.views.generic import ListView

def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'blog/post/list.html', {'posts':posts})

def post_detail(request, year, month, day, post):
    # post = get_object_or_404(Post, id=id, status = Post.Status.PUBLISHED, )
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED, 
                             slug = post, 
                             publish__year =year, 
                             publish__month = month, 
                             publish__day= day)

    comments = post.commetns.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 
                                                     'comments': comments, 
                                                     'form': form})  

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'

@require_POST
def post_comment(request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        comment = None

        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

        context = {'post':post, 'form':form, 'comment':comment}
        return render(request, 'blog/post/comment.html', context)