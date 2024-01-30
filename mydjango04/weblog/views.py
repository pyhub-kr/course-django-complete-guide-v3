from django.core.files.uploadedfile import UploadedFile
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse, reverse_lazy

from django.views.generic import DeleteView as DjangoDeleteView
from vanilla import FormView, CreateView, UpdateView, DeleteView, ListView

# from django.views.generic import FormView

from weblog.forms import PostForm, ConfirmDeleteForm
from weblog.models import Post


# def index(request):
#     return render(request, "weblog/index.html")


index = ListView.as_view(
    model=Post,
    template_name="weblog/index.html",
)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(
        request,
        "weblog/post_detail.html",
        {
            "post": post,
        },
    )


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    # template_name = "weblog/post_form.html"
    # success_url = "/"

    def form_valid(self, form):
        self.object = form.save(commit=False)  # noqa
        self.object.ip = self.request.META["REMOTE_ADDR"]
        return super().form_valid(form)

    # def get_success_url(self) -> str:
    #     # return f"/weblog/{self.object.pk}/"
    #     # return resolve_url("weblog:post_detail", self.object.pk)
    #     # return self.object.get_absolute_url()
    #     return resolve_url(self.object)


post_new = PostCreateView.as_view()


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    # template_name = "weblog/post_form.html"
    # success_url = "/"

    # 장고 기본의 FormView 버전
    # def get_form_kwargs(self):
    #     post_pk = self.kwargs["pk"]
    #     instance = get_object_or_404(Post, pk=post_pk)
    #
    #     form_kwargs = super().get_form_kwargs()
    #     form_kwargs["instance"] = instance
    #     return form_kwargs

    # django-vanilla-views의 FormView 버전
    # def get_form(self, data=None, files=None, **kwargs):
    #     post_pk = self.kwargs["pk"]
    #     instance = get_object_or_404(Post, pk=post_pk)
    #     kwargs["instance"] = instance
    #     return super().get_form(data=data, files=files, **kwargs)

    # def form_valid(self, form):
    #     form.save(commit=True)
    #     return super().form_valid(form)


post_edit = PostUpdateView.as_view()


# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         post.delete()
#         return redirect("weblog:post_new")  # TODO: list 페이지
#     return render(
#         request,
#         "weblog/post_confirm_delete.html",
#         {
#             "post": post,
#         },
#     )


class PostDeleteView(DjangoDeleteView):
    model = Post
    form_class = ConfirmDeleteForm
    success_url = reverse_lazy("weblog:index")


post_delete = PostDeleteView.as_view()
