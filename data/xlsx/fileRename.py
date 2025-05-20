import os

folder_path = "~/yugioh-data/data/xlsx/"
folder_path = os.path.expanduser(folder_path)

for filename in os.listdir(folder_path):
    if '打牌记录' in filename:
        # 分离文件名和扩展名
        name_part, ext = os.path.splitext(filename)
        # 提取数字部分并转换为小写
        new_name = name_part.split('打牌记录')[0].lower()
        new_name = new_name.strip()  # 去掉多余的空格
        # 创建旧文件和新文件的完整路径
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name + ext)  # 保留扩展名
        # 重命名文件
        os.rename(old_file, new_file)

print("文件重命名完成！")
