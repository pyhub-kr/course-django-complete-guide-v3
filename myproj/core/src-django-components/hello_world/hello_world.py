from django_components.component import register, Component

try:
    from core.react_components_map import mapper
except ImportError:
    print("mapper 파일을 임포트할 수 없습니다.")
    mapper = {}


try:
    css_list = mapper["hello_world.html"]["css"]
except KeyError:
    css_list = []


try:
    js_list = mapper["hello_world.html"]["js"]
except KeyError:
    js_list = []


@register("hello-world")
class HelloWorld(Component):
    template_name = "hello_world/hello_world.html"

    def get_context_data(self, id=None, name=None, **kwargs):
        klass = kwargs.get("class", None)
        return {
            "id": id,
            "class": klass,
            "name": name,
        }

    class Media:
        css = {
            "all": css_list,
        }
        js = js_list
