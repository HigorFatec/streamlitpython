import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from termcolor import colored

st.set_page_config(layout='wide')

page_bg_img = """
<style>
[data-testid=stAppViewContainer]{
background-image: linear-gradient(#45A3D2,#0D3592);
}
[data-testid=stSidebar]{
background-image: linear-gradient(#45A3D2,#0D3592);
}
[data-testid=StyledLinkIconContainer]{
background-image: linear-gradient(#12239E,#12239E);
}
.titulo-customizado{
color: #FFFFFF;
text-align: center;
}
[data-testid="stHeader"]{
background-image: linear-gradient(#45A3D2,#45A3D2);
}
[data-testid="stMarkdownContainer"]{
color: #FFFFFF;
}
[class="main-svg"]{
style="background: rgb(255, 255, 255, 0);";
}
</style>
"""
st.markdown(page_bg_img,unsafe_allow_html=True)

# Configurando a senha desejada
senha_correta = "123"

# Adicionando um espaço vazio para a mensagem
mensagem_placeholder = st.empty()

senha = st.sidebar.text_input("Digite a senha:", type="password")


# Verificando a senha
if senha == senha_correta:

    mensagem_placeholder.success("Senha correta! Acesso permitido.")
    
    # Se a senha estiver correta, você pode prosseguir com o código do seu dashboard abaixo.

    # Restante do seu código aqui...


    # Exibir o código HTML usando st.markdown

    st.markdown("<h1 class='titulo-customizado'>DASHBOARD CONTROLE DE ATIVOS</h1>", unsafe_allow_html=True)

    # 1 - ABRINDO O ARQUIVO JSON (FONTE DE DADOS)
    file = open('json.json')
    data = json.load(file)
    df = pd.DataFrame.from_dict(data)
    file.close()

    # 1.1 - ABRINDO O ARQUIVO JSON (RESULTADO)
    file_resultado = open('resultado.json')
    data_resultado = json.load(file_resultado)
    df_resultado = pd.DataFrame.from_dict(data_resultado)
    file.close()

    # 1.2 - ABRINDO O ARQUIVO JSON (DEVOLUTIVO)
    file_devolutivo = open('devolutivos.json')
    data_devolutivo = json.load(file_devolutivo)
    df_devolutivo = pd.DataFrame.from_dict(data_devolutivo)
    file.close()


    # 2 - DATA
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df = df.sort_values('data')
    df = df.drop_duplicates()

    #2.1 - DATA (RESULTADO)
    df_resultado['DATA'] = pd.to_datetime(df_resultado['DATA'], dayfirst=True)
    df_resultado = df_resultado.sort_values('DATA')

    #2.1.1 - DATA (DEVOLUTIVO)
    df_devolutivo['data'] = pd.to_datetime(df_devolutivo['data'],dayfirst=True)
    df_devolutivo = df_devolutivo.sort_values('data')
    df_devolutivo = df_devolutivo.drop_duplicates()
    # Remover caracteres não numéricos da coluna 'quantidade'
    df_devolutivo['quantidade'] = df_devolutivo['quantidade'].str.replace(r'\D', '', regex=True)

    df_devolutivo['quantidade'] = df_devolutivo['quantidade'].astype(int)

    #2.2 - MODIFICANDO PARA STRING (RESULTADO)
    df_resultado['TRANSPORTE'] = df_resultado['TRANSPORTE'].astype(str)

    #2.3 - FILTRANDO RESULTADOS
    lista_de_valores = ['Cerv Heineken Pil 0,60Gfa Rt 24Un',
    'CERV AMSTEL LAGER 0,60L GFA RT 24UN',
    'Cerv Amstel Lager 0,60l Gfa Rt 24un',
    'Draft Beer Heineken Pilsen 30L Pbr2',
    'Refr Schl Itub 0,60Lgfa Rt 24Un',
    'Cerv Glacial Pil 0,60Lgfa Rt 24Un',
    'Cerv Glacial Pil 1Lgfa Rt 12Un',
    'Cerv Schin Pil 1Lgfa Rt 12Un',
    'Draft Beer Heineken Pilsen 50L Pbr2',
    'Cerv Amstel Lager 1Lgfa Rt 12Un',
    'CERV SCHIN PIL 0,60LGFA RT 24UN',
    'Draft Beer Amstel Lager 50L Pbr2',
    'Draft Beer Lagunitas Ipa 30L Pbr2',
    'Draft Beer Baden Ipa 30L Pbr2',
    'Draft Beer Baden Pilsen Cristal 30L Pbr2',
    'Draft Beer Blue Moon 30L Pbr2',

    ]
    df_resultado = df_resultado[df_resultado['DESCR. DO MATERIAL'].isin(lista_de_valores)]

    #2.4 MAPEAMENTO DE VALORES
    # Mapeamento de valores antigos para novos
    mapeamento_resultado = {
        'Cerv Heineken Pil 0,60Gfa Rt 24Un': 'CAIXA PLAST HEINEKEN 0,60L 24UN (IM)',
        'CERV AMSTEL LAGER 0,60L GFA RT 24UN': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
        'Cerv Amstel Lager 0,60l Gfa Rt 24un': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
        'Draft Beer Heineken Pilsen 30L Pbr2': 'BARRIL 30L',
        'Refr Schl Itub 0,60Lgfa Rt 24Un': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
        'Cerv Glacial Pil 0,60Lgfa Rt 24Un': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
        'Cerv Glacial Pil 1Lgfa Rt 12Un': 'CAIXA PLASTICA 1L (IM)',
        'Cerv Schin Pil 1Lgfa Rt 12Un': 'CAIXA PLASTICA 1L (IM)',
        'Draft Beer Heineken Pilsen 50L Pbr2': 'BARRIL 50L',
        'Cerv Amstel Lager 1Lgfa Rt 12Un': 'CAIXA PLASTICA 1L (IM)',
        'CERV SCHIN PIL 0,60LGFA RT 24UN': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
        'Draft Beer Amstel Lager 50L Pbr2': 'BARRIL 50L',
        'Draft Beer Lagunitas Ipa 30L Pbr2': 'BARRIL 30L',
        'Draft Beer Baden Ipa 30L Pbr2': 'BARRIL 30L',
        'Draft Beer Baden Witbier 30L Pbr2': 'BARRIL 30L',
        'Draft Beer Baden Pilsen Cristal 30L Pbr2': 'BARRIL 30L',
        'Draft Beer Blue Moon 30L Pbr2': 'BARRIL 30L',
    }

    # Renomear os valores na coluna 'DESCR. DO MATERIAL'
    df_resultado['DESCR. DO MATERIAL'] = df_resultado['DESCR. DO MATERIAL'].replace(mapeamento_resultado)

    mapeamento_devolutivo = {
    'CERV AMSTEL LAGER 0,60L RT 24UN': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
    'CERV HEINEKEN PIL 0,60GRF RT 24UN.': 'CAIXA PLAST HEINEKEN 0,60L 24UN (IM)',
    'CERV GLACIAL PIL 0,60LGFA RT 24UN': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
    'CERV AMSTEL LAGER 1LGFA RT 12UN': 'CAIXA PLASTICA 1L (IM)',
    'CERV GLACIAL PIL 1LGFA RT 12UN': 'CAIXA PLASTICA 1L (IM)',
    'DRAFT BEER AMSTEL LAGER 50L.':'BARRIL 50L',
    'CERV DEVASSA LAGER 0,60LGFA RT 24UN': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
    'CERV DEVASSA LAGER 1LGFA RT 12UN': 'CAIXA PLASTICA 1L (IM)',
    'DRAFT BEER  BADEN IPA 30L': 'BARRIL 30L',
    'DRAFT BEER BADEN WITBIER 30L PBR2': 'BARRIL 30L',
    'DRAFT BEER LAGUNITAS IPA 30L': 'BARRIL 30L',
    'DRAFT BEER HEINEKEN PIL30L': 'BARRIL 30L',
    'CERV SCHIN PIL 0,60LGFA RT 24UNu': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',
    'DRAFT BEER HEINEKEN PIL 50L':'BARRIL 50L',
    'CERV SCHIN PIL 1LGFA RT 12UN': 'CAIXA PLASTICA 1L (IM)',
    'REFR SCHL ITUB 0,60LGFA RT 24UN': 'CAIXA PLAST AMARELA 0,60L 24UN (IM)',

    }

    # Renomear os valores na coluna 'DESCR. DO MATERIAL'
    df_devolutivo['nome'] = df_devolutivo['nome'].replace(mapeamento_devolutivo)


    # 2.5 = REORDENANDO
    df['data'] = df['data'].apply(lambda x: f"{x.day}-{x.month}-{x.year}")
    df_resultado['DATA'] = df_resultado['DATA'].apply(lambda x: f"{x.day}-{x.month}-{x.year}")
    df_devolutivo['data'] = df_devolutivo['data'].apply(lambda x: f"{x.day}-{x.month}-{x.year}")


    # 2.6 Mostrar tudo
    date_list = ['TOTAL'] + list(df['data'].unique())
    date_list_resultado = ['TOTAL'] + list(df_resultado['DATA'].unique())
    date_list_devolutivo = ['TOTAL'] + list(df_devolutivo['data'].unique())
    filial_list = ['LOCALIDADE'] + list(df['filial'].unique())

    # 3 - Filtro de Busca DT e DATA
    selected_date = st.sidebar.selectbox('Filtro Data', date_list)
    if selected_date != 'TOTAL':
        df_filtered_date = df[df['data'] == selected_date].reset_index(drop=True)
        df_filtered_date_resultado = df_resultado[df_resultado['DATA'] == selected_date].reset_index(drop=True)
        df_filtered_date_devolutivo = df_devolutivo[df_devolutivo['data'] == selected_date].reset_index(drop=True)
    else:
        df_filtered_date = df
        df_filtered_date_resultado = df_resultado
        df_filtered_date_devolutivo = df_devolutivo

    # 3.1 Filtrar opções de DT com base na seleção de Data
    dt_list = ['TOTAL'] + list(df_filtered_date['dt'].unique())
    selected_dt = st.sidebar.selectbox('Filtro DT Conferidos', dt_list)
    if selected_dt != 'TOTAL':
        df_filtered_dt = df_filtered_date[df_filtered_date['dt'] == selected_dt].reset_index(drop=True)
        df_filtered_dt_resultado = df_filtered_date_resultado[df_filtered_date_resultado['TRANSPORTE'] == selected_dt].reset_index(drop=True)
        df_filtered_dt_devolutivo = df_filtered_date_devolutivo[df_filtered_date_devolutivo['dt'] == selected_dt].reset_index(drop=True)
    else:
        df_filtered_dt = df_filtered_date
        df_filtered_dt_resultado = df_filtered_date_resultado
        df_filtered_dt_devolutivo = df_filtered_date_devolutivo

    # 3.2 Filtrar por produto
    produto_list = ['TOTAL'] + list(df_filtered_dt['nome'].unique())
    selected_nome = st.sidebar.selectbox('Filtro Retorno por Produto',produto_list)
    if selected_nome != 'TOTAL':
        df_filtered_nome = df_filtered_dt[df_filtered_dt['nome'] == selected_nome].reset_index(drop=True)

    else:
        df_filtered_nome = df_filtered_dt


    # 4 - Atribuindo valores aos DataFrame
    #json
    dt_df_filtered = df_filtered_nome
    #resultado
    dt_df_filtered_resultado = df_filtered_dt_resultado
    dt_df_filtered_devolutivo = df_filtered_dt_devolutivo

    # 4 - Exibindo o DataFrame
    #dt_df_filtered
    #dt_df_filtered_resultado
    #df_filtered_dt_devolutivo

    # 4.2 GERANDO ADERENCIA AO APLICATIVO
    total_linhas_dt = dt_df_filtered['dt'][dt_df_filtered['dt'].isin(dt_df_filtered_resultado['TRANSPORTE'])].nunique()
    total_linhas_transporte = len(dt_df_filtered_resultado['TRANSPORTE'].unique())

    porcentagem_dt_em_transporte = (total_linhas_dt / total_linhas_transporte) * 100
    porcentagem_dt_em_transporte = "{:.2f}".format(porcentagem_dt_em_transporte)


    #4.3 - Criando Filtro por DT Divergente
    divergencia_list = dt_df_filtered_resultado['TRANSPORTE'][~dt_df_filtered_resultado['TRANSPORTE'].isin(dt_df_filtered['dt'])].unique()
    divergencia_list = [' '] + list(divergencia_list)
    selected_divergencia = st.sidebar.selectbox('Filtro DTs não conferidas', divergencia_list)

    if selected_divergencia != ' ':
        dt_df_filtered_resultado = dt_df_filtered_resultado[dt_df_filtered_resultado['TRANSPORTE'] == selected_divergencia].reset_index(drop=True)
        
        #OCULTANDO OS OUTROS GRAFICOS PARA MELHOR VISUALIZAÇÃO
        dt_df_filtered = dt_df_filtered[dt_df_filtered['dt'] == selected_divergencia].reset_index(drop=True)

        df_filtered_dt_devolutivo = df_filtered_dt_devolutivo[df_filtered_dt_devolutivo['dt'] == selected_divergencia].reset_index(drop=True)

        dt_df_filtered_devolutivo = dt_df_filtered_devolutivo[dt_df_filtered_devolutivo['dt'] == selected_divergencia].reset_index(drop=True)


    # 4.5 - Obtendo a soma

    dt_df_filtered['SOMA'] = dt_df_filtered.groupby('nome')[['quantidade']].transform('sum')
    dt_df_filtered_resultado['SOMA'] = dt_df_filtered_resultado.groupby('DESCR. DO MATERIAL')[['TOTAL.CAIXAS']].transform('sum')

    dt_df_filtered_devolutivo['SOMA'] = dt_df_filtered_devolutivo.groupby('nome')[['quantidade']].transform('sum')

    #4.6 - Reordenando pela Soma

    dt_df_filtered = dt_df_filtered.sort_values(by='SOMA', ascending=True)
    dt_df_filtered_resultado = dt_df_filtered_resultado.sort_values(by='SOMA', ascending=True)
    dt_df_filtered_devolutivo = dt_df_filtered_devolutivo.sort_values(by='SOMA', ascending=True)

    soma_total = dt_df_filtered['SOMA'].unique().sum()
    soma_total_resultado = dt_df_filtered_resultado['SOMA'].unique().sum()
    soma_total_devolutivo = dt_df_filtered_devolutivo['SOMA'].unique().sum()

    # Obter os valores únicos de 'observacoes' e 'nome' como DataFrame
    unique_values_df = dt_df_filtered[['observacoes', 'nome']].drop_duplicates()
    # Eliminar linhas onde 'observacoes' é vazio
    unique_values_df = unique_values_df.dropna(subset=['observacoes'])
    # Ordenar por 'observacoes' e redefinir o índice
    unique_values_df = unique_values_df.sort_values(by='nome').reset_index(drop=True)

    #4.7 - Criando DataFrames para graficos

    # Criar um DataFrame para Plotly Express
    df_pie = pd.DataFrame({'values': [total_linhas_transporte,total_linhas_dt],
                        'names': ['TOTAL', 'CONFERIDO']})

    # Criar um DataFrame com as somas totais
    df_somas = pd.DataFrame({
        'Categoria': ['RETORNO', 'SAÍDA', 'DEVOLUÇÃO'],
        'Soma': [soma_total, soma_total_resultado, soma_total_devolutivo]
    })

    #SOMAR GRAFICOS

    # Mesclar os DataFrames usando colunas diferentes
    dt_df_filtered = dt_df_filtered.drop_duplicates()
    dt_df_filtered_resultado = dt_df_filtered_resultado.drop_duplicates()
    dt_df_filtered_devolutivo = dt_df_filtered_devolutivo.drop_duplicates()

    #FAZENDO O AGRUPAMENTO PELA QUANTIDADE
    df_grouped = dt_df_filtered.groupby(['dt', 'nome'], as_index=False)['quantidade'].sum()
    df_grouped_resultado = dt_df_filtered_resultado.groupby(['TRANSPORTE', 'DESCR. DO MATERIAL'], as_index=False)['TOTAL.CAIXAS'].sum()
    df_grouped_devolutivo = dt_df_filtered_devolutivo.groupby(['dt','nome'], as_index=False)['quantidade'].sum()

    #SOMANDO DEVOLUÇÃO COM RETORNO
    # Agrupa os DataFrames
    df_grouped = pd.merge(df_grouped, df_grouped_devolutivo, on=['dt', 'nome'], suffixes=('_original', '_devolutivo'), how='outer')
    # Preenche valores nulos com 0
    df_grouped = df_grouped.fillna(0)
    # Soma as quantidades
    df_grouped['quantidade'] = df_grouped['quantidade_original'] + df_grouped['quantidade_devolutivo']

    print(df_grouped)

    merged_df = pd.merge(df_grouped, df_grouped_resultado, left_on=['dt', 'nome'], right_on=['TRANSPORTE', 'DESCR. DO MATERIAL'])

    merged_df = merged_df.groupby(['dt', 'nome'], as_index=False).agg({'quantidade':'sum', 'TOTAL.CAIXAS':'sum'})

    merged_df['DIFERENCA'] = merged_df['TOTAL.CAIXAS'] - merged_df['quantidade']

    merged_df = merged_df.sort_values(by='DIFERENCA', ascending=False)

    merged_df = merged_df[merged_df['DIFERENCA'] >= 1]


    #print(merged_df[['nome','TOTAL.CAIXAS','quantidade','DIFERENCA']])
    # Cria um gráfico de barras para a diferença


    # 5 - Gerando graficos

    col1, col2 = st.columns(2)

    col3, col4 = st.columns(2)
    col5 ,col6, col7 = st.columns(3)

    fig_date = px.histogram(dt_df_filtered, y='nome', labels='SOMA',x='quantidade',title='Quantidade Retorno de Ativos')

    fig_date_resultado = px.histogram(dt_df_filtered_resultado, y = 'DESCR. DO MATERIAL', x = 'TOTAL.CAIXAS',labels={'Total:':'SOMA'},orientation='h', title= 'Quantidade Saida de Ativos')

    fig_date_devolutivo = px.histogram(dt_df_filtered_devolutivo, y = 'nome', x = 'quantidade', orientation='h', title= "Quantidade de Devolução de Ativos")

        
    fig_date_aderencia = px.pie(df_pie, values= 'values', names='names',title='Aderencia ao aplicativo',labels = {'values':'Valores'},hover_data=['values'],color_discrete_sequence=['#12239E', '#2CC7B5'])

    fig_date_diferenca = px.pie(df_somas, values = 'Soma', names='Categoria',title='Diferença entre Saida e Retorno de Ativos', hole=0.6,color_discrete_sequence=['#12239E', '#2CC7B5','red'])

    # Criar uma tabela interativa usando plotly
    fig_table = go.Figure(data=[go.Table(
        header=dict(values=['Ativo', 'Observações'],fill_color='#12239E',font=dict(color='white',size=24)
                    ),
        cells=dict(values=[unique_values_df['nome'], unique_values_df['observacoes']],               line_color='darkslategray',fill_color='white', align='left',
    )
    )])

    fig_diferenca_ativo = px.histogram(merged_df, x='nome', y='DIFERENCA', color='dt',
                barmode='group',
                labels={'DIFERENCA': 'Diferença', 'dt': 'Documento'},
                title='Diferença entre TOTAL.CAIXAS e Quantidade por Produto')


    #5.5 - Rotulo de dados
    #RETORNO ATIVOS
    fig_date.update_traces(marker_color='#12239E')
    fig_date.update_traces(textposition='outside', texttemplate='%{x} ', customdata=dt_df_filtered['SOMA'],textfont=dict(color='white'))
    fig_date.update_traces(marker_line_color='#12239E', marker_line_width=2, opacity=1)

    #SAIDA ATIVOS
    fig_date_resultado.update_traces(marker_color='#12239E')
    fig_date_resultado.update_traces(textposition='outside', texttemplate='%{x} ', customdata=dt_df_filtered['SOMA'],textfont=dict(color='white'))
    fig_date_resultado.update_traces(marker_line_color='#12239E', marker_line_width=2, opacity=1)

    #DEVOLUÇÃO
    fig_date_devolutivo.update_traces(marker_color='#12239E')
    fig_date_devolutivo.update_traces(textposition='outside', texttemplate='%{x} ', customdata=dt_df_filtered['SOMA'],textfont=dict(color='white'))
    fig_date_devolutivo.update_traces(marker_line_color='#12239E', marker_line_width=2, opacity=1)

    #ADERENCIA AO APLICATIVO
    fig_date_aderencia.update_traces(textfont=dict(color='white'))
    fig_date_aderencia.update_traces(marker_line_width=1, opacity=1)

    #DIFERENCA DE ATIVOS
    fig_date_diferenca.update_traces(textfont=dict(color='white'))
    fig_date_diferenca.update_traces(marker_line_width=1, opacity=1)

    #SAIDA X RETORNO
    fig_diferenca_ativo.update_traces(textposition='outside', texttemplate='%{y} ', customdata=merged_df['DIFERENCA'],textfont=dict(color='white'))

    #5.6 Cores nos gráficos
    fig_date.update_layout(showlegend=True,plot_bgcolor='rgba(255, 255, 255, 0)')
    fig_date.update_layout(paper_bgcolor='rgba(255, 255, 255, 0.2)')
    fig_date.update_layout(yaxis=dict(title='',tickfont=dict(color='white')))
    fig_date.update_layout(
        title='Quantidade Retorno de Produtos',
        title_font=dict(size=24, color='white'),  # Define o tamanho e a cor do título
    )
    fig_date.update_layout(xaxis=dict(title='',tickfont=dict(color='white')))
    fig_date_aderencia.update_traces(textinfo='label+value', textposition='inside')


    # SAIDA ATIVOS
    fig_date_resultado.update_layout(showlegend=True,plot_bgcolor='rgba(255, 255, 255, 0)')
    fig_date_resultado.update_layout(paper_bgcolor='rgba(255, 255, 255, 0.2)')
    fig_date_resultado.update_layout(yaxis=dict(title='',tickfont=dict(color='white')))
    fig_date_resultado.update_layout(
        title='Quantidade Saida de Ativos',
        title_font=dict(size=24, color='white'),  # Define o tamanho e a cor do título
    )
    fig_date_resultado.update_layout(xaxis=dict(title='',tickfont=dict(color='white')))

    #DEVOLUCAO
    fig_date_devolutivo.update_layout(showlegend=True,plot_bgcolor='rgba(255, 255, 255, 0)',width=800)
    fig_date_devolutivo.update_layout(paper_bgcolor='rgba(255, 255, 255, 0.2)')
    fig_date_devolutivo.update_layout(yaxis=dict(title='',tickfont=dict(color='white')))
    fig_date_devolutivo.update_layout(
        title='Quantidade de Devolução de Produtos',
        title_font=dict(size=24, color='white'),  # Define o tamanho e a cor do título
    )
    fig_date_devolutivo.update_layout(xaxis=dict(title='',tickfont=dict(color='white')))

    # ADERENCIA AO APLICATIVO
    fig_date_aderencia.update_layout(showlegend=False,plot_bgcolor='rgba(255, 255, 255, 0)')
    fig_date_aderencia.update_layout(paper_bgcolor='rgba(255, 255, 255, 0.2)')
    fig_date_aderencia.update_layout(yaxis=dict(title='',tickfont=dict(color='white')))
    fig_date_aderencia.update_layout(
        title='Aderência ao Aplicativo',
        title_font=dict(size=24, color='white'),  # Define o tamanho e a cor do título
    )
    fig_date_aderencia.update_layout(xaxis=dict(title='',tickfont=dict(color='white')))

    # DIFERENCA DE ATIVOS
    fig_date_diferenca.update_layout(showlegend=True,legend=dict(font=dict(size=20)))
    fig_date_diferenca.update_layout(paper_bgcolor='rgba(255, 255, 255, 0.2)')
    fig_date_diferenca.update_layout(yaxis=dict(title='',tickfont=dict(color='white')))
    fig_date_diferenca.update_layout(
        title='Diferença entre Saida e Retorno de Ativos',
        title_font=dict(size=24, color='white'),  # Define o tamanho e a cor do título
    )
    fig_date_diferenca.update_layout(xaxis=dict(title='',tickfont=dict(color='white')))

    fig_table.update_layout(margin=dict(t=0, b=0))

    # SAIDA X RETORNO
    fig_diferenca_ativo.update_layout(showlegend=True,plot_bgcolor='rgba(255, 255, 255, 0)')
    fig_diferenca_ativo.update_layout(paper_bgcolor='rgba(255, 255, 255, 0.2)')
    fig_diferenca_ativo.update_layout(yaxis=dict(title='',tickfont=dict(color='white')))
    fig_diferenca_ativo.update_layout(
        title='Diferença Saida x Retorno de Produtos',
        title_font=dict(size=24, color='white'),  # Define o tamanho e a cor do título
    )
    fig_diferenca_ativo.update_layout(xaxis=dict(title='',tickfont=dict(color='white')))
    #fig_diferenca_ativo.update_layout(bargap=0)

    # 6 - Atribuindo nas Colunas (dashBoard)
    col1.plotly_chart(fig_date_resultado,use_container_width=True)

    col3.plotly_chart(fig_date,use_container_width=True)

    col4.plotly_chart(fig_date_devolutivo,use_container_width=True)

    #col2.dataframe(dt_df_filtered_resultado['TRANSPORTE'].unique())

    #col4.dataframe(dt_df_filtered['dt'].unique())

    col5.plotly_chart(fig_date_aderencia,use_container_width=True)

    col6.plotly_chart(fig_date_diferenca,use_container_width=True)

    #col7.dataframe(unique_values_df,use_container_width=True)
    col7.plotly_chart(fig_table,use_container_width=True)

    col2.plotly_chart(fig_diferenca_ativo,use_container_width=True)

else:
    st.error("Senha incorreta! Acesso negado.")