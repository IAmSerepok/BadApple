const FPS = 30;
const FRAME_DELAY = 1000 / FPS;
const TOTAL_FRAMES = 6752;
const STEP = 30;

let currentFrame = 0;
let isPlaying = false;
let animationId = null;
let checkboxes = [];
let lastFrameTime = 0;

// Инициализация сетки чекбоксов
function initCheckboxGrid() {
    const grid = $('#checkbox-grid');
    grid.empty();
    
    const cols = Math.floor(960 / STEP);
    const rows = Math.floor(720 / STEP);
    
    // Создаем чекбоксы
    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            const checkbox = $('<input type="checkbox" class="pixel-checkbox">');
            grid.append(checkbox);
            checkboxes.push(checkbox[0]); // Сохраняем DOM-элемент
        }
        grid.append('<br>');
    }
}

// Обновление кадра
function updateFrame(data) {
    const colors = data.colors;
    const checkboxCount = checkboxes.length;
    
    // Быстрое обновление через прямой доступ к DOM
    for (let i = 0; i < checkboxCount; i++) {
        const y = Math.floor(i / data.cols);
        const x = i % data.cols;
        checkboxes[i].checked = colors[y][x][0] < 25;
    }
    
    $('#frameCounter').text(`Frame: ${currentFrame}`);
}

// Загрузка кадра
function loadFrame(frameIndex) {
    $.get(`/get_data/${frameIndex}`, function(data) {
        updateFrame(data);
        
        if (isPlaying) {
            currentFrame = (frameIndex + 1) % TOTAL_FRAMES;
            const now = performance.now();
            const elapsed = now - lastFrameTime;
            const delay = Math.max(0, FRAME_DELAY - elapsed);
            
            setTimeout(() => {
                lastFrameTime = performance.now();
                loadFrame(currentFrame);
            }, delay);
        }
    }).fail(() => {
        if (isPlaying) {
            currentFrame = (frameIndex + 1) % TOTAL_FRAMES;
            loadFrame(currentFrame);
        }
    });
}

// Управление воспроизведением
$('#playBtn').click(function() {
    if (!isPlaying) {
        isPlaying = true;
        lastFrameTime = performance.now();
        loadFrame(currentFrame);
    }
});

$('#stopBtn').click(function() {
    isPlaying = false;
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
});

// Инициализация при загрузке
$(document).ready(function() {
    initCheckboxGrid();
    loadFrame(0);
});