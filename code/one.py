from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

# Mock Database
tasks = [
    {"id": 1, "title": "Setup Project", "status": "Completed", "priority": "High"},
    {"id": 2, "title": "Design UI", "status": "In Progress", "priority": "Medium"},
    {"id": 3, "title": "API Integration", "status": "Pending", "priority": "Low"}
]

class TaskManager:
    def __init__(self, name):
        self.name = name
        self.created_at = datetime.datetime.now()

    def get_all_tasks(self):
        return tasks

    def add_task(self, title, priority):
        new_id = len(tasks) + 1
        new_task = {
            "id": new_id,
            "title": title,
            "status": "Pending",
            "priority": priority
        }
        tasks.append(new_task)
        return new_task

manager = TaskManager("Admin Dashboard")

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(manager.get_all_tasks())

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    priority = data.get('priority', 'Medium')
    if not title:
        return jsonify({"error": "Title is required"}), 400
    task = manager.add_task(title, priority)
    return jsonify(task), 201

@app.route('/api/status', methods=['GET'])
def system_status():
    return jsonify({
        "system": manager.name,
        "uptime": "Active",
        "timestamp": manager.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    print(f"Server starting for {manager.name}...")
    app.run(debug=True, port=5000)