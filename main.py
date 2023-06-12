import json
import requests
from pathlib import Path

#Создам основную функцию, которая будет озвучивать исходный текст
def text_to_speech():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMDlkMTJkODYtZjRlOS00MWQ0LTliNWMtOWQ3NTczZDM5MmRlIiwidHlwZSI6ImZyb250X2FwaV90b2tlbiJ9.wRHlaVupySH0Q83ghnDL-JCLHTnh600CbFHbFVTUrpY"}    #создам словарь для авторизации на edenAI, указав полученный API ключ
    url = 'https://api.edenai.run/v2/audio/text_to_speech'    #API адрес, куда будут идти запросы

    input_path = Path('C:/Users/lobod/PycharmProjects/TexttoSpeech/Input texts')    #буду обрабатывать каждый файл, находящийся в папке, по отдельности
    print('Запускаю процесс обработки. Немного подождите...')
    for files in input_path.glob('*.txt'):
        file_name = files.stem
        with open(files, 'r', encoding='UTF-8') as text:
            text = text.read()
        payload = {
            'providers': 'lovoai',
            'language': 'ru-RU',
            'option': 'FEMALE',
            'lovoai': 'ru-RU_Natalia Sychyov',
            'text': f'{text}'
        }

        response = requests.post(url, json=payload, headers=headers)    #отправляем запрос
        result = json.loads(response.text)    #сохраняем ответ
        # unx_time = int(time.time())    #формируем название файлов, например значение времени в unix формате
        with open(f'{file_name}.json', 'w') as file:    #сохраняем ответ на запрос для дальнейшего анализа и проработки
            json.dump(result, file, indent=5, ensure_ascii=False)

        audio_url = result.get('lovoai').get('audio_resource_url')    #выбираем url для сохраненяи и обработки аудиофайла (адрес указан в json формате выше)
        audio_response = requests.get(audio_url)    #делаем запрос для загрузки аудиофайла
        with open(f'C:/Users/lobod/PycharmProjects/TexttoSpeech/Output audio/{file_name}.wav', 'wb') as file:    #сохраняем аудиофайл в соотвествующей папке
            file.write(audio_response.content)
    print('Готово!')


def main():
    text_to_speech()

if __name__ == '__main__':
    main()
