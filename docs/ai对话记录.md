## 考题一 第1轮：清洗函数

**我的提问：**
请用 Python 写一个函数 clean_sales(df)，输入 pandas DataFrame，字段：日期、销售员、产品、数量、单价、地区。
要求：删除关键字段缺失的行；剔除数量 <= 0 的行；按全字段去重；返回清洗后的 DataFrame。
约束：不要读写文件；不要修改传入的 df；数量列用 pd.to_numeric(errors="coerce")；加中文注释；空 DataFrame 直接返回。

**AI 输出摘要：**
AI 给出 clean_sales 函数，含 df.copy()、数量转数值、dropna、数量>0 筛选、drop_duplicates、reset_index。

**人工修改：**
- AI 只把"数量"转了数值，没转"单价"，我补了 `df_clean['单价'] = pd.to_numeric(df_clean['单价'], errors='coerce')`。

**运行结果：**
输入 6 行，清洗后剩 3 行。负数量、数量 0、重复行均被正确剔除。

## 考题一 第2轮：统计函数 build_stats

**我的提问：**
请基于 clean_sales 函数，写 build_stats(df)，返回按销售员、按地区、总览三个 DataFrame，空 DataFrame 返回空结果，不报错。

**AI 输出摘要：**
AI 给出 build_stats，含 df.copy()、销售额列计算、groupby 汇总、sort_values 降序、空 DataFrame 处理。

**人工修改：**
无，AI 输出直接可用。

**运行结果：**
按销售员：李四 160，张三 20
按地区：华北 160，华东 20
月度总额：180
（与人工核对一致）

**踩坑记录：**
首次贴代码时 VS Code 用了 GBK 编码，中文乱码导致 import 失败。改为 UTF-8 后正常。

## 考题一 第3轮：主流程 + 异常处理

**我的提问：**
请基于 clean_sales 和 build_stats，写 main() 主流程，读取 data/sales_raw.xlsx，输出 output/report.xlsx 四个工作表，异常情况给中文提示不崩溃。

**AI 输出摘要：**
AI 给出 main()，含文件存在检查、读取异常捕获、空文件检查、缺字段检查、清洗后空数据检查、ExcelWriter 输出四个工作表、成功提示。

**人工修改：**
无，AI 输出直接可用。

**运行结果：**
✅ 报表生成成功，清洗后 3 行，月度总额 180。
output/report.xlsx 四个工作表齐全，数值与人工核对一致。

## 考题一 第4轮：pytest 测试用例

**我的提问：**
请为 clean_sales 和 build_stats 写 pytest 测试，含正常用例、边界用例（数量、缺字段、重复行）、异常用例（空 DataFrame）。

**AI 输出摘要：**
AI 给出 5 个测试用例：
- test_normal_flow：正常数据清洗+统计
- test_clean_invalid_quantity：数量 <= 0 剔除
- test_clean_missing_fields：关键字段缺失删除
- test_clean_duplicates：重复行去重
- test_empty_dataframe：空 DataFrame 不报错

**人工修改：**
无，AI 输出直接可用。

**运行结果：**
5 passed in 0.24s。
截图保存在 docs/images/test_excel_result.pngs