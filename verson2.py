#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime

def plan_v7(x1):
    put_info = []
    money = []
    winp = 0.97885
    lostp = 1.2
    x = x1
    #     循环开始
    while True:
        try:
    #         需要变动的请求内容
            token = '5a7i6ga7cacq8i9tzdsrpcpl1a1t7agc4hlesrtc'
            unix = '1572489038'
            keycode = 'c09207153ab42b0bfc5b40f440ca1178'

            part = 'ptype=1&deviceid=6F9BCDBE-7730-43E7-9D36-B152FA0B7B9C&token=' + token + '&unix='+ unix + '&userid=28069084&keycode=' + keycode + '&phonemodel=iPhone+7&osversion=13.1.3&simtype=0&simid=&resolution=&mac=02:00:00:00:00:00&appversion=1.4.0&channelid=1&ruserid=0'
        #     获取时间
            url = 'http://ifsapp.pceggs.com/IFS/Riddle28/riddle28_List.ashx?' + part 
            params = {
                      'ptype':'1',
                      'deviceid':'6F9BCDBE-7730-43E7-9D36-B152FA0B7B9C',
                      'token': token,
                      'unix': unix,
                      'userid':'28069084',
                      'keycode': keycode,
                      'phonemodel':'iPhone+7',
                      'osversion':'13.1.3',
                      'simtype':'0',
                      'simid':'',
                      'resolution':'',
                      'mac':'02:00:00:00:00:00',
                      'appversion':'1.4.0',
                      'channelid':'1',
                      'ruserid':'0',}
            headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
            params = json.dumps(params)
            response = requests.get(url,headers=headers,params=params,timeout=5).json()
            money.append(response['data']['items'][3]['tmoney'])
            if response['data']['items'][3]['tmoney'] > 0:
                odds = response['data']['items'][3]['tmoney']
                biaoji = 1
            else:
                odds = 0
                biaoji = 0
            if len(np.array(money)) > 1:
                if response['data']['items'][3]['tmoney'] != 0:
                    if biaoji == 1 :
                        if x <= 20:
                            x = 20
                        else:
                            x *= winp
                    else:
                        if response['data']['items'][3]['tmoney'] < x*(-500) :
                            if x <= 20000:
                                x *= lostp
            print('$【{0}】,X【{1:.0f}】'.format(np.array(money).sum()-np.array(money)[0],x),end=",")       
            countdown = response['data']['items'][2]['countdown']      # 剩余时间
            number = response['data']['items'][2]['number']            # 即将open
            if countdown == 0:
                print('------------------------已超时，跳过本次！------------------------')
                time.sleep(20)
                continue
            print('ID: {}'.format(number),end=",【")
        #     判断是否在设定时间之内,不是继续等待   ====================================================
            s = 7
            if int(countdown) > s:
                time.sleep(int(countdown)-s)
        #     获取概率分布以及目标概率分布定义
            dict = {'sort':[1050.00,349.97,175.03,105.00,69.99,49.99,37.50,29.16,23.33,19.09,16.66,15.21,14.37,14.00,14.00,14.37,15.21,16.66,19.09,23.33,29.16,37.50,49.99,69.99,105.00,175.03,349.97,1050.00],
                    'main':[1,3,6,10,15,21,28,36,45,55,63,69,73,75,75,73,69,63,55,45,36,28,21,15,10,6,3,1],
                    'now':[]}        
            url1 = 'http://ifsapp.pceggs.com/IFS/Riddle28/riddle28_Betting_Odds.ashx?issueid='+str(int(number))+'&' + part
            response = requests.get(url1,headers=headers,params=params,timeout=5).json()

            for i in range(28):
                dict['now'].append(float(response['data']['items'][0]['c'+str(i)]))
            data = pd.DataFrame(dict)
    #==================================设置倍率(原始1000)=======================================   
            money_up = 950 * x
            money_down = 900 * x
    # ==========================================================================================
            data['main'] = data['main'] * x
            data['main'] = data['main'].astype("int")
            df = data['main'].copy()
# --------------------------------------------------------------------------------------------------------------            
            for i in range(28):
                data.iloc[i,0] = data.iloc[i,1] * data.iloc[i,2]
            df1 = data['sort'].copy()
#             df1 = abs(df1 - 1000*x)
            df1 = df1 - 1000*x
            df2 = df1.sort_values().copy()
            for i in range(20):
                if df.sum() > money_down:
                    if df.sum() - data.iloc[int(df2.index[i]),1] > money_down:
                        df[int(df2.index[i])] = 0
                        print('{}'.format(df2.index[i]),end=",")
                else:
                    break
            leiji = df.sum()        
# --------------------------------------------------------------------------------------------------------------
            put_info.append(leiji)      
            if leiji > 0 :              
                ls = [str(i) for i in list(df)]     # 列表元素转为str
                xstr = ",".join(ls)        # 结果字符串
                print('】投入【{}】'.format(leiji),end=",")
                url2 = 'http://ifsapp.pceggs.com/IFS/Riddle28/riddle28_Betting.ashx?issue='+str(number)+'&totalgoldeggs='+str(leiji)+'&bettinglist='+xstr+'&' + part
                time.sleep(3)
                response = requests.get(url2,headers=headers,params=params,timeout=5).json()
            #     判断是否成功
                print(response['msg'],end=",")
                if response['msg'] == '成功':     # 判断下是否成功
#                     f = open('埋点数据.csv','a')
#                     f.write(str(number)+','+str(np.array(money).sum()-np.array(money)[0])+','+str(leiji)+','+str(datetime.now().time())+','+str(biaoji)+','+str(len(np.array(money)))+','+str(int(x))+'\n')
#                     f.close()
                    print(time.strftime('%H:%M:%S ',time.localtime(time.time())))
                    time.sleep(30)
                    time.sleep(30)
                    time.sleep(30)
                else:
                    print('跳过本次')
                    time.sleep(30)
            else:
                print('暂无好的方案,跳过本期')
                time.sleep(110)
        except Exception as e:
            print('出现错误!')
            print(e)
            time.sleep(50)
            
plan_v7(60)   

