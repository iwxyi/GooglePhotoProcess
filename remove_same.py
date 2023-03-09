'''
下载的图片其他地方可能已经有备份了（比如NAS、WebDAV）
这里遍历所有图片，如果有重复的，就删除
之后再手动备份上去
'''

import os
import filecmp

library_path = "P:/wxy"  # 被检测的文件夹
reduct_path = "G:/设备备份/谷歌TakeOut/相册1"  # 去重的文件夹

total_count = 0

all_files = []  # 仅保存文件名，用于快速匹配
all_paths = []  # 完整路径，用于确认重复文件

'''
在备份的照片库中获取所有已有的照片
可以是WebDAV等网络文件夹，速度应该不会太慢
'''
def loopAllFiles(base_dir):
    # 遍历所有文件夹
    file_list = os.listdir(base_dir)
    for file in file_list:
        cur_path = os.path.join(base_dir, file)
        if os.path.isdir(cur_path):
            # 遍历子文件夹
            loopAllFiles(cur_path)
        else:
            if file.endswith(".json"):
                continue
            else:
                all_files.append(file)
                all_paths.append(cur_path)


'''
将照片一一比对，如果有重复的，就删除
'''
def detectSameFile(path):
    file_name = os.path.basename(path)
    if file_name in all_files:
        # 重复的文件
        index = all_files.index(file_name)
        full_path = all_paths[index]
        # if filecmp.cmp(path, full_path, shallow=True):
        print(total_count, "重复的文件：", path, " -> ", all_paths[index])
        os.remove(path)

'''
遍历目标文件夹，获取所有目标文件
'''
def loopTargetFiles(base_dir):
    global total_count
    # 遍历所有文件夹
    file_list = os.listdir(base_dir)
    for file in file_list:
        cur_path = os.path.join(base_dir, file)
        if os.path.isdir(cur_path):
            # 遍历子文件夹
            loopTargetFiles(cur_path)
        else:
            if file.endswith(".json"):
                continue
            else:
                detectSameFile(cur_path)
                # print(total_count, cur_path)
                total_count = total_count + 1


if __name__ == "__main__":
    loopAllFiles(library_path)
    print('待匹配文件数量：', len(all_files))
    loopTargetFiles(reduct_path)

