import streamlit as st
import mysql.connector


# ---------------- DATABASE CONNECTION ----------------

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOURPASSWORD",
        database="taskly"
    )


# ---------------- ADD TASK ----------------

def add_task(task):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, status) VALUES (%s, 'active')",
        (task,)
    )

    db.commit()
    cursor.close()
    db.close()


# ---------------- GET TASKS ----------------

def get_tasks(status):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, task FROM tasks WHERE status = %s",
        (status,)
    )

    tasks = cursor.fetchall()

    cursor.close()
    db.close()

    return tasks


# ---------------- UPDATE TASK ----------------

def update_status(task_id, status):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE tasks SET status = %s WHERE id = %s",
        (status, task_id)
    )

    db.commit()
    cursor.close()
    db.close()


# ---------------- DELETE PERMANENTLY ----------------

def delete_task(task_id):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    db.commit()
    cursor.close()
    db.close()


# ---------------- PAGE DESIGN ----------------

st.set_page_config(
    page_title="Taskly",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background-color: #111827;
    color: white;
}

.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.task {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------

st.markdown(
    '<div class="title">Taskly ✨</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your little space to get things done 🌙</div>',
    unsafe_allow_html=True
)


# ---------------- ADD TASK ----------------

task = st.text_input(
    " ",
    placeholder="What do you need to do?"
)

if st.button("➕ Add Task"):

    if task.strip() != "":
        add_task(task)
        st.success("Task added!")
        st.rerun()

    else:
        st.warning("Please enter a task.")


st.divider()


# ---------------- TABS ----------------

tab1, tab2, tab3 = st.tabs(
    ["📋 My Tasks", "✅ Completed", "🗑️ Bin"]
)


# =====================================================
# ACTIVE TASKS
# =====================================================

with tab1:

    st.subheader("My Tasks")

    tasks = get_tasks("active")

    if len(tasks) == 0:

        st.info("🌱 No tasks yet. Add something!")

    else:

        for task_id, task_name in tasks:

            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:
                st.write("📝", task_name)

            with col2:
                if st.button("✓", key=f"complete{task_id}"):

                    update_status(task_id, "completed")
                    st.rerun()

            with col3:
                if st.button("🗑️", key=f"delete{task_id}"):

                    update_status(task_id, "bin")
                    st.rerun()


# =====================================================
# COMPLETED TASKS
# =====================================================

with tab2:

    st.subheader("Completed 🎉")

    tasks = get_tasks("completed")

    if len(tasks) == 0:

        st.info("Complete a task and it will appear here.")

    else:

        for task_id, task_name in tasks:

            col1, col2 = st.columns([6, 1])

            with col1:
                st.write("✅", task_name)

            with col2:
                if st.button("🗑️", key=f"completed_delete{task_id}"):

                    update_status(task_id, "bin")
                    st.rerun()


# =====================================================
# BIN
# =====================================================

with tab3:

    st.subheader("Bin 🗑️")

    tasks = get_tasks("bin")

    if len(tasks) == 0:

        st.info("Your bin is empty.")

    else:

        for task_id, task_name in tasks:

            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:
                st.write("🗑️", task_name)

            with col2:
                if st.button("♻️", key=f"restore{task_id}"):

                    update_status(task_id, "active")
                    st.rerun()

            with col3:
                if st.button("❌", key=f"permanent{task_id}"):

                    delete_task(task_id)
                    st.rerun()


# ---------------- FOOTER ----------------

st.divider()

st.caption("Taskly • Small steps, big progress ✨")