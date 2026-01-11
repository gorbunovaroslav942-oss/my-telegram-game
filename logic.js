let tg = window.Telegram.WebApp;
tg.expand();

let state = { money: 100, hunger: 100, clean: 100, hasPoo: false };

window.onload = () => {
    const v = Date.now();
    // Обновляем пути (проверь расширения .jpg или .png у себя!)
    document.getElementById('img-feed').src = "feed_btn.jpg?v=" + v;
    document.getElementById('img-play').src = "play_btn.jpg?v=" + v;
    document.getElementById('img-clean-static').src = "clean_disabled.png?v=" + v;
    document.getElementById('img-clean-active').src = "clean_active.png?v=" + v;
    document.getElementById('pet-img').src = "cat.jpg?v=" + v;
    updateUI();
};

function switchTab(e, name) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active-tab'));
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active-nav'));
    document.getElementById(name).classList.add('active-tab');
    if(e) e.currentTarget.classList.add('active-nav');
    tg.HapticFeedback.impactOccurred('light');
}

function updateUI() {
    document.getElementById('money').innerText = state.money;
    document.getElementById('hunger').innerText = Math.floor(state.hunger);
    document.getElementById('clean').innerText = Math.floor(state.clean);
    
    const btnActive = document.getElementById('clean-btn');
    const btnStatic = document.getElementById('clean-static');

    if (state.hasPoo) {
        btnActive.style.display = 'block';
        btnStatic.style.display = 'none';
    } else {
        btnActive.style.display = 'none';
        btnStatic.style.display = 'block';
    }
}

function action(type) {
    if (type === 'feed' && state.money >= 10) {
        state.money -= 10; 
        state.hunger = Math.min(100, state.hunger + 25);
        tg.HapticFeedback.notificationOccurred('success');
    } else if (type === 'play') {
        state.money += 15; 
        state.hunger = Math.max(0, state.hunger - 15);
        tg.HapticFeedback.impactOccurred('medium');
    }
    updateUI();
}

function cleanPoo() {
    if (!state.hasPoo) return;
    state.hasPoo = false; 
    state.clean = 100;
    tg.HapticFeedback.notificationOccurred('success');
    updateUI();
}

setInterval(() => {
    state.hunger = Math.max(0, state.hunger - 1);
    if (Math.random() > 0.90) state.hasPoo = true;
    if (state.hasPoo) state.clean = Math.max(0, state.clean - 2);
    updateUI();
}, 5000);
