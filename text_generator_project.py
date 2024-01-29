# -*- coding: utf-8 -*-
"""Text_Generator_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BuzJMMFN1Vblx6kwu3I917_H2oaQ4kP0
"""

#importing dependencies
import keras
import numpy
import sys
import nltk
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint

# Loading the data
file = open("Text_project.txt", encoding="utf8").read()

"""# New Section"""

#Tokenization
#Standardization
def tokenize_words(input):
    input = input.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(input)
    filtered = filter(lambda token: token not in stopwords.words('english'), tokens)
    return "".join(filtered)
processed_input = tokenize_words(file)

# Converting Characters to numbers
chars = sorted(list(set(processed_input)))
char_to_num = dict((c,i) for i, c in enumerate (chars))

#Checking if conversion of words to characters or characters to numbers worked?
input_len = len(processed_input)
vocab_len = len(chars)
print("Total number of Characters:", input_len)
print("Total vocab:", vocab_len)

#Sequence length
seq_length = 100
x_data = []
y_data = []

#Loopin through the sequence
for i in range(0, input_len - seq_length, 1):
    in_seq = processed_input[i:i + seq_length]
    out_seq = processed_input[i+seq_length]
    x_data.append([char_to_num[char] for char in in_seq])
    y_data.append(char_to_num[out_seq])

n_patterns = len(x_data)
print("Total patterns:", n_patterns)

n_patterns = len(x_data)
print("Total patterns:", n_patterns)

#convert input sequence into an array


X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
X = X/float(vocab_len)

# one-hot encoding our data
y = to_categorical(y_data)

#creating the model
model = Sequential()
model.add(LSTM(256,input_shape= (X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1],activation='softmax'))

# Compiling the model

model.compile(loss='categorical_crossentropy', optimizer='adam')

#saving weights
filepath = "model_weights_saved.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose = 1, save_best_only=True, mode='min')
desired_callbacks =[checkpoint]

#fit the model and let it train
model.fit(X, y, epochs=4, batch_size=256, callbacks = desired_callbacks)

#Recompile model with the saved weights
filename = "model_weights_saved.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

#Output of the model back into characters
num_to_char = dict((i, c) for i, c in enumerate(chars))

start = numpy.random.randint(0, len(x_data)-1)
pattern = x_data[start]
print("Random Seed:")
print("\"", ''.join([num_to_char[value] for value in pattern]), "\"")

#Generate the text
for i in range(1000):
    x = numpy.reshape(pattern, (1,len(pattern),1))
    x = x/float(vocab_len)
    prediction = model.predict(x, verbose = 0)
    index = numpy.argmax(prediction)
    result = num_to_char[index]
    seq_in = [num_to_char[value] for value in pattern]
    sys.stdout.write(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]