# === Stage 1: Builder ===
FROM ubuntu:22.04 AS builder

# 非対話モード
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    tzdata \
    software-properties-common \
    wget \
    gnupg2 && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo "$TZ" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# deadsnakes リポジトリの追加
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update

# Python 3.11、pip、git のインストール
RUN apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    git && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    python3 -m pip install --upgrade pip setuptools wheel

# CUDA ランタイムのセットアップ
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends cuda-runtime-12-4 && \
    rm -rf /var/lib/apt/lists/*

# グローバル（デフォルト）のインストール先へ pip パッケージをインストール
RUN python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 && \
    python3 -m pip install pyyaml requests && \
    python3 -m pip cache purge

# === Stage 2: Runtime 環境 ===
FROM ubuntu:22.04 AS runtime

# 非対話モード
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    tzdata \
    software-properties-common \
    wget \
    gnupg2 \ 
    gosu && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo "$TZ" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# deadsnakes リポジトリの追加と Python 3.11、pip、git のインストール
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && \
    apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    git && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# CUDA ランタイムのセットアップ（runtime 側）
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends cuda-runtime-12-4 && \
    rm -rf /var/lib/apt/lists/*

# builder でグローバルにインストールしたパッケージとスクリプトをコピー
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# --- ここからユーザ関連の設定 ---
# ビルド引数でログインユーザ情報を受け取る
ARG APP_USER
ARG UID
ARG GID

# 非rootユーザ作成
# ユーザーのホームディレクトリに ComfyUI を設置
RUN groupadd -g ${GID} ${APP_USER} && \
    useradd -m -u ${UID} -g ${GID} ${APP_USER}
WORKDIR /home/${APP_USER}

# ホストのrequirements.txtをコピー
COPY requirements.txt /tmp/requirements.txt

# Python の依存パッケージをインストール
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Entrypoint のシェルスクリプトをコピー
COPY entrypoint.sh /home/${APP_USER}/entrypoint.sh
RUN chmod +x /home/${APP_USER}/entrypoint.sh && chown -R ${APP_USER}:${APP_USER} /home/${APP_USER}/
# --- ここまでユーザ関連の設定 ---

# Web UI 用のポートを公開
EXPOSE 8188

# コンテナ起動時に entrypoint.sh を実行（非rootユーザで実行）
USER ${APP_USER}
ENTRYPOINT ["sh", "-c", "/home/${APP_USER}/entrypoint.sh"]
