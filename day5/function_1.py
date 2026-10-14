def get_grade(marks):
    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 50:
        return 'C'
    elif marks < 50:
        return 'F'
    else:
        return 'Invalid marks' 

for i in range(5):
    marks = int(input("Enter marks for student {}: ".format(i + 1)))
    grade = get_grade(marks)
    print("Grade for student {}: {}".format(i + 1, grade))