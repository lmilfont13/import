import streamlit as st

st.set_page_config(page_title="Simulador de Custos de Importação", layout="centered")
st.title("Simulador de Custos de Importação")

st.markdown("""
Esse aplicativo simula os custos de importação para produtos FOB, considerando impostos, custos logísticos e margens de segurança.  
Preencha os campos abaixo para obter uma estimativa detalhada dos custos de importação.
""")

# --- INPUTS ---
st.header("🔢 Dados básicos da operação")

col1, col2 = st.columns(2)
with col1:
    fob_unit = st.number_input("Preço FOB unitário (USD)", value=4.95, min_value=0.0, step=0.01)
    quantidade = st.number_input("Quantidade de produtos", value=4132, min_value=1)
    frete_usd = st.number_input("Frete internacional (USD)", value=14000.0, min_value=0.0)
    seguro_usd = st.number_input("Seguro internacional (USD)", value=0.0, min_value=0.0)
    icms_uf = st.selectbox("ICMS do Estado Destino (%)", options=[18, 17, 19, 20, 21, 22], index=0)
    dollar = st.number_input("Dólar do dia (USD/BRL)", value=5.85, min_value=1.0)
with col2:
    armazenagem = st.number_input("Armazenagem (BRL)", value=3400.0, min_value=0.0)
    capatazia = st.number_input("Capatazia/THC (BRL)", value=2489.0, min_value=0.0)
    desembaraco = st.number_input("Desembaraço Aduaneiro (BRL)", value=2800.0, min_value=0.0)
    frete_rodoviario = st.number_input("Frete rodoviário (BRL)", value=9590.03, min_value=0.0)
    admin_imp = st.number_input("Administração da Importação (BRL)", value=12683.15, min_value=0.0)
    margem_cambio = st.number_input("Margem extra/câmbio (%)", value=10.0, min_value=0.0, step=0.5)

st.header("⚡ Impostos & Taxas (padrão NCM 8516.60.00, editáveis)")
ii = st.number_input("II - Imposto de Importação (%)", value=18.0, min_value=0.0, step=0.01)
ipi = st.number_input("IPI (%)", value=7.8, min_value=0.0, step=0.01)
pis = st.number_input("PIS (%)", value=2.1, min_value=0.0, step=0.01)
cofins = st.number_input("COFINS (%)", value=9.65, min_value=0.0, step=0.01)
afrmm = st.number_input("Taxa AFRMM - Marinha Mercante (R$)", value=7165.44, min_value=0.0)
custo_siscomex = st.number_input("Taxa SISCOMEX (R$)", value=223.64, min_value=0.0)

# --- CÁLCULOS BÁSICOS ---
# Custos em USD
valor_fob_total_usd = fob_unit * quantidade
valor_cif_usd = valor_fob_total_usd + frete_usd + seguro_usd

# Conversão para BRL
valor_fob_total_brl = valor_fob_total_usd * dollar
frete_brl = frete_usd * dollar
seguro_brl = seguro_usd * dollar
valor_cif_brl = valor_fob_total_brl + frete_brl + seguro_brl

# Base de Cálculo para II, IPI, PIS, COFINS, ICMS
base_ii = valor_cif_brl
valor_ii = base_ii * (ii / 100)
base_ipi = base_ii + valor_ii
valor_ipi = base_ipi * (ipi / 100)
base_pis_cofins = base_ii + valor_ii + valor_ipi
valor_pis = base_pis_cofins * (pis / 100)
valor_cofins = base_pis_cofins * (cofins / 100)

# ICMS
bc_icms = (
    valor_cif_brl + valor_ii + valor_ipi + valor_pis + valor_cofins + 
    armazenagem + capatazia + desembaraco + frete_rodoviario + admin_imp + afrmm + custo_siscomex
) / (1 - icms_uf / 100)
valor_icms = bc_icms * (icms_uf / 100)

# --- TOTALIZAÇÃO ---
custos_tributarios = (
    valor_ii + valor_ipi + valor_pis + valor_cofins + valor_icms + afrmm + custo_siscomex
)
custos_logisticos = (
    armazenagem + capatazia + desembaraco + frete_rodoviario + admin_imp
)
valor_total = (
    valor_fob_total_brl + frete_brl + seguro_brl + custos_tributarios + custos_logisticos
)
valor_total_margem = valor_total * (1 + (margem_cambio / 100))

valor_unitario = valor_total_margem / quantidade

# --- SAÍDA ---
st.header("📊 Resultado da Simulação")

colr1, colr2 = st.columns(2)
with colr1:
    st.write("### Valores Chave")
    st.metric("Custo total estimado (BRL)", f"R$ {valor_total_margem:,.2f}")
    st.metric("Custo unitário com margem (BRL)", f"R$ {valor_unitario:,.2f}")
    st.metric("Valor total da mercadoria (BRL)", f"R$ {valor_fob_total_brl:,.2f}")
    st.metric("Valor total de impostos (BRL)", f"R$ {custos_tributarios:,.2f}")
    st.metric("Valor total logístico/admin. (BRL)", f"R$ {custos_logisticos:,.2f}")

with colr2:
    st.write("### Impostos Detalhados")
    st.write(f"II: R$ {valor_ii:,.2f}")
    st.write(f"IPI: R$ {valor_ipi:,.2f}")
    st.write(f"PIS: R$ {valor_pis:,.2f}")
    st.write(f"COFINS: R$ {valor_cofins:,.2f}")
    st.write(f"ICMS: R$ {valor_icms:,.2f}")
    st.write(f"AFRMM: R$ {afrmm:,.2f}")
    st.write(f"SISCOMEX: R$ {custo_siscomex:,.2f}")

st.write("### Outros componentes do custo")
st.write(f"Frete internacional (BRL): R$ {frete_brl:,.2f}")
st.write(f"Seguro internacional (BRL): R$ {seguro_brl:,.2f}")
st.write(f"Armazenagem: R$ {armazenagem:,.2f}")
st.write(f"Desembaraço: R$ {desembaraco:,.2f}")
st.write(f"Capatazia (THC): R$ {capatazia:,.2f}")
st.write(f"Frete rodoviário: R$ {frete_rodoviario:,.2f}")
st.write(f"Administração importação: R$ {admin_imp:,.2f}")

# Alertas de possíveis custos faltantes
st.warning("**Seguro internacional está zerado!** Recomenda-se proteger a carga.")
if seguro_usd == 0.0:
    st.info("Se o custo do seguro não for conhecido, use 0,5%–2% do valor da carga como referência.")

for nome, valor in [
    ("certificação INMETRO/Laudos", 0), ("taxas bancárias", 0), ("custos extras logísticos (demurrage, storage extra)", 0)
]:
    st.info(f"Dica: Lembre-se de incluir eventuais {nome} caso aplicável.")

st.success("Simulação pronta! Revise os campos, salve em PDF com Ctrl+P ou baixe esta página.")

# Fim do app