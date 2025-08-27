from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserProfileSerializer
from apps.apis.models import Api

User = get_user_model()

# Simple logout function
def logout_view(request):
    logout(request)
    return redirect('home')

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_apis'] = Api.objects.order_by('-created_at')[:6]
        context['total_apis'] = Api.objects.count()
        return context

# Template Views
class LoginTemplateView(TemplateView):
    template_name = 'accounts/login.html'

class RegisterTemplateView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Basic validation
        if not all([username, email, password, password_confirm]):
            context = {'error': 'Tüm zorunlu alanları doldurunuz.'}
            return render(request, self.template_name, context)
        
        if password != password_confirm:
            context = {'error': 'Şifreler eşleşmiyor.'}
            return render(request, self.template_name, context)
        
        if User.objects.filter(username=username).exists():
            context = {'error': 'Bu kullanıcı adı zaten kullanılıyor.'}
            return render(request, self.template_name, context)
        
        if User.objects.filter(email=email).exists():
            context = {'error': 'Bu email zaten kullanılıyor.'}
            return render(request, self.template_name, context)
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('home')
        except Exception as e:
            context = {'error': f'Kayıt sırasında hata oluştu: {str(e)}'}
            return render(request, self.template_name, context)

class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_apis'] = Api.objects.filter(user=self.request.user)
        return context

class LogoutTemplateView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
    def post(self, request):
        logout(request)
        return redirect('home')

# API Views (REST)
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'})
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)