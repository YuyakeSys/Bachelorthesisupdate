from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(verbose_name="name", max_length=16, unique=True)
    password = models.CharField(verbose_name="password", max_length=64)
    age = models.IntegerField(verbose_name="age")
    status_choices = (
        (0, "Normal"),
        (1, "Banned"),
    )
    status = models.SmallIntegerField(verbose_name="status", choices=status_choices, default=0)
    plan_choices = (
        (0, "null"),
        (1, "monthly"),
        (2, "seasonally"),
        (3, "half-year"),
        (4, "annually"),
        (5, "lifelong"),
    )
    plan = models.SmallIntegerField(verbose_name="plan", choices=plan_choices, default=0)
    start_time = models.DateField(verbose_name="time", default='1999-09-19')
    gender_choices = (
        (1, "Male"),
        (2, "Female"),
    )
    gender = models.SmallIntegerField(verbose_name="sex", choices=gender_choices)
    email = models.EmailField(verbose_name="email", max_length=40, default="")

    def __str__(self):
        return self.name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if models.UserInfo.objects.filter(email=email):
            raise ValidationError("E-mail address already used")
        else:
            return email


class Game(models.Model):
    """ Games """
    name = models.CharField(verbose_name="game_name", max_length=48, unique=True)
    price = models.FloatField(verbose_name="game_price", max_length=15)
    description = models.CharField(verbose_name="game_description", max_length=200)
    label_choices = (
        (1, "Sports"),
        (2, "Action"),
        (3, "RolePlaying"),
        (4, "Adventure"),
        (5, "Simulation"),
        (6, "Strategy"),
    )
    label = models.SmallIntegerField(verbose_name="label", choices=label_choices)
    image = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    discount = models.FloatField(default=1)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url

    @property
    def getPrice(self):
        try:
            final_price = self.price * self.discount
        except:
            final_price = ''
        return final_price

    @property
    def getDiscount(self):
        final_discount = str(self.discount * 100) + "%"
        return final_discount


class Comment(models.Model):
    """ Comments of users """
    attitude_choices = (
        (1, "Recommended"),
        (2, "Not recommended"),
    )
    attitude = models.SmallIntegerField(verbose_name="attitude", choices=attitude_choices)
    comment = models.CharField(verbose_name="comment", max_length=200)
    game = models.ForeignKey(verbose_name="game", to="Game", to_field="name", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="user", to="UserInfo", to_field="name", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class List(models.Model):
    customer = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    cost = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        listitems = self.listitem_set.all()
        total = sum([item.get_total for item in listitems])
        return total

    @property
    def get_cart_items(self):
        listitems = self.listitem_set.all()
        total = sum([item.quantity for item in listitems])
        return total


class ListItem(models.Model):
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, blank=True, null=True)
    List = models.ForeignKey(List, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.game.price * self.quantity * self.game.discount
        return total


class Address(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(List, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=120, null=True)
    state = models.CharField(max_length=120, null=True)
    zipcode = models.CharField(max_length=120, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.address


class PlanOrder(models.Model):
    customer = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateField(auto_now_add=True)
    transaction_id = models.CharField(max_length=150, null=True)
    plan_choices = (
        (0, "null"),
        (1, "monthly"),
        (2, "seasonally"),
        (3, "half-year"),
        (4, "annually"),
        (5, "lifelong"),
    )
    plan = models.SmallIntegerField(verbose_name="plan", choices=plan_choices, null=False)

    def __str__(self):
        return str(self.id)


class Appeal(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=40, null=True)
    issue = models.CharField(max_length=500, null=True)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
