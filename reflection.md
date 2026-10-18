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

My design changed once I started thinking about what would happen when an owner had
more than one pet. At first, task collection was too close to the scheduling logic.
I moved that responsibility into `Owner.get_all_tasks()` and let `Scheduler` ask the
owner for the full list. That choice made the relationship between the classes much
clearer. I also added validation, completion tracking, priority ordering, recurrence,
and an optional time limit as the project grew. I checked the design with two pets in
`main.py` and with automated tests instead of assuming the class relationships worked.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler looks at whether a task is valid and unfinished, how important it is,
how long it takes, and how much time the owner has available. It also keeps track of
the pet, start time, and recurring frequency. I made priority and available time the
main planning constraints because urgent care, such as medication, should be selected
before a lower-priority activity when the owner has a busy day.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that conflict detection only checks for matching start times. For
example, an 8:00 walk lasting 30 minutes will not conflict with an 8:15 feeding task,
even though they overlap. I kept the exact-match rule because it is predictable and
easy to explain at this stage. If I continued the project, I would calculate end times
from each task's duration and detect partial overlaps too.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

The most useful AI features were being able to discuss a method, edit several related
files, and run the tests in the same workflow. I used the assistant to compare ways of
sorting tasks, explain `lambda` and `timedelta`, draft test cases, and check whether the
UML still matched the code. The best prompts were specific, such as asking for a small
method with an expected input and output. I still ran the tests and read the terminal
output myself before treating a suggestion as finished.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One suggestion I changed was an early design built around a separate `Schedule` class.
It added another object without giving it a clear responsibility, and the assignment
already called for a `Scheduler`. I kept `Scheduler` as the planning class and used
`Owner.get_all_tasks()` for multi-pet task collection. I also chose exact-time conflict
detection over a more complicated overlap algorithm because the simpler behavior fit
the data model I had actually built.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the actions that would cause the biggest problems if they were wrong: adding
and completing tasks, sorting them by time, filtering by pet, creating the next daily
task, and warning about duplicate times. I also tested a pet with no tasks because an
empty account is a normal starting point, not an error. Together, the six tests cover
the main scheduler behavior without depending on the Streamlit interface.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

My confidence level is 4 out of 5. All six tests pass, and the terminal demo exercises
the same methods with two pets. I am leaving one star open because the Streamlit
interactions are not covered by automated tests and the conflict rule does not catch
partially overlapping tasks. Those would be my next testing priorities.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied that the project stayed understandable as I added features. `Owner`
and `Pet` handle the relationships, `Task` holds care details, and `Scheduler` handles
the planning decisions. Because those responsibilities are separate, I could test the
algorithms directly without launching Streamlit every time.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

With another iteration, I would store start times as real time or datetime values and
calculate end times for better conflict detection. I would also add editing and deletion
controls and write Streamlit interaction tests so the interface has the same level of
coverage as the backend.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Using separate chats for design, algorithms, testing, and final polish helped me keep
each conversation focused. I could give the assistant only the context needed for that
phase and avoid mixing old ideas into the current task. My biggest takeaway is that the
AI can move quickly, but I still have to act as the lead architect: define the goal,
question suggestions, keep the class responsibilities clean, and verify the result with
tests and real output.
