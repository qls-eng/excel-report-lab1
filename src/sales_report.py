import pandas as pd
import os
import sys

def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    清洗销售数据 DataFrame。
    """
    if df.empty:
        return df.copy()

    df_clean = df.copy()

    # 将“数量”和“单价”强制转换为数值类型，无法转换的脏数据会变为 NaN
    df_clean['数量'] = pd.to_numeric(df_clean['数量'], errors='coerce')
    df_clean['单价'] = pd.to_numeric(df_clean['单价'], errors='coerce')

    required_cols = ['日期', '销售员', '产品', '数量', '单价', '地区']

    # 删除关键字段中存在缺失值的行
    df_clean = df_clean.dropna(subset=required_cols)
    # 剔除数量 <= 0 的无效行
    df_clean = df_clean[df_clean['数量'] > 0]
    # 按全字段进行去重
    df_clean = df_clean.drop_duplicates()
    # 重置索引
    df_clean = df_clean.reset_index(drop=True)

    return df_clean


def build_stats(df: pd.DataFrame):
    """
    基于清洗后的销售数据，统计按销售员、按地区的销售额汇总以及月度总额。
    """
    # 处理空 DataFrame 的边界情况，返回具有正确列名的空 DataFrame
    if df.empty:
        empty_by_sales = pd.DataFrame(columns=['销售员', '销售额'])
        empty_by_region = pd.DataFrame(columns=['地区', '销售额'])
        empty_total = pd.DataFrame(columns=['月度总额'])
        return empty_by_sales, empty_by_region, empty_total

    df_stats = df.copy()
    
    # 新建"销售额"列
    df_stats['销售额'] = df_stats['数量'] * df_stats['单价']
    
    # 按销售员汇总销售额，并按销售额降序排列
    by_sales = df_stats.groupby('销售员', as_index=False)['销售额'].sum()
    by_sales = by_sales.sort_values(by='销售额', ascending=False).reset_index(drop=True)
    
    # 按地区汇总销售额，并按销售额降序排列
    by_region = df_stats.groupby('地区', as_index=False)['销售额'].sum()
    by_region = by_region.sort_values(by='销售额', ascending=False).reset_index(drop=True)
    
    # 计算月度总额
    total = pd.DataFrame({'月度总额': [df_stats['销售额'].sum()]})
    
    return by_sales, by_region, total


def main():
    """
    主流程函数：读取、清洗、统计并导出 Excel 报表。
    """
    input_path = 'data/sales_raw.xlsx'
    output_path = 'output/report.xlsx'
    required_cols = ['日期', '销售员', '产品', '数量', '单价', '地区']
    
    # 1. 检查文件是否存在
    if not os.path.exists(input_path):
        print(f"错误：找不到输入文件 '{input_path}'，请检查文件路径是否正确。")
        sys.exit(1)
        
    # 2 & 3. 尝试读取文件，捕获读取失败（如文件损坏、格式错误等）
    try:
        df = pd.read_excel(input_path, engine='openpyxl')
    except Exception as e:
        print(f"错误：读取文件 '{input_path}' 失败，请检查文件是否损坏。\n详细信息：{e}")
        sys.exit(1)
        
    # 4. 检查文件是否为空（无数据行）
    if df.empty:
        print("错误：读取到的 Excel 文件为空，没有数据可供处理。")
        sys.exit(1)
        
    # 5. 检查是否缺少关键字段
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"错误：输入文件缺少以下关键字段：{', '.join(missing_cols)}。")
        sys.exit(1)
        
    # 6. 调用 clean_sales 清洗数据
    df_clean = clean_sales(df)
    if df_clean.empty:
        print("提示：经过数据清洗后，没有留下任何有效的销售数据，无法生成报表。")
        sys.exit(0)
        
    # 7. 调用 build_stats 统计数据
    by_sales, by_region, total = build_stats(df_clean)
    
    # 8. 输出到 output/report.xlsx
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_clean.to_excel(writer, sheet_name='明细清洗后', index=False)
            by_sales.to_excel(writer, sheet_name='按销售员', index=False)
            by_region.to_excel(writer, sheet_name='按地区', index=False)
            total.to_excel(writer, sheet_name='总览', index=False)
    except Exception as e:
        print(f"错误：写入输出文件 '{output_path}' 失败，请检查目录权限。\n详细信息：{e}")
        sys.exit(1)
        
    # 9. 输出成功提示，包含清洗后行数和月度总额
    total_amount = total['月度总额'].iloc[0]
    print("✅ 报表生成成功！")
    print(f" - 清洗后有效数据行数：{len(df_clean)}")
    print(f" - 月度总销售额：{total_amount}")
    print(f" - 输出文件路径：{os.path.abspath(output_path)}")


# 10. 脚本入口
if __name__ == "__main__":
    main()