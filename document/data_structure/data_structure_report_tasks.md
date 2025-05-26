### 日報データの中間テーブル【report_tasksテーブル】 
| 項目名 | 型 | 説明 | 制約 |
|-|-|-|-|
| task_id | INTEGER | 日報ID(各作業を一意に識別) | 主キー(PRIMARY KEY) |
| report_id | INTEGER | 日報ID(reportsテーブルの外部キー) | FOREIGN KEY(reportsテーブルのreport_id) |
| task_order | INTEGER | 作業の並び順(1～3) | NOT NULL |
| task_name | TEXT | 作業名(選択式) | NOT NULL |
| task_duration | INTEGER | 作業時間(時間単位) | NOT NULL |
| task_note | TEXT | 利用者コメント | |