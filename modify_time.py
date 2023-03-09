
'''
修改谷歌相册导出的照片时间
谷歌相册到处的是一堆按时间+相册排序的照片文件+JSON文件，会拆分成多个压缩包，解压合并后恢复完整的文件夹
文件的“修改时间”是开始导出的时间，“创建时间”是解压下载的文件或之后复制的时间
每一个修改前的源文件对应一个JSON文件，里面有照片的拍摄时间和导出时间
本脚本会遍历所有照片文件，读取对应的JSON文件，修改照片的“修改时间”和“访问时间”为照片的拍摄时间
'''

import os
import json
import time
import shutil
import filecmp
import re

src_path = "G:/设备备份/谷歌TakeOut/相册"
dst_path = "G:/设备备份/谷歌TakeOut/相册1"

total_count = 0

def modifyFileByJson(file_path):
    origin_path = file_path
    global total_count
    # 确定输入输出路径
    file_path = file_path.replace('-已修改', '')  # 谷歌相册编辑后的会增加后缀，这里只保留编辑后的照片
    file_name = os.path.basename(file_path)
    if len(file_name) > 46:
        file_path = file_path[:len(file_path) - (len(file_name) - 46)]

    save_path = origin_path.replace(src_path, dst_path)
    # print(file_name, file_path)
    if os.path.exists(save_path) and filecmp.cmp(origin_path, save_path, shallow=False):
        return
    
    json_path = file_path + ".json"
    if not os.path.exists(json_path):
        new_json_path = re.sub(r'^(.+) ?(\(\d+\))(\.\w+)\.json$', r'\1\3\2.json', json_path)
        if json_path != new_json_path:
            json_path = new_json_path
    
    if not os.path.exists(json_path):
        print(total_count, "json file not found:", json_path, origin_path)
        return
    total_count = total_count + 1
    print(total_count, origin_path, ' -> ', save_path)
    
    # 解析JSON
    timestamp = 0
    with open(json_path, 'r', encoding='utf8') as f:
        json_data = json.load(f)
        create_timestamp = int(json_data['creationTime']['timestamp'])
        taken_timestamp = int(json_data['photoTakenTime']['timestamp'])
        timestamp = min(create_timestamp, taken_timestamp)
        # 输出时间字符串
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        # print(total_count, file_path, time_str)
    
    # 复制文件到新的路径
    shutil.copy(origin_path, save_path)
    
    # 修改文件的最后修改时间和访问时间
    os.utime(save_path, (timestamp, timestamp))


def findPhotos(base_dir):
    # 对应的输出文件夹
    save_dir = base_dir.replace(src_path, dst_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 遍历所有文件夹
    file_list = os.listdir(base_dir)
    for file in file_list:
        cur_path = os.path.join(base_dir, file)
        if os.path.isdir(cur_path):
            # 遍历子文件夹
            findPhotos(cur_path)
        else:
            # 修改所有非JSON文件
            if file.endswith(".json"):
                continue
            else:
                modifyFileByJson(cur_path)
                # if total_count > 100:  # 上限
                    # return


if __name__ == "__main__":
    findPhotos(src_path)