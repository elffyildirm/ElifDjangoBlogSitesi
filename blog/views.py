from django.shortcuts import render
from http.client import HTTPResponse
from blog.models import Comment, CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect

def index(request):
    return HTTPResponse("Blog Page")

# @login_required(login_url='/login')#check login
   
def addcomment(request,id):
    url = request.META.get ('HTTP_REFERER') # get last url
    if request.method == 'POST': # form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user # Access User Session information
            data = Comment() #model ile bağlantı kur
            data.user_id = current_user.id
            data.blog_id =id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data[ 'rate']
            data.ip = request.META.get('REMOTE_ADDR') # Client computer ip address
            data.save() # verirabanına kaydet
            messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz ")
            return HttpResponseRedirect(url)
            #return HttpResponse("Kaydedildi")
            messages.warning(request, "Yorumunuz Kaydedilmedi. Lutfen Kontrol Ediniz ")

        return HttpResponseRedirect(url)
