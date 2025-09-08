import streamlit as st
import streamlit.components.v1 as components
from itertools import permutations
import json
import re
import numpy as np
import matplotlib.pyplot as plt
import decimal
import gspread
from google.oauth2.service_account import Credentials
import datetime
import os

st.set_page_config(page_title="Final Exam", layout="centered")
st.title("Final Exam")
st.header("Student Information")

# ========== Student Info ==========
class_options = ["1/11", "1/12"]
selected_class = st.selectbox("Select your class:", class_options)
nickname = st.text_input("Nickname")
student_number = st.text_input("Student Number")

answers = st.secrets["answers"]

# ========== Part I: Sudoku Puzzle (6pts) ==========
st.header("Part I: Sudoku Puzzle (6pts)")
st.write("**Instruction:** Solve the 4x4 and 6x6 Sudoku using the appropriate numbers.")

puzzle_4x4 = st.secrets["sudoku_4x4"]["puzzle"]
solution_4x4 = st.secrets["sudoku_4x4"]["solution"]
puzzle_6x6 = st.secrets["sudoku_6x6"]["puzzle"]
solution_6x6 = st.secrets["sudoku_6x6"]["solution"]

sudoku = components.declare_component("sudoku", path="sudoku_component")
sudoku2 = components.declare_component("sudoku2", path="sudoku_component2")

st.write("### 4x4 Sudoku")
board_4x4 = sudoku(default=puzzle_4x4, key="sudoku4x4")

st.write("### 6x6 Sudoku")
board_6x6 = sudoku2(default=puzzle_6x6, key="sudoku6x6")

# ========== Part II: Counting Combinations I (2pts) ==========
st.header("Part II: Counting Combinations I (2pts)")
st.write("**Instruction:** Given the colors below, make the possible combinations and answer the following questions.")
st.image("rby.png")

colors = ["", "Red", "Blue", "Yellow"]
tower_inputs = {}
cols = st.columns(6)
for i, col in enumerate(cols):
    with col:
        st.markdown(f"**Tower {i+1}**")
        tower_inputs[i] = []
        for block in range(3):
            block_color = st.selectbox(f"Select", colors, key=f"tower{i}_block{block}", label_visibility="collapsed")
            tower_inputs[i].append(block_color)

questions_4_6 = {
    4: ("How many three block towers can you make out of them?", ["a. 5", "b. 6", "c. 8", "d. 12"], answers["q4"]),
    5: ("If there is a restriction that you cannot put the yellow block at the top. How many towers can you make?", ["a. 2", "b. 4", "c. 6", "d. 8"], answers["q5"]),
    6: ("If there is a restriction that you cannot put the red block and blue block at the top. How many towers can you make?", ["a. 2", "b. 4", "c. 6", "d. 8"], answers["q6"]),
}
for qnum in questions_4_6:
    q, opts, _ = questions_4_6[qnum]
    st.radio(f"**{qnum}. {q}**", options=opts, key=f"q{qnum}")

# ========== Part III: Counting Combinations II (2pts) ==========
st.header("Part III: Counting Combinations II (2pts)")
st.write("**Instruction:** Suppose that the five-character code has the following restrictions:")
st.markdown("""
- Numbers only
- Cannot repeate characters
""")
st.image("5ch.png")

questions_7_10 = {
    7: ("What sets of characters can the code contain?", ["a. a-z (lowercase letters)", "b. 0-9 (numbers)", "c. A-Z (uppercase letters)", "d. All of the above"], answers["q7"]),
    8: ("How many possible numbers and letters are there for the first character of the code?", ["a. 52 possible letters and numbers", "b. 10 possible numbers", "c. 62 possible letters and numbers", "d. 9 possible numbers"], answers["q8"]),
    9: ("How many possible numbers and letters are there for the fifth character of the code?", ["a. 52 possible letters and numbers", "b. 10 possible numbers", "c. 62 possible letters and numbers", "d. 6 possible numbers"], answers["q9"]),
    10: ("How many different code combinations are possible given the statement above?", [
        "a. 44,261,653,680 possible combinations",
        "b. 380,204,032 possible combinations",
        "c. 100,000 possible combinations",
        "d. 30,240 possible combinations"
    ], answers["q10"]),
}

for qnum in questions_7_10:
    q, opts, _ = questions_7_10[qnum]
    st.radio(f"**{qnum}. {q}**", options=opts, key=f"q{qnum}")




# LCM

# Part IV: Lowest Common Multiple (5pts)
st.header("Part IV: Lowest Common Multiple (5pts)")
st.write("**Instruction:** Given the two numbers, find the LCM (Lowest Common Multiple) using the Listing Method.")

# LCM Questions (Question ID: (num1, num2))
lcm_questions = {
    11: (3, 8),
    12: (3, 12),
    13: (8, 9),
}

