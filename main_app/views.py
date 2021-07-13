from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Instruction, Mug, Photo
from .forms import UseForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import boto3
import uuid

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'alliecats'

# CBV functions

class MugCreate(LoginRequiredMixin, CreateView):
    model = Mug
    fields = ['name', 'material', 'origin', 'color', 'description']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MugUpdate(LoginRequiredMixin, UpdateView):
    model = Mug
    fields = ['material', 'origin', 'color', 'description']

class MugDelete(LoginRequiredMixin, DeleteView):
    model = Mug
    success_url = '/mugs/'

class InstructionList(LoginRequiredMixin, ListView):
    model = Instruction

class InstructionDetail(LoginRequiredMixin, DetailView):
    model = Instruction

class InstructionCreate(LoginRequiredMixin, CreateView):
    model = Instruction
    fields = '__all__'

class InstructionUpdate(LoginRequiredMixin, UpdateView):
    model = Instruction
    fields = ['description']

class InstructionDelete(LoginRequiredMixin, DeleteView):
    model = Instruction
    success_url = '/instructions/'

# Create your views here.

def home(request):
    return redirect('about')

def about(request):
    return render(request, 'about.html')

@login_required
def mugs_index(request):
    mugs = Mug.objects.filter(user=request.user)
    return render(request, 'mugs/index.html', { 'mugs': mugs })

@login_required
def mugs_detail(request, mug_id):
    mug = Mug.objects.get(id=mug_id)
    instructions_mug_doesnt_have = Instruction.objects.exclude(id__in = mug.instructions.all().values_list('id'))
    use_form = UseForm()
    return render(request, 'mugs/detail.html', { 
        'mug': mug,
        'use_form': use_form,
        'instructions': instructions_mug_doesnt_have
        })

@login_required
def add_use(request, mug_id):
    form = UseForm(request.POST)
    if form.is_valid():
        new_use = form.save(commit=False)
        new_use.mug_id = mug_id
        new_use.save()
    return redirect('detail', mug_id=mug_id)

@login_required
def assoc_inst(request, mug_id, instruction_id):
    Mug.objects.get(id=mug_id).instructions.add(instruction_id)
    return redirect('detail', mug_id=mug_id)

@login_required
def unassoc_inst(request, mug_id, instruction_id):
    Mug.objects.get(id=mug_id).instructions.remove(instruction_id)
    return redirect('detail', mug_id=mug_id)

@login_required
def add_photo(request, mug_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            Photo.objects.create(url=url, mug_id=mug_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', mug_id=mug_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)