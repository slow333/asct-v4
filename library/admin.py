from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.utils.html import format_html
from django.db.models import Count
from library.models import Author, Genre, Book, BookInstance, Language

class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    exclude = ['summary']
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death', 'author_book_count')
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')]
    list_per_page = 20
    search_fields = ('last_name', 'first_name')
    inlines = [BookInline]
    
    @admin.display(ordering='author_book_count')
    def author_book_count(self, author):
        url = (reverse('admin:library_book_changelist') 
            + f'?author__id__exact={author.id}')
        return format_html(f'<a href="{url}">{author.author_book_count}</a>')
    author_book_count.short_description = 'Book Count'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            author_book_count=Count('book')
        )
    
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class LanguageUpdateForm(forms.Form):
    language = forms.ModelChoiceField(queryset=Language.objects.all(), label='Language')
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('language','genre')
    list_select_related = ('author',)
    list_per_page = 20
    inlines = [BooksInstanceInline]
    actions = ['update_language']
    
    search_fields = ('title', 'author__last_name','language__name')
    autocomplete_fields = ('author','language',)
    
    # m2m field에 대하 추가 쿼리 방지(사전에 join을 수행)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('genre')

    # 이해가 안됨
    def update_language(self, request, queryset):
        if 'apply' in request.POST:
            form = LanguageUpdateForm(request.POST)
            if form.is_valid():
                language = form.cleaned_data['language']
                count = queryset.update(language=language)
                self.message_user(request, f"{count} books updated to {language}.")
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = LanguageUpdateForm()

        return render(request, 'library/update_language.html', {
            'objects': queryset,
            'form': form,
            'title': 'Update Language',
        })
    update_language.short_description = "Update language for selected books"

admin.site.register(Genre)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status','due_back')
    list_select_related = ('book',)
    list_per_page = 20
    search_fields = ( 'borrower',)
    autocomplete_fields = ('borrower',)

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ( 'name',)