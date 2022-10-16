import speech_recognition as sr
import nltk
from signs_dict import *
import cv2
import numpy as np


# nltk.download('punkt')

r = sr.Recognizer()
word_gap = 100  # space between words


def recognize():
    with sr.Microphone() as source:
        print('Hi!!! Say Something:')
        audio = r.listen(source)
        print('Audio Recognition Done!')

    try:
        text = r.recognize_google(audio, language='si-LK')
    except:
        print("Not recognized")
        exit()

    return text


def letter_mapping(token):
    letters = list(token)
    print('letters:', letters)
    output_letters = []

    i = 0

    while i < len(letters):
        if letters[i] in vowels:  # for vowel letter
            output_letters.append(letter_sign_dict[letters[i]])
        elif letters[i] in consonants.keys():
            output_letters.append(letter_sign_dict[consonants[letters[i]]])
            try:
                if letters[i + 1] == '්':
                    i += 1
                elif letters[i + 1] in pili.keys():  # for any vowel other than අ
                    output_letters.append(letter_sign_dict[pili[letters[i + 1]]])
                    i += 1
                else:  # for අ
                    output_letters.append(letter_sign_dict['අ'])
            except:
                output_letters.append(letter_sign_dict['අ'])

        elif letters[i] in letter_sign_dict.keys():  # for digit
            output_letters.append(letter_sign_dict[letters[i]])

        i += 1

    return output_letters


def sign_mapping(text):
    signs = []  # to store sign images and space between signs

    if text in word_sign_dict.keys():  # checking if whole sentence is in the dictionary
        signs.append(word_sign_dict[text])
        signs.append(word_gap)

    else:  # mapping each word to sign
        tokens = nltk.word_tokenize(text)  # to split the sentence into words
        # tokens = text.split()
        print('Tokens:', tokens)

        token_count = len(tokens)
        i = 0

        while i < token_count:

            if tokens[i] in full_key:
                pos = i
                t = tokens[i]

                # checking for combined token in word_sign_dict
                for j in range(i, token_count - 1):
                    t = ' '.join([t, tokens[j + 1]]) # place where tokens are joined
                    # t = 'ආයුබෝවන් ඔබට'
                    if t in full_key:
                        pos += 1
                    else:
                        k = len(tokens[j + 1]) + 1
                        t = t[:-k]
                        # t = 'ආයුබෝවන්'
                        break

                if t in word_sign_dict.keys():
                    signs.append(word_sign_dict[t])
                    i = pos
                # elif tokens[i] in word_sign_dict.keys():
                #     signs.append(word_sign_dict[tokens[i]])
                else:
                    signs += letter_mapping(tokens[i])

            else:
                signs += letter_mapping(tokens[i])

            signs.append(word_gap)
            i += 1

    signs.pop()
    return signs


def display_results(signs):
    images = []
    gap_image = np.zeros((1, word_gap, 3))

    for sign in signs:
        if sign == word_gap:
            images.append(gap_image)
        else:
            images.append(cv2.imread(sign))

    if images == []:
        print('Failed to recognize. Not in Sinhala Language')
        exit()

    shapes = [image.shape for image in images]
    max_h = max(shapes, key=lambda item: item[0])[0]
    total_w = sum(j for i, j, k in shapes)

    result = np.zeros((max_h, total_w, 3), dtype=np.uint8)
    cumulative_width = 0

    for i in range(len(images)):
        result[:shapes[i][0], cumulative_width:cumulative_width + shapes[i][1]] = images[i]
        cumulative_width += shapes[i][1]

    cv2.imshow('result', result)
    cv2.imwrite('result.png', result)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if k == ord('c'): # press c key for correct results
        return True
    elif k == 27: # press escape key to exit
        exit()
    return False


if __name__ == '__main__':
    text = recognize()
    print('You said:', text)
    signs = sign_mapping(text)
    print('signs:', signs)
    display_results(signs)
