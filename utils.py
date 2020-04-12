
import os,csv,cv2,base64

def nparr2base64(npimg):
    """
    方法--日志保存
    将识别记录写入文件夹下work_log.csv文件
    若无此文件则自动创建并写入表头
    """

    img_str = cv2.imencode('.jpg', npimg)[1].tostring()  # 将图片编码成流数据，放到内存缓存中，然后转化成string格式
    return base64.b64encode(img_str) # 编码成base64

def save_to_csv(invoice_data,filename):
    """
    方法--日志保存
    将识别记录写入给定文件夹下文件
    若无此文件则自动创建并写入表头
    """
    if filename not in os.listdir("./data"):
        not_found = True
    else:
        not_found = False

    with open(f"./data/{filename}", 'a+',newline='',encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        if not_found:
            writer.writerow(invoice_data.keys())
        writer.writerow(invoice_data.values())