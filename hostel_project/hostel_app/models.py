from django.db import models

# Create your models here.

"""class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    room_no = models.CharField(max_length=10)
    base_rent = models.IntegerField(default=1000)
    food_fee = models.IntegerField(default=3000)

    def __str__(self):
        return self.name"""


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    room_no = models.CharField(max_length=10)
    extra_fees = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # for ice cream
    
    def calculate_fee(self, month_days=30):
        base_rent = 1000
        food_fee = 100 * month_days

        # apply mess cut
        total_cut = 0
        mess_cuts = self.messcut_set.all()  # related mess cuts
        for cut in mess_cuts:
            days = (cut.to_date - cut.from_date).days + 1
            if days >= 3:
                total_cut += days * 100

        return base_rent + food_fee - total_cut + self.extra_fees


class MessCut(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()

    def days_count(self):
        return (self.to_date - self.from_date).days + 1


class IceCream(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name} - Rs.{self.price}"


class StudentIceCream(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    icecream = models.ForeignKey(IceCream, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
