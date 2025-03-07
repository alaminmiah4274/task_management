from django import forms
from tasks.models import Task, TaskDetail


# Django Form:
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, label="Assigned To"
    )

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)

        self.fields["assigned_to"].choices = [(emp.id, emp.name) for emp in employees]


class StyledFormMixin:
    """Mixin to apply style to form fields"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widgets()

    default_class = "w-full border-2 border-gray-300 p-3 rounded-md shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update(
                    {
                        "class": self.default_class,
                        "placeholder": f"Enter {field.label.lower()}",
                    }
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "class": f"resize-none {self.default_class}",
                        "placeholder": f"Enter {field.label.lower()}",
                        "rows": 5,
                    }
                )
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update(
                    {
                        "class": "border-2 border-gray-300 p-3 rounded-md shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                    }
                )
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({"class": "space-y-2"})
            else:
                field.widget.attrs.update({"class": self.default_class})


# Djagno Model Form for Task:
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "assigned_to"]
        # exclude = ["project", "is_completed", "created_at", "updated_at"]

        widgets = {
            "due_date": forms.SelectDateWidget,
            "assigned_to": forms.CheckboxSelectMultiple,
        }

        # using widget manually
        # widgets = {
        # 	"title": forms.TextInput(attrs={
        # 			"class": "w-full p-3 border-2 border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500",
        # 			"placeholder": "Enter task title"
        # 		}),
        # 	"description": forms.Textarea(attrs={
        # 		"class": "w-full p-3 border-2 border-gray-300 rounded-md shadow-sm",
        # 		"placeholder": "Describe the task",
        # 		"rows": 5
        # 		}),
        # 	"due_date": forms.SelectDateWidget(attrs = {
        # 			"class": "border-2 p-3 borger-gray-300 rounded-md shadow-sm"
        # 		}),
        # 	"assigned_to": forms.CheckboxSelectMultiple(attrs = {
        # 			"class": "space-x-10"
        # 		})
        # }

    # def __init__(self, *args, **kwargs):
    # 	super().__init__(*args, **kwargs)
    # 	self.apply_style_widgets()


class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ["priority", "notes", "asset"]

    # def __init__(self, *args, **kwargs):
    # 	super().__init__(*args, **kwargs)
    # 	self.apply_style_widgets()
