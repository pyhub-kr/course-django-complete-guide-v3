from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, redirect, get_object_or_404

from weblog.forms import PostForm
from weblog.models import Post


def post_new(request):
    if request.method == "GET":
        form = PostForm()
    else:
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            print("form.cleaned_data :", form.cleaned_data)

            post = form.save(commit=True)

            #
            # post = Post()
            # post.title = form.cleaned_data["title"]
            # post.content = form.cleaned_data["content"]
            # post.status = form.cleaned_data["status"]
            # # post.photo = form.cleaned_data["photo"]
            #
            # photo_file: UploadedFile = form.cleaned_data["photo"]
            # if photo_file is not None:
            #     post.photo.save(photo_file.name, photo_file, save=False)
            #
            # post.save()

            # TODO: detail view 로 이동
            return redirect("/")
        else:
            pass

    return render(
        request,
        "weblog/post_form.html",
        {
            "form": form,
        },
    )


def post_edit(request, pk):
    instance = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        form = PostForm(instance=instance)
    else:
        form = PostForm(data=request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            post = form.save(commit=True)
            # TODO: detail view 로 이동
            return redirect("/")

    return render(
        request,
        "weblog/post_form.html",
        {
            "form": form,
        },
    )
