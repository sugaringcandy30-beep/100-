import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="wide")

st.title("🏙️ 모던 벡터 시티 & 투자 RPG")
st.caption("방향키(A, D)로 이동, Space키로 점프! 미니게임을 진행할수록 점점 어려워지는 하이퍼 난이도 시스템!")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');

    body {
        margin: 0;
        padding: 0;
        background-color: #0b0f19;
        color: #f8fafc;
        font-family: 'Pretendard', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    #newsTickerBox {
        width: 840px;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        color: #38bdf8;
        font-size: 14px;
        font-weight: 600;
        padding: 12px 20px;
        border-radius: 16px 16px 0 0;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-bottom: none;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    #newsTag {
        background: linear-gradient(135deg, #f43f5e, #e11d48);
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    #newsText {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    #gameContainer {
        position: relative;
    }
    canvas {
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 0 0 16px 16px;
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }
    #uiBox {
        width: 840px;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 16px;
        margin-top: 14px;
        box-sizing: border-box;
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
        font-weight: 600;
        color: #e2e8f0;
        font-size: 15px;
    }
    #progressContainer {
        width: 100%;
        height: 22px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 11px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 14px;
    }
    #progressBar {
        width: 1%;
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #10b981);
        transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 10px;
    }
    #progressText {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        font-size: 12px;
        text-align: center;
        line-height: 22px;
        color: white;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.6);
    }
    .action-btn {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        padding: 11px 20px;
        margin: 4px;
        border-radius: 10px;
        cursor: pointer;
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
        transition: all 0.2s ease;
    }
    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.6);
    }
    .enter-btn {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        padding: 12px 26px;
        border-radius: 10px;
        cursor: pointer;
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
    }
    .exit-btn {
        background: linear-gradient(135deg, #f43f5e, #e11d48);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-family: 'Pretendard', sans-serif;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 4px 14px rgba(244, 63, 94, 0.4);
    }
    .controls {
        display: grid;
        grid-template-columns: repeat(4, 90px);
        gap: 12px;
        justify-content: center;
        margin-top: 16px;
    }
    .ctrl-btn {
        width: 90px;
        height: 56px;
        font-size: 16px;
        font-weight: 600;
        font-family: 'Pretendard', sans-serif;
        background: rgba(30, 41, 59, 0.9);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.1s ease;
    }
    .ctrl-btn:active {
        transform: translateY(2px);
        background: rgba(56, 189, 248, 0.2);
    }
    #dialogue {
        min-height: 52px;
        background: rgba(15, 23, 42, 0.6);
        padding: 14px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.15);
        margin-top: 8px;
        font-size: 15px;
        line-height: 1.6;
        color: #cbd5e1;
    }
    #minigameBox {
        display: none;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(245, 158, 11, 0.5);
        border-radius: 12px;
        padding: 18px;
        margin-top: 12px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    #meterBar {
        width: 100%;
        height: 28px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 14px;
        position: relative;
        overflow: hidden;
        margin: 14px 0;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    #meterIndicator {
        width: 18px;
        height: 100%;
        background: #f43f5e;
        position: absolute;
        left: 0;
        border-radius: 8px;
        box-shadow: 0 0 10px #f43f5e;
    }
    #targetZone {
        width: 110px;
        height: 100%;
        background: rgba(16, 185, 129, 0.7);
        position: absolute;
        left: 330px;
        border-radius: 6px;
    }
</style>
</head>
<body>

<div id="newsTickerBox">
    <span id="newsTag">속보</span>
    <span id="newsText">모던 벡터 시티 금융 시장이 개장했습니다. 미니게임 난이도는 플레이할수록 상승합니다!</span>
</div>

<div id="gameContainer">
    <canvas id="gameCanvas" width="840" height="480"></canvas>
</div>

