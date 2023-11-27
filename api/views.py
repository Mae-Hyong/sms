import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from .sms import send_sms
from .models import Sms
from .serializers import AuthUserSerializer

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
             # Serializer에서 입력받은 원시 비밀번호를 가져옵니다.
            raw_password = serializer.validated_data.get('password')
            
            # make_password 함수를 사용하여 비밀번호를 해시화하고 저장합니다.
            hashed_password = make_password(raw_password)
            serializer.save(password=hashed_password)

            return Response({'message': '회원 가입이 완료되었습니다.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def SMS(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        auth_number = str(random.randint(100000, 999999))
        sms_content = f"[TEST]\n인증 코드는 {auth_number} 입니다."
        send_result = send_sms(phone_number, sms_content)

        if send_result:  # 인증 문자 전송에 성공한 경우에만 응답을 반환
            # SMS를 데이터베이스에 저장
            Sms.create_sms(phone_number, auth_number)
            return Response({'message': '인증 문자 전송이 완료되었습니다.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '인증 문자 전송에 실패했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)