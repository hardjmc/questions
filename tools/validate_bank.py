"""題庫檢查:push 前跑一次,有錯就不要上線。

    python3 tools/validate_bank.py Questions.json

錯誤(會讓 App 顯示壞掉):題號重複、正解超出範圍、格式標記沒成對、$ 沒成對、
數學式大括號不平衡或用了 App 不支援的指令、optionsRich 數量不符、表格欄數不一致、圖片無法解碼。
警告(要人工看一眼):格式版和純文字版的數字對不起來。
"""
import json, re, sys, base64, io
from collections import Counter

KNOWN = {'frac', 'dfrac', 'tfrac', 'sqrt', 'text', 'mathrm', 'left', 'right',
         'times', 'div', 'pm', 'mp', 'cdot', 'le', 'leq', 'ge', 'geq', 'ne', 'neq', 'approx', 'lt', 'gt',
         'pi', 'circ', 'degree', 'angle', 'triangle', 'perp', 'parallel', 'cong', 'sim', 'infty',
         'alpha', 'beta', 'gamma', 'theta', 'Delta', 'lambda', 'mu', 'rightarrow', 'to', 'Rightarrow',
         'therefore', 'because', 'quad'}
TAG = re.compile(r'</?([ubi])>')

def check_markup(s, where, errs):
    stack = []
    for m in TAG.finditer(s):
        t = m.group(1)
        if m.group(0).startswith('</'):
            if not stack or stack[-1] != t: errs.append(f'{where}: 標記 </{t}> 沒有對應的開頭'); return
            stack.pop()
        else:
            stack.append(t)
    if stack: errs.append(f'{where}: 標記 <{stack[-1]}> 沒有結尾')
    body = s.replace('\\$', '')
    if body.count('$') % 2: errs.append(f'{where}: $ 沒有成對'); return
    for expr in re.findall(r'\$([^$]*)\$', body):
        depth = 0
        for ch in expr:
            depth += ch == '{'; depth -= ch == '}'
            if depth < 0: break
        if depth != 0: errs.append(f'{where}: 數學式大括號不平衡:{expr}')
        for cmd in re.findall(r'\\([A-Za-z]+)', expr):
            if cmd not in KNOWN: errs.append(f'{where}: App 不支援的指令 \\{cmd}')

def to_plain(s):
    s = TAG.sub('', s)
    s = re.sub(r'\\sqrt\{([^{}]*)\}', r'√\1', s)
    for _ in range(3): s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'\1/\2', s)
    return s.replace('$', '')

def digits(s): return Counter(re.findall(r'\d', s))

def main(path):
    d = json.load(open(path)); qs = d['questions'] if isinstance(d, dict) else d
    errs, warns = [], []
    ids = Counter(q['id'] for q in qs)
    errs += [f'題號 {i} 重複 {n} 次' for i, n in ids.items() if n > 1]
    for q in qs:
        i = q['id']
        if not q['options'] or not 0 <= q['answerIndex'] < len(q['options']): errs.append(f'{i}: 正解索引超出範圍')
        for key in ('stem', 'explanation', 'stemRich', 'explanationRich'):
            if key in q and '$' in q[key] or key.endswith('Rich') and key in q: check_markup(q.get(key, ''), f'{i}.{key}', errs)
        if 'optionsRich' in q:
            if len(q['optionsRich']) != len(q['options']): errs.append(f'{i}: optionsRich 數量和 options 不同')
            for k, o in enumerate(q['optionsRich']): check_markup(o, f'{i}.optionsRich[{k}]', errs)
            for k, (r, p) in enumerate(zip(q['optionsRich'], q['options'])):
                if digits(to_plain(r)) != digits(p): warns.append(f'{i}.選項{k}: 數字對不上 「{p}」 vs 「{to_plain(r)}」')
        if 'table' in q:
            t = q['table']; rows = t.get('rows') or []
            width = len(t['header']) if t.get('header') else (len(rows[0]) if rows else 0)
            if not rows: errs.append(f'{i}: 表格沒有資料列')
            for r in rows:
                if len(r) != width: errs.append(f'{i}: 表格某列有 {len(r)} 欄,應為 {width} 欄')
            for cell in (t.get('header') or []) + [c for r in rows for c in r] + ([t['caption']] if t.get('caption') else []):
                check_markup(cell, f'{i}.table', errs)
        if 'explanationRich' in q and digits(to_plain(q['explanationRich'])) != digits(q['explanation']):
            warns.append(f'{i}.詳解: 數字對不上')
        if 'stemRich' in q and 'table' not in q and digits(to_plain(q['stemRich'])) != digits(q['stem']):
            warns.append(f'{i}.題幹: 數字對不上')
        if q.get('imageData'):
            try:
                from PIL import Image
                Image.open(io.BytesIO(base64.b64decode(q['imageData']))).verify()
            except Exception as e:
                errs.append(f'{i}: 圖片無法解碼({e})')
    rich = sum(1 for q in qs if any(k in q for k in ('stemRich', 'optionsRich', 'explanationRich', 'table')))
    print(f'{len(qs)} 題,有格式欄位 {rich} 題,附圖 {sum(1 for q in qs if q.get("imageData"))} 題')
    for w in warns: print('警告', w)
    for e in errs: print('錯誤', e)
    print(f'錯誤 {len(errs)}、警告 {len(warns)}')
    return 1 if errs else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'Questions.json'))
