from __future__ import print_function
import pickle
import os
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

from googleapiclient.http import MediaFileUpload


def google_api_warranty_push():
    information_file = open(sys.argv[0][:-34] + "Information.txt")

    option = information_file.readline()
    option_split = option.split(":")

    sheet_link_id = option_split[1][1:].replace("\n", "")

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    worksheet = information_file.readline()

    information_file.close()

    worksheet_split = worksheet.split("=")
    worksheet = worksheet_split[1].replace("\n", "")

    # Full ID and range of a the sheet.
    Full_Range = worksheet + '!A1:YY'
    creds = None

    if os.path.exists(sys.argv[0][:-34] + 'token.pickle'):
        with open(sys.argv[0][:-34] + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                sys.argv[0][:-34] + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sys.argv[0][:-34] + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_link_id,
                                range=Full_Range).execute()
    values = result.get('values', [])

    text_information = open(sys.argv[0][:-34] + "Information.txt", "r")

    array_of_info = text_information.readlines()

    text_information.close()
    for info in array_of_info:
        info_split = info.split("=")
        if "Customer_Name" == info_split[0]:
            customer_name = str(info_split[1][:-1])
        elif "Pair_ID" == info_split[0]:
            pair_id = str(info_split[1][:-1])
        elif "Job_Nr" == info_split[0]:
            job_nr = str(info_split[1][:-1])
        elif "Re_Order" == info_split[0]:
            re_order = str(info_split[1][:-1])
        elif "Date" == info_split[0]:
            date = str(info_split[1][:-1])
        elif "Office" == info_split[0]:
            office = str(info_split[1][:-1])
        elif "Comment_For_Error_List" == info_split[0]:
            comment_errlst = str(info_split[1][:-1])
        elif "Which_Lens" == info_split[0]:
            which_lens = str(info_split[1][:-1])
        elif "Entered_By" == info_split[0]:
            entered_by = str(info_split[1][:-1])
        elif "Discount" == info_split[0]:
            discount = str(info_split[1][:-1])
        elif "Mistake_By" == info_split[0]:
            mistake_by = str(info_split[1][:-1])


    array_of_info_to_add = [[customer_name, pair_id, job_nr, re_order, date, office, comment_errlst, which_lens, entered_by, discount, mistake_by]]

    body = {
        'values': array_of_info_to_add
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_link_id, range=Full_Range,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))