<div id="uiBox">
    <div class="status-bar">
        <span>📍 위치: <span id="locationText" style="color: #38bdf8;">메인 스트리트</span></span>
        <span>🔥 난이도 Lv.<span id="diffLevelText" style="color: #f43f5e;">1</span></span>
        <span>📅 턴: <span id="turnText">1</span>/12</span>
        <span>💰 자산: <span id="moneyText" style="color: #10b981;">1,000,000</span>원</span>
    </div>

    <div id="progressContainer">
        <div id="progressBar"></div>
        <div id="progressText">1억 원 목표 달성도: 1%</div>
    </div>

    <div id="dialogue">💬 방향키로 세련된 벡터 빌딩들을 탐험하고 입구 포탈[▲ / W]로 입장해보세요.</div>
    
    <div id="minigameBox">
        <div id="minigameTitle" style="color:#fbbf24; font-weight:700; font-size: 16px;">🎯 타이밍 게이지 미니게임</div>
        <div id="meterBar">
            <div id="targetZone"></div>
            <div id="meterIndicator"></div>
        </div>
        <button class="action-btn" style="background: linear-gradient(135deg, #f43f5e, #e11d48);" onclick="stopMeter()">🎯 STOP (타이밍 맞추기)</button>
    </div>

    <div id="actionArea" style="margin-top: 10px; text-align: center;"></div>
</div>

<div class="controls">
    <button class="ctrl-btn" onclick="moveLeft()">◄ 이동</button>
    <button class="ctrl-btn" onclick="jump()">▲ 점프</button>
    <button class="ctrl-btn" onclick="moveRight()">이동 ►</button>
    <button class="ctrl-btn" style="color: #10b981; border-color: rgba(16, 185, 129, 0.4);" onclick="interactPortal()">▲ 포탈</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let money = 1000000;
let turn = 1;
let currentScene = 'town';
let ownedBuildings = [];
const goalMoney = 100000000;

// 미니게임 누적 플레이 횟수 및 난이도 계수
let miniGameCount = 0;

let floatingTexts = [];

let currentNews = { text: "시티 금융 시장이 개장했습니다.", stockMod: 0, cryptoMod: 0 };
const newsEvents = [
    { text: "🔥 [속보] 혁신 기술 기업 대형 호재 발생! 주식 시장 강세!", stockMod: 0.4, cryptoMod: 0 },
    { text: "📉 [속보] 글로벌 자산 규제 강화 발표! 코인 시장 위축 주의!", stockMod: 0, cryptoMod: -0.3 },
    { text: "🚀 [속보] 중앙은행 대규모 유동성 공급! 전 시장 동반 폭등!", stockMod: 0.25, cryptoMod: 0.3 },
    { text: "⚠️ [속보] 금리 인상 이슈 대두! 투자 심리 경계감 확산!", stockMod: -0.2, cryptoMod: -0.2 }
];

const player = {
    x: 120,
    y: 320,
    vx: 0,
    vy: 0,
    speed: 7,
    jumpPower: -13,
    groundY: 320,
    isGrounded: true,
    facing: 'right',
    animFrame: 0,
    name: '투자자'
};

const buildings = [
    { id: 'bank', name: '🏦 네오 중앙은행', x: 120, portalX: 220, colorMain: '#1e293b', accent: '#10b981' },
    { id: 'stock', name: '📈 메트로 증권타워', x: 500, portalX: 600, colorMain: '#1e293b', accent: '#3b82f6' },
    { id: 'crypto', name: '🚀 사이버 코인랩', x: 880, portalX: 980, colorMain: '#1e293b', accent: '#f43f5e' },
    { id: 'realty', name: '🏢 스카이 부동산', x: 1260, portalX: 1360, colorMain: '#1e293b', accent: '#fbbf24' }
];

const interiorNPCs = {
    bank: { x: 420, y: 290, name: '🏦 은행 딜러 김수호' },
    stock: { x: 420, y: 290, name: '📈 펀드매니저 박차트' },
    crypto: { x: 420, y: 290, name: '🚀 코인 애널리스트 나대박' },
    realty: { x: 420, y: 290, name: '🏢 부동산 디벨로퍼 최건물' }
};

let cameraX = 0;
let portalAnim = 0;
let keys = {};

let meterPos = 0;
let baseMeterSpeed = 6;
let meterSpeed = 6;
let meterActive = false;
let meterAnimId = null;

let lastProximityKey = null;

document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    if ((e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') && currentScene === 'town') {
        interactPortal();
    }
    if ((e.key === ' ' || e.key === 'Spacebar') && player.isGrounded) {
        jump();
    }
});
document.addEventListener('keyup', (e) => { keys[e.key] = false; });

function moveLeft() { player.vx = -player.speed; player.facing = 'left'; }
function moveRight() { player.vx = player.speed; player.facing = 'right'; }
function jump() {
    if (player.isGrounded) {
        player.vy = player.jumpPower;
        player.isGrounded = false;
    }
}

