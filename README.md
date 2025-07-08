# Warudo Blueprint Copy Tool

## Overview / 概要

Warudo Blueprint Copy Tool is a GUI utility for copying blueprints (BP) between Warudo scene files (JSON).
Warudo シーンファイル（JSON）間でブループリント（BP）をコピーするための GUI ツールです。

## Features / 主な機能

- Load Warudo scene files (JSON)
- Display blueprint list (ID, name, node count, connection count)
- View blueprint details
- Copy or move blueprints between scenes
- **Keep original ID when copying** (maintain global variable references)
- Auto-rename duplicate names
- Replace existing blueprints
- Create new scene files
- Output blueprint JSON to clipboard
- Copy blueprint ID to clipboard

- Warudo シーンファイル（JSON）の読み込み
- ブループリント一覧の表示（ID、名前、ノード数、接続数）
- ブループリントの詳細表示
- ブループリントのコピー・移動
- **元の ID を保持してコピー**（グローバル変数参照を維持）
- 重複名の自動リネーム
- 既存ブループリントの置換
- 新規シーンファイルの作成
- ブループリントの JSON 出力（クリップボード）
- ブループリント ID のクリップボードコピー

## Requirements / 必要環境

- Python 3.12 or later
- tkinter (usually included with Python)

- Python 3.12 以上
- tkinter（通常、Python に標準で含まれています）

## Usage / 使い方

### English

1. Start the application:
   ```powershell
   WarudoBPCopy_start.bat
   ```
2. Click "Load Source Scene" to select the source scene file.
3. Click "Load Target Scene" to select the target scene file.
4. Select blueprints in the left (Source Scene) panel.
5. Set copy options in the center:
   - Copy/Move: Choose copy or move
   - Replace if exists: Replace if a blueprint with the same name exists
   - Auto-rename duplicates: Automatically rename duplicates
   - Keep original ID: Keep the original ID (maintain global variable references)
6. Click "Copy →" to copy.

### 日本語

1. アプリケーションを起動します:
   ```powershell
   WarudoBPCopy_start.bat
   ```
2. 「Load Source Scene」ボタンでコピー元シーンファイルを選択
3. 「Load Target Scene」ボタンでコピー先シーンファイルを選択
4. 左側（Source Scene）でコピーしたいブループリントを選択
5. 中央のコピーオプションを設定
   - Copy/Move: コピーまたは移動を選択
   - Replace if exists: 同名ブループリントが存在する場合に置換
   - Auto-rename duplicates: 重複名を自動でリネーム
   - Keep original ID: 元の ID を保持（グローバル変数参照を維持）
6. 「Copy →」ボタンでコピー実行

### Other Features / その他の機能

- Right-click menu: View details, rename, output JSON/ID
- Double-click: View blueprint details
- Refresh: Update both scenes
- Create New Scene: Create a new empty scene file

- 右クリックメニュー: 詳細表示、リネーム、JSON/ID 出力
- ダブルクリック: ブループリントの詳細表示
- Refresh: 両シーンの表示を更新
- Create New Scene: 新しい空のシーンファイルを作成

## Important: Keep Original ID / 重要な機能：元の ID を保持

If "Keep original ID" is enabled, the blueprint's ID is preserved.
This allows:

- Maintaining global variable references from other blueprints
- Keeping camera controller and other links working
- Warning if a blueprint with the same ID already exists

「Keep original ID」オプションを有効にすると、ブループリントの ID が元のまま保持されます。
これにより：

- 他のブループリントからのグローバル変数参照が維持される
- カメラコントローラーなどの連携機能が正常に動作する
- 同じ ID のブループリントが既に存在する場合は警告が表示される

**Note:** If a blueprint with the same ID already exists, copying will fail unless "Replace if exists" is enabled.
**注意:** 同じ ID のブループリントが既に存在する場合、「Replace if exists」オプションを有効にしない限りコピーは失敗します。

## File Structure / ファイル構成

```
WarudoBPCopy/
├── main.py                     # Main application / メインアプリケーション
├── README.md                   # This file / このファイル
├── requirements.txt            # Required packages / 必要なパッケージ
└── src/
    ├── __init__.py
    ├── gui/
    │   ├── __init__.py
    │   ├── main_window.py      # Main window / メインウィンドウ
    │   └── blueprint_list_frame.py  # Blueprint list / ブループリントリスト
    ├── models/
    │   ├── __init__.py
    │   └── blueprint_data.py   # Blueprint data management / ブループリントデータ管理
    └── utils/
        ├── __init__.py
        └── json_handler.py     # JSON handling / JSON処理
```

## Notes / 注意事項

- Please make a backup of your scene files before use.
- Large scene files may take time to load.
- Supports Warudo 0.13.1 format scene files.

- シーンファイルのバックアップを作成してから使用することを推奨します
- 大きなシーンファイルの場合、読み込みに時間がかかる場合があります
- Warudo 0.13.1 形式のシーンファイルに対応しています
