import random
import os
import re

print("Enter 'Quit' at any time to quit the program.")


def ReadFile(FileName):
    try:
        with open(f'{FileName}.txt','r') as File:
            return(File.readlines())
    except FileNotFoundError:
        with open(f'{FileName}.txt','w') as File:
            pass
        with open(f'{FileName}.txt','r') as File:
            return(File.readlines())
        

def WriteFile(FileName,TextList):
    with open(f'{FileName}.txt','w') as File:
        File.writelines(TextList)


def AppendFile(FileName,Data):
    with open(f'{FileName}.txt','a') as File:
        File.write(Data)


def InterpretFile(FileData):
    Dictionary = {}
    for line in FileData:
        QuizList = line.replace('\n','').split(':')
        Dictionary[QuizList[0]] = QuizList[1]
    return(Dictionary)


def InterpretQuizzes(QuizData):
    return([i.replace('\n','') for i in QuizData])


def Create():
    Quiz = {}
    Question = input("What is the first question?: ")
    while Question == '':
        Question = input("What is the first question?: ")
    while Question:
        if Question == 'quit':
            quit()
        Answer = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("What is the answer to this question?: ").lower()))
        while Answer == '':
            Answer = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("What is the answer to this question?: ").lower()))
        if Answer == 'quit':
            quit()
        Quiz[Question] = Answer
        Question = input("What is the next question?: ")
        if Answer == 'quit':
            quit()
    return(Quiz)


def Study(QuizData):
    print("Enter 'Quit' when finished studying.")
    Questions = [Question for Question in QuizData]
    start = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Enter 'Start' to begin studying: ").lower()))
    while start != 'start' and start != 'quit':
        start = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Enter 'Start' to begin studying: ").lower()))
    if start == 'quit':
        quit()
    Choice = Questions[random.randint(0,len(Questions)-1)]
    Response = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input(Choice + ': ').lower()))
    while Response != 'quit':
        if Response == QuizData[Choice]:
            print('Correct!')
        else:
            print(f"Incorrect, the answer is {QuizData[Choice]}.")
        Choice = Questions[random.randint(0,len(Questions)-1)]
        Response = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input(Choice + ': ').lower()))
        

def Save(QuizData):
    WriteQuiz = [Question+':'+Answer+'\n' for Question,Answer in QuizData.items()]
    Name = input('What is the name of the quiz?: ')
    while Name == '' or Name == 'quit' or Name == 'Saved_Quizzes':
        print('This name is invalid.')
        Name = input('What is the name of the quiz?: ')
    WriteFile(Name,WriteQuiz)
    AppendFile('Saved_Quizzes',Name+'\n')


def Load(QuizList):
    QuizData = {}
    FileName = input(f'Which file would you like to Load from {QuizList}?: ')
    while FileName not in QuizList and FileName != 'quit':
        FileName = input(f'Which file would you like to Load from {QuizList}?: ')
    if FileName == 'quit':
        quit()
    Read = ReadFile(FileName)
    for i in Read:
        Split = i.replace('\n','').split(':')
        QuizData[Split[0]] = Split[1]
    return(QuizData)


def Delete(FileName,QuizList):
    Quizzes = []
    for i in QuizList:
        if i != FileName:
            Quizzes.append(i)
    WriteFile('Saved_Quizzes',Quizzes)
    os.remove(f'{FileName}.txt')
    print(f"{FileName} has been deleted. ")


def Rename(FileName,QuizList):
    Quizzes = []
    NewName = input(f"What is the new name of {FileName}?: ")
    while NewName == '' or NewName == 'quit' or NewName == 'Saved_Quizzes':
        print('This name is invalid.')
        NewName = input(f'What is the new name of the {FileName}?: ')
    os.rename(FileName + '.txt',NewName + '.txt')
    for i in QuizList:
        if i != FileName:
            Quizzes.append(i)
        else:
            Quizzes.append(NewName+'\n')
    WriteFile('Saved_Quizzes',Quizzes)
    print(f"{FileName} has been renamed to {NewName}.")


