from django.shortcuts import render, HttpResponse, redirect
from .forms import UserRegistrationForm
from .models import UserRegistrationModel,UserImagePredictinModel
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .utility.GetImageStressDetection import ImageExpressionDetect
from .utility.MyClassifier import KNNclassifier
from subprocess import Popen, PIPE
import subprocess
from .decorators import user_login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Create your views here.


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


@csrf_protect
@never_cache
def UserLoginCheck(request):
    if request.session.get('loginid'):
        return redirect('UserHome')
        
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            if status == "activated":
                request.session['loginid'] = check.loginid
                request.session['loggeduser'] = check.name
                request.session['email'] = check.email
                response = redirect('UserHome')
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response
            else:
                messages.error(request, 'Your Account Not Activated')
        except Exception as e:
            print('Exception is ', str(e))
            messages.error(request, 'Invalid Login id and password')
    
    response = render(request, 'UserLogin.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@user_login_required
@never_cache
def UserHome(request):
    return render(request, 'users/UserHome.html', {})

@user_login_required
@never_cache
def UploadImageForm(request):
    if request.session.get('loginid'):
        loginid = request.session['loginid']
        data = UserImagePredictinModel.objects.filter(loginid=loginid)
        return render(request, 'users/UserImageUploadForm.html', {'data': data})
    else:
        messages.error(request, 'Please login to upload images')
        return redirect('UserLogin')

@user_login_required
@never_cache
def UploadImageAction(request):
    if request.method == 'POST' and request.session.get('loginid'):
        try:
            if 'file' not in request.FILES:
                messages.error(request, 'Please select an image to upload')
                return redirect('UploadImageForm')

            uploaded_file = request.FILES['file']
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if uploaded_file.content_type not in allowed_types:
                messages.error(request, 'Please upload a valid image file (JPEG, PNG, or GIF)')
                return redirect('UploadImageForm')
            
            # Validate file size (max 5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, 'Image size should be less than 5MB')
                return redirect('UploadImageForm')

            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)
            
            obj = ImageExpressionDetect()
            emotion = obj.getExpression(filename)
            
            loginid = request.session['loginid']
            username = request.session['loggeduser']
            email = request.session['email']
            
            UserImagePredictinModel.objects.create(
                username=username,
                email=email,
                loginid=loginid,
                filename=filename,
                emotions=emotion,
                file=uploaded_file_url
            )
            
            messages.success(request, 'Image uploaded and analyzed successfully')
            
        except Exception as e:
            messages.error(request, f'Error processing image: {str(e)}')
            
        return redirect('UploadImageForm')
        
    else:
        messages.error(request, 'Invalid request or user not logged in')
        return redirect('UserLogin')

def UserEmotionsDetect(request):
    if request.method=='GET':
        imgname = request.GET.get('imgname')
        obj = ImageExpressionDetect()
        emotion = obj.getExpression(imgname)
        loginid = request.session['loginid']
        data = UserImagePredictinModel.objects.filter(loginid=loginid)
        return render(request, 'users/UserImageUploadForm.html', {'data': data})

def UserLiveCameDetect(request):
    obj = ImageExpressionDetect()
    obj.getLiveDetect()
    return render(request, 'users/UserLiveHome.html', {})

def UserKerasModel(request):
    # p = Popen(["python", "kerasmodel.py --mode display"], cwd='StressDetection', stdout=PIPE, stderr=PIPE)
    # out, err = p.communicate()
    subprocess.call("python kerasmodel.py --mode display")
    return render(request, 'users/UserLiveHome.html', {})

def UserKnnResults(request):
    obj = KNNclassifier()
    df,accuracy,classificationerror,sensitivity,Specificity,fsp,precision = obj.getKnnResults()
    df.rename(columns={'Target': 'Target', 'ECG(mV)': 'Time pressure', 'EMG(mV)': 'Interruption', 'Foot GSR(mV)': 'Stress', 'Hand GSR(mV)': 'Physical Demand', 'HR(bpm)': 'Performance', 'RESP(mV)': 'Frustration', }, inplace=True)
    data = df.to_html()
    return render(request,'users/UserKnnResults.html',{'data':data,'accuracy':accuracy,'classificationerror':classificationerror,
                                                       'sensitivity':sensitivity,"Specificity":Specificity,'fsp':fsp,'precision':precision})
