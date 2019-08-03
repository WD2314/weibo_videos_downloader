import requests,time,json
import os
#from tqdm import tqdm
import subprocess
import re
from urllib import request

def rm(string):
               
    #windows文件名不能含 <>?\/:|*"  字符 

    illeagal_list = ['\r','\f','\n','\t','<','>','\?',"\\\\",'/',':','\|','\\*','\"','\'']
    replace = '_'
    a = string
    '''
    if(not a):
        a='xyz<>?\/:|*"456<>?\/:|*"abc'

    print('原字符：\n',a,'\n')
    '''
    for i in illeagal_list:
        p=re.compile(i)
        a = p.sub(replace,a)
    print('处理后：\n',a,'\n')
    return(a)



def info2txt(page,url,date,title):
    f=open("page_"+page+'.txt','a+',encoding="utf-8")
    f.write("page："+page+'\n')
    f.write("date："+date+'\n')
    f.write("title："+title+'\n')
    f.write("mp4_hd_url："+url+'\n')
    f.write('\n')
    f.close()
    
def main():
    
    ua={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    #ua={"User-Agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19"}

    #proxy = {'http':'163.204.243.129:9999'}
    #proxy = {'http':'222.189.191.46:9999'}
    #创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    #创建Opener
    opener = request.build_opener(proxy_support)
    #添加User Angent
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    #安装OPener
    request.install_opener(opener)
    
    user_id = input("请输入获取到的用户id？")
    if(user_id == ""):
        user_id = "2058586920" #微博 宇哥考研 
        print("用户id默认为"+user_id+"\n")
        
    start_page = input("请输入要获取的 起始 微博页数？")
    if(start_page ==""):
        start_page = 1
        print("起始 微博页数默认为1\n")
    else:
        start_page = int(start_page)
        
    end_page = input("请输入要获取的 终止 微博页数？")
    if(end_page ==""):
        end_page = 5
        print("终止 微博页数默认为5\n")
    else:
        end_page = int(end_page)
    
    for i in range(start_page,end_page+1):
        page=str(i)
        html=request.urlopen(url="https://m.weibo.cn/api/container/getIndex?type=uid&value="+user_id+"&containerid=107603"+user_id+"&page="+page)
        text=html.read().decode("utf-8")
        
        #html=requests.get(url="https://m.weibo.cn/api/container/getIndex?type=uid&value="+user_id+"&containerid=107603"+user_id+"&page="+page,headers=ua)
        #text=html.content.decode()
        
        print("page"+page+"长度："+str(len(text)))
        if('media_info'in text):
            print("page"+page+"有视频")
            info = json.loads(text)
            card = info["data"]["cards"]
            for each in card:
                try:#自己的微博视频
                    url=each["mblog"]["page_info"]["media_info"]["mp4_hd_url"]
                    date=each["mblog"]["created_at"]
                    title = each["mblog"]["page_info"]["media_info"]["titles"][0]["title"]#["next_title"]
                    info2txt(page,url,date,title)
                    os.system('powershell.exe "youtube-dl  -o \''+rm(date+'_'+"page"+page+'_'+title[:50])+'.mp4\' \''+url+'\' " ')
                    print("让微博休息一下...")
                    time.sleep(3)
                                        
                except KeyError as e:
                    pass
                
                try:#转载的微博视频
                    url=each["mblog"]["retweeted_status"]["page_info"]["media_info"]["mp4_hd_url"]
                    date=each["mblog"]["retweeted_status"]["created_at"]
                    title = each["mblog"]["retweeted_status"]["page_info"]["media_info"]["titles"][0]["title"]#["next_title"]
                    info2txt(page,url,date,title)
                    os.system('powershell.exe "youtube-dl  -o \''+rm(date+'_'+"page"+page+'_'+title[:50])+'.mp4\' \''+url+'\' " ')
                    print("让微博休息一下...")
                    time.sleep(3)
                
                except KeyError as e:
                    pass
                
        else:
            print("page"+page+"无视频")
        time.sleep(1)


def main2():
    
    #ua={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    ua={"User-Agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19"}

    #proxy = {'http':'163.204.243.129:9999'}
    proxy = {'http':'222.189.191.46:9999'}
    #创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    #创建Opener
    opener = request.build_opener(proxy_support)
    #添加User Angent
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    #安装OPener
    request.install_opener(opener)
    
    user_id = input("请输入获取到的用户id？")
    if(user_id == ""):
        user_id = "2058586920"
        print("用户id默认为"+user_id+"\n")
        
    start_page = input("请输入要获取的 起始 微博页数？")
    if(start_page ==""):
        start_page = 1
        print("起始 微博页数默认为1\n")
    else:
        start_page = int(start_page)
        
    end_page = input("请输入要获取的 终止 微博页数？")
    if(end_page ==""):
        end_page = 5
        print("终止 微博页数默认为5\n")
    else:
        end_page = int(end_page)
    
    for i in range(start_page,end_page+1):
        page=str(i)
        html=request.urlopen(url="https://m.weibo.cn/api/container/getIndex?type=uid&value="+user_id+"&containerid=107603"+user_id+"&page="+page)
        text=html.read().decode("utf-8")
        #html=requests.get(url="https://m.weibo.cn/api/container/getIndex?type=uid&value="+user_id+"&containerid=107603"+user_id+"&page="+page,headers=ua)
        #text=html.content.decode()
        print("page"+page+"长度："+str(len(text)))
        if('media_info'in text):
            print("page"+page+"有视频")
            info = json.loads(text)
            card = info["data"]["cards"]
            for each in card:
                try:#自己的微博视频
                    url=each["mblog"]["page_info"]["media_info"]["mp4_hd_url"]
                    date=each["mblog"]["created_at"]
                    title = each["mblog"]["page_info"]["media_info"]["titles"][0]["title"]#["next_title"]
                    info2txt(page,url,date,title)
                    os.system('PowerShell.exe -ExecutionPolicy Bypass -File a.ps1 -url \"'+
                              url+'\" -out "F:\@MyFile\我的Python\实战\微博视频\weibo_video\\'+
                              rm(date+'_'+"page"+page+'_'+title[:50])+'.mp4\" -ProxyUsage Override -ProxyList @(http://222.189.191.46:9999)')
                    
                    print("让微博休息一下...")
                    time.sleep(3)
                                        
                except KeyError as e:
                    pass
                
                try:#转载的微博视频
                    url=each["mblog"]["retweeted_status"]["page_info"]["media_info"]["mp4_hd_url"]
                    date=each["mblog"]["retweeted_status"]["created_at"]
                    title = each["mblog"]["retweeted_status"]["page_info"]["media_info"]["titles"][0]["title"]#["next_title"]
                    info2txt(page,url,date,title)
                    os.system('PowerShell.exe -ExecutionPolicy Bypass -File a.ps1 -url \"'+
                              url+'\" -out "F:\@MyFile\我的Python\实战\微博视频\weibo_video\\'+
                              rm(date+'_'+"page"+page+'_'+title[:50])+'.mp4\" -ProxyUsage Override -ProxyList @(http://222.189.191.46:9999)')
                    
                    print("让微博休息一下...")
                    time.sleep(3)
                
                except KeyError as e:
                    pass
                
        else:
            print("page"+page+"无视频")
        time.sleep(1)

if __name__ == '__main__':
     main()

