import matplotlib.pyplot as plt

# Define the data
whisper_words = 15147
iflytek_words = 18723

# Set up the chart
labels = ['WhisperAPI', 'iFlyTek']
sizes = [whisper_words, iflytek_words]
colors = ['#ff9999','#66b3ff']

# Create the chart
fig1, ax1 = plt.subplots()
ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)

# Add a title
ax1.set_title('Number of Words Transcribed by WhisperAPI and iFlyTek')

# Show the chart
plt.show()

import matplotlib.pyplot as plt

# Data
whisper_word_count = 15147
iflytek_word_count = 18723
whisper_time = 318 # seconds
iflytek_time = 30 * 60 # seconds

# Plot
fig, ax = plt.subplots()
ax.bar(['WhisperAPI', 'iFlyTek'], [whisper_word_count, iflytek_word_count])
ax.set_ylabel('Word Count')
ax2 = ax.twinx()
ax2.plot(['WhisperAPI', 'iFlyTek'], [whisper_time, iflytek_time], color='red', marker='o')
ax2.set_ylabel('Time Taken (Seconds)')
plt.title('Comparison of Word Count and Time Taken for Transcription')
plt.show()

