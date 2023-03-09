import librosa
import numpy as np
import os
from numpy.linalg import norm
from random import shuffle


def get_mfcc(wav_name, mode):
    y, sr = librosa.load(wav_name, sr=16000)

    # 0.2s => 16000 * 0.2 = 3200
    # 0.1s => 16000 * 0.1 = 1600
    # 自動偵測範圍
    y = y[y.tolist().index(max(y)):y.tolist().index(max(y)) + 1600]

    '''
    print('取樣率:', sr)
    print('signal length:', len(y))
    print('time:', len(y) / sr, 's')
    '''

    n_mfcc = 13
    hop_length = int(sr * 0.01)
    n_fft = int(sr * 0.025)

    # 取出 mfcc
    mfcc = librosa.feature.mfcc(
        y=y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)

    # 處理要回傳的mfcc格式
    if mode == "average":
        mfcc_avg_vector = np.zeros(mfcc.shape[0])
        for i in range(mfcc.shape[1]):
            mfcc_avg_vector += mfcc[:, i]
        mfcc_avg_vector /= mfcc_avg_vector.shape[0]
        return mfcc_avg_vector
    elif mode == "duration":
        mfcc_dur_vectors = list()
        for i in range(mfcc.shape[1]):
            mfcc_dur_vectors.append(np.array(mfcc[:, i]))
        mfcc_dur_vectors = np.array(mfcc_dur_vectors)
        return mfcc_dur_vectors


def compete(A_wav_path, B_wav_path, Test_wav_path, mode):
    if mode == "average":
        A_mfcc = get_mfcc(A_wav_path, mode)
        A_vector = A_mfcc[1:].copy()

        B_mfcc = get_mfcc(B_wav_path, mode)
        B_vector = B_mfcc[1:].copy()

        test_mfcc = get_mfcc(Test_wav_path, mode)
        Test_vector = test_mfcc[1:].copy()

        # A - test
        cosine_A_Test = np.dot(A_vector, Test_vector)/(
            norm(A_vector)*norm(Test_vector))
        # B - test
        cosine_B_Test = np.dot(B_vector, Test_vector) / \
            (norm(B_vector)*norm(Test_vector))

        # print("A_wav:", cosine_A_Test)
        # print("B_wav:", cosine_B_Test)

        if cosine_A_Test >= cosine_B_Test:
            return 'A'
        else:
            return 'B'

    elif mode == "duration":
        A_mfccs = get_mfcc(A_wav_path, mode)
        A_vectors = A_mfccs.copy()

        B_mfccs = get_mfcc(B_wav_path, mode)
        B_vectors = B_mfccs.copy()

        test_mfccs = get_mfcc(Test_wav_path, mode)
        Test_vectors = test_mfccs.copy()

        for i in range(len(A_vectors)):
            A_mfcc_win_count = 0
            B_mfcc_win_count = 0

            # A - test
            cosine_A_Test = np.dot(A_vectors[i], Test_vectors[i])/(
                norm(A_vectors[i])*norm(Test_vectors[i]))
            # B - test
            cosine_B_Test = np.dot(B_vectors[i], Test_vectors[i]) / \
                (norm(B_vectors[i])*norm(Test_vectors[i]))

            if cosine_A_Test >= cosine_B_Test:
                A_mfcc_win_count += 1
            else:
                B_mfcc_win_count += 1

        if A_mfcc_win_count >= B_mfcc_win_count:
            return 'A'
        else:
            return 'B'


def process(category, wav_name):
    Category_list = [os.path.join("category", category, "a"), os.path.join("category", category, "b")]
    # ---------------------------------------------------
    A_wav_name_list = os.listdir(os.getcwd() + '/' + Category_list[0])
    B_wav_name_list = os.listdir(os.getcwd() + '/' + Category_list[1])

    A_win_count = 0
    B_win_count = 0

    # 內部進行比較
    for j in range(min(len(A_wav_name_list),len(B_wav_name_list))):
        A_wav_path = os.getcwd() + '/' + \
            Category_list[0] + '/' + A_wav_name_list[j]
        B_wav_path = os.getcwd() + '/' + \
            Category_list[1] + '/' + B_wav_name_list[j]
        Test_wav_path = os.getcwd() + '/' + wav_name

        win_category = compete(
            A_wav_path, B_wav_path, Test_wav_path, "average")  # average duration
        if win_category == 'A':
            A_win_count += 1
        elif win_category == 'B':
            B_win_count += 1

    result_value = int(A_win_count/(A_win_count + B_win_count) * 100)
    if category == "watermelon":
        if A_win_count > B_win_count:
            return f'新鮮 {result_value}%'
        elif A_win_count < B_win_count:
            return f'成熟 {result_value}%'
        else:
            return f'適中 {result_value}%'
    else:
        if A_win_count > B_win_count:
            return f'水瓶 {result_value}%'
        elif A_win_count < B_win_count:
            return f'空瓶 {result_value}%'
        else:
            return f'適中 {result_value}%'
        

if __name__ == '__main__':
    # 修改處
    category = "watermelon"
    Category_list = [os.path.join("category", category, "a"), os.path.join("category", category, "b")]
    # ---------------------------------------------------
    A_wav_name_list = os.listdir(os.getcwd() + '/' + Category_list[0])
    B_wav_name_list = os.listdir(os.getcwd() + '/' + Category_list[1])

    Test_wav_name_list = os.listdir(os.getcwd() + '/' + Category_list[2])

    if len(Test_wav_name_list) == 0:
        print('目錄Category_Test內沒有測試音檔')
        exit(1)

    # Test 全部測試
    for i in range(len(Test_wav_name_list)):
        A_win_count = 0
        B_win_count = 0

        # 內部進行比較
        for j in range(min(len(A_wav_name_list),len(B_wav_name_list))):
            A_wav_path = os.getcwd() + '/' + \
                Category_list[0] + '/' + A_wav_name_list[j]
            B_wav_path = os.getcwd() + '/' + \
                Category_list[1] + '/' + B_wav_name_list[j]
            Test_wav_path = os.getcwd() + '/' + \
                Category_list[2] + '/' + Test_wav_name_list[i]

            win_category = compete(
                A_wav_path, B_wav_path, Test_wav_path, "average")  # average duration
            if win_category == 'A':
                A_win_count += 1
            elif win_category == 'B':
                B_win_count += 1

        # 最後數量判斷
        result_value = int(A_win_count/(A_win_count + B_win_count) * 100)
        if A_win_count > B_win_count:
            print(Test_wav_name_list[i], '辨識結果為',
                  Category_list[0], f"{result_value}%")
        elif A_win_count < B_win_count:
            print(Test_wav_name_list[i], '辨識結果為',
                  Category_list[1], f"{result_value}%")
        else:
            print(Test_wav_name_list[i], '辨識結果為',
                  "medium", f"{result_value}%")

