"""題庫簽章金鑰(Ed25519)。私鑰只存在本機 macOS 鑰匙圈,不進 repo。

python3 tools/bank_key.py init     產生金鑰對並存進鑰匙圈(已存在就拒絕,避免蓋掉)
python3 tools/bank_key.py pubkey   印出公鑰(base64,內建進 App)
python3 tools/bank_key.py backup <檔案>  把私鑰匯出成檔案(權限 600),請自行移到安全的地方保存
"""
import base64, subprocess, sys, os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

SERVICE, ACCOUNT = 'hsexam-bank-signing', 'ed25519-private'

def _get():
    r = subprocess.run(['security', 'find-generic-password', '-s', SERVICE, '-a', ACCOUNT, '-w'],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None

def load_private() -> Ed25519PrivateKey:
    b64 = _get()
    if not b64: sys.exit('鑰匙圈裡沒有題庫簽章私鑰,請先執行 tools/bank_key.py init')
    return Ed25519PrivateKey.from_private_bytes(base64.b64decode(b64))

def pubkey_b64(priv: Ed25519PrivateKey) -> str:
    raw = priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'init':
        if _get(): sys.exit('鑰匙圈已經有私鑰了,不覆蓋。')
        k = Ed25519PrivateKey.generate()
        raw = k.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())
        subprocess.run(['security', 'add-generic-password', '-s', SERVICE, '-a', ACCOUNT,
                        '-w', base64.b64encode(raw).decode(), '-U'], check=True)
        print('已存進鑰匙圈。公鑰:', pubkey_b64(k))
    elif cmd == 'pubkey':
        print(pubkey_b64(load_private()))
    elif cmd == 'backup' and len(sys.argv) > 2:
        path = sys.argv[2]
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.write(fd, (_get() or '').encode()); os.close(fd)
        print('已匯出到', path, '(請移到密碼管理器或離線備份後刪除此檔)')
    else:
        print(__doc__)
