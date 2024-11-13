import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from decouple import Config, RepositoryEnv
from transformers import pipeline

import os, time
import pandas as pd
def text_validation(df_Lineas_NR, back_Office_PQR,gestor,asesor_remite,organizacion,estado_cf,fecha_gestion,Type,observacion,estado,motivo,cert_Number,attachments,state,attachments2,no_documents,content):
    texto=content
    preguntas_filtro =[
    #Pregunas filtro primera capa, externo 
    "Si el cliente especifica explicitamente la linea o las lineas que no reconoce, afectadas, bloqueadas, suspendida por fraude o que desea eliminar , escribelas sin espacios ni el '+57','57' y entre comas, de lo contrario escribe: PENDIENTE",#0
    "Si el cliente manifiesta algun tipo de error, escribe: VALIDAR MANUALMENTE, de lo contrario escribe: PENDIENTE"
    "Si el cliente manifiesta no reconoce una linea y solo da parte de la linea mas no ocmpleta como por ejemplo 302 o 310 etc, escribela, de lo contrario escribe: PENDIENTE ",
    "Si el cliente solicita textualmente la activación o reactivación de una linea bloqueada o suspendida por fraude, escribe: REACTIVACIÓN DE LINEA, de lo contrario escribe: PENDIENTE ",#1 
    "Si el cliente menciona de una compra no autorizada de un dispositivo movil o celular, escribe: COMPRA MOVIL NO AUTORIZADO, de lo contrario escribe: PENDIENTE",#2
    "Si el cliente menciona de una portabilidad no autorizada o reconocida, escribe: PORTABILIDAD NO RECONOCIDA, de lo contrario escribe: PENDIENTE",#3
    "Si el cliente solo menciona no reconocer o autorizar un plan adquirido Mas no una linea, escribe: UPGRADE NO RECONOCIDO, de lo contrario escribe: PENDIENTE ",#4
    #Preguntas puntuales del texto, interno
    "Si el cliente admite nunca haber adquirido servicios o activar ninguna linea o reconocer ningun plan de servicio con nosotros WOM, de lo contrario escribe: PENDIENTE",#5
    "Si el cliente menciona palabras como denuncia, fiscalia, sic, superintendencia, autoridades o Reposcicion simcard, escribe: VALIDAR MANUALMENTE, de lo contrario escribe: PENDIENTE",#6
    "Si el cliente menciona cosas como: Reporte negativo, centrales de riesgo, derecho de peticion, mora, datacenter, datacredito, escribe: NUNCA SOLICITO SERVICIO, de lo contrario escribe: PENDIENTE",#7
    "Si el cliente reconoce no haber adquirido ningun servicio WOM o con nosotros, escribe: NUNCA SOLICTO SERVICIO, de lo contrario escribe: PENDIENTE",#8
    "Si el cliente cuenta explicitamente la cantidad de lineas que no reconoce, escribe la cantidad, de lo contrario escribe: PENDIENTE",#9
    "Si el cliente solo menciona de una linea sin su consentimiento, escribe: 1, de lo contrario escribe: PENDIENTE",#10
    ]
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    
    #Primera capa
    if texto!="":
        #Segundo filtro
        respuesta = qa_pipeline({'question': preguntas_filtro[0], 'context': texto})
        result = respuesta['answer']
        if any(char.isalpha() for char in result):  # Si encuentra un número en la respuesta
            result="PENDIENTE"       # Se asume que se especificó una línea
        else:
            lineas = result.split(',')
            numero_de_lineas = len(lineas)
            for linea in numero_de_lineas:
                new_file= pd.DataFrame({'Back_Office_PQR':[back_Office_PQR],'Gestor':[gestor],'Asesor_remite':[asesor_remite],'Organizacion':[organizacion],'ESTADO_CF':[estado_cf],'FECHA_GESTION':[fecha_gestion],'LINEA':[linea],'Type':[Type],'Observacion':[observacion],'Estado':[estado],'Motivo':[motivo],'Cert_Number':[cert_Number],'Attachments':[attachments],'State':[state],'attachments2':[attachments2],'No_Documents':[no_documents]})
                df_Lineas_NR =pd.concat([df_Lineas_NR,new_file],ignore_index=True)
        if result == "PENDIENTE":
            result=""
            result = qa_pipeline({'question': preguntas_filtro[1], 'context': texto})
            if result =="PENDIENTE":
                result=""
                result = qa_pipeline({'question': preguntas_filtro[2], 'context': texto})
                if result =="PENDIENTE":
                    result=""
                    result = qa_pipeline({'question': preguntas_filtro[3], 'context': texto})
                    if result =="PENDIENTE":
                        result=""
                        result = qa_pipeline({'question': preguntas_filtro[4], 'context': texto})
                        if result =="PENDIENTE":
                            result=""
                            result = qa_pipeline({'question': preguntas_filtro[5], 'context': texto})
                            if result == "PENDIENTE":
                                result=""
                                result = qa_pipeline({'question': preguntas_filtro[6], 'context': texto})
                                if result =="PENDIENTE":
                                    result=""
                                    result = qa_pipeline({'question': preguntas_filtro[7], 'context': texto})
                                    if result =="PENDIENTE":
                                        result=""
                                        result = qa_pipeline({'question': preguntas_filtro[8], 'context': texto})
                                        if result =="PENDIENTE":
                                            result=""
                                            result = qa_pipeline({'question': preguntas_filtro[9], 'context': texto})
                                            if result =="PENDIENTE":
                                                result=""
                                                result = qa_pipeline({'question': preguntas_filtro[10], 'context': texto})
                                                if result =="PENDIENTE":
                                                    result ="VALIDAR MANUALMENTE"
    else:
        if adjuntos==True:
            result ="VALIDAR MANUALMENTE"
        else:
            result = "LINEA NO ESPECIFICADA"
    print("\n\nLa repuesta final es: ",result)
    return result
