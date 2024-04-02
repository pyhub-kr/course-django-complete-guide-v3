from django_components.component import register, Component


@register("carousel")
class Carousel(Component):
    template_name = "carousel/carousel.html"

    def get_context_data(self, photo_list, attr_name=None):
        keys = (attr_name or "").split(".")

        img_url_list = []
        for attr in photo_list:
            for key in keys:
                attr = getattr(attr, key, None)
            img_url_list.append(attr)

        return {
            "img_url_list": img_url_list,
        }

    class Media:
        js = [
            "observe-node-insertion.js",
            "carousel/carousel.js",
        ]
        css = {
            "all": [
                "carousel/carousel.css",
            ],
        }
