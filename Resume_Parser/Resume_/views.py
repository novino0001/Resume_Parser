from django.shortcuts import render,redirect,HttpResponse
from .models import *
from pyresparser import ResumeParser
import os
from docx import Document
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


 

def register(request):
    if request.method == "POST":
        data = request.POST
    
        username = data.get('username')
        password = data.get('pswd')
        email = data.get('email')
        print("---------register-------------->")
        print("---------out-------------->",username)
        print("---------out-------------->",password)
        print("---------out-------------->",email)
        
        user = request.user
          
        user = User.objects.filter(username = username , email = email  )
        if user.exists():
            messages.info(request,'username already exist')
            return redirect('/')
            

        user = User.objects.create(username =username,email = email ) 
        user.set_password(password)
        user.save() 
        messages.info(request, 'account created successfully')
        print("----------------------->",username)
        return redirect('/')
       
    
    return HttpResponse("Not found")



def login_page(request):
     
     if request.method == "POST":
        data = request.POST
         
        username = data.get('username')
        password = data.get('pswd')
        
        print("---------login-------------->")
        print("---------out-------------->",username)
        print("---------out-------------->",password)
        if not User.objects.filter(username = username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/')
        
        user = authenticate(username = username , password = password)
        # give a object if username and pswd is right
        print("=================",user)

        if user is None:
             messages.error(request,'Invalid Password')

             print("------------if----------->",username)
             print("------------if----------->",password)
             return redirect('/')
        else:
             login(request,user)
             print("----------else------------->",username)
             messages.error(request,'now you are logged in')

             return redirect('/')
             

     return HttpResponse('not found')

def logout_page(request):
    logout(request)
    return redirect("/")




def convert_decimal_to_years_months(decimal_value):
    years = int(decimal_value)
    months = int((decimal_value - years) * 12)
    return years, months

# Create your views here.
def home(request):
    context = {}
    if request.method == 'POST':
        get_file = request.FILES["filename"]
        user = request.user
        resume = Resume(upload_resume = get_file, user = request.user)
        resume.save()

        res = Resume.objects.order_by('-id')[0]        
        pdf_n = res.upload_resume.name.split('/')[1]
        print("===>", pdf_n)
        target_path = "Resume_/documents/"
        files = os.listdir(target_path)
        # latest_file = files[-1]
        
      
        file_path = os.path.join(target_path, pdf_n)
        print("file_path ---->",file_path)
        # file_path = 'Resume_/Siemens_cv.pdf'

        try:
            doc = Document()
            with open(file_path, 'r') as file:
                doc.add_paragraph(file.read())
            doc.save("text.docx")
            data = ResumeParser('text.docx').get_extracted_data()
            # print("data ------------->",data)
            # print("--------------exp---=============",data["total_experience"])  
            experience_str = ""
            if data['total_experience'] is not None:
                years, months = convert_decimal_to_years_months(data['total_experience'])
                print("------------------------",months,years)
                if years == 0 and months != 0 :
                     if months == 1:
                        experience_str = f"{months} month" 
                     else:   
                        experience_str = f"{months} months"
                elif months == 0 and years != 0:
                     if years == 1:
                         experience_str = f"{years} year"
                     else:    
                         experience_str = f"{years} years"

                elif months != 0 and years != 0:   
                   experience_str = f"{years} years {months} months" 

                elif months == 0 and years == 0:
                     experience_str = "fresher"
                data['total_experience'] = experience_str
 
          
          
            if data['degree'] == None:
                data['degree'] = ''
            if data['name'] == None:
                data['name'] = 'not accessiable'
            if data['email'] == None:
                data['email'] = 'not accessiable'
            if data['skills'] == None:
                data['skills'] = 'not accessiable'
            if data['mobile_number'] == None:
                data['mobile_number'] = 'not accessiable' 
             

            print("----------------exp-=============",data["total_experience"])  

            degrees = ', '.join(data['degree'])    
            skills = ', '.join(data['skills'])    
            Candidate.objects.create(Name = data['name'],Email = data['email'],Phone_number = data['mobile_number'],Degree = degrees , Skills = skills ,Experience = data['total_experience'], user = request.user,resume_file = get_file)
            return  redirect("/next/")
 
        except:
            data = ResumeParser(file_path).get_extracted_data()
            print("--------------exp---=============",data["total_experience"])  
            experience_str = ""
            if data['total_experience'] is not None:
                years, months = convert_decimal_to_years_months(data['total_experience'])
                print("------------------------",months,years)
                if years == 0 and months != 0 :
                     if months == 1:
                        experience_str = f"{months} month" 
                     else:   
                        experience_str = f"{months} months"
                elif months == 0 and years != 0:
                     if years == 1:
                         experience_str = f"{years} year"
                     else:    
                         experience_str = f"{years} years"

                elif months != 0 and years != 0:   
                   experience_str = f"{years} years {months} months"

                elif months == 0 and years == 0:
                     experience_str = "fresher"
                data['total_experience'] = experience_str
              
 
  

            if data['degree'] == None:
                data['degree'] = ''
            if data['name'] == None:
                data['name'] = 'not accessiable'
            if data['email'] == None:
                data['email'] = 'not accessiable'
            if data['skills'] == None:
                data['skills'] = 'not accessiable'
            if data['mobile_number'] == None:
                data['mobile_number'] = 'not accessiable' 
               

            degrees = ', '.join(data['degree'])   
            skills = ', '.join(data['skills'])    
            print("--------------exp---=============",data["total_experience"])    
# redirect(f"/update_transition/{queryset.id}/")
            
            Candidate.objects.create(Name = data['name'],Email = data['email'],Phone_number = data['mobile_number'],Degree = degrees , Skills = skills ,Experience = data['total_experience'], user = request.user, resume_file = get_file)
            
            return redirect("/next/")
    return render(request,'candidate.html',context)


def nextpage(request):
    queryset = Candidate.objects.order_by('-user_id').first()
    # print("----------id-------",id)
    # queryset2 = Resume.objects.get(id=id)
    print("------------",queryset)
    # print(queryset)
    if request.method == 'POST':
        data = request.POST
        name = data.get('user_name')
        email = data.get('user_email')
        phone_number = data.get('phone')
        degree = data.get('degree')
        exp = data.get('user_exp')
        skill = data.get('user_skill')
        applyfor = data.get('apply_for')
        Additional_info = data.get('Additional_info')
        Additional_link = data.get('Additional_link')

        # candidate = Candidate.objects.create(Applyfor = applyfor , 
        #                                      Name = name,
        #                                      Email = email,
        #                                      Phone_number = phone_number,
        #                                      Degree = degree,
        #                                      Skills = skill
        #                                      additional_info = Additional_info , additional_link = Additional_link,user=request.user)
        # candidate.save()

        queryset.Name = name
        queryset.Email = email
        queryset.Phone_number = phone_number
        queryset.Degree = degree
        queryset.Experience = exp
        queryset.Skills = skill
        queryset.Applyfor = applyfor
        queryset.additional_info = Additional_info
        queryset.additional_link = Additional_link
        queryset.save()
        return redirect("/")
    
    
   

    print('queryset---------------------',queryset)
    print('queryset---------------------',queryset.Email)
    print('queryset---------------------',queryset.Phone_number)

    return render(request,'demo.html',{'queryset':queryset}) 

