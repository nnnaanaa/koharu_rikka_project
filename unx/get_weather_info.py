"""
指定されたURLから天気情報を取得し、140文字以内で日本語に対応して分割し、
speaktextフォルダ配下にテキストファイルとして出力するスクリプト
"""

import requests
import json
import os
import re

TARGET_URL = "https://weather.tsukumijima.net/api/forecast?city=110010"

def split_text_by_words(text, max_len=140):
    """
    日本語対応版: 文章を句読点や空白で区切り、max_len以内にまとめる。
    区切りが無い長文は強制的に分割する。
    """
    # 区切り文字（。、やスペース）を保持して分割
    tokens = re.split(r'([。、\s])', text)
    chunks = []
    current_chunk = ""

    for token in tokens:
        if not token:  # 空文字はスキップ
            continue

        # 次を追加すると max_len を超えるなら確定
        if len(current_chunk) + len(token) > max_len:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = token
        else:
            current_chunk += token

        # token が極端に長く、max_len を超える場合は強制分割
        while len(current_chunk) > max_len:
            chunks.append(current_chunk[:max_len])
            current_chunk = current_chunk[max_len:]

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def get_weather_info():
    target_url = TARGET_URL

    try:
        response = requests.get(target_url)
        response.raise_for_status()

        # JSONレスポンスをパース
        weather_data = response.json()

        # 今日の天気を取得
        weather_data_today = weather_data["forecasts"][0]

        # 各要素を取得
        weather_data_today_info = {
            "date": weather_data_today["date"],
            "telop": weather_data_today["telop"],
            "detail": weather_data_today["detail"]["weather"],
            "max_temp": weather_data_today["temperature"]["max"]["celsius"] if weather_data_today["temperature"]["max"] else "N/A",
            "min_temp": weather_data_today["temperature"]["min"]["celsius"] if weather_data_today["temperature"]["min"] else "N/A",
            "description": weather_data["description"]["text"].replace("\n", "").replace("　", "").strip()
        }

        # 見出し文を作成
        weather_headline = (
            f"{weather_data_today['dateLabel']}、{weather_data_today_info['date']} の天気情報です。"
            f"天気は {weather_data_today_info['telop']}、"
            f"最高気温は {weather_data_today_info['max_temp']} 度、"
            f"最低気温は {weather_data_today_info['min_temp']} 度です。"
        )

        # 説明文
        weather_description = weather_data_today_info["description"]

        # 全体のテキスト
        weather_today = f"{weather_headline}\n{weather_description}"

        # 出力先ディレクトリを準備
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, "speaktext")
        os.makedirs(output_dir, exist_ok=True)

        # 日本語対応で140文字以内に分割
        chunks = split_text_by_words(weather_today, max_len=140)

        for idx, chunk in enumerate(chunks, start=1):
            output_filename = os.path.join(output_dir, f"weather_info_part{idx}.txt")
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(chunk)
            print(f"天気情報の一部が {output_filename} に出力されました。")

        print("\n--- 出力された天気情報 ---")
        for idx, chunk in enumerate(chunks, start=1):
            print(f"[Part {idx}] {chunk}")

    except requests.exceptions.RequestException as e:
        print(f"リクエスト中にエラーが発生しました: {e}")
    except json.JSONDecodeError:
        print("エラー: JSONレスポンスをデコードできませんでした。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    # 出力フォルダ内の既存 wav ファイルを削除
    for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "speaktext")):
        if f.lower().endswith(".txt"):
            try:
                os.remove(os.path.join(output_dir, f))
                print(f"[削除] {f}")
            except Exception as e:
                print(f"[警告] {f} の削除に失敗しました: {e}")


    get_weather_info()
