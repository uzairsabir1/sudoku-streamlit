import streamlit as st
import random

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    for r in range(9):
        if board[r][col] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return -1, -1

def solve_sudoku(board):
    row, col = find_empty_location(board)
    if row == -1:
        return True
    for num in random.sample(range(1, 10), 9):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku(board)
    return board

def create_puzzle(solved_board, removed_count=40):
    puzzle = [row[:] for row in solved_board]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:removed_count]:
        puzzle[r][c] = 0
    return puzzle

st.set_page_config(page_title="Sudoku Game", layout="centered")
st.title("🧩 Sudoku Game")

if "original" not in st.session_state:
    solved = generate_sudoku()
    st.session_state.original = create_puzzle(solved)
    st.session_state.board = [row[:] for row in st.session_state.original]

for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        if st.session_state.original[r][c] != 0:
            cols[c].markdown(
                f"<div style='text-align:center;font-size:22px;font-weight:bold'>{st.session_state.original[r][c]}</div>",
                unsafe_allow_html=True
            )
        else:
            val = cols[c].number_input(
                "",
                min_value=0,
                max_value=9,
                value=st.session_state.board[r][c],
                key=f"{r}-{c}"
            )
            if val != st.session_state.board[r][c]:
                if val == 0:
                    st.session_state.board[r][c] = 0
                elif is_valid(st.session_state.board, r, c, val):
                    st.session_state.board[r][c] = val
                else:
                    st.warning(f"Invalid move at Row {r+1}, Column {c+1}")
                    st.session_state.board[r][c] = 0

st.divider()

if st.button("🔄 Reset Game"):
    st.session_state.clear()
    st.experimental_rerun()
