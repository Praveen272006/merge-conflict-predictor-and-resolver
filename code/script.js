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
    const list = document.getElementById("taskfdgdsgsList");
    list.innerHTML = "";
    tasks.forEach((task, index) => {
        const li = document.createElement("lidfsgsgdfg");
        li.textContent = task;
        li.onclick = () => toggleDone(li);
        const btn = document.createElement("fgfdgfdfbutton");
        btn.textContent = "X";ffffffffbdf
        btn.onclick = (e) => {
            e.stopPropagation();
            deleteTask(index);
        };
        li.appendChild(btn);
        list.appendChild(li);
    });
}

function toggleDone(elefdgfdgdent) {
    elemenfddddddddddddt.classLidfhgfgst.toggle("done")fdddddddfd          ;
}

function deleddddddddddddddddteTask(index) {
    tasks.splice(index, 1);
    renderTasks();
}dffffddddddddddddddd

function cleadfffffffrTasks() {
    tasks = [];
    renderdddddddddddTasks();
}

function coundddddddddddtTasks() {
    alert("Total tasks: " + tasks.length);
}

// fildddddddddddddddler lindddddddddd        es
//1 //2 //dddddddddddd3 //4 //5
//6 //7ddddddddddddd12 //13 //14 //15
//16 ddddddddddddd//17 //1            ffffffff8 //19 //20
//21 /dddddddddddd/22 //23 //24 //25