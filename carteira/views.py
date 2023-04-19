from django.shortcuts import render
from carteira.formularios.forms import Balanco
from carteira.models import ContaUsuario
from financa.formularios.forms import BancoUsuarios
import plotly.express as px
import numpy as np
import datetime as dt
import django
from carteira.models import ContaUsuario
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from django.contrib import messages

def tratar_df(dados):
    dados.data = pd.to_datetime(dados.data)
    dados['mes'] = dados.data.apply(lambda x: x.month)
    dados['ano'] = dados.data.apply(lambda x: x.year)
    dados['mesano'] = dados.data.apply(lambda x:
                                        f'{x.month}/{x.year}')
    return dados

def filtrar_dados(df, data):
        dados = df.copy()
        dados['delta'] = dados.data - data
        dados.delta = dados.delta.astype(str)
        dados.delta = dados.delta.str.replace(' days', '')
        dados.delta = dados.delta.astype(int)
        dados = dados.loc[dados.delta >= 0]

        return dados

# Create your views here.
def dash(request):
    conta = ContaUsuario.objects.filter(login = request.user).values()
    user = BancoUsuarios.objects.filter(login=request.user).values()
    salario = user[0]['salario']
    df = tratar_df(pd.DataFrame(conta))
    # df = filtrar_dados(df, dt.datetime.now())
    # mes_atual = dt.datetime.now().month
    # ano_atual = dt.datetime.now().year
    # dados_mes_atual = df.loc[(df.mes == mes_atual) &
    #                                     (df.ano == ano_atual)]
    # dados_mes_passado = df\
    #                         .loc[(df.mes == (mes_atual-1)) &
    #                                 (df.ano == ano_atual)]
    # atual = round(dados_mes_atual.valor.sum(), 2)
    # passado = round(dados_mes_passado.valor.sum(), 2)
    x = [i for i in range(12)]
    y = np.random.normal(2000, 100, 12)
    x2 = ['casa', 'lazer', 'transporte']
    y2 = np.random.randint(100, 600, 3)

    
    # @app.callback(
    #     Output('fig', 'figure'), Input('fig', 'figure'))
    def line_plot():
        layout = go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    title_x = 0.5,
                    title='Histórico de Gasto',
                    xaxis={'gridcolor':'rgba(0,0,0,0.10)',
                           'linecolor': '#000000',
                           'dtick': 1,},
                    yaxis={'gridcolor':'rgba(0,0,0,0.10)',
                           'color':'#000000', 
                           'linecolor': '#000000'
                           }
                )
        fig= go.Figure(layout=layout)
        fig.add_trace(
        go.Scatter(x=x, y=y, mode='lines'))
        return fig

    # @app.callback(
    #     Output('fig2', 'figure'), Input('fig2', 'figure'))
    def bar_plot():
        layout = go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    title_x = 0.5,
                    title='Histórico de Gasto',
                    xaxis={'gridcolor':'rgba(0,0,0,0)'},
                    yaxis={'gridcolor':'rgba(0,0,0,0)', 'color':'rgba(0,0,0,0)'}
                )
        fig= go.Figure(layout=layout)
        fig.add_trace(
        go.Bar(x=x2, y=y2, text=y2))
        return fig
    
    
    # @app.callback(
    #     Output('caixa', 'figure'),
    #     [Input('dropdown-color', 'value')])
    def caixa():
        layout = go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Indicator(mode="number+delta",
                                   value=df.valor.sum(),
                                   number={"prefix": "R$", 'valueformat': '.2f'},
                                   delta={'reference': salario, 'relative':True,
                                          "valueformat": ".1%",
                                          'increasing': {'color':'#0000ff'}},
                                   title='Caixa'))
        fig.update_layout(height=250)
        return fig
    
    # @app.callback(
    #     Output('gasto_atual', 'figure'),
    #     [Input('dropdown-color', 'value')])
    def gasto_mensal():
        layout = go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Indicator(mode="number+delta",
                                   number={"prefix": "R$", 'valueformat': '.2f'},
                                   delta={'reference': 300, 'relative':True,
                                          "valueformat": ".1%", 'increasing': {'color':'#0000ff'}},
                                   value=400,
                                   title='Evolução do gasto mensal'))
        fig.update_layout(height=250)
        return fig
    
    # @app.callback(
    #     Output('gasto_mes_passado', 'figure'),
    #     [Input('dropdown-color', 'value')])
    def gasto_anterior():
        layout = go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Indicator(mode="number+delta",
                                   value=500,
                                   number={"prefix": "R$", 'valueformat': '.2f'},
                                   delta={'reference':300, 'relative': True,
                                                     'valueformat': '.1%',
                                                     'increasing': {'color':'#0000ff'}},
                                   title='Evolução do gasto do mes anterior'))
        fig.update_layout(height=250)
        return fig

    app = DjangoDash('teste', add_bootstrap_links=True)
    app.css.append_css({"external_url": "/static/styles/style.css"})
    app.layout = html.Div(id='div_dash',
                          children=[
                                        html.Div(className='Filtros', children=[
                                            dbc.Container(id='filters', children=[
                                                        dbc.Row([
                                                            dbc.Col(dcc.DatePickerRange(start_date=dt.date(2023,4,1),
                                                                                        end_date=dt.datetime.now()), md=4)
                                                        ])])
                                    ]),
                                    html.Div(className='metricas', children=[
                                                dbc.Container(id='graphs', children=[
                                                        dbc.Row([
                                                            dbc.Col(dcc.Graph(id='caixa', figure=caixa()), md=4),
                                                            dbc.Col(dcc.Graph(id='gasto_atual', figure=gasto_mensal()), md=4),
                                                            dbc.Col(dcc.Graph(id='gasto_mes_passado', figure=gasto_anterior()), md=4),
                                                        ])])
                                                                
                                    ]),
                                    dbc.Container(id='graphs', children=[
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id='fig',
                                                              figure=line_plot()), md=6),
                                            dbc.Col(dcc.Graph(id='fig2',
                                                              figure=bar_plot()), md=6)
                                            ]),
                                    ])
                                ])

    
    login = request.user
    salario = BancoUsuarios.objects.filter(login=login).values('salario')
    nome = BancoUsuarios.objects.filter(login=login).values('nome')
    salario = salario[0]['salario']
    salario = str(salario).replace('.', ',')
    context = {
        'dash_html': app,
        'salario': salario,
        'login': nome[0]['nome']
    }

    return render(request, 'carteira/dash.html', context)


