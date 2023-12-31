from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy
from .forms import AddBookForm
from django.contrib import messages
from .models import Book
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Email Sending Function
def send_author_email(user, subject, template):
        message = render_to_string(template,{
            'user': user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()
        
# Create your views here.
class AddBookView(CreateView):
    template_name = 'book.html'
    success_url = reverse_lazy('profile')
    form_class = AddBookForm
    
    def form_valid(self, form):
        messages.success(self.request, 'Book Added Successfully')
        form.instance.author = self.request.user.profile
        send_author_email(self.request.user, "Add Book to eBOOK", 'add_book_mail.html')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'name': 'Add A Book',
            'type': '1',
        })
        return context
    
class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    
class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book_details.html'
    context_object_name = 'book'
    