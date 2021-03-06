from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/lists/the-only-list-in-the-world/')
	return render(request, 'home.html')

def new_list(request):
	list_ = List.objects.create()
	item = Item.objects.create(text=request.POST['item_text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request, 'home.html', {"error": error})
	
	return redirect(list_)

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	error = None
	if request.method == 'POST':
		try:
			item = Item(text=request.POST['item_text'], list=list_)
			item.full_clean()
			item.save()
			return redirect(list_)
		except ValidationError:
			error = "You can't have an empty list item"
			return render(request, 'list.html', {'list': list_, 'error': error})
		
	return render(request, 'list.html',	{'lists': list_})
	