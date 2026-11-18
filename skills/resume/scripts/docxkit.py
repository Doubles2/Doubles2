#!/usr/bin/env python3
"""워드(.docx) 입사지원서 양식을 서식을 깨뜨리지 않고 편집하는 도구.

핵심 전제: 한글 워드 문서는 한 문장이 여러 run으로 쪼개져 있다.
따라서 텍스트 치환은 run 단위가 아니라 '단락 단위'로 해야 한다.
단락의 첫 w:t에 전체 문자열을 넣고 나머지 w:t를 비우면
첫 run의 서식(폰트/크기/굵기)이 그대로 유지된다.

사용법:
  python docxkit.py dump    FILE                     구조 출력 (표 좌표 포함)
  python docxkit.py check   FILE                     제출 전 자동 점검
  python docxkit.py cell    FILE T R C "줄1" "줄2"    표 셀 채우기 (여러 줄 가능)
  python docxkit.py rebuild FILE T R C lines.txt     서술 셀 전체 교체 (빈 줄 허용)
  python docxkit.py replace FILE "옛 문구" "새 문구"   단락 단위 문자열 치환
  python docxkit.py pages   FILE OUT.pages           Pages(.pages)로 변환
"""
import copy, re, shutil, subprocess, sys, zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
XS = '{http://www.w3.org/XML/1998/namespace}space'


def load(path):
    z = zipfile.ZipFile(path)
    raw = z.read('word/document.xml').decode('utf-8')
    for pfx, uri in re.findall(r'xmlns:([A-Za-z0-9]+)="([^"]+)"', raw[:3000]):
        ET.register_namespace(pfx, uri)
    root = ET.fromstring(raw)
    payload = {i.filename: z.read(i.filename) for i in z.infolist()}
    infos = list(z.infolist())
    z.close()
    return root, infos, payload


def save(path, root, infos, payload, backup=True):
    """편집 전 .prev 스냅샷을 남긴다. 되돌릴 곳이 없으면 실험을 못 한다."""
    if backup:
        shutil.copy(path, path + '.prev')
    out = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    payload['word/document.xml'] = out
    # 같은 파일을 읽으면서 쓰면 깨진다. 미리 메모리에 올려두고 한 번에 쓴다.
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zo:
        for info in infos:
            zo.writestr(info, payload[info.filename])


def ptxt(p):
    return ''.join(t.text or '' for t in p.iter(W + 't'))


def setp(p, s):
    """단락 텍스트 교체. 첫 run의 서식을 상속한다."""
    ts = list(p.iter(W + 't'))
    if not ts:                     # 빈 셀은 run 자체가 없다
        r = ET.SubElement(p, W + 'r')
        ts = [ET.SubElement(r, W + 't')]
    ts[0].text = s
    ts[0].set(XS, 'preserve')
    for t in ts[1:]:
        t.text = ''


def tables(root):
    return list(root.iter(W + 'tbl'))


def cell(root, ti, ri, ci):
    return tables(root)[ti].findall(W + 'tr')[ri].findall(W + 'tc')[ci]


def fill(tc, lines):
    """셀을 여러 줄로 채운다. 기존 첫 단락을 틀로 복제하므로 서식이 유지된다.
    빈 셀(run 없음)에 그냥 글자를 넣으면 주변과 글씨 크기가 어긋나므로,
    같은 표의 채워진 행을 틀로 쓰고 싶을 땐 clone_from을 쓸 것."""
    ps = tc.findall(W + 'p')
    tpl = copy.deepcopy(ps[0])
    idx = list(tc).index(ps[0])
    for p in ps:
        tc.remove(p)
    for off, s in enumerate(lines):
        np = copy.deepcopy(tpl)
        setp(np, s)
        tc.insert(idx + off, np)


def clone_from(src_tc, dst_tc, lines, drop_bold=False):
    """다른 셀(보통 이미 채워진 같은 열)의 서식을 그대로 가져와 채운다.
    빈 칸을 새로 채울 때 이 방식이 아니면 폰트 크기가 튄다."""
    tpl = copy.deepcopy(src_tc.findall(W + 'p')[0])
    if drop_bold:
        for r in tpl.findall(W + 'r'):
            rPr = r.find(W + 'rPr')
            if rPr is not None:
                b = rPr.find(W + 'b')
                if b is not None:
                    rPr.remove(b)
    for p in dst_tc.findall(W + 'p'):
        dst_tc.remove(p)
    for s in lines:
        np = copy.deepcopy(tpl)
        setp(np, s)
        dst_tc.append(np)


