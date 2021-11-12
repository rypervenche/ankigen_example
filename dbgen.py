import sqlite3
import re


# region
connection = sqlite3.connect("chardict.db")
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS characters (id INTEGER NOT NULL, simplified TEXT)"
)
cursor.execute("CREATE TABLE IF NOT EXISTS pinyin (id INTEGER NOT NULL, pinyin TEXT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS definitions (id INTEGER NOT NULL, definition TEXT)"
)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS cn_sentence (id INTEGER NOT NULL, cn_sentence TEXT)"
)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS en_sentence (id INTEGER NOT NULL, en_sentence TEXT)"
)

with open("cedict_tatoeba_userdict.txt", encoding="utf-8") as tatoeba:
    wordid = 0
    for line in tatoeba:
        tabsplit = line.split("\t")
        characters = tabsplit[0]
        simplified = characters.split("[")[0]
        # trad = characters.split("[")[1]
        pinyin = tabsplit[1]
        definitions_sentences = tabsplit[2].split("")
        definitions = definitions_sentences[0].split("")
        cursor.execute("INSERT INTO characters VALUES (?, ?)", (wordid, simplified))
        cursor.execute("INSERT INTO pinyin VALUES (?, ?)", (wordid, pinyin))
        def_list = []
        for word in definitions:
            cursor.execute(
                "INSERT INTO definitions VALUES (?, ?)", (wordid, word.rstrip())
            )

        if len(definitions_sentences) > 1:
            sentence_split = definitions_sentences[1].split("")
            cn_sentence = sentence_split[0]
            eng_sentence = sentence_split[1]
            cursor.execute(
                "INSERT INTO cn_sentence VALUES (?, ?)", (wordid, cn_sentence)
            )
            cursor.execute(
                "INSERT INTO en_sentence VALUES (?, ?)", (wordid, eng_sentence)
            )
        wordid = wordid + 1
connection.commit()
# endregion


connection2 = sqlite3.connect("cedict.db")
cursor2 = connection2.cursor()
cursor2.execute(
    "CREATE TABLE IF NOT EXISTS characters (id INTEGER NOT NULL, simplified TEXT)"
)
cursor2.execute("CREATE TABLE IF NOT EXISTS pinyin (id INTEGER NOT NULL, pinyin TEXT)")
cursor2.execute(
    "CREATE TABLE IF NOT EXISTS definitions (id INTEGER NOT NULL, definition TEXT)"
)


cc_cedict = open("cedict_ts.u8", encoding="utf-8")
cdict_id = 0
for line in cc_cedict:
    if not line.startswith("#") and not line.startswith("%"):
        regex = r"([^ ]+)\s+([^ ]+)\s+(\[[^]]+\])\s+(.*)"
        parsed_string = re.search(regex, line)
        trad = parsed_string.group(1)
        simp = parsed_string.group(2)
        pinyin = parsed_string.group(3)
        definition = parsed_string.group(4)
        cursor2.execute("INSERT INTO characters VALUES(?, ?)", (cdict_id, simp))
        cursor2.execute("INSERT INTO pinyin VALUES (?, ?)", (cdict_id, pinyin))
        for defin in definition.split("/"):
            cursor2.execute("INSERT INTO definitions VALUES (?, ?)", (cdict_id, defin))
        cdict_id += 1
connection2.commit()
connection2.close()
