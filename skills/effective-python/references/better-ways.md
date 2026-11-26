# 90가지 Better Way 적용 요령

제목은 책의 규칙이고, 화살표 뒤는 코드를 쓸 때 실제로 할 일이다(직접 풀어 쓴 요약).
번호는 개정2판 기준이다. 해당 장의 코드를 쓸 때 이 장을 통째로 읽고 따른다.

## 1장 파이썬답게 생각하기

1. 사용 중인 파이썬의 버전을 알아두라 → `python3 --version`과 프로젝트 설정을 먼저 확인한다.
2. PEP 8 스타일 가이드를 따르라 → 들여쓰기 4칸, 줄 79자 안팎, `snake_case`, `if not x`, `is None`, import는 표준·서드파티·로컬 순.
3. bytes와 str의 차이를 알아두라 → 경계에서만 encode/decode, 파일은 `'rb'`/`'wb'`와 `encoding=` 명시.
4. f-문자열을 사용하라 → `f'{name}: {value:.2f}'`. `%`·`str.format` 금지.
5. 복잡한 식 대신 도우미 함수 → 두세 번 반복되거나 한 줄이 복잡하면 함수로.
6. 인덱스 대신 대입으로 언패킹 → `for rank, (name, cal) in enumerate(items, 1)`.
7. range보다 enumerate → 인덱스가 필요하면 `enumerate(seq, start)`.
8. 나란히 돌 땐 zip → 길이가 다르면 `zip(..., strict=True)`(3.10+)나 `zip_longest`.
9. for/while 뒤 else 금지 → 찾았는지 여부는 도우미 함수의 반환값으로.
10. 대입식으로 반복 피하기 → `if (count := d.get('x', 0)) > 0:`. 읽기 쉬울 때만.

## 2장 리스트와 딕셔너리

11. 슬라이싱 → `a[:n]`, `a[-n:]`. 슬라이스는 새 리스트, `a[:] = b`는 제자리 교체.
12. 스트라이드와 슬라이스를 한 식에 쓰지 말라 → 두 단계로 나누거나 `itertools.islice`. bytes를 `[::-1]`로 뒤집지 않는다.
13. 슬라이싱보다 나머지를 잡는 언패킹 → `oldest, *others = sorted_ages`.
14. 복잡한 정렬은 key → `sort(key=lambda x: (x.weight, -x.price))`.
15. dict 삽입 순서 의존 주의 → 진짜 `dict`일 때만 순서를 믿고, 아니면 타입 검사·애너테이션.
16. in·KeyError보다 get → `counts[k] = counts.get(k, 0) + 1`, 세기는 `Counter`.
17. setdefault보다 defaultdict → `defaultdict(set)`, `defaultdict(list)`.
18. `__missing__` → 키에 따라 기본값이 다르면 dict 하위 클래스에서 만들고 저장.

## 3장 함수

19. 반환값 네 개 이상을 언패킹하지 말라 → `NamedTuple`/`dataclass` 반환.
20. None 반환보다 예외 → 실패는 `raise ValueError(...)`(내부 예외를 바꿔 던짐), 반환 타입은 `-> float`처럼 None 없이, 발생 예외는 독스트링 `Raises:`에 적는다. `(성공, 결과)` 튜플도 `_`로 무시되기 쉬우니 피한다. 호출 쪽은 `try/except/else`의 else에서 결과를 쓴다. None을 꼭 반환하면 `if not x` 말고 `is None`으로 검사.
21. 변수 영역과 클로저 → 클로저 안의 대입은 바깥 변수를 바꾸지 못하고 새 지역 변수를 만든다(영역 지정 버그: 플래그가 계속 False). 간단한 함수에서만 `nonlocal`을 쓰고, 함수가 길거나 선언과 대입이 멀면 상태를 `__call__` 있는 작은 클래스로 감싼다. `global`로 모듈 영역에 쓰지 않는다.
22. 가변 위치 인자로 잡음 줄이기 → `def log(msg, *values)`. 제너레이터를 넘기면 다 소진됨에 주의.
23. 키워드 인자로 선택 기능 → 새 옵션은 기본값 있는 키워드 인자로 추가해 호출부 호환 유지.
24. None과 독스트링으로 동적 기본값 → `def f(when=None):` 안에서 `if when is None: when = datetime.now()`. 가변 기본값 금지.
25. 위치 전용·키워드 전용 → `def safe_div(n, d, /, *, ignore_zero=False)`.
26. functools.wraps로 데코레이터 → 이름·독스트링·`help()` 보존.

## 4장 컴프리헨션과 제너레이터

27. map·filter 대신 컴프리헨션 → `[x**2 for x in a if x % 2 == 0]`.
28. 제어 하위 식 셋 이상 금지 → 루프 두 단계 + 조건 하나까지. 넘으면 일반 `for`.
29. 컴프리헨션 안 반복은 대입식 → `{k: v for k in order if (v := get(k))}`.
30. 리스트 반환보다 제너레이터 → 결과를 모아 `append`하는 함수는 `yield`로.
31. 인자 이터레이션은 방어적으로 → 여러 번 순회하면 컨테이너(`__iter__`)를 받고 이터레이터면 `TypeError`.
32. 긴 리스트 컴프리헨션보다 제너레이터 식 → 큰 입력은 `(len(x) for x in f)`.
33. yield from으로 합성 → 하위 제너레이터 연결.
34. send로 주입하지 말라 → 입력은 이터레이터 인자로 넘긴다.
35. throw로 상태 변경 말라 → `__iter__`를 가진 클래스로 상태 관리.
36. itertools → `chain`, `islice`, `takewhile`, `groupby`, `product`, `accumulate` 먼저 찾기.

