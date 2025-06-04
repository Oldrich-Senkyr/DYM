from django.shortcuts import render
from agent.models import Person


# Create your views here.


def persons_list(request):
    query = request.GET.get("unique_id", "")
    persons = Person.objects.all()
    if query:
        persons = persons.filter(unique_id__icontains=query)
    return render(request, "entrix/persons-list.html", {"persons": persons})

