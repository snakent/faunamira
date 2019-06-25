from django.contrib.auth.models import User
from django.db.models import Q
from pages.animal.models import Animal, AnimalAttr

def get_similar_people(user, people):
    """
    Поиск похожих людей
    """
    query = User.objects.filter(is_active=True).exclude(username=people.username).exclude(username=user.username)
    if query:
        try:
            pfind = people.about.find
            ppurp = people.about.purpose
        except:
            results = None
        else:
            results = query.filter(profile__gender=pfind, about__purpose=ppurp)
            if not results:
                results = query.filter(Q(profile__gender=pfind) | Q(about__purpose=ppurp))
                if not results:
                    results = query
    else:
        results = None
    return results


def get_similar_animal(animal):
    """
    Поиск похожих животных
    """
    query = Animal.objects.filter(user__is_active=True).exclude(pk=animal.pk)
    if query:
        try:
            astatus = animal.status
            agender = animal.gender
            akind = animal.kind
            aattrs = AnimalAttr.objects.filter(animal__pk=animal.pk)
            attrlist = []
            for atr in aattrs:
                attrlist.append(atr.value)
        except:
            results = None
        else:
            results = query.filter(gender=agender, status=astatus, kind=akind, AnimalAttr__value__in=attrlist)
            if not results:
                results = query.filter(gender=agender, status=astatus, kind=akind)
    else:
        results = None
    return results