function addFloatingText(amount) {
    let text = amount >= 0 ? `+${amount.toLocaleString()}원` : `-${Math.abs(amount).toLocaleString()}원`;
    let color = amount >= 0 ? '#10b981' : '#f43f5e';
    floatingTexts.push({
        x: player.x,
        y: player.y - 60,
        text: text,
        color: color,
        opacity: 1.0,
        vy: -1.5
    });
}

function interactPortal() {
    if (currentScene === 'town') {
        for (let b of buildings) {
            if (Math.abs(player.x - b.portalX) < 55) {
                enterBuilding(b.id);
                return;
            }
        }
    }
}

function enterBuilding(bId) {
    currentScene = bId;
    player.x = 120;
    player.y = 320;
    lastProximityKey = null;
    const bObj = buildings.find(b => b.id === bId);
    document.getElementById('locationText').innerText = bObj.name;
    checkProximity();
}

function exitBuilding() {
    let bObj = buildings.find(b => b.id === currentScene);
    currentScene = 'town';
    player.x = bObj.portalX;
    player.y = 320;
    lastProximityKey = null;
    document.getElementById('locationText').innerText = '메인 스트리트';
    document.getElementById('minigameBox').style.display = 'none';
    meterActive = false;
    checkProximity();
}

function checkProximity() {
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');

    if (currentScene === 'town') {
        let nearB = buildings.find(b => Math.abs(player.x - b.portalX) < 55);
        let stateKey = nearB ? 'town_' + nearB.id : 'town_none';

        if (lastProximityKey !== stateKey) {
            lastProximityKey = stateKey;
            if (nearB) {
                dialogue.innerHTML = `✨ <b>[${nearB.name}] 입구입니다!</b> [▲ / W]키나 아래 버튼으로 입장하세요!`;
                actionArea.innerHTML = `<button class="enter-btn" onclick="enterBuilding('${nearB.id}')">🚪 건물 입장하기</button>`;
            } else {
                dialogue.innerHTML = "💬 방향키로 세련된 벡터 빌딩들을 탐험하고 입구 포탈로 들어가보세요!";
                actionArea.innerHTML = "";
            }
        }
    } else {
        let npc = interiorNPCs[currentScene];
        let dist = Math.abs(player.x - npc.x);
        let zone = player.x < 70 ? 'exit' : (dist < 100 ? 'npc' : 'walk');
        let stateKey = currentScene + '_' + zone;

        if (lastProximityKey !== stateKey) {
            lastProximityKey = stateKey;
            if (zone === 'exit') {
                dialogue.innerHTML = "🚪 메인 스트리트로 나가는 출구입니다.";
                actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
            } else if (zone === 'npc') {
                let currentLevel = miniGameCount + 1;
                dialogue.innerHTML = `💬 <b>${npc.name}</b>: "어서오세요! (현재 난이도 Lv.${currentLevel}) 아래 버튼을 눌러 도전하세요."`;
                renderDialogueOptions(currentScene);
            } else {
                dialogue.innerHTML = `🏢 컨설팅 데스크로 가까이 다가가세요.`;
                actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
            }
        }
    }
}

