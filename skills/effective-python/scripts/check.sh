#!/usr/bin/env bash
# 『파이썬 코딩의 기술』 규칙 중 기계가 잡을 수 있는 것을 ruff로 확인한다. 고치지는 않는다.
# 사용: check.sh <파일 또는 폴더>...
#   프로젝트에 ruff 설정이 있어도 --isolated로 이 규칙만 본다(프로젝트 린트는 따로 돌린다).
#
# 규칙 ↔ Better Way
#   E711         is None 으로 비교                    (BW2)
#   UP031 UP032  % 포맷·str.format 대신 f-문자열        (BW4)
#   SIM113       직접 센 인덱스 대신 enumerate          (BW7)
#   PLW0120      break 없는 for/while 뒤 else         (BW9)
#   B006 B008    가변·호출식 기본 인자 대신 None        (BW24)
#   C417 PERF401 map·append 루프 대신 컴프리헨션        (BW27)
set -euo pipefail
[ $# -ge 1 ] || { echo "사용: $0 <파일 또는 폴더>..." >&2; exit 2; }
RULES="E711,UP031,UP032,SIM113,PLW0120,B006,B008,C417,PERF401"
if command -v ruff >/dev/null; then RUFF=(ruff); else RUFF=(uvx -q ruff); fi
"${RUFF[@]}" check --no-cache --isolated --select "$RULES" --output-format concise "$@"
