import pymssql
import pandas
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import json


scopes =  ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive'
          ]
key = json.dumps({
  "type": "service_account",
  "project_id": "minimarche",
  "private_key_id": "c5afd8c671262bb72c9f997a968a9d13f723aa51",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCtgsXZOwWgRP0u\nvim6Pspa+KaW8QtC7Rg6nUh7JQEo2jfA2jcGlO6c+FXdWQCcM6rOIUF0OoKIGxbN\n9oZ+ZSxU5V9OjZqi90FHp1BZfCweaYY3FLDMn8reyKxckGAmikELpQCoKbIGxFhU\n7EksXtuRvoftZ/cxq3F0+1TlU00JEdsgz/pwB7Q+GlVhenkU/fCPbAVhUkpf3II+\net4ZhKfWIOrXtc0mCUKlp3hHMQjhYHIeOErSjTRk68YsjuY4uyGTnpSrfRcaEF+n\nj6ehaGTLFMZ+0sTR7w8+0NXt6y8OF+1Fm74d9LxsT9qMGlRKWJUNjG89x/Wvgf+n\nJ9547y0dAgMBAAECggEAEs4soVmrR26SvkEwBpaNmgR/Ebb4UH2f9aJcW7RsBsB3\n8Hf2JMl5fxvPOplN3qAe8A5cqLs6sIO3GgWRGBvhDSZ7COmCDA2eTqTMqZYyte0b\n9dZRPyxGcZTwUWv4b9TmLdvpUVCLkf4v0Kx3Vc7GH2q2Er4E5aY+Or6OufgoTkYq\nJkrVpdpoAI/Xk4qLU9f5289G2Kc1TELGxpl9s9zTIUARvJrYgpu8sHBCLpz2zFkz\nD4InQI285cnVE+ujRPgPhwocWx+ltiOnDM87cTWGwh2Qp02n4gOTcuC6cYlVJqAK\ntEQ36OReqD1SH0pHPi3ebBmsoZ3y+pTqEM4hr2UiBQKBgQDtbDCU8bDyHSd5eS3b\nxjK4iSYQ0amZTYpbEP/cV+s9it5UvNYa1gMlr8u4S12aIJJuCGFr3OwBkU9uz4eI\nYY/+WLUpldpsZjwmvG1swreUUsWb3MbQksclGqZK5mrAAhK+y85nkl6wDr34PGoe\nb6ZQYms/5oSpLJq27o9WUnB7kwKBgQC7Fl3gOYjTGu93VsLMSpokPuOTUyTa5fzX\nqEyJ+pjpMSi+zqA5V56g3VD4I+80m4nPumU0tjvVrWq3rJTt3/yXNPEnI3mfNol3\nXG/RQOdhuoFO2+rlzl3jNHyGaBBbcS5BrLHniN969CaBKJG8hf7n75F2cIG8lH7Q\nSCP1DDECjwKBgFzX3fegu+0x8WnTNVeoHdWD7FrPYl8Mr3oFH8juqJMcZu0EG0XL\nQtfN8wBSmHvZGOnmZRJlBfVm+YT/qqRuYny3+8ATVaLmJ8eOD8xkKJ3b8GKO50BQ\n5Ydg8H6BtGT5apMp58Egv95hJXCZT3Yvev4cPoxyfJYbVzUJ/QtomYv5AoGBAICm\nLsOjjKzuFsFPjgCBRGGsRT3nrK5B/I4nkwpGoqOoREaBO7hywggIaEdaHoFke222\n1SVcMuUKrRnEuVyh68Xmh/XL9TRAgmLr05BnOzT+1TBvFaYVNIaqbv7VzHm06IQM\nxwFaI6MfBONIDH9A/TpsiPCTCQOucU20bdVyHrmNAoGAfuluRGvIXM+4r6Sg6l4T\nMDkOMyqe9tW3khv3bN0I3BL6LkC4dUMMfZEjS4ovOXzbZg+5twpArXSleAwwVmLq\nv95CXaOdQFSWaPZ6QFUcdRrmsD6bCU2bWrwqvgXSDYQ5xmqBBMLycQ8ZhvhrGDi1\nflYD+8bpxEaToTNoP/LmzFM=\n-----END PRIVATE KEY-----\n",
  "client_email": "minimarche@minimarche.iam.gserviceaccount.com",
  "client_id": "102852912942069385667",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/minimarche%40minimarche.iam.gserviceaccount.com"
})
service_account_info = json.loads(key)


creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scopes=scopes)

file = gspread.authorize(creds)
workbook = file.open("ibpmon_tables")

spreadsheetId = "1aAhC8LOswC_fPQssvoUNhvnCV2YygroEkEQiS-tRR64"  # Please set the Spreadsheet Id.

client = gspread.authorize(creds)
sh = client.open_by_key(spreadsheetId)
worksheet_list = sh.worksheets()

worksheet = sh.get_worksheet(0)
worksheet = sh.worksheet("table_name")
table = worksheet.col_values(1)

for c in table:
    table_name = c
    sql = "SELECT * FROM ibope.dbo." + table_name
    file_name = "C:\\projects\\sno\\data\\export\\" + str(table_name).lower() + ".parquet"
    print("Geração do arquivo: "+table_name)
    conn = pymssql.connect("(local)", "datalab", "datalab", "ibope")
    df = pandas.read_sql(sql, conn)
    df.to_parquet(file_name)