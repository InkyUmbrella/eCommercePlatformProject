import os
import django
import subprocess

def run_init_scripts():
    """运行所有初始化脚本"""
    print("=" * 50)
    print("开始初始化所有数据...")
    print("=" * 50)
    
    # 运行 products 的初始化脚本（如果你之前创建了）
    try:
        subprocess.run(['python', 'products/init_data.py'])
    except:
        print("products 初始化脚本未找到，跳过")
    
    # 运行 marketing 的初始化脚本
    try:
        subprocess.run(['python', 'marketing/init_data.py'])
    except Exception as e:
        print(f"marketing 初始化脚本执行失败: {e}")
    
    print("=" * 50)
    print("数据初始化完成！")
    print("=" * 50)

if __name__ == '__main__':
    run_init_scripts()