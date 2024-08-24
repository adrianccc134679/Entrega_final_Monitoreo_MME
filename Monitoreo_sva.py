from pickle import TRUE
from turtle import width
import pandas as pd
from io import StringIO
import re
from dash import Dash, dcc, html, Input, Output,dash_table,State
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
#import dash_auth

#################################################################
#################################################################
#################################################################
#                                                               #
#                        MONITOREO DE MME                       #
#            CREADO POR ADRIAN CASTILLO CASTRO CONDE            #
#                                                               #
#                                                               #
#################################################################
#################################################################
#################################################################



app = Dash('Monitoreo_MME')

"""auth = dash_auth.BasicAuth(
    app,
    {'password':'password',
     'admin':'12345'
     }
)"""
color_mapping = {
    'WARNING': 'lightblue',
    'MINOR': 'yellow',
    'MAJOR': 'orange',
    'CRITICAL': 'red'
}

df_alarm_desc = pd.DataFrame(['alarma', 'fecha', 'hora', 'severidad'])

#dise�o HTML
app.layout = dbc.Container(
    [   
        html.H1("MONITOREO MME", className="ms-3",style={
            'textAlign': 'center',
            'fontFamily': 'Arial',
            'fontSize': '40px',
            'fontWeight': 'bold'
        }),
        html.H3("Nodo:", className="ms-3"),
        dcc.Dropdown(
            id="region_input",
            options=["MME ROM", "MME SMO", "MME TGU", "MME SPS" ," MME ES", "MME VF", "MME POZ", "MME HER"],
            value=(""),
            clearable=True  ,
            style={"width": 400},
            multi=False
            ),

         dbc.Row([
            dbc.Col([
            html.Div(id="tabla_alarmas", children=[], className="col-md-6")
            ]),
            dbc.Col([
            #html.Div(id="tabla_eventos", children=[], className="col-md-6"),
            dcc.Graph(id="tabla_eventos")
            ]),
         ], 
            style={'display': 'flex','flex-wrap': 'wrap','justify-content': 'space-around','backgroundColor': '#f0f0f0','padding': '20px','border': '10px solid #ccc' }
         ),
         

         dbc.Row([
            html.Div(id="tabla_enodeb", children=[], className="col-md-12"),
            html.Div(id="tabla_diameter", children=[], className="col-md-12"),
         ],
            style={'display': 'flex', 'justify-content': 'space-between','justify-content': 'space-around','backgroundColor': '#f0f0f0','padding': '20px','border': '10px solid #ccc'}
         ),
         
        dbc.Row([
            html.Div(id="tabla_hw", children=[], className="col-md-12"),
            html.Div(id="tabla_links", children=[], className="col-md-12"),
         ],
            style={'display': 'flex', 'justify-content': 'space-between','justify-content': 'space-around','backgroundColor': '#f0f0f0','padding': '20px','border': '10px solid #ccc'}
         ),
         
         dbc.Row([
          #  html.H2("CPU", className="ms-3"),
            dcc.Graph(id="tabla_cpu"),
            
         ],
            style={'display': 'flex', 'justify-content': 'space-between','justify-content': 'space-around','backgroundColor': '#f0f0f0','padding': '20px','border': '10px solid #ccc'}
         ),
         #KPIS
         dbc.Row([
             
             html.Div(id="tabla_KPI_2G", children=[], className="col-md-12"),
             dbc.Col([
                      html.H3("Grafica KPI Tecnologia 2G", className="ms-3"),
                      dcc.Dropdown(
                        id="estadistico",
                        options=["Attach", "PDP-Act", "Intra-SGSN_RAU", "Inter-SGSN_RAU" ,"Paging", "Cut-off"],
                        value=("Attach"),
                        clearable=True  ,
                        style={"width": 800},
                        multi=True
                      ),
                      dcc.Graph(id="Graph_kpi_2g"),
                      ],
                 )
           
            
         ],
            style={'display': 'flex', 'justify-content': 'space-between','backgroundColor': '#f0f0f0','padding': '20px','border': '10px solid #ccc'}
         ),
                 dbc.Row([   
                     html.Div(id="tabla_KPI_3G", children=[], className="col-md-12"),
                     dbc.Col([
                            html.H3("Grafica KPI Tecnologia 3G", className="ms-3"),
                            dcc.Dropdown(
                                id="estadistico_3G",
                                options=['Attach', 'PDP-Act','Intra-SGSN_RAU', 'Inter-SGSN_RAU', 'Paging', 'Cut-off', 'RAB-Est', 'Ser-Req'],
                                value=("Attach"),
                                clearable=True  ,
                                style={"width": 800},
                                multi=True
                              ),
                              dcc.Graph(id="Graph_kpi_3g"),
                              ],
                         )
        
            
         ],
            style={'display': 'flex', 'justify-content': 'space-between','justify-content': 'space-around','backgroundColor': '#f0f0f0','padding': '20px','border': '10px solid #ccc'}
         ),
         
         dbc.Row([   
             html.Div(id="tabla_KPI_4G", children=[], className="col-md-12"),
             dbc.Col([
                        html.H3("Grafica KPI Tecnologia 4G", className="ms-3"),
                        dcc.Dropdown(
                                id="estadistico_4G",
                                options=['Attach', 'X2_Handover','S1_Handover', 'Paging', 'Bearer', 'Ser-Req', 'Intra-MME_TAU'],
                                value=("Attach"),
                                clearable=True  ,
                                style={"width": 800},
                                multi=True
                              ),
                              dcc.Graph(id="Graph_kpi_4g"),
                              ],
                         )
        
            
         ],
            style={'display': 'flex', 'justify-content': 'space-between','justify-content': 'space-around','backgroundColor': '#f0f0f0','padding': '20px','border': '10px solid #ccc'}
         ),
         


    ],
    fluid=True,
    style={'backgroundColor': '#C0C0C0'}
)

