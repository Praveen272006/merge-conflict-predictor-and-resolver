let tasks = [];

function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}

function renderTasks() {
    const list = document.getElementById("taskList");
    list.innerHTML = "";
    tasks.forEach((task, index) => {
        const li = document.createElement("li");
        li.textContent = task;
        li.onclick = () => toggleDone(li);
        const btn = document.createElement("button");
        btn.textContent = "X";
        btn.onclick = (e) => {
            e.stopPropagation();
            deleteTask(index);
        };
        li.appendChild(btn);
        list.appendChild(li);
    });
}

function toggleDone(element) {
    element.classList.toggle("done");
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}

function deleteTask(index) {
    tasks.splice(index, 1);
    renderTasks();
}

function clearTasks() {
    tasks = [];
    renderTasks();
}

function countTasks() {
    alert("Total tasks: " + tasks.length);
}

// filler lines
//1 //2 //3 //4 //5
//6 //7 //8 //9 //10
//11 //12 //13 //14 //15
//16 //17 //18 //19 //20
//21 //22 //23 //24 //25


function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}

function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}

function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}

function addTask() {
    const input = document.getElementById("taskInput");
    const value = input.value.trim();
    if (value === "") return;
    tasks.push(value);
    input.value = "";
    renderTasks();
}
