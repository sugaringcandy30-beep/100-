import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="centered")

st.title("🏙️ 모던 픽셀 비치 & 투자 RPG")
st.caption("방향키(A, D)로 이동, Space키로 점프! 웅장해진 건물 입구 포탈[▲ / W]로 입장하세요.")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=NeoDunggeunmo&display=swap');

    body {
        margin: 0;
        padding: 0;
        background-color: #0d111a;
        color: white;
        font-family: 'NeoDunggeunmo', 'Courier New', monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    #newsTicker {
        width: 600px;
        background: #181f2c;
        color: #f1c40f;
        font-size: 14px;
        font-weight: bold;
        padding: 10px 16px;
        border-radius: 12px 12px 0 0;
        border: 2px solid #3d5af1;
        border-bottom: none;
        box-sizing: border-box;
        overflow: hidden;
        white-space: nowrap;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.5);
    }
    #gameContainer {
        position: relative;
    }
    canvas {
        border: 2px solid #3d5af
