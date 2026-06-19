import pandas as pd
import os

# 获取当前脚本（本文件）所在的绝对路径 )
current_dir = os.path.dirname(os.path.abspath(__file__))

# 找到与当前文件夹平级的 data 文件夹路径 (即 .../data/)
data_dir = os.path.join(current_dir, "..", "data")


# 之前写死的是 "1.xlsx"，现在拼接到动态的 data 文件夹下
excel_file = os.path.join(data_dir, "1.xlsx") 


# 如果想把导出的 CSV 依然存放在 data 文件夹里的某个子目录下（例如 data/extracted_csvs）
output_dir = os.path.join(data_dir, "extracted_csvs")

# 如果想直接把 CSV 平铺倒在 data 文件夹根目录，就把上一行改成：
# output_dir = data_dir

# 创建输出文件夹
os.makedirs(output_dir, exist_ok=True)


print(f"正在读取文件: {excel_file}")
# 加载所有的 Sheet
excel_sheets = pd.read_excel(excel_file, sheet_name=None)

# 循环转换
for sheet_name, df in excel_sheets.items():
    # 保持原命名规则
    csv_file_name = f"{sheet_name}.csv"
    csv_path = os.path.join(output_dir, csv_file_name)
    
    # 导出为 utf-8-sig 编码（防止中文乱码）
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"已成功将 Sheet [{sheet_name}] 转换为: {csv_path}")