def google_drive_image_upload(image_path):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(sys.argv[0][:-34] + 'token_drive.pickle'):
        with open(sys.argv[0][:-34] + 'token_drive.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                sys.argv[0][:-34] + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sys.argv[0][:-34] + 'token_drive.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    image_path_split = image_path.split('\r')
    image_path_split_2 = image_path.split(".")

    file_metadata = {'name': image_path_split[len(image_path_split) - 1]}
    media = MediaFileUpload(image_path, mimetype='image/' + image_path_split_2[len(image_path_split_2) - 1])
    file = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()

    body_permission = {'role': 'reader',
                       'type': 'anyone'
                       }

    file_permissions = service.permissions().create(fileId=file.get('id'), body=body_permission).execute()

    import time
    time.sleep(5)

    return str(file.get('id'))


def google_api_complaints_push():
    information_file = open(sys.argv[0][:-34] + "Information.txt")

    option = information_file.readline()
    option_split = option.split(":")

    sheet_link_id = option_split[1][1:].replace("\n", "")

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    worksheet = information_file.readline()

    information_file.close()

    worksheet_split = worksheet.split("=")
    worksheet = worksheet_split[1].replace("\n", "")

    # Full ID and range of a the sheet.
    Full_Range = worksheet + '!A1:YY'
    creds = None

    if os.path.exists(sys.argv[0][:-34] + 'token.pickle'):
        with open(sys.argv[0][:-34] + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                sys.argv[0][:-34] + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sys.argv[0][:-34] + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_link_id,
                                range=Full_Range).execute()
    values = result.get('values', [])

    text_information = open(sys.argv[0][:-34] + "Information.txt", "r")

    image1_path = ""
    image2_path = ""
    array_of_info = text_information.readlines()

    text_information.close()
    for info in array_of_info:
        info_split = info.split("=")
        if "Pair_ID" == info_split[0]:
            pair_id = str(info_split[1][:-1])
        elif "Date" == info_split[0]:
            date = str(info_split[1][:-1])
        elif "Comment_For_Error_List" == info_split[0]:
            comment_errlst = str(info_split[1][:-1])
        elif "Comment_For_Iasi" == info_split[0]:
            comment_iasi = str(info_split[1][:-1])
        elif "Image1_Path" == info_split[0]:
            image1_path = str(info_split[1][:-1])
        elif "Image2_Path" == info_split[0]:
            image2_path = str(info_split[1][:-1])

    image1_hyperlink = ""
    image2_hyperlink = ""
    if image1_path != "":
        image1_id = google_drive_image_upload(image1_path)
        image1_path = '=IMAGE("https://drive.google.com/uc?export=view&id=' + image1_id + '", 1)'
        image1_hyperlink = '=HYPERLINK("https://drive.google.com/uc?export=view&id=' + image1_id + '", "View Image")'

    if image2_path != "":
        image2_id = google_drive_image_upload(image2_path)
        image2_path = '=IMAGE("https://drive.google.com/uc?export=view&id=' + image2_id + '", 1)'
        image2_hyperlink = '=HYPERLINK("https://drive.google.com/uc?export=view&id=' + image2_id + '", "View Image")'


    array_of_info_to_add = [[pair_id, date + " " + comment_errlst, image1_path, image2_path, "", comment_iasi, image1_hyperlink, image2_hyperlink]]

    body = {
        'values': array_of_info_to_add
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_link_id, range=Full_Range,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))


def google_api_defects_push():
    information_file = open(sys.argv[0][:-34] + "Information.txt")

    option = information_file.readline()
    option_split = option.split(":")

    sheet_link_id = option_split[1][1:].replace("\n", "")

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    worksheet = information_file.readline()

    information_file.close()

    worksheet_split = worksheet.split("=")
    worksheet = worksheet_split[1].replace("\n", "")

    # Full ID and range of a the sheet.
    Full_Range = worksheet + '!A1:YY'
    creds = None

    if os.path.exists(sys.argv[0][:-34] + 'token.pickle'):
        with open(sys.argv[0][:-34] + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                sys.argv[0][:-34] + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sys.argv[0][:-34] + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API 
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_link_id,
                                range=Full_Range).execute()
    values = result.get('values', [])

    text_information = open(sys.argv[0][:-34] + "Information.txt", "r")

    image1_path = ""
    image2_path = ""
    array_of_info = text_information.readlines()

    text_information.close()
    for info in array_of_info:
        info_split = info.split("=")
        if "Pair_ID" == info_split[0]:
            pair_id = str(info_split[1][:-1])
        elif "Date" == info_split[0]:
            date = str(info_split[1][:-1])
        elif "Comment_For_Error_List" == info_split[0]:
            comment_errlst = str(info_split[1][:-1])
        elif "Frame_Supplier" == info_split[0]:
            frame_supplier = str(info_split[1][:-1])
        elif "Image1_Path" == info_split[0]:
            image1_path = str(info_split[1][:-1])
        elif "Image2_Path" == info_split[0]:
            image2_path = str(info_split[1][:-1])

    image1_hyperlink = ""
    image2_hyperlink = ""
    if image1_path != "":
        image1_id = google_drive_image_upload(image1_path)
        image1_path = '=IMAGE("https://drive.google.com/uc?export=view&id=' + image1_id + '", 1)'
        image1_hyperlink = '=HYPERLINK("https://drive.google.com/uc?export=view&id=' + image1_id + '", "View Image")'

    if image2_path != "":
        image2_id = google_drive_image_upload(image2_path)
        image2_path = '=IMAGE("https://drive.google.com/uc?export=view&id=' + image2_id + '", 1)'
        image2_hyperlink = '=HYPERLINK("https://drive.google.com/uc?export=view&id=' + image2_id + '", "View Image")'

    array_of_info_to_add = [[pair_id, date + " " + comment_errlst, image1_path, image2_path, frame_supplier, image1_hyperlink, image2_hyperlink]]

    body = {
        'values': array_of_info_to_add
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_link_id, range=Full_Range,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))


