from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

class OrderView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    try:
      order = Order.objects.get(user=request.user, ordered=False)
      context = {
        'order': order
      }
      return render(request, 'app/order.html', context)
    except ObjectDoesNotExist:
      return render(request, 'app/order.html')

@login_required
def addItem(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order_item, created = OrderItem.objects.get_or_create(
    item=item,
    user=request.user,
    ordered=False
  )
  order = Order.objects.filter(user=request.user, ordered=False)

  if order.exists():
    order = order[0]
    if order.items.filter(item__slug=item.slug).exists():
      order_item.quantity += 1
      order_item.save()
    else:
      order.items.add(order_item)
  else:
    order = Order.objects.create(user=request.user, ordered_data=timezone.now())
    order.items.add(order_item)

  return redirect('order')

@login_required
def removeItem(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order = Order.objects.filter(
    user=request.user,
    ordered=False
  )
  if order.exists():
    order = order[0]
    if order.items.filter(item__slug=item.slug).exists():
      order_item = OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
      )[0]
      order.items.remove(order_item)
      order_item.delete()
      return redirect("order")

    return redirect("product", slug=slug)

@login_required
def removeSingleItem(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order = Order.objects.filter(
    user=request.user,
    ordered=False
  )
  if order.exists():
    order = order[0]
    if order.items.filter(item__slug=item.slug).exists():
      order_item = OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
      )[0]
      if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
      else:
        order.items.remove(order_item)
        order_item.delete()
      return redirect("order")

    return redirect("product", slug=slug)

class ItemDetailView(DetailView):
  model = Item
  template_name = 'app/product.html'

class IndexView(ListView):
  model = Item
  template_name = 'app/index.html'