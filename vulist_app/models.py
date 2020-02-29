from django.db import models

# Create your models here.

class Product(models.Model):
	title = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=100, decimal_places=2, null=True)
	description = models.TextField()
	img = models.ImageField()

	def __str__(self):
		return self.title