#---------------callbcks-------------------------
#Tabla de alarmas
@app.callback(
    Output("tabla_alarmas", "children"),    
    Input(component_id='region_input', component_property='value'),
)
def update_tabla_alarmas(region_input):
    nombre_archivo=region_input+".txt"
    return Alarmas(nombre_archivo)
#Tabla de eventos
@app.callback(
    Output("tabla_eventos", "figure"),    
    Input(component_id='region_input', component_property='value'),
)
def update_tabla_eventos(region_input):
    nombre_archivo=region_input+".txt"
    df_events=Eventos(nombre_archivo)
    fig = px.histogram(df_events,x='evento', y='ocurrencia',text_auto=True)
    fig = go.Figure(fig)
    fig.update_layout(
        xaxis_title="<b>Eventos</b>",  # Personaliza la leyenda del eje X
        yaxis_title="<b>Ocurrencia</b>",  # Personaliza la leyenda del eje Y
        width=700,
        height=600,
        title="eventos"
    )
    return fig
"""

def update_tabla_events(region_input):
    nombre_archivo=region_input+".txt"
    return Eventos(nombre_archivo)
"""

        #Tabla de enodeb
@app.callback(
    Output("tabla_enodeb", "children"),    
    Input(component_id='region_input', component_property='value'),
   
)
def update_tabla_enodeb(region_input):
    nombre_archivo=region_input+".txt"
    return enodeb(nombre_archivo)
#Tabla de DIAMETER
@app.callback(
    Output("tabla_diameter", "children"),    
    Input(component_id='region_input', component_property='value'),
   
)
def update_tabla_diameter(region_input):
    nombre_archivo=region_input+".txt"
    return diameter(nombre_archivo)

#____________________________________________
 #Tabla de HW
@app.callback(
    Output("tabla_hw", "children"),    
    Input(component_id='region_input', component_property='value'),
   
)
def update_tabla_enodeb(region_input):
    nombre_archivo=region_input+".txt"
    return hw(nombre_archivo)
#Tabla de DIAMETER
@app.callback(
    Output("tabla_links", "children"),    
    Input(component_id='region_input', component_property='value'),
   
)
def update_tabla_diameter(region_input):
    nombre_archivo=region_input+".txt"
    return ip(nombre_archivo)
#_________________________________________________

#Grafica cpu
@app.callback(
    Output("tabla_cpu", "figure"),    
    Input(component_id='region_input', component_property='value'),
   
)
def update_tabla_cpu(region_input):
    nombre_archivo=region_input+".txt"
    df_cpu=cpu(nombre_archivo)
    fig = px.histogram(df_cpu,x='AP', y='Porcentaje', range_y=[0, 100])
    fig = go.Figure(fig)
    fig.update_layout(
        xaxis_title="<b>blade</b>",  # Personaliza la leyenda del eje X
        yaxis_title="<b>Porcentaje de Uso cpu(%)</b>",  # Personaliza la leyenda del eje Y
        width=1200,
        height=500,
        title="CPU"
    )
    return fig
#Tabla de kpis 2G
@app.callback(
    Output("tabla_KPI_2G", "children"),    
    Input(component_id='region_input', component_property='value'),
   
)
def update_tabla_kpi2g(region_input):
    nombre_archivo=region_input+".txt"
    t_kpi_2g=tabla_kpi_2G(nombre_archivo)
    return t_kpi_2g
#Tabla de kpis 3G
@app.callback(
    Output("tabla_KPI_3G", "children"),    
    Input(component_id='region_input', component_property='value'),
   
)
def update_tabla_kpi3g(region_input):
    nombre_archivo=region_input+".txt"
    t_kpi_3g=tabla_kpi_3G(nombre_archivo)
    return t_kpi_3g
