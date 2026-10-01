import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="김개미의 건물주 도전기", page_icon="🎮", layout="centered")

# 세션 상태 초기화
if "money" not in st.session_state:
    st.session_state.money = 1000000  # 초기 자금 100만 원
if "turn" not in st.session_state:
    st.session_state.turn = 1
if "history" not in st.session_state:
    st.session_state.history = []
if "status" not in st.session_state:
    st.session_state.status = "normal"  # normal, happy, sad, panic
if "dialogue" not in st.session_state:
    st.session_state.dialogue = "안녕! 난 갓 입사한 흙수저 김개미야. 12턴 안에 1억을 모아서 갓물주가 되는 게 내 꿈이지!"

# 캐릭터 이미지 URL (Unsplash 이미지 연동)
CHAR_IMAGES = {
    "normal": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&auto=format&fit=crop&q=80",  # 진지한 모습
    "happy": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&auto=format&fit=crop&q=80",   # 환하게 웃는 모습
    "sad": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&auto=format&fit=crop&q=80",     # 우울한 모습
    "panic": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&auto=format&fit=crop&q=80",   # 멘붕 온 모습
    "win": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&auto=format&fit=crop&q=80"     # 성공한 건물주
}

# 스토리 장(Chapter) 정보
def get_chapter_info(turn):
    if turn <= 3:
        return "CHAPTER 1: 흙수저 직장인의 첫 종잣돈 모으기"
    elif turn <= 6:
        return "CHAPTER 2: 잔혹한 주식 시장 입성"
    elif turn <= 9:
        return "CHAPTER 3: 24시간 잠들지 않는 코인 지옥"
    else:
        return "CHAPTER 4: 영끌 부동산과 최후의 승부"

# 타이틀 및 진행도
st.title("🏢 김개미의 1억 만들기 TRPG")
st.caption(get_chapter_info(st.session_state.turn))

# 턴 진행률 바
progress = min(st.session_state.turn / 12, 1.0)
st.progress(progress, text=f"목표 달성까지 남은 기회: {13 - st.session_state.turn}턴 / 12턴")

st.divider()

# --- 캐릭터 & 대사 화면 (RPG 대화창 스타일) ---
col_img, col_talk = st.columns([1, 2])

with col_img:
    img_url = CHAR_IMAGES.get(st.session_state.status, CHAR_IMAGES["normal"])
    st.image(img_url, caption="주인공 : 김개미 (28세)", use_container_width=True)

with col_talk:
    st.subheader("💬 김개미의 한마디")
    st.info(f'"{st.session_state.dialogue}"')
    
    # 상태 메트릭
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("📅 현재 턴", f"{st.session_state.turn} / 12 턴")
    m_col2.metric("💰 보유 자산", f"{st.session_state.money:,} 원")

st.divider()

# --- 게임 결과 조건 처리 ---
if st.session_state.money <= 0:
    st.error("💥 [GAME OVER] 통장 잔고가 0원이 되었습니다... 김개미는 다시 붕어빵 장사를 시작합니다.")
    st.session_state.status = "panic"
    if st.button("🔄 처음부터 다시 도전하기"):
        st.session_state.money = 1000000
        st.session_state.turn = 1
        st.session_state.status = "normal"
        st.session_state.dialogue = "좋아, 다시 시작해보자! 이번엔 진짜 건물주 간다!"
        st.session_state.history = []
        st.rerun()

elif st.session_state.money >= 100000000:
    st.balloons()
    st.success("🎉 [CLEAR] 1억 원 달성 성공! 김개미는 드디어 강남 건물주가 되었습니다!")
    st.session_state.status = "win"
    if st.button("🏆 새로운 전설 쓰기 (다시 시작)"):
        st.session_state.money = 1000000
        st.session_state.turn = 1
        st.session_state.status = "normal"
        st.session_state.dialogue = "건물주 한번 더 도전!"
        st.session_state.history = []
        st.rerun()

elif st.session_state.turn > 12:
    if st.session_state.money >= 50000000:
        st.warning("⏱️ [TIME OVER] 12턴이 끝났습니다! 건물주는 못 되었지만 중산층 진입에 성공했습니다.")
    else:
        st.error("⏱️ [TIME OVER] 12턴이 지났지만 1억을 모으지 못했습니다... 다음 기회를 노려보세요!")
    if st.button("🔄 다시 시작하기"):
        st.session_state.money = 1000000
        st.session_state.turn = 1
        st.session_state.status = "normal"
        st.session_state.dialogue = "이번엔 진짜 12턴 안에 1억 뚫는다!"
        st.session_state.history = []
        st.rerun()

else:
    # --- 투자 선택지 (게임 플레이 영역) ---
    st.subheader("🎯 이번 턴에 김개미는 어떤 선택을 할까?")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🏦 안전 적금")
        st.caption("확정 이자 +5%\n\n위험도: 없음")
        if st.button("적금 넣기"):
            profit = int(st.session_state.money * 0.05)
            st.session_state.money += profit
            st.session_state.status = "happy"
            st.session_state.dialogue = f"티끌 모아 태산이지! 소소하게 {profit:,}원 벌었어!"
            st.session_state.history.append(f"{st.session_state.turn}턴: 적금 +{profit:,}원")
            st.session_state.turn += 1
            st.rerun()
            
    with c2:
        st.markdown("### 📈 주식 투자")
        st.caption("50% 확률로 +30% OR -20%\n\n위험도: 보통")
        if st.button("주식 매수"):
            if random.random() < 0.5:
                profit = int(st.session_state.money * 0.3)
                st.session_state.money += profit
                st.session_state.status = "happy"
                st.session_state.dialogue = f"가즈아~! 주식 대박 터져서 +{profit:,}원 떡상했다!"
                st.session_state.history.append(f"{st.session_state.turn}턴: 주식 성공 +{profit:,}원")
            else:
                loss = int(st.session_state.money * 0.2)
                st.session_state.money -= loss
                st.session_state.status = "sad"
                st.session_state.dialogue = f"아... 파란불 등장했네... -{loss:,}원 손실이야..."
                st.session_state.history.append(f"{st.session_state.turn}턴: 주식 실패 -{loss:,}원")
            st.session_state.turn += 1
            st.rerun()

    with c3:
        st.markdown("### 🚀 코인 올인")
        st.caption("20% 확률로 +150% OR 80% 확률로 -40%\n\n위험도: 극상")
        if st.button("코인 올인"):
            if random.random() < 0.2:
                profit = int(st.session_state.money * 1.5)
                st.session_state.money += profit
                st.session_state.status = "happy"
                st.session_state.dialogue = f"🚨 화성 갈뻔했다!! 코인 초대박으로 +{profit:,}원 연쇄 상승!"
                st.session_state.history.append(f"{st.session_state.turn}턴: 코인 초대박 +{profit:,}원")
            else:
                loss = int(st.session_state.money * 0.4)
                st.session_state.money -= loss
                st.session_state.status = "panic"
                st.session_state.dialogue = f"경고! 떡락장에 물렸다... -{loss:,}원 증발... 실화냐?"
                st.session_state.history.append(f"{st.session_state.turn}턴: 코인 떡락 -{loss:,}원")
            st.session_state.turn += 1
            st.rerun()

st.divider()

# --- 지난 기록 (로그) ---
with st.expander("📜 김개미의 지난 모험 기록 보기"):
    for log in reversed(st.session_state.history):
        st.write(log)
