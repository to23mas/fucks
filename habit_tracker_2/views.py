from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import HabitForm
from habit_tracker_1.models import Habit


def habit_tracker(request):
	if request.method == "POST":
		form = HabitForm(request.POST)
		if form.is_valid():
			habit_name = form.cleaned_data["name"]
			Habit.objects.create(name=habit_name)

			return redirect("habit_tracker_2:index")
	else:
		form = HabitForm()

	reset_progress()
	habits = Habit.objects.all()

	return render(request, "habit_tracker_2/index.html", {
		"habits": habits,
		"form": form,
	})

def complete_habit(request, habit_id):
	habit = Habit.objects.get(id=habit_id)
	habit.completed = True
	habit.date_completed = timezone.now().date()
	habit.completion_count += 1 
	habit.save()

	reset_progress()

	return redirect("habit_tracker_2:index")


def delete_habit(request, habit_id):
	habit = Habit.objects.get(id=habit_id)
	habit.delete()

	return redirect("habit_tracker_2:index")

def reset_progress():
	current_date = timezone.now().date()
	habits = Habit.objects.all()

	for habit in habits:
		if habit.date_completed != current_date:
			habit.completion_count = 0
			habit.date_completed = None
			habit.save()
