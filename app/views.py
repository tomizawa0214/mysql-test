from django.views.generic import ListView, DetailView
from .models import Item

class ItemDetailView(DetailView):
  model = Item
  template_name = 'app/product.html'
  
class IndexView(ListView):
  model = Item
  template_name = 'app/index.html'