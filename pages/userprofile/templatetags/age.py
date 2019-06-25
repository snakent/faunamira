from django import template
import datetime

register = template.Library()

def age(bday, d=None):
	try:
	    if d is None:
	        d = datetime.date.today()
	    age = (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))
	    return str(age) + ' ' + ('год' if age%10==1 else ('года' if age%10>1 and age%10<5 else 'лет'))
	except:
		return ''

register.filter('age', age)