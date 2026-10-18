from pawpal_system import Pet, Task


def test_task_completion_changes_status():
    task = Task("Morning walk", duration_minutes=30)

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")

    pet.add_task(Task("Feed breakfast", duration_minutes=10))

    assert len(pet.tasks) == 1
