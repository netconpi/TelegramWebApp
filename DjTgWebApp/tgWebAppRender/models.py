from django.db import models

# Create your models here.
class Company(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Назначено")
    # subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name="Предмет", null=True)
    telegram_id = models.CharField(max_length=255, verbose_name='Tg ID', null=True)
    name = models.CharField(max_length=255, verbose_name='Name', null=True)
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    work_time = models.TextField(null=True, blank=True, verbose_name="Work time")
    meet_timing = models.TextField(null=True, blank=True, verbose_name="Meet timing START")
    meet_timing_end = models.TextField(null=True, blank=True, verbose_name="Meet timing END")
    duration = models.TextField(null=True, blank=True, verbose_name="Duration")
    # links = models.TextField(null=True, blank=True, verbose_name="Links")
    email = models.CharField(max_length=255, blank=True, verbose_name='WhatsApp link', null=True)
    whatsapp = models.CharField(max_length=255, blank=True, verbose_name='whatsapp link', null=True)
    meeting_link = models.CharField(max_length=255, blank=True, verbose_name='Meeting link', null=True)
    skype = models.CharField(max_length=255, blank=True, verbose_name='Skype link', null=True)
    tg_link = models.CharField(max_length=255, blank=True, verbose_name='TG link', null=True)
    password_unsafe = models.CharField(max_length=255, blank=True, verbose_name='Password unsafe', null=True)
    password_confirm_unsafe = models.CharField(max_length=255, blank=True, verbose_name='Password unsafe', null=True)
    payment_data_unsafe = models.TextField(null=True, blank=True, verbose_name="Payment data unsafe")
    photo_url = models.TextField(null=True, blank=True, verbose_name="Photo url")

    def __str__(self) -> str:
        return f"Компания: {self.name}"

    class Meta:
        pass


class TelegramData(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Назначено")
    # subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name="Предмет", null=True)
    telegram_id = models.CharField(max_length=255, verbose_name='Tg ID', null=True)
    company_associated = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="Company associated", null=True)

    def __str__(self) -> str:
        return f"Пользователь: {self.telegram_id}"

    class Meta:
        pass


class Notification(models.Model):
    company_link = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="Company link", null=True)
    starts = models.DateTimeField(auto_now_add=True, verbose_name="Starts at: ")
    status = models.TextField(null=True, blank=True, verbose_name="Status")
    # user_attached = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="For who:")
    user_attached = models.ManyToManyField(Company, blank=True, symmetrical=False, related_name='user_attached')

    def __str__(self) -> str:
        return f"{self.company_link}"

    class Meta:
        ordering = ['starts']


class Event(models.Model):
    created_by = models.CharField(max_length=255, verbose_name='Tg ID', null=True)
    name = models.CharField(max_length=255, verbose_name='Name', null=True)
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    link_method = models.TextField(null=True, blank=True, verbose_name="Link method")
    meet_timing = models.TextField(null=True, blank=True, verbose_name="Meet timing")
    # links = models.TextField(null=True, blank=True, verbose_name="Links")
    user_attached = models.ManyToManyField(Company, blank=True, symmetrical=False, related_name='attached')
    category = models.TextField(null=True, blank=True, verbose_name="Cetegory")
    event_date = models.DateTimeField(auto_now_add=True, verbose_name="Date: ")

    def __str__(self) -> str:
        return f"{self.company_link}"

    class Meta:
        ordering = ['event_date']