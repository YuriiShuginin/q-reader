import pdfplumber
from gtts import gTTS
from pathlib import Path
from tempfile import NamedTemporaryFile
from playsound import playsound
import re
import time

def parse_questions(file_path, quest_num=36):
    with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
        pages = [page.extract_text() for page in pdf.pages]

    text = ''.join(pages)

    questions = []
    for i in range(quest_num):
        start_ind = text.find(f"Вопрос {i + 1}.")
        finish_ind = text[start_ind::].find("Ответ:") + start_ind

        q = text[start_ind:finish_ind - 2]

        if "[логическая пауза]" in q:
            q = q.replace("[логическая пауза]", "")

        if "Раздаточный материал:" in q:
            ind_1 = q.find("Раздаточный материал:")
            ind_2 = q[ind_1::].find("\n", q[ind_1::].find("\n") + 1) + ind_1
            q = q[:ind_1] + q[ind_2 + 1:]
        
        if "[" in q:
            ind_1 = q.find("[")
            ind_2 = q.find("]")
            q = q[:ind_1] + q[ind_2 + 4:]
        
        q = q.replace("Вопрос ", "Вопрос №", 1)
        q = q.replace(".", ":", 1)
        q = q.replace('\n', '')
        if "..." in q:
            q = q.replace("...", " ")
        
        marks = []
        for sym in q:
            if sym in ".?!:;":
                marks.append(sym)

        q_list = re.split('[.!?:;]', q)

        for i, mark in enumerate(marks):
            q_list[i] = q_list[i] + mark

        questions.append(q_list[:len(q_list )- 1])

    return questions

def read(question="Сегодня мы играем в ЧГК!"):
    player = NamedTemporaryFile(suffix=".mp3")

    audio = gTTS(text=question, lang="ru", slow=True)
    audio.write_to_fp(player)
    playsound(player.name)

    player.close()
    
    if question[-1] in '.?!':
        time.sleep(6)
    else:
        time.sleep(3)

def game(questions=[]):
    read("Удачи!")

    for i, q in enumerate(questions):
        print(f"\n[+] Reading question #{i + 1}...")

        for sent in q:
            read(sent)

        while (inp := input("[?] Enter r to repeat the question or n to read the next: ")) != "n":
            if inp == "r":
                print(f"\n[+] Reading question #{i + 1}...")
                for sent in q:
                    read(sent)
    
    print("\n[+] The game is finished successfully!")

def main():
    file_path = input("\n[?] Enter a file's path: ")
    
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':
        quest_num = int(input("[?] Enter the number of questions in the game: "))
        game(parse_questions(file_path, quest_num))
    else:
        print("[-] File doesn't exist, check the file path!")
        main()
    
if __name__ == '__main__':
    main()