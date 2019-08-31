import re

#   ******************************************************
#   * A small script for generating the spellings.json   *
#   * out of all products. Simply takes every word only  *
#   * once and add a weight of 100. Some words may need  *
#   * to be manually re-weighted should erronous correc- *
#   * become a problem.                                  *
#   ******************************************************

seen = set()
json = []
word_regex = re.compile(r"\b[^\d\W]+\b") # -> matches every word that does not contain numbers
with open("products.txt", "r", encoding="utf-8") as file:
    for line in file:
        split_line = line.split("|")

        words = split_line[0].split(" ")

        for word in words:
            if word_regex.match(word):
                if word not in seen:
                    json.append("\""+word+"\": 100,")
                seen.add(word)
    file.close()

with open("spellings.json", "w", encoding="utf-8") as json_file:
    json_file.write("{")
    for line in json:
        json_file.write("\t" + line + "\n")
    json_file.write("}")
    json_file.close()
