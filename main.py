# -*- coding: utf-8 -*-
# 主函数
import cv2
import io, base64, sys
from PIL import Image  
from apis import Scanner

def main():
    """
    主方法
    一部分为通过摄像头发票识别和处理，另一部分为对于指令做出反应
    """
    scanner = Scanner()

    # 启用摄像头
    cap = cv2.VideoCapture(0)        #'0'选择笔记本电脑自带参数，‘1’为USB外置摄像头
    cap.set(propId=3, value=150)     #设置你想捕获的视频的宽度
    cap.set(propId=4, value=120)     #设置你想捕获的视频的高度
    print("视频捕获启动\n - q:退出 - space: 捕捉")
    while (True):
        _, frame = cap.read()      #读取图像并显示
        cv2.imshow('frame', cv2.flip(frame,1,dst=None))  
       
        c = cv2.waitKey(1)&0xFF
        if c == ord('q'):  #按‘q’键退出后，释放摄像头资源
            cap.release()                    
            cv2.destroyAllWindows()
            print("退出系统")
            break
        elif c == ord('z'):   #按‘z’后，截取图像调用api
            # cv2.imwrite("./test.jpg", frame)
            # image = Image.fromarray(frame)
            img_str = cv2.imencode('.jpg', frame)[1].tostring()
            image_data = base64.b64encode(img_str)
            scanner.scanimg(image_data)


            

    pass

if __name__ == "__main__":
    main()