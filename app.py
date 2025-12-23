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

st.markdown("""
<style>
.sudoku-cell {
    width: 45px;
    height: 45px;
    text-align: center;
    font-size: 20px;
    border: 1px solid black;
}
.bold-border-right {
    border-right: 3px solid black;
}
.bold-border-bottom {
    border-bottom: 3px solid black;
}
.prefilled {
    background-color: #f0f0f0;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

grid_html = "<table style='border-collapse: collapse; margin: auto;'>"

for r in range(9):
    grid_html += "<tr>"
    for c in range(9):
        extra_class = ""
        if c in [2, 5]:
            extra_class += " bold-border-right"
        if r in [2, 5]:
            extra_class += " bold-border-bottom"

        if st.session_state.original[r][c] != 0:
            grid_html += f"""
            <td class='sudoku-cell prefilled{extra_class}'>
                {st.session_state.original[r][c]}
            </td>
            """
        else:
            value = st.session_state.board[r][c]
            grid_html += f"""
            <td class='sudoku-cell{extra_class}'>
                <input type='number' min='1' max='9'
                value='{value if value != 0 else ""}'
                style='width:100%; height:100%; text-align:center; font-size:18px; border:none;'
                onchange="this.form.submit()">
            </td>
            """
    grid_html += "</tr>"

grid_html += "</table>"

st.markdown(grid_html, unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset Game"):
        st.session_state.clear()
        st.experimental_rerun()

with col2:
    if find_empty_location(st.session_state.board)[0] == -1:
        st.success("🎉 Congratulations! Puzzle Solved!")