#Tabla de kpis 4G
@app.callback(
    Output("tabla_KPI_4G", "children"),    
    Input(component_id='region_input', component_property='value'),
   
)
def update_tabla_kpi4g(region_input):
    nombre_archivo=region_input+".txt"
    t_kpi_4g=tabla_kpi_4G(nombre_archivo)
    return t_kpi_4g
#GRAFICAde kpis 2G
@app.callback(
    Output("Graph_kpi_2g", "figure"),    
    Input(component_id='region_input', component_property='value'),
    Input(component_id='estadistico', component_property='value'),
   
)
def update_graph_kpi2g(region_input,estadistico):
    nombre_archivo=region_input+".txt"
    kpi_2g_graph=kpi_2G(nombre_archivo)
    fig=create_graph(kpi_2g_graph,estadistico)
    return fig
#GRAFICAde kpis 3G
@app.callback(
    Output("Graph_kpi_3g", "figure"),    
    Input(component_id='region_input', component_property='value'),
    Input(component_id='estadistico_3G', component_property='value'),
   
)
def update_graph_kpi3g(region_input,estadistico_3G):
    nombre_archivo=region_input+".txt"
    kpi_3g_graph=kpi_3G(nombre_archivo)
    fig=create_graph(kpi_3g_graph,estadistico_3G)
    return fig

#GRAFICAde kpis 4G
@app.callback(
    Output("Graph_kpi_4g", "figure"),    
    Input(component_id='region_input', component_property='value'),
    Input(component_id='estadistico_4G', component_property='value'),
   
)
def update_graph_kpi4g(region_input,estadistico_4G):
    nombre_archivo=region_input+".txt"
    kpi_4g_graph=kpi_4G(nombre_archivo)
    fig=create_graph(kpi_4g_graph,estadistico_4G)
    return fig



#funcion que crea las graficas de kpis 2g-3g-4g
def create_graph(df_kpi,estadistico):
    df_kpi['datetime'] = df_kpi['Day'].astype(str) + ' ' + df_kpi['Time'].astype(str)
    fig = px.line(df_kpi, x='datetime', y=estadistico)
    fig.update_layout(
        xaxis_title="<b>Time</b>",  # Personaliza la leyenda del eje X
        yaxis_title="<b>% Falla</b>",  # Personaliza la leyenda del eje Y
        xaxis=dict(autorange="reversed"),
        width=800,
        height=600,
        title="kpi"
    )
    return fig
