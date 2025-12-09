"""

MIT License

Copyright (c) 2025 SRINJOY DAS 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import streamlit as st
import random
import time

# ---------------- COLORS ----------------
BG = "#070616"
NEON_X = "#1cd8ff"
NEON_O = "#ff4d6d"
NEON_ACCENT = "#7c5cff"
TEXT_FAINT = "#C8D0E0"

EMPTY = " "
HUMAN = "X"
AI = "O"

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# ---------------- RESPONSIVE CSS ----------------
st.markdown(f"""
<style>
html, body, .stApp {{
    background: {BG};
    color: {TEXT_FAINT};
}}

.title {{
    font-size: 42px;
    color: {NEON_X};
    text-align: center;
    font-weight: 700;
    margin-bottom: 15px;
}}

.cell {{
    width: 100%;
    height: 110px;
    border-radius: 14px;
    background: #0c0b20;
    border: 2px solid {NEON_ACCENT};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
    cursor: pointer;
    user-select: none;
    transition: 0.15s;
    box-shadow: 0 0 18px rgba(124, 92, 255, 0.23);
}}

.cell:hover {{
    transform: scale(1.06);
    box-shadow: 0 0 25px rgba(124, 92, 255, 0.40);
}}

.xsym {{
    color: {NEON_X};
    text-shadow: 0 0 12px {NEON_X};
}}

.osym {{
    color: {NEON_O};
    text-shadow: 0 0 12px {NEON_O};
}}

.resetbutton .stButton>button {{
    background: {NEON_ACCENT};
    border-radius: 10px;
    color: black;
    padding: 10px 22px;
    font-weight: bold;
    box-shadow: 0 0 15px {NEON_ACCENT};
}}

.scoreboard {{
    display: flex;
    justify-content: space-around;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 15px;
}}

/* ---------- MOBILE RESPONSIVE ---------- */
@media (max-width: 600px) {{
    .title {{
        font-size: 30px;
    }}

    .cell {{
        height: 80px;
        font-size: 36px;
        border-radius: 10px;
    }}

    .scoreboard {{
        font-size: 16px;
    }}

    .resetbutton .stButton>button {{
        padding: 8px 15px;
        font-size: 14px;
    }}

    .stSelectbox label {{
        font-size: 15px !important;
    }}
}}

