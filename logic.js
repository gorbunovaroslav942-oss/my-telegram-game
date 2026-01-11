let tg = window.Telegram.WebApp;
tg.expand();

let state = { money: 100, hunger: 100, clean: 100, hasPoo: false };

window.onload = () => {
    const v = Date.now();
    const assets = {
        'img-feed': 'feed_btn.png',
        'img-play': 'play_btn.png',
        'img-clean-static': 'clean_disabled.png',
        'img-clean-active': 'clean_active.png',
        'pet-img': 'cat.png'
    };
    
    for (let id in assets) {
        let el = document.getElementById(id);
        if (el) el.src = assets[id] + "?v=" + v;
    }
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
        btnActive.style.display = 'flex'; // Используем flex для центрирования
        btnStatic.style.display = 'none';
    } else {
        btnActive.style.display = 'none';
        btnStatic.style.display = 'flex'; // Используем flex для центрирования
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
