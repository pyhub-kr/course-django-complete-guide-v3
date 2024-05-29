from django.http import HttpResponse
from django.shortcuts import render
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import cache_page, cache_control
from django.views.generic import CreateView, UpdateView
from django_nextjs.render import render_nextjs_page

from blog.forms import TodoForm
from blog.models import Todo, Post
from blog.serializers import TodoSerializer


@cache_page(600)
# @cache_control(private=True)
def index(request):
    post_qs = Post.objects.all()

    query = request.GET.get("query", "")
    if query:
        post_qs = post_qs.filter(title__icontains=query)

    response = render(
        request,
        "blog/index.html",
        {
            "post_list": post_qs,
        },
    )

    if query:
        patch_cache_control(response, private=True)

    return response


def whoami(request):
    status = 200 if request.user.is_authenticated else 401
    username = request.user.username or "anonymous"
    return HttpResponse(f"Your username is <strong>{username}</strong>.", status=status)


class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "blog/_todo_form.html"

    def form_valid(self, form):
        todo = form.save()
        todo_data = TodoSerializer(instance=todo).data

        return render(
            self.request,
            self.template_name,
            {
                "saved_data": todo_data,
            },
        )


todo_new = TodoCreateView.as_view()


class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "blog/_todo_form.html"

    def form_valid(self, form):
        todo = form.save()
        todo_data = TodoSerializer(instance=todo).data

        return render(
            self.request,
            self.template_name,
            {
                "saved_data": todo_data,
            },
        )


todo_edit = TodoUpdateView.as_view()
