from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status():
    task = Task("Morning walk", duration_minutes=30)

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")

    pet.add_task(Task("Feed breakfast", duration_minutes=10))

    assert len(pet.tasks) == 1


def test_scheduler_sorts_and_filters_tasks():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task("Dinner", 15, time="18:00"))
    pet.add_task(Task("Walk", 30, time="08:00"))
    owner = Owner(name="Jordan", pets=[pet])
    scheduler = Scheduler(owner)

    assert [task.description for task in scheduler.sort_by_time()] == ["Walk", "Dinner"]
    assert [task.description for task in scheduler.filter_tasks(pet_name="Mochi")] == [
        "Dinner",
        "Walk",
    ]


def test_completing_daily_task_creates_next_occurrence():
    pet = Pet(name="Mochi", species="dog")
    task = Task("Medication", 10, frequency="daily", due_date=date(2026, 10, 19))
    pet.add_task(task)
    scheduler = Scheduler(Owner(name="Jordan", pets=[pet]))

    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 10, 20)
    assert len(pet.tasks) == 2


def test_conflicts_report_exact_matching_times():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task("Walk", 30, time="08:00"))
    pet.add_task(Task("Medication", 10, time="08:00"))
    scheduler = Scheduler(Owner(name="Jordan", pets=[pet]))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
