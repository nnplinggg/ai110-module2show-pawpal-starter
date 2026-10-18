"""Small terminal demo for PawPal+."""

from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="dog")
whiskers = Pet(name="Whiskers", species="cat")

mochi.add_task(
    Task("Morning walk", 30, frequency="daily", priority="high", time="08:00")
)
mochi.add_task(
    Task("Give medication", 10, frequency="daily", priority="high", time="08:00")
)
whiskers.add_task(
    Task("Feed dinner", 15, frequency="daily", priority="medium", time="18:00")
)

owner.add_pet(mochi)
owner.add_pet(whiskers)

scheduler = Scheduler(owner)
print(scheduler.format_schedule())

print("\nTasks sorted by time:")
for task in scheduler.sort_by_time():
    print(task.format_for_schedule())

print("\nPending Mochi tasks:")
for task in scheduler.filter_tasks(pet_name="Mochi", completed=False):
    print(task.format_for_schedule())

print("\nConflict check:")
for warning in scheduler.detect_conflicts():
    print(warning)

completed_task = mochi.tasks[0]
next_task = scheduler.mark_task_complete(completed_task)
if next_task:
    print(f"\nRecurring task created for {next_task.due_date}: {next_task.description}")
