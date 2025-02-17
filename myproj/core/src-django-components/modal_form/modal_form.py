from django_components import register, Component


@register("modal-form")
class ModalForm(Component):
    template_name = "modal_form/modal_form.html"

    class Media:
        js = [
            "observe-node-insertion.js",
            "modal_form/modal_form.js",
        ]
