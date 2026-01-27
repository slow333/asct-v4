from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Q, Count
from .models import Post, Category, Comment
from .forms import PostForm, PostFormAdmin, CommentForm
from polls.forms import QuestionForm, ChoiceForm

def post_list(request):
    query_set = Post.objects.all().order_by('-updated_at')\
            .select_related('author')\
            .select_related('author__profile')\
            .select_related('category')\
                .annotate(like_count=Count('likes'))

    search_title = request.GET.get('searched', '')
    if search_title:
        query_set = query_set.filter(Q(title__icontains=search_title) | Q(author__username__icontains=search_title))

    category_list = list(Category.objects.all().values('name')) 

    # [{'name': '카테고리1', 'count': 5}, {'name': '카테고리2', 'count': 3}, ...]
    for cat in category_list:
        cat['count'] = Post.objects.filter(category__name=cat['name']).count()

    current_category = request.GET.get('category', '')
    
    if current_category == '미분류':
        query_set = query_set.filter(category__isnull=True)

    # 미분류(None) 카테고리 추가
    none_category_count = Post.objects.filter(category__isnull=True).count()
    category_list.append({'name': '미분류', 'count': none_category_count})
    
    if current_category:
        query_set = query_set.filter(category__name=current_category)
    
    paginator = Paginator(query_set, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    likes_count = Post.objects.annotate(like_count=Count('likes'))
    context = {
        'page_obj': posts,
        'category_list': category_list,
        'current_category': current_category,
        'likes_count': likes_count,
    }
    return render(request, 'blog/home.html', context )

@login_required
def add_post(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = PostFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '새 게시글이 생성되었습니다.')
                return redirect('blog:index')
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.instance.author = request.user
                form.save()
                messages.success(request, '새 게시글이 생성되었습니다.')
                return redirect('blog:index')
    else:
        if request.user.is_superuser:
            form = PostFormAdmin()
        else:
            form = PostForm()
    return render(request, 'blog/create.html', {'form': form})

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if request.user.is_superuser:
            form = PostFormAdmin(request.POST, instance=post, files=request.FILES)
        else:
            form = PostForm(request.POST, instance=post, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', pk=post.pk)
    else:
        if request.user.is_superuser:
            form = PostFormAdmin(instance=post)
        else:
            form = PostForm(instance=post)
    return render(request, 'blog/update.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = Comment.objects.filter(post=post).select_related('author').select_related('author__profile') # type: ignore
    comment_form = CommentForm()
    q_form = QuestionForm(initial={'blog': post})
    c_form = ChoiceForm()
    
    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comment,
        'q_form': q_form,
        'c_form': c_form,
    }
    return render(request, 'blog/detail.html', context )

@login_required # type: ignore
def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if user in post.likes.all(): # type: ignore
            post.likes.remove(user) # type: ignore
            messages.info(request, 'You unliked the post.')
        else:
            post.likes.add(user) # type: ignore
            messages.success(request, 'You liked the post.')
        return_url = request.META.get('HTTP_REFERER', reverse_lazy('blog:detail', kwargs={'pk': post.pk}))
        return redirect(return_url)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/delete.html', {'post': post})

def user_post_list(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-updated_at')
    messages.success(request, f'{user.username} 님의 게시글 입니다.')
    
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    return render(request, 'blog/user_posts.html', {'page_obj': page_obj})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:detail', pk=comment.post.pk)
    return render(request, 'blog/delete_comment.html', {'comment': comment})
