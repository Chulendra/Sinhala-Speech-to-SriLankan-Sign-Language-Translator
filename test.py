from time import sleep
from recognizer import sign_mapping, display_results

test_data = [
    'ආයුබෝවන් ඔබට කොහොමද මම ගණිත විෂය පාඩම් කරනවා',
    'වැස්ස නිසා තණකොළ කොළ පාටින් බබළනවා',
    'කෝච්චිය මග ඇරුනු නිසා මම බැංකුව වෙතට ඇවිදිනවා',
    'ඔහුගේ උපන්දිනය 1998 අගෝස්තු 9 වැනි දිනයේ තියෙනවා',
    'උදේ ආහාරය සඳහා පාන් සමඟ කෙසෙල් තියෙනවා',
    'මගේ පවුලේ තාත්තා අම්මා අයියා අක්කා සහ සීයා ඉන්නවා',
    'සමහරවිට සියලුම දෙනා හෙට පාසල පිරිසිදු කරනවා',
    'පූසා පස්සෙන් බල්ලා දුවනවා',
    'අද මම ගෙදර ගිහින් බත් කනවා',
    'මම මඤ්ඤොක්කා කන්න ගොඩක් ආසයි',
    'අපි ගුරුතුමා වෙත ගෞරවය කරනවා'
]

def get_accuracy():
    correct = 0

    for text in test_data:
        sleep(0.2)
        signs = sign_mapping(text)
        print('signs:', signs)
        if display_results(signs):
            correct += 1

    accuracy = (correct/len(test_data)) * 100
    print(f'Accuracy: {accuracy:.2f}%')

get_accuracy()
