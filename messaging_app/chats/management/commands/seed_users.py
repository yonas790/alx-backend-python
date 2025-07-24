from django.core.management.base import BaseCommand
from chats.models import User  # Adjust if you're using a custom user model
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed 10 random users using Faker'

    def handle(self, *args, **kwargs):
        fake = Faker()
        roles = ['admin', 'guest', 'moderator', 'member']

        created_count = 0
        for _ in range(10):
            email = fake.unique.email()
            username = fake.unique.user_name()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = '1234'  # Same default password for simplicity
            role = random.choice(roles)

            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    role=role
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created user: {username} ({email})'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done. {created_count} users created.'))
