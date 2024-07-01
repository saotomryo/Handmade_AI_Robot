from bot_create_speech import speech
from bot_listner import speech2text
import llms
import take_photo
import motor
import os
import json
import warnings
import time

warnings.simplefilter('ignore')

os.environ["GOOGLE_API_KEY"] = "ここにAPIキーを保存する"


def main():
    continue_flag = True
    speech("こんにちは、お話しましょう")
    #motorドライバの初期化
    my_motor = motor.Motor()
    # llmの初期化
    my_llms = llms.llm_function()
    my_llms.set_template()
    my_llms.create_comversation()
    #myled = led.led()
    i = 0
    while continue_flag:
        #myled.led_on()
        result_text = speech2text()
        #myled.led_off()
        if (("終わり" in result_text) or ("おわり" in result_text) or (result_text == "")):
            continue_flag = False
            speech("また、遊びましょう")
            my_motor.destroy()
            break
        
        if i==0:
           return_message = my_llms.send_message("お話ししましょう")
        return_message = my_llms.send_message(result_text)
        print(return_message)
        i+=1
        try:
            tmp_message = str(return_message).replace("json","").replace("`","")
            return_dict = json.loads(tmp_message)
            print(return_dict)
            print(return_dict["返事"])
            speech(return_dict["返事"])
            if return_dict["前進"] == 1:
                print("前に進みます")
                my_motor.move(1)
                time.sleep(5)
                print("止まります")
                my_motor.move(0)
            if return_dict["後退"] == 1:
                print("後ろに行きます")
                my_motor.move(-1)
                time.sleep(5)
                print("止まります")
                my_motor.move(0)

            if return_dict["右"] == 1:
                print("右に回ります")
                my_motor.move(2)
                time.sleep(5)
                print("止まります")
                my_motor.move(0)

            if return_dict["左"] == 1:
                print("左に回ります")
                my_motor.move(3)
                time.sleep(5)
                print("止まります")
                my_motor.move(0)

            if return_dict["撮影"] == 1:
                print("写真を撮ります")
                take_photo.capture_image()
                return_message = my_llms.send_photos(result_text,"photo/captured_image.jpg")
                tmp_message = str(return_message).replace("json","").replace("`","")
                return_dict = json.loads(tmp_message)
                speech(return_dict["返事"])
                print(return_dict["返事"])
            if return_dict["感情"] == 1:
                print("嬉しいので前後に動きます")
                my_motor.move(1)
                time.sleep(3)
                print("止まります")
                my_motor.move(0)
                time.sleep(3)
                my_motor.move(-1)
                time.sleep(3)
                print("止まります")
                my_motor.move(0)
        except Exception as e:
            print("エラー")
            print(str(e))
            pass
        
        if return_message == "":
            continue_flag = False
        #speech(return_message)
       


if __name__ == "__main__":
    main()
