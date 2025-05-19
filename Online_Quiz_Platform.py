
import pandas as pd
import random

def load_questions_from_excel(filepath):
    df = pd.read_excel(filepath, sheet_name=None)
    subjects = {}

    for subject, data in df.items():
        question_bank = {}
        for idx, row in data.iterrows():
            question_bank[idx + 1] = {
                'Q': row['Question'],
                'options': [row['Option A'], row['Option B'], row['Option C'], row['Option D']],
                'Answer': str(row['Answer']).strip().lower(),
                'Level': str(row['Level']).strip().upper()
            }
        subjects[subject.lower()] = question_bank
    return subjects

subjects = load_questions_from_excel("subject_wise_questions_split.xlsx")

Physics = subjects.get('physics', {})
Chemistry = subjects.get('chemistry', {})
Math = subjects.get('math', {})
Biology = subjects.get('biology', {})

def ask_quiz(Subject, per_q_mark, total_marks):
    score = 0
    num_q = total_marks // per_q_mark
    easy_q = int(num_q * 0.5)
    med_q = int(num_q * 0.25)
    hard_q = num_q - (easy_q + med_q)

    easy = [question_id for question_id, question in Subject.items() if question['Level'] == 'EASY']
    medium = [question_id for question_id, question in Subject.items() if question['Level'] == 'MEDIUM']
    hard = [question_id for question_id, question in Subject.items() if question['Level'] == 'HARD']

    selected_easy = random.sample(easy, min(easy_q, len(easy)))
    selected_medium = random.sample(medium, min(med_q, len(medium)))
    selected_hard = random.sample(hard, min(hard_q, len(hard)))

    selected_ids = selected_easy + selected_medium + selected_hard
    random.shuffle(selected_ids)

    user_responses = []

    for question_id in selected_ids:
        question = Subject[question_id]
        print("\n" + question['Q'])
        # Simple option display without enumerate/chr
        print("a. " + question['options'][0])
        print("b. " + question['options'][1])
        print("c. " + question['options'][2])
        print("d. " + question['options'][3])
        
        user_answer = input("Your answer (a/b/c/d): ").lower()
        is_correct = (user_answer == question['Answer'])
        if is_correct:
            score += per_q_mark
        user_responses.append({
            'question': question['Q'],
            'your_answer': user_answer,
            'correct_answer': question['Answer'],
            'result': "Correct" if is_correct else "Wrong"
        })

    return score, user_responses

def distribution_pcm(total_marks):
    phy_marks = int(total_marks * 0.25)
    chem_marks = int(total_marks * 0.25)
    maths_marks = int(total_marks * 0.5)
    return phy_marks, chem_marks, maths_marks

def distribution_pcb(total_marks):
    phy_marks = int(total_marks * 0.25)
    chem_marks = int(total_marks * 0.25)
    bio_marks = int(total_marks * 0.5)
    return phy_marks, chem_marks, bio_marks
    
def set_general_aptitude():
    print("\n-- General Aptitude Quiz --")
    total_marks = int(input("Enter total marks for General Aptitude: "))
    print("\nCombo Options:\n1. PCM\n2. PCB")
    combo = input("Choose combo (1/2): ")

    final_responses = []

    if combo == '1':
        phy_marks, chem_marks, math_marks = distribution_pcm(total_marks)
        p_score, p_responses = ask_quiz(Physics, 1, phy_marks)
        c_score, c_responses = ask_quiz(Chemistry, 1, chem_marks)
        m_score, m_responses = ask_quiz(Math, 2, math_marks)
        final_responses = p_responses + c_responses + m_responses
        print(f"\nPhysics: {p_score}/{phy_marks}")
        print(f"Chemistry: {c_score}/{chem_marks}")
        print(f"Math: {m_score}/{math_marks}")
        print(f"Total: {p_score + c_score + m_score}/{total_marks}")
    elif combo == '2':
        phy_marks, chem_marks, bio_marks = distribution_pcb(total_marks)
        p_score, p_responses = ask_quiz(Physics, 1, phy_marks)
        c_score, c_responses = ask_quiz(Chemistry, 1, chem_marks)
        b_score, b_responses = ask_quiz(Biology, 2, bio_marks)
        final_responses = p_responses + c_responses + b_responses
        print(f"\nPhysics: {p_score}/{phy_marks}")
        print(f"Chemistry: {c_score}/{chem_marks}")
        print(f"Biology: {b_score}/{bio_marks}")
        print(f"Total: {p_score + c_score + b_score}/{total_marks}")
    else:
        print("Invalid combo choice.")
    
    return final_responses

# Main quiz interface
print("Quiz Topics:\n1. Physics\n2. Chemistry\n3. Math\n4. Biology\n5. General Aptitude (PCM/PCB)")
choice = input("Choose topic (1-5): ")

final_responses = []

if choice == "1":
    print("\nPhysics Quiz:")
    total_marks = int(input("Enter total marks for Physics: "))
    p_score, final_responses = ask_quiz(Physics, 1, total_marks)
    print(f"\nYour Score: {p_score}/{total_marks}")
elif choice == "2":
    print("\nChemistry Quiz:")
    total_marks = int(input("Enter total marks for Chemistry: "))
    c_score, final_responses = ask_quiz(Chemistry, 1, total_marks)
    print(f"\nYour Score: {c_score}/{total_marks}")
elif choice == "3":
    print("\nMath Quiz:")
    total_marks = int(input("Enter total marks for Math: "))
    m_score, final_responses = ask_quiz(Math, 2, total_marks)
    print(f"\nYour Score: {m_score}/{total_marks}")
elif choice == "4":
    print("\nBiology Quiz:")
    total_marks = int(input("Enter total marks for Biology: "))
    b_score, final_responses = ask_quiz(Biology, 2, total_marks)
    print(f"\nYour Score: {b_score}/{total_marks}")
elif choice == "5":
    final_responses = set_general_aptitude()
else:
    print("Invalid topic choice.")

if final_responses:
    print("\n--- Your Responses ---")
    for response in final_responses:
        print(f"\nQ: {response['question']}")
        print(f"Your Answer: {response['your_answer']}")
        print(f"Correct Answer: {response['correct_answer']}")
        print(f"Result: {response['result']}")
