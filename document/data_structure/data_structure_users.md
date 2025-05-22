| 項目名 | 型 | 説明 | 制約 |
|-|-|-|-|
| user_id | INTEGER | ユーザID(各ユーザを一意に識別) | 主キー(PRIMARY KEY) |
| username | TEXT | ログイン用ユーザ名 | NOT NULL |
| password | TEXT | ハッシュ化されたパスワード | NOT NULL |
| name | TEXT | 表示名（本名） | NOT NULL |
| role | TEXT | ユーザ種別(user=利用者、staff=職員) | NOT NULL |
| created_at | DATETIME | 登録日時 | DEFAULT CURRENT_TIMESTAMP |