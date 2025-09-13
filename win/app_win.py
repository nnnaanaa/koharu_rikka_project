from get_weather_info import get_weather_info
from create_wav import main as cmain
from play_wav_files import play_wav_files

def main():
    # 天気情報を取得してテキストファイルに保存
    get_weather_info()
    # テキストファイルから音声ファイルを生成
    cmain()
    # 生成された音声ファイルを再生
    play_wav_files()
    


if __name__ == "__main__":
    main()
