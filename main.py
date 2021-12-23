#from google.colab import drive
from extra import prepare_data
from core import train_auto_enocder_1
from core import train_bi_lstm
from core import test_lstm_v2
# drive.mount('/content/sign-language/drive')


# prepare_data.main()

import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# 1. Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

print('start excutioon--------------')
# prepare_data.main(drive)
train_auto_enocder_1.mainf()

# train_bi_lstm.mainf()

# test_lstm_v2.mainf()

#file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
# for file1 in file_list:
#  print('title: %s, id: %s' % (file1['title'], file1['id']))

#folder = drive.CreateFile({'title' : 'train', 'mimeType' : 'application/vnd.google-apps.folder'})
# folder.Upload()

#fId = folder.get('id')

#uploaded = drive.CreateFile({'title': 'x2.mp4', "parents":  [{"id": fId}],})
# uploaded.SetContentFile('/content/sign-language/data/videos/bg_train_data/01/001_001_001.mp4')
# uploaded.Upload()
#print('Uploaded file with ID {}'.format(uploaded.get('id')))
