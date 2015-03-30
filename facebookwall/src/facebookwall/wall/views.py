from wall.models import Status, Likes
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from wall.forms import StatusForm, PostStatusForm, PostReplyForm
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
import json

# Create your views here.


def class_view_decorator(function_decorator):
    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View
    return simple_decorator


class DeleteStatus(generic.View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            get = request.GET
            status = get_object_or_404(Status, pk=get['pk'])
            status.delete()
            response_data = {
                'result': 'success'
            }
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


class LikeStatus(generic.View):
    def get(self, request, *args, **kwargs):
        get = request.GET
        status = get_object_or_404(Status, pk=get['pk'])
        like = Likes.objects.filter(liked_status=status, liker=request.user)
        response_data = {}
        print like
        if like:
            like.delete()
            response_data['result'] = "Like"
        else:
            like = Likes(liked_status=status, liker=request.user)
            like.save()
            response_data['result'] = "Unlike"

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

# def like_status(request):
#     post = request.POST
#     user = request.user
#     status = get_object_or_404(Status, pk=post['status_id'])
#     like = Likes(liked_status=status, liker=user)
#     like.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class StatusUpdateView(generic.UpdateView):
    model = Status
    fields = ['message']
    form_class = StatusForm
    template_name = 'wall/update-form.html'

    def form_valid(self, form):
        self.object = form.save()
        response_data = {}
        response_data['result'] = 'Edit saved'
        response_data['message'] = form.data['message']
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


@class_view_decorator(login_required)
class IndexView(generic.ListView, FormMixin):
    model = Status
    template_name = 'wall/index.html'
    context_object_name = 'latest_wall_updates'
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        self.form = PostStatusForm(self.request.user, self.request.POST)
        if self.form.is_valid():
            status = self.form.save()

        # return self.get(request, *args, **kwargs)
        return HttpResponseRedirect('/wall/status_detail/'+str(status.id))

    def get_queryset(self):
        return Status.objects.exclude(
                    in_reply_to__isnull=False
                ).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = self.request.user.get_username()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        return context


class MyIndexView(IndexView):
    form_class = StatusForm
    model = Status


@class_view_decorator(login_required)
class DetailView(generic.DetailView, FormMixin):
    model = Status
    template_name = 'wall/detail.html'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        self.object = self.get_object()

        context = self.get_context_data(form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.form = PostReplyForm(self.request.user,
                                  kwargs['pk'],
                                  self.request.POST)
        if self.form.is_valid():
            self.form.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user

        return context


class MyDetailView(DetailView):
    form_class = StatusForm
    model = Status


class ReplyView(generic.ListView):
    model = Status
    template_name = 'wall/reply.html'
    context_object_name = 'replies'
    # paginate_by = 2

    def get_queryset(self):
        return Status.objects.filter(
                    in_reply_to=self.request_pk
                ).order_by('pub_date')  # [:2]

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            self.request_pk = request.POST['pk']
            return super(ReplyView, self).get(request, *args, **kwargs)


class ReplyFromIndexView(generic.CreateView):
    form_class = StatusForm
    template_name = 'wall/reply-wall.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            self.form = PostReplyForm(self.request.user,
                                      self.request.POST['status_id'],
                                      self.request.POST)
            if self.form.is_valid():
                status = self.form.save()

            return HttpResponseRedirect('/wall/reply_detail/'+str(status.id))

    def get_context_data(self, **kwargs):
        context = super(ReplyFromIndexView, self).get_context_data(**kwargs)
        context['reply_to'] = self.request.GET['in_reply_to']

        return context


class ReplyDetail(generic.DetailView):
    model = Status
    template_name = 'wall/reply-single.html'

    def get_context_data(self, **kwargs):
        context = super(ReplyDetail, self).get_context_data(**kwargs)
        context['user'] = self.request.user

        return context


class StatusDetail(generic.DetailView):
    model = Status
    template_name = 'wall/status-single.html'

    def get_context_data(self, **kwargs):
        context = super(StatusDetail, self).get_context_data(**kwargs)
        context['user'] = self.request.user

        return context
