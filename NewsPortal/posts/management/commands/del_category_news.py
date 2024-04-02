from django.core.management.base import BaseCommand
from posts.models import Post


class Command(BaseCommand):
	help = 'Команда удаляет все новости из указанной категории'

	def add_arguments(self, parser):
		parser.add_argument('category', type=str)

	def handle(self, *args, **options):
		self.stdout.readable()
		self.stdout.write('Вы действительно хотите удалить все новости? (yes/no)')
		answer = input()

		if answer == 'yes':
			Post.objects.filter(categories__category_name=options['category'], post_type=Post.news).delete()
			self.stdout.write(self.style.SUCCESS(f'Все новости в категории {options["category"]} удалены'))
			return

		self.stdout.write(self.style.ERROR('Отменено'))
