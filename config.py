URL = 'https://translate.google.cn/' #翻译网站

FILE_NAME = r"D:\视频\字幕\Game.of.Thrones.S08E05.WEB.H264-MEMENTO[eztv]_track3_eng.srt"  #要翻译的文件位置

NEW_NAME = FILE_NAME +".txt" #用于缓存

# ass格式文件匹配正则
P_1 = 'Dialogue.*?,,(.*)'
P_2 = 'Dialogue.*?{.*?}(.*)'

#等待响应时间
SLEEP_TIME = 0.8
