import streamlit as st
import matplotlib.pyplot as plt
import os
DATA_FILE = 'valores.txt'
def salvar_aluno(nome, serie, n1, n2, n3):
    with open(DATA_FILE, 'a') as f:
        f.write(f"{nome},{serie},{n1},{n2},{n3}\n")
def ler_dados():
    alunos = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    try:
                        nome, serie, n1, n2, n3 = linha.split(',')
                        n1 = float(n1)
                        n2 = float(n2)
                        n3 = float(n3)
                        media = (n1 + n2 + n3) / 3
                        alunos.append({
                            'nome': nome,
                            'serie': serie.upper(),
                            'n1': n1,
                            'n2': n2,
                            'n3': n3,
                            'media': media
                        })
                    except:
                        continue
    return alunos
def calcular_medias_por_serie(alunos):
    series = {}
    for aluno in alunos:
        serie = aluno['serie']
        if serie not in series:
            series[serie] = {'total': 0, 'quantidade': 0}
        series[serie]['total'] += aluno['media']
        series[serie]['quantidade'] += 1
    medias = {}
    for serie in series:
        total = series[serie]['total']
        qtd = series[serie]['quantidade']
        medias[serie] = total / qtd
    return medias
st.title("Sistema de Notas - Professor")
with st.form("form_cadastro"):
    st.subheader("Cadastrar Aluno")
    nome = st.text_input("Nome do aluno")
    serie = st.text_input("Série (ex: 1D, 2D, 3D)").upper()
    n1 = st.number_input("Nota 1", min_value=0.0, max_value=10.0, step=0.1)
    n2 = st.number_input("Nota 2", min_value=0.0, max_value=10.0, step=0.1)
    n3 = st.number_input("Nota 3", min_value=0.0, max_value=10.0, step=0.1)
    enviar = st.form_submit_button("Salvar")
    if enviar:
        if nome.strip() and serie.strip():
            salvar_aluno(nome.strip(), serie.strip(), n1, n2, n3)
            st.success(f"Aluno {nome} salvo com sucesso!")
        else:
            st.error("Nome e série são obrigatórios.")
alunos = ler_dados()
if alunos:
    st.subheader("Relatórios")
    st.markdown("Média geral por série:")
    medias_serie = calcular_medias_por_serie(alunos)
    for serie, media in sorted(medias_serie.items()):
        st.write(f"**Série {serie}**: Média Geral = `{media:.2f}`")
    series_disponiveis = sorted(set(a['serie'] for a in alunos))
    serie_selecionada = st.selectbox("Selecione uma série para ver o gráfico de médias:", series_disponiveis)
    alunos_serie = [a for a in alunos if a['serie'] == serie_selecionada]
    alunos_serie.sort(key=lambda x: x['nome'])  
    nomes = [a['nome'] for a in alunos_serie]
    medias = [a['media'] for a in alunos_serie]
    fig, ax = plt.subplots()
    ax.bar(nomes, medias, color='skyblue')
    ax.set_title(f"Média dos Alunos - Série {serie_selecionada}")
    ax.set_ylabel("Média Final")
    ax.set_ylim(0, 10)
    ax.set_xlabel("Nome do Aluno")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
else:
    st.info("Nenhum aluno cadastrado ainda.")
