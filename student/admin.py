from django.contrib import admin

from student.models import Student, Book


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'price')
    search_fields = ('title', 'author')


admin.site.register(Student, StudentAdmin)
admin.site.register(Book, BookAdmin)
