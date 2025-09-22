import subprocess
import datetime
import os

def main():
    # このスクリプトが存在するディレクトリ
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 入力フォルダ (speaktext) と出力フォルダ (speakwav)
    input_dir = os.path.join(base_dir, "speaktext")
    output_dir = os.path.join(base_dir, "speakwav")
    os.makedirs(output_dir, exist_ok=True)

    # 出力フォルダ内の既存 wav ファイルを削除
    for f in os.listdir(output_dir):
        if f.lower().endswith(".wav"):
            try:
                os.remove(os.path.join(output_dir, f))
                print(f"[削除] {f}")
            except Exception as e:
                print(f"[警告] {f} の削除に失敗しました: {e}")

    # speaktext 配下のテキストファイルをすべて処理
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            # 出力ファイル名はテキストファイル名に対応した .wav
            basename = os.path.splitext(filename)[0]
            now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            output_filename = f"{basename}_{now_str}.wav"
            output_path = os.path.join(output_dir, output_filename)

            run_voicepeak_tts(input_path, output_path)

    print("すべてのテキストファイルの処理が完了しました。")

def run_voicepeak_tts(input_textfile, output_wavfile):
    """
    VOICEPEAK.exe を使用してテキストファイルを音声ファイルに変換します。
    """
    target_exec_path = r"C:\Program Files\VOICEPEAK\VOICEPEAK.exe"

    command = [
        target_exec_path,
        "-t", input_textfile,   # 読み込むテキストファイル
        "-o", output_wavfile    # 出力する wav ファイル
    ]

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, encoding='utf-8'
        )
        print(f"[OK] {input_textfile} → {output_wavfile}")
        if result.stderr:
            print("標準エラー出力:\n", result.stderr)
    except FileNotFoundError:
        print(f"エラー: 実行ファイル '{target_exec_path}' が見つかりません。パスを確認してください。")
    except subprocess.CalledProcessError as e:
        print(f"エラー: VOICEPEAK.exe 実行中に失敗しました ({input_textfile})")
        print(f"コマンド: {' '.join(e.cmd)}")
        print(f"リターンコード: {e.returncode}")
        print(f"標準出力:\n{e.stdout}")
        print(f"標準エラー出力:\n{e.stderr}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました ({input_textfile}): {e}")

if __name__ == "__main__":
    main()
