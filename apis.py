import base64
import csv
import os
import time
import requests
from config import api_config
from utils import save_to_csv

class Scanner:
    """
    发票识别类
    使用百度发票识别API，免费使用额度为每日500次
    官方地址 https://ai.baidu.com/docs#/OCR-API/5099e085
    其它功能及配置请移步官网
    """
    def __init__(self,quality="normal"):
        self.access_token = api_config['access_token']
        self.api_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice?access_token={self.access_token}"
        # 识别quality可选high及normal
        # normal（默认配置）对应普通精度模型，识别速度较快，在四要素的准确率上和high模型保持一致，
        # high对应高精度识别模型，相应的时延会增加，因为超时导致失败的情况也会增加（错误码282000）
        self.quality = quality  
        self.header = {"Content-Type": "application/x-www-form-urlencoded"}

    def scanimg(self,image_data):
        """
        提交表单
        需求base64图片
        """
        try:
            data = {"accuracy": self.quality, "image": image_data}
            response = requests.post(self.api_url, data=data, headers=self.header)
            if response.status_code != 200:
                print(time.ctime()[:-5], "Failed to get info")
                return None
            else:
                
                result = response.json()["words_result"]
                print("- ",result)
                invoice_data = {
                    '检索日期': '-'.join(time.ctime().split()[1:3]),
                    "发票类型": result["InvoiceType"],
                    '发票代码': result['InvoiceCode'],
                    '发票号码': result['InvoiceNum'],
                    '开票日期': result['InvoiceDate'],
                    '合计金额': result['TotalAmount'],
                    '税率': result['CommodityTaxRate'][0]['word'],
                    '合计税额': result['TotalTax'],
                    '价税合计': result['AmountInFiguers'],
                    '销售方名称': result['SellerName'],
                    '销售方税号': result['SellerRegisterNum'],
                    '购方名称': result['PurchaserName'],
                    '购方税号': result['PurchaserRegisterNum'],
                    '备注': result['Remarks'],
                    
                }
                save_to_csv(invoice_data, "test.csv")
                return invoice_data
        except:
            message = "发票识别API调用出现错误"
            # Pushover.push_message(message)
            return None
        finally:
            print(time.ctime()[:-5], "产生一次了调用")

    