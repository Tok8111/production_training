### 日報データ構造【reportsテーブル】 
| 項目名 | 型 | 説明 | 制約 |
|-|-|-|-|
| report_id | INTEGER | 日報ID(各日報を一意に識別) | 主キー(PRIMARY KEY) |
| user_id | INTEGER | ユーザID(usersテーブルの外部キー） | FOREIGN KEY(usersテーブルのuser_id) |
| report_date | DATE | 日付(作業日) | NOT NULL |
| condition | TEXT | 体調記録（選択式） | NOT NULL |
| start_time | TIME | 出勤時間 | NOT NULL |
| end_time | TIME | 退勤時間 | NOT NULL |
| work_time | INTEGER | 作業時間（時間単位） | NOT NULL |
| work_detail | TEXT | 作業内容（選択式） | NOT NULL |
| user_comment | TEXT | 利用者の自由コメント欄 | |
| staff_comment | TEXT | 職員によるコメント | |
| created_at | DATETIME | 登録日時 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | 最終更新日時 | DEFAULT CURRENT_TIMESTAMP |