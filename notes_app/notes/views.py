from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



from notes.forms import NoteForm
from notes.models import Note

# Create your views here.
def greetings(response):
    return HttpResponse("Hello from Notes app.")

def not_found(response):
    return HttpResponse(status=404)


def create_notes(request):
    notes = Note.objects.all()
    return render(request, "index.html", {"notes": notes})


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note_list")


class NoteDetailView(DetailView):
    model = Note
    template_name = "note_detail.html"


# class NoteUpdateView(UpdateView):
#     model = Note
#     form_class = NoteForm
#     template_name = "note_form.html"
#     success_url = reverse_lazy("note_list")

class NoteUpdateView(View):
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        data = request.POST
        note.title = data.get("title", note.title)
        note.text = data.get("text", note.text)
        note.reminder = data.get("reminder", note.reminder)
        note.save()
        return JsonResponse({"status": "success", "title": note.title})

# class NoteDeleteView(DeleteView):
#     model = Note
#     template_name = "note_confirm_delete.html"
#     success_url = reverse_lazy("note_list")

class NoteDeleteView(DeleteView):
    model = Note

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=204)  

class NoteListView(ListView):
    model = Note
    template_name = "note_list.html"
    context_object_name = "notes"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category")
        search_title = self.request.GET.get("search")

        if category:
            queryset = queryset.filter(category__title=category)

        if search_title:
            queryset = queryset.filter(title__icontains=search_title)

        return queryset
# https://github.com/WonderliP/notes_app/tree/main/notes_app

