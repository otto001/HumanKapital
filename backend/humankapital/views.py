from django.views.generic.base import RedirectView, TemplateView


app_view = TemplateView.as_view(template_name="application.html")
test_view = TemplateView.as_view(template_name="test.html")
redirect_to_app = RedirectView.as_view(url="/", permanent=True)
