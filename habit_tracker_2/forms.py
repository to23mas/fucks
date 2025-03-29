from django import forms
from habit_tracker_1.models import Habit


class HabitForm(forms.ModelForm): 
	class Meta:
		model = Habit # Určujeme, ze kterého modelu se má formulář generovat
		fields = ["name"]  # Z modelu chceme pouze jméno zvyku
		widgets = {
			"name": forms.TextInput( # name bude mít podobu <input type="text"> 
				attrs={ # Tímto způzobem se přidávají další html atributy
					"placeholder": "Název zvyku",
					"class": "habit_tracker_input_field",
		})}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["name"].label = False  # Nechceme zobrazovat html zančku <label>
