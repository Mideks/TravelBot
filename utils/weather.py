import requests


def get_weather_message(city_name):
    url = f"https://wttr.in/{city_name}?lang=ru&format=j1"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        try:
            current_condition = json_data['current_condition'][0]
            message = (
                f"📍{city_name}:\n"
                f"🌡️Температура: {current_condition['temp_C']}°C\n"
                f"💨Ощущается как: {current_condition['FeelsLikeC']}°C\n"
                f"☁️Облачность: {current_condition['cloudcover']}%\n"
                f"💦Влажность: {current_condition['humidity']}%\n"
                f"🌧️Осадки: {current_condition['precipMM']} мм\n"
                f"📏Видимость: {current_condition['visibility']} км\n"
                f"🔋Давление: {current_condition['pressure']} гПа\n"
                f"🌬️Скорость ветра: {current_condition['windspeedKmph']} км/ч\n"
            )
            return message
        except KeyError as e:
            return f"Ошибка при обработке данных: {e}"
    else:
        return "Ошибка при получении данных о погоде"


# Пример использования функции
city_name = "Москва"
print(get_weather_message(city_name))
