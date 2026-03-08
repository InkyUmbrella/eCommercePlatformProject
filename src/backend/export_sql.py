import os
import django
from django.core.management import call_command

def export_sql():
    """导出数据库为 SQL 文件"""
    print("正在导出数据库结构...")
    
    # 导出结构
    with open('database_structure.sql', 'w', encoding='utf-8') as f:
        call_command('sqlmigrate', 'products', '0001', stdout=f)
        call_command('sqlmigrate', 'marketing', '0001', stdout=f)
    
    # 导出数据（使用 dumpdata 然后手动转换，或直接用 dumpdata 输出 JSON）
    print("正在导出数据...")
    with open('initial_data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'products', 'marketing', indent=2, stdout=f)
    
    print("导出完成！")
    print("生成的文件：")
    print("  - database_structure.sql (数据库结构)")
    print("  - initial_data.json (初始化数据)")

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendCore.settings')
    django.setup()
    export_sql()