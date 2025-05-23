from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('counseling')

for model in app.get_models():
    admin.site.register(model)

# app = apps.get_app_config('users')

# for model in app.get_models():
    # admin.site.register(model)
