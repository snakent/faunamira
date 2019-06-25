from django.forms import ModelForm, inlineformset_factory, modelformset_factory


from pages.animal.models import Animal, AnimalAttr, KindAnimalAttr,AnimalPhoto


class AnimalForm(ModelForm):

    class Meta:
        model = Animal
        fields = ['first_name', 'second_name', 'gender', 'info', 'birthday', 'kind', 'avatar']


class AnimalAttrForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnimalAttrForm, self).__init__(*args,**kwargs)
        try:
        	attrs_already_have = list(AnimalAttr.objects.filter(animal=self.instance).values('attr').values_list('attr', flat=True))
        	kinds = KindAnimalAttr.objects.filter(kind=self.instance.kind)
        	attrs_filtered = kinds.exclude(id__in=attrs_already_have)
       		self.fields['attr'].queryset = attrs_filtered
       	except:
       		pass

        #super(AnimalAttrForm, self).__init__(*args, **kwargs)


    class Meta:
        model = AnimalAttr
        fields = ['attr', 'value']


class AnimalUpdAttrForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnimalUpdAttrForm, self).__init__(*args,**kwargs)
        try:
        	attrs = list(AnimalAttr.objects.filter(pk=self.instance.pk).values('attr').values_list('attr', flat=True))
        	kinds = KindAnimalAttr.objects.filter(id__in=attrs)
       		self.fields['attr'].queryset = kinds
       	except:
       		pass

    class Meta:
        model = AnimalAttr
        fields = ['attr', 'value']



class AnimalPhotoForm(ModelForm):

    class Meta:
        model = AnimalPhoto
        fields = ['title', 'photo']



#AnimalFormset = inlineformset_factory(Animal, AnimalAttr, fields=('attr', 'value'))
#AnimalFormset = modelformset_factory(AnimalAttr, form=AnimalAttrForm, fields=('attr', 'value'))