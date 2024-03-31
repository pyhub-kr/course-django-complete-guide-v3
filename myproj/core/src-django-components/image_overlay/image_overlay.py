from django_components.component import register, Component


@register("image-overlay")
class ImageOverlay(Component):
    template_name = "image_overlay/image_overlay.html"

    def get_context_data(self, link=None, target=None, text=None, **kwargs):
        klass = kwargs.get("class")
        return {"link": link, "target": target, "text": text, "class": klass}

    class Media:
        css = {
            "all": [
                "image_overlay/image_overlay.css",
            ]
        }
