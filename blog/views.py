from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse

from .models import Post, Comment
from .forms import CommentForm



 
# @login_required(login_url="login")
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return redirect('home')




def home(request):
    posts = Post.objects.all()
    title = 'Home Page'

    context = {}
    context['posts'] = posts
    context['title'] = title
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 4
    ordering=['-date_posted']

    # oxirgi ikkitasini qaytaradi
    #  def get_queryset(self, **kwargs):
    #      return Post.objects.order_by('-comment')

    def get_queryset(self, **kwargs):
        return Post.objects.annotate(num_comments=Count('comment')).order_by('-num_comments')


    # def get_queryset(self, **kwargs):
    #     return Post.objects.order_by('-date_posted')[:2]

    # agar context ga biror narsa qo'shib narsa jo'natmoqchi bo'lsa get_context_data ishlatiladi
    # agar kelayotgan ma'lumotni o'zgartirish uchun get_queryset ishlatiladi


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4


    # def get_queryset(self):
    #     user =  get_object_or_404(User, username=self.kwargs.get('user name'))
    #     return Post.objects.filter(author=user).order_by('-date_posted')




class PostDetailView(DetailView):
    model = Post
    form = CommentForm


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                post = self.get_object()
                user_comments = Comment.objects.filter(author=request.user, post=post)
                # user 3tadan ko'p comment yoza olmaydi bitta postga
                if len(user_comments) < 3:
                    form.instance.author = request.user
                    form.instance.post = post
                    form.save()
                return redirect('post_detail', pk=post.pk)
        return redirect('login')
 
    def get_context_data(self, **kwargs):
        post_comments = self.get_object().comment_set.all().order_by('-date')
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['post_comments'] = post_comments
        return context



class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        

def about(request):
    return render(request, 'blog/about.html')


def gotopage(request):
    page = request.GET['page']
    return redirect('/?page=' + page)


def visits(request):
    request.session['visits'] = int(request.session.get('visits', 0)) + 1
    return HttpResponse("<h1>Visits:" + str(request.session['visits']) + "</h1>")




