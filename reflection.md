# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design uses four classes:

- **Owner** stores the owner's name and pets. It can add a pet and return every task across all pets through `get_all_tasks()`.
- **Pet** stores a pet's name, species, and care tasks. It can add a task and return its task list.
- **Task** represents one care activity, including its description, duration, frequency, priority, and completion status. It can mark itself complete, validate its data, and format itself for a schedule.
- **Scheduler** is the system's planning brain. It receives an `Owner`, retrieves tasks through `Owner.get_all_tasks()`, filters pending tasks, orders them by priority and duration, and applies an optional time limit.

The relationships are that an owner can have multiple pets, each pet can have multiple care tasks, and a scheduler organizes tasks from all of the owner's pets.

The three core actions a user should be able to perform are:

1. **Add or update a pet profile:** The user can enter basic information about their pet, such as its name and type, and edit that information when it changes.
2. **Add or edit a care task:** The user can record tasks such as walks, feeding, medication, enrichment, or grooming, including how long each task takes and how important it is.
3. **Generate and review today's care plan:** The user can provide their available time and preferences, then generate a daily schedule. The app displays the selected tasks clearly and explains how time limits, priorities, and other constraints affected the plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

During the AI review of [pawpal_system.py](./pawpal_system.py), I first noticed that a plan needed to work across multiple pets rather than only one pet. I accepted the suggestion to add `Owner.get_all_tasks()` and make `Scheduler` call that method, which keeps multi-pet collection in one place. I also accepted the suggestion to add validation, completion handling, priority ordering, and an optional time limit. I rejected keeping the earlier `Schedule` class as the planning brain because the assignment specifically calls for a `Scheduler`; I replaced it with `Scheduler` and updated the UML. I verified the design by creating two pets in `main.py`, adding tasks to both, and checking that the formatted schedule includes tasks from both pets. The quick tests also verify completion and task addition directly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to turn the UML skeleton into working dataclasses, clarify how `Scheduler` should retrieve tasks from an `Owner`, generate the terminal demo, and draft the two focused pytest tests. Prompts that named the required classes, relationships, and expected behavior were the most helpful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I did not keep the first `Schedule`-based design unchanged because it did not match the required `Scheduler` class and could encourage scheduling only one pet's tasks. I compared the suggestion with the assignment requirements, changed the design to use `Owner.get_all_tasks()`, and verified the multi-pet behavior in `main.py` and the tests in `tests/test_pawpal.py`.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
