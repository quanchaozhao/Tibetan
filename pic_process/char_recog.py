# coding:utf-8


import numpy as np
import os
from skimage import transform,io



def get_string_by_img(imgs,words_text='tools\\words_Titan.txt',model_path='tools\\model_lenet5_v2.h5'):

    data = []
    for img in imgs:
        if len(img) == 0:
            continue
        img = transform.resize(img,(64,32))
        data.append(img)
    data = np.asarray(data)
    data = np.reshape(data,(-1,64,32,1))
    import keras.models
    model = keras.models.load_model(model_path)
    text_unicode = model.predict(data)

    word_dict = []
    with open(words_text,'r') as f:
        for line in f.readlines():
            word_dict.append(line.strip())

    out_char_list = []
    for i,s_char in enumerate(text_unicode):
        char_uni = word_dict[np.argmax(s_char)]
        try:
            if 47 < int(char_uni,16) < 58:
                arr_temp = np.argsort(s_char)
                char_uni = word_dict[arr_temp[1]]
                out_char_list.append(chr(int(char_uni, 16)))
            else:
                out_char_list.append(chr(int(char_uni,16)))
        except Exception as e:
            print(i,e)

    return ''.join(out_char_list)


if __name__ == '__main__':
    path = r'D:\Users\Riolu\Desktop\t33'
    files = os.listdir(path)
    imgs = []
    for file in files:
        print(file)
        img = io.imread(os.path.join(path,file))
        imgs.append(img)
    print(get_string_by_img(imgs,words_text='..\\tools\\words_Titan.txt',model_path='..\\tools\\model_lenet5_v2.h5'))
