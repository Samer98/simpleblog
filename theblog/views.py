from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post, Category, Comment, Message
from .forms import PostForm, EditPostForm, CommentForm, SendMessageForm
from django.urls import reverse_lazy , reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.

# def home(request):
#     return render(request,'home.html',{})


def LikeView(request,pk):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return  HttpResponseRedirect(reverse('article-detail',args=[str(pk)]))
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView,self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request,'category_list.html',{'cat_menu_list':cat_menu_list})



class ArticleDetailView(DetailView,CreateView):
    model = Post
    template_name = 'article_details.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        if self.request.user.username == "":
            form.instance.name = "Guest"
        else:
            form.instance.name = self.request.user.username
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post,id=self.kwargs['pk'])

        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context['liked'] = liked
        context['comments'] = stuff.comments.all().order_by('-date_added')

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("article-detail", kwargs={'pk': pk})



class AddPostView(CreateView):
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm
    # fields = '__all__'

class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    form_class = CommentForm

    def form_valid(self,form):
        form.instance.post_id = self.kwargs['pk']
        if self.request.user.username == "":
            form.instance.name = "Guest"
        else:
            form.instance.name = self.request.user.username
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("article-detail", kwargs={'pk': pk})

class SendMessageView(CreateView):
    model = Message
    template_name = 'send_message.html'
    form_class = SendMessageForm

    def form_valid(self, form):
        # print(Post.objects.filter(id=self.kwargs['pk'])[0].author)
        form.instance.receiver_name=Post.objects.filter(id=self.kwargs['pk'])[0].author
        form.instance.sender_name = self.request.user
        # print(get_object_or_404(User,username='samer'))
        receiver = get_object_or_404(User,username=form.instance.receiver_name)
        receiver.profile.has_new_messages = True
        receiver.profile.save()

        return super().form_valid(form)
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("article-detail", kwargs={'pk': pk})
def MessageView(request,pk):

    messages = Message.objects.filter(receiver_name_id=pk).order_by('-date_added')
    try:
        receiver = get_object_or_404(User, username=messages[0].receiver_name)
        receiver.profile.has_new_messages = False
        receiver.profile.save()
    except:
        pass

    return render(request,'message_detail.html',{'messages':messages,'receiver_id':pk})
# class MessageView(DetailView):
#     model = Message
#     template_name = 'message_detail.html'
#
#     def get_context_data(self, *args, **kwargs):
#         message = Message.objects.filter(id=2)
#         context = super(MessageView, self).get_context_data(*args, **kwargs)
#
#         context["message"] = message
#         return context

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    # form_class = PostForm
    fields = '__all__'

def CategoryView(request,cats):
    category_post = Post.objects.filter(category=cats.title().replace('-',' '))
    category = cats.title().replace('-',' ')
    return render(request,'categories.html',{'cats':category,'category_posts':category_post})

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'update_post.html'
    # fields = ['title','title_tag','body']

class DeletePostView(DeleteView):
    model = Post
    # form_class = EditPostForm
    template_name = 'delete_post.html'
    success_url =  reverse_lazy('home')