def DeleteQuestion(FileName):
    NewQuizData = {}
    WriteData = []
    QuizData = InterpretFile(ReadFile(FileName))
    print('\n')
    for q,a in QuizData.items():
        print(f"{q}:{a}")
    print('\n')
    Choice = input("Enter the question:answer that you would like to delete: ")
    if Choice == 'quit':
        quit()
    Question = Choice.split(':')
    while Question[0] not in QuizData.keys() or Question[1] not in QuizData.values():
        Choice = input("Enter the question:answer that you would like to delete: ")
        if Choice == 'quit':
            quit()
        Question = Choice.split(':')
    for Q,A in QuizData.items():
        if Q != Question[0]:
           NewQuizData[Q] = A
    for Q,A in NewQuizData.items():
        WriteData.append(Q + ':' + A + '\n')
    WriteFile(FileName,WriteData)


def AddQuestion(FileName):
    Q = input("What is the question?: ")
    while Q == '':
        Q = input("What is the question?: ")
    if Q == 'quit':
        quit()
    A = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("What is the answer to this question?: ").lower()))
    while A == '':
        A = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("What is the answer to this question?: ").lower()))
    if Q == 'quit':
        quit()
    AppendFile(FileName,Q + ':' + A + '\n')


def Edit(FileName):
    Action = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Would you like to 'Add' or 'Delete' a question?: ").lower()))
    while Action != 'add' and Action != 'delete' and Action != 'quit':
        Action = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Would you like to 'Add' or 'Delete' a question?: ")))
    if Action == 'quit':
        quit()
    elif Action == 'delete':
        DeleteQuestion(FileName)
    elif Action == 'add':
        AddQuestion(FileName)


def Settings(QuizList):
    FileName = input(f"Which file would you like to edit from {QuizList}?: ")
    while FileName not in QuizList and FileName != 'quit':
        FileName = input(f"Which file would you like to edit from {QuizList}?: ")
    if FileName == 'quit':
        quit()
    else:
        Action = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Would you like to 'Delete', 'Rename' or 'Edit' this file?: ").lower()))
        while Action != 'delete' and Action != 'rename' and Action != 'edit' and Action != 'quit':
            Action = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Would you like to 'Delete', 'Rename' or 'Edit' this file?: ").lower()))
        if Action == 'quit':
            quit()
        elif Action == 'delete':
            Delete(FileName,QuizList)
        elif Action == 'rename':
            Rename(FileName,QuizList)
        elif Action == 'edit':
            Edit(FileName)
        

def Menu():
    Quiz_List = InterpretQuizzes(ReadFile('Saved_Quizzes'))
    if Quiz_List == []:
        Action = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Create a new quiz with 'Create': ").lower()))
        while Action != 'create' and Action != 'quit':
            Action = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Create a new quiz with 'Create': ").lower()))
        if Action == 'quit':
            quit()
        else:
            Created_Quiz = Create()
            Study(Created_Quiz)
            Keep = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Would you like to save this quiz? ('Yes' or 'No'): ").lower()))
            while Keep != 'yes' and Keep != 'no' and Keep != 'quit':
                Keep = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Would you like to save this quiz? ('Yes' or 'No'): ").lower()))
            if Keep == 'yes':
                Save(Created_Quiz)
    else:
        Action = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input(f"Load a new quiz with 'Load', create a new quiz with 'Create' or edit one with 'Settings': ").lower()))
        while Action != 'create' and Action != 'create' and Action != 'settings' and Action != 'load' and Action != 'quit':
            Action = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input(f"Load a new quiz with 'Load', create a new quiz with 'Create' or edit one with 'Settings': ").lower()))
        if Action == 'quit':
            quit()
        elif Action == 'load':
            Study(Load(Quiz_List))
        elif Action == 'create':
            Created_Quiz = Create()
            Study(Created_Quiz)
            Keep = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Would you like to save this quiz? ('Yes' or 'No'): ").lower()))
            while Keep != 'yes' and Keep != 'no' and Keep != 'quit':
                Keep = ' '.join(re.split(r'\s+|[.,?!:;-]\s*',input("Would you like to save this quiz? ('Yes' or 'No'): ").lower()))
            if Keep == 'yes':
                Save(Created_Quiz)
        elif Action == 'settings':
            Settings(Quiz_List)


Menu()