# Function to get multiples of a number up to the LCM
def get_multiples(num, lcm):
    multiples = []
    i = 1
    while num * i <= lcm:
        multiples.append(num * i)
        i += 1
    return multiples

# Initialize total score
total_score = 0
question_scores = {}

# Iterate over each question
for question_id, (num1, num2) in lcm_questions.items():
    st.write(f"Question {question_id}: Find the LCM of **{num1}** and **{num2}**.")
    
    # Calculate the correct LCM
    lcm = np.lcm(num1, num2)
    
    # Get the correct multiples for both numbers up to the LCM
    correct_multiples_num1 = get_multiples(num1, lcm)
    correct_multiples_num2 = get_multiples(num2, lcm)
    
    # Input for multiples of num1
    multiples_num1 = st.text_area(f"Multiples of {num1} (comma-separated):", placeholder=f"e.g, 3, 6, 9...", key=f"multiples_num1_{question_id}")
    
    # Input for multiples of num2
    multiples_num2 = st.text_area(f"Multiples of {num2} (comma-separated):", placeholder=f"e.g, 3, 6, 9...", key=f"multiples_num2_{question_id}")
    
    # Input for LCM guess
    lcm_guess = st.text_input(f"LCM of {num1} and {num2}:", key=f"lcm_guess_{question_id}")
    st.write("")
    st.write("")
    
    # Store user inputs
    user_multiples = {
        "num1": [int(x.strip()) for x in multiples_num1.split(",") if x.strip().isdigit()],
        "num2": [int(x.strip()) for x in multiples_num2.split(",") if x.strip().isdigit()],
    }

    try:
        user_lcm_guess = int(lcm_guess)
    except:
        user_lcm_guess = -1

    # Check if the LCM is listed in either of the multiples
    lcm_correct = str(lcm) in [str(x) for x in user_multiples["num1"]] or str(lcm) in [str(x) for x in user_multiples["num2"]]
    
    # Grading the LCM guess
    lcm_guess_correct = user_lcm_guess == lcm
    
#     # Provide feedback for each question
#     st.write(f"---\nQuestion {question_id}:")
    
#     if lcm_correct:
#         st.success(f"Your multiples include the LCM! +2 points")
#     else:
#         st.warning(f"Your multiples do not include the LCM. The LCM is {lcm}.")
    
#     if lcm_guess_correct:
#         st.success(f"Your LCM guess is correct! +3 points")
#     else:
#         st.warning(f"Your LCM guess is incorrect. The correct LCM is {lcm}.")

# # Show the total score
# st.write(f"---\nTotal Score: {total_score} / 15")

# # Show detailed scores for each question
# for question_id, scores in question_scores.items():
#     st.write(f"Question {question_id}: {scores['total']} points")
#     st.write(f"  - Multiples: {scores['multiples_correct']} points")
#     st.write(f"  - LCM Guess: {scores['lcm_correct']} points")












# Factor Trees
tree = components.declare_component("tree", path="tree_component")
st.write("**14 - 15. Find the Prime Factors of the following numbers.**")
tree_result = tree(key="factor_tree")


# ========== Part V: Binary Number System (5pts) ==========
st.header("Part V: Binary Number System (5pts)")

st.write("**Instruction:** Add the following binary numbers.")

# Q16
col1, col2, col3 = st.columns([1, 2, 8])

with col1:
    st.text("16.\n     +\n\n\n     =")  # Use st.text, not st.write!

with col2:
    st.text("0010\n0001\n----")
    binary_sum_16 = st.text_input("Answer", key="bin_sum_16", label_visibility="collapsed")

# Q17
col1, col2, col3 = st.columns([1, 2, 8])

with col1:
    st.text("17.\n     +\n\n\n     =")

with col2:
    st.text("0111\n0001\n----")
    binary_sum_17 = st.text_input("Answer", key="bin_sum_17", label_visibility="collapsed")

st.write("")
st.write("")








# Q18 - Decimal 9 to binary
st.write("**Instruction:** Use the Divide By 2 Method to convert the following decimal numbers into binary.")
st.write("18. Convert the decimal number **9** into binary.")

if "div2_steps_q18" not in st.session_state:
    st.session_state.div2_steps_q18 = []

if "input_error_q18" not in st.session_state:
    st.session_state.input_error_q18 = ""

def add_div2_step_q18():
    raw = st.session_state.div2_input_q18.strip()
    try:
        dividend, divisor = map(int, raw.split("/"))
        if divisor != 2:
            st.session_state.input_error_q18 = "❌ You must divide by 2."
            return

        quotient = dividend // 2
        remainder = dividend % 2

        st.session_state.div2_steps_q18.append(f"{dividend} ÷ 2 = {quotient} R{remainder}")
        st.session_state.div2_input_q18 = ""
        st.session_state.input_error_q18 = ""
    except:
        st.session_state.input_error_q18 = "❌ Invalid format. Use e.g., 9/2"

