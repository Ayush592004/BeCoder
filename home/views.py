from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import json

# Create your views here.
def home(request):
    return render(request,'home/home.html')
def contact(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please Fill The Form Correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone ,content=content)
            contact.save()
            messages.success(request, "Your Message is successfully sent")
    
    return render(request,'home/contact.html')

def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if allPosts.count() == 0:
        messages.warning(request,"No Search Results Found, Please Make Changes To Your Query.")
    params = {'allPosts': allPosts, 'query': query}             
    return render(request, 'home/search.html', params)

def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
    # Basic Checks
        if len(username)<10 :
            messages.error(request, "You username should be atleast 10 characters")
            return redirect("home")
        if not username.isalnum():
            messages.error(request, "You username should only contains alphabet and numbers")
            return redirect("home")
        if pass1 != pass2 :
            messages.error(request, "You password does not match.")
            return redirect("home")

    # Code to create a user account
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname         
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your BeCoder account has been created successfully.")
        return redirect("home")
        
       
    else:
        return render(request, 'home/404.html')
def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request,user)
            messages.success(request, "Logged in Successfully")
            return redirect("home")
        else:
            messages.error(request, "Invaild Credentials, Please Try Again")
            return redirect("home")


    return render(request, 'home/404.html')

def handleLogout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("home")

    return HttpResponse("Logout")

def recaptcha(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
      # ReCaptcha Stuff
        clientKey = request.POST['g-recaptcha-response']
        secretKey = '6LcdUcAZAAAAAMCOOVfSaFv3TuGBwnFPWuR_y7iZ'
        captchaData = {'secret':secretKey, 'response':clientKey}
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['sucess']
        if verify:
            return HttpResponse('<script> alert("success"); </script>')
        else:
            return HttpResponse('<script> alert("success"); </script>')
