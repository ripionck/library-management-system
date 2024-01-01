from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy
from .forms import AddBookForm, ReviewForm
from django.contrib import messages
from .models import Book, Review
from users.models import UserProfile
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
    
    def get(self, request):
        books_with_reviews = []

        # Retrieve all books
        all_books = Book.objects.all()

        # Iterate through each book and retrieve its reviews
        for book in all_books:
            reviews = Review.objects.filter(book=book)
            books_with_reviews.append({'book': book, 'reviews': reviews})

        return render(request, self.template_name, {'books_with_reviews': books_with_reviews})
    
class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book_details.html'
    context_object_name = 'book'

@method_decorator(login_required, name='dispatch')
class CreateReviewView(View):
    template_name = 'books/create_review.html'

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = ReviewForm()
        return render(request, self.template_name, {'book': book, 'form': form})

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']

            # Get the UserProfile instance corresponding to the logged-in user
            user_profile = get_object_or_404(UserProfile, user=request.user)

            Review.objects.create(user=user_profile, book=book, rating=rating, comment=comment)

            # You may want to add a success message or redirect to the book detail page
            return redirect('book_review', book_id=book.id)

        # If form is not valid, render the form again with errors
        return render(request, self.template_name, {'book': book, 'form': form})