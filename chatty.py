import matplotlib.pyplot as plt
import re
from datetime import datetime, timedelta
from tkinter import Tk, filedialog

# 파일 선택 대화 상자 표시
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select Chat Log File", filetypes=[("Text Files", "*.log"), ("All Files", "*.*")])

if not file_path:
    print("No file selected.")
    exit()

# 채팅로그 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    chat_log = file.readlines()

# 시작 시간 추출
start_time_regex = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}):\d{2}"
start_time_match = re.search(start_time_regex, chat_log[0])
if start_time_match:
    start_time = start_time_match.group(1)
else:
    start_time = ""

# 시간대 빈도수 계산 (1분 단위)
time_frequency = {}
time_regex = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}):\d{2}"
for entry in chat_log:
    match = re.search(time_regex, entry)
    if match:
        time = match.group(1)
        time_frequency[time] = time_frequency.get(time, 0) + 1

# 시간대 정렬
sorted_times = sorted(time_frequency.keys())

# 빈도수 추출
frequencies = [time_frequency[time] for time in sorted_times]

# 막대 그래프 그리기
plt.bar(sorted_times, frequencies)
plt.title("Chat Frequency by Time (1-minute intervals)")
plt.xlabel("Time")
plt.ylabel("Frequency")

# x축 눈금에 시작 시간을 뺀 상대적인 시간 표시
if start_time:
    relative_times = [(int(time.split(':')[0]) * 60 + int(time.split(':')[1])) - (int(start_time.split(':')[0]) * 60 + int(start_time.split(':')[1])) for time in sorted_times]
    plt.xticks(sorted_times, relative_times, rotation=45)

plt.show()
