async function loadForum() {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) return;
        
        const threads = await api.getForumThreads();
        const contributors = await api.getTopContributors();
        
        displayForumThreads(threads.threads);
        displayTopContributors(contributors.contributors);
    } catch (error) {
        console.error('Error loading forum:', error);
    }
}

function displayForumThreads(threads) {
    const container = document.getElementById('forumThreads');
    container.innerHTML = '';
    
    threads.forEach(thread => {
        const div = document.createElement('div');
        div.className = 'thread-item';
        div.innerHTML = `
            <h4>${thread.title}</h4>
            <p>${thread.preview || thread.content.substring(0, 100)}...</p>
            <small>By ${thread.author} • ${new Date(thread.createdAt).toLocaleDateString()} • ${thread.responseCount} replies</small>
        `;
        div.onclick = () => viewThread(thread.id);
        container.appendChild(div);
    });
}

function displayTopContributors(contributors) {
    const container = document.getElementById('topContributors');
    container.innerHTML = '';
    
    contributors.forEach((contributor, index) => {
        const div = document.createElement('div');
        div.className = 'contributor-item';
        div.innerHTML = `
            <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold;">
                ${index + 1}
            </div>
            <div>
                <p style="margin: 0; font-weight: bold;">${contributor.name}</p>
                <p style="margin: 0; font-size: 0.9rem; color: #666;">${contributor.postCount} posts</p>
            </div>
        `;
        container.appendChild(div);
    });
}

function viewThread(threadId) {
    alert(`View thread ${threadId} - implement thread detail view`);
}

function showNewThreadForm() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <h2>Start a Discussion</h2>
            <input type="text" id="threadTitle" placeholder="Discussion Title" class="input-field">
            <textarea id="threadContent" placeholder="What do you want to discuss?" class="input-field" style="min-height: 150px; resize: vertical;"></textarea>
            <button class="btn-primary" onclick="createThread()">Post Discussion</button>
        </div>
    `;
    document.body.appendChild(modal);
}

async function createThread() {
    const title = document.getElementById('threadTitle').value;
    const content = document.getElementById('threadContent').value;
    
    if (!title || !content) {
        alert('Please fill all fields');
        return;
    }
    
    try {
        await api.createThread({ title, content });
        alert('Discussion posted successfully!');
        loadForum();
        document.querySelector('.modal').remove();
    } catch (error) {
        alert('Error posting discussion: ' + error.message);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('forum')) {
        loadForum();
        setInterval(loadForum, 60000);
    }
});