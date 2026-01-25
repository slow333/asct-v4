from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import generic
from library.models import Book, BookInstance, Author
from django.core.paginator import Paginator
from .forms import BookForm, BookInstanceForm, AuthorForm

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'library/index.html', context=context)

def book_list(request):
    queryset = Book.objects.all().select_related('author')
    author_id = request.GET.get('author_id')
    if author_id:
        queryset = queryset.filter(author__id=author_id)

    search_query = request.GET.get('searched','')
    if search_query:
        queryset = queryset.filter(title__icontains=search_query)

    paginator = Paginator(queryset, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    book_count = Book.objects.count()

    return render(request, 'library/book_list.html', 
                { 'page_obj': page_obj, 'book_count': book_count, })

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('library:book-detail', pk=book.pk)
    else:
        form = BookForm()
        return render(request, 'library/book_create.html', { 'form': form })
    
def book_update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('library:book-detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
        return render(request, 'library/book_update.html', { 'form': form })

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})

def book_delete(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('library:books')

def author_list(request):
    queryset = Author.objects.annotate(book_count=Count('book'))
    
    paginator = Paginator(queryset, 9)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    return render(request, 'library/author_list.html', { 'page_obj': page_obj, })

def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            return redirect('library:author-detail', pk=author.pk)
    else:
        form = AuthorForm()
        return render(request, 'library/author_create.html', { 'form': form, })

def author_update(request, pk):
    author = Author.objects.get(pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('library:author-detail', pk=author.pk)
    else:
        form = AuthorForm(instance=author)
        return render(request, 'library/author_update.html', { 'form': form, })

def author_delete(request, pk):
    author = Author.objects.get(pk=pk)
    author.delete()
    return redirect('library:authors')

def author_detail(request, pk):
    author = Author.objects.get(pk=pk)
    author_books = Book.objects.filter(author=author)
    context = {
        'author': author,
        'author_books': author_books,
    }
    return render(request, 'library/author_detail.html', context)

def bookinstances(request):
    queryset = BookInstance.objects.all().select_related('book')
    
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page')
    book_instances = paginator.get_page(page)
    
    return render(request, 'library/bookinstance_list.html', {'page_obj': book_instances })

def bookinstance_create(request, pk=None):
    if request.method == 'POST':
        form = BookInstanceForm(request.POST)
        if form.is_valid():
            book_instance = form.save(commit=False)
            if pk:
                book = Book.objects.get(pk=pk)
                book_instance.book = book
            book_instance.save()
            return redirect('library:bookinstance-detail', pk=book_instance.pk)
    else:
        form = BookInstanceForm()
        if pk:
                book = Book.objects.get(pk=pk)
                form.fields['book'].initial = book
        
        return render(request, 'library/bookinstance_create.html', { 'form': form })

def bookinstance_update(request, pk):
    book_instance = BookInstance.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookInstanceForm(request.POST, instance=book_instance)
        form.fields['book'].disabled = True
        form.fields['imprint'].disabled = True
        if form.is_valid():
            form.save()
            return redirect('library:bookinstance-detail', pk=book_instance.pk)
    else:
        book_instance = BookInstance.objects.get(pk=pk)
        book_status = list(BookInstance.LOAN_STATUS)
        form = BookInstanceForm(instance=book_instance)
        form.fields['book'].disabled = True
        form.fields['imprint'].disabled = True
        context = {
            'bookinstance': book_instance,
            'book_status': book_status,
            'form': form,
        }
        return render(request, 'library/bookinstance_update.html', context )

def bookinstance_detail(request, pk):
    if request.method == 'POST':
        book_instance_status = request.POST.get('book_instance_status')
        book_instance = BookInstance.objects.get(pk=pk)
        book_instance.status = book_instance_status
        book_instance.save()
        return redirect('library:bookinstance-detail', pk=pk)
    
    book_instance = BookInstance.objects.get(pk=pk)
    book_status = list(BookInstance.LOAN_STATUS)
    context = {
        'bookinstance': book_instance,
        'book_status': book_status,
    }
    return render(request, 'library/bookinstance_detail.html', context)

def bookinstance_delete(request, pk):
    book_instance = BookInstance.objects.get(pk=pk)
    book_instance.delete()
    return redirect('library:bookinstances')

def bookinstance_available(request):
    book_instance = BookInstance.objects.filter(status__exact='a').select_related('book')
    
    paginator = Paginator(book_instance, 10)
    page = request.GET.get('page')
    book_instances = paginator.get_page(page)
    
    context = {
        'page_obj': book_instances,
    }
    
    return render(request, 'library/bookinstance_list.html', context)
