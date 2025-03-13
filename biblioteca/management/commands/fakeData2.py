from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from biblioteca.models import Usuari, Llibre, Exemplar, Llengua

# Diccionario de idiomas para Faker
faker_idiomas = {
    "Catalán": "es_CA",   # Prueba con "es_CA" en vez de "ca_ES"
    "Castellano": "es_MX",
    "Inglés": "en_US",
    "Italiano": "it_IT",
}
class Command(BaseCommand):
    help = "Genera datos falsos para usuarios, libros, ejemplares y lenguas"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Generando datos falsos..."))

        # Crear Lenguas
        llengues_data = ["Catalán", "Castellano", "Inglés", "Italiano"]
        llengues = {nom: Llengua.objects.create(nom=nom) for nom in llengues_data}

        # Crear Usuarios
        usuarios = []
        faker = Faker("es_ES")  # Faker general en español
        for _ in range(50):
            user = Usuari.objects.create_user(
                username=faker.unique.user_name(),
                email=faker.unique.email(),
                password="password123",
                first_name=faker.first_name(),
                last_name=faker.last_name()
            )
            usuarios.append(user)

        # Crear Libros y Ejemplares
        for idioma, llengua in llengues.items():
            faker = Faker(faker_idiomas.get(idioma, "en_US"))  # Faker en el idioma correcto

            for _ in range(10):
                llibre = Llibre.objects.create(
                    titol=faker.sentence(nb_words=4),  # Título en el idioma correcto
                    autor=faker.name(),
                    editorial=faker.company(),
                    ISBN=faker.isbn13(),
                    pagines=randint(100, 1000),
                    llengua=llengua  # Se guarda la lengua asociada
                )

                # Crear 2 ejemplares por libro
                for _ in range(2):
                    Exemplar.objects.create(
                        cataleg=llibre,
                        registre=faker.uuid4(),
                        exclos_prestec=faker.boolean(),
                        baixa=False
                    )

        self.stdout.write(self.style.SUCCESS("✅ Datos falsos generados con éxito 🎉"))