def google_api_refunds_push():
    information_file = open(sys.argv[0][:-34] + "Information.txt")

    option = information_file.readline()
    option_split = option.split(":")

    sheet_link_id = option_split[1][1:].replace("\n", "")

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    worksheet = information_file.readline()

    information_file.close()

    worksheet_split = worksheet.split("=")
    worksheet = worksheet_split[1].replace("\n", "")

    # Full ID and range of a the sheet.
    Full_Range = worksheet + '!A1:YY'
    creds = None

    if os.path.exists(sys.argv[0][:-34] + 'token.pickle'):
        with open(sys.argv[0][:-34] + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                sys.argv[0][:-34] + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sys.argv[0][:-34] + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API 
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_link_id,
                                range=Full_Range).execute()
    values = result.get('values', [])

    text_information = open(sys.argv[0][:-34] + "Information.txt", "r")

    image1_path = ""
    image2_path = ""
    array_of_info = text_information.readlines()

    text_information.close()

    for info in array_of_info:
        info_split = info.split("=")
        if "Pair_ID" == info_split[0]:
            pair_id = str(info_split[1][:-1])
        elif "Date" == info_split[0]:
            date = str(info_split[1][:-1])
        elif "Comment_For_Error_List" == info_split[0]:
            comment_errlst = str(info_split[1][:-1])
        elif "Ticket_Nr" == info_split[0]:
            ticket_nr = str(info_split[1][:-1])
        elif "Image1_Path" == info_split[0]:
            image1_path = str(info_split[1][:-1])
        elif "Image2_Path" == info_split[0]:
            image2_path = str(info_split[1][:-1])

    image1_hyperlink = ""
    image2_hyperlink = ""
    if image1_path != "":
        image1_id = google_drive_image_upload(image1_path)
        image1_path = '=IMAGE("https://drive.google.com/uc?export=view&id=' + image1_id + '", 1)'
        image1_hyperlink = '=HYPERLINK("https://drive.google.com/uc?export=view&id=' + image1_id + '", "View Image")'

    if image2_path != "":
        image2_id = google_drive_image_upload(image2_path)
        image2_path = '=IMAGE("https://drive.google.com/uc?export=view&id=' + image2_id + '", 1)'
        image2_hyperlink = '=HYPERLINK("https://drive.google.com/uc?export=view&id=' + image2_id + '", "View Image")'

    array_of_info_to_add = [[pair_id, date + " " + comment_errlst, image1_path, image2_path, ticket_nr, image1_hyperlink, image2_hyperlink]]

    body = {
        'values': array_of_info_to_add
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_link_id, range=Full_Range,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))

