from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import UserRegistrationModel,UserImagePredictinModel
from .utility.AlgorithmExecutions import KNNclassifier
from users.utility.GetImageStressDetection import ImageExpressionDetect
from users.decorators import admin_login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Create your views here.

@csrf_protect
@never_cache
def AdminLoginCheck(request):
    if request.session.get('admin_logged_in'):
        return redirect('AdminHome')
        
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        if usrid == 'admin' and pswd == 'admin':
            request.session['admin_logged_in'] = True
            response = redirect('AdminHome')
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
        elif usrid == 'Admin' and pswd == 'Admin':
            request.session['admin_logged_in'] = True
            response = redirect('AdminHome')
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
        else:
            messages.error(request, 'Please Check Your Login Details')
    
    response = render(request, 'AdminLogin.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@admin_login_required
@never_cache
def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


@admin_login_required
@never_cache
def ViewRegisteredUsers(request):
    data = UserRegistrationModel.objects.all().order_by('-id')
    return render(request, 'admins/RegisteredUsers.html', {'data': data})


@admin_login_required
@never_cache
def AdminActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/RegisteredUsers.html', {'data': data})


@admin_login_required
@never_cache
def AdminStressDetected(request):
    data = UserImagePredictinModel.objects.all()
    return render(request, 'admins/AllUsersStressView.html', {'data': data})


@admin_login_required
@never_cache
def AdminKNNResults(request):
    obj = KNNclassifier()
    df, accuracy, classificationerror, sensitivity, Specificity, fsp, precision = obj.getKnnResults()
    df.rename(
        columns={'Target': 'Target', 'ECG(mV)': 'Time pressure', 'EMG(mV)': 'Interruption', 'Foot GSR(mV)': 'Stress',
                 'Hand GSR(mV)': 'Physical Demand', 'HR(bpm)': 'Performance', 'RESP(mV)': 'Frustration', },
        inplace=True)
    data = df.to_html()
    return render(request, 'admins/AdminKnnResults.html',
                  {'data': data, 'accuracy': accuracy, 'classificationerror': classificationerror,
                   'sensitivity': sensitivity, "Specificity": Specificity, 'fsp': fsp, 'precision': precision})


@admin_login_required
@never_cache
def AdminEmotionsDetect(request):
    if request.method == 'GET':
        try:
            imgname = request.GET.get('imgname')
            if not imgname:
                messages.error(request, 'No image name provided')
                return redirect('AdminStressDetected')
                
            obj = ImageExpressionDetect()
            emotion = obj.getExpression(imgname)
            data = UserImagePredictinModel.objects.all()
            return render(request, 'admins/AllUsersStressView.html', 
                        {'data': data, 'detected_emotion': emotion, 'current_image': imgname})
        except Exception as e:
            messages.error(request, f'Error detecting emotion: {str(e)}')
            return redirect('AdminStressDetected')
    return redirect('AdminStressDetected')
