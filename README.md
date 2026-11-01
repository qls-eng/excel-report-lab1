# Lab1：Excel 销售报表生成脚本（Python Vibe Coding 实验一）

使用 pandas 读取原始销售数据，完成脏数据清洗与多维度汇总，输出包含四个工作表的 Excel 报表。原始文件只读，所有异常情况给出中文提示，程序不崩溃。

## 功能

1. **数据清洗**
   - 删除关键字段（日期、销售员、产品、数量、单价、地区）缺失的行
   - 剔除数量 ≤ 0 的异常行
   - 全字段去重
2. **统计汇总**
   - 按销售员汇总销售额（数量 × 单价）
   - 按地区汇总销售额
   - 月度销售总额
3. **输出报表** `output/report.xlsx`，包含四个工作表：
   - `明细清洗后`：清洗后的完整明细
   - `按销售员`：销售员销售额汇总
   - `按地区`：地区销售额汇总
   - `总览`：月度销售总额

## 目录结构

```
excel-report-lab1/
├── data/
│   └── sales_raw.xlsx          # 原始样例数据（只读，不做修改）
├── output/
│   └── report.xlsx             # 生成的报表
├── src/
│   ├── __init__.py
│   └── sales_report.py         # 清洗、统计、主流程
├── tests/
│   ├── __init__.py
│   └── test_excel.py           # pytest 测试用例
└── docs/
    ├── 需求澄清_考题一.md
    ├── ai对话记录.md
    ├── 复盘.md
    └── images/
        └── test_excel_result.png   # 测试通过截图
```

## 环境要求

- Python 3.10+
- 依赖见 `requirements.txt`：pandas、openpyxl、pytest

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 生成报表
python src/sales_report.py
```

运行成功后在 `output/report.xlsx` 查看报表。

## 运行测试

```bash
pytest
```

共 5 个用例：正常流程、数量 ≤ 0 剔除、关键字段缺失删除、重复行去重、空 DataFrame 异常处理。

## 边界与异常处理

- 原始文件不存在 → 中文提示并退出
- 文件为空 → 中文提示并退出
- 缺少关键字段 → 列出缺失字段并退出
- 清洗后无有效数据 → 友好提示，不生成空报表
- 原始文件只读，所有输出写入 `output/`，不回写 `data/`

## 设计说明与过程文档

- [需求澄清](docs/需求澄清_考题一.md)
- [AI 协作对话记录](docs/ai对话记录.md)
- [复盘](docs/复盘.md)
