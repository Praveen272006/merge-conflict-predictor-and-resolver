document.addEventListener('DOMContentLoaded', () => {
    const taskBody = document.getElementById('task-body');
    const modal = document.getElementById('task-modal');
    const addBtn = document.getElementById('add-task-btn');
    const closeBtn = document.querySelector('.close');
    const taskForm = document.getElementById('new-task-form');

    let tasks = [
        { id: 1, name: "Database Optimization", status: "In Progress", priority: "High" },
        { id: 2, name: "Login Bug Fix", status: "Pending", priority: "High" },
        { id: 3, name: "UI Polish", status: "Completed", priority: "Low" },
        { id: 4, name: "Mobile Responsiveness", status: "In Progress", priority: "Medium" }
    ];

    function renderTasks() {
        taskBody.innerHTML = '';
        tasks.forEach(task => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>#${task.id}</td>
                <td>${task.name}</td>
                <td><span class="badge ${task.status.toLowerCase().replace(' ', '-')}">${task.status}</span></td>
                <td>${task.priority}</td>
                <td><button onclick="deleteTask(${task.id})" class="btn-delete">Delete</button></td>
            `;
            taskBody.appendChild(row);
        });
        updateStats();
    }

    function updateStats() {
        document.getElementById('total-count').innerText = tasks.length;
        document.getElementById('comp-count').innerText = tasks.filter(t => t.status === 'Completed').length;
        document.getElementById('pend-count').innerText = tasks.filter(t => t.status === 'Pending').length;
    }

    window.deleteTask = (id) => {
        tasks = tasks.filter(t => t.id !== id);
        renderTasks();
    };

    addBtn.onclick = () => {
        modal.style.display = "block";
    };

    closeBtn.onclick = () => {
        modal.style.display = "none";
    };

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    taskForm.onsubmit = (e) => {
        e.preventDefault();
        const title = document.getElementById('task-title').value;
        const priority = document.getElementById('task-priority').value;

        const newTask = {
            id: tasks.length + 1,
            name: title,
            status: "Pending",
            priority: priority
        };

        tasks.push(newTask);
        renderTasks();
        modal.style.display = "none";
        taskForm.reset();
        
        console.log("Task added successfully:", title);
        alert("Success! New task has been created.");
    };

    // Initial log for debugging
    console.log("Dashboard Initialized...");
    console.log("Current Task Count:", tasks.length);
    renderTasks();
});

// Utility function for animations
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
}