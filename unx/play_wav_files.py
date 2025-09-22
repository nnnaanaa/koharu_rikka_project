import os
import time
from playsound import playsound

def play_wav_files():
    """
    speakwav フォルダ配下の .wav ファイルを一つずつ再生する
    """
    # このスクリプトが存在するディレクトリ
    base_dir = os.path.dirname(os.path.abspath(__file__))
    wav_dir = os.path.join(base_dir, "speakwav")

    if not os.path.exists(wav_dir):
        print(f"フォルダが見つかりません: {wav_dir}")
        return

    # フォルダ内の wav ファイルを取得（ファイル名昇順でソート）
    wav_files = sorted([f for f in os.listdir(wav_dir) if f.lower().endswith(".wav")])

    if not wav_files:
        print("wav ファイルが存在しません。")
        return

    # 1つずつ再生
    for wav in wav_files:
        wav_path = os.path.join(wav_dir, wav)
        print(f"[再生開始] {wav_path}")
        try:
            playsound(wav_path)  # 同期再生（終わるまで待つ）
            print(f"[再生終了] {wav_path}")
        except Exception as e:
            print(f"再生エラー: {wav_path} ({e})")

        # 少し待機（不要なら削除してOK）
        time.sleep(1)

if __name__ == "__main__":
    play_wav_files()
