import pandas as pd

# 读取Excel文件
df = pd.read_excel('登录测试用例.xlsx')

# 显示前几行
print("Excel文件的前5行:")
print(df.head())

# 显示所有列名
print("\n列名:")
print(df.columns.tolist())

# 检查是否有重复的ID（文件内重复检查）
# 注意：系统支持在不同项目中使用相同的用例ID，但在同一项目内用例ID必须唯一
if 'ID' in df.columns:
    print("\nID列的值:")
    print(df['ID'].tolist())
    print("\n重复的ID:")
    duplicated_ids = df[df.duplicated('ID', keep=False)]['ID']
    print(duplicated_ids.tolist() if not duplicated_ids.empty else "没有重复的ID")
else:
    print("未找到ID列")