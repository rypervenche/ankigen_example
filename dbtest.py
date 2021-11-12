import sqlite3
import re


connection = sqlite3.connect("chardict.db")
cursor = connection.cursor()

connection2 = sqlite3.connect("cedict.db")

cursor2 = connection2.cursor()
word = input("Enter a word to look up: ")

cursor2.execute("SELECT id FROM characters WHERE simplified = (?)", (word,))

result = cursor2.fetchall()

idlist = []
pinlist = []
deflist = []
for id in result:
    wordid = int(str(id)[1:-2])
    idlist.append(wordid)
    cursor2.execute("SELECT definition FROM definitions WHERE id = (?)", (wordid,))
    definitions = cursor2.fetchall()
    deflist2 = []
    for term in definitions:
        if str(term)[2:-3] != "":
            deflist2.append(str(term)[2:-3])
    deflist.append(deflist2)

print(
    f"{word} has the following pronunciation(s). Please select the number of the entry/entries you'd like to add (separated by spaces): "
)


for id in idlist:
    cursor2.execute("SELECT pinyin FROM pinyin WHERE id = (?)", (id,))
    pinlist.append(cursor2.fetchone()[0][1:-1])

valid_choices = set()
for count, pronunciation in enumerate(pinlist):
    print(f"{count}. {pronunciation}: ", end="")
    for term in deflist[count]:
        if term != deflist[count][-1]:
            print(f"{term}; ", end="")
        else:
            print(f"{term}")
    valid_choices.add(count)


isRunning = True
while isRunning:
    userchoice = input()
    added_numbers = []
    if len(userchoice.strip()) > 0:
        user_split = re.split(r"\s+", userchoice)
        user_split = list(filter(("").__ne__, user_split))
        for count, selection in enumerate(user_split):
            search = re.match(r"\d+", selection)
            if search is None:
                print(
                    "Please enter all of your selections again, ensuring they are separated by spaces."
                )
                break
            elif int(search.group()) not in valid_choices:
                print(
                    f"{int(search.group())} is not a valid selection for the given entries. Please enter your selections again."
                )
                break
            else:
                added_numbers.append(int(search.group()))
            if count == len(user_split) - 1:
                isRunning = False
    for number in added_numbers:
        print(f"Added the following terms: {word} {pinlist[number]}.")
