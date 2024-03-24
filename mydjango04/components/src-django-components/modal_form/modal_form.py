from django_components.component import register, Component


@register("modal-form")
class ModalForm(Component):
    template_name = "modal_form/modal_form.html"

    def get_context_data(self, id=None):
        return {"id": id}

    class Media:
        js = [
            "observe-node-insertion.js",
            "modal_form/modal_form.js",
        ]
