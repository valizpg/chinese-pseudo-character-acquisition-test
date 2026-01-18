import os

def check_files():
    """
    Checks for the existence of all required files and directories for the experiment.
    Handles both padded (e.g., 01) and unpadded (e.g., 1) file numbers.
    """
    print("开始检查所需文件...")
    missing_files = []

    static_paths = [
        ('stimuli/definitions.xlsx', "包含所有'字'的英文定义的Excel文件"),
        ('stimuli/speaker_icon.png', "学习阶段用于重播发音的喇叭图标"),
        ('data', "目录: data"),
        ('stimuli/images', "目录: stimuli/images"),
        ('stimuli/meanings', "目录: stimuli/meanings"),
        ('stimuli/pronunciations', "目录: stimuli/pronunciations"),
        ('stimuli/radical_awareness', "目录: stimuli/radical_awareness")
    ]
    for path, desc in static_paths:
        if not os.path.exists(path):
            missing_files.append(f"- 【缺失】 {path} ({desc})")

    conditions = ['FS_R', 'FS_NR', 'MS_R', 'MS_NR']
    stim_types = {
        'images': ('.png', '图片'),
        'meanings': ('.png', '含义图'),
        'pronunciations': ('.wav', '发音')
    }

    for cond in conditions:
        for i in range(1, 13):
            for stim_folder, (ext, desc_suffix) in stim_types.items():
                path_unpadded = f'stimuli/{stim_folder}/{cond}_{i}{ext}'
                path_padded = f'stimuli/{stim_folder}/{cond}_{i:02d}{ext}'
                
                if not (os.path.exists(path_unpadded) or os.path.exists(path_padded)):
                    missing_files.append(f"- 【缺失】 {path_padded} ({cond} {desc_suffix} {i})")

    radical_types = ['form_reg_A', 'form_reg_B', 'pos_reg_A', 'pos_reg_B']
    for r_type in radical_types:
        for i in range(1, 6):
            path = f'stimuli/radical_awareness/{r_type}_{i}.png'
            if not os.path.exists(path):
                missing_files.append(f"- 【缺失】 {path} (部件意识任务图片 {r_type}_{i})")

    if not missing_files:
        print("🎉 全部检查通过！所有必需的文件和目录都已就绪。")
    else:
        print("⚠️ 发现文件缺失！请根据以下列表创建或移动文件到正确位置：")
        for entry in sorted(missing_files):
            print(entry)
            
    if not os.path.exists('stimuli/definitions.xlsx'):
         print("提示: 'stimuli/definitions.xlsx' 文件缺失。你需要创建一个Excel文件，")
         print("其中包含四个列标题: FS_R, FS_NR, MS_R, MS_NR。")
         print("每个列下面应该有12行，分别对应12个'字'的英文定义。")


if __name__ == '__main__':
    check_files()
