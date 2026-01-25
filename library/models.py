from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from datetime import date

class Genre(models.Model):
    name = models.CharField(
        max_length=200, 
        help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(
        max_length=200, 
        help_text="Enter the book's natural language (e.g. Korean, English, French etc.)")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Book(models.Model):
    title = models.CharField(max_length=200, 
        help_text='책 제목', verbose_name='책 제목')
    summary = models.TextField(
        max_length=1000, 
        help_text='Enter a brief description of the book',
        verbose_name='책 요약')
    isbn = models.CharField('ISBN', 
        max_length=15, 
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # author에서 book을 생성
    author = models.ForeignKey('Author', 
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='저자')
    genre = models.ManyToManyField(Genre, verbose_name='책분류')
    language = models.ForeignKey(
        'Language', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        verbose_name='언어')
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = '분야'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)]) # type: ignore

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'author']

class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    imprint = models.CharField(
        max_length=200,
        help_text='출판사')
    due_back = models.DateField(null=True, blank=True,
                                help_text='대출 만료일')

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
        max_length=1,
        #Django는 모델 필드에 choices 인자가 설정되어 있으면, 해당 필드의 "사람이 읽을 수 있는 이름(label)"을 반환하는 메서드를 자동으로 추가합니다. 이 메서드의 이름 규칙은 get_필드명_display()입니다. get_status_display
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
    
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.book.title} {self.status}' # pyright: ignore
    
    def get_absolute_url(self):
        return reverse("bookinstance-detail", kwargs={"pk": self.pk})

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Birthday',null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    # book에서 foreign key를 생성해서 book으로 조회 가능

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)]) # type: ignore

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['last_name', 'first_name']

