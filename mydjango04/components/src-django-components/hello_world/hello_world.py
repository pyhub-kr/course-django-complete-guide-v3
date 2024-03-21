from typing import Dict, Any

from django_components.component import register, Component


@register("hello-world")
class HelloWorld(Component):
    template_name = "hello_world/hello_world.html"

    def get_context_data(self, name=None) -> dict:
        return {"name": name}

    class Media:
        css = {
            "all": [
                "hello_world/hello_world.css",
            ],
        }
        js = [
            "hello_world/hello_world.js",
        ]
