from django.shortcuts import render
from django.http import JsonResponse
from google.cloud import translate_v2 as gtranslate
import sentencepiece as spm
import ctranslate2
import requests
import urllib
import json

translate_client = gtranslate.Client()
source = 'en'
target = 'zh-TW'

translator = ctranslate2.Translator("/Users/winniehsu/Program/python/MT/autocomplete-api/research_data/run6/model/")

sp = spm.SentencePieceProcessor(model_file='/Users/winniehsu/Program/python/MT/autocomplete-api/research_data/run6/en.model')
sp_zh = spm.SentencePieceProcessor(model_file='/Users/winniehsu/Program/python/MT/autocomplete-api/research_data/run6/zh.model')


def translate(request, phrase):
    data = [{'src': phrase, 'id': 100}]
    header = {
        "Content-Type": "application/json",
    }
    req = requests.post('http://127.0.0.1:7414/translator/translate', data=json.dumps(data), headers=header)
    results = req.json()

    return JsonResponse({'status': results})

def translate2(request, phrase):
    p = sp.encode(phrase, out_type=str)
    pt = translator.translate_batch([p])

    # OpenNMT-py Server
    # data = [{'src': ' '.join(p), 'id': 200}]
    # header = {
    #     "Content-Type": "application/json",
    # }
    # req = requests.post('http://127.0.0.1:7414/translator/translate', data=json.dumps(data), headers=header)
    # results = req.json()

    return JsonResponse({'translation': sp_zh.decode(pt[0][0]['tokens'])})


def google_translate(request, phrase):
    # phrase = request.GET['content']
    result = translate_client.translate(
        phrase, source_language=source, target_language=target)

    return JsonResponse({'en': result["input"], 'zh': result["translatedText"]})
