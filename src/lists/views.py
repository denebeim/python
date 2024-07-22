from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .forms import ItemForm, EMPTY_ITEM_ERROR
from .models import Item, List


# Create your views here.
def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)

    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            item = Item.objects.create(text=request.POST["text"], list=our_list)
            return redirect(our_list)
    else:
        form = ItemForm()
    return render(request, "list.html", {"list": our_list, "form": form})
