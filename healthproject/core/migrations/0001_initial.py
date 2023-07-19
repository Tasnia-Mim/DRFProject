# Generated by Django 4.2.3 on 2023-07-18 10:11

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_doctor", models.BooleanField(default=False)),
                ("is_patient", models.BooleanField(default=False)),
                ("is_organization_user", models.BooleanField(default=False)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Medicine",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Prescription",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                ("treatment", models.TextField(blank="True", null="True")),
                (
                    "doctor",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor_prescription",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prescription",
                        to="core.medicine",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_prescription",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PatientFollow",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follow_receiver_doctor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follow_sender_patient",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "blood_group",
                    models.CharField(blank="True", max_length=50, null="True"),
                ),
                ("weight", models.TextField(blank="True", null="True")),
                ("height", models.TextField(blank="True", null="True")),
                (
                    "gender",
                    models.CharField(
                        blank="True",
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Others", "Others"),
                        ],
                        max_length=20,
                        null="True",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("address", models.TextField(blank="True", null="True")),
                (
                    "user",
                    models.OneToOneField(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrganizationUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(blank="True", max_length=100, null="True")),
                (
                    "gender",
                    models.CharField(
                        blank="True",
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Others", "Others"),
                        ],
                        max_length=20,
                        null="True",
                    ),
                ),
                (
                    "personal_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("personal_address", models.TextField(blank="True", null="True")),
                (
                    "user",
                    models.OneToOneField(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DoctorFollow",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "follow_status",
                    models.CharField(
                        blank="True",
                        choices=[
                            ("approved", "approved"),
                            ("canceled", "canceled"),
                            ("pending", "pending"),
                        ],
                        max_length=20,
                        null="True",
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follow_receiver",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follow_sender",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "speciality",
                    models.CharField(blank="True", max_length=100, null="True"),
                ),
                (
                    "chamber_email",
                    models.CharField(blank="True", max_length=100, null="True"),
                ),
                (
                    "chamber_phone",
                    models.CharField(blank="True", max_length=100, null="True"),
                ),
                (
                    "personal_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("personal_address", models.TextField(blank="True", null="True")),
                ("about", models.TextField(blank="True", null="True")),
                (
                    "gender",
                    models.CharField(
                        blank="True",
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Others", "Others"),
                        ],
                        max_length=20,
                        null="True",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("tittle", models.CharField(blank="True", max_length=200, null="True")),
                ("blog", models.TextField(blank="True", null="True")),
                (
                    "blogger",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blogs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("request_time", models.DateTimeField(auto_now_add=True)),
                ("problem", models.TextField(blank="True", null="True")),
                (
                    "appointment_time",
                    models.DateTimeField(blank="True", max_length=100, null="True"),
                ),
                ("fee", models.TextField(blank="True", null="True")),
                (
                    "appointment_status",
                    models.CharField(
                        blank="True",
                        choices=[
                            ("approved", "approved"),
                            ("canceled", "canceled"),
                            ("pending", "pending"),
                        ],
                        max_length=20,
                        null="True",
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor_appointment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank="True",
                        null="True",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_appointment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]