
from django.conf import settings
from django.db import models

class Item(models.Model):
  title = models.CharField(max_length=100)
  price = models.IntegerField()
  category = models.CharField(max_length=100)
  slug = models.SlugField()
  description = models.TextField()
  image = models.ImageField(upload_to='images')

  def __str__(self):
    return self.title

class OrderItem(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  ordered = models.BooleanField(default=False)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)

  def get_total_item_price(self):
    return self.quantity * self.item.price

  def __str__(self):
    return f"{self.item.title} : {self.quantity}"

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  items = models.ManyToManyField(OrderItem)
  start_data = models.DateTimeField(auto_now_add=True)
  ordered_data = models.DateTimeField()
  ordered = models.BooleanField(default=False)

  def get_total(self):
    total = 0
    for order_item in self.items.all():
      total += order_item.get_total_item_price()
    return total

  def __str__(self):
    return self.user.email
