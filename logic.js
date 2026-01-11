let tg = window.Telegram.WebApp;
tg.expand();

// Переменные состояния
let state = { money: 100, hunger: 100, clean: 100, hasPoo: false };

// Предзагрузка ресурсов и кеш-брейкер
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

// Переключение вкладок
function switchTab(e, name) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active-tab'));
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active-nav'));
    document.getElementById(name).classList.add('active-tab');
    if(e) e.currentTarget.classList.add('active-nav');
    tg.HapticFeedback.impactOccurred('light');
}

// Обновление интерфейса
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

// Основные действия
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

// Очистка
function cleanPoo() {
    if (!state.hasPoo) return;
    state.hasPoo = false; 
    state.clean = 100;
    tg.HapticFeedback.notificationOccurred('success');
    updateUI();
}

// Игровой цикл
setInterval(() => {
    state.hunger = Math.max(0, state.hunger - 1);
    if (Math.random() > 0.90) state.hasPoo = true;
    if (state.hasPoo) state.clean = Math.max(0, state.clean - 2);
    updateUI();
}, 5000);
