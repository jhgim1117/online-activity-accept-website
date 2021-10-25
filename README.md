# 온라인 활승 프로젝트
## 개요
* 겉으로 보기에 세 부분으로 나뉨
  * 신청
  * 승인
  * 확인
  * 관리
* 내부적으로 보기에는 아래와 같은 과정을 거쳐야 함.
  * 신청 → 처리 → DB(신청 내역)
    *  처리: 암호화 및 블록체인 등 보안
  * 승인 화면 ← 처리 ← DB(신청 내역)
    *  처리: 복호화 등
  * 승인 여부 → 처리 → DB(승인 내역)
    *  처리: 암호화 및 블록체인 등 보안
  * 확인 ← 처리 ← DB(신청 내역&승인 내역)
    *  처리: 복호화 등
  * 관리 내용 → 처리 → DB(유저 목록 등)
* DB 구조
  1. 유저 목록
  2. 신청 내역
  3. 승인 내역
  4. 가입 및 접속 기록
* 역할 분담
  * 신청 받기(신청 화면, 신청 후 DB까지) - 태원
  * 승인 받기(승인 화면, 승인 후 DB까지) - 병도
  * 확인(DB로부터 데이터 가져와 표시, 형식 다양하게) - 승헌
  * 유저 관리(가입, 로그인 등) - 시환.
  * 관리자 화면(유저 목록, 접속 등) - 민재

## 프로젝트 관련 공지 및 안내
모두 학생회 카페 전자활승 프로젝트 게시판에서 이루어질 예정이니 아래 링크를 이용하십시오.
https://cafe.naver.com/kndlunion