/* EXTRA SMALL DEVICES (very small phones) */
@media (max-width: 380px) {{
    .cell {{
        height: 65px;
        font-size: 30px;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "board" not in st.session_state:
    st.session_state.board = [[EMPTY]*3 for _ in range(3)]
if "turn" not in st.session_state:
    st.session_state.turn = HUMAN
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Impossible"
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "first_move" not in st.session_state:
    st.session_state.first_move = "Human"
if "score" not in st.session_state:
    st.session_state.score = {"Human":0, "AI":0, "Tie":0}

# ---------------- Winner check ----------------
def check_winner(board):
    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2]!=EMPTY:
            return board[i][0]
        if board[0][i]==board[1][i]==board[2][i]!=EMPTY:
            return board[0][i]
    if board[0][0]==board[1][1]==board[2][2]!=EMPTY:
        return board[0][0]
    if board[0][2]==board[1][1]==board[2][0]!=EMPTY:
        return board[0][2]
    if all(board[r][c]!=EMPTY for r in range(3) for c in range(3)):
        return "Tie"
    return None

# ---------------- Minimax AI ----------------
def minimax(board, depth, is_max):
    winner = check_winner(board)
    if winner == AI: return 10 - depth, None
    if winner == HUMAN: return depth - 10, None
    if winner == "Tie": return 0, None

    if is_max:
        best = -999; mv = None
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = AI
                    val,_ = minimax(board, depth+1, False)
                    board[r][c] = EMPTY
                    if val > best: best = val; mv = (r,c)
        return best, mv
    else:
        best = 999; mv = None
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = HUMAN
                    val,_ = minimax(board, depth+1, True)
                    board[r][c] = EMPTY
                    if val < best: best = val; mv = (r,c)
        return best, mv

def ai_pick_move():
    board = st.session_state.board
    empty = [(r,c) for r in range(3) for c in range(3) if board[r][c]==EMPTY]
    diff = st.session_state.difficulty

    if diff == "Easy": return random.choice(empty)
    if diff == "Medium" and random.random() < 0.5: return random.choice(empty)
    if diff == "Hard" and random.random() < 0.18: return random.choice(empty)

    _, mv = minimax([row[:] for row in board], 0, True)
    return mv or random.choice(empty)

# ---------------- UI HEADER ----------------
st.markdown("<div class='title'>TIC TAC TOE</div>", unsafe_allow_html=True)
st.markdown("Play Tic Tac Toe against an AI or a friend!")
st.markdown("Please turn on dextop mode for better experence in mobiles and tablet!! ")

# ---------------- Game Settings ----------------
mode = st.selectbox("Mode", ["Player vs AI", "Player vs Player"])
if mode=="Player vs AI":
    st.session_state.difficulty = st.selectbox("Difficulty", ["Easy","Medium","Hard","Impossible"])
    st.session_state.first_move = st.selectbox("Who moves first?", ["Human", "AI"])
else:
    st.session_state.first_move = st.selectbox("Who moves first?", ["Player 1", "Player 2"])

# ---------------- Scoreboard ----------------
score = st.session_state.score
st.markdown(f"""
<div class='scoreboard'>
    <div>👤 Player 1: {score['Human']}</div>
    <div>🤖 Player 2/AI: {score['AI']}</div>
    <div>🤝 Ties: {score['Tie']}</div>
</div>
""", unsafe_allow_html=True)

# ---------------- Set Turn ----------------
if st.session_state.game_over == False and all(cell==EMPTY for row in st.session_state.board for cell in row):
    if mode == "Player vs AI":
        st.session_state.turn = HUMAN if st.session_state.first_move=="Human" else AI
    else:
        st.session_state.turn = "Player 1" if st.session_state.first_move=="Player 1" else "Player 2"

# ---------------- Board UI ----------------
for r in range(3):
    cols = st.columns([1,1,1], gap="small")
    for c in range(3):
        cell = st.session_state.board[r][c]
        clickable = False

        if mode == "Player vs AI":
            clickable = (not st.session_state.game_over and cell==EMPTY and st.session_state.turn==HUMAN)
        else:
            clickable = (not st.session_state.game_over and cell==EMPTY)

        with cols[c]:
            if cell == HUMAN or cell=="X":
                display_html = "<div class='cell'><span class='xsym'>X</span></div>"
            elif cell == AI or cell=="O":
                display_html = "<div class='cell'><span class='osym'>O</span></div>"
            else:
                display_html = "<div class='cell'></div>"

            st.markdown(display_html, unsafe_allow_html=True)

            if clickable:
                if st.button(" ", key=f"{r}{c}"):
                    if mode == "Player vs AI":
                        st.session_state.board[r][c] = HUMAN
                        st.session_state.turn = AI
                    else:
                        st.session_state.board[r][c] = "X" if st.session_state.turn=="Player 1" else "O"
                        st.session_state.turn = "Player 2" if st.session_state.turn=="Player 1" else "Player 1"

                    w = check_winner(st.session_state.board)
                    if w:
                        st.session_state.game_over = True
                        if w=="Tie": st.session_state.score["Tie"] += 1
                        elif w==HUMAN or w=="X": st.session_state.score["Human"] += 1
                        elif w==AI or w=="O": st.session_state.score["AI"] += 1

                    st.rerun()

# ---------------- AI MOVE ----------------
if mode=="Player vs AI" and st.session_state.turn == AI and not st.session_state.game_over:
    time.sleep(0.25)
    r,c = ai_pick_move()
    st.session_state.board[r][c] = AI
    st.session_state.turn = HUMAN
    w = check_winner(st.session_state.board)
    if w:
        st.session_state.game_over = True
        if w=="Tie": st.session_state.score["Tie"] += 1
        elif w==HUMAN: st.session_state.score["Human"] += 1
        elif w==AI: st.session_state.score["AI"] += 1
    st.rerun()

# ---------------- GAME STATUS ----------------
winner = check_winner(st.session_state.board)
if winner == HUMAN or winner=="X":
    st.success("Player 1 wins!" if mode=="Player vs Player" else "You win!")
    st.snow()
elif winner == AI or winner=="O":
    st.error("Player 2 wins!" if mode=="Player vs Player" else "AI wins!")
elif winner == "Tie":
    st.info("It's a tie!")
else:
    if mode=="Player vs AI":
        st.write("Your turn!" if st.session_state.turn==HUMAN else "AI thinking...")
    else:
        st.write(f"{st.session_state.turn}'s turn")

# ---------------- RESET BUTTON ----------------
st.markdown("<div class='resetbutton'>", unsafe_allow_html=True)
if st.button("Reset Game"):
    st.session_state.board = [[EMPTY]*3 for _ in range(3)]
    st.session_state.game_over = False
    if mode == "Player vs AI":
        st.session_state.turn = HUMAN if st.session_state.first_move=="Human" else AI
    else:
        st.session_state.turn = "Player 1" if st.session_state.first_move=="Player 1" else "Player 2"
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("Made by Srinjoy Das")
