import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === NOVAS IMPORTAÇÕES PARA A INTELIGÊNCIA ARTIFICIAL ===
import numpy as np
from sklearn.linear_model import LinearRegression

# ==========================================
# 1. CONFIGURAÇÃO DA INTERFACE (STREAMLIT)
# ==========================================
st.set_page_config(page_title="Gestão de Estoque Inteligente", layout="wide")
st.title("📦 Sistema de Monitoramento & Predição de Estoque")

# Painel Lateral para Configurações de E-mail
st.sidebar.header("📧 Configurações de Alerta")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = st.sidebar.text_input("E-mail Remetente", value="seu_email@gmail.com")
SENDER_PASSWORD = st.sidebar.text_input("Senha de App (Google)", type="password", value="sua_senha_de_app")
RECEIVER_EMAIL = st.sidebar.text_input("E-mail Destinatário", value="destinatario_alerta@gmail.com")

# ==========================================
# 2. CONFIGURAÇÃO DO BANCO DE DADOS PERSISTENTE
# ==========================================
conn = sqlite3.connect("inventory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY, 
        name TEXT, 
        current_stock INTEGER,
        status TEXT DEFAULT 'Ativo'
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        product_id INTEGER, 
        quantity INTEGER, 
        sale_date TEXT
    )
""")

# Carga inicial de teste (só insere se o banco estiver limpo)
cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        [(101, "Mechanical Keyboard", 15, "Ativo"), 
         (102, "Gaming Mouse", 80, "Ativo")]
    )
    today = datetime.now()
    d1 = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    d2 = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    d3 = (today - timedelta(days=3)).strftime('%Y-%m-%d')
    cursor.executemany(
        "INSERT INTO sales VALUES(?, ?, ?)",
        [(101, 5, d1), (101, 5, d2), (101, 5, d3),
         (102, 2, d1), (102, 4, d2), (102, 3, d3)]
    )
    conn.commit()

# ==========================================
# 3. FUNÇÃO DE ENVIO DE E-MAIL
# ==========================================
def send_email_alert(product_name, remaining_days, depletion_date, stock):
    if SENDER_EMAIL == "seu_email@gmail.com":
        return "ℹ️ Envio de e-mail pulado: configure suas credenciais na barra lateral."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"⚠️ [ALERTA DE COMPRA] - {product_name} acabando!"

    body = f"""
    Atenção, o sistema detectou uma necessidade crítica de reposição:
    
    Produto: {product_name}
    Estoque Atual: {stock} unidades
    Dias Restantes Estimados: {remaining_days} dias
    Data Prevista para Esgotamento: {depletion_date}
    
    Por favor, gere uma nova ordem de compra imediatamente.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        return f"📧 E-mail de alerta enviado com sucesso para {RECEIVER_EMAIL}!"
    except Exception as e:
        return f"❌ Falha ao enviar e-mail: {e}"

# ==========================================
# 4. CRIAÇÃO DAS ABAS NA INTERFACE WEB
# ==========================================
aba_dashboard, aba_cadastro, aba_status, aba_simulador = st.tabs([
    "📊 Painel Geral & Predição", 
    "🆕 Cadastrar Produtos", 
    "⚙️ Gerenciar Linha de Produtos",
    "🛒 Simular Novas Vendas"
])

