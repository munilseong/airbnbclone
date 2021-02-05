from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
import random
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "this command create users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="how many create rooms"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        houserule = room_models.HouseRule.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_user),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 20),
            },
        )
        created_photo = seeder.execute()
        created_clean = flatten(list(created_photo.values()))
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"room_photos/{random.randint(1,31)}.webp",
                    room=room,
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for h in houserule:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(h)
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))