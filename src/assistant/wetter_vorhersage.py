# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Weather Forecast Feature."""

# import difflibs
import json

import requests


def json_weather_api_request(city: str) -> str:
    """Use http request for wttr.in API.

    Args:
        city: the city we want to get the weather from

    Returns:
        returns output as string

    """
    response = requests.get(f'https://de.wttr.in/{city}?format=j1')
    response.raise_for_status()
    return str(response.content.decode('utf8').strip())


def extract_output_string(
    time_keyword: str,
    city: str,
    condition: str,
    tempreture: str,
    feels_like_tempreture: str,
) -> str:
    """Convert data into a spoken string.

    Args:
        time_keyword: specified time
        city: city as string
        condition: weather condition as string
        tempreture: temprutre as string
        feels_like_tempreture: feels like tempreture as string

    Returns:
        a readable text that describes the weather.

    """
    if city:
        return f'Das Wetter {time_keyword} in {city}'\
               f' ist {condition} mit einer Temperatur'\
               f' von {tempreture}, aber es fühlt sich an wie {feels_like_tempreture}.'

    return f'Das Wetter {time_keyword} ist {condition}'\
           f' mit einer Temperatur von {tempreture}, '\
           f'aber es fühlt sich an wie {feels_like_tempreture}.'


def find_city(input_str: str) -> str:
    """Find cities in a string.

    Args:
        input_str: name of a city as string

    Returns:
        city name.

    """
    if 'in' not in input_str:
        return ''
    splits = input_str.split(' in ')[1]
    splits = splits.replace('heute', '')
    splits = splits.replace('übermorgen', '')
    splits = splits.replace('morgen', '')
    if len(splits.split(' ')) > 2:
        city = splits.split(' ')[0]
    else:
        city = splits
    return city.strip()


def weather_output_hnadler(input_sentence: str) -> str:
    """Search for the weather forecast in specific city.

    Args:
        input_sentence: of the input sentence as string

    Returns:
        plain text to be spoken out.

    """
    try:
        city = find_city(input_sentence)
        output_sentence = ''
        j = json.loads(json_weather_api_request(city))
        for word in input_sentence.split(' '):
            if word in 'morgen':
                output_sentence = extract_output_string(
                    'morgen',
                    city,
                    j['weather'][1]['hourly'][4]['lang_de'][0]['value'],
                    j['weather'][1]['hourly'][4]['tempC'],
                    j['weather'][1]['hourly'][4]['FeelsLikeC'],
                )
                break
            if word in 'übermorgen':
                output_sentence = extract_output_string(
                    'übermorgen',
                    city,
                    j['weather'][2]['hourly'][4]['lang_de'][0]['value'],
                    j['weather'][2]['hourly'][4]['tempC'],
                    j['weather'][2]['hourly'][4]['FeelsLikeC'],
                )
                break
        if not output_sentence:
            return extract_output_string(
                'heute',
                city,
                j['current_condition'][0]['lang_de'][0]['value'],
                j['current_condition'][0]['temp_C'],
                j['current_condition'][0]['FeelsLikeC'],
            )
        return output_sentence
    except requests.exceptions.ConnectionError:
        return 'Die Wettervorhersage wurde nicht angezeigt! Bitte überprüfen Sie Ihr Internet'
