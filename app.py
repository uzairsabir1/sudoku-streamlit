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
    board = [[0]*9 for _ in range(9)]
    solve_sudoku(board)
    return board

def create_puzzle(board, removed=40):
    puzzle = [row[:] for row in board]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:removed]:
        puzzle[r][c] = 0
    return puzzle

st.title("🧩 Sudoku Game")

if "board" not in st.session_state:
    solved = generate_sudoku()
    st.session_state.original = create_puzzle(solved)
    st.session_state.board = [row[:] for row in st.session_state.original]

for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        if st.session_state.original[r][c] != 0:
            cols[c].write(f"**{st.session_state.original[r][c]}**")
        else:
            val = cols[c].number_input(
                "", 1, 9, 0,
                key=f"{r}-{c}"
            )
            if val != 0:
                if is_valid(st.session_state.board, r, c, val):
                    st.session_state.board[r][c] = val
                else:
                    st.warning(f"Invalid move at Row {r+1}, Col {c+1}")

if st.button("Reset Game"):
    st.session_state.clear()