def remove_last_div2_step_q18():
    if st.session_state.div2_steps_q18:
        st.session_state.div2_steps_q18.pop()

# Show steps
for step in st.session_state.div2_steps_q18:
    st.text(step)

# Input and buttons
st.text_input("Type a division step (e.g., 9/2)", key="div2_input_q18")
if st.session_state.input_error_q18:
    st.warning(st.session_state.input_error_q18)

cols = st.columns([1.5, 6])
with cols[0]:
    st.button("Add division step", on_click=add_div2_step_q18, key="add_div2_step_q18")
with cols[1]:
    st.button("Remove last step", on_click=remove_last_div2_step_q18, key="remove_div2_step_q18")

binary_q18 = st.text_input("Answer:", placeholder="e.g., 0010", key="binary_q18")
st.write("")
st.write("")



# Q19 - Decimal 21 to binary
st.write("")
st.write("19. Convert the decimal number **21** into binary.")

if "div2_steps_q19" not in st.session_state:
    st.session_state.div2_steps_q19 = []

if "input_error_q19" not in st.session_state:
    st.session_state.input_error_q19 = ""

def add_div2_step_q19():
    raw = st.session_state.div2_input_q19.strip()
    try:
        dividend, divisor = map(int, raw.split("/"))
        if divisor != 2:
            st.session_state.input_error_q19 = "❌ You must divide by 2."
            return

        quotient = dividend // 2
        remainder = dividend % 2

        st.session_state.div2_steps_q19.append(f"{dividend} ÷ 2 = {quotient} R{remainder}")
        st.session_state.div2_input_q19 = ""
        st.session_state.input_error_q19 = ""
    except:
        st.session_state.input_error_q19 = "❌ Invalid format. Use e.g., 21/2"


def remove_last_div2_step_q19():
    if st.session_state.div2_steps_q19:
        st.session_state.div2_steps_q19.pop()

# Show steps
for step in st.session_state.div2_steps_q19:
    st.text(step)

# Input and buttons
st.text_input("Type a division step (e.g., 21/2)", key="div2_input_q19")
if st.session_state.input_error_q19:
    st.warning(st.session_state.input_error_q19)

cols = st.columns([1.5, 6])
with cols[0]:
    st.button("Add division step", on_click=add_div2_step_q19, key="add_div2_step_q19")
with cols[1]:
    st.button("Remove last step", on_click=remove_last_div2_step_q19, key="remove_div2_step_q19")

binary_q19 = st.text_input("Answer:", placeholder="e.g., 0010", key="binary_q19")


# Q20: Convert each decimal number into a 7-bit binary number to complete the image.
st.write("")
st.write("")
st.write("20. Convert each decimal number into a 7-bit binary number to complete the image.")

# Decimals with partial conversions provided (first 2 rows fixed)
decimal_values = [93, 93, 0, 42, 73, 8, 8]
provided_binaries = [
    format(93, '07b'),       # Fixed: 93
    format(93, '07b'),       # Fixed: 93
    format(0, '07b'),        # Fixed: 0
    "", "", "", ""           # User inputs for the last 5 rows (2 to 6)
]

def validate_binary_input(user_input):
    """Validate and trim the binary input."""
    user_input = user_input.strip()  # Remove leading/trailing whitespaces
    if len(user_input) != 7:
        return False, "❌ Input must be exactly 7 digits."
    if not all(c in '01' for c in user_input):
        return False, "❌ Only 0 or 1 are allowed."
    return True, user_input  # Valid input, return the trimmed value

# Inputs for last 5 binaries (Q20) — keys q20_4 to q20_8 for last five rows (indices 3 to 7)
binary_inputs_q20 = []

col1, col2 = st.columns([1.1, 7])

with col1:
    # Display provided binary values for the first 3 rows (disabled inputs)
    for idx in range(3):  # Show the first three fixed rows
        unique_key = f"q20_{idx}"
        st.text_input(f"{decimal_values[idx]}", value=provided_binaries[idx], disabled=True, key=unique_key)
    
    # Input fields for the last rows (user can fill in the binary values)
    for idx in range(3, 7):  # Indices 3 to 7
        unique_key = f"q20_{idx}"
        binary_input = st.text_input(f"{decimal_values[idx]}", key=unique_key)
        
        # Validate binary input before appending to the list
        if binary_input:  # Only validate if input is not empty
            is_valid, validated_input = validate_binary_input(binary_input)
            if not is_valid:
                st.warning(validated_input)  # Show a warning if invalid input
            else:
                binary_inputs_q20.append(validated_input)
        else:
            # If input is empty, we just leave the field unvalidated
            binary_inputs_q20.append("")

