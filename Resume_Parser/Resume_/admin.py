from django.contrib import admin
from . import models
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['Name','Contact_Details','Degree','Experience','Skills','resume_file']
    search_fields = ('Skills','Name',)
    list_editable = ('Skills',)
    list_per_page = 10

    fieldsets = (
        ("Basic Details",{
            "fields":(
                'Name','Email','Phone_number'
            ),
        }),
        ("Education Details",{
            "fields":(
                'Degree','Experience','Skills',
            ),
        }),
         ("Additional Details",{
            "fields":(
                'Applyfor','additional_info','additional_link','resume_file'
            ),
        }),

    )
    
    # def custom_name_link(self, obj):
    #     url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name),  args=[obj.pk] )
    #     return format_html('<a href="{}">{}</a>', url, obj.Name)

    # custom_name_link.admin_order_field = 'Name'  # Make 'Name' clickable for sorting
    # custom_name_link.short_description = 'Name' 
   
   
   
   
   
    def Skills(self, obj): 
      return format_html(f'<span style="width: 10px;">{obj.content[0:100]}</span>')
    
    class Media:
        css = {
            'all': ('static/css/custom_admin.css',)
        }
    
admin.site.register(models.Candidate,CandidateAdmin)





# ,'Applyfor','additional_info','additional_link'
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id','upload_resume']
admin.site.register(models.Resume,ResumeAdmin)
