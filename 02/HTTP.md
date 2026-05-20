# HTTP (HyperText Transfer Protocol)
> 클라이언트와 서버가 데이터를 주고받기 위해 사용하는 통신 규약
- HTTPS : HTTP 웨에 TLS(SSL) 암호화를 적용한 프로토콜 

특징
- Stateless : 각 요청은 독립적으로 서버가 이전 요청을 기억하지 않음

# HTTP Message
구성
- StartLine 
    - 요청의 경우 : HTTP Version, Path, Method 
    - 응답의 경우 : HTTP Version, Status Code, Status Message
- Header : 요청이나 응답에 대한 부가 정보를 담는 영역
- 빈 줄 : Header와 Body를 구분하기 위해 사용
- Body : json, HTML 형태

Header 종류
- General Header : 요청과 응답에 모두 쓰이는 헤더
- Request Header : 클라이언트가 서버에 요청을 보낼 때 사용.
    - Host : 요청을 보낼 서버 주소
    - User-Agent : 클라이언트(브라우저, 앱) 정보
    - Accept : 클라이언트가 받을 수 있는 데이터 형식
    - Authorization : 인증 정보 전달
    - Accept-Language : 선호 언어 정보
    - Accept-Encoding : 지원 가능한 압축 방식
    - Referrer-Policy : 이전 URL 정보 전송 정책 설정
    - Cookie : 클라이언트 쿠기 전달
- Response Header
    - age : 캐시된 응답이 생성된 후 지난 시간
    - Content-Type : Body의 형태
        - application/json
        - text/html
        - multipart/form-data : 파일 업로드시 주로 사용
    - Connection : 연결 유지 여부
    - Server : 서버 소프트웨어 정보
    - Content-Length : Body 데이터 크기
    - Set-Cookie : 서버가 쿠기 저장 요청

# HTTP Method
> 리소스를 조회, 삽입, 수정, 삭제할 지 표현
- GET : 리소스 조회
- POST : 서버에 새로운 리소스를 생성하거나 처리를 요청
- PUT : 리소스를 전체 수정하거나 없으면 새로 생성
- PATCH : 리소스의 일부 필드를 수정
- DELETE : 리소스 삭제

# HTTP URL
- 구성
    - Scheme : http, https, ftp 등 어떤 프로토콜을 사용하는지 표현
    - domain : 서버의 주소. 도메인 이름이나 IP를 쓰기도 한다
    - port : 운영 체제에서 특정 서비스나 프로세스를 식별하기 위해 사용
        ex. http : 80, https : 443, ssh : 22
    - path : 리소스의 경로를 표현
    - query : 추가 정보를 표현
    
## Path variable
- URL 경로에 값을 포함해서 특정 리소스를 식별하는 방식
    ex. /users/1

## Query string
- URL 뒤에 추가적인 조건이나 옵션 데이터를 키-값 형태로 전달하는 방식
    ex. /users?page=1&size=20


# HTTP Status code
- 1XX : Information
- 200 OK : Success
    - 201 Created : 요청이 성공적으로 완료되어 새로운 리소스가 생성됨
    - 202 Accepted : 요청은 접수됐지만 서버가 아직 작업중
    - 204 No Content : 요청이 성공적으로 완료되었고 반환할 데이터 없음
- 3XX : Redirect
- 4XX : Client Error
    - 401 Unauthorized : 인증(Authentication) 실패
    - 403 Forbidden : 인가(Authorization) 실패
    - 404 Not Found : 리소스를 찾을 수 없음
    - 422 Unprocessable Content: 요청 형식은 맞지만 데이터 검증(validation) 실패
    - 429 Too Many Requests : 요청이 너무 많음
- 5XX : Server Error
    - 501 Not Implemented : 서버가 해당 기능을 지원하지 않음 
    - 503 Service Unavailable: 서버가 일시적으로 요청 처리 불가능 

