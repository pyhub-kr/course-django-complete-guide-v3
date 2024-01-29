from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from vanilla import FormView

from weblog.forms import PostForm
from weblog.models import Post


class PostCreateView(FormView):
    form_class = PostForm
    template_name = "weblog/post_form.html"
    success_url = "/"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.ip = self.request.META["REMOTE_ADDR"]
        post.save()
        form.save_m2m()
        return super().form_valid(form)


post_new = PostCreateView.as_view()


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