function renderDialogueOptions(type) {
    const actionArea = document.getElementById('actionArea');
    if (type === 'bank') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investBank()">🏦 예금 가입 (+5% 확정)</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'stock') {
        actionArea.innerHTML = `<button class="action-btn" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8);" onclick="startStockMiniGame()">🎮 [미니게임] 주식 매수 타이밍 도전</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'crypto') {
        actionArea.innerHTML = `<button class="action-btn" style="background: linear-gradient(135deg, #f43f5e, #e11d48);" onclick="startCryptoMiniGame()">🎮 [미니게임] 코인 폭발 타이밍 도전</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'realty') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="buyBuilding('초역세권 오피스텔', 30000000, 2000000)">🏠 오피스텔 (3천만)</button>
            <button class="action-btn" onclick="buyBuilding('테헤란로 빌딩', 60000000, 5000000)">🏢 빌딩 (6천만)</button>
            <button class="action-btn" onclick="buyBuilding('강남 타워', 100000000, 12000000)">🏙️ 강남타워 (1억)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        `;
    }
}

function startStockMiniGame() {
    document.getElementById('actionArea').innerHTML = '';
    document.getElementById('minigameBox').style.display = 'block';
    
    // 난이도 반영: 미니게임을 할수록 속도가 빨라지고 타겟 영역이 좁아짐 (최소 폭 40px까지 축소)
    let speedBonus = miniGameCount * 1.5;
    let targetWidth = Math.max(40, 110 - (miniGameCount * 12));
    
    document.getElementById('targetZone').style.width = targetWidth + 'px';
    document.getElementById('minigameTitle').innerText = `📈 [주식 미니게임 Lv.${miniGameCount + 1}] 초록 영역 적중 시 성공!`;
    
    meterPos = 0;
    meterSpeed = 7 + speedBonus;
    meterActive = true;
    updateMeter();
}

function startCryptoMiniGame() {
    document.getElementById('actionArea').innerHTML = '';
    document.getElementById('minigameBox').style.display = 'block';
    
    let speedBonus = miniGameCount * 2.2;
    let targetWidth = Math.max(35, 100 - (miniGameCount * 14));
    
    document.getElementById('targetZone').style.width = targetWidth + 'px';
    document.getElementById('minigameTitle').innerText = `🚀 [코인 미니게임 Lv.${miniGameCount + 1}] 고속 게이지 폭등 도전!`;
    
    meterPos = 0;
    meterSpeed = 12 + speedBonus;
    meterActive = true;
    updateMeter();
}

function updateMeter() {
    if (!meterActive) return;
    meterPos += meterSpeed;
    if (meterPos > 780 || meterPos < 0) meterSpeed *= -1;
    document.getElementById('meterIndicator').style.left = meterPos + 'px';
    meterAnimId = requestAnimationFrame(updateMeter);
}

function stopMeter() {
    meterActive = false;
    cancelAnimationFrame(meterAnimId);
    document.getElementById('minigameBox').style.display = 'none';

    // 현재 설정된 타겟 영역의 위치와 너비를 기준으로 판정
    let targetZoneEl = document.getElementById('targetZone');
    let targetLeft = parseFloat(targetZoneEl.style.left) || 330;
    let targetWidth = parseFloat(targetZoneEl.style.width) || 110;
    let indicatorPos = meterPos + 9; // 인디케이터 중심점 보정

    let success = indicatorPos >= targetLeft && indicatorPos <= (targetLeft + targetWidth);
    
    if (currentScene === 'stock') {
        let winProb = 0.5 + currentNews.stockMod;
        if (success || Math.random() < winProb) {
            let profit = Math.floor(money * 0.4);
            money += profit;
            addFloatingText(profit);
            alert(`🎉 [주식 대성공 (Lv.${miniGameCount + 1})] 타이밍 적중! +${profit.toLocaleString()}원 수익!`);
        } else {
            let loss = Math.floor(money * 0.2);
            money -= loss;
            addFloatingText(-loss);
            alert(`📉 [주식 손실] 타이밍 실패... -${loss.toLocaleString()}원`);
        }
    } else if (currentScene === 'crypto') {
        if (success) {
            let profit = Math.floor(money * 2.0);
            money += profit;
            addFloatingText(profit);
            alert(`🚀 [코인 초대박 (Lv.${miniGameCount + 1})] 초록 타겟 정확히 저격! +${profit.toLocaleString()}원 폭등!!`);
        } else {
            let loss = Math.floor(money * 0.5);
            money -= loss;
            addFloatingText(-loss);
            alert(`💥 [코인 청산] 타이밍 실패로 -${loss.toLocaleString()}원 손실...`);
        }
    }

    // 미니게임 완료 후 난이도 단계 상승
    miniGameCount += 1;
    document.getElementById('diffLevelText').innerText = miniGameCount + 1;

    processTurn();
}

function processTurn() {
    let rentSum = 0;
    ownedBuildings.forEach(b => rentSum += b.rent);
    if (rentSum > 0) {
        money += rentSum;
        addFloatingText(rentSum);
    }
    turn += 1;
    
    if (Math.random() < 0.75) {
        currentNews = newsEvents[Math.floor(Math.random() * newsEvents.length)];
    } else {
        currentNews = { text: "시티 금융 시장이 안정세를 유지하고 있습니다.", stockMod: 0, cryptoMod: 0 };
    }
    document.getElementById('newsText').innerText = currentNews.text;

    updateUI();
    lastProximityKey = null;

    if (money >= goalMoney) alert("🎉 1억 원 달성! 강남 건물주가 되었습니다!");
    else if (turn > 12) alert("⏱ 12턴 종료! 최종 자산: " + money.toLocaleString() + "원");
    else if (money <= 0) alert("💥 파산했습니다!");
}

function investBank() {
    let interest = Math.floor(money * 0.05);
    money += interest;
    addFloatingText(interest);
    alert("🏦 예금 이자가 입금되었습니다!");
    processTurn();
}

function buyBuilding(name, price, rent) {
    if (money < price) { alert("자산이 부족합니다!"); return; }
    money -= price;
    addFloatingText(-price);
    ownedBuildings.push({ name, rent });
    alert(`🎉 [${name}] 매수 성공! 매 턴 월세가 들어옵니다.`);
    updateUI();
}

function updateUI() {
    document.getElementById('moneyText').innerText = money.toLocaleString();
    document.getElementById('turnText').innerText = turn;

    const skinText = document.getElementById('skinText');
    if (money >= 50000000) {
        skinText.innerText = "👑 골드 건물주";
        skinText.style.color = "#fbbf24";
    } else if (money >= 20000000) {
        skinText.innerText = "💼 명품 트레이더";
        skinText.style.color = "#a855f7";
    } else {
        skinText.innerText = "👔 초보 개미";
        skinText.style.color = "#38bdf8";
    }

    let percent = Math.min(100, Math.max(1, Math.floor((money / goalMoney) * 100)));
    document.getElementById('progressBar').style.width = percent + '%';
    document.getElementById('progressText').innerText = `1억 원 목표 달성도: ${percent}% (${money.toLocaleString()}원 / 100,000,000원)`;
}

function update() {
    if (keys['ArrowLeft'] || keys['a'] || keys['A']) { player.vx = -player.speed; player.facing = 'left'; }
    else if (keys['ArrowRight'] || keys['d'] || keys['D']) { player.vx = player.speed; player.facing = 'right'; }
    else { player.vx *= 0.6; }

    player.x += player.vx;
    player.vy += 0.65;
    player.y += player.vy;

    if (player.y >= player.groundY) {
        player.y = player.groundY;
        player.vy = 0;
        player.isGrounded = true;
    }

    if (currentScene === 'town') {
        player.x = Math.max(20, Math.min(1580, player.x));
        cameraX = player.x - canvas.width / 2;
        cameraX = Math.max(0, Math.min(1600 - canvas.width, cameraX));
    } else {
        player.x = Math.max(20, Math.min(820, player.x));
        cameraX = 0;
    }

    portalAnim += 0.08;
    player.animFrame += 0.15;

    checkProximity();
    draw();
    requestAnimationFrame(update);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(-cameraX, 0);

    if (currentScene === 'town') drawTown();
    else drawInterior();

    drawVectorPlayer(player.x, player.y, player.facing);
    drawFloatingTexts();

    ctx.restore();
}

function drawTown() {
    let skyGradient = ctx.createLinearGradient(0, 0, 0, 260);
    skyGradient.addColorStop(0, '#090d16');
    skyGradient.addColorStop(1, '#1e293b');
    ctx.fillStyle = skyGradient;
    ctx.fillRect(cameraX, 0, canvas.width, 260);

    ctx.fillStyle = 'rgba(30, 41, 59, 0.4)';
    ctx.fillRect(cameraX + 50, 100, 90, 160);
    ctx.fillRect(cameraX + 300, 70, 110, 190);
    ctx.fillRect(cameraX + 700, 80, 100, 180);
    ctx.fillRect(cameraX + 1100, 50, 130, 210);

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 360, 1600, 120);
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, 360, 1600, 6);

    buildings.forEach(b => {
        ctx.fillStyle = b.colorMain;
        ctx.fillRect(b.x, 110, 200, 250);

        for (let wx = b.x + 20; wx < b.x + 180; wx += 40) {
            for (let wy = 140; wy < 320; wy += 45) {
                ctx.fillStyle = 'rgba(56, 189, 248, 0.15)';
                ctx.fillRect(wx, wy, 22, 28);
                ctx.fillStyle = 'rgba(251, 191, 36, 0.8)';
                ctx.fillRect(wx + 4, wy + 4, 14, 20);
            }
        }

        ctx.fillStyle = b.accent;
        ctx.fillRect(b.x, 80, 200, 32);
        ctx.fillStyle = '#ffffff';
        ctx.font = '600 15px Pretendard, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + 100, 101);

        let px = b.portalX;
        let py = 320;
        let scale = Math.sin(portalAnim) * 6;
        
        ctx.save();
        ctx.strokeStyle = b.accent;
        ctx.lineWidth = 4;
        ctx.shadowColor = b.accent;
        ctx.shadowBlur = 15;
        ctx.beginPath();
        ctx.ellipse(px, py, 22 + scale, 40 + scale, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.fillStyle = b.accent;
        ctx.globalAlpha = 0.25;
        ctx.fill();
        ctx.restore();
    });
}

function drawInterior() {
    let bObj = buildings.find(b => b.id === currentScene);
    let npc = interiorNPCs[currentScene];

    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, 840, 480);
    
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, 840, 90);

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 360, 840, 120);

    ctx.fillStyle = '#334155';
    ctx.fillRect(340, 300, 160, 60);
    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(340, 350, 160, 10);

    ctx.save();
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 4;
    ctx.shadowColor = '#f43f5e';
    ctx.shadowBlur = 15;
    ctx.beginPath();
    ctx.ellipse(40, 320, 18, 36, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();

    drawVectorNPC(npc.x, npc.y, npc.name);
}

function drawVectorPlayer(x, y, facing) {
    let bounce = Math.sin(player.animFrame) * 2;
    if (!player.isGrounded) bounce = -6;

    if (money >= 50000000) {
        ctx.save();
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#fbbf24';
        ctx.shadowBlur = 18;
        ctx.beginPath();
        ctx.arc(x, y - 18 + bounce, 32, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }

    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    ctx.roundRect(x - 14, y - 42 + bounce, 28, 48, [10]);
    ctx.fill();

    ctx.fillStyle = '#fce7f3';
    ctx.beginPath();
    ctx.roundRect(x - 10, y - 30 + bounce, 20, 16, [6]);
    ctx.fill();

    if (money >= 50000000) {
        ctx.fillStyle = '#fbbf24';
        ctx.fillRect(x - 12, y - 38 + bounce, 24, 10);
        ctx.fillStyle = '#fbbf24';
        ctx.fillRect(x - 2, y - 14 + bounce, 4, 16);
    } else if (money >= 20000000) {
        ctx.fillStyle = '#a855f7';
        ctx.fillRect(x - 12, y - 38 + bounce, 24, 10);
        ctx.fillStyle = '#e2e8f0';
        ctx.fillRect(x - 2, y - 14 + bounce, 4, 16);
    } else {
        ctx.fillStyle = '#3b82f6';
        ctx.fillRect(x - 12, y - 38 + bounce, 24, 10);
        ctx.fillStyle = '#38bdf8';
        if (facing === 'right') {
            ctx.fillRect(x + 2, y - 14 + bounce, 6, 16);
        } else {
            ctx.fillRect(x - 8, y - 14 + bounce, 6, 16);
        }
    }

    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.beginPath();
    ctx.roundRect(x - 45, y - 62 + bounce, 90, 20, [6]);
    ctx.fill();
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)';
    ctx.stroke();

    ctx.fillStyle = money >= 50000000 ? '#fbbf24' : '#38bdf8';
    ctx.font = '600 12px Pretendard, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(player.name, x, y - 48 + bounce);
}

function drawFloatingTexts() {
    for (let i = floatingTexts.length - 1; i >= 0; i--) {
        let ft = floatingTexts[i];
        ft.y += ft.vy;
        ft.opacity -= 0.02;

        if (ft.opacity <= 0) {
            floatingTexts.splice(i, 1);
            continue;
        }

        ctx.save();
        ctx.globalAlpha = Math.max(0, ft.opacity);
        ctx.fillStyle = ft.color;
        ctx.font = '700 16px Pretendard, sans-serif';
        ctx.textAlign = 'center';
        ctx.shadowColor = '#000000';
        ctx.shadowBlur = 6;
        ctx.fillText(ft.text, ft.x, ft.y);
        ctx.restore();
    }
}

function drawVectorNPC(x, y, name) {
    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    ctx.roundRect(x - 14, y - 42, 28, 48, [10]);
    ctx.fill();

    ctx.fillStyle = '#fce7f3';
    ctx.beginPath();
    ctx.roundRect(x - 10, y - 30, 20, 16, [6]);
    ctx.fill();

    ctx.fillStyle = '#10b981';
    ctx.fillRect(x - 12, y - 38, 24, 10);

    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.beginPath();
    ctx.roundRect(x - 55, y - 62, 110, 20, [6]);
    ctx.fill();
    ctx.strokeStyle = 'rgba(16, 185, 129, 0.3)';
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = '600 12px Pretendard, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x, y - 48);
}

requestAnimationFrame(update);
</script>
</body>
</html>
"""

components.html(game_html, height=920)
