let tasks = [];
const BACKEND_URL = 'http://localhost:8000';

function addTask() {
    const title = document.getElementById('taskTitle').value.trim();
    const hours = parseFloat(document.getElementById('hours').value) || 1;
    const importance = parseInt(document.getElementById('importance').value) || 5;

    if (!title) {
        alert('Please enter task title');
        return;
    }

    const task = {
        title: title,
        estimated_hours: hours,
        importance: importance,
        due_date: new Date(Date.now() + 86400000).toISOString().split('T')[0]
    };

    tasks.push(task);
    updateTaskList();
    clearForm();
}

function clearForm() {
    document.getElementById('taskTitle').value = '';
    document.getElementById('hours').value = '1';
    document.getElementById('importance').value = '5';
}

function updateTaskList() {
    const list = document.getElementById('taskList');
    list.innerHTML = '';

    tasks.forEach((task, index) => {
        const item = document.createElement('div');
        item.className = 'task-item';
        item.innerHTML = `
            <div>
                <strong>${task.title}</strong><br>
                <small>${task.estimated_hours}h | Importance: ${task.importance}/10</small>
            </div>
            <button class="remove-btn" onclick="removeTask(${index})">❌</button>
        `;
        list.appendChild(item);
    });
}

function removeTask(index) {
    tasks.splice(index, 1);
    updateTaskList();
}

async function analyzeTasks() {
    if (tasks.length === 0) {
        alert('Please add tasks first');
        return;
    }

    showLoading('results', '🔮 Analyzing your tasks...');
    const strategy = document.getElementById('strategy').value;

    try {
        const response = await fetch(`${BACKEND_URL}/api/tasks/analyze/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({tasks: tasks, strategy: strategy})
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        const data = await response.json();
        displayResults(data.tasks, '🎯 Your Analyzed Tasks');
        
    } catch (error) {
        showError('results', `❌ Connection Failed! Make sure backend is running:\n\ncd backend\npython manage.py runserver`);
    }
}

async function getSuggestions() {
    showLoading('results', '💡 Getting smart suggestions...');
    const strategy = document.getElementById('strategy').value;

    try {
        const response = await fetch(`${BACKEND_URL}/api/tasks/suggest/?strategy=${strategy}`);
        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        const data = await response.json();
        displayResults(data.suggestions, '🌟 Top Suggestions');
        
    } catch (error) {
        showError('results', `❌ Connection Failed! Make sure backend is running:\n\ncd backend\npython manage.py runserver`);
    }
}

function displayResults(items, title) {
    const container = document.getElementById('results');
    container.innerHTML = `<h3>${title}</h3>`;

    if (!items || items.length === 0) {
        container.innerHTML += '<div class="error">No results found</div>';
        return;
    }

    items.forEach((item, index) => {
        const priority = getPriority(item.score);
        const element = document.createElement('div');
        element.className = `result-item ${priority}`;
        element.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4>${index + 1}. ${item.title || 'Unnamed Task'}</h4>
                <div class="score">${item.score || 'N/A'}</div>
            </div>
            <div style="color: #666; margin-top: 10px; font-style: italic;">
                ${item.explanation || 'No explanation available'}
            </div>
            <div style="margin-top: 15px; color: #7f8c8d;">
                Priority: <strong style="color: inherit;">${priority.toUpperCase()}</strong>
            </div>
        `;
        container.appendChild(element);
    });
}

function getPriority(score) {
    if (score >= 80) return 'critical';
    if (score >= 60) return 'high';
    if (score >= 40) return 'medium';
    return 'low';
}

function showLoading(containerId, message) {
    document.getElementById(containerId).innerHTML = `<div class="loading">${message}</div>`;
}

function showError(containerId, message) {
    document.getElementById(containerId).innerHTML = `<div class="error">${message}</div>`;
}

function clearAll() {
    if (confirm('Clear all tasks?')) {
        tasks = [];
        updateTaskList();
        document.getElementById('results').innerHTML = '<div class="loading">🎯 Add tasks and click "Analyze" to see magical results!</div>';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    updateTaskList();
    showLoading('results', '✨ Welcome! Add your tasks and click "Analyze Tasks" to see smart prioritization!');
});