def google_api_stylists_push():
    information_file = open(sys.argv[0][:-34] + "Information.txt")

    option = information_file.readline()
    option_split = option.split(":")

    sheet_link_id = option_split[1][1:].replace("\n", "")

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    worksheet = information_file.readline()

    information_file.close()

    worksheet_split = worksheet.split("=")
    worksheet = worksheet_split[1].replace("\n", "")

    # Full ID and range of a the sheet.
    Full_Range = worksheet + '!A1:YY'
    creds = None

    if os.path.exists(sys.argv[0][:-34] + 'token.pickle'):
        with open(sys.argv[0][:-34] + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                sys.argv[0][:-34] + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sys.argv[0][:-34] + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_link_id,
                                range=Full_Range).execute()
    values = result.get('values', [])

    text_information = open(sys.argv[0][:-34] + "Information.txt", "r")

    image1_path = ""
    image2_path = ""
    array_of_info = text_information.readlines()
    text_information.close()

    for info in array_of_info:
        info_split = info.split("=")
        if "Customer_Name" == info_split[0]:
            customer_name = str(info_split[1][:-1])
        elif "Comment_For_Error_List" == info_split[0]:
            comment_errlst = str(info_split[1][:-1])
        elif "Image1_Path" == info_split[0]:
            image1_path = str(info_split[1][:-1])
        elif "Image2_Path" == info_split[0]:
            image2_path = str(info_split[1][:-1])

    image1_hyperlink = ""
    image2_hyperlink = ""
    if image1_path != "":
        image1_id = google_drive_image_upload(image1_path)
        image1_path = '=IMAGE("https://drive.google.com/uc?export=view&id=' + image1_id + '", 1)'
        image1_hyperlink = '=HYPERLINK("https://drive.google.com/uc?export=view&id=' + image1_id + '", "View Image")'

    if image2_path != "":
        image2_id = google_drive_image_upload(image2_path)
        image2_path = '=IMAGE("https://drive.google.com/uc?export=view&id=' + image2_id + '", 1)'
        image2_hyperlink = '=HYPERLINK("https://drive.google.com/uc?export=view&id=' + image2_id + '", "View Image")'

    array_of_info_to_add = [[customer_name, comment_errlst, image1_path, image2_path, "", image1_hyperlink, image2_hyperlink]]

    body = {
        'values': array_of_info_to_add
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_link_id, range=Full_Range,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))


def magento_api_push():

    text_file = open(sys.argv[0][:-34] + "Information.txt")

    array_of_lines_file = text_file.readlines()
    aux_split = array_of_lines_file[1].split("=")
    order_nr = aux_split[1]
    aux_split = array_of_lines_file[2].split("=")
    comment = aux_split[1]

    text_file.close()

    import requests

    information_file = open(sys.argv[0][:-34] + "Information.txt")

    option = information_file.readline()

    information_file.close()

    option_split = option.split(" ")

    url = option_split[1].replace("\n", "")

    myobj = {"order_number":order_nr[:-1], "comment":comment[:-1]}

    x = requests.post(url, data=myobj)
    print(x.text)


def odoo_api_push():
    text_file = open(sys.argv[0][:-34] + "Information.txt")

    array_of_lines_file = text_file.readlines()

    text_file.close()
    for info in array_of_lines_file:
        info_split = info.split("=")
        if "Order_NR" == info_split[0]:
            order_nr = str(info_split[1][:-1])
        elif "Pair_ID" == info_split[0]:
            pair_id = str(info_split[1][:-1])
        elif "Letter_Odoo" == info_split[0]:
            letter = str(info_split[1][:-1])
        elif "Qa_Problem" == info_split[0]:
            qa_problem = str(info_split[1][:-1])
        elif "Which_Lenses" == info_split[0]:
            which_lenses = str(info_split[1][:-1])
            if which_lenses == "R":
                which_lenses = "right"
            elif which_lenses == "L":
                which_lenses = "left"
        elif "Mistake_Type" == info_split[0]:
            mistake_type = str(info_split[1][:-1])
        elif "Mistake_By" == info_split[0]:
            mistake_by = str(info_split[1][:-1])
        elif "Re_Order_Nr" == info_split[0]:
            re_order_nr = str(info_split[1][:-1])
        elif "Date" == info_split[0]:
            date = str(info_split[1][:-1])
        elif "Comment_Odoo" == info_split[0]:
            comment = str(info_split[1][:-1])

    import requests

    link_split = array_of_lines_file[0].split(" ")

    url = link_split[1].replace("\n", "") + "/reason_qa_problem"
    myobj = {"order_number":order_nr, "pair_id":pair_id, "letter":letter, "value":qa_problem}

    x = requests.post(url, data=myobj)
    print (x.text)

    url = link_split[1].replace("\n", "") + "/which_lens"
    myobj = {"order_number":order_nr, "pair_id":pair_id, "letter":letter, "value":which_lenses}

    x = requests.post(url, data=myobj)
    print (x.text)

    url = link_split[1].replace("\n", "") + "/mistake_type"
    myobj = {"order_number":order_nr, "pair_id":pair_id, "letter":letter, "value":mistake_type}

    x = requests.post(url, data=myobj)
    print(x.text)

    url = link_split[1].replace("\n", "") + "/mistake_by"
    myobj = {"order_number":order_nr, "pair_id":pair_id, "letter":letter, "value":mistake_by}

    x = requests.post(url, data=myobj)
    print(x.text)

    url = link_split[1].replace("\n", "") + "/re_order"
    myobj = {"order_number":order_nr, "pair_id":pair_id, "letter":letter, "value":re_order_nr}

    x = requests.post(url, data=myobj)
    print(x.text)

    url = link_split[1].replace("\n", "") + "/date_order_lab"
    myobj = {"order_number":order_nr, "pair_id":pair_id, "letter":letter, "value":date}

    x = requests.post(url, data=myobj)
    print(x.text)

    url = link_split[1].replace("\n", "") + "/comment"
    myobj = {"order_number":order_nr, "pair_id":pair_id, "letter":letter, "value":comment}

    x = requests.post(url, data=myobj)
    print(x.text)



