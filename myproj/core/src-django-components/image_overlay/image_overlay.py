from django_components.component import register, Component


@register("image-overlay")
class ImageOverlay(Component):
    template_name = "image_overlay/image_overlay.html"

    def get_context_data(self, href=None, target=None, **kwargs):
        klass = kwargs.get("class")
        return {"href": href, "target": target, "class": klass}

    class Media:
        css = {
            "all": [
                "image_overlay/image_overlay.css",
            ],
        }
