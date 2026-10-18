"""Class skeleton for the PawPal+ pet-care planning system."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A care task that may be included in a pet's daily plan."""

    title: str
    duration_minutes: int
    priority: str
    notes: str = ""

    def validate(self) -> bool:
        """Return whether this task has valid scheduling data."""
        pass

    def describe(self) -> str:
        """Return a human-readable description of the task."""
        pass


@dataclass
class Pet:
    """Basic pet information and the care tasks associated with the pet."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        pass

    def update_profile(self, name: str, species: str) -> None:
        """Update the pet's basic profile information."""
        pass


@dataclass
class Owner:
    """Pet-owner information, preferences, and pets."""

    name: str
    preferences: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's profile."""
        pass

    def update_preferences(self, preferences: str) -> None:
        """Update the owner's care-planning preferences."""
        pass


@dataclass
class Schedule:
    """A daily plan containing selected care tasks and its explanation."""

    date: str
    available_minutes: int
    selected_tasks: list[Task] = field(default_factory=list)
    explanation: str = ""

    def build(self, tasks: list[Task]) -> None:
        """Build a plan from tasks, respecting constraints and priorities."""
        pass

    def display(self) -> str:
        """Return a human-readable version of the daily plan."""
        pass
