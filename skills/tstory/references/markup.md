# 실측 자료 — 티스토리가 실제로 내보내는 마크업

> **이 마크업을 직접 쓸 일은 없습니다.** 글은 기본모드로 타이핑합니다(`manuscript.md`).
> 이 문서는 "왜 원고 태그가 이렇게 정해졌는지"의 근거 자료입니다.

이 문서는 `doubles-won.tistory.com`에 실제 발행된 12편(#133~#144)의 HTML을
전수 조사해 뽑아낸 규격입니다. 추측이 아니라 실측값입니다.

## 대원칙

**툴바가 직접 만들어내는 요소만 쓴다. 커스텀 `style` 속성은 붙이지 않는다.**

이유: 발행 후 글쓰기(기본모드) 화면에서 본인이 직접 수정할 수 있어야 하기 때문입니다.
`data-ke-*` 속성은 티스토리 에디터의 **블록 식별자**라서, HTML 모드로 붙여넣고
기본모드로 돌아오면 제목·인용구·표·목록이 전부 일반 블록으로 잡힙니다.
반면 인라인 `style`을 얹으면 툴바로는 되돌릴 수 없는 상태가 됩니다.

## 허용 목록 (이게 전부)

| 용도 | 마크업 |
|---|---|
| 본문 문단 | `<p data-ke-size="size16">…</p>` |
| 대단원 (에디터 **제목1**) | `<h2 data-ke-size="size26">…</h2>` |
| 소단원 (에디터 **제목2**) | `<h3 data-ke-size="size23">…</h3>` |
| 구분선 | `<hr data-ke-style="style1">` |
| 인용구 | `<blockquote data-ke-style="style1"><p data-ke-size="size16">…</p></blockquote>` |
| 불릿 목록 | `<ul data-ke-list-type="disc"><li>…</li></ul>` |
| 번호 목록 | `<ol data-ke-list-type="decimal"><li>…</li></ol>` |
| 표 | `<table data-ke-align="alignLeft"><thead>…</thead><tbody>…</tbody></table>` |
| 코드블록 | `<pre class="언어"><code>…</code></pre>` |
| 이미지 | `<figure class="imageblock alignCenter" data-ke-mobilestyle="widthOrigin">…</figure>` |

인라인 요소: `<b>`, `<code>`, `<a href … target="_blank" rel="noopener">`, `<br>`

## 금지

- `style="…"` 속성 (아래 한 가지 예외만)
- 바깥을 감싸는 `<div>` 래퍼 — 기존 글에는 폰트 지정용 `<div>`가 있었지만 이제 넣지 않습니다
- `<span>`으로 폰트/크기 지정
- `<h1>` — 글 제목은 티스토리 제목 칸이 담당합니다
- `<i>`, `<u>`, `<strong>`, `<em>` — 이 블로그는 강조를 전부 `<b>`로 통일합니다

**유일한 예외:** 출처 문구의 회색 처리.
글자색은 툴바 기능이므로 `<span style="color: #999999;">…</span>`는 네이티브로 취급합니다.

## 사용 빈도 (12편 실측)

`<b>` 379 · `<p>` 184 · `<li>` 137 · `<hr>` 95 · `<td>` 94 · `<code>` 82 · `<h2>` 71 ·
`<blockquote>` 49 · `<ul>` 40 · `<pre>` 27 · `<h3>` 16 · `<table>` 9

읽히는 신호: **`<b>`가 문단만큼 많습니다.** 이 블로그는 한 문단에 핵심어 1~2개를
굵게 처리하는 것이 기본 리듬입니다. 굵게가 없는 문단이 연속되면 톤이 어긋납니다.

## 세부 규칙

### 구분선
모든 `h2` 섹션 **앞**에 `<hr data-ke-style="style1">`을 넣습니다.
글 전체에서 `hr`이 `h2`보다 많은 이유(95 vs 71)는 출처 문구 위아래에도 들어가기 때문입니다.

### 리스트 항목
`<li><b>용어</b> — 설명</li>` 형태. 구분자는 em dash(`—`)이고 앞뒤로 공백 하나씩.
하이픈(`-`)이나 콜론(`:`)이 아닙니다.

### 표
`thead`에 헤더 행, `tbody`에 본문 행. 첫 열은 보통 `<b>`로 감쌉니다.

```html
<table data-ke-align="alignLeft">
<thead>
<tr><th>계층</th><th>로드</th><th>시점 / 비용</th></tr>
</thead>
<tbody>
<tr><td><b>1. Catalog</b></td><td>name + description</td><td>세션 시작 / 스킬당 ~50-100토큰</td></tr>
</tbody>
</table>
```

### 코드블록
`<pre class="언어"><code>…</code></pre>`. `class`는 하이라이터용 언어명
(`python`, `yaml`, `json`, `dockerfile`, `bash`, `markdown` 등).
내부의 `<`, `>`, `&`는 반드시 이스케이프합니다.

### 이미지
```html
<figure class="imageblock alignCenter" data-ke-mobilestyle="widthOrigin">
  <img src="[업로드 후 티스토리가 넣어줍니다]">
</figure>
```
원고에서는 `(fig-01.png 삽입) — 설명`으로 위치만 표시하고,
실제 업로드는 글쓰기 화면에서 **이미지 버튼 → 사진**으로 합니다.


## 에디터 프리셋 ↔ 태그 (확인 완료)

**이름이 한 칸씩 어긋납니다.** 에디터의 "제목1"이 `h2`입니다.

| 에디터 프리셋 | 태그 | 토큰 |
|---|---|---|
| 제목1 | `h2` | `size26` |
| 제목2 | `h3` | `size23` |
| 제목3 | `h4` | `size20` |
| 본문1 | `p` | `size18` |
| 본문2 (기본값) | `p` | `size16` |
| 본문3 | `p` | `size14` |

출처 문구를 한 단계 줄이고 싶다면 **본문3(`size14`)**을 쓸 수 있습니다.
지금은 크기를 줄이지 않고 회색 처리만 합니다 — 기존 12편이 그렇습니다.
