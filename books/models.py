from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    date_of_publication = models.DateField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='books/uploads', blank=True, null=True)
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField('Category', related_name='books')
    is_borrowed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title} - {self.author}'