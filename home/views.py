from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from home.models import ContactFormMessage, ContactFormu, FAQ, Setting, UserProfile
from django.contrib import messages
from blog.models import Blog, Category, Images, Comment
import json
from home.forms import SearchForm, SignUpForm
from django.contrib.auth import authenticate, login, logout

def index(request):
    current_user=request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Blog.objects.all()[:5]
    slide_resim = Blog.objects.filter(status='True').order_by('-update_at')[:1]
    news = Blog.objects.filter(type='haber', status='True').order_by('-id')[:4]
    announcement = (Blog.objects.filter(type='duyuru', status='True')|Blog.objects.filter(type='blog', status='True')).order_by('-id')[:3]
    category = Category.objects.all()
    context = {'setting': setting, 
               'page':'home', 
               'sliderdata':sliderdata,
               'category': category,
               'news': news,
               'slide_resim':slide_resim,
               'announcement': announcement, 
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'hakkimizda', 'category': category,}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'page': 'referanslar', 'category': category, }
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name'] 
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data[ 'message']
            data.save() # verirabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz ")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form, 'category': category, }
    return render(request, 'iletisim.html', context)

# def details(request):
#     setting = Setting.objects.get(pk=1)
#     context = {'setting': setting, 'page':'details'}
#     return render(request, 'details.html', context)

def category_blogs(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    blogs = Blog.objects.filter(category_id=id)
    context = {'blogs': blogs,'category': category,'categorydata': categorydata}
    return render(request, 'details.html', context)


def blog_details(request, id, slug):
    category = Category.objects.all()
    blog = Blog.objects.get(pk=id,slug=slug)
    images = Images.objects.filter(blog_id=id)
    comments= Comment.objects.filter(blog_id=id,status='True')
    context = {'category': category, 
               'blog':blog,
               'images':images,
               'comments': comments,}
    return render(request, 'blog_details.html', context)


def blog_search(request):
    if request.method == 'POST': # Chect form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] 
            blog = Blog.objects.filter(title__icontains=query)
            context = {'blog': blog,
                       'category': category,}
            return render(request, 'blog_search.html', context)
    return HttpResponseRedirect('/')

def blog_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        blog = Blog.objects.filter(title__icontains=q)
        results = []
        for rs in blog:
            blog_json = {}
            blog_json = rs.title
            results.append(blog_json)
            data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            messages.warning(request, "Login Hatasi ! kullanici adi veya Sifre yanlis")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category,}
    return render (request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get ('username')
            password = form.cleaned_data.get ('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save ()
            messages.success(request, "Hoş Geldiniz.. Sitemize başarılı bir şekilde üye oldunuz.")
            return HttpResponseRedirect('/home')

    form = SignUpForm()    
    category = Category.objects.all()
    context = {'category': category,
               'form': form,}

    return render(request, 'signup.html', context)

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {'category': category,
               'faq':faq,  
    }

    return render(request, 'faq.html', context)
