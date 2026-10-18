"""Core data classes and scheduling logic for PawPal+."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """A single pet-care activity."""

    description: str
    duration_minutes: int
    frequency: str = "daily"
    completed: bool = False
    priority: str = "medium"
    pet_name: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_valid(self) -> bool:
        """Return whether the task has usable scheduling information."""
        valid_priorities = {"low", "medium", "high"}
        return (
            bool(self.description.strip())
            and self.duration_minutes > 0
            and bool(self.frequency.strip())
            and self.priority in valid_priorities
        )

    def format_for_schedule(self) -> str:
        """Return a readable line for a terminal schedule."""
        pet_label = f" ({self.pet_name})" if self.pet_name else ""
        status = "done" if self.completed else "pending"
        return (
            f"- {self.description}{pet_label} — "
            f"{self.duration_minutes} min, {self.frequency}, {status}"
        )


@dataclass
class Pet:
    """A pet and the care tasks assigned to it."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task and associate it with this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    """An owner who manages one or more pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's account."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task belonging to every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.get_tasks()]


@dataclass
class Scheduler:
    """The scheduling brain that organizes tasks across all of an owner's pets."""

    owner: Owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve tasks through the owner's multi-pet access method."""
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> List[Task]:
        """Return valid, incomplete tasks from all of the owner's pets."""
        return [
            task for task in self.get_all_tasks() if not task.completed and task.is_valid()
        ]

    def build_schedule(self, available_minutes: Optional[int] = None) -> List[Task]:
        """Build a priority-ordered schedule, optionally bounded by available time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks = sorted(
            self.get_pending_tasks(),
            key=lambda task: (priority_order[task.priority], task.duration_minutes),
        )

        if available_minutes is None:
            return tasks

        schedule: List[Task] = []
        minutes_used = 0
        for task in tasks:
            if minutes_used + task.duration_minutes <= available_minutes:
                schedule.append(task)
                minutes_used += task.duration_minutes
        return schedule

    def format_schedule(self, available_minutes: Optional[int] = None) -> str:
        """Return a readable schedule for terminal output."""
        tasks = self.build_schedule(available_minutes)
        if not tasks:
            return "Today's Schedule\n- No pending tasks."
        lines = ["Today's Schedule"]
        lines.extend(task.format_for_schedule() for task in tasks)
        return "\n".join(lines)
