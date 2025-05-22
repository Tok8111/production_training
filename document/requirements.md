# 要件定義書（日報作成アプリ（仮称））
2025年1月～5月Java+Pythonプログラマー養成科における制作実習のリポジトリ

## 1.概要
- アプリ名称：日報作成アプリ（仮称）
- 対象：就労移行支援・就労継続A型支援事業所の利用者・職員
- 目的：利用者が日々の業務報告（日報）を簡便に記録・提出できる仕組みを提供することで、職員による確認・フィードバックを円滑化する。

## 2.想定ユーザ、役割
| ユーザ区分 | 概要・役割 |
|-|-|
| 利用者 | 業務終了後に日報をスマートフォン／PCから入力 |
| 職員 | 利用者の日報を確認し、コメントやフィードバックを入力 |

## 3.利用シナリオ（ユースケース）
- 利用者はログイン後、自分の日報入力画面から当日の内容（出退勤時間、作業内容、体調など）を入力・保存  
- 職員は一覧画面から日報を閲覧し、必要に応じてコメントを追記・保存  
- 利用者は過去の日報履歴を閲覧可能  

## 4.アプリの主な機能
| 区分 | 機能名 | 概要 |
|-|-|-|
| 共通 | ログイン機能 | 利用者・職員に応じた認証処理 |
| 利用者用 | 日報入力 | 出退勤時間、作業内容、体調、作業時間、自由記述欄などを入力 |
| 職員用 | 日報一覧表示 | 利用者ごとの日報を日付順に表示し、コメントを入力 |
| 共通 | 履歴閲覧機能 | 過去の日報データの一覧表示・閲覧 |

## 5.画面構成(予定)
| 画面名 | 対象ユーザ | 機能概要 |
|-|-|-|
| ログイン画面 | 全員 | ユーザ認証（利用者／職員） |
| 日報入力画面 | 利用者 | 日報内容を入力・保存 |
| 日報一覧／確認画面 | 職員 | 利用者の日報一覧を確認し、コメント記入 |
| 履歴閲覧画面 | 利用者 | 自分の過去の日報を確認可能 |

## 6.ユーザデータ構造（共通テーブル）【usersテーブル】
| 項目名 | 型 | 説明 | 制約 |
|-|-|-|-|
| user_id | INTEGER | ユーザID(各ユーザを一意に識別) | 主キー(PRIMARY KEY) |
| username | TEXT | ログイン用ユーザ名 | NOT NULL |
| password | TEXT | ハッシュ化されたパスワード | NOT NULL |
| name | TEXT | 表示名（本名） | NOT NULL |
| role | TEXT | ユーザ種別(user=利用者、staff=職員) | NOT NULL |
| created_at | DATETIME | 登録日時 | DEFAULT CURRENT_TIMESTAMP |

## 7.日報データ構造（想定DB項目）【reportsテーブル】
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
| user_comment | TEXT | 利用者の自由コメント欄 | NOT NULL |
| staff_comment | TEXT | 職員によるコメント | NOT NULL |
| created_at | DATETIME | 登録日時 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | 最終更新日時 | DEFAULT CURRENT_TIMESTAMP |

## 8.日報データの中間テーブル【report_tasksテーブル】
| 項目名 | 型 | 説明 | 制約 |
|-|-|-|-|
| task_id | INTEGER | 日報ID(各作業を一意に識別) | 主キー(PRIMARY KEY) |
| report_id | INTEGER | 日報ID(reportsテーブルの外部キー) | FOREIGN KEY(reportsテーブルのreport_id) |
| task_order | INTEGER | 作業の並び順(1～3) | NOT NULL |
| task_name | TEXT | 作業名(選択式) | NOT NULL |
| task_duration | INTEGER | 作業時間(時間単位) | NOT NULL |

## 9.使用技術・環境（予定）
| 項目 | 使用予定技術 |
|-|-|
| フロントエンド | HTML / CSS / JavaScript (Bootstrap) |
| バックエンド | Pythom (Flask) |
| データベース | SQLite |
| 開発環境 | VSCode (ローカル開発) |
| その他 | Git、レスポンシブ対応設計 |


## 10.開発スケジュール

| 日付(目安) | 作業内容 |
|-|-|
| 1日目（2025年5月15日） | 要件定義・画面設計 |
| 2日目（2025年5月16日） | 画面デザイン |
| 3日目（2025年5月20日） | ログイン機能、日報投稿画面の実装 |
| 4日目（2025年5月21日） | 日報の閲覧機能の実装 |
| 5日目（2025年5月22日） | 職員側の機能（一覧表示、コメント入力）実装 |
| 6日目（2025年5月23日） | UI調整・スマホ対応 |
| 7日目（2025年5月26日） | 動作確認・バグ修正 |
| 8日目（2025年5月27日） | ドキュメント(マニュアル)作成・発表資料作成/準備 |
| 9日目（2025年5月28日） | （バッファ） |
