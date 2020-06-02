from django.contrib import admin
from blog.models import Blog, Category, Comment, Images
from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

class BlogImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ( 'image_tag', )

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status', 'image_tag']
    readonly_fields = ( 'image_tag', )
    list_filter = ['status','category']
    inlines = [BlogImageInline]
    

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'blog', 'image_tag']
    readonly_fields = ( 'image_tag', )


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_blogs_count', 'related_blogs_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative Blog count
        qs = Category.objects.add_related_count(
                qs,
                Blog,
                'category',
                'blogs_cumulative_count',
                cumulative=True)

        # Add non cumulative Blog count
        qs = Category.objects.add_related_count(qs,
                 Blog,
                 'category',
                 'blogs_count',
                 cumulative=False)
        return qs

    def related_blogs_count(self, instance):
        return instance.blogs_count
    related_blogs_count.short_description = 'Related blogs (for this specific category)'

    def related_blogs_cumulative_count(self, instance):
        return instance.blogs_cumulative_count
    related_blogs_cumulative_count.short_description = 'Related blogs (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'blog', 'user','status']
    list_filter = ['status']

admin.site.register(Category, CategoryAdmin2)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register (Comment, CommentAdmin)

