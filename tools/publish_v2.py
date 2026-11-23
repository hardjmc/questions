"""新版題庫線(App 1.11 起):圖片獨立成檔、清單列 SHA-256、用鑰匙圈私鑰簽名。

python3 tools/publish_v2.py <來源 Questions.json(可含 imageData)> <版本號> [--app <App 原始碼的 HSExamCountdown 資料夾>]

產生(都在 repo 根目錄下):
  bank/Questions.json   題目;附圖改成 "image": {"name": "<題號>.png", "sha256": "…"}
  bank/images/*.png     一題一張圖
  manifest2.json        {"payload": base64(JSON), "signature": base64(Ed25519 簽名)}
--app 會把同一份題庫與圖片複製進 App(內建題庫+BankImages 資料夾)。
舊版 App 用的根目錄 Questions.json / manifest.json 不動。
"""
import base64, hashlib, json, os, shutil, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bank_key import load_private

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_IMAGE = 2_000_000
PNG_MAGIC = b'\x89PNG\r\n\x1a\n'

def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    args = sys.argv[1:]
    app = None
    if '--app' in args:
        i = args.index('--app'); app = args[i + 1]; del args[i:i + 2]
    src, version = args[0], int(args[1])
    bank = json.load(open(src, encoding='utf-8'))
    out_dir = os.path.join(ROOT, 'bank'); img_dir = os.path.join(out_dir, 'images')
    if os.path.isdir(img_dir): shutil.rmtree(img_dir)
    os.makedirs(img_dir)
    images = {}
    for q in bank['questions']:
        b64 = q.pop('imageData', None)
        if not b64: continue
        data = base64.b64decode(b64)
        assert data.startswith(PNG_MAGIC), f"{q['id']} 不是 PNG"
        assert len(data) <= MAX_IMAGE, f"{q['id']} 圖太大"
        name = f"{q['id']}.png"
        open(os.path.join(img_dir, name), 'wb').write(data)
        q['image'] = {'name': name, 'sha256': sha(data)}
        images[name] = sha(data)
    bank_bytes = json.dumps(bank, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    open(os.path.join(out_dir, 'Questions.json'), 'wb').write(bank_bytes)
    payload = {
        'format': 2, 'version': version, 'createdAt': int(time.time()),
        'bank': {'path': 'bank/Questions.json', 'sha256': sha(bank_bytes), 'size': len(bank_bytes)},
        'imageBase': 'bank/images/', 'images': images,
    }
    pbytes = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    sig = load_private().sign(pbytes)
    manifest = {'payload': base64.b64encode(pbytes).decode(), 'signature': base64.b64encode(sig).decode()}
    json.dump(manifest, open(os.path.join(ROOT, 'manifest2.json'), 'w'), indent=1)
    print(f'v{version}:{len(bank["questions"])} 題、{len(images)} 張圖,題庫 {len(bank_bytes)/1e6:.2f} MB,已簽名')
    if app:
        shutil.copy(os.path.join(out_dir, 'Questions.json'), os.path.join(app, 'Questions.json'))
        dst = os.path.join(app, 'BankImages')
        if os.path.isdir(dst): shutil.rmtree(dst)
        shutil.copytree(img_dir, dst)
        print('已複製進 App:', app)

if __name__ == '__main__':
    main()
