from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage
from .models import Post, FeedBack
from django.views.decorators.http import require_POST
from .forms import CommentForm, ContactUsForm
from django.views.generic import ListView
from django.http import HttpResponse

def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
        
    return render(request, 'blog/post/list.html', {'posts':posts})

def new_post_list(request):
    posts = Post.published.all()
    recent = request.GET.get('recent')
    if recent:
        posts = posts.filter(publish__gte='2024-01-01')

    sort_by = request.GET.get('sort', 'desc') 
    if sort_by == 'asc':
        posts = posts.order_by('publish')
    else:
        posts = posts.order_by('-publish')

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    return render(request, 'blog/post/list.html', {'posts': posts})
     


# def post_list(request):
#      posts = Post.objects.all()
#      context = {"posts": posts}
#      return render(request,'blog/post/list.html', context)

# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED)
#     context = {'post': post}
#     return render(request, 'blog/post/detail.html', post)


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

def contact_success(request):
    return render(request, 'blog/post/contacts/contact_success.html')

def contact_us_form(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            FeedBack.objects.create(name = name, email = email, message = message)
            return redirect('blog:contact_success')
        else: return HttpResponse("error")
    else:
        form = ContactUsForm()
        context = {'form':form}
        return render(request, 'blog/post/contacts/contact.html', context)

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