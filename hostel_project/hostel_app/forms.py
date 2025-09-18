from django import forms
from .models import Student, MessCut, StudentIceCream, IceCream

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'room_no']

class MessCutForm(forms.ModelForm):
    class Meta:
        model = MessCut
        fields = ['from_date', 'to_date']

#class StudentIceCreamForm(forms.ModelForm):
 #   class Meta:
  #      model = StudentIceCream
   #     fields = ['icecream']


class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['name', 'price']