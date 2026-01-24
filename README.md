<!-- README.md (日本語版) -->
# ComfyUI Docker コンテナ

これは、Docker コンテナ上で [ComfyUI](https://github.com/comfyanonymous/ComfyUI) を起動するためのプロジェクトです。  
[English README](docs/README_EN.md) はこちら。

## 概要

本プロジェクトは、Docker Compose とマルチステージ Dockerfile を用いて、ComfyUI を効率的にビルド・実行するための設定ファイルとスクリプトを提供します。

## 構成ファイル

- **docker-compose.yaml**  
  コンテナのビルドおよび実行に必要な各種設定が記述されています。
- **Dockerfile**  
  Builder ステージと Runtime ステージに分かれており、Python、CUDA、その他の必要な依存関係をインストールします。
- **entrypoint.sh**  
  コンテナ起動時に実行され、ComfyUI のリポジトリのクローン、依存パッケージのインストール、Web UI の起動を行います。

## 使い方

1. リポジトリをクローンします。

   ```bash
   git clone <リポジトリURL>
   cd <リポジトリディレクトリ>
   ```

2. Docker Compose を用いてビルドし、コンテナを起動します。

    ```bash
    docker compose up -d --build
    ```  

3. ブラウザで [ローカルコンテナ](http://localhost:8188) にアクセスし、ComfyUI の Web UI を確認してください。

## 注意事項

- NVIDIA GPU を活用する設定が含まれています。GPU 利用時は、適切な NVIDIA ドライバーおよび Docker の NVIDIA コンテナツールキットの導入が必要です。
- タイムゾーンは `Asia/Tokyo` に設定されています。必要に応じて変更してください。

## ライセンス

本プロジェクトのライセンスは、各自のプロジェクト方針に従います。詳細は LICENSE ファイルをご確認ください。

## インストールを推奨するカスタムノード

- WAS Node Suite
- Comfy-Custom-Scripts

## uvチェックでComfyUI-Managerのprestartup_script.pyの実行が失敗する

### エラー内容

コンテナの実行時に以下のエラーメッセージが表示される

```bash
[ComfyUI-Manager] Neither `python -m pip` nor `uv` are available. Cannot proceed with package operations.

Failed to execute startup-script: /home/{USER}/ComfyUI/custom_nodes/ComfyUI-Manager/prestartup_script.py / Neither `pip` nor `uv` are available for package management
```

### 対処方法

ComfyUI-Managerのprestartup_script.pyでpipを使用する場合は/home/{USER}/ComfyUI/user/__manager/config.iniの
use_uvをFalseに修正します
