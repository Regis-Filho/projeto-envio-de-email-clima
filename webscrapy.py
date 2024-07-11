import requests
from bs4 import BeautifulSoup


import smtplib
import email.message

user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

link = 'https://www.google.com/search?q=clima+morrinhos+ce'

response = requests.get(headers=user_agent,url=link)

html_site = BeautifulSoup(response.text,'html.parser')

#atual
temperatura_atual = html_site.find('span',id= "wob_tm").text

dia_semana_atual = html_site.find('div',id="wob_dts").text.split(',')[0]

condicao_tempo_atual = html_site.find('span',id="wob_dc").text

#proximos 3 dias
lista_3_proximos_dias = []

for dia in html_site.find_all('div', class_="wob_df")[1:4]:
    lista = []

    dia_seguinte = dia.find_all('div')[0]
    dia_semana_seguinte = dia_seguinte.get('aria-label')

    condicao_tempo_html = dia.find_all('div')[2]
    condicao_tempo_html = dia.find('img')
    condicao_tempo_seguinte = condicao_tempo_html.get('alt')


 
    temperatura_seguinte_1 = dia.find_all('span')[0].text
    temperatura_seguinte_2 = dia.find_all('span')[2].text
    temperatura_seguinte = f'{temperatura_seguinte_1}°/{temperatura_seguinte_2}°'


    lista.append(dia_semana_seguinte)
    lista.append(condicao_tempo_seguinte)
    lista.append(temperatura_seguinte)
  

    lista_3_proximos_dias.append(lista)

  
    



def enviar_email():  
    corpo_email = f"""

    <p>CLIMA ATUAL</p>
    <p>DIA SEMANA: {dia_semana_atual.upper()} <br /> TEMPERATURA: {temperatura_atual}° <br /> CONDIÇÃO CLIMATICA: {condicao_tempo_atual.upper()}</p>
    <p>CLIMA DOS PROXIMOS 3 DIAS</p>
    <p>DIA SEMANA: {lista_3_proximos_dias[0][0].upper()} <br /> TEMPERATURA: {lista_3_proximos_dias[0][-1]} <br /> CONDIÇÃO CLIMATICA: {lista_3_proximos_dias[0][1].upper()}</p>
    <p>DIA SEMANA: {lista_3_proximos_dias[1][0].upper()} <br /> TEMPERATURA :{lista_3_proximos_dias[1][-1]} <br /> CONDIÇÃO CLIMATICA :{lista_3_proximos_dias[1][1].upper()}</p>
    <p>DIA SEMANA: {lista_3_proximos_dias[-1][0].upper()} <br /> TEMPERATURA :{lista_3_proximos_dias[-1][-1]} <br /> CONDIÇÃO CLIMATICA: {lista_3_proximos_dias[-1][1].upper()}</p>

    """

    
    msg = email.message.Message()
    msg['Subject'] = "CLIMA ATUALIZADO"#assunto
    msg['From'] = ''#remetente
    msg['To'] = ''#destinario
    password = '' #senha
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Credenciais de login para enviar o e-mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

enviar_email()



