import sys
import os
import pandas as pd
import pytest

# 将项目根目录加入 sys.path，确保能正确导入 src 下的模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sales_report import clean_sales, build_stats


# ================= 辅助函数 =================

def get_base_df():
    """构造一份基础的有效销售数据 DataFrame"""
    data = {
        '日期': ['2023-01-01', '2023-01-02'],
        '销售员': ['张三', '李四'],
        '产品': ['A', 'B'],
        '数量': [2, 4],
        '单价': [10, 40],
        '地区': ['华东', '华北']
    }
    return pd.DataFrame(data)


# ================= 测试用例 =================

def test_normal_flow():
    """
    正常用例：测试正常数据的清洗和统计结果。
    断言清洗后行数、各销售员销售额、月度总额是否正确。
    """
    df = get_base_df()
    
    # 1. 清洗数据
    df_clean = clean_sales(df)
    assert len(df_clean) == 2, "清洗后应保留 2 行有效数据"
    
    # 2. 统计数据
    by_sales, by_region, total = build_stats(df_clean)
    
    # 3. 断言月度总额 (2*10 + 4*40 = 180)
    assert total['月度总额'].iloc[0] == 180, "月度总额计算错误"
    
    # 4. 断言按销售员汇总的销售额
    zhang_san_sales = by_sales[by_sales['销售员'] == '张三']['销售额'].iloc[0]
    li_si_sales = by_sales[by_sales['销售员'] == '李四']['销售额'].iloc[0]
    assert zhang_san_sales == 20, "张三的销售额计算错误"
    assert li_si_sales == 160, "李四的销售额计算错误"


def test_clean_invalid_quantity():
    """
    边界用例1：测试剔除数量 <= 0 的行。
    混入数量为 0 和负数的脏数据，断言清洗后被正确剔除。
    """
    df = get_base_df()
    # 构造数量为 0 和负数的脏数据
    invalid_rows = pd.DataFrame({
        '日期': ['2023-01-03', '2023-01-04'],
        '销售员': ['王五', '赵六'],
        '产品': ['C', 'D'],
        '数量': [0, -5],
        '单价': [10, 20],
        '地区': ['华南', '华西']
    })
    df = pd.concat([df, invalid_rows], ignore_index=True)
    
    df_clean = clean_sales(df)
    
    # 断言：脏数据被剔除，只剩下原本的 2 行
    assert len(df_clean) == 2, "数量 <= 0 的行未被正确剔除"
    assert (df_clean['数量'] > 0).all(), "清洗后的数据中仍存在数量 <= 0 的行"


def test_clean_missing_fields():
    """
    边界用例2：测试删除关键字段缺失的行。
    混入缺失“销售员”字段的行，断言清洗后被正确删除。
    """
    df = get_base_df()
    # 构造关键字段缺失的脏数据
    missing_row = pd.DataFrame({
        '日期': ['2023-01-05'],
        '销售员': [None],  # 关键字段缺失
        '产品': ['E'],
        '数量': [1],
        '单价': [10],
        '地区': ['华东']
    })
    df = pd.concat([df, missing_row], ignore_index=True)
    
    df_clean = clean_sales(df)
    
    # 断言：缺失行被剔除，且剩余数据的关键字段无空值
    assert len(df_clean) == 2, "关键字段缺失的行未被正确删除"
    assert df_clean['销售员'].notna().all(), "清洗后的数据中仍存在关键字段缺失"


def test_clean_duplicates():
    """
    边界用例3：测试按全字段去重。
    混入完全重复的行，断言清洗后重复行被剔除。
    """
    df = get_base_df()
    # 追加一行与第一行完全相同的数据
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    
    df_clean = clean_sales(df)
    
    # 断言：重复行被剔除，行数保持为 2
    assert len(df_clean) == 2, "全字段重复的行未被正确去重"


def test_empty_dataframe():
    """
    异常用例：测试传入空 DataFrame 时不报错，且返回结构正确。
    分别验证 clean_sales 和 build_stats 对空数据的兼容性。
    """
    # 构造一个具有正确列名但无数据的空 DataFrame
    empty_df = pd.DataFrame(columns=['日期', '销售员', '产品', '数量', '单价', '地区'])
    
    # 1. 验证 clean_sales 不报错且返回空 DataFrame
    df_clean = clean_sales(empty_df)
    assert df_clean.empty, "空 DataFrame 经过 clean_sales 后应为空"
    
    # 2. 验证 build_stats 不报错，且返回的三个 DataFrame 列名正确
    by_sales, by_region, total = build_stats(empty_df)
    
    assert by_sales.empty, "空数据按销售员汇总应为空"
    assert list(by_sales.columns) == ['销售员', '销售额'], "by_sales 列名不正确"
    
    assert by_region.empty, "空数据按地区汇总应为空"
    assert list(by_region.columns) == ['地区', '销售额'], "by_region 列名不正确"
    
    assert total.empty, "空数据的月度总额应为空"
    assert list(total.columns) == ['月度总额'], "total 列名不正确"