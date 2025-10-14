n = [size := 6]
sub = ["Maths", "Science", "English", "Hindi", "Social","Marathi"]
total_marks = 0
out_of = 600

print("Enter marks out of 100 for each subject:")
for i in range(6):
    marks = int(input(f"Enter {sub[i]} marks: "))
    n.append(marks)
    total_marks += marks
    i = i+1

percentage = (total_marks / out_of)*100
print(f"Total Marks : {total_marks}/{out_of}")
print("Percentage : ", percentage)

if percentage >= 90:
    print("Grade : O")
    print("Remarks : Excellent")
elif percentage >= 80:
    print("Grade : A+")
    print("Remarks : Very Good")
elif percentage >= 70:
    print("Grade : A")
    print("Remarks : Good")
elif percentage >= 60:
    print("Grade : B")
    print("Remarks : Average")
elif percentage >= 40:
    print("Grade : C")
    print("Remarks : Poor")
else:
    print("Grade : F")
    print("Remarks : Fail")