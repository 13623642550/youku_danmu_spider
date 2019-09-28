'''
爬取优酷电视剧《长安十二时辰》的弹幕，并做词云分析
'''

import requests
import json
import time
import random
import jieba
import os
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# 文件保存路径
YOUKU_DANMU_RESULT = 'youku_danmu.txt'
# 字体路径-宋体
FONT_PATH_SONGTI = 'C:\Windows\Fonts\simsun.ttc'
# 面板底图路径
MASK_IMAGE = 'man.jpg'
# 最终结果图片的路径
RESULT_IMG_PATH = 'danmu_cloud.jpg'


def get_danmu(mat, vid):
    '''
    解析弹幕的请求，将弹幕信息存入文件
    :param mat:
    :return:
    '''
    url = 'https://service.danmu.youku.com/list?jsoncallback=jQuery111209758089504287095_1569249955626&mat=%d&mcount=1&ct=1001&iid=%s&aid=322943&cid=97&lid=0&ouid=0&_=1569249955637' % (
    mat, vid)
    print(url)
    kv = {
        'Referer': 'https://v.youku.com/v_show/id_XNDI0NDYyNjk1Mg==.html?spm=a2h1n.8261147.0.0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=kv)
        response.raise_for_status()
        resp_json = jsonp_func_to_json_obj(response.text)
        result_list = resp_json['result']
        if result_list:
            for result in result_list:
                with open(YOUKU_DANMU_RESULT, 'a+', encoding='utf-8') as file:
                    file.write(result['content'] + '\n')
                    print(result['content'])
                    time.sleep(random.random() * 2)
            return True
        else:
            print('爬取完毕')
            return False
    except Exception as e:
        raise e


def get_vid_list():
    '''
    通过接口获取请求url地址中的iid的值列表，此接口中返回的vid即为iid参数
    :return:
    '''
    url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.16&appKey=24679788&t=1569682679813&sign=e3dafa30ddb43e5bf423784f69f4de75&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&AntiFlood=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22utid%5C%22%3A%5C%22NMcPFkBMnW0CAd9oAzQTYRz%2B%5C%22%2C%5C%22client_ts%5C%22%3A1569682679%2C%5C%22version%5C%22%3A%5C%221.9.6%5C%22%2C%5C%22ckey%5C%22%3A%5C%22120%23bX1bSBr%2BsLvVCOD%2B4c4ggzU%2Fqa6bkYPhjBO3t8y%2BzKeYnkUoINsbPiTvxrEXKNZVHeN1HCee65n3qrRTvj3xhq1RwgXOnuw%2B%2F%2F44kxY2p1XGoIJ11YGdUOEvpe9u%2FjEI39AzUYS8eBTCbjcyknLFlAPs0l7Saz%2BbNFYvSi5%2FybbS7UGPWWl%2FoYk6y%2FA54Ihx5bxYg6ikmtf6RNdPTbjg8%2FI9iVXZZeQzsjfnaGINgQXEb05Au0xmwp37e1M3FtWIYk73hFq1SrGvHiykmmGKywMuleVRwx2Uu4BC37DWns9NUpy6XXpCLumBorruJ7Y7OLSz9P6nL90OdjDwApETF7teYkCGuV90gghg9VCFDXZtC3vdBNhKxevJUO4DVGWhum1rbMjapVDETYZQ8%2BrqJIs1yfPFICiOsfRlIW5qyrzd3Q8KZ7RVEvQopSA08FxXaCRxWXUDbyCP%2FVE0KSmZSe%2F1nqmaGE9eviO2d%2FdnSEgArTp42d2Vh9rntgtY4xVIsahX95MZGZ2fRV26Fmi%2Bt5GRdMsgCJ0p%2F8DNrNZCYgjf%2FkdYATRW39i0E3EB5w2wjAUscRx2I%2BnE4lBx%2F4VKb9AZp6y9In0mpROeTGpjMjNE%2B97ksH9bOvvjJ80bbT2MvF56jnlzYjhYzjScBDjXLIbuB7AfOB5uKYm%2BZIVCUQ%2F%2F9nRMuYb3%2F4rEff%2FNlw40TehY%2F96uSDq31leMygRZnwNZrM1rK1nYcPGzIa1o%2BM%2FHC09ya10qKI8g4bEh6SUahnpLReofS0pMKoYVXk%2BnbvWgov%3D%3D%5C%22%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XNDI0NDYyNjk1Mg%3D%3D%5C%22%2C%5C%22play_ability%5C%22%3A5376%2C%5C%22current_showid%5C%22%3A%5C%22322943%5C%22%2C%5C%22preferClarity%5C%22%3A3%2C%5C%22master_m3u8%5C%22%3A1%2C%5C%22media_type%5C%22%3A%5C%22standard%2Csubtitle%5C%22%2C%5C%22app_ver%5C%22%3A%5C%221.9.6%5C%22%7D%22%2C%22ad_params%22%3A%22%7B%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22pver%5C%22%3A%5C%221.9.6%5C%22%2C%5C%22sver%5C%22%3A%5C%222.0%5C%22%2C%5C%22site%5C%22%3A1%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22fu%5C%22%3A0%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22os%5C%22%3A%5C%22win%5C%22%2C%5C%22osv%5C%22%3A%5C%2210%5C%22%2C%5C%22dq%5C%22%3A%5C%22auto%5C%22%2C%5C%22atm%5C%22%3A%5C%22%5C%22%2C%5C%22partnerid%5C%22%3A%5C%22null%5C%22%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22isvert%5C%22%3A0%2C%5C%22vip%5C%22%3A0%2C%5C%22emb%5C%22%3A%5C%22AjEwNjExNTY3MzgCc28ueW91a3UuY29tAi9zZWFyY2hfdmlkZW8vcV8lRTklOTUlQkYlRTUlQUUlODklRTUlOEQlODElRTQlQkElOEMlRTYlOTclQjYlRTglQkUlQjA%3D%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22needbf%5C%22%3A2%7D%22%7D'
    # 在浏览器-调试工具-console中输入：document.cookie获取cookie信息
    # cookie信息定时会更换，请注意修改为当前的cookie
    kv = {
        'Referer': 'https://v.youku.com/v_show/id_XNDI0NDYyNjk1Mg==.html?spm=a2h0k.11417342.soresults.dtitle&s=efbfbd78efbfbd5cefbf',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'cookie': 'P_F=1; P_T=1569689475; cna=NMcPFkBMnW0CAd9oAzQTYRz+; __ysuid=1569253951978Zzs; juid=01dlfd6i272hiq; UM_distinctid=16d5ed351ce573-05aa213414753-e343166-144000-16d5ed351cfaf2; _m_h5_tk=40a76fc46f53f68f5a274b95d71c4ddf_1569687015867; _m_h5_tk_enc=aeafe2d69a29dee67f719af40cb966a6; __ayft=1569682194620; __aysid=1569682194620RGL; __ayscnt=1; __arpvid=1569682207700Kic5kl-1569682207711; __aypstp=3; __ayspstp=3; CNZZDATA1277955961=1227091303-1569248872-https%253A%252F%252Fv.youku.com%252F%7C1569681760; seid=01dls5jen41kbt; referhost=https%3A%2F%2Fso.youku.com; seidtimeout=1569684009509; ypvid=15696822120515UM0Qs; yseid=1569682212052JvJy3I; ysestep=1; yseidcount=2; yseidtimeout=1569689412054; ycid=0; ystep=5; __ayvstp=6; __aysvstp=6; isg=BLCw6GGcmTwVOkU_g834_GDzgX4C-ZRDYCkT2qoAroveZVIPUglk0ikXvS2gdUwb'
    }
    try:
        response = requests.get(url, headers=kv)
        response.raise_for_status()
        print(response.text)
        resp_json = jsonp_func_to_json_obj(response.text)
        video_list = resp_json['data']['data']['videos']['list']
        print(video_list)
        return (video['vid'] for video in video_list)
    except Exception as e:
        raise e


def jsonp_func_to_json_obj(jsonp_func):
    '''
    将获取的结果截取字符后转换为json对象返回
    :param josnp_func:
    :return:
    '''
    start_index = jsonp_func.index('(') + 1
    end_index = jsonp_func.rindex(')')
    jsonp_func = jsonp_func[start_index:end_index]
    return json.loads(jsonp_func)


def batch_spider():
    '''
    批量爬取弹幕信息
    :return:
    '''
    if os.path.exists(YOUKU_DANMU_RESULT):
        os.remove(YOUKU_DANMU_RESULT)
    # 爬取弹幕
    vids = get_vid_list()
    for vid in vids:
        print(vid)
        i = 0
        while get_danmu(i, vid):
            i += 1
            print('正在爬取，i=' + str(i))


def cut_danmu():
    '''
    分词
    :return:
    '''
    with open(YOUKU_DANMU_RESULT, 'r', encoding='utf-8') as file:
        result_txt = file.read()
        words_list = jieba.cut(result_txt, cut_all=True)
        wl = ' '.join(words_list)
        return wl


def create_words_cloud():
    '''
    制作词云
    :return:
    '''
    wc_mask = np.array(Image.open(MASK_IMAGE))
    # 这里指定需要过滤掉的词组
    stop_words = ['哈哈', '哈哈哈', '什么', '为什么', '知道', '怎么']
    wc = WordCloud(background_color='white', max_words=200, mask=wc_mask, scale=4, max_font_size=40,
                   stopwords=stop_words, random_state=30, font_path=FONT_PATH_SONGTI)
    wc.generate(cut_danmu())
    wc.to_file(RESULT_IMG_PATH)


if __name__ == '__main__':
    # 批量爬取弹幕信息
    # batch_spider()

    # 制作词云
    create_words_cloud()
