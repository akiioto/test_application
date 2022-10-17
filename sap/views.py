import requests
from django.shortcuts import render
import collections


def make_statistics(lst):
    filtered_list = list(filter(None, lst))
    return collections.Counter(filtered_list)


def index(request):
    repo_list = []
    events_list = []
    repo_language = []

    url_user_info = 'https://api.github.com/users/{}'
    url_user_repository_info = 'https://api.github.com/users/{}/repos'
    url_user_events_info = 'https://api.github.com/users/{}/events'
    user = 'dmadison'

    user_info = requests.get(url_user_info.format(user)).json()
    user_repository_info = requests.get(url_user_repository_info.format(user)).json()
    user_events_info = requests.get(url_user_events_info.format(user)).json()

    for user_details in user_repository_info:
        repo_list.append(user_details['name'])
        repo_language.append(user_details['language'])

    for events in user_events_info:
        if events['type'] == 'PushEvent':
            events_list.append((events['actor']['login'], events['repo']['name']))

    user_details = {
        'user_email': user_info['name'],
        'user_repositories': repo_list,
        'preferred_lang': make_statistics(repo_language),
        'events_list': events_list
    }

    context = {'user_details': user_details}

    return render(request, 'github/index.html', context)
