

with open("C:/Users/Dominic-Asus/Documents/UZH/Semester_4/CALiR/dictionary.csv", "r",
          encoding="utf-8") as f:
    fr_word_ls = f.read().splitlines()

#print(len(fr_word_ls))



with open("C:/Users/Dominic-Asus/Documents/UZH/Semester_4/CALiR/parole_uniche.txt", "r",
          encoding="utf-8") as f:
    it_word_ls = f.read().splitlines()

#print(len(it_word_ls))

with open("C:/Users/Dominic-Asus/Documents/UZH/Semester_4/CALiR/words_alpha.txt", "r",
          encoding="utf-8") as f:
    en_word_ls = f.read().splitlines()

print(len(en_word_ls))