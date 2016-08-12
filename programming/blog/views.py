from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from blog.forms import CommentModelForm, CommentForm
from blog.models import Post, Comment


def post_list(request):
    return render(request, 'blog/post_list.html', {
        'post_list': Post.objects.all(),
    })


def post_detail(request, pk):
    # try:
    #     post = Post.objects.get(pk=pk)   # Post.DoesNotExist
    # except Post.DoesNotExist:
    #     raise Http404

    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        'post': post,
    })


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentModelForm(request.POST, request.FILES)  # 파일 업로드 받을 때에는 필히 request.FILES 지정하기 !!!
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            # return redirect('blog:post_detail', post.pk)
            messages.success(request, '새 댓글을 저장했습니다.')
            return redirect(post)
            # return redirect(post.get_absolute_url())
            # return redirect('/2/')
    else:
        form = CommentModelForm()

    return render(request, 'blog/comment_form.html', {
        'form': form,
    })


@login_required
def comment_edit(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = Comment.objects.get(pk=pk)

    if (not request.user.is_staff) and (comment.author != request.user):
        messages.warning(request, '본인 댓글만 수정가능합니다.')
        return redirect(post)

    if request.method == 'POST':
        form = CommentModelForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, '댓글을 수정했습니다.')
            return redirect(post)
    else:
        form = CommentModelForm(instance=comment)

    return render(request, 'blog/comment_form.html', {
        'form': form,
    })
