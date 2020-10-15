# Yally-Back-End_python

## 기능

### USER
- 회원가입     
POST /user

- 로그인     
POST /user/auth

- 회원가입 이메일 인증 코드 전송    
POST /user/auth-code/email

- 인증 코드 검사
POST /user/auth-code

- 비밀번호 초기화 이메일 인증 코드 전송    
POST /user/reset-code/email

- 비밀번호 초기화  
PUT /user/auth/password

- 리스닝 하기, 취소:   
POST /user/listening (JWT)  
DELETE /user/listening (JWT)

### 타임라인
- `<email>` 이 작성한 글 타임라인    
GET /profile/timeline/<email>/<int:page>

### 검색
- 사용자 검색 결과     
GET  /search/user/<userNickname>/<int:page> (JWT)