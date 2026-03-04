from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Category
from django.db.models import Count

class Command(BaseCommand):
 help = '查找并可选合并同名重复分类（谨慎使用）\n用法: python manage.py fix_category_duplicates --list\n python manage.py fix_category_duplicates --merge-auto'

 def add_arguments(self, parser):
 parser.add_argument('--list', action='store_true', help='仅列出同名重复分类')
 parser.add_argument('--merge-auto', action='store_true', help='按名称自动合并同名分类（保留最早创建或最小 id）')

 def handle(self, *args, **options):
 # 查找具有相同 name 的分类组
 groups = Category.objects.values('name').annotate(c=Count('id')).filter(c__gt=1)
 if not groups:
 self.stdout.write(self.style.SUCCESS('未发现同名重复分类。'))
 return

 if options['list']:
 self.stdout.write('发现以下同名分类组：')
 for g in groups:
 name = g['name']
 self.stdout.write(f"\n名称: {name}")
 for c in Category.objects.filter(name=name).order_by('id'):
 parent = c.parent.name if c.parent else '（无父级）'
 self.stdout.write(f" id={c.id} parent={parent} created_at={c.created_at}")
 return

 if options['merge_auto']:
 self.stdout.write('开始按名称自动合并同名分类（请事先备份数据库）...')
 for g in groups:
 name = g['name']
 cats = list(Category.objects.filter(name=name).order_by('id'))
 # 保留第一个（最小 id）为主分类
 primary = cats[0]
 others = cats[1:]
 self.stdout.write(f"\n合并名称 '{name}'，保留 id={primary.id}，将合并 {len(others)} 个记录")
 with transaction.atomic():
 for other in others:
 #1) 将 other 的子分类指向 primary
 children = list(other.children.all())
 for ch in children:
 ch.parent = primary
 ch.save()
 #2) 将关联的商品指向 primary
 products = other.products.all()
 for p in products:
 p.category = primary
 p.save()
 #3) 删除 other
 other.delete()
 self.stdout.write(self.style.SUCCESS(f"已合并到 id={primary.id}"))
 self.stdout.write(self.style.SUCCESS('\n自动合并完成。请在 admin 中检查结果并运行测试。'))
 return

 # 默认行为：提示并列出
 self.stdout.write('发现同名重复分类，使用 --list 查看详情或 --merge-auto进行自动合并（会修改数据，请先备份数据库）。')