def replace(root, old, new):
    """단락 단위 치환. run이 쪼개져 있어도 잡힌다."""
    n = 0
    for p in root.iter(W + 'p'):
        t = ptxt(p)
        if old in t:
            setp(p, t.replace(old, new))
            n += 1
    return n


# ── 점검 ────────────────────────────────────────────────────────────
CHECKS = [
    ('미기재 자리표시자', r'\[입력 필요\]|\[.*?기입.*?\]|202\*'),
    ('서술형 어미(개조식 위반)', r'했습니다|입니다|였습니다|합니다'),
    ('나열용 가운뎃점(쉼표로)', r'(?<=\S)·(?=\S)'),
    ('양식 지시문 잔존', r'제외하여 작성|기입 必|위주 기술|전체 대상'),
]


def check(path):
    root, _, _ = load(path)
    txt = ''.join(t.text or '' for t in root.iter(W + 't'))
    bad = 0
    for label, pat in CHECKS:
        hits = re.findall(pat, txt)
        mark = 'OK ' if not hits else '점검'
        if hits:
            bad += 1
        print(f'{mark} {label}: {len(hits)}건', (sorted(set(hits))[:6] if hits else ''))
    # 빈 표 셀
    empties = []
    for ti, tbl in enumerate(tables(root)):
        for ri, tr in enumerate(tbl.findall(W + 'tr')):
            for ci, tc in enumerate(tr.findall(W + 'tc')):
                if not ''.join(t.text or '' for t in tc.iter(W + 't')).strip():
                    empties.append((ti, ri, ci))
    print(f'--- 빈 셀 {len(empties)}개 (의도적 공란인지 눈으로 확인): {empties[:20]}')
    return bad


def dump(path):
    root, _, _ = load(path)
    body = root.find(W + 'body')
    ti = -1
    for el in body:
        if el.tag == W + 'p':
            t = ptxt(el)
            if t.strip():
                print(f'[본문] {t[:120]}')
        elif el.tag == W + 'tbl':
            ti += 1
            print(f'--- 표 {ti} ---')
            for ri, tr in enumerate(el.findall(W + 'tr')):
                cells = []
                for ci, tc in enumerate(tr.findall(W + 'tc')):
                    v = ' / '.join(ptxt(p) for p in tc.findall(W + 'p') if ptxt(p))
                    cells.append(f'({ti},{ri},{ci}){v[:45]}')
                print('  ' + ' | '.join(cells))


def to_pages(src, dst):
    """Pages는 IWA(protobuf) 포맷이라 직접 편집하면 서식 오프셋이 깨진다.
    항상 .docx를 원본으로 두고 Pages로 다시 내보내는 방향으로만 간다."""
    script = f'''tell application "Pages"
    activate
    set d to open POSIX file "{src}"
    delay 3
    save d in POSIX file "{dst}"
    delay 3
    close d saving no
end tell'''
    subprocess.run(['osascript', '-e', script], check=True)
    print('pages 생성:', dst)


if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == 'dump':
        dump(path)
    elif cmd == 'check':
        sys.exit(0 if check(path) == 0 else 1)
    elif cmd == 'pages':
        to_pages(path, sys.argv[3])
    else:
        root, infos, payload = load(path)
        if cmd == 'cell':
            ti, ri, ci = map(int, sys.argv[3:6])
            fill(cell(root, ti, ri, ci), sys.argv[6:])
        elif cmd == 'rebuild':
            ti, ri, ci = map(int, sys.argv[3:6])
            lines = open(sys.argv[6], encoding='utf-8').read().split('\n')
            fill(cell(root, ti, ri, ci), lines)
        elif cmd == 'replace':
            n = replace(root, sys.argv[3], sys.argv[4])
            print('치환', n, '건')
            if n == 0:
                sys.exit('치환 실패 — dump로 실제 문자열을 확인할 것')
        save(path, root, infos, payload)
        print('저장 완료 (원본은', path + '.prev)')
