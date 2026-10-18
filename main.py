"""Small terminal demo for PawPal+."""

from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="dog")
whiskers = Pet(name="Whiskers", species="cat")

mochi.add_task(Task("Morning walk", 30, frequency="daily", priority="high"))
mochi.add_task(Task("Give medication", 10, frequency="daily", priority="high"))
whiskers.add_task(Task("Feed dinner", 15, frequency="daily", priority="medium"))

owner.add_pet(mochi)
owner.add_pet(whiskers)

scheduler = Scheduler(owner)
print(scheduler.format_schedule())