#funcion que determina las alarmas y crea un data frame con las alarmas actuales
def Alarmas(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            alarma_inicio = contenido.find ("alarmas_inicio")+15
            alarma_fin = contenido.find("alarmas_fin")-1
            #print("indice_inicio: "+str(alarma_inicio)) 
            #print("indice_fin: "+str(alarma_fin) )
            texto_alarma = contenido[alarma_inicio:alarma_fin]
            #texto_alarma=[linea for linea in texto_alarma if not all(c == '-' for c in linea.strip())]
            texto_limpio = "\n".join(line.lstrip() for line in texto_alarma.splitlines())
            texto_limpio== '\n'.join(texto_limpio.split('\n')[1:-1])
            texto_limpio=texto_limpio.replace('fmAlarmId time faultId eventType', '')
            texto_limpio=texto_limpio.replace('-', '')
            df_alarm = pd.read_csv(StringIO(texto_limpio), sep=' ', header=None, engine='python')
            df_alarm=pd.DataFrame(df_alarm)  
            df_alarm=df_alarm.iloc[1:].reset_index(drop=True)
            df_alarm.columns = ['alarma', 'fecha', 'hora', 'severidad']
            print(df_alarm)
            
    #Etapa de conteo de alarmas
            conteo_warning = 0
            conteo_major = 0
            conteo_minor = 0
            conteo_critical = 0
            # Recorrer cada fila del dataframe
            for index, row in df_alarm.iterrows():
                # Obtener el valor de la columna 3 (asumiendo que es la columna de alarmas)
                valor_alarma = row[3]
                # Contar las apariciones de cada palabra clave
                if valor_alarma == "WARNING":
                  conteo_warning += 1
                elif valor_alarma == "MAJOR":
                  conteo_major += 1
                elif valor_alarma == "MINOR":
                  conteo_minor += 1
                elif valor_alarma == "CRITICAL":
                  conteo_critical += 1
                else:
                    conteo_warning += 1
        
         
            Columna1=['WARNING', 'MINOR', 'MAJOR', 'CRITICAL']
            Columna2=[conteo_warning,conteo_minor   ,conteo_major,conteo_critical] 
            df_total = pd.DataFrame({'severidad':Columna1, 'ocurrencia':Columna2})

            #print(df_total)
            #df_alarm.to_csv("dataframe_alarmas.csv")

            #regreso de la alarma es un segmento de codigo que se injecta sobre el layout con las tablas de alarmas creadas
            return  dbc.Col(dbc.Card([
                        html.H2("ALARMAS", className="ms-3"),
                
                        dash_table.DataTable(
                            data=df_total.to_dict('records'),
                            columns=[
                                {'name': str(i), 'id': str(i) }  
                                
                                for i in df_total.columns
                            ],style_cell={
                                "textAlign": "center",
                                "font-family": "sans-serif",
                                "fontSize": 14,
                                        },
                          
                        ),
                        
			            dash_table.DataTable
                        (
                            data=df_alarm.to_dict("records"),
                            columns=[{"name": str(c), "id": str(c)} for c in df_alarm.columns],
                            #columns=[{"name": i, "id": i} for i in ['alarma', 'fecha', 'hora', 'severidad']],                            
                            style_table={"height": 600,"width": "600px"},
                            style_cell={
                                "textAlign": "center",
                                "font-family": "sans-serif",
                                "fontSize": 14,
                                        }
                        ),
                        
                ],  
                style={'max-width': '1200px','margin': '10px','max-height': '600px','overflow-y': 'auto' }  ,           
                className="m-3 px-2",
            ))
         
    except FileNotFoundError:
        print("Error al leer alarmas")

def Eventos(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            #print("Contenido del archivo:")
            #print(contenido)
            eventos_inicio = contenido.find ("eventos_inicio")+14
            eventos_fin = contenido.find("eventos_fin")
            #print("indice_inicio: " +str(eventos_inicio)) 
            #print("indice_fin: "+str(eventos_fin))
            texto_eventos = contenido[eventos_inicio:eventos_fin] 
            texto_limpio_evento = "\n".join(line.lstrip() for line in texto_eventos.splitlines())
            #print(texto_limpio_evento)
            #texto_limpio_evento= StringIO(texto_limpio_evento)  
            df_event = pd.read_csv(StringIO(texto_limpio_evento),sep=r'\s', header=None, engine='python')
            #print(df_event)
            df_event = pd.DataFrame(df_event)
            #print(df_event)
            df_event.columns= ['ocurrencia', 'evento']
            df_hist = df_event[['evento', 'ocurrencia']]
            #print(df_hist)
            #dato=df_event.iloc[0, 1]
            #print(dato)
            #df_event.to_csv("dataframe_alarmas.csv")
            #print (df_event)
            #df_hist['ocurrencia'] = df_hist['ocurrencia'].str.strip()
            df_hist['ocurrencia'] = df_hist['ocurrencia'].astype(int)
            #df_hist['evento'] = df_hist['evento'].str.strip()
            df_hist['evento'] = df_hist['evento'].astype(str)
            print(df_hist)
            return df_hist
    except FileNotFoundError:
            print("Error al leer eventos")

"""
            return  dbc.Col(dbc.Card([  
                        html.H2("EVENTOS", className="ms-3"),
			            dash_table.DataTable
                        (
                            data=df_event.to_dict("records"),
                            columns=[{"name": str(c), "id": str(c)} for c in df_event.columns],
                            #columns=[{"name": i, "id": i} for i in ['alarma', 'fecha', 'hora', 'severidad']],                            
                            style_table={"height": 500,"width": "600px"},
                            style_cell={
                                "textAlign": "center",
                                "font-family": "sans-serif",
                                "fontSize": 14,
                                        }
                        )            
                ],
                #style={'min-width': '200px','max-width': '400px','margin': '10px'},
                style={'max-width': '1200px','margin': '10px','max-height': '600px','overflow-y': 'auto'},
                className="m-3 px-2",
            ))
            """
   

def enodeb(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            enodeb_inicio = contenido.find ("enodeb_inicio")+14
            enodeb_fin = contenido.find("enodeb_fin")
            #print("indice_inicio: " +str(enodeb_inicio)) 
            #print("indice_fin: "+str(enodeb_fin))
            texto_enodeb= contenido[enodeb_inicio:enodeb_fin] 
            texto_limpio_enodeb = texto_enodeb.split('\n')
            texto_limpio_enodeb.pop(1)
            texto_limpio_enodeb = '\n'.join(texto_limpio_enodeb)  # une las lineas
            texto_limpio_enodeb=texto_limpio_enodeb.replace('|', ' ')
            texto_limpio_enodeb = re.sub(r'-geni\s+', '', texto_limpio_enodeb)

            #print(texto_limpio_enodeb)
            texto_limpio_enodeb= StringIO(texto_limpio_enodeb)    
            df_enodeb = pd.read_csv(texto_limpio_enodeb, delim_whitespace=True)
            
            df_enodeb=df_enodeb.iloc[:, :-5]
            #print(df_enodeb)
            #print(df.iloc[:,2:6])
            #df_enodeb.to_csv("dataframe_alarmas.csv")
            return  dbc.Card([  
                        html.H2("EnodeB", className="ms-3"),
			            dash_table.DataTable
                        (
                            data=df_enodeb.to_dict("records"),
                            columns=[{"name": str(c), "id": str(c)} for c in df_enodeb.columns],
                            style_table={"height": 600,"width": 600},
                            style_cell={
                                "textAlign": "center",
                                "font-family": "sans-serif",
                                "fontSize": 14,
                                        }
                        )            
                ],
                style={ "display": "inline-block",'max-width': '1200px','margin': '10px','max-height': '600px','overflow-y': 'auto'},
                className="m-3 px-2",
            )
    except FileNotFoundError:
        print("Error al leer enodeb")

def diameter(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            diameter_inicio = contenido.find ("diameter_inicio")+16
            diameter_fin = contenido.find("diameter_fin")-1
            #print("indice_inicio: " +str(diameter_inicio)) 
            #print("indice_fin: "+str(diameter_fin))
            texto_enodeb= contenido[diameter_inicio:diameter_fin] 
            texto_limpio_diameter = texto_enodeb.split('\n')
            texto_limpio_diameter.pop(1)
            texto_limpio_diameter = '\n'.join(texto_limpio_diameter)  # une las lineas
            texto_limpio_diameter=texto_limpio_diameter.replace('|', ' ')
            texto_limpio_diameter = re.sub(r' -ip\s+', '', texto_limpio_diameter)

            #print(texto_limpio_diameter)
            texto_limpio_diameter= StringIO(texto_limpio_diameter)    
            df_diameter = pd.read_csv(texto_limpio_diameter, delim_whitespace=True)
            df_diameter=df_diameter.iloc[:, 2:]
            #print(df_diameter)
            #print(df.iloc[:,2:6])
            #df_diameter.to_csv("dataframe_alarmas.csv")
            return  dbc.Card([  
                        html.H2("DIAMETER", className="ms-3"),
			            dash_table.DataTable
                        (
                            data=df_diameter.to_dict("records"),
                            columns=[{"name": str(c), "id": str(c)} for c in df_diameter.columns],
                            style_table={"height": 600,"width": 600},
                            style_cell={
                                "textAlign": "center",
                                "font-family": "sans-serif",
                                "fontSize": 14,
                                        }
                        )            
                ],
                style={"display": "inline-block",'max-width': '1200px','margin': '10px','max-height': '600px','overflow-y': 'auto'},
                className="m-3 px-2",
            )
    except FileNotFoundError:
        print("Error al leer diameter")
                
def cpu(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            diameter_inicio = contenido.find ("CPU_inicio")+10
            diameter_fin = contenido.find("CPU_fin")-1
            #print("indice_inicio: " +str(diameter_inicio)) 
            #print("indice_fin: "+str(diameter_fin))
            texto_CPU= contenido[diameter_inicio:diameter_fin]         
            #print(texto_CPU)
            texto_APin=texto_CPU.find("AP:")+3
            texto_APfin=texto_CPU.find("DP:")
            texto_AP=texto_CPU[texto_APin:texto_APfin] 
            #print(texto_AP)
            lineas = texto_AP.strip().split('\n')
            lineas = [line.split(':') for line in lineas if ':' in line]
            df = pd.DataFrame(lineas, columns=['AP', 'Porcentaje'])
            df['AP'] = df['AP'].str.strip()
            df['AP'] = df['AP'].astype(str)
            df['Porcentaje'] = df['Porcentaje'].str.strip()
            df['Porcentaje'] = df['Porcentaje'].astype(int)
            #print("----------------------------------")
            #print(df)
            return df



    except FileNotFoundError:
        print("Error al leer cpu")
            
def hw(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            HW_inicio = contenido.find ("HW_inicio")+9
            HW_fin = contenido.find("HW_fin")
            #print("indice_inicio: " +str(HW_inicio)) 
            #print("indice_fin: "+str(HW_fin))
            texto_HW= contenido[HW_inicio:HW_fin-174] 
            texto_limpio_HW=texto_HW.strip().split('\n')
            #texto_limpio_HW=[linea for linea in texto_limpio_HW if not all(c == '-' for c in linea.strip())]
            texto_limpio_HW='\n'.join(texto_limpio_HW)
            texto_limpio_HW=texto_limpio_HW.replace('eq Eq Class Type AdminState OperState PowerState Revision', '')            
            texto_limpio_HW=texto_limpio_HW.replace('---------------------------------------------------------------------------------------------------------------------------------------', '')
            texto_limpio_HW = texto_limpio_HW.lstrip()
            #print(texto_limpio_HW)
            df_HW = pd.read_csv(StringIO(texto_limpio_HW), delim_whitespace=True)
            #sep=' ', engine='python'
            df_HW.columns = ['eq','equipo', 'EQ', 'Class_Type', 'AdminState','OperState','PowerState', 'Revision']
            #df_hw = pd.DataFrame(df_hw)
            #df_hw.to_excel('archivo_HW.xlsx', index=False)            
            #df_hw.to_csv("dataframe_alarmas.csv")
            #print(df_HW)
            return dbc.Card([  
                        html.H2("Hardware status", className="ms-3"),
			            dash_table.DataTable
                        (
                            data=df_HW.to_dict("records"),
                            columns=[{"name": str(c), "id": str(c)} for c in df_HW.columns],
                            style_table={"height": 600,"width": 600},
                            style_cell={
                                "textAlign": "center",
                                "font-family": "sans-serif",
                                "fontSize": 14,
                                        }
                        )            
                ],
                style={"display": "inline-block",'max-width': '1200px','margin': '10px','max-height': '600px','overflow-y': 'auto'},
                className="m-3 px-2",
            )
           

    except FileNotFoundError:
        print("Error al leer hw")

def ip(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            ip_inicio = contenido.find ("ip_inicio")+9
            ip_fin = contenido.find("ip_fin")
            #print("indice_inicio: " +str(HW_inicio)) 
            #print("indice_fin: "+str(HW_fin))
            texto_ip= contenido[ip_inicio:ip_fin] 
            texto_limpio_ip=texto_ip.strip().split('\n')
            texto_limpio_ip=[linea for linea in texto_limpio_ip if not all(c == '-' for c in linea.strip())]
            texto_limpio_ip='\n'.join(texto_limpio_ip)
            texto_limpio_ip=texto_limpio_ip.replace('Ip Interfaces STATUS', '')
            
            
            #print(texto_limpio_ip)
            df_ip = pd.read_csv(StringIO(texto_limpio_ip), delim_whitespace=True)
            df_ip.columns = ['nombre', 'Net', 'Eq', 'IP_Address','CPU', 'Traf', 'Tx', 'Rx','Tx_Error','Rx_error']
            print(df_ip)
            return dbc.Card([  
                        html.H2("Interface status", className="ms-3"),
			            dash_table.DataTable
                        (
                            data=df_ip.to_dict("records"),
                            columns=[{"name": str(c), "id": str(c)} for c in df_ip.columns],
                            style_table={"height": 600,"width": 600},
                            style_cell={
                                "textAlign": "center",
                                "font-family": "sans-serif",
                                "fontSize": 14,
                                        }
                        )            
                ],
                style={"display": "inline-block",'max-width': '1200px','margin': '10px','max-height': '600px','overflow-y': 'auto'},
                className="m-3 px-2",
            )

    except FileNotFoundError:
        print("Error al leer hw")
def kpi_alarma(kpi_df):
        columnas_a_calcular = kpi_df.iloc[:, 2:]
        columnas_a_calcular.mean()
        #print("------------------kpi--------------")
        #print(columnas_a_calcular)
        alarmas = []

        for columna in columnas_a_calcular.columns:            
            media = columnas_a_calcular[columna].mean()
            var= columnas_a_calcular[columna].std()
            if 15 < media < 50:
              severidad = "Menor"
              alarmas.append({'columna': columna, 'alarma': "threshold fuera de meta",'severidad': severidad})
            elif 50 < media < 70:
              severidad = "Major"
              alarmas.append({'columna': columna, 'alarma': "threshold fuera de meta",'severidad': severidad})
            elif 70 < media:
              severidad = "Critical"
              alarmas.append({'columna': columna, 'alarma': "threshold fuera de meta",'severidad': severidad})
            
            for filas, s in columnas_a_calcular.iterrows():
                threshold=3
                valor=columnas_a_calcular.loc[filas, columna]
                if ((valor-media)>(threshold * var)):
                    severidad = "Major"
                    alarmas.append({'columna': columna, 'alarma': "Aumento inesperado",'severidad': severidad})
                    
        alarmas=pd.DataFrame(alarmas)    
        #print(alarmas)
        return alarmas
        
       



def kpi_2G(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            kpi_inicio = contenido.find ("kpi_inicio")+10
            kpi_fin = contenido.find("kpi_fin")
            #print("indice_inicio: " +str(kpi_inicio)) 
            #print("indice_fin: "+str(kpi_fin))
            texto_kpi= contenido[kpi_inicio:kpi_fin] 
            #print(texto_kpi)
            texto_limpio_kpi_2G = texto_kpi.split('\n')
            texto_limpio_kpi_3G = texto_kpi.split('\n')
            texto_limpio_kpi_4G = texto_kpi.split('\n')
            
            #kpi 2G
            for i in range(18): 
                texto_limpio_kpi_2G.pop(0)
            for j in range(1228): 
                texto_limpio_kpi_2G.pop()
                
            texto_limpio_kpi_2G = [linea for linea in texto_limpio_kpi_2G if "=" not in linea] 
            
            #texto_limpio_kpi_2G = [linea for linea in texto_limpio_kpi_2G if "-" not in linea]  
            texto_limpio_kpi_2G='\n'.join(texto_limpio_kpi_2G)
            texto_limpio_kpi_2G=texto_limpio_kpi_2G.replace('Intra-SGSN RAU', 'Intra-SGSN_RAU')
            texto_limpio_kpi_2G=texto_limpio_kpi_2G.replace('Inter-SGSN RAU', 'Inter-SGSN_RAU')
            texto_limpio_kpi_2G=texto_limpio_kpi_2G.replace('%', '')
            #print(texto_limpio_kpi_2G)
            df2g = pd.read_csv(StringIO(texto_limpio_kpi_2G),  delim_whitespace=True)
            df2g.columns = ['Day', 'Time', 'Attach', 'PDP-Act','Intra-SGSN_RAU', 'Inter-SGSN_RAU', 'Paging', 'Cut-off']
            return df2g
    except FileNotFoundError:
        print("Error al leer kpis")            

def tabla_kpi_2G(nombre_archivo):
    try:           
        df2g=kpi_2G(nombre_archivo)
        alarmas=kpi_alarma(df2g)
        #print("-------------------------------------")
        #print(alarmas)
        return dbc.Col(dbc.Card([
                    html.H2("KPI Tecnologia 2G", className="ms-3"),
            
                    dash_table.DataTable(
                        data=alarmas.to_dict('records'),
                        columns=[
                            {'name': str(i), 'id': str(i) }  
                            
                            for i in alarmas.columns
                        ],style_cell={
                            "textAlign": "center",
                            "font-family": "sans-serif",
                            "fontSize": 14,
                                    }
                        
                    ),
                    
		            dash_table.DataTable
                    (
                        data=df2g.to_dict("records"),
                        columns=[{"name": str(c), "id": str(c)} for c in df2g.columns],
                        #columns=[{"name": i, "id": i} for i in ['alarma', 'fecha', 'hora', 'severidad']],                            
                        style_table={"height": 600,"width": 600},
                        style_cell={
                            "textAlign": "center",
                            "font-family": "sans-serif",
                            "fontSize": 14,
                                    }
                    ),
                    
            ],  
            style={'margin': '10px','max-height': '600px','overflow-y': 'auto' }  ,           
            className="m-3 px-2",
        ))
        
    except FileNotFoundError:
        print("Error al leer kpis")

def kpi_3G(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            kpi_inicio = contenido.find ("kpi_inicio")+10
            kpi_fin = contenido.find("kpi_fin")
            #print("indice_inicio: " +str(kpi_inicio)) 
            #print("indice_fin: "+str(kpi_fin))
            texto_kpi= contenido[kpi_inicio:kpi_fin] 
            #print(texto_kpi)
            texto_limpio_kpi_2G = texto_kpi.split('\n')
            texto_limpio_kpi_3G = texto_kpi.split('\n')
            texto_limpio_kpi_4G = texto_kpi.split('\n')            
            #kpi 3G
            for i in range(87): 
                texto_limpio_kpi_3G.pop(0)
            for i in range(1160): 
                texto_limpio_kpi_3G.pop()
               
            texto_limpio_kpi_3G = [linea for linea in texto_limpio_kpi_3G if "=" not in linea] 
            texto_limpio_kpi_3G='\n'.join(texto_limpio_kpi_3G)
            texto_limpio_kpi_3G=texto_limpio_kpi_3G.replace('Intra-SGSN RAU', 'Intra-SGSN_RAU')
            texto_limpio_kpi_3G=texto_limpio_kpi_3G.replace('Inter-SGSN RAU', 'Inter-SGSN_RAU')
            texto_limpio_kpi_3G=texto_limpio_kpi_3G.replace('%', '')
            #print (texto_limpio_kpi_3G) 
            df3g = pd.read_csv(StringIO(texto_limpio_kpi_3G),  delim_whitespace=True)
            df3g.columns = ['Day', 'Time', 'Attach', 'PDP-Act','Intra-SGSN_RAU', 'Inter-SGSN_RAU', 'Paging', 'Cut-off', 'RAB-Est', 'Ser-Req']
            #print(df3g)
            return df3g
    except FileNotFoundError:
        print("Error al leer kpis")
def tabla_kpi_3G(nombre_archivo):
    try:
        df3g=kpi_3G(nombre_archivo)
        alarmas=kpi_alarma(df3g)
        #print("-------------------------------------")
        #print(alarmas)
        return dbc.Col(dbc.Card([
                    html.H2("KPI Tecnologia 3G", className="ms-3"),
            
                    dash_table.DataTable(
                        data=alarmas.to_dict('records'),
                        columns=[
                            {'name': str(i), 'id': str(i) }  
                            
                            for i in alarmas.columns
                        ],style_cell={
                            "textAlign": "center",
                            "font-family": "sans-serif",
                            "fontSize": 14,
                                    }
                        
                    ),
                    
                    dash_table.DataTable
                    (
                        data=df3g.to_dict("records"),
                        columns=[{"name": str(c), "id": str(c)} for c in df3g.columns],
                        #columns=[{"name": i, "id": i} for i in ['alarma', 'fecha', 'hora', 'severidad']],                            
                        style_table={"height": 600,"width": 600},
                        style_cell={
                            "textAlign": "center",
                            "font-family": "sans-serif",
                            "fontSize": 14,
                                    }
                    ),
                    
            ],  
            style={'margin': '10px','max-height': '600px','overflow-y': 'auto' }  ,           
            className="m-3 px-2",
        ))
    except FileNotFoundError:
        print("Error al leer kpis")

def kpi_4G(nombre_archivo):
    try:
        with open(nombre_archivo, encoding="utf8") as archivo:
            contenido = archivo.read()
            kpi_inicio = contenido.find ("kpi_inicio")+10
            kpi_fin = contenido.find("kpi_fin")
            #print("indice_inicio: " +str(kpi_inicio)) 
            #print("indice_fin: "+str(kpi_fin))
            texto_kpi= contenido[kpi_inicio:kpi_fin] 
            #print(texto_kpi)
            texto_limpio_kpi_2G = texto_kpi.split('\n')
            texto_limpio_kpi_3G = texto_kpi.split('\n')
            texto_limpio_kpi_4G = texto_kpi.split('\n')
            #kpi 4G
            for i in range(155): 
                texto_limpio_kpi_4G.pop(0)
            for i in range(1092): 
                texto_limpio_kpi_4G.pop()
             
            texto_limpio_kpi_4G = [linea for linea in texto_limpio_kpi_4G if "=" not in linea] 
            texto_limpio_kpi_4G='\n'.join(texto_limpio_kpi_4G)
            texto_limpio_kpi_4G=texto_limpio_kpi_4G.replace('X2 Handover', 'X2_Handover')
            texto_limpio_kpi_4G=texto_limpio_kpi_4G.replace('S1 Handover', 'S1_Handover')
            texto_limpio_kpi_4G=texto_limpio_kpi_4G.replace('Intra-MME TAU', 'Intra-MME_TAU')
            texto_limpio_kpi_4G=texto_limpio_kpi_4G.replace('%', '')
            #print (texto_limpio_kpi_4G)
            df4g = pd.read_csv(StringIO(texto_limpio_kpi_4G),  delim_whitespace=True)
            #print(".--------print 4g-------")
            #print(df4g)
           #df4g.to_csv("dataframe_alarmas.csv")
            df4g.columns = ['Day', 'Time', 'Attach', 'X2_Handover','S1_Handover', 'Paging', 'Bearer', 'Ser-Req', 'Intra-MME_TAU']
            return df4g
    except FileNotFoundError:
        print("Error al leer kpis")
            
def tabla_kpi_4G (nombre_archivo):
    try:
        df4g=kpi_4G(nombre_archivo)
        alarmas=kpi_alarma(df4g)
        #print("-------------------------------------")
        #print(alarmas)
        return dbc.Col(dbc.Card([
                    html.H2("KPI Tecnologia 4G", className="ms-3"),
            
                    dash_table.DataTable(
                        data=alarmas.to_dict('records'),
                        columns=[
                            {'name': str(i), 'id': str(i) }  
                            
                            for i in alarmas.columns
                        ],style_cell={
                            "textAlign": "center",
                            "font-family": "sans-serif",
                            "fontSize": 14,
                                    }
                        
                    ),
                    
		            dash_table.DataTable
                    (
                        data=df4g.to_dict("records"),
                        columns=[{"name": str(c), "id": str(c)} for c in df4g.columns],
                        #columns=[{"name": i, "id": i} for i in ['alarma', 'fecha', 'hora', 'severidad']],                            
                        style_table={"height": 600,"width": 600},
                        style_cell={
                            "textAlign": "center",
                            "font-family": "sans-serif",
                            "fontSize": 14,
                                    }
                    ),
                    
            ],  
            style={'margin': '10px','max-height': '600px','overflow-y': 'auto' }  ,           
            className="m-3 px-2",
        )) 
    
    except FileNotFoundError:
        print("Error al leer kpis")
        


    
if __name__ == "__main__":
    #nombre="MME VF.txt"
    #Alarmas(nombre)
    #hw(nombre)
    #ip(nombre)
    #Eventos(nombre)
    app.run_server(debug=True,host='0.0.0.0', port=8050)
