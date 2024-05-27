from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django_nextjs.render import render_nextjs_page

from blog.forms import TodoForm
from blog.models import Todo
from blog.serializers import TodoSerializer


def whoami(request):
    status = 200 if request.user.is_authenticated else 401
    username = request.user.username or "anonymous"
    return HttpResponse(f"Your username is <strong>{username}</strong>.", status=status)


async def index(request):
    # return render(request, "blog/index.html")
    return await render_nextjs_page(
        request,
        template_name="blog/index.html",
        context={},
    )


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
