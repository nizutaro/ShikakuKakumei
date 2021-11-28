#!/usr/bin/env python
# coding: utf-8

# In[13]:


import PySimpleGUI as sg
from os.path import basename
import os
#画像を読み込み
from PIL import Image


# In[22]:


sg.theme('Light Brown')

frame1 = [[sg.Radio('ファイルを正方形にする', 1, key='-MULTI-SHEET-', default=True)]]          

col1 = [[sg.Button('実行')],
       [sg.Button('終了')]]

layout = [[sg.Text('ファイル選択', size=(15, 1), justification='right'),
          sg.InputText('ファイル一覧', enable_events=True,),
          sg.FilesBrowse('ファイルを追加', key='-FILES-', file_types=(('jpgファイル', '*.jpg'),))],
          [sg.Output(size=(100, 5), key='-MULTILINE-')],
          [sg.Button('入力一覧をクリア')],
          [sg.Listbox([], size=(100, 10), enable_events=True, key='-LIST-')],
          [sg.Frame('処理内容', frame1), sg.Column(col1)]]

window = sg.Window('しかくかくめい（β）', layout)

#配列に格納する
new_files = []
new_file_names = []

while True:
    event, values = window.read()
    if event in (None, '終了'):
        break

    if event == '実行':
        print('処理を実行')
        print('処理対象ファイル：', new_files)

        # ラジオボタンの値によって処理が変わる
        if values['-MULTI-SHEET-']:
            img = Image.open(values[0])
            width = img.width
            height = img.height
            print('画像を正方形にする')
         
            def expand2square(pil_img, background_color):
                width, height = pil_img.size
                if width == height:
                    return pil_img
                elif width > height:
                    result = Image.new(pil_img.mode, (width, width), background_color)
                    result.paste(pil_img, (0, (width - height) // 2))
                    return result
                else:
                    result = Image.new(pil_img.mode, (height, height), background_color)
                    result.paste(pil_img, ((height - width) // 2, 0))
                    return result
            for i in new_file_names :
                img_new = expand2square(img, (255, 255, 255)).resize((400,400))
                img_new.save(os.getcwd() + '\\sq_' + (str((i))) , quality=95)
            
        # ポップアップ
        sg.popup('処理が正常終了しました')
    elif event == '入力一覧をクリア':
        print('入力一覧をクリア')

        new_files.clear()
        new_file_names.clear()
        window['-LIST-'].update('')
    elif values['-FILES-'] != '':
       #  print('FilesBrowse')

        # TODO:実運用には同一ファイルかどうかの処理が必要
        new_files.extend(values['-FILES-'].split(';'))
        new_file_names.extend([basename(file_path) for file_path in new_files])

        print('ファイルを追加')
        window['-LIST-'].update(new_file_names)  # リストボックスに表示します

window.close()

