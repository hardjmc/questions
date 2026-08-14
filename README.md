# 會考倒數・題庫

「會考倒數」iOS App 的線上題庫。App 啟動時會在背景讀取 `manifest.json`,
版本比 App 內建/已下載的新,就下載 `Questions.json` 覆蓋內建題庫(下次啟動生效)。

## 檔案

- `Questions.json` — 完整題庫(格式:`{"questions": [...]}`),與 App 內建檔相同格式。
- `manifest.json` — 版本資訊:

  ```json
  {
    "version": 1,
    "url": "https://raw.githubusercontent.com/hardjmc/questions/main/Questions.json"
  }
  ```

## 版本規則

- App 內建題庫的基準版本寫在 App 端 `QuizQuestion.swift` 的 `bundledVersion`(目前 = 1)。
- `manifest.json` 的 `version` **大於** 使用者手上的版本(內建基準或已下載版)才會觸發下載。
- 所以 `version: 1` = 「與 App 1.0 內建題庫相同」,不會有人下載;第一次線上勘誤請改成 2。

## 改題(勘誤)流程

1. 修改 `Questions.json` 裡的題目。
2. `manifest.json` 的 `version` +1。
3. commit + push,全球使用者下次開 App 自動更新,**不需送審**。
4. 同步把改動複製回 App repo 的 `HSExamCountdown/Questions.json`
   (下次發版時一併把 App 端 `bundledVersion` 改成當時 manifest 的版本號,
   新安裝的使用者就不會多下載一次)。

## 驗證

push 前先確認 JSON 有效:

```
python3 -c "import json; qs=json.load(open('Questions.json'))['questions']; print(len(qs), '題 OK')"
```

App 端下載後也會先完整解析驗證,失敗會丟棄不落地,但仍建議 push 前自檢。
