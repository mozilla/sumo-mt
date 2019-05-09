#!/usr/bin/env python


from google.cloud import translate_v3beta1 as translate


client = translate.TranslationServiceClient()

project_id = "driven-fragment-240113"
text = u'Hello, world!'
location = 'global'

print "Text: " + text

parent = client.location_path(project_id, location)

response = client.translate_text(
    parent=parent,
    contents=[text],
    mime_type='text/plain',  # mime types: text/plain, text/html
    source_language_code='en',
    target_language_code='ru')

for translation in response.translations:
    print(u'Translation: {}'.format(translation.translated_text))