def osticket_api_push():
    from pyosticket import OSTicketAPI

    osticket = OSTicketAPI(url="http://duuja.com/support/scp/tickets.php", api_key="06266BEDA7A182920746825F296067B4")

    ticket = osticket.ticket.get(ticket_number="KDE-000080", email="bulz.sebastian.work@gmail.com")

    print("Something")



def email_push ():
    import base64
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    creds = None

    if os.path.exists(sys.argv[0][:-34] + 'token_email.pickle'):
        with open(sys.argv[0][:-34] + 'token_email.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                sys.argv[0][:-34] + 'credentials.json', 'https://www.googleapis.com/auth/gmail.send')
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sys.argv[0][:-34] + 'token_email.pickle', 'wb') as token:
            pickle.dump(creds, token)


    service = build('gmail', 'v1', credentials=creds)

    text_information_file = open(sys.argv[0][:-34] + "Information.txt", "r")

    array_of_information = text_information_file.readlines()

    text_information_file.close()

    emailMsg = ""
    for i in range(1, len(array_of_information) - 1):
        emailMsg = emailMsg + array_of_information[i]

    mimeMessage = MIMEMultipart()

    email_address = array_of_information[len(array_of_information) - 1].replace("\n", "").split("=")

    mimeMessage['to'] = email_address[1]
    mimeMessage['subject'] = 'testsubject'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    draft = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()

def print_to_text_push():

    import subprocess as sp
    from tkinter import filedialog, Tk

    root = Tk()
    root.withdraw()
    programName = filedialog.askopenfilename(initialdir="/", title="Select the path to the notepad++ executable", filetypes = (("Executable file", "*.exe"), ("All Files", "*.*")))

    fileName = sys.argv[0][:-34] + "Information.txt"
    sp.Popen([programName, fileName])

def main():
    text_file = open(sys.argv[0][:-34] + "Information.txt")
    option = text_file.readline()
    text_file.close()

    if "Gsheets Warranty" in option:
        google_api_warranty_push()
    elif "Gsheets Complaints" in option:
        google_api_complaints_push()
    elif "Gsheets Defects" in option:
        google_api_defects_push()
    elif "Gsheets Refunds" in option:
        google_api_refunds_push()
    elif "Gsheets Stylists" in option:
        google_api_stylists_push()
    elif "Magento" in option:
        magento_api_push()
    elif "Odoo" in option:
        odoo_api_push()
    elif option == "Option=OSTicket\n":
        osticket_api_push()
    elif option == "Option=EMail\n":
        email_push()
    elif option == "Option=Print to Text\n":
        print_to_text_push()


    if option != "Option=Print to Text\n":
        os.remove(sys.argv[0][:-34] + "Information.txt")

if __name__ == '__main__':
    main()