# --- ABA 1: PAINEL GERAL (MONITOR TRADICIONAL + INTELIGÊNCIA ARTIFICIAL) ---
with aba_dashboard:
    st.header("Análise Automatizada de Riscos e Tendências")
    
    col_tradicional, col_ia = st.columns(2)
    
    with col_tradicional:
        st.subheader("Análise Estatística Tradicional")
        st.caption("Calcula o esgotamento baseado estritamente na média de vendas dos últimos 3 dias.")
        
        if st.button("🔄 Rodar Análise por Média Simples", type="primary"):
            three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            
            query = """
                SELECT 
                    p.id, p.name, p.current_stock, 
                    (IFNULL(SUM(s.quantity), 0) / 3.0) AS daily_average
                FROM products p
                LEFT JOIN sales s ON p.id = s.product_id AND s.sale_date >= ?
                WHERE p.status = 'Ativo'
                GROUP BY p.id
            """
            df = pd.read_sql_query(query, conn, params=(three_days_ago,))

            for index, row in df.iterrows():
                average = row['daily_average']
                stock = row['current_stock']
                name = row['name']
                
                if average > 0:
                    remaining_days = int(stock / average)
                    depletion_date = (datetime.now() + timedelta(days=remaining_days)).strftime('%Y-%m-%d')

                    if remaining_days <= 5:
                        st.error(f"⚠️ **TRADICIONAL:** O produto **{name}** (ID: {row['id']}) vai zerar em **{remaining_days} dias** ({depletion_date}).")
                        status_email = send_email_alert(name, remaining_days, depletion_date, stock)
                        st.info(status_email)
                    else:
                        st.success(f"✅ **{name}**: Estoque seguro. Mais {remaining_days} dias.")
                else:
                    st.warning(f"ℹ️ **{name}**: Sem vendas recentes para calcular média.")

    with col_ia:
        st.subheader("Predição Avançada por IA")
        st.caption("Usa Machine Learning (Regressão Linear) para mapear aceleração ou queda de demanda no tempo.")
        
        if st.button("🧠 Rodar Predição Preditiva com IA", type="secondary"):
            query_vendas = "SELECT product_id, quantity, sale_date FROM sales"
            df_vendas = pd.read_sql_query(query_vendas, conn)
            
            query_produtos = "SELECT id, name, current_stock FROM products WHERE status = 'Ativo'"
            df_produtos = pd.read_sql_query(query_produtos, conn)

            for index, produto in df_produtos.iterrows():
                p_id = produto['id']
                name = produto['name']
                stock = produto['current_stock']
                
                # Filtra o histórico do produto específico
                vendas_prod = df_vendas[df_vendas['product_id'] == p_id].copy()
                
                if len(vendas_prod) >= 3:
                    # IA estuda os números ordinais de dias
                    vendas_prod['dia_num'] = range(1, len(vendas_prod) + 1)
                    X = vendas_prod[['dia_num']].values  # Dias
                    y = vendas_prod['quantity'].values   # Quantidades
                    
                    # Treinamento e predição em tempo real
                    modelo_ia = LinearRegression()
                    modelo_ia.fit(X, y)
                    
                    proximo_dia = np.array([[len(vendas_prod) + 1]])
                    previsao_vendas_amanha = modelo_ia.predict(proximo_dia)[0]
                    previsao_vendas_amanha = max(0.1, previsao_vendas_amanha) # Evita divisão por zero ou negativa
                    
                    remaining_days = int(stock / previsao_vendas_amanha)
                    depletion_date = (datetime.now() + timedelta(days=remaining_days)).strftime('%Y-%m-%d')
                    
                    if remaining_days <= 5:
                        st.error(f"🚨 **ALERTA CRÍTICO DA IA:** **{name}** detectado em forte tendência! Zera em **{remaining_days} dias** ({depletion_date}).")
                        status_email = send_email_alert(name, remaining_days, depletion_date, stock)
                        st.info(status_email)
                    else:
                        st.success(f"🧠 **IA ANÁLISE:** **{name}** calculada com estabilidade comercial. Restam {remaining_days} dias.")
                else:
                    st.warning(f"ℹ️ **{name}**: Histórico insuficiente para inteligência preditiva (Mínimo de 3 registros).")

# --- ABA 2: CADASTRO DE PRODUTOS ---
with aba_cadastro:
    st.header("Entrada de Novos Itens no Banco")
    with st.form("form_cadastro", clear_on_submit=True):
        id_prod = st.number_input("Código ID Único", min_value=1, step=1)
        nome_prod = st.text_input("Nome do Produto comercial")
        estoque_ini = st.number_input("Quantidade de Estoque Inicial", min_value=0, step=1)
        botao_salvar = st.form_submit_button("Gravar no Banco SQL")
        
        if botao_salvar:
            if nome_prod:
                try:
                    cursor.execute("INSERT INTO products (id, name, current_stock, status) VALUES (?, ?, ?, 'Ativo')", (id_prod, nome_prod, estoque_ini))
                    conn.commit()
                    st.success(f"Produto '{nome_prod}' adicionado com sucesso ao SQL!")
                except sqlite3.IntegrityError:
                    st.error("Erro: Já existe um produto cadastrado com este ID.")
            else:
                st.error("O nome do produto não pode ficar em branco.")

# --- ABA 3: FORA DE LINHA / STATUS ---
with aba_status:
    st.header("Status de Comercialização")
    st.caption("Produtos marcados como 'Fora de Linha' são ignorados pelo robô de disparo de e-mails.")
    
    produtos_df = pd.read_sql_query("SELECT id, name, current_stock, status FROM products", conn)
    
    for idx, row in produtos_df.iterrows():
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(f"**{row['name']}** (ID: {row['id']}) - Estoque: {row['current_stock']}")
        with col2:
            st.write(f"Status: `{row['status']}`")
        with col3:
            if row['status'] == 'Ativo':
                if st.button("Mudar p/ Fora de Linha", key=f"del_{row['id']}"):
                    cursor.execute("UPDATE products SET status = 'Fora de Linha' WHERE id = ?", (row['id'],))
                    conn.commit()
                    st.rerun()
            else:
                if st.button("Reativar Produto", key=f"act_{row['id']}"):
                    cursor.execute("UPDATE products SET status = 'Ativo' WHERE id = ?", (row['id'],))
                    conn.commit()
                    st.rerun()

# --- ABA 4: SIMULADOR DE VENDAS ---
with aba_simulador:
    st.header("Registrar Saída de Estoque (Venda)")
    prod_venda = st.selectbox("Escolha o Produto", pd.read_sql_query("SELECT id, name FROM products WHERE status='Ativo'", conn))
    qtd_venda = st.number_input("Quantidade Vendida", min_value=1, step=1)
    
    if st.button("Confirmar Venda"):
        p_id = int(prod_venda.split()[0])
        cursor.execute("UPDATE products SET current_stock = current_stock - ? WHERE id = ?", (qtd_venda, p_id))
        cursor.execute("INSERT INTO sales VALUES (?, ?, ?)", (p_id, qtd_venda, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        st.success("Venda processada! Estoque atualizado no SQL.")