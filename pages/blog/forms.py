from django import forms
from tinymce.widgets import TinyMCE

from pages.blog.models import Blog
from pages.animal.models import Animal

class BlogForm(forms.ModelForm):	
	article = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))

	def __init__(self, *args, **kwargs):
		try:
			user=self.user
			self.img = self.instance.image
			self.fields['article'].required = False
		except:
			pass
		super(BlogForm, self).__init__(*args,**kwargs)
		try:
			if user:
				self.fields['animals'].queryset = Animal.objects.filter(user=user)
		except:
			pass

	class Meta:
		model = Blog
		fields = ['title', 'image', 'article', 'animals']
