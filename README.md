# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps pet owners organize care tasks and
build a practical daily plan.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

The project includes a Python scheduling layer, a Streamlit interface, an automated
test suite, and a [final Mermaid UML diagram](diagrams/uml_final.mmd).

## Features

- Add multiple pets and assign care tasks to each one.
- Record duration, priority, start time, and daily, weekly, or one-time frequency.
- Sort tasks chronologically with `Scheduler.sort_by_time()`.
- Filter the task table by pet and completion status with `Scheduler.filter_tasks()`.
- Show actionable warnings when pending tasks have the same start time.
- Mark tasks complete and automatically create the next daily or weekly occurrence.
- Build a priority-based plan that fits within the owner's available minutes.

## Implementation Summary

PawPal+ models each care activity with `Task`, including its description, duration, frequency, priority, and completion status. `Pet` stores tasks and associates them with a pet, while `Owner` manages multiple pets and exposes all of their tasks through `get_all_tasks()`. `Scheduler` uses that owner-level method to collect tasks across every pet, filters completed or invalid tasks, orders the remaining tasks by priority and duration, and can apply an available-time limit. The terminal demo in `main.py` shows the combined schedule for multiple pets.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

The terminal demo in `main.py` creates one owner with two pets and combines their tasks:

```
Today's Schedule
- 08:00 Give medication (Mochi) — 10 min, daily, pending
- 08:00 Morning walk (Mochi) — 30 min, daily, pending
- 18:00 Feed dinner (Whiskers) — 15 min, daily, pending
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
python -m pytest --cov
```

The test suite covers basic task completion and pet-task association, chronological
sorting, filtering by pet, empty-pet behavior, daily recurrence, and exact-time
conflict warnings.

Successful test output:

```
============================= test session starts ==============================
collected 6 items

tests/test_pawpal.py ......                                           [100%]

============================== 6 passed in 0.02s ===============================
```

**Confidence level:** ★★★★☆ (4/5). The core behaviors have automated happy-path
and edge-case coverage. A future version should add UI interaction tests and
overlapping-duration conflict tests.

## Smarter Scheduling

PawPal+ includes a small algorithmic layer to make the schedule useful as task data grows:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks chronologically using their `HH:MM` time. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name, completion status, or both. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warning messages for pending tasks with the same exact time. |
| Recurring tasks | `Scheduler.mark_task_complete()` and `Task.next_occurrence()` | Completing a daily or weekly task adds the next occurrence using `timedelta`. |

## Demo Walkthrough

The Streamlit UI supports the following workflow:

1. Enter an owner name and add one or more pets.
2. Select a pet, enter a task description, duration, priority, scheduled time, and
   recurrence frequency.
3. Filter the current tasks by pet or completion status. The table remains sorted
   chronologically.
4. If pending tasks share an exact time, review the warning and move one task to
   resolve the conflict.
5. Mark a task complete. Daily and weekly tasks automatically create their next
   occurrence.
6. Set available minutes and generate a priority-based schedule. The terminal demo
   also shows filtering, recurrence, and conflict output.

Example CLI output from `python main.py`:

```text
Today's Schedule
- 08:00 Give medication (Mochi) — 10 min, daily, pending
- 08:00 Morning walk (Mochi) — 30 min, daily, pending
- 18:00 Feed dinner (Whiskers) — 15 min, daily, pending

Tasks sorted by time:
- 08:00 Morning walk (Mochi) — 30 min, daily, pending
- 08:00 Give medication (Mochi) — 10 min, daily, pending
- 18:00 Feed dinner (Whiskers) — 15 min, daily, pending

Pending Mochi tasks:
- 08:00 Morning walk (Mochi) — 30 min, daily, pending
- 08:00 Give medication (Mochi) — 10 min, daily, pending

Conflict check:
Warning: 08:00 has both 'Morning walk' for Mochi and 'Give medication' for Mochi.

Recurring task created for 2026-10-20: Morning walk
```
