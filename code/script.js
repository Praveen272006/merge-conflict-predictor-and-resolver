const form = document.getElementById("studentForm");
const table = document.getElementById("studentTable").getElementsByTagName('tbody')[0];

let students = [];

form.addEventListener("submit",function(e){

e.preventDefault();

let name=document.getElementById("name").value;
let age=document.getElementById("age").value;
let dept=document.getElementById("dept").value;

let student={
name:name,
age:age,
dept:dept
};

students.push(student);

displayStudents();

form.reset();

});

function displayStudents(){

table.innerHTML="";

students.forEach(function(student,index){

let row=table.insertRow();

let cell1=row.insertCell(0);
let cell2=row.insertCell(1);
let cell3=row.insertCell(2);
let cell4=row.insertCell(3);

cell1.innerHTML=student.name;
cell2.innerHTML=student.age;
cell3.innerHTML=student.dept;

let btn=document.createElement("button");

btn.innerText="Delete";
btn.className="delete-btn";

btn.onclick=function(){
deleteStudent(index);
};

cell4.appendChild(btn);

});

}

function deleteStudent(index){

students.splice(index,1);

displayStudents();

}

function searchStudent(name){

return students.filter(function(student){

return student.name.toLowerCase().includes(name.toLowerCase());

});

}