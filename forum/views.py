from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Message, User

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect(reverse('logging'))

@csrf_exempt
def logging(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                context = {
                    "wrong": True,
                }
                return render(request, 'logging.html', context)
        else:
            return render(request, 'logging.html')

def loggingout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def clean_string(string):
    string = string.replace("[b]", "<b>") 
    string = string.replace("[/b]", "</b>")
    string = string.replace("[u]", "<u>") 
    string = string.replace("[/u]", "</u>")
    string = string.replace("[center]", "<center>")
    string = string.replace("[/center]", "</center>")
    string = string.replace("[hr]", "<hr/>")
    string = string.replace("<script>", "")
    string = string.replace("</script>", "")
    return string

@csrf_exempt
def subforum(request, category):
    if request.user.is_authenticated:
        if category < 0 or category > 3:
            return HttpResponseRedirect(reverse('index'))
        else:
            pinned_posts = Post.objects.filter(category=category, pinned=True).order_by('-pk')
            posts = Post.objects.filter(category=category, pinned=False).order_by('-pk')
            context = {
                "category": category,
                "pinned_posts": pinned_posts,
                "posts": posts,
            }
            if request.method == "POST":
                caption = request.POST["caption"]
                caption = clean_string(caption)
                message = request.POST["message"]
                message = clean_string(message)
                pinned = request.POST.get("pinned", False)

                # We save the post.
                if pinned == "yes":
                    new_post = Post(caption=caption, category=category, pinned=True)
                else:
                    new_post = Post(caption=caption, category=category, pinned=False)
                new_post.save()

                # We save the message.
                new_message = Message(post=new_post, text=message, author=request.user)
                new_message.save()
            return render(request, 'subforum.html', context)
    else:
        return HttpResponseRedirect(reverse('logging'))

@csrf_exempt
def reading(request, id):
    if request.user.is_authenticated:
        messages = Message.objects.filter(post=id).order_by('pk')
        post = Post.objects.get(pk=id)
        #first_message = post.find_first_message(id)
        context = {
            'messages': messages,
            'post': post,
            'id_post': id,
        }
        if request.method == "POST":
            text = request.POST["text"]
            text = clean_string(text)
            new_message = Message(post=post, text=text, author=request.user)
            new_message.save()
        return render(request, 'reading.html', context)
    else:
        return HttpResponseRedirect(reverse('logging'))

@csrf_exempt
def editing(request, id):
    if request.user.is_authenticated:
        message = Message.objects.get(pk=id)
        # Filter of mistakes.
        if message == None:
            return HttpResponseRedirect(reverse('index'))
        if message.author != request.user:
            return HttpResponseRedirect(reverse('index'))
        #-----
        context = {
            'message': message
        }
        if request.method == "POST":
            new_text = request.POST["text"]
            new_text = clean_string(new_text)
            message.text = new_text
            message.save()
            return HttpResponseRedirect(reverse('reading', args=(message.post.pk,)))
        return render(request, 'editing.html', context)
    else:
        return HttpResponseRedirect(reverse('logging'))

def deleting(request, id):
    if request.user.is_authenticated:
        message = Message.objects.get(pk=id)
        post = Post.objects.get(pk=message.post.pk)
        post_category = post.category
        # Filter of mistakes.
        if message == None:
            return HttpResponseRedirect(reverse('index'))
        #-----
        post_id = message.post.pk
        if message.author == request.user:
            message.delete()
        # We check if it was the post main message.
        messages = Message.objects.filter(post=post.pk)
        if not messages:
            post.delete()
            return HttpResponseRedirect(reverse('subforum', args=(post_category,)))

        return HttpResponseRedirect(reverse('reading', args=(post_id,)))
    else:
        return HttpResponseRedirect(reverse('logging'))

def profile(request, id):
    if request.user.is_authenticated:
        user_profile = User.objects.get(pk=id)
        amount = Message.count_messages(user_profile)
        context = {
            'user': user_profile,
            'amount': amount,
        }
        return render(request, 'profile.html', context)
    else:
        return HttpResponseRedirect(reverse('logging'))