def balanco(request):
    if request.method=='GET':
        form = Balanco()
        login = request.user
        salario = BancoUsuarios.objects.filter(login=login).values('salario')
        salario = salario[0]['salario']
        nome = BancoUsuarios.objects.filter(login=login).values('nome')
        context = {
            'form': form,
            'salario': salario,
            'login': nome[0]['nome']
        }
        return render(request, 'carteira/balanco.html', context)
    else:
        form = Balanco(request.POST)
        if form.is_valid():
            login = request.user
            data = django.utils.timezone.now()
            valor = form.cleaned_data.get('valor')
            categoria = form.cleaned_data.get('categoria')
            extra_gasto = form.cleaned_data.get('gasto_extra')
            conta = ContaUsuario(login=login, data=data, valor=valor, categoria=categoria, extra_gasto=extra_gasto)
            conta.save()
            texto = f'R$ {valor:.2f} cadastrado para a categoria {categoria}'
            messages.success(request, texto)
            form = Balanco()
            salario = BancoUsuarios.objects.filter(login=login).values('salario')
            salario = salario[0]['salario']
            nome = BancoUsuarios.objects.filter(login=login).values('nome')
            context = {
                'form': form,
                'salario': salario,
                'login': nome[0]['nome']
            }
            return render(request, 'carteira/balanco.html', context)
            


        