import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="픽셀 건물주 RPG", page_icon="🕹️", layout="centered")

st.title("🕹️ 픽셀 캐릭터 부동산 & 투자 RPG")
st.caption("방향키(W, A, S, D 또는 화살표)나 화면의 조이스틱 버튼으로 캐릭터를 움직여 건물에 접근해 보세요!")

# HTML5 Canvas + JS 기반 픽셀 RPG 게임 커스텀 컴포넌트
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        background-color: #1a1a2e;
        color: white;
        font-family: 'Courier New', Courier, monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    #gameContainer {
        position: relative;
        margin-top: 10px;
    }
    canvas {
        border: 4px solid #e94560;
        border-radius: 8px;
        background-color: #16213e;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
    }
    #uiBox {
        width: 480px;
        background-color: #0f3460;
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
        box-sizing: border-box;
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-weight: bold;
        color: #f1c40f;
    }
    .action-btn {
        background-color: #e94560;
        color: white;
        border: none;
        padding: 8px 12px;
        margin: 4px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
    }
    .action-btn:hover {
        background-color: #ff6b6b;
    }
    .controls {
        display: grid;
        grid-template-columns: repeat(3, 50px);
        gap: 5px;
        justify-content: center;
        margin-top: 10px;
    }
    .ctrl-btn {
        width: 50px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        background: #16213e;
        color: white;
        border: 2px solid #e94560;
        border-radius: 8px;
        cursor: pointer;
    }
    .ctrl-btn:active {
        background: #e94560;
    }
    #dialogue {
        min-height: 40px;
        background: #16213e;
        padding: 8px;
        border-radius: 4px;
        border: 1px solid #0f3460;
        margin-top: 5px;
        font-size: 13px;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas" width="480" height="360"></canvas>
</div>

<div id="uiBox">
    <div class="status-bar">
        <span>📅 턴: <span id="turnText">1</span> / 12</span>
        <span>💰 현금: <span id="moneyText">1,000,000</span>원</span>
    </div>
    <div id="dialogue">💬 건물에 가까이 가서 상호작용해 보세요! (은행/증권사/코인소/부동산)</div>
    <div id="actionArea" style="margin-top: 10px; text-align: center;"></div>
</div>

<!-- 모바일/클릭 조작용 조이스틱 버튼 -->
<div class="controls">
    <div></div>
    <button class="ctrl-btn" onclick="moveChar(0, -15)">▲</button>
    <div></div>
    <button class="ctrl-btn" onclick="moveChar(-15, 0)">◄</button>
    <button class="ctrl-btn" onclick="moveChar(0, 15)">▼</button>
    <button class="ctrl-btn" onclick="moveChar(15, 0)">►</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 게임 상태 변수
let money = 1000000;
let turn = 1;
let ownedBuildings = [];

// 캐릭터 상태
const player = {
    x: 220,
    y: 160,
    size: 24,
    color: '#00fff5',
    speed: 12,
    name: '김개미'
};

// 건물 데이터 (맵 상의 위치)
const buildings = [
    { id: 'bank', name: '🏦 안전 은행', x: 40, y: 30, w: 90, h: 70, color: '#2ecc71', type: 'bank' },
    { id: 'stock', name: '📈 미래 증권', x: 350, y: 30, w: 90, h: 70, color: '#3498db', type: 'stock' },
    { id: 'crypto', name: '🚀 코인 거래소', x: 40, y: 240, w: 90, h: 70, color: '#e74c3c', type: 'crypto' },
    { id: 'realty', name: '🏢 강남 부동산', x: 350, y: 240, w: 90, h: 70, color: '#f1c40f', type: 'realty' }
];

let nearBuilding = null;

// 키보드 조작 이벤트
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') moveChar(0, -player.speed);
    if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') moveChar(0, player.speed);
    if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') moveChar(-player.speed, 0);
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') moveChar(player.speed, 0);
});

function moveChar(dx, dy) {
    if (turn > 12 || money <= 0) return;
    
    player.x = Math.max(10, Math.min(canvas.width - player.size - 10, player.x + dx));
    player.y = Math.max(10, Math.min(canvas.height - player.size - 10, player.y + dy));
    
    checkProximity();
    drawMap();
}

// 건물 근접 체크
function checkProximity() {
    nearBuilding = null;
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');
    
    for (let b of buildings) {
        // 거리 계산
        let cx = b.x + b.w / 2;
        let cy = b.y + b.h / 2;
        let px = player.x + player.size / 2;
        let py = player.y + player.size / 2;
        let dist = Math.hypot(cx - px, cy - py);
        
        if (dist < 75) {
            nearBuilding = b;
            break;
        }
    }
    
    if (nearBuilding) {
        dialogue.innerHTML = `📍 <b>[${nearBuilding.name}]</b> 앞에 도착했습니다. 아래 메뉴를 선택하세요!`;
        renderActionButtons(nearBuilding.type);
    } else {
        dialogue.innerHTML = "💬 방향키나 버튼으로 캐릭터를 움직여 건물에 다가가세요!";
        actionArea.innerHTML = "";
    }
}

