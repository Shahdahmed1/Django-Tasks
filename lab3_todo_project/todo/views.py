from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'todo/task_detail.html'
    context_object_name = 'task'


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todo/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'todo/user_profile.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(assigned_to=self.object)
        return context
