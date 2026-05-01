# アーキテクチャ設計（初版）

## コンポーネント
1. **Webhook Receiver**
   - JIRAからのイベント受信・署名検証。
2. **Assignment Evaluator**
   - assignee変更有無の判定、対象イベントの抽出。
3. **Routing Resolver**
   - 担当者→プリンタのマッピング解決。
4. **Document Renderer**
   - 印刷テンプレート生成（HTML/PDF/TXT）。
5. **Print Dispatcher**
   - プリンタキュー投入、結果収集。
6. **Audit Logger**
   - 監査ログ保存（DB/ファイル/SIEM）。

## データストア
- `user_printer_map`
  - `jira_account_id`
  - `printer_id`
  - `site`
  - `enabled`
- `print_jobs`
  - `event_id`
  - `issue_key`
  - `assignee`
  - `printer_id`
  - `status`
  - `created_at`

## エラーハンドリング方針
- ルーティング未定義: 既定プリンタ or 保留キューへ退避。
- 印刷失敗: exponential backoffで再試行。
- 永続失敗: アラート通知（Slack/メール）。

