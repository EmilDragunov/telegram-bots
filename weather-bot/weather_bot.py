import math
import datetime
import requests
from aiogram import Bot, Dispatcher, types, executor
from config import YOUR_TOKEN, API


bot = Bot(YOUR_TOKEN)
dp = Dispatcher(bot)
code_to_smile = {
     "Clear": "Ясно \U00002600",
     "Clouds": "Облачно \U00002601",
     "Rain": "Дождь \U00002614",
     "Drizzle": "Дождь \U00002614",
     "Thunderstorm": "Гроза \U000026A1",
     "Snow": "Снег \U0001F328",
     "Mist": "Туман \U0001F32B"
}


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я пришлю сводку погоды')


@dp.message_handler()
async def get_weather(message: types.Message):
    city = message.text.strip().lower()
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}', params={'units': 'metric', 'lang': 'ru', 'APPID': API})
    if response.status_code == 200:
        data = response.json()
        city = data['name']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']

        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        weather_description = data['weather'][0]['main']

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, я не понимаю, что там за погода...'

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Погода в городе: {city}\n"
                            f"Температура: {temp} °C {wd}\n"
                            f"Ощущается как: {feels_like} °C\n"
                            f"Влажность: {humidity} %\n"
                            f"Давление: {math.ceil(pressure/1.333)} мм.рт.ст\n"
                            f"Скорость ветра: {wind_speed} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\n"
                            f"Закат солнца: {sunset_timestamp}\n"
                            f"Продолжительность дня: {length_of_the_day}\n"
                            f"Хорошего дня!")
    else:
        await message.reply('Проверьте название города!')


executor.start_polling(dp)
