import os
import smtplib

from mailer import Mailer
from spreadsheet_reader import CSVReader

subject = "Save the date - Convite Workshop SGSO"
body = "Boa tarde pessoal,<br/><br/>" \
       "É com grande satisfação que a RSE Consultoria os convida para participar do nosso Workshop \"SGSO: Práticas Essenciais para a Segurança Operacional no Setor de Petróleo e Gás\". O evento será realizado via Teams no dia 29 de fevereiro às 19h.<br/><br/>" \
       "Neste workshop, você terá a oportunidade de aprender e dominar as práticas essenciais para garantir a segurança operacional no setor de petróleo e gás. Durante o evento, exploraremos detalhadamente as resoluções da ANP n°43/2007 e n°5/2014.  Junte-se a nós e aprenda com renomados especialistas do setor de SEPRO.<br/><br/>" \
       "Clique no botão abaixo para garantir sua participação:<br/><br/>" \
        "<a href=\"https://us02web.zoom.us/webinar/register/7817086977656/WN_yalkaTTzREChhrRG5Y_f9A\" style=\"color: blue; font-weight: bold;\">Inscrever-se Agora</a><br/><br/><br/>" \
       "Não perca essa oportunidade única de adquirir conhecimentos e insights valiosos.<br/><br/>" \
       "Atenciosamente,<br/><br/>" \
       "Equipe RSE<br/><br/>" \
       "+55 71 9 9979-3008<br/>" \
       "+55 71 3506-8957<br/>" \
       "site: <a href=\"https://www.rse-global.com/en/\" style=\"color: blue; font-weight: bold;\">rse-global.com</a><br/><br/>"

sender_name = os.getenv('SENDER_NAME')
sender_email = os.getenv('SENDER_EMAIL')
password = os.getenv('SENDER_PASSWORD')

reader = CSVReader('files/email.csv', ['Email'])
recipients = reader.read_target()

mailer = Mailer(sender_name, sender_email, password)

print(f'Sending {len(recipients)} emails...')

failed = []
failed_exc = []
for index, recipient in enumerate(recipients):
    print(f'Sending {index} out of {len(recipients)} emails...')
    try:
        mailer.send_email([recipient], subject, body, ['attachments/Convite SGSO.pdf'])
    except smtplib.SMTPException as e:
        failed.append(recipient)
        failed_exc.append(e)


print('Execution completed:')
print(f'{len(recipients) - len(failed)} emails sent successfully')
print(f'Failed to send to {len(failed)} recipients\n')

print('Report:')
print(f'Failed recipients: {failed}')
print(f'Failed reasons: {failed_exc}')

mailer.close_smtp()

