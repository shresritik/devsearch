from .models import Project,Review
from django import forms

# creating form based on the Project model of the database and using it in as html


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description',
                  'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
# overridinig init method to apply class for styling

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['value','body']
        labels={
            'value':"Place your vote",
            'body':"Add a comment with your vote"
        }
      
# overridinig init method to apply class for styling

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
