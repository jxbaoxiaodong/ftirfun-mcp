[中文](README.zh.md) | [English](README.md) | [Español](README.es.md) | [Français](README.fr.md) | 日本語

# FTIR.fun MCP サーバー

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

**[FTIR.fun](https://ftir.fun)** 向けの MCP サーバーおよび REST API クライアント — オンライン赤外線スペクトルライブラリと材料識別プラットフォーム。

---

## FTIR.fun とは？

**[FTIR.fun](https://ftir.fun)** は、52 カ国以上の研究者やエンジニアに利用されているクラウドベースの赤外分光分析プラットフォームです。ポリマー・添加剤・コーティング・医薬品添加物・工業化学品など、**13 万件以上の FTIR 参照スペクトル**を持つ継続更新ライブラリへの高速アクセスを提供します。

[ftir.fun](https://ftir.fun) の主な機能：

- **スペクトルライブラリ検索** — 測定ファイルをアップロードするか、ピーク位置を入力し、類似度スコアと文献 DOI 付きのランキング結果を取得
- **AI によるピーク解説** — 任意の波数について質問し、化学ナレッジグラフに基づく官能基帰属を取得
- **トライアクシス完全レポート** — 自動多段階材料識別と共有可能な結果 URL の生成
- **画像から CSV への変換** — 論文図版からスペクトル曲線をデジタル化
- **配合解析ワークベンチ** — 多成分逆解析と未知混合物の同定

このパッケージにより、AI アシスタント（Claude・Cursor・VS Code Copilot・Gemini CLI など）やコードパイプラインから、ブラウザに切り替えることなく FTIR.fun を直接呼び出せます。

**ステップバイステップの設定ガイドと API ドキュメント：** https://ftir.fun/ai-integration/

---

## API キーの取得

1. [ftir.fun](https://ftir.fun) にログイン — 新規アカウントには無料試用クレジットが含まれます。
2. **アカウント → API キー** に移動し、**生成** をクリックします。
3. キーをすぐにコピーしてください（`ftir_` で始まり、一度しか表示されません）。

認証は単一ヘッダーで行われます — OAuth もブラウザリダイレクトも不要：

```
# MCP（ホスト型）
Authorization: Bearer ftir_your_key_here

# REST API
X-API-Key: ftir_your_key_here
```

---

## ホスト型 MCP（推奨）

本番エンドポイントに直接接続 — ローカルインストール不要。

### VS Code（GitHub Copilot エージェントモード）

プロジェクトに `.vscode/mcp.json` を作成：

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "ftirfun-api-key",
      "description": "FTIR.fun API key",
      "password": true
    }
  ],
  "servers": {
    "ftirfun": {
      "type": "http",
      "url": "https://ftir.fun/mcp",
      "headers": {
        "Authorization": "Bearer ${input:ftirfun-api-key}"
      }
    }
  }
}
```

コマンドパレット → **MCP: List Servers** → `ftirfun` → **Start** の順に操作します。

### Claude Desktop / Claude Code

```
URL:    https://ftir.fun/mcp
ヘッダー: Authorization: Bearer ftir_your_key_here
```

**Claude Code** のワンライン設定：

```bash
claude mcp add --transport http ftirfun https://ftir.fun/mcp \
  --header "Authorization: Bearer ftir_your_key_here"
```

### Cursor

`~/.cursor/mcp.json` を作成または編集：

```json
{
  "mcpServers": {
    "ftirfun": {
      "url": "https://ftir.fun/mcp",
      "headers": { "Authorization": "Bearer ftir_your_key_here" }
    }
  }
}
```

### Gemini CLI

`~/.gemini/settings.json` を編集：

```json
{
  "mcpServers": {
    "ftirfun": {
      "httpUrl": "https://ftir.fun/mcp",
      "headers": { "Authorization": "Bearer ftir_your_key_here" }
    }
  }
}
```

`/mcp` を実行して `ftirfun` の接続を確認してください。

### テストプロンプト

```
FTIR.fun を使用して 1715 cm-1 の赤外ピークを説明してください。
FTIR ピーク 2915、1715、1450 cm-1 からこのポリマーを識別してください。
FTIR.fun ライブラリでポリプロピレンの参照スペクトルを検索してください。
```

---

## REST API

Python・JavaScript・R・MATLAB・Go など任意の言語から呼び出し可能。LIMS 統合、バッチ処理、独自アプリへの FTIR 検索追加に最適です。

完全な API リファレンス：https://ftir.fun/api-docs/

### ヘルスチェック（キー不要）

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### ピーク位置による未知物質の識別

```bash
curl -X POST https://ftir.fun/ftir/analyze_spectrum \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"peaks": [2915, 1715, 1450, 1260, 1090], "options": {"top_k": 10}}'
```

```python
import requests

resp = requests.post(
    "https://ftir.fun/ftir/analyze_spectrum",
    headers={"X-API-Key": "ftir_your_key_here"},
    json={"peaks": [2915, 1715, 1450, 1260, 1090]},
)
print(resp.json())
```

### 測定ファイルからの識別

```python
import base64, requests

with open("sample.spa", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

resp = requests.post(
    "https://ftir.fun/ftir/analyze_spectrum",
    headers={"X-API-Key": "ftir_your_key_here"},
    json={"file_base64": b64, "filename": "sample.spa"},
)
print(resp.json())
```

28 以上のフォーマット対応：Thermo `.spa`/`.spc`・Bruker `.opus`・PerkinElmer `.sp`・JCAMP-DX・CSV・Excel など。

---

## ツール一覧

| ツール名 | 説明 |
|----------|------|
| `parse_ftir_spectrum` | base64 エンコードされた測定ファイルを解析 |
| `analyze_ftir_spectrum` | 未知スペクトルのライブラリ検索 |
| `submit_ftir_report` | トライアクシスワークフローへのスペクトル送信 |
| `get_ftir_report_status` | 送信済みレポートのステータス確認 |
| `explain_peaks` | フル検索なしでピークを解説 |
| `find_spectra` | 名称・CAS 番号・キーワードで参照スペクトルを検索 |
| `fetch_result` | レポート番号で過去の結果を取得 |

---

## ローカルプロキシ（セルフホスト）

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
pip install ftirfun-mcp
ftirfun-mcp
```

---

## リンク集

| リソース | URL |
|----------|-----|
| ウェブサイト | https://ftir.fun |
| 設定ガイド | https://ftir.fun/ai-integration/ |
| API ドキュメント | https://ftir.fun/api-docs/ |
| MCP エンドポイント | https://ftir.fun/mcp |
| Smithery | https://smithery.ai/servers/hlin2097/ftirfun |
| PyPI | https://pypi.org/project/ftirfun-mcp/ |
