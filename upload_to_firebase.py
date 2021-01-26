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


# for root, dirs, files in os.walk("/content/sign-language/newdata/all"):
#  for filename in files:
#    print(filename)
#    break

filenameListList = [filename for filename in (
    files for root, dirs, files in os.walk("/content/sign-language/newdata/all"))]

filenameList = filenameListList[0]
filenameList.sort()
# print(filenameList)

trainingDataBaseFolder = '/content/drive/MyDrive/data/videos/training_data'
testingDataBaseFolder = '/content/drive/MyDrive/videos/testing_data'

# if not os.path.exists(trainingDataBaseFolder):
#  os.makedirs(trainingDataBaseFolder)

# if not os.path.exists(testingDataBaseFolder):
#  os.makedirs(testingDataBaseFolder)

# create folders
currentIndex = 1
# for fName in filenameList:
#currentFolderName = fName.split('_')[0][1:]
#print('current folder : ' + currentFolderName)

# if(currentIndex % 3 == 0):


#  if not os.path.exists(trainingDataBaseFolder + "/" + currentFolderName):
#    os.makedirs(trainingDataBaseFolder+ "/" + currentFolderName)


def findDriveFolderId(path, baseFolderId):

    subFolder = path[0]

    strPath = "\'" + baseFolderId + "\'" + " in parents and trashed=false"
    sub_folder_list = drive.ListFile({'q': strPath}).GetList()

    subFolderFound = False
    subFolderId = ''

    for file1 in sub_folder_list:
        if(file1['title'] == subFolder):
            subFolderFound = True
            subFolderId = file1['id']

            break

    if(not subFolderFound):
        folder = drive.CreateFile({'title': subFolder, "parents":  [
                                  {"id": baseFolderId}], 'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        subFolderId = folder.get('id')

    if(len(path) == 1):
        return subFolderId

    return findDriveFolderId(path[1:], subFolderId)

#file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
# for file1 in file_list:
    #print('title: %s, id: %s' % (file1['title'], file1['id']))
    # if(file1['title'] == baseFolder):
    #  baseFolderFound = True
    #  baseFolderId = file1['id']
    #  break

#currentIndex = 1;
# for fName in filenameList[0 : 20]:
#  currentFolderName = fName.split('_')[0][1:]
#  print('current folder : ' + currentFolderName)


#print(findDriveFolderId('data/videos/training_data/01'.split("/"), 'root'))

testFolderId = findDriveFolderId('data/videos/testing_data'.split("/"), 'root')

print('testing id  : ' + testFolderId)


currentIndex = 1
for fName in filenameList[2000:]:

    last_part = fName.split('_')[2]

    if(last_part == '004.mp4' or last_part == '005.mp4'):
        print('upload to testdata : ' + fName)
        uploaded = drive.CreateFile(
            {'title': fName, "parents":  [{"id": testFolderId}], })
        uploaded.SetContentFile('/content/sign-language/newdata/all/'+fName)
        uploaded.Upload()

    else:
        currentFolderName = fName.split('_')[0][1:]
        print('upload to current folder ' +
              currentFolderName + 'file : ' + fName)
        fId = findDriveFolderId(
            ('data/videos/training_data/'+currentFolderName).split("/"), 'root')
        uploaded = drive.CreateFile(
            {'title': fName, "parents":  [{"id": fId}], })
        uploaded.SetContentFile('/content/sign-language/newdata/all/'+fName)
        uploaded.Upload()
