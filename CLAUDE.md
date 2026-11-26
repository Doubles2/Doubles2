# doubles2 — 홈 레포

이 저장소는 세 가지를 한곳에 담는다.

1. **스킬 모음**: 내가 만들어 쓰는 Claude Code 스킬. 이 repo 자체가 플러그인 마켓플레이스다.
2. **포트폴리오**: 코드·모델 작업은 별도 repo를 만들지 않고 `projects/` 아래 폴더로 쌓는다.
3. **노하우 위키**: 해결한 문제와 배운 것을 `wiki/`에 쌓아 같은 설명을 반복하지 않는다.

로컬 위치는 어느 컴퓨터에서든 `~/code/doubles2`로 고정한다. 스킬이 이 경로를 쓴다.
에이전트는 가능하면 이 폴더에서 실행한다.

## 폴더 지도

| 경로 | 내용 |
|---|---|
| `skills/<이름>/SKILL.md` | 내 스킬. 한 폴더에 스킬 하나. 하위 분류 폴더를 만들지 않는다 |
| `principles/` | 스킬이 공통으로 따르는 원칙. 목차는 `principles/principles.md` |
| `projects/<YYYY-MM>-<이름>/` | 코드·모델 작업 하나. 규칙은 `projects/README.md` |
| `wiki/` | 노하우 위키. 규칙은 `wiki/CLAUDE.md`, 목차는 `wiki/index.md` |
| `repos.md` | 이 repo 밖에 있는 공개 repo 포인터 |
| `private/` | 개인 자료(이력서 자료, 비공개 repo 포인터). 이 컴퓨터에만 있고 GitHub에 올리지 않는다 |
| `.claude-plugin/` | 플러그인·마켓플레이스 매니페스트 |
| `.claude/settings.json` | 받아 쓰는 외부 스킬 마켓플레이스 목록 |

## 규칙

- **이 repo는 공개다.** 이력서·연봉·연락처, 회사 내부 코드·데이터·주소는 `private/`에만 둔다.
  커밋 전에 회사명이 들어간 파일, `.env`, 키, 데이터 파일이 섞이지 않았는지 확인한다.
- **질문을 받거나 작업을 시작하면 `wiki/index.md`를 먼저 본다.** 이미 해결한 문제를 다시 풀지 않는다.
- **스킬은 Step 1에서 `principles/principles.md`와 링크된 원칙을 새로 읽는다.** 스킬끼리 판단 기준을 여기 한 곳에서 맞춘다.
- **작업을 마치면 배운 것을 남긴다.** 해결한 문제는 wiki에, 반복되는 절차는 스킬로 만든다.
- **스킬을 고치면 커밋 후 push해야** 다른 컴퓨터의 플러그인에 반영된다.
- **커밋과 push는 따로 하고, 각각 실행 전에 사용자에게 다시 확인한다**(`skills/git-confirm`). repo 생성·삭제·이름 변경도 먼저 확인한다.
- 외부 스킬은 파일을 복사해 오지 않는다. `.claude/settings.json`에 마켓플레이스만 등록한다.

## 다른 repo

- 공개 repo: `repos.md`
- 비공개 repo: `private/repos.md` (없으면 개인 자료가 없는 컴퓨터다)

포인터에 적힌 경로에 repo가 없으면 그 경로로 clone한 뒤 작업한다.
그 repo를 고치기 전에는 그 repo의 `CLAUDE.md`나 `README.md`를 먼저 읽는다.
