import cv2

def capture_image(filename='photos/captured_image.jpg'):
    # Webカメラを初期化
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("カメラを開くことができませんでした")
        return

    # カメラからフレームを読み取る
    ret, frame = cap.read()
    
    if ret:
        # 画像ファイルとして保存
        cv2.imwrite(filename, frame)
        print(f'画像が保存されました: {filename}')
    else:
        print("フレームをキャプチャできませんでした")

    # カメラをリリース
    cap.release()
    cv2.destroyAllWindows()

# 画像をキャプチャして保存
capture_image()