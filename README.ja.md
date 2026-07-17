[中文](README.zh.md) | [English](README.md) | [Español](README.es.md) | [Français](README.fr.md) | 日本語

# FTIR.fun MCP サーバー

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

**[FTIR.fun](https://ftir.fun)** 向けの MCP サーバーおよび REST API クライアント — AI アシスタントやコードパイプラインから 13 万件以上の FTIR 赤外参照スペクトルに直接アクセスし、材料識別・ピーク解説・スペクトルライブラリ検索が行えます。

## ツール一覧

| ツール | 機能 |
|--------|------|
| [`analyze_ftir_spectrum`](#analyze_ftir_spectrum) | 未知 FTIR スペクトルの識別 — ピーク、自然言語クエリ、測定ファイル（28+ 形式）に対応。類似度スコアと文献 DOI 付きランキング結果を返却。 |
| [`explain_peaks`](#explain_peaks) | 赤外ピーク位置の解説 — フル検索なしで官能基帰属を取得。 |
| [`parse_ftir_spectrum`](#parse_ftir_spectrum) | FTIR 測定ファイルを解析し、波数-強度データ点と検出ピークを出力。 |
| [`find_spectra`](#find_spectra) | 13 万+ 参照ライブラリを物質名・CAS 番号・キーワードで検索。比較用カーブデータを返却。 |
| [`submit_ftir_report`](#submit_ftir_report) | スペクトルをトライアクシスワークフローに送信（ウェブサイトと同じ多段階分析）。 |
| [`get_ftir_report_status`](#get_ftir_report_status) | レポート進捗をポーリング；完了時に構造化結果と共有 URL を返却。 |
| [`fetch_result`](#fetch_result) | レポート番号で任意の FTIR.fun 過去分析結果を取得。 |

---

## API キーの取得

1. [ftir.fun](https://ftir.fun) にログイン — 新規アカウントには無料試用クレジットが含まれます。
2. **アカウント → API キー** に移動し、**生成** をクリック。
3. キーをすぐにコピー（`ftir_` で始まり、一度しか表示されません）。

```
# MCP（ホスト型）
Authorization: Bearer ftir_your_key_here

# REST API
X-API-Key: ftir_your_key_here
```

---

## MCP ツール

ホスト MCP エンドポイント `https://ftir.fun/mcp` は七つのツールを提供します。

---

### `analyze_ftir_spectrum`

FTIR 赤外スペクトルライブラリで未知スペクトルを検索。ピーク、自然言語クエリ、または測定ファイルを受け付けます。

**パラメータ**

| パラメータ | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `query` | string | いいえ | 自然言語の FTIR リクエスト — ピーク位置は自動抽出されます。 |
| `peaks` | number[] | いいえ | FTIR ピーク位置 cm⁻¹（例：`[1736, 1379, 1241]`）。 |
| `file_base64` | string | いいえ | Base64 エンコードの FTIR 測定ファイル。28+ 形式対応。 |
| `filename` | string | いいえ | 形式検出用の元ファイル名。 |
| `top_k` | integer | いいえ | 返却する候補数（1–50、デフォルト 15）。 |
| `tolerance_cm1` | integer | いいえ | ピーク一致許容範囲 cm⁻¹（1–30、デフォルト 8）。 |

**返却：** 候補材料ランキング、類似度スコア、ピーク毎の証拠（DOI）、信頼度。

**例**
```
この赤外スペクトルを識別：ピーク 2915、1715、1450、1260、1090 cm-1。
```

---

### `explain_peaks`

フル検索なしで FTIR 赤外ピークを解説。

**パラメータ**

| パラメータ | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `query` | string | いいえ | 自然言語のピーク質問。 |
| `peaks` | number[] | いいえ | ピーク位置 cm⁻¹。 |
| `sampling_mode` | string | いいえ | `ATR`、`Thin Film`、`KBr Pellet` 等。 |

---

### `parse_ftir_spectrum`

Base64 エンコードの FTIR 測定ファイルを解析し、整列済み曲線点と検出ピークを返却。

**パラメータ**

| パラメータ | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `file_base64` | string | はい | Base64 エンコードの FTIR ファイル。 |
| `filename` | string | はい | 元ファイル名。 |

---

### `find_spectra`

物質名・CAS 番号・キーワードで FTIR 参照スペクトルを検索。

**パラメータ**

| パラメータ | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `query` | string | はい | 物質名、CAS、`NUM`、またはキーワード。 |
| `limit` | integer | いいえ | 結果数（1–20、デフォルト 10）。 |

---

### `submit_ftir_report`

スペクトルを FTIR.fun トライアクシスワークフローに送信。`task_id` と `result_num` を即時返却。

**パラメータ**

| パラメータ | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `file_base64` | string | はい | Base64 エンコードの FTIR ファイル。 |
| `filename` | string | はい | 元ファイル名。 |

---

### `get_ftir_report_status`

送信済みレポートのステータスを確認。完了時に `report_view` と `report_url` を返却。

**パラメータ**

| パラメータ | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `task_id` | string | はい | `submit_ftir_report` が返した `task_id`。 |

---

### `fetch_result`

レポート番号で FTIR.fun の過去分析結果を取得。

**パラメータ**

| パラメータ | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `result_num` | string | はい | FTIR.fun レポート番号。 |
| `language_code` | string | いいえ | 表示言語（デフォルト `en`）。 |

---

## REST API

Python・JavaScript・R・MATLAB・Go など任意の言語から呼び出し可能。LIMS 統合、バッチ赤外スペクトル処理、独自アプリへの検索追加に最適。

完全な API リファレンス：https://ftir.fun/api-docs/

### ヘルスチェック（キー不要）

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### ピーク位置による未知赤外スペクトルの識別

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

### 赤外ピークの解説

```bash
curl -X POST https://ftir.fun/ftir/explain_peaks \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"peaks": [1715, 2915], "sampling_mode": "ATR"}'
```

---

## MCP クライアント設定

ホスト MCP エンドポイントはローカルインストール不要。URL：`https://ftir.fun/mcp`、`Bearer` トークン使用。

### VS Code

```json
{
  "inputs": [
    { "type": "promptString", "id": "ftirfun-api-key", "description": "FTIR.fun API key", "password": true }
  ],
  "servers": {
    "ftirfun": {
      "type": "http",
      "url": "https://ftir.fun/mcp",
      "headers": { "Authorization": "Bearer ${input:ftirfun-api-key}" }
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http ftirfun https://ftir.fun/mcp \
  --header "Authorization: Bearer ftir_your_key_here"
```

### Cursor

```json
{ "mcpServers": { "ftirfun": { "url": "https://ftir.fun/mcp", "headers": { "Authorization": "Bearer ftir_your_key_here" } } } }
```

### Gemini CLI

```json
{ "mcpServers": { "ftirfun": { "httpUrl": "https://ftir.fun/mcp", "headers": { "Authorization": "Bearer ftir_your_key_here" } } } }
```

---

## ローカルプロキシ（セルフホスト）

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
pip install ftirfun-mcp
ftirfun-mcp
```

---

## FTIR.fun について

**[FTIR.fun](https://ftir.fun)** は、52 カ国以上の研究者やエンジニアに利用されているクラウドベースの赤外分光分析プラットフォームです。**13 万件以上の FTIR 参照スペクトル**を持つ継続更新ライブラリへの高速アクセスを提供します。

[ftir.fun](https://ftir.fun) の機能：

- **スペクトルライブラリ検索** — 類似度スコアと文献 DOI 付きランキング結果
- **AI ピーク解説** — 化学ナレッジグラフに基づく官能基帰属
- **トライアクシス完全レポート** — 多段階材料識別と共有 URL
- **画像→CSV 変換** — 論文図版からスペクトル曲線をデジタル化
- **配合解析ワークベンチ** — 多成分逆解析

設定ガイド：https://ftir.fun/ai-integration/

---

## リンク集

| リソース | URL |
|----------|-----|
| ウェブサイト | https://ftir.fun |
| 設定ガイド | https://ftir.fun/ai-integration/ |
| API ドキュメント | https://ftir.fun/api-docs/ |
| MCP エンドポイント | https://ftir.fun/mcp |
| Server card | https://ftir.fun/.well-known/mcp/server-card.json |
| Smithery | https://smithery.ai/servers/hlin2097/ftirfun |
| MCP.so | https://mcp.so/server/ftir-spectral-search/ftir_fun |
| PyPI | https://pypi.org/project/ftirfun-mcp/ |
