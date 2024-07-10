from tkinter import *
from tkinter import messagebox

# Enigma 창 정의
window = Tk()
window.title("Enigma")
window.geometry("400x200")
window.resizable(False, False)

# 로터 배열, 반사판 설정, 로터 설정, 플러그 설정을 위한 레이블과 입력 필드 정의
rotorLabel = Label(window, text="로터 배열 (1-8, 공백으로 구분):")
rotorLabel.grid(row=0, column=0)
rotorInput = Entry(window)
rotorInput.grid(row=0, column=1)

reflectorLabel = Label(window, text="반사판 설정 (B 또는 C):")
reflectorLabel.grid(row=1, column=0)
reflectorInput = Entry(window)
reflectorInput.grid(row=1, column=1)

rotorSettingLabel = Label(window, text="로터 설정 (1-26, 공백으로 구분):")
rotorSettingLabel.grid(row=2, column=0)
rotorSettingInput = Entry(window)
rotorSettingInput.grid(row=2, column=1)

plugLabel = Label(window, text="플러그 설정 (AB CD EF ...):")
plugLabel.grid(row=3, column=0)
plugInput = Entry(window)
plugInput.grid(row=3, column=1)

textLabel = Label(window, text="암호화 할 텍스트:")
textLabel.grid(row=4, column=0)
textInput = Entry(window)
textInput.grid(row=4, column=1)

# 로터 및 반사판 정의
rotors = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "VZBRGITYUPSDNHLXAWMJQOFECK",
    "JPGVOUMFYQBENHZRDKASXLICTW",
    "NZJHGRCXMYSWBOUFAIVLPEKQDT",
    "FKQHTLXOCBJSPDZRAMEWNIUYGV"
]
reflectorB = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
reflectorC = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

# 실패 메시지 출력 함수
def fail():
    messagebox.showinfo("실패", "입력값이 올바르지 않습니다.")

# 입력값 유효성 검사 함수
def validate_inputs(rotorOrder, rotorSetting, plugSetting, reflector):
    # 길이 검사
    if len(rotorOrder) != 3 or len(rotorSetting) != 3:
        return False
    # 중복 검사
    if len(set(rotorOrder)) != 3:
        return False
    # 범위 검사
    if not all(1 <= r <= 8 for r in rotorOrder):
        return False
    # 범위 검사
    if not all(1 <= s <= 26 for s in rotorSetting):
        return False
    # 플러그 설정 검사
    all_plugs = ''.join(plugSetting)
    if len(set(all_plugs)) != len(all_plugs): # 중복 검사
        return False
    for pair in plugSetting: # 길이 및 알파벳 검사
        if len(pair) != 2 or not pair.isalpha():
            return False
    # 반사판 검사
    if reflector not in ["B", "C"]:
        return False
    return True

# 로터 회전 함수
def rotate_rotors(rotorSetting):
    rotorSetting[2] = (rotorSetting[2] + 1) % 26
    if rotorSetting[2] == 0:  # 오른쪽 로터가 26에서 1로 돌아감
        rotorSetting[1] = (rotorSetting[1] + 1) % 26
        if rotorSetting[1] == 0:  # 중간 로터가 26에서 1로 돌아감
            rotorSetting[0] = (rotorSetting[0] + 1) % 26

# 에니그마 암호화 함수
def enigma_encrypt(char, rotorOrder, rotorSetting, plugSetting, reflector):
    char = char.upper()
    
    # 플러그보드 교환 구현
    for plug in plugSetting:
        if char in plug:
            char = plug[1] if char == plug[0] else plug[0]

    # 로터 통과 (순방향)
    for i in range(3):
        offset = (ord(char) - 65 + rotorSetting[i]) % 26
        char = rotors[rotorOrder[i] - 1][offset]
    
    # 반사판 통과
    char = reflectorB[ord(char) - 65] if reflector == "B" else reflectorC[ord(char) - 65]
    
    # 로터 통과 (역방향)
    for i in range(2, -1, -1):
        offset = (rotors[rotorOrder[i] - 1].index(char) - rotorSetting[i]) % 26
        char = chr(offset + 65)
    
    # 플러그보드 교환 구현
    for plug in plugSetting:
        if char in plug:
            char = plug[1] if char == plug[0] else plug[0]

    return char

# 암호화 함수
def encrypt():
    try:
        # 입력값 얻기
        rotorOrder = list(map(int, rotorInput.get().split()))
        rotorSetting = list(map(int, rotorSettingInput.get().split()))
        plugSetting = plugInput.get().upper().split()
        reflector = reflectorInput.get().upper()
        input_text = textInput.get().upper()
        
        # 입력값 유효성 검사
        if not validate_inputs(rotorOrder, rotorSetting, plugSetting, reflector):
            fail()
            return

        # 입력 텍스트의 유효성 검사 (알파벳과 공백만 허용)
        if not all(c.isalpha() or c.isspace() for c in input_text):
            messagebox.showinfo("실패", "알파벳과 공백만 입력 가능합니다.")
            return

        # 암호화
        encrypted_text = ''
        for char in input_text:
            if char.isalpha():
                encrypted_text += enigma_encrypt(char, rotorOrder, rotorSetting, plugSetting, reflector)
                rotate_rotors(rotorSetting)  # 로터 회전
            else:
                encrypted_text += char

        # 암호화 결과를 클립보드에 복사
        window.clipboard_clear()
        window.clipboard_append(encrypted_text)
        messagebox.showinfo("암호화 결과", f"암호화된 텍스트: {encrypted_text}\n(클립보드에 복사되었습니다.)")
    except Exception as e:
        print(e)
        fail()

# 암호화 버튼 정의
button = Button(window, text="암호화", command= encrypt)
button.grid(row=5, column=1, sticky=W+E)

# Enigma 창 실행
window.mainloop()