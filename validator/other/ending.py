# 1. ВВОД - строка "должна быть красной"
# 2. определяю declination(строка) // rule = должна
# 3. определяю наличие суффикса быть
#       (true) вырезаю(строка, суффикс)
# 4. вырезаю( строка, declination ) // word_cut = красной
# 5. возвращаю кортеж ( declination, word_cut ) // должна, красной
# 
# 6. изменяю transform_word( word_cut по endings на layout )
# 7.    определяю ending для word_cut // ending = "ой"
# 8.    word_cut.заменить(ending на layout[ending]) // красная


endings = ["ый", "ым", "ой", "ая", "ые", "ое"]

declination = [
    "должен",
    "должна",
    "должно",
    "должны"
]

layout = {
    "ый": "ый",
    "ым": "ый",
    "ой": "ая",
    "ая": "ая",
    'ые': 'ые',
    'ыми':'ые',
    'ими':'ие',
    'ым': 'ое',
    "им": "ее",
    "ое": "ое"
}

# layout = {
#     "должен": ("ый", "ым"),
#     "должна": ("ой", "ая"),
#     "должны": ("ые", "ие"),
#     "должно": ("ое", "ee")
# }
def extract_layout(word, declination):
    suffix = "быть"
    for rule in declination:
        if ( word.count(rule) ):
            word_cut = word.replace(rule, "").strip()
            word_cut = word.replace(suffix, "").strip()

    if word_cut.count(suffix):
        word_cut = word.replace(suffix, "")
        rule 
        print(rule)

    return (rule, word_cut)

def transform_word(word, endings):
    for end in endings:
        return 1


# word_extracted = extract_layout("должна быть красной", declination)

# word_transform = transform_word(word_extracted, endings) 

# print(word_extracted)



key = "должен"

for end in layout[key]:
    print(end)

# print (declination["должен"])

