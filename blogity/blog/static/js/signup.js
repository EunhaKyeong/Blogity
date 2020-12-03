//email 중복체크 결과. 성공하면 true, 실패는 false.
var check_result = false;

//email값이 변경될 때마다 중복체크의 결과를 false로 바꿔서 중복체크 후에 이메일이 변경됐을 때 다시 한 번 중복체크를 하지 않고 넘어가는 오류를 방지.
function email_change() {
    check_result = false;
}

//email 중복체크를 하는 함수.
function email_check() {
    email = document.querySelector('input[name="email"]').value;
    fetch('/signup/emailcheck/'+email).then(function(response) {
        response.json().then(function(data) {
            if (data.result=='overlap') {
                check_result = false;
                window.alert('중복된 이메일이 존재합니다.');
            }
            else {
                check_result = true;
                window.alert('사용 가능한 이메일입니다.');
            }
        });
    });
}

//회원가입을 완료하기 전 이메일 중복확인 여부를 확인하는 함수.
var form = document.getElementsByClassName('form')[0];
form.addEventListener('submit', function(event){ 
    if(check_result==false){ 
        window.alert('이메일 중복체크를 해주세요'); 
        event.preventDefault(); 
    } 
});