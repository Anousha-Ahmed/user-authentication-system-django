from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SignUp, StudentDetails
from .serializers import SignUpSerializer, LoginSerializer, StudentDetailsSerializer
from django.core.mail import send_mail
from django.conf import settings
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def is_authenticated(request):
    return request.session.get('is_authenticated', False)

class CustomPermissions:
    def has_permission(self, request, view):
        if request.session.get('is_authenticated'):
            return True
        return False

class StudentDetailsView(APIView):
    permission_classes = [CustomPermissions]
    
    def get(self, request, pk=None):
        if pk is not None:
            try:
                student = StudentDetails.objects.get(pk=pk)
                serializer = StudentDetailsSerializer(student)
                return Response(serializer.data)
            except StudentDetails.DoesNotExist:
                return Response({"error": "Student not found"}, status=404)
        else:
            students = StudentDetails.objects.all()
            serializer = StudentDetailsSerializer(students, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = StudentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        try:
            student = StudentDetails.objects.get(pk=pk)
        except StudentDetails.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)
        
        serializer = StudentDetailsSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            student = StudentDetails.objects.get(pk=pk)
            student.delete()
            return Response({"message": "Student deleted successfully"}, status=200)
        except StudentDetails.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = generate_otp()
            user.otp = otp
            user.is_verified = False
            user.save()
            
            try:
                send_mail(
                    'Your OTP for Signup Verification',
                    f'Hello {user.userName},\n\nYour OTP for email verification is: {otp}\n\nThis OTP is valid for 10 minutes.\n\nThank you!',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email error: {e}")
            
            return Response({
                'message': 'Signup successful! Please verify OTP.',
                'userName': user.userName,
                'email': user.email
            }, status=201)
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        userName = request.data.get('userName')
        otp = request.data.get('otp')
        
        if not userName or not otp:
            return Response({"error": "Username and OTP are required"}, status=400)
        
        try:
            user = SignUp.objects.get(userName=userName)
            if user.otp == otp:
                user.is_verified = True
                user.otp = None
                user.save()
                return Response({
                    'message': 'OTP verified successfully! You can now login.'
                }, status=200)
            else:
                return Response({'error': 'Invalid OTP!'}, status=400)
        except SignUp.DoesNotExist:
            return Response({'error': 'User not found!'}, status=404)

class ResendOTPView(APIView):
    def post(self, request):
        userName = request.data.get('userName')
        
        if not userName:
            return Response({"error": "Username is required"}, status=400)
        
        try:
            user = SignUp.objects.get(userName=userName)
            if user.is_verified:
                return Response({'error': 'User is already verified!'}, status=400)
            
            otp = generate_otp()
            user.otp = otp
            user.save()
            
            send_mail(
                'Your New OTP for Signup Verification',
                f'Hello {user.userName},\n\nYour new OTP for email verification is: {otp}\n\nThank you!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            return Response({'message': 'New OTP sent successfully!'}, status=200)
        except SignUp.DoesNotExist:
            return Response({'error': 'User not found!'}, status=404)

class LoginView(APIView):
    def post(self, request):
        userName = request.data.get('userName')
        password = request.data.get('password')
        
        if not userName or not password:
            return Response({"error": "Username and Password are required"}, status=400)
        
        try:
            user = SignUp.objects.get(userName=userName)
            
            if not user.is_verified:
                return Response({'error': 'Please verify your email first using OTP!'}, status=401)
            
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['userName'] = user.userName
                request.session['is_authenticated'] = True
                return Response({
                    'message': 'Login successful!',
                    'userName': user.userName,
                    'redirect': '/api/users/dashboard/'
                }, status=200)
            else:
                return Response({'error': 'Invalid password!'}, status=400)
        except SignUp.DoesNotExist:
            return Response({'error': 'User not found!'}, status=404)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({"error": "Email required"}, status=400)
        
        try:
            user = SignUp.objects.get(email=email)
            otp = generate_otp()
            user.otp = otp
            user.save()
            
            try:
                send_mail(
                    'Password Reset OTP',
                    f'Hello {user.userName},\n\nYour OTP for password reset is: {otp}\n\nThank you!',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email error: {e}")
            
            return Response({'message': 'OTP sent to your email'}, status=200)
        except SignUp.DoesNotExist:
            return Response({'message': 'If email exists, OTP sent'}, status=200)

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        if not email or not otp or not new_password:
            return Response({"error": "Email, OTP and new_password required"}, status=400)
        
        try:
            user = SignUp.objects.get(email=email)
            
            if user.otp != otp:
                return Response({"error": "Invalid OTP"}, status=400)
            
            user.password = new_password
            user.otp = None
            user.save()
            
            return Response({'message': 'Password reset successful!'}, status=200)
        except SignUp.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UpdatePasswordView(APIView):
    def post(self, request):
        if not is_authenticated(request):
            return Response({"error": "Authentication required"}, status=401)
            
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({"error": "old_password and new_password required"}, status=400)
        
        try:
            user = SignUp.objects.get(id=request.session['user_id'])
            
            if user.password != old_password:
                return Response({"error": "Old password incorrect"}, status=400)
            
            user.password = new_password
            user.save()
            
            return Response({'message': 'Password updated successfully!'}, status=200)
        except SignUp.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class LogoutView(APIView):
    def post(self, request):
        request.session.flush()
        return Response({"message": "Logout successful"}, status=200)

class CheckSessionView(APIView):
    def get(self, request):
        if 'user_id' in request.session:
            return Response({
                'authenticated': True,
                'userName': request.session.get('userName')
            }, status=200)
        return Response({
            'authenticated': False
        }, status=401)



def signup_page(request):
    return render(request, 'signup.html')

def login_page(request):
    return render(request, 'login.html')

def verify_otp_page(request):
    return render(request, 'verify_otp.html')

def forgot_password_page(request):
    return render(request, 'forgot_password.html')

def reset_password_page(request):
    return render(request, 'reset_password.html')

def Dashboard(request):
    if 'user_id' in request.session:
        context = {'userName': request.session.get('userName')}
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/api/users/login-page/')

def students_page(request):
    if 'user_id' in request.session:
        return render(request, 'students.html')
    else:
        return redirect('/api/users/login-page/')