// 상호작용 버튼 생성
function renderActionButtons(type) {
    const actionArea = document.getElementById('actionArea');
    actionArea.innerHTML = "";
    
    if (type === 'bank') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investBank()">🏦 적금 넣기 (확정 +5%)</button>`;
    } else if (type === 'stock') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investStock()">📈 주식 매수 (50% 확률로 +30% / -20%)</button>`;
    } else if (type === 'crypto') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investCrypto()">🚀 코인 올인 (20% 확률로 +150% / -40%)</button>`;
    } else if (type === 'realty') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="buyBuilding('반지하 고시원', 10000000, 500000)">🏚️ 고시원 매수 (1,000만)</button>
            <button class="action-btn" onclick="buyBuilding('원룸 빌라', 30000000, 1500000)">🏠 빌라 매수 (3,000만)</button>
            <button class="action-btn" onclick="buyBuilding('강남 타워', 100000000, 10000000)">🏙️ 강남타워 매수 (1억 - 승리)</button>
        `;
    }
}

// 턴 및 월세 처리
function processTurn() {
    let rentSum = 0;
    ownedBuildings.forEach(b => rentSum += b.rent);
    money += rentSum;
    turn += 1;
    updateUI();
    
    if (money >= 100000000) {
        alert("🎉 축하합니다! 1억 원을 모아 건물주가 되었습니다!");
    } else if (turn > 12) {
        alert("⏱️ 12턴이 지났습니다! 최종 보유 자산: " + money.toLocaleString() + "원");
    } else if (money <= 0) {
        alert("💥 파산했습니다! 게임 오버!");
    }
}

// 투자 처리 함수들
function investBank() {
    let profit = Math.floor(money * 0.05);
    money += profit;
    alert(`🏦 적금 이자로 +${profit.toLocaleString()}원을 획득했습니다!`);
    processTurn();
}

function investStock() {
    if (Math.random() < 0.5) {
        let profit = Math.floor(money * 0.3);
        money += profit;
        alert(`📈 주식 떡상! +${profit.toLocaleString()}원 이득!`);
    } else {
        let loss = Math.floor(money * 0.2);
        money -= loss;
        alert(`📉 주식 떡락... -${loss.toLocaleString()}원 손실!`);
    }
    processTurn();
}

function investCrypto() {
    if (Math.random() < 0.2) {
        let profit = Math.floor(money * 1.5);
        money += profit;
        alert(`🚨 코인 대폭등! +${profit.toLocaleString()}원 초대박!`);
    } else {
        let loss = Math.floor(money * 0.4);
        money -= loss;
        alert(`📉 코인 폭락... -${loss.toLocaleString()}원 손실...`);
    }
    processTurn();
}

function buyBuilding(name, price, rent) {
    if (money < price) {
        alert("잔액이 부족합니다!");
        return;
    }
    money -= price;
    ownedBuildings.push({ name, rent });
    alert(`🎉 [${name}] 매수 성공! 매 턴 월세 +${rent.toLocaleString()}원이 들어옵니다.`);
    updateUI();
}

function updateUI() {
    document.getElementById('moneyText').innerText = money.toLocaleString();
    document.getElementById('turnText').innerText = turn;
}

// 2D 맵 및 캐릭터 그리기
function drawMap() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 격자 바닥 타일 표현
    ctx.strokeStyle = '#1a2639';
    for (let x = 0; x < canvas.width; x += 30) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 30) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }
    
    // 건물 그리기
    buildings.forEach(b => {
        ctx.fillStyle = b.color;
        ctx.fillRect(b.x, b.y, b.w, b.h);
        
        // 건물 지붕 스타일
        ctx.fillStyle = 'rgba(255,255,255,0.2)';
        ctx.fillRect(b.x, b.y, b.w, 15);
        
        // 건물 테두리
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.strokeRect(b.x, b.y, b.w, b.h);
        
        // 건물 이름 텍스트
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + b.w/2, b.y + b.h/2 + 4);
    });
    
    // 픽셀 스타일 캐릭터 그리기
    ctx.fillStyle = player.color;
    // 캐릭터 몸통
    ctx.fillRect(player.x, player.y, player.size, player.size);
    
    // 캐릭터 눈/얼굴 픽셀 표현
    ctx.fillStyle = '#000000';
    ctx.fillRect(player.x + 4, player.y + 6, 4, 4);
    ctx.fillRect(player.x + 16, player.y + 6, 4, 4);
    
    // 캐릭터 이름표 (상단 유저 이름)
    ctx.fillStyle = '#f1c40f';
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(player.name, player.x + player.size/2, player.y - 6);
}

// 최초 실행
drawMap();
checkProximity();
</script>
</body>
</html>
"""

# 스트림릿 화면에 HTML5 캔버스 내장
components.html(game_html, height=650)