class Lineas_NR:
    def __init__(self, url, headless=True, driver_path=None):
        
        self.url = url
        self.headless = headless
        self.options = uc.ChromeOptions()
        
        # Configuración del navegador según el parámetro `headless`
        if self.headless:
            self.options.add_argument('--headless=new')  # Modo headless moderno
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        
        # Usar perfil de usuario para evitar bloqueos de autenticación
        self.options.add_argument(r"--user-data-dir=C:/Users/richard.vega/AppData/Local/Google/Chrome/User Data")
        self.options.add_argument(r'--profile-directory=Default')
        
        # Inicializar el navegador `undetected_chromedriver` con la ruta del driver si se proporciona
        self.driver = uc.Chrome(options=self.options, driver_executable_path=driver_path)

    def land_first_page(self):
        #env_file_path = os.path.join(os.path.dirname(__file__), 'entorno_virtual', '.env')
        #config = Config(RepositoryEnv(env_file_path))
        
        # Abrir la URL y realizar acciones
        print(f"Navegando a: {self.url}")
        self.driver.get(self.url)

        #username = config('EKIA_USERNAME')
        #password = config('EKIA_PASSWORD')

        # Esperar a que el elemento de carga desaparezca
        time.sleep(5)

        # Ejemplo: iniciar sesión en la página
        #self.driver.find_element(By.XPATH, '//*[@id="inputUserName"]').send_keys(username)
        #self.driver.find_element(By.XPATH, '//*[@id="inputPasswd"]').send_keys(password)
        
        # Esperar a que el botón esté clickeable y hacer clic en él
        login_button = WebDriverWait(self.driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="btnLogin"]'))
        )
        login_button.click()
       
        time.sleep(5)

    def information_case(self,cod_cases):
        columns = ['Back_Office_PQR','Gestor','Asesor_remite','Organizacion','ESTADO_CF','FECHA_GESTION','LINEA','Type','Observacion','Estado','Motivo','Cert_Number','Attachments','State','attachments2','No_Documents']
        df_Lineas_NR = pd.DataFrame(columns=columns)
        actions = ActionChains(self.driver)

        # Ingreso al menu TT Order Query
        Menu_button = WebDriverWait(self.driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="portalDropdown"]/span'))
        )
        Menu_button.click()
        Menu_button.click()
        Trouble_ticket_button= WebDriverWait(self.driver, 15).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="portalDropdown"]/ul/li[2]/a'))
        )
        Trouble_ticket_button.click()
        time.sleep(5)
        History_button= WebDriverWait(self.driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div/ul[1]/li[1]/span'))
        )
        History_button.click()
        TT_Order_button= WebDriverWait(self.driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="menuRecentListUl"]/li[1]/a/span/span'))
        )
        TT_Order_button.click()
        date_today = datetime.now()
        filter_date = date_today - timedelta(days=58)
        format_date=filter_date.strftime("%Y-%m-%d")
        date_filter_button= WebDriverWait(self.driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="PORTAL_DIV_MENU_2011"]/div/div[1]/form/div[1]/div[4]/div/div/div/input'))
        )
        actions.click(date_filter_button).click(date_filter_button).click(date_filter_button).perform()
        self.driver.find_element(By.XPATH, '//*[@id="PORTAL_DIV_MENU_2011"]/div/div[1]/form/div[1]/div[4]/div/div/div/input').send_keys(format_date)
        time.sleep(5)
        #Validacion de campos primera parte
        for element in cod_cases:
            back_Office_PQR=element
            gestor='bot.cfraude'
            asesor_remite=''
            organizacion=''
            estado_cf=''
            content=''
            fecha_gestion=datetime.now().strftime("%d/%m/%Y")
            linea=""
            Type=""
            observacion=""
            estado=""
            motivo="Lineas no reconocidas"
            cert_Number=""
            attachments=""
            state=""
            attachments2=""
            no_documents=""

            order_by_button= WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="orderCodeDiv"]/div/div/input'))
            )
            actions.click(order_by_button).click(order_by_button).perform()
            #Insertamos codigo
            self.driver.find_element(By.XPATH, '//*[@id="orderCodeDiv"]/div/div/input').send_keys(element)
            Query_button= WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="PORTAL_DIV_MENU_2011"]/div/div[1]/form/div[2]/div[3]/div/input[1]'))
            )
            Query_button.click()
            print("Cargando")
            time.sleep(10)
            
            Case_Code_button= WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/table/tbody/tr[2]/td[3]/div/button'))
            )
            actions.click(Case_Code_button).click(Case_Code_button).perform()
            time.sleep(5)
            
            print("Cargando2")
            time.sleep(15)
            # Extraccion de campos

            #Nombre Asesor
            nombre_asesor = self.driver.find_element(By.XPATH,'//*[@id="timeaxis"]/ul/li/div[2]/div[2]')
            nombre_asesor = nombre_asesor.text
            filtered_name= nombre_asesor.replace("By ", "").replace("(Staff)", "").strip()
            print("\nNombre Asesor: ",filtered_name)
            asesor_remite=filtered_name

            #Nombre Organizacion
            nombre_org = self.driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div[1]/form/div/div[6]/div/div/input')
            actions.click(nombre_org).click(nombre_org).click(nombre_org).perform()
            nombre_org_filtered = self.driver.execute_script("return window.getSelection().toString();")
            if nombre_org_filtered == "":
                nombre_org_filtered ="Back_Office_PQR"
            
            print("\nNombre Organizacion: ",nombre_org_filtered)
            organizacion=nombre_org_filtered

            #Cert_Number
            cert_number = self.driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div/div[1]/form/div[3]/form/div/div[7]/div/div/input')
            actions.click(cert_number).click(cert_number).perform()
            cert_number_filtered = self.driver.execute_script("return window.getSelection().toString();")
            print("\nCert Number: ",cert_number_filtered)
            cert_Number=cert_number_filtered

            #Contenido del texto
            content = self.driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div/div[1]/form/div[5]/div/div/div/div')
            content = content.text
            print("\nmensaje: \n",content)

            #Adjuntos si existen:
            try:
                adjuntos = self.driver.find_element(By.XPATH,'//*[@id="attachMentLable"]')
                adjuntos= True
            except:
                adjuntos= False
            attachments=adjuntos
            
            print("\nAdjuntos?: ",adjuntos)  

            linea = text_validation(df_Lineas_NR, back_Office_PQR,gestor,asesor_remite,organizacion,estado_cf,fecha_gestion,Type,observacion,estado,motivo,cert_Number,attachments,state,attachments2,no_documents,content)
            new_file= pd.DataFrame({'Back_Office_PQR':[back_Office_PQR],'Gestor':[gestor],'Asesor_remite':[asesor_remite],'Organizacion':[organizacion],'ESTADO_CF':[estado_cf],'FECHA_GESTION':[fecha_gestion],'LINEA':[linea],'Type':[Type],'Observacion':[observacion],'Estado':[estado],'Motivo':[motivo],'Cert_Number':[cert_Number],'Attachments':[attachments],'State':[state],'attachments2':[attachments2],'No_Documents':[no_documents]})
            df_Lineas_NR =pd.concat([df_Lineas_NR,new_file],ignore_index=True)

            Skip_button= WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/button/span'))
            )
            Skip_button.click()
            df_Lineas_NR.to_csv("Consolidado_Lineas_No_Reconocidas.csv", index=False)
        print("Datos guardados: ")
        pd.set_option('display.max_rows', None)  # Mostrar todas las filas
        pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
        pd.set_option('display.width', None)  # Ancho automático
        print(df_Lineas_NR)

    def __call__(self):
        # Define el comportamiento cuando se invoca el objeto
        self.land_first_page()

    def close(self):
        # Método para cerrar el navegador
        self.driver.quit()

    def termination_line(self,df,bool):
        x
        return x
# Especifica la ruta del chromedriver al crear el objeto
codes = [
'20241113_00029839399'
]
bot_LNR = Lineas_NR("https://ekia.wom.co/portal/#Overview", headless=False, driver_path="C:/Users/richard.vega/OneDrive - WOM Colombia/Documentos/SeleniumDriver/chromedriver")
bot_LNR.land_first_page()
bot_LNR.information_case(codes)
bot_LNR.close()