## 5장 클래스와 인터페이스

37. 내장 타입 중첩보다 클래스 합성 → dict/tuple이 2단을 넘으면 `dataclass`/`NamedTuple`로 쪼갠다.
38. 간단한 인터페이스는 함수를 받아라 → 훅은 함수, 상태가 필요하면 `__call__`.
39. @classmethod 다형성 → 생성 방법이 여럿이면 `@classmethod` 팩토리.
40. super로 부모 초기화 → `super().__init__(...)`, 다이아몬드 상속도 MRO로 안전.
41. 믹스인으로 기능 합성 → 상태 없는 작은 믹스인(`ToDictMixin` 같은).
42. 비공개보다 공개 애트리뷰트 → `_protected` 관례 + 문서화, `__private`은 이름 충돌 방지용만.
43. 커스텀 컨테이너는 collections.abc 상속 → 빠진 메서드를 알려 준다.

## 6장 메타클래스와 애트리뷰트

44. 세터·게터 대신 평범한 애트리뷰트 → `obj.x = 1`.
45. 리팩터링 대신 @property → 나중에 계산·검증이 필요해지면 호출부를 바꾸지 않고 `@property`로.
46. 재사용 가능한 @property는 디스크립터 → 같은 검증을 여러 애트리뷰트에 쓰면 `__get__`/`__set__`.
47. 지연 계산은 `__getattr__`·`__getattribute__`·`__setattr__` → 무한 재귀는 `super()`로 피한다.
48. `__init_subclass__`로 하위 클래스 검증.
49. `__init_subclass__`로 클래스 등록.
50. `__set_name__`으로 클래스 애트리뷰트 표시.
51. 메타클래스보다 클래스 데코레이터 → 합성 가능한 확장은 데코레이터로.

## 7장 동시성과 병렬성

52. 자식 프로세스는 subprocess → `subprocess.run(..., check=True, capture_output=True, timeout=)`.
53. 블로킹 I/O는 스레드, 병렬성은 피하라 → GIL 때문에 CPU 병렬엔 스레드가 효과 없다.
54. 데이터 경합은 Lock → 공유 카운터 갱신은 `with lock:`.
55. 스레드 간 작업 조율은 Queue → 파이프라인은 `queue.Queue` + `task_done`/`join`.
56. 언제 동시성이 필요한지 인식하라 → 팬아웃(fan-out)·팬인(fan-in) 지점을 찾는다.
57. 요구마다 새 스레드를 만들지 말라.
58. Queue로 리팩터링하는 방법 이해.
59. 스레드가 필요하면 ThreadPoolExecutor → `with ThreadPoolExecutor(max_workers=n) as ex: ex.map(...)`.
60. I/O 동시성은 코루틴 → `async def` + `asyncio.gather`.
61. 스레드 I/O를 asyncio로 포팅.
62. 스레드와 코루틴 섞기 → `asyncio.to_thread`, `run_in_executor`.
63. 이벤트 루프를 블록하지 말라 → 루프 안에서 블로킹 호출 금지.
64. 진정한 병렬성은 concurrent.futures → CPU 작업은 `ProcessPoolExecutor`.

## 8장 강건성과 성능

65. try/except/else/finally 각 블록 활용 → `try`엔 실패할 줄만, 성공 후속은 `else`, 정리는 `finally`.
66. contextlib과 with → `@contextmanager`로 재사용 가능한 정리 동작.
67. time보다 datetime → 시간대는 `datetime` + `zoneinfo`(3.9+).
68. copyreg로 pickle 안정화 → 신뢰할 수 없는 데이터는 애초에 unpickle 하지 않는다.
69. 정확도가 중요하면 decimal → 돈 계산은 `Decimal('1.45')`(문자열로 생성), 반올림 명시.
70. 최적화 전 프로파일링 → `cProfile` + `pstats`.
71. 생산자-소비자 큐는 deque → `list.pop(0)` 금지.
72. 정렬된 시퀀스 검색은 bisect.
73. 우선순위 큐는 heapq.
74. bytes 복사 없이 다루기 → `memoryview`, `bytearray`.

## 9장 테스트와 디버깅

75. 디버깅 출력은 repr → `print(f'{x!r}')`, 클래스엔 `__repr__`.
76. TestCase 하위 클래스로 검증 → `assertEqual`, `assertRaises`; 사용자는 pytest도 가능.
77. setUp/tearDown으로 격리 → 임시 디렉터리 등은 테스트마다 새로.
78. 목으로 복잡한 의존성 테스트 → `unittest.mock`, `patch`.
79. 의존 관계를 캡슐화해 모킹 쉽게 → 의존성을 인자로 주입.
80. pdb로 대화형 디버깅 → `breakpoint()`.
81. tracemalloc으로 메모리 이해.

## 10장 협업

82. 커뮤니티 모듈은 PyPI에서 찾는다.
83. 가상 환경으로 의존성 격리 → `python3 -m venv .venv`, `requirements.txt`/`pyproject.toml`.
84. 모든 함수·클래스·모듈에 독스트링 → 첫 줄 요약, 인자·반환·예외 설명.
85. 패키지로 모듈 체계화 → `__init__.py`, `__all__`로 공개 API.
86. 배포 환경 설정은 모듈 영역 코드로.
87. 최상위 Exception 정의 → `class MyLibError(Exception)`을 루트로 하위 예외 계층.
88. 순환 의존성 깨기 → import 재배치, 동적 import, 구조 변경.
89. warning으로 마이그레이션 안내 → `warnings.warn(..., DeprecationWarning, stacklevel=2)`.
90. typing과 정적 분석 → 공개 API에 타입 힌트, `mypy`로 검사.
