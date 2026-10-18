from datetime import time as clock_time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown(
    """
PawPal+ helps a pet owner keep track of care tasks and build a daily plan.
The owner and pet data are stored in Streamlit session state so they survive
the reruns caused by form interactions.
"""
)


# Streamlit reruns this file from top to bottom after most interactions. Keep
# the Owner object in session_state so it is created only once per session.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

with st.expander("Owner and pet", expanded=True):
    owner_name = st.text_input("Owner name", value=owner.name)
    owner.name = owner_name

st.subheader("Add a pet")
pet_name = st.text_input("New pet name", value="Mochi", key="new_pet_name")
species = st.selectbox(
    "Species", ["dog", "cat", "other"], key="new_pet_species"
)

if st.button("Add pet"):
    if not pet_name.strip():
        st.error("Enter a pet name.")
    elif any(existing_pet.name == pet_name for existing_pet in owner.pets):
        st.warning(f"{pet_name} is already in your pets.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name} to your pets.")

if owner.pets:
    st.write("Pets in this session:")
    st.write(", ".join(f"{pet.name} ({pet.species})" for pet in owner.pets))

    st.subheader("Add a care task")
    selected_pet = st.selectbox(
        "Pet for this task",
        owner.pets,
        format_func=lambda pet: f"{pet.name} ({pet.species})",
    )
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_description = st.text_input(
            "Task description", value="Morning walk"
        )
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        task_time = st.time_input("Time", value=clock_time(9, 0))
    with col5:
        frequency = st.selectbox("Repeats", ["daily", "weekly", "once"])

    if st.button("Add task"):
        selected_pet.add_task(
            Task(
                description=task_description,
                duration_minutes=int(duration),
                frequency=frequency,
                priority=priority,
                time=task_time.strftime("%H:%M"),
            )
        )
        st.success(f"Added task for {selected_pet.name}.")
else:
    st.info("Add a pet before scheduling a care task.")


all_tasks = owner.get_all_tasks()
if all_tasks:
    st.subheader("Current tasks")
    st.table(
        [
            {
                "Pet": task.pet_name,
                "Task": task.description,
                "Duration (min)": task.duration_minutes,
                "Time": task.time,
                "Repeats": task.frequency,
                "Priority": task.priority,
                "Completed": task.completed,
            }
            for task in scheduler.sort_by_time(all_tasks)
        ]
    )

    for warning in scheduler.detect_conflicts():
        st.warning(warning)
else:
    st.info("No tasks yet. Add one above.")


st.subheader("Today's schedule")
available_minutes = st.number_input(
    "Available time today (minutes)", min_value=1, max_value=1440, value=120
)

if st.button("Generate schedule"):
    selected_schedule = scheduler.build_schedule(int(available_minutes))
    if selected_schedule:
        st.success(f"Scheduled {len(selected_schedule)} task(s) within the time limit.")
    st.code(scheduler.format_schedule(int(available_minutes)))