def decode_binary_to_image(bin_list):
    """Convert list of 7-bit binary strings into a 7x7 numpy array (pixels)"""
    pixels = np.zeros((7, 7))
    for i, b in enumerate(bin_list):
        if len(b) == 7 and all(c in '01' for c in b):
            pixels[i] = np.array([int(bit) for bit in b])
        else:
            pixels[i] = np.zeros(7)  # Empty row for incomplete binary data
    return pixels

# Combine the provided and user inputs (use user inputs for rows 4 to 8)
full_binary_list = provided_binaries[:3] + binary_inputs_q20
img_pixels = decode_binary_to_image(full_binary_list)

with col2:
    fig, ax = plt.subplots(figsize=(4, 6))
    ax.imshow(img_pixels, cmap="gray_r", vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)



decimal.getcontext().rounding = decimal.ROUND_HALF_UP

if st.button("Submit Test"):
    if not nickname or not student_number:
        st.error("Please fill in your nickname and student number.")
    else:
        # Build submission record
        submission = {
            "nickname": nickname,
            "student_number": student_number,
            
            "answers": {
                "sudoku": [board_4x4, board_6x6],

                "blocks": {
                    # Tower inputs (6 towers × 3 blocks)
                    "towers": {
                        f"tower{i}": [
                            st.session_state.get(f"tower{i}_block0", ""),
                            st.session_state.get(f"tower{i}_block1", ""),
                            st.session_state.get(f"tower{i}_block2", "")
                        ]
                        for i in range(6)
                    },
                    # Q4 to Q7 multiple choice answers
                    **{f"q{q}": st.session_state.get(f"q{q}", "") for q in range(4, 7)}
                },
                
                "code": {
                    # Q7 to Q10 multiple choice answers
                    **{f"q{q}": st.session_state.get(f"q{q}", "") for q in range(7, 11)}
                },

                # Part III: LCM
                "lcm": {
                    "multiples_num1_11": st.session_state.get("multiples_num1_11", ""),
                    "multiples_num2_11": st.session_state.get("multiples_num2_11", ""),
                    "lcm_guess_11": st.session_state.get("lcm_guess_11", ""),

                    "multiples_num1_12": st.session_state.get("multiples_num1_12", ""),
                    "multiples_num2_12": st.session_state.get("multiples_num2_12", ""),
                    "lcm_guess_12": st.session_state.get("lcm_guess_12", ""),

                    "multiples_num1_13": st.session_state.get("multiples_num1_13", ""),
                    "multiples_num2_13": st.session_state.get("multiples_num2_13", ""),
                    "lcm_guess_13": st.session_state.get("lcm_guess_13", ""),

                    "factor_tree": st.session_state.get("factor_tree", ""),
                },

                "binary": {
                    
                    "bin_sum_16": st.session_state.get("bin_sum_16", ""),
                    "bin_sum_17": st.session_state.get("bin_sum_17", ""),
                    "div2_steps_q18": st.session_state.get("div2_steps_q18", ""),
                    "binary_q18": st.session_state.get("binary_q18", ""),
                    "div2_steps_q19": st.session_state.get("div2_steps_q19", ""),
                    "binary_q19": st.session_state.get("binary_q19", ""),
                    **{f"q{q}": st.session_state.get(f"q20_{q}", "") for q in range(3, 7)},
                }
            }
                    }

        
        # Save to file
        import json, os
        os.makedirs("submissions", exist_ok=True)
        
        import gspread
        from google.oauth2.service_account import Credentials

        # Set up creds and open your sheet
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        
        # Load credentials from Streamlit secrets
        service_account_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        
        client = gspread.authorize(creds)
        import datetime
        
        # Timestamp for filenames and sheets
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        
        json_path = f'{selected_class.replace("/", "-")}_{nickname}_{student_number}_{filename_ts}.json'
        with open(json_path, "w") as f:
            json.dump(submission, f, indent=2)
            
        

        # try:
        #     sheet = client.open("Final").worksheet(selected_class)
        # except gspread.WorksheetNotFound:
        #     st.error(f"Worksheet '{selected_class}' not found. Please check your Google Sheet.")

        # Convert your submission dict into a list of values (flatten if needed)
        # row = [
        #     submission["student_number"],
        #     submission["nickname"],
        #     submission["scores"]["part1_sudoku"],
        #     submission["scores"]["part2_code"],
        #     submission["scores"]["part3_gcf"],
        #     submission["scores"]["part4_graphs"],
        #     submission["scores"]["total"],
        #     timestamp
        #     # add other fields or stringify answers if needed
        # ]

        # sheet.append_row(row)
        # st.success("Submission sent to Google Sheets! ✅")
        # st.success(f"Submission received! ✅ Total Score: {round(total)}/20")
        
        with open(json_path, "rb") as f:
            st.download_button(
            "Download answers",
                data=f,
                file_name=os.path.basename(json_path),
                mime="application/json"
            )























