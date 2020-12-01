from django.conf import settings
from django.contrib.auth import login

class NaverLoginMixin:
    naver_client = NaverClient()

    def login_with_naver(self, state, code):

        #인증토큰 발급
        is_success, token_infos = self.naver_client.get_access_token(state, code)
        if not is_success:
            return False, '{} [{}]'.format(token_infos.get('error_desc'), token_infos.get('error'))

        access_token = token_infos.get('access_token')
        refresh_token = token_infos.get('refresh_token')
        expires_in = token_infos.get('expires_in')
        token_type = token_infos.get('token_type')

        #네이버 프로필 얻기
        is_success, profiles = self.get_naver_profile(access_token, token_type)
        if not is_success:
            return False, profiles

        #사용자 생성 또는 업데이트
        user, created = self.model.objects.get_or_create(email=profiles.get('email'))
        if created: #사용자 생성일 경우
            user.set_password(None)
        user.name = profiles.get('name')
        user.is_active = True
        user.save()

        #로그인
        login(self.request, user, 'user.oauth.backends.NaverBackend')   #NaverBackend를 통한 인증 시도

        #세션데이터 추가
        self.set_session(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)

        return True, user

    def get_naver_profile(self, access_token, token_type):
        is_success, profiles = self.naver_client.get_profile(access_token, token_type)

        if not is_success:
            return False, profiles

        for profile in self.required_profiles:
            if profile not in profiles:
                return False, '{}은 필수 정보입니다. 정보제공에 동의해주세요.'.format(profile)

        return True, profiles