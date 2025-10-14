# Student Grade Calculator

A simple Python script that accepts marks (out of 100) for six subjects and prints the total, percentage, grade and remarks.

Files
- `Task2_(Student_Grade_Calculator).py` — main script (interactive). 

Prerequisites
- Python 3.x installed

How to run
1. Open a terminal in the project folder (where `Task2_(Student_Grade_Calculator).py` is located).
2. Run:

```powershell
python .\Task2_(Student_Grade_Calculator).py
```

Sample run (example input shown):

Enter marks out of 100 for each subject:
```
Enter Maths marks: 95
Enter Science marks: 92
Enter English marks: 88
Enter Hindi marks: 90
Enter Social marks: 85
Enter Marathi marks: 93
```

Sample output for the above inputs:

```
Total Marks : 543/600
Percentage :  90.5
Grade : O
Remarks : Excellent
```

Notes
- The script expects integer inputs (0-100) for each subject. It does minimal input validation and will raise an error for non-integer input.

Feel free to modify the subject list or scoring logic as needed.
