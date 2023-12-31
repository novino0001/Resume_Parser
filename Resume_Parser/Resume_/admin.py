from django.contrib import admin
from . import models
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['Name','Contact_Details','Degree','Experience','Skills','resume_file']
    search_fields = ('Skills','Name','Experience')
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
         ("Documents",{
            "fields":(
                'resume_file',
            ),
        }),

    )

    #  use for heading in path Home › Resume_ › Candidates  › Username  = change candidate
    def change_view(self, request, object_id, form_url='', extra_context = None):
        obj = self.get_object(request, object_id)
        context = {
            **self.admin_site.each_context(request),
            'title': f'Change {obj.user.username} Data' if obj else 'Change Candidate'
        }
        return super().change_view(
            request, object_id, form_url, extra_context=context
        )
    
  
   
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
