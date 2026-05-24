# 회고
## API 명세서 만들기
API 명세서를 적으면서 특정 게시글의 댓글 목록을 조회하는 api를 어떻게 설계할 지 고민되었다.
api들을 post, comment 별로 나눴는데 게시글에 대한 댓글을 조회하니까 post에 넣을지, 댓글을 조회하니까 comment에 넣을지 고민이었다. 
post에 넣는다면 endpoint는 /posts/{post_id}/comments,
comment에 넣는다면 endpoint는 /comments?post_id={post_id}.
고민해본 결과 post_id는 필수이고 게시글에 대한 댓글이므로 게시글에 초첨을 맞춰서 설계하였다. 

## 구조 개선하기
처음에는 Router - Controller - Service - Repository 로 나누어서 구현했다. Service는 비즈니스 로직, Repository는 데이터베이스 접근이므로 둘은 나누는게 좋을 것 같았다.
하지만 개발하다보니 의미없는 중간단계만 늘어난 느낌이었다. 그래서 Controller는 제외하였다. 
그리고 고민이었던 건 도메인 주도 개발처럼 post 안에 PostRouter, PostService, PostRepository를 넣는 방식이 좋을지 
지금처럼 routers, services, repositories로 나누는 방식이 좋을지 고민이었다. 
그런데 ai service를 넣을 경우 분류를 어떻게 할지 모호하기도 해서 계층 분류로 개발을 했다.

## 추후 개선사항
전체적으로 예외 처리가 빠진 곳들이 있어 추가해야할 것 같다. 
유저 관련해서도 비밀번호를 평문 그대로 db에 저장하는데 보안을 위해 암호화를 적용해야할 것 같고, 인증, 인가 로직이 전혀 없는데 나중에 추가해야할 것 같다.
그리고 게시글 작성이나 댓글 작성시 user_id를 body로 보내는데 나중에는 토큰에서 추출하는 방식을 적용해도 좋을 것 같다.
