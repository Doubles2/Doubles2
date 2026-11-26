---
name: effective-python
description: >-
  파이썬 코드를 『파이썬 코딩의 기술』(브렛 슬라킨, 개정2판, 90가지 Better Way) 규칙대로 쓰고 검토한다.
  Use when 파이썬 코드(.py, 노트북 셀, 스크립트, 데이터 처리 코드)를 새로 쓰거나 고치거나 리뷰할 때.
  Triggers: "파이썬답게", "Pythonic", "파이썬 코딩의 기술대로", "BetterWay N대로", "이 코드 리뷰해 줘"(파이썬).
  Not for: 모듈 나누기·의존 선택 같은 구조·설계 판단 → pragmatic-programmer(파이썬 코드를 쓰면서 구조도 정하면 둘 다 쓴다),
  파이썬 책 사진 정리·노션 복습 → book-study, 코드가 없는 파이썬 개념 질문에는 쓰지 않는다.
---

# 파이썬 코딩의 기술대로 코딩하기

**산출물: 요청받은 파이썬 코드(또는 리뷰 의견)와, 적용한 주요 BetterWay 2~4개를 짚은 짧은 설명. Do NOT 요청받지 않은 기존 코드를 책 규칙대로 다시 쓰지 않는다. 바꾼 줄 근처만 맞춘다.**

사용자는 이 책을 공부 중이다. 코드를 보고 "이건 BetterWay 몇 번이구나"를 알아볼 수 있게 하는 것도 목적이다.
effective-python은 "이 줄을 파이썬답게"를, pragmatic-programmer는 "이 구조가 나중에 바꾸기 쉬운가"를 맡는다.

## Step 0 — 규모 판정
- **몇 줄·함수 하나**: Step 3의 자주 틀리는 것과 `scripts/check.sh`만 거친다.
- **파일 여러 개·새 모듈·클래스 설계·동시성·테스트**: `references/better-ways.md`에서 해당 장을 읽고 전체 순서를 탄다. 구조 판단이 섞이면 pragmatic-programmer도 함께.

## Step 1 — 원칙 새로 읽기
`~/code/doubles2/principles/principles.md`를 읽고, 아래 Principles에 링크된 원칙 파일을 읽는다.
**외워 둔 내용을 쓰지 말고 매번 새로 읽는다.**

## Step 2 — 환경과 프로젝트 규칙
- 대상 파이썬 버전을 먼저 본다(`python3 --version`, `pyproject.toml`, `.python-version`). 이 Mac은 `python3` = 3.13(pyenv), `/usr/bin/python3` = 3.9. 책은 3.8 기준이다. 버전 때문에 쓸 수 없는 문법은 쓰지 않는다.
- 이미 있는 코드의 스타일·린터 설정(ruff, black, flake8)이 책과 다르면 프로젝트를 따른다. 책 규칙은 프로젝트가 정하지 않은 부분을 채운다.

## Step 3 — 쓰기
`references/better-ways.md`가 90개 규칙의 단일 기준이다. 1–3장(기본기·리스트와 딕셔너리·함수)은 거의 모든 코드에 해당하니 늘 따르고,
클래스(5–6장)·동시성(7장)·강건성(8장)·테스트(9장)·협업(10장) 코드를 쓸 때는 그 장을 읽는다.

기계가 못 잡아서 사람이 봐야 하는, **자주 틀리는 것**:
- 실패를 `None`으로 알리지 말고 예외를 던진다. 반환 타입에 `None`을 섞지 않는다. (BW20)
- 클로저 안에서 바깥 변수에 대입하면 새 지역 변수가 된다. 간단하면 `nonlocal`, 길면 작은 클래스로. (BW21)
- 값 네 개 이상을 튜플로 반환하지 않는다 → `NamedTuple`/`dataclass`. (BW19)
- 한 줄에 우겨넣은 복잡한 식은 도우미 함수로. `:=`는 읽기 쉬울 때만. (BW5, 10)
- 헷갈리는 인자는 키워드 전용(`*`)·위치 전용(`/`)으로. (BW25)
- 내장 타입을 세 단계 이상 중첩하지 말고 클래스로 나눈다. (BW37)
- 결과가 크면 리스트 대신 제너레이터, 여러 번 순회할 인자는 이터레이터 방어. (BW30, 31)

## Step 4 — 확인
1. 기계로 잡히는 규칙은 지시문 대신 스크립트로 확인한다:
   ```bash
   bash ~/code/doubles2/skills/effective-python/scripts/check.sh <파일·폴더>
   ```
   `is None`(BW2), f-문자열(BW4), enumerate(BW7), 루프 뒤 else(BW9), 가변 기본 인자(BW24), 컴프리헨션(BW27)을 ruff로 본다. 고치지는 않는다.
2. **실행해서 출력을 확인한다.** 실행할 수 없으면 실행하지 못했다고 말한다. 출력을 지어내지 않는다.
3. 공개 함수·클래스에 독스트링·타입 힌트가 있는지 본다(BW84, 90).

## Principles
- [[encode-lessons-in-structure]] — 기계가 잡는 규칙은 `scripts/check.sh`로. 지시문에는 사람 판단이 필요한 것만.
- [[prove-it-works]] — 코드를 실행해서 출력을 본다. 3.8 이후 버전 차이는 실제 버전으로 확인한다.
- [[subtract-before-you-add]] — 규칙 설명은 `references/better-ways.md` 한 곳. 여기에 다시 적지 않는다.
- [[guard-the-context-window]] — 필요한 장만 읽는다(1–3장은 늘, 나머지는 해당 코드일 때).

## 반패턴 (하지 말 것)
- 규칙을 기계적으로 적용해 읽기 어려운 코드를 만들기(억지로 끼운 `:=`). 책도 가독성을 최우선으로 둔다.
- 사용자가 고쳐 달라고 하지 않은 기존 코드를 전부 다시 쓰기.
- 책 본문을 길게 옮겨 적기. 규칙 이름과 BetterWay 번호로 짚는다.
- 실행하지 않은 코드의 출력을 지어내기.

## 끝맺음 템플릿
```
<무엇을 만들었/고쳤는지 한 줄>
- 적용: <규칙 한 줄 (BW N)> × 2~4개
- 확인: check.sh <통과 / N건>, 실행 <출력 요약 / 실행 못 함: 이유>
- 버전 메모: <3.8 이후 문법을 썼다면 무엇(예: zip(strict=True) 3.10+)>
```

## 참고
- `references/better-ways.md`: 90개 Better Way 전체와 장별 적용 요령. 공부한 항목은 밑줄 기준으로 보강되어 있다.
- 공부 자료: `/Users/soonwon/study/책/공부_파이썬 코딩의 기술(개정2판)/` (`코드/gilbut/ChapterN/Better wayN.py` 예제, `내용/` 밑줄 사진). 공부 반영 절차는 book-study Step 4.
- 3.8 이후 바뀐 점은 설명에서 따로 밝힌다(`zip(strict=True)` 3.10+, `zoneinfo` 3.9+, `match` 3.10+, `list[int]` 3.9+).
