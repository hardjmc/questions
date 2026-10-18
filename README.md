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

push 前一定要跑檢查工具,有「錯誤」就不要 push:

```
python3 tools/validate_bank.py Questions.json
```

它會檢查題號重複、正解範圍、格式標記與數學式是否成對、表格欄數、圖片能否解碼,
並在格式版和純文字版的數字對不起來時提出警告。App 端下載後也會解析驗證,失敗會丟棄不落地。

## 格式欄位(App 1.7 起)

每題除了純文字的 `stem` / `options` / `explanation`,可以再加格式版(都可省略):

| 欄位 | 內容 |
|---|---|
| `stemRich` | 題幹格式版 |
| `optionsRich` | 選項格式版,數量必須和 `options` 相同 |
| `explanationRich` | 詳解格式版 |
| `table` | 附表:`{"caption": 選填, "header": [...], "rows": [[...], ...], "rowHeader": true/false}` |

格式標記:`<u>底線</u>`、`<b>粗體</b>`、`<i>斜體</i>`、`$…$` 數學式。
數學式支援 `\frac{分子}{分母}`、`\sqrt{x}`、`\sqrt[3]{x}`、`^{上標}`、`_{下標}`,
以及 `\times \div \pm \le \ge \ne \approx \pi \circ \angle \triangle \cdot` 等符號;字面的錢字號寫 `\$`。

**規則:純文字欄位一定要保留而且要能獨立看懂。** 1.6 以前的 App 不認得格式欄位,只會顯示純文字版,
所以有表格的題目,純文字題幹裡也要寫出資料;用底線標示的字,純文字版改用「」或 [ ] 標出來。

## 題目附圖

86 題內嵌 base64 PNG 附圖(`imageData` 欄位),由 `tools/fig_all.py` 產生
(matplotlib + Pillow;需 `pip3 install matplotlib pillow`;存檔時自動壓成 64 色 PNG)。修圖流程:

```
python3 tools/fig_all.py <題號>        # 重新產生單張到 figs/
# 再用 base64 塞回 Questions.json 的該題 imageData,version +1 後 push
```

新增附圖:在 fig_all.py 加一個 @fig(<題號>) 函式(參考現有模板:
parallel_cut / chord_dist / rt_tri / pie_fig / wave_pair …)。
