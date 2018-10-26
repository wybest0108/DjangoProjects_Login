from django import forms
from .models import Project, Module


# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ["name", "description", "status"]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-control",
#                                            "style": "margin: 8px;"
#                                            }),
#             "description": forms.Textarea(attrs={"class": "form-control",
#                                                  "style": "margin: 8px;",
#                                                  "rows": "3",
#                                                  "cols": "40"
#                                                  }),
#             "status": forms.CheckboxInput(attrs={"style": "margin: 5px 8px 8px 8px;"}),
#         }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        exclude = ["create_time"]