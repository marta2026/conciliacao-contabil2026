import streamlit as st
import json
import io
from datetime import datetime

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Conciliação Contábil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── LOGOS (base64 inline) ──────────────────────────────────────────────────────
LOGO_NC = "data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAD9tgABAAAAADLLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChjVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAGJsdWMAAAAAAAAAAQAAAAxlblVTAAAANAAAABwATgBvACAAYwBvAHAAeQByAGkAZwBoAHQALAAgAHUAcwBlACAAZgByAGUAZQBsAHkAAAAAWFlaIAAAAAAAAPbWAAEAAAAA0y1YWVogAAAAAAAAAxYAAAMkAAC/h1hZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAC0AVoDASIAAhEBAxEB/8QAHQABAAIDAQEBAAAAAAAAAAACBwUGCAkEAwH/xABREAEDAQMDBAcLCAcFBQAAAAAAAQACAwQFBhESITETQVFTkpKjswnhCRQVIiMyNzhCYXSBtBgYIzZVdJGV0RcmNlV0kaXRF"

LOGO_MF = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABJ0AAAJPCAYAAADW"

# ── DADOS ─────────────────────────────────────────────────────────────────────
CONTAS = [
    # ══ NUTRICASH — ATIVO ══
    {"id":"nc-caixa","nome":"Caixa","codigo":"11110000001","tipo":"ativo","icon":"💵","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-bb-10927","nome":"Banco do Brasil - 10927-4","codigo":"11230000001","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-sant-13019","nome":"Santander - 13019419-6","codigo":"11230000102","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-sant-13005","nome":"Santander - 13005710-3","codigo":"11230000103","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-cef-1277","nome":"Caixa Econômica Federal - 1277-8","codigo":"11230000200","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-brad-078288","nome":"Bradesco - 078288-2","codigo":"11230000300","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-safra-401811","nome":"Safra - 401811-6","codigo":"11230000400","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-banese-125042","nome":"Banese - 125042-2","codigo":"11230000500","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-itau-10026","nome":"Itaú - 10026-5","codigo":"11230000601","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-itau-03973","nome":"Itaú - 03973-1","codigo":"11230000600","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-itau-03882","nome":"Itaú - 03882-1","codigo":"11230000602","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-itau-11407","nome":"Itaú - 11407-7","codigo":"11230000603","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-itau-89168","nome":"Itaú - 89168-5","codigo":"11230000609","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-itau-56247","nome":"Itaú - 56247-3","codigo":"11230000610","tipo":"ativo","icon":"🏦","empresas":["nc"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"nc-cdb-brad","nome":"CDB Bradesco","codigo":"13110250001","tipo":"ativo","icon":"📈","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-apl-bb","nome":"Aplicação Banco do Brasil","codigo":"13115300300","tipo":"ativo","icon":"📈","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-apl-itau","nome":"Aplicação Itaú","codigo":"13115300001","tipo":"ativo","icon":"📈","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-apl-safra","nome":"Aplicação Safra","codigo":"13115300100","tipo":"ativo","icon":"📈","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-adto-sal","nome":"Adiantamento de Salários","codigo":"18803000001","tipo":"ativo","icon":"💸","empresas":["nc"],"campos":["Saldo Inicial","Adiantamentos do Período","Baixas (Folha)","Saldo Razão"]},
    {"id":"nc-adto-13sal","nome":"Adiantamento de 13º Salário","codigo":"18803000002","tipo":"ativo","icon":"💸","empresas":["nc"],"campos":["Saldo Inicial","Adiantamentos do Período","Baixas (Folha)","Saldo Razão"]},
    {"id":"adto-fer","nome":"Adiantamento de Férias","codigo":"18803000003","tipo":"ativo","icon":"🏖️","empresas":["nc","mf"],"campos":["Saldo Inicial","Adiantamentos do Período","Baixas (Folha)","Saldo Razão"]},
    {"id":"nc-emp-conc","nome":"Empréstimos Concedidos","codigo":"18803000004","tipo":"ativo","icon":"💳","empresas":["nc"],"campos":["Saldo Inicial","Concessões do Período","Recebimentos","Saldo Razão"]},
    {"id":"nc-adto-func","nome":"Adiantamento a Funcionários - Desp. Admin.","codigo":"18805000002","tipo":"ativo","icon":"👤","empresas":["nc"],"campos":["Saldo Inicial","Adiantamentos do Período","Prestação de Contas","Saldo Razão"]},
    {"id":"adto-forn","nome":"Adiantamento a Fornecedores","codigo":"18805000003","tipo":"ativo","icon":"🏭","empresas":["nc","mf"],"campos":["Saldo Relatório Auxiliar (Contas a Pagar)","Saldo Razão"]},
    {"id":"nc-adto-boleto","nome":"Adiantamento de Boletos Multibeneficios","codigo":"18805000004","tipo":"ativo","icon":"📄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-adto-imob","nome":"Adiantamentos p/ Conta de Imobilizações","codigo":"18810000001","tipo":"ativo","icon":"🏗️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-csll-dif","nome":"CSLL - Valores Diferidos","codigo":"18825500002","tipo":"ativo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Pagamentos a Maior","Compensações","Saldo Razão"]},
    {"id":"nc-irpj-pago","nome":"IRPJ - Valores Pagos a Maior","codigo":"18825500003","tipo":"ativo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Pagamentos a Maior","Compensações","Saldo Razão"]},
    {"id":"nc-csll-pago","nome":"CSLL - Valores Pagos a Maior (LP)","codigo":"18825500004","tipo":"ativo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Pagamentos a Maior","Compensações","Saldo Razão"]},
    {"id":"nc-blq-bb","nome":"Bloqueio Judicial Banco do Brasil","codigo":"18840200001","tipo":"ativo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-blq-brad","nome":"Bloqueio Judicial Bradesco","codigo":"18840200004","tipo":"ativo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-blq-itau","nome":"Bloqueio Judicial Itaú","codigo":"18840200005","tipo":"ativo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-blq-banese","nome":"Bloqueio Judicial Banese","codigo":"18840200007","tipo":"ativo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-dep-trab","nome":"Depósito Judicial - Ações Trabalhistas","codigo":"18840209999","tipo":"ativo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-blq-bb2","nome":"Bloqueio Judicial BB - Ações Cíveis","codigo":"18840900001","tipo":"ativo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-dep-civel","nome":"Depósito Judicial - Ações Cíveis","codigo":"18840909999","tipo":"ativo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-irrf-serv-a","nome":"IRRF s/ Prestação de Serviço","codigo":"18845100001","tipo":"ativo","icon":"💰","empresas":["nc"],"campos":["Saldo Inicial","Retenções do Período","Compensações / Baixas","Saldo Razão"]},
    {"id":"nc-irrf-recup","nome":"IRRF a Recuperar","codigo":"18845100002","tipo":"ativo","icon":"💰","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"irrf-antec","nome":"IRRF Antecipado","codigo":"18845100003","tipo":"ativo","icon":"💰","empresas":["nc","mf"],"campos":["Saldo Inicial","Retenções do Período","Compensações / Baixas","Saldo Razão"]},
    {"id":"nc-csll-serv-a","nome":"CSLL s/ Prestação de Serviço","codigo":"18845200001","tipo":"ativo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","Retenções do Período","Compensações","Saldo Razão"]},
    {"id":"nc-csll-recup","nome":"CSLL a Recuperar","codigo":"18845200002","tipo":"ativo","icon":"📊","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-pis-serv-a","nome":"PIS s/ Prestação de Serviço","codigo":"18845900001","tipo":"ativo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","PIS Retido","Compensações","Saldo Razão"]},
    {"id":"nc-pis-recup","nome":"PIS a Recuperar","codigo":"18845900002","tipo":"ativo","icon":"📊","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-cofins-serv-a","nome":"COFINS s/ Prestação de Serviço","codigo":"18845900003","tipo":"ativo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","COFINS Retida","Compensações","Saldo Razão"]},
    {"id":"nc-cofins-recup","nome":"COFINS a Recuperar","codigo":"18845900004","tipo":"ativo","icon":"📊","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-iss-serv-a","nome":"ISS s/ Prestação de Serviço","codigo":"18845900005","tipo":"ativo","icon":"🏙️","empresas":["nc"],"campos":["Saldo Inicial","ISS Retido","Compensações","Saldo Razão"]},
    {"id":"nc-iss-fonte-a","nome":"ISS na Fonte a Realizar","codigo":"18845900006","tipo":"ativo","icon":"🏙️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-ret-interm","nome":"Retenções s/ Valores Intermediados","codigo":"18845900007","tipo":"ativo","icon":"💸","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-irrf-interm","nome":"IRRF s/ Valores Intermediados","codigo":"18845900011","tipo":"ativo","icon":"💸","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-irrf-aplic","nome":"IRRF s/ Aplicação","codigo":"18850000001","tipo":"ativo","icon":"📈","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-tit-rec-cp","nome":"Títulos a Receber (CP)","codigo":"18880100001","tipo":"ativo","icon":"📑","empresas":["nc"],"campos":["Saldo Inicial","Emissões","Recebimentos","Saldo Razão"]},
    {"id":"nc-trans-fat-cp","nome":"Transações a Faturar (CP)","codigo":"18880100002","tipo":"ativo","icon":"📑","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-tit-rec-lp","nome":"Títulos a Receber (LP)","codigo":"18880100004","tipo":"ativo","icon":"📑","empresas":["nc"],"campos":["Saldo Inicial","Emissões","Recebimentos","Saldo Razão"]},
    {"id":"nc-tit-rec-cp2","nome":"Títulos a Receber - Intermediados (CP)","codigo":"18880200001","tipo":"ativo","icon":"📑","empresas":["nc"],"campos":["Saldo Inicial","Emissões","Recebimentos","Saldo Razão"]},
    {"id":"nc-trans-fat-cp2","nome":"Transações a Faturar - Intermediados","codigo":"18880200002","tipo":"ativo","icon":"📑","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-tit-rec-lp2","nome":"Títulos a Receber LP - Intermediados","codigo":"18880200004","tipo":"ativo","icon":"📑","empresas":["nc"],"campos":["Saldo Inicial","Emissões","Recebimentos","Saldo Razão"]},
    {"id":"nc-ativo-acg","nome":"Ativo - ACG","codigo":"18880200006","tipo":"ativo","icon":"📑","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-sirius","nome":"Sirius Investimentos","codigo":"18885000001","tipo":"ativo","icon":"🏢","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-ponta","nome":"Ponta das Caieiras","codigo":"18885000002","tipo":"ativo","icon":"🏢","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-rv-tec","nome":"RV Tecnologia","codigo":"18885000003","tipo":"ativo","icon":"🏢","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-maxi-invest","nome":"Maxifrota Serviços de Manutenção de Frota","codigo":"18885000006","tipo":"ativo","icon":"🚛","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-ret-maxi","nome":"Retenção Valores Intermediados Maxifrota","codigo":"18885000007","tipo":"ativo","icon":"🚛","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-canopus","nome":"Canopus Investimentos e Participações S.A","codigo":"18885000008","tipo":"ativo","icon":"🏢","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-rosane","nome":"Rosane de Freitas Manica","codigo":"18892000001","tipo":"ativo","icon":"👤","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-outros-rec","nome":"Outros Valores a Receber","codigo":"18892000003","tipo":"ativo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Novos Valores","Recebimentos","Saldo Razão"]},
    {"id":"nc-caucoes-a","nome":"Cauções","codigo":"18892000004","tipo":"ativo","icon":"🔒","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-chargeback-a","nome":"Chargeback","codigo":"18892000005","tipo":"ativo","icon":"↩️","empresas":["nc"],"campos":["Saldo Inicial","Chargebacks do Período","Recuperações","Saldo Razão"]},
    {"id":"nc-canopus2","nome":"Canopus Invest. e Participações S.A (2)","codigo":"18892000006","tipo":"ativo","icon":"🏢","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-outros-cp","nome":"Outros (CP)","codigo":"19810990000","tipo":"ativo","icon":"📋","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-mat-consumo","nome":"Materiais de Consumo","codigo":"19840000001","tipo":"ativo","icon":"📦","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-seguros","nome":"Seguros a Apropriar","codigo":"19910000001","tipo":"ativo","icon":"🛡️","empresas":["nc"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"nc-assinatura","nome":"Assinatura de Periódicos","codigo":"19910000002","tipo":"ativo","icon":"📰","empresas":["nc"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"nc-contrato-man","nome":"Contrato de Manutenção","codigo":"19910000003","tipo":"ativo","icon":"🔧","empresas":["nc"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"nc-iptu","nome":"IPTU","codigo":"19910000004","tipo":"ativo","icon":"🏠","empresas":["nc"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"nc-desp-antec","nome":"Despesas Antecipadas Diversas","codigo":"19910009999","tipo":"ativo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"nc-maxi-invest2","nome":"Maxifrota Serv. Manutenção de Frota Ltda","codigo":"21990000002","tipo":"ativo","icon":"🚛","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-terreno","nome":"Terreno","codigo":"21990000003","tipo":"ativo","icon":"🏗️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-moveis","nome":"Móveis e Utensílios","codigo":"22530100001","tipo":"ativo","icon":"🪑","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-benfeitorias","nome":"Benfeitorias em Imóveis de Terceiros","codigo":"22550000001","tipo":"ativo","icon":"🏠","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-equip-ti","nome":"Equipamentos de Processamento de Dados","codigo":"22530200001","tipo":"ativo","icon":"💻","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-maquinas","nome":"Máquinas e Equipamentos","codigo":"22530900001","tipo":"ativo","icon":"⚙️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-dep-moveis","nome":"Depreciação Móveis/Utensílios (-)","codigo":"22599300001","tipo":"ativo","icon":"📉","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-dep-maq","nome":"Depreciação Máquinas/Equipamentos (-)","codigo":"22599300002","tipo":"ativo","icon":"📉","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-dep-benf","nome":"(-) Benfeitorias em Imóveis de Terceiros","codigo":"22599500001","tipo":"ativo","icon":"📉","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-dep-ti","nome":"Depreciação Equipamentos de Processamento (-)","codigo":"22599900001","tipo":"ativo","icon":"📉","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-amort-imov","nome":"(-) Amortização Gastos em Imóv. Terceiros","codigo":"24199200001","tipo":"ativo","icon":"📉","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-sw-adq","nome":"Software - Adquiridos","codigo":"25115100001","tipo":"ativo","icon":"💾","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-sw-gen","nome":"Software - Gerados Internamente","codigo":"25115200001","tipo":"ativo","icon":"💾","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-marcas","nome":"Marcas","codigo":"25130000001","tipo":"ativo","icon":"®️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-desenv-prod","nome":"Desenvolvimento de Produtos","codigo":"25190000001","tipo":"ativo","icon":"🔬","empresas":["nc"],"campos":["Saldo Inicial","Adições","Baixas","Saldo Razão"]},
    {"id":"nc-intang-desenv","nome":"Intangível em Desenvolvimento","codigo":"25198000005","tipo":"ativo","icon":"🔬","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-amort-intang","nome":"Amort. Acumulada de Ativos Intangíveis","codigo":"25199000002","tipo":"ativo","icon":"📉","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-amort-sw","nome":"(-) Amortização Softwares","codigo":"25199150001","tipo":"ativo","icon":"📉","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    # ══ NUTRICASH — PASSIVO ══
    {"id":"nc-emp-brad","nome":"Empréstimo Bradesco","codigo":"46210100002","tipo":"passivo","icon":"🏦","empresas":["nc"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"nc-emp-bb","nome":"Empréstimo Banco do Brasil","codigo":"46210100005","tipo":"passivo","icon":"🏦","empresas":["nc"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"nc-emp-sant","nome":"Empréstimo Santander","codigo":"46210100006","tipo":"passivo","icon":"🏦","empresas":["nc"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"nc-leas-cp","nome":"Leasing CP - Bradesco","codigo":"46210100007","tipo":"passivo","icon":"🏦","empresas":["nc"],"campos":["Saldo Inicial","Novos Contratos","Amortizações","Saldo Razão"]},
    {"id":"nc-leas-lp","nome":"Leasing LP - Bradesco","codigo":"46210100009","tipo":"passivo","icon":"🏦","empresas":["nc"],"campos":["Saldo Inicial","Novos Contratos","Amortizações","Saldo Razão"]},
    {"id":"nc-emp-bndes","nome":"Empréstimo BNDES","codigo":"46210100011","tipo":"passivo","icon":"🏦","empresas":["nc"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"nc-jcp","nome":"Juros sobre Capital Próprio","codigo":"49310000002","tipo":"passivo","icon":"💰","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-irpj-rec","nome":"Imposto de Renda a Recolher","codigo":"49410000001","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","IRPJ Apurado","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"nc-csll-rec","nome":"Contribuição Social a Recolher","codigo":"49410000002","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","CSLL Apurada","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"irrf-serv","nome":"IRRF s/ Serviços a Recolher (1708)","codigo":"49420100001","tipo":"passivo","icon":"📋","empresas":["nc","mf"],"campos":["Saldo Inicial","IRRF Retido no Período","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"irrf-com","nome":"IRRF s/ Comissões a Recolher (8045)","codigo":"49420100002","tipo":"passivo","icon":"📋","empresas":["nc","mf"],"campos":["Saldo Inicial","IRRF Retido no Período","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"nc-piscofins-serv","nome":"PIS/COFINS/CSLL s/ Serviços (5952)","codigo":"49420100003","tipo":"passivo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","Retenções do Período","Recolhimentos","Saldo Razão"]},
    {"id":"nc-inss-serv","nome":"INSS s/ Serviços a Recolher","codigo":"49420100004","tipo":"passivo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","INSS Retido","Recolhimentos (GPS)","Saldo Razão"]},
    {"id":"nc-irrf-serv2","nome":"IRRF s/ Serviços a Recolher (0588)","codigo":"49420100005","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","IRRF Retido no Período","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"nc-iss-fonte-p","nome":"ISS Retido na Fonte","codigo":"49420100007","tipo":"passivo","icon":"🏙️","empresas":["nc"],"campos":["Saldo Inicial","ISS Retido","Recolhimentos","Saldo Razão"]},
    {"id":"nc-inss-rec","nome":"INSS a Recolher","codigo":"49420200001","tipo":"passivo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","INSS Apurado","Recolhimentos (GPS)","Saldo Razão"]},
    {"id":"nc-fgts-rec","nome":"FGTS a Recolher","codigo":"49420200002","tipo":"passivo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","FGTS Apurado","Recolhimentos","Saldo Razão"]},
    {"id":"nc-irrf-trabalho","nome":"IRRF s/ Rendimento Trabalho Assalariado (0561)","codigo":"49420200003","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","IRRF Retido","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"nc-sind","nome":"Contribuição Sindical a Recolher","codigo":"49420200004","tipo":"passivo","icon":"🤝","empresas":["nc"],"campos":["Saldo Inicial","Contribuições Apuradas","Recolhimentos","Saldo Razão"]},
    {"id":"pis","nome":"PIS a Recolher","codigo":"49420900001","tipo":"passivo","icon":"📊","empresas":["nc","mf"],"campos":["Saldo Inicial","PIS Apurado","Recolhimentos","Saldo Razão"]},
    {"id":"cofins","nome":"COFINS a Recolher","codigo":"49420900002","tipo":"passivo","icon":"📊","empresas":["nc","mf"],"campos":["Saldo Inicial","COFINS Apurado","Recolhimentos","Saldo Razão"]},
    {"id":"iss","nome":"ISS a Recolher","codigo":"49420900003","tipo":"passivo","icon":"🏙️","empresas":["nc","mf"],"campos":["Saldo Inicial","ISS Apurado","Recolhimentos","Saldo Razão"]},
    {"id":"nc-iof-mutuo","nome":"IOF a Recolher s/ Mútuo","codigo":"49420900004","tipo":"passivo","icon":"💰","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-parcel-fed","nome":"Parcelamento Admin. Débitos Federais CP","codigo":"49420900005","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Parcelas Vencidas","Pagamentos","Saldo Razão"]},
    {"id":"nc-refis","nome":"Parcelas Adesão ao REFIS IV","codigo":"49420900006","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Parcelas Vencidas","Pagamentos","Saldo Razão"]},
    {"id":"nc-parcel-fed-lp","nome":"Parcelamento Admin. Débitos Federais LP","codigo":"49420900007","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Parcelas Vencidas","Pagamentos","Saldo Razão"]},
    {"id":"nc-parcel-mun","nome":"Parcelamento Admin. Débitos Municipais","codigo":"49420900009","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Parcelas Vencidas","Pagamentos","Saldo Razão"]},
    {"id":"nc-emp-bndes-lp","nome":"Empréstimo Longo Prazo - BNDES","codigo":"49420900008","tipo":"passivo","icon":"🏦","empresas":["nc"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"nc-sal-pagar","nome":"Salários/Ordenados a Pagar","codigo":"49930100001","tipo":"passivo","icon":"💸","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-indeniz","nome":"Indenizações Trabalhistas a Pagar","codigo":"49930100002","tipo":"passivo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Inicial","Novas Indenizações","Pagamentos","Saldo Razão"]},
    {"id":"nc-pensao","nome":"Pensão Alimentícia a Pagar","codigo":"49930100003","tipo":"passivo","icon":"👨‍👧","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-prov-13sal","nome":"Provisão de 13º Salário a Pagar","codigo":"49930100004","tipo":"passivo","icon":"💸","empresas":["nc"],"campos":["Saldo Inicial","Provisões do Período","Pagamentos","Saldo Razão"]},
    {"id":"nc-prov-fer","nome":"Provisão de Férias a Pagar","codigo":"49930100007","tipo":"passivo","icon":"🏖️","empresas":["nc"],"campos":["Saldo Inicial","Provisões do Período","Pagamentos","Saldo Razão"]},
    {"id":"nc-prov-inss-fer","nome":"Provisão INSS Férias","codigo":"49930100008","tipo":"passivo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","Provisões do Período","Pagamentos","Saldo Razão"]},
    {"id":"nc-prov-fgts-fer","nome":"Provisão FGTS Férias","codigo":"49930100009","tipo":"passivo","icon":"📊","empresas":["nc"],"campos":["Saldo Inicial","Provisões do Período","Pagamentos","Saldo Razão"]},
    {"id":"nc-folha-pagar","nome":"Folha a Pagar","codigo":"49930100011","tipo":"passivo","icon":"💸","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-cont-trab","nome":"Provisão Contingências Trabalhistas","codigo":"49935100001","tipo":"passivo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Inicial","Novas Provisões","Reversões/Pagamentos","Saldo Razão"]},
    {"id":"nc-cont-civel","nome":"Provisão Contingências Cíveis","codigo":"49935900001","tipo":"passivo","icon":"⚖️","empresas":["nc"],"campos":["Saldo Inicial","Novas Provisões","Reversões/Pagamentos","Saldo Razão"]},
    {"id":"nc-maxi-p","nome":"Maxifrota Serviços de Manutenção de Frota","codigo":"49985000005","tipo":"passivo","icon":"🚛","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"forn","nome":"Fornecedores","codigo":"49992000001","tipo":"passivo","icon":"🤝","empresas":["nc","mf"],"campos":["Saldo Inicial","NF Recebidas","Pagamentos Realizados","Saldo Razão"]},
    {"id":"rede-conv","nome":"Rede Conveniada a Pagar","codigo":"49992000002","tipo":"passivo","icon":"🏪","empresas":["nc"],"campos":["Saldo Inicial","Transações do Período","Repasses Realizados","Saldo Razão"]},
    {"id":"nc-moeda-pat","nome":"Moeda Eletrônica - PAT","codigo":"49992000003","tipo":"passivo","icon":"💳","empresas":["nc"],"campos":["Saldo Inicial","Emissões do Período","Resgates / Utilizações","Saldo Razão"]},
    {"id":"nc-moeda-frota","nome":"Moeda Eletrônica - Frota","codigo":"49992000004","tipo":"passivo","icon":"⛽","empresas":["nc"],"campos":["Saldo Inicial","Emissões do Período","Resgates / Utilizações","Saldo Razão"]},
    {"id":"nc-moeda-prem","nome":"Moeda Eletrônica - Nutricash Premium","codigo":"49992000005","tipo":"passivo","icon":"⭐","empresas":["nc"],"campos":["Saldo Inicial","Emissões do Período","Resgates / Utilizações","Saldo Razão"]},
    {"id":"nc-trans-pre-pat","nome":"Transitória Transações Pré - PAT","codigo":"49992000007","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-trans-pre-frota","nome":"Transitória Transações Pré - Frota","codigo":"49992000008","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-trans-pre-prem","nome":"Transitória Transações Pré - NC Premium","codigo":"49992000009","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-trans-pos-frota","nome":"Transitória Transações Pós - Frota Abastec.","codigo":"49992000011","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-trans-multi","nome":"Transitória Transações Pós - Multibeneficios","codigo":"49992000013","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-adto-cli","nome":"Adiantamento de Clientes","codigo":"49992000014","tipo":"passivo","icon":"💰","empresas":["nc"],"campos":["Saldo Inicial","Novos Adiantamentos","Amortizações","Saldo Razão"]},
    {"id":"nc-caucao-cli","nome":"Caução de Clientes","codigo":"49992000015","tipo":"passivo","icon":"🔒","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-emp-consig","nome":"Empréstimo Consignado Colaboradores","codigo":"49992000016","tipo":"passivo","icon":"💳","empresas":["nc"],"campos":["Saldo Inicial","Novos Consignados","Amortizações","Saldo Razão"]},
    {"id":"nc-vt","nome":"Vale Transporte","codigo":"49992000017","tipo":"passivo","icon":"🚌","empresas":["nc"],"campos":["Saldo Inicial","Emissões do Período","Utilizações","Saldo Razão"]},
    {"id":"nc-trans-fat-rede","nome":"Transitória de Faturamento de Rede","codigo":"49992000019","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"moeda-pat","nome":"Moeda Eletrônica PAT Papel","codigo":"49992000022","tipo":"passivo","icon":"💳","empresas":["nc"],"campos":["Saldo Inicial","Emissões do Período","Resgates / Utilizações","Saldo Razão"]},
    {"id":"nc-trans-antec","nome":"Transitória de Antecipado","codigo":"49992000024","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-trans-imob","nome":"Transitória Bens a Imobilizar","codigo":"49992000025","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-trans-enc","nome":"Transitória de Encontro de Contas","codigo":"49992000026","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-desc-vt","nome":"Desconto por Carga Vencida VT","codigo":"49992000028","tipo":"passivo","icon":"🚌","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-moeda-yuo","nome":"Moeda Eletrônica - YUO","codigo":"49992000030","tipo":"passivo","icon":"📱","empresas":["nc"],"campos":["Saldo Inicial","Emissões do Período","Resgates / Utilizações","Saldo Razão"]},
    {"id":"nc-trans-yuo","nome":"Transitória Transação - YUO","codigo":"49992000031","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-cred-reimb","nome":"Credenciado a Reembolsar","codigo":"49992000096","tipo":"passivo","icon":"💸","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-trans-cr","nome":"Transitória Contas a Receber","codigo":"49992000097","tipo":"passivo","icon":"🔄","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-outras-cp","nome":"Outras Contas a Pagar","codigo":"49992000099","tipo":"passivo","icon":"📋","empresas":["nc"],"campos":["Saldo Inicial","Novos Valores","Pagamentos","Saldo Razão"]},
    {"id":"nc-cotas","nome":"Cotas","codigo":"61110280001","tipo":"passivo","icon":"🏛️","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-lucros","nome":"Lucros/Prejuízos Acumulados","codigo":"61810000001","tipo":"passivo","icon":"📊","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"nc-div-lucros","nome":"Dividendos e Lucros Pagos Antecipadamente (-)","codigo":"61880000001","tipo":"passivo","icon":"💰","empresas":["nc"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    # ══ MAXIFROTA — ATIVO ══
    {"id":"mf-caixa","nome":"Caixa","codigo":"11110000001","tipo":"ativo","icon":"💵","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-bb-21122","nome":"Banco do Brasil - 21122-2","codigo":"11230000002","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-sant-13005708","nome":"Banco Santander - 13005708-6","codigo":"11230000101","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-cef-2617","nome":"Caixa Econômica Federal - 2617-5","codigo":"11230000201","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-brad-2901","nome":"Bradesco - 000290 1-7","codigo":"11230000301","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-safra-401811","nome":"Safra - 401811-6","codigo":"11230000400","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-banese-130695","nome":"Banese - 130695-9","codigo":"11230000501","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-itau-60527","nome":"Itaú - 60527-5","codigo":"11230000605","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-itau-36651","nome":"Itaú - 36651-1","codigo":"11230000606","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-itau-36985","nome":"Itaú - 36985-3","codigo":"11230000607","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-daycoval","nome":"Banco Daycoval - 749245-8","codigo":"11230000608","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-itau-00986920","nome":"Itaú - 00986920","codigo":"11230000611","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-sofisa","nome":"Banco Sofisa - 52-1","codigo":"11230000950","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-sicredi","nome":"Banco Cooperativa Sicredi S.A. - 01182-3","codigo":"11230000960","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-transpocred","nome":"Transpocred","codigo":"11230001001","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-sifra","nome":"Sifra","codigo":"11230001200","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-xp","nome":"XP Investimentos - 460077-8","codigo":"11230000800","tipo":"ativo","icon":"🏦","empresas":["mf"],"campos":["Saldo Sistema","Saldo Extrato Bancário","Saldo Razão"]},
    {"id":"mf-apl-itau","nome":"Itaú 60527 - Aplicação","codigo":"13115300001","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-sant","nome":"Santander 13005708-6 - Aplicação","codigo":"13115300201","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-safra","nome":"Safra - Aplicação","codigo":"13115300101","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-bb","nome":"Banco do Brasil - Aplicação","codigo":"13115300300","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-brad","nome":"Bradesco 2901 - Aplicação","codigo":"13115300500","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-xp","nome":"XP Investimentos - Aplicação","codigo":"13115300700","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-day1","nome":"Daycoval - Aplicação 1","codigo":"13115300701","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-day2","nome":"Daycoval - Aplicação 2","codigo":"13115300702","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-sofisa","nome":"Banco Sofisa - Aplicação","codigo":"13115300900","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-apl-sicredi","nome":"Sicredi - Aplicação","codigo":"13115300960","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-adto-sal","nome":"Adiantamento de Salários","codigo":"18803000001","tipo":"ativo","icon":"💸","empresas":["mf"],"campos":["Saldo Inicial","Adiantamentos do Período","Baixas (Folha)","Saldo Razão"]},
    {"id":"mf-adto-13sal","nome":"Adiantamento de 13º Salário","codigo":"18803000002","tipo":"ativo","icon":"💸","empresas":["mf"],"campos":["Saldo Inicial","Adiantamentos do Período","Baixas (Folha)","Saldo Razão"]},
    {"id":"mf-adto-fer2","nome":"Adiantamento de Férias","codigo":"18803000003","tipo":"ativo","icon":"🏖️","empresas":["mf"],"campos":["Saldo Inicial","Adiantamentos do Período","Baixas (Folha)","Saldo Razão"]},
    {"id":"mf-emp-conc","nome":"Empréstimos Concedidos","codigo":"18803000004","tipo":"ativo","icon":"💳","empresas":["mf"],"campos":["Saldo Inicial","Concessões do Período","Recebimentos","Saldo Razão"]},
    {"id":"mf-adto-viagem","nome":"Adiantamento para Viagens","codigo":"18805000001","tipo":"ativo","icon":"✈️","empresas":["mf"],"campos":["Saldo Inicial","Adiantamentos do Período","Prestação de Contas","Saldo Razão"]},
    {"id":"mf-adto-func","nome":"Adiantamento a Funcionários - Desp. Admin.","codigo":"18805000002","tipo":"ativo","icon":"👤","empresas":["mf"],"campos":["Saldo Inicial","Adiantamentos do Período","Prestação de Contas","Saldo Razão"]},
    {"id":"mf-adto-forn2","nome":"Adiantamento a Fornecedores","codigo":"18805000003","tipo":"ativo","icon":"🏭","empresas":["mf"],"campos":["Saldo Relatório Auxiliar (Contas a Pagar)","Saldo Razão"]},
    {"id":"mf-irpj-dif","nome":"IRPJ - Valores Diferidos","codigo":"18825500001","tipo":"ativo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos a Maior","Compensações","Saldo Razão"]},
    {"id":"mf-csll-dif","nome":"CSLL - Valores Diferidos","codigo":"18825500002","tipo":"ativo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos a Maior","Compensações","Saldo Razão"]},
    {"id":"mf-irpj-pago","nome":"IRPJ - Valores Pagos a Maior","codigo":"18825500003","tipo":"ativo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos a Maior","Compensações","Saldo Razão"]},
    {"id":"mf-csll-pago","nome":"CSLL - Valores Pagos a Maior (LP)","codigo":"18825500004","tipo":"ativo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos a Maior","Compensações","Saldo Razão"]},
    {"id":"mf-adto-imob","nome":"Adiantamentos p/ Conta de Imobilizações","codigo":"18810000001","tipo":"ativo","icon":"🏗️","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-dep-trab","nome":"Depósito Judicial - Ações Trabalhistas","codigo":"18840209999","tipo":"ativo","icon":"⚖️","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-irrf-recup","nome":"IRRF a Recuperar","codigo":"18845100002","tipo":"ativo","icon":"💰","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-irrf-serv-a","nome":"IRRF s/ Prestação de Serviço","codigo":"18845100001","tipo":"ativo","icon":"💰","empresas":["mf"],"campos":["Saldo Inicial","Retenções do Período","Compensações / Baixas","Saldo Razão"]},
    {"id":"mf-irrf-antec2","nome":"IRRF Antecipado","codigo":"18845100003","tipo":"ativo","icon":"💰","empresas":["mf"],"campos":["Saldo Inicial","Retenções do Período","Compensações / Baixas","Saldo Razão"]},
    {"id":"mf-csll-serv-a","nome":"CSLL s/ Prestação de Serviço","codigo":"18845200001","tipo":"ativo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","Retenções do Período","Compensações","Saldo Razão"]},
    {"id":"mf-csll-recup","nome":"CSLL a Recuperar","codigo":"18845200002","tipo":"ativo","icon":"📊","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-pis-recup","nome":"PIS a Recuperar","codigo":"18845900002","tipo":"ativo","icon":"📊","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-cofins-recup","nome":"COFINS a Recuperar","codigo":"18845900004","tipo":"ativo","icon":"📊","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-pis-serv-a","nome":"PIS s/ Prestação de Serviço","codigo":"18845900001","tipo":"ativo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","PIS Retido","Compensações","Saldo Razão"]},
    {"id":"mf-cofins-serv-a","nome":"COFINS s/ Prestação de Serviço","codigo":"18845900003","tipo":"ativo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","COFINS Retida","Compensações","Saldo Razão"]},
    {"id":"mf-iss-serv-a","nome":"ISS s/ Prestação de Serviço","codigo":"18845900005","tipo":"ativo","icon":"🏙️","empresas":["mf"],"campos":["Saldo Inicial","ISS Retido","Compensações","Saldo Razão"]},
    {"id":"mf-iss-fonte-a","nome":"ISS na Fonte a Realizar","codigo":"18845900006","tipo":"ativo","icon":"🏙️","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-iss-recup","nome":"ISS a Recuperar","codigo":"18845900009","tipo":"ativo","icon":"🏙️","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-ret-interm","nome":"Retenções s/ Valores Intermediados","codigo":"18845900007","tipo":"ativo","icon":"💸","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-iof-recup","nome":"IOF a Recuperar","codigo":"18845900010","tipo":"ativo","icon":"💰","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-irrf-interm","nome":"IRRF s/ Valores Intermediados","codigo":"18845900011","tipo":"ativo","icon":"💸","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-pis-recup-lp","nome":"PIS a Recuperar LP","codigo":"18845900012","tipo":"ativo","icon":"📊","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-cofins-recup-lp","nome":"COFINS a Recuperar LP","codigo":"18845900013","tipo":"ativo","icon":"📊","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-irrf-aplic","nome":"IRRF s/ Aplicação","codigo":"18850000001","tipo":"ativo","icon":"📈","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-tit-rec-cp","nome":"Títulos a Receber (CP)","codigo":"18880100001","tipo":"ativo","icon":"📑","empresas":["mf"],"campos":["Saldo Inicial","Emissões","Recebimentos","Saldo Razão"]},
    {"id":"mf-trans-fat-cp","nome":"Transações a Faturar (CP)","codigo":"18880100002","tipo":"ativo","icon":"📑","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-emissor-nc-cp","nome":"Emissor Nutricash (CP)","codigo":"18880100005","tipo":"ativo","icon":"📑","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-tit-rec-cp2","nome":"Títulos a Receber - Intermediados (CP)","codigo":"18880200001","tipo":"ativo","icon":"📑","empresas":["mf"],"campos":["Saldo Inicial","Emissões","Recebimentos","Saldo Razão"]},
    {"id":"mf-trans-fat-cp2","nome":"Transações a Faturar - Intermediados","codigo":"18880200002","tipo":"ativo","icon":"📑","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-emissor-nc-lp","nome":"Emissor Nutricash (LP) - 18880200005","codigo":"18880200005","tipo":"ativo","icon":"📑","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-sirius","nome":"Sirius Investimentos","codigo":"18885000001","tipo":"ativo","icon":"🏢","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-ponta","nome":"Ponta das Caieiras","codigo":"18885000002","tipo":"ativo","icon":"🏢","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-rv-tec","nome":"RV Tecnologia","codigo":"18885000003","tipo":"ativo","icon":"🏢","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-outros-rec","nome":"Outros Valores a Receber","codigo":"18892000003","tipo":"ativo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","Novos Valores","Recebimentos","Saldo Razão"]},
    {"id":"mf-nutricash-invest","nome":"Nutricash Serviços Ltda","codigo":"18885000005","tipo":"ativo","icon":"🏢","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-caucoes-a","nome":"Cauções","codigo":"18892000004","tipo":"ativo","icon":"🔒","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-chargeback-a","nome":"Chargeback","codigo":"18892000005","tipo":"ativo","icon":"↩️","empresas":["mf"],"campos":["Saldo Inicial","Chargebacks do Período","Recuperações","Saldo Razão"]},
    {"id":"mf-seguros","nome":"Seguros a Apropriar","codigo":"19910000001","tipo":"ativo","icon":"🛡️","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"mf-assinatura","nome":"Assinatura de Periódicos","codigo":"19910000002","tipo":"ativo","icon":"📰","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"mf-contrato-man","nome":"Contrato de Manutenção","codigo":"19910000003","tipo":"ativo","icon":"🔧","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"mf-iptu","nome":"IPTU","codigo":"19910000004","tipo":"ativo","icon":"🏠","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"mf-desp-antec","nome":"Despesas Antecipadas Diversas","codigo":"19910009999","tipo":"ativo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","Pagamentos","Apropriações do Período","Saldo Razão"]},
    {"id":"mf-moveis","nome":"Móveis e Utensílios","codigo":"22530100001","tipo":"ativo","icon":"🪑","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-benfeitorias","nome":"Benfeitorias em Imóveis de Terceiros","codigo":"22550000001","tipo":"ativo","icon":"🏠","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-equip-ti","nome":"Equipamentos de Processamento de Dados","codigo":"22530200001","tipo":"ativo","icon":"💻","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-maquinas","nome":"Máquinas e Equipamentos","codigo":"22530900001","tipo":"ativo","icon":"⚙️","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-dep-moveis","nome":"Depreciação Móveis/Utensílios (-)","codigo":"22599300001","tipo":"ativo","icon":"📉","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-dep-maq","nome":"Depreciação Máquinas/Equipamentos (-)","codigo":"22599300002","tipo":"ativo","icon":"📉","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-dep-benf","nome":"(-) Benfeitorias em Imóveis de Terceiros","codigo":"22599500001","tipo":"ativo","icon":"📉","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-dep-ti","nome":"Depreciação Equipamentos de Processamento (-)","codigo":"22599900001","tipo":"ativo","icon":"📉","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-sw-adq","nome":"Software - Adquiridos","codigo":"25115100001","tipo":"ativo","icon":"💾","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-sw-gen","nome":"Software - Gerados Internamente","codigo":"25115200001","tipo":"ativo","icon":"💾","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-marcas","nome":"Marcas","codigo":"25130000001","tipo":"ativo","icon":"®️","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-marcas-pat","nome":"Marcas e Patentes","codigo":"25198000004","tipo":"ativo","icon":"®️","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-intang-desenv","nome":"Intangível em Desenvolvimento","codigo":"25198000005","tipo":"ativo","icon":"🔬","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-amort-intang","nome":"Amort. Acumulada de Ativos Intangíveis","codigo":"25199000002","tipo":"ativo","icon":"📉","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-amort-sw","nome":"(-) Amortização Softwares","codigo":"25199150001","tipo":"ativo","icon":"📉","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    # ══ MAXIFROTA — PASSIVO ══
    {"id":"mf-emp-bb","nome":"Empréstimo Banco do Brasil","codigo":"46210100005","tipo":"passivo","icon":"🏦","empresas":["mf"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"mf-emp-sant","nome":"Empréstimo Santander","codigo":"46210100006","tipo":"passivo","icon":"🏦","empresas":["mf"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"mf-emp-daycoval","nome":"Empréstimo Daycoval - 749245-8","codigo":"46210100013","tipo":"passivo","icon":"🏦","empresas":["mf"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"mf-emp-sofisa","nome":"Empréstimo Sofisa","codigo":"46210100014","tipo":"passivo","icon":"🏦","empresas":["mf"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"mf-emp-sicredi","nome":"Empréstimo Sicredi S.A.","codigo":"46210100015","tipo":"passivo","icon":"🏦","empresas":["mf"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"mf-emp-itau","nome":"Empréstimo Itaú - 91075-8","codigo":"46210100012","tipo":"passivo","icon":"🏦","empresas":["mf"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"mf-emp-safra","nome":"Empréstimo Safra","codigo":"46210100003","tipo":"passivo","icon":"🏦","empresas":["mf"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"mf-irpj-rec","nome":"Imposto de Renda a Recolher","codigo":"49410000001","tipo":"passivo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","IRPJ Apurado","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"mf-csll-rec","nome":"Contribuição Social a Recolher","codigo":"49410000002","tipo":"passivo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","CSLL Apurada","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"mf-irrf-serv2","nome":"IRRF s/ Serviços a Recolher (1708)","codigo":"49420100001","tipo":"passivo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","IRRF Retido no Período","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"mf-irrf-com2","nome":"IRRF s/ Comissões a Recolher (8045)","codigo":"49420100002","tipo":"passivo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","IRRF Retido no Período","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"mf-piscofins-serv","nome":"PIS/COFINS/CSLL s/ Serviços (5952)","codigo":"49420100003","tipo":"passivo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","Retenções do Período","Recolhimentos","Saldo Razão"]},
    {"id":"mf-inss-serv","nome":"INSS s/ Serviços a Recolher","codigo":"49420100004","tipo":"passivo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","INSS Retido","Recolhimentos (GPS)","Saldo Razão"]},
    {"id":"mf-iss-fonte-p","nome":"ISS Retido na Fonte","codigo":"49420100007","tipo":"passivo","icon":"🏙️","empresas":["mf"],"campos":["Saldo Inicial","ISS Retido","Recolhimentos","Saldo Razão"]},
    {"id":"mf-irrf-serv-3426","nome":"IRRF s/ Serviços a Recolher (3426)","codigo":"49420100009","tipo":"passivo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","IRRF Retido no Período","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"mf-inss-rec","nome":"INSS a Recolher","codigo":"49420200001","tipo":"passivo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","INSS Apurado","Recolhimentos (GPS)","Saldo Razão"]},
    {"id":"mf-fgts-rec","nome":"FGTS a Recolher","codigo":"49420200002","tipo":"passivo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","FGTS Apurado","Recolhimentos","Saldo Razão"]},
    {"id":"mf-irrf-trabalho","nome":"IRRF s/ Rendimento Trabalho Assalariado (0561)","codigo":"49420200003","tipo":"passivo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","IRRF Retido","Recolhimentos (DARF)","Saldo Razão"]},
    {"id":"mf-sind","nome":"Contribuição Sindical a Recolher","codigo":"49420200004","tipo":"passivo","icon":"🤝","empresas":["mf"],"campos":["Saldo Inicial","Contribuições Apuradas","Recolhimentos","Saldo Razão"]},
    {"id":"mf-pis2","nome":"PIS a Recolher","codigo":"49420900001","tipo":"passivo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","PIS Apurado","Recolhimentos","Saldo Razão"]},
    {"id":"mf-cofins2","nome":"COFINS a Recolher","codigo":"49420900002","tipo":"passivo","icon":"📊","empresas":["mf"],"campos":["Saldo Inicial","COFINS Apurado","Recolhimentos","Saldo Razão"]},
    {"id":"mf-iss2","nome":"ISS a Recolher","codigo":"49420900003","tipo":"passivo","icon":"🏙️","empresas":["mf"],"campos":["Saldo Inicial","ISS Apurado","Recolhimentos","Saldo Razão"]},
    {"id":"mf-iof-mutuo","nome":"IOF a Recolher s/ Mútuo","codigo":"49420900004","tipo":"passivo","icon":"💰","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-parcel-mun","nome":"Parcelamento Admin. Débitos Municipais","codigo":"49420900009","tipo":"passivo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","Parcelas Vencidas","Pagamentos","Saldo Razão"]},
    {"id":"mf-emp-sofisa-lp","nome":"Empréstimo Longo Prazo - Sofisa","codigo":"49420900010","tipo":"passivo","icon":"🏦","empresas":["mf"],"campos":["Saldo Inicial","Novos Empréstimos","Amortizações","Saldo Razão"]},
    {"id":"mf-sal-pagar","nome":"Salários/Ordenados a Pagar","codigo":"49930100001","tipo":"passivo","icon":"💸","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-afac","nome":"AFAC - Adiantamento para Futuro Aumento de Capital","codigo":"49915000001","tipo":"passivo","icon":"💰","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-indeniz","nome":"Indenizações Trabalhistas a Pagar","codigo":"49930100002","tipo":"passivo","icon":"⚖️","empresas":["mf"],"campos":["Saldo Inicial","Novas Indenizações","Pagamentos","Saldo Razão"]},
    {"id":"mf-pensao","nome":"Pensão Alimentícia a Pagar","codigo":"49930100003","tipo":"passivo","icon":"👨‍👧","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-prov-13sal","nome":"Provisão de 13º Salário a Pagar","codigo":"49930100004","tipo":"passivo","icon":"💸","empresas":["mf"],"campos":["Saldo Inicial","Provisões do Período","Pagamentos","Saldo Razão"]},
    {"id":"mf-prov-fer","nome":"Provisão de Férias a Pagar","codigo":"49930100007","tipo":"passivo","icon":"🏖️","empresas":["mf"],"campos":["Saldo Inicial","Provisões do Período","Pagamentos","Saldo Razão"]},
    {"id":"mf-sirius-p","nome":"Sirius Investimentos","codigo":"49985000001","tipo":"passivo","icon":"🏢","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-rv-p","nome":"RV Tecnologia","codigo":"49985000002","tipo":"passivo","icon":"🏢","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-folha-pagar","nome":"Folha a Pagar","codigo":"49930100011","tipo":"passivo","icon":"💸","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-cont-trab","nome":"Provisão Contingências Trabalhistas","codigo":"49935100001","tipo":"passivo","icon":"⚖️","empresas":["mf"],"campos":["Saldo Inicial","Novas Provisões","Reversões/Pagamentos","Saldo Razão"]},
    {"id":"mf-nutricash-p","nome":"Nutricash Serviços Ltda","codigo":"49985000003","tipo":"passivo","icon":"🏢","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-forn2","nome":"Fornecedores","codigo":"49992000001","tipo":"passivo","icon":"🤝","empresas":["mf"],"campos":["Saldo Inicial","NF Recebidas","Pagamentos Realizados","Saldo Razão"]},
    {"id":"mf-rede-conv","nome":"Rede Conveniada a Pagar","codigo":"49992000002","tipo":"passivo","icon":"🏪","empresas":["mf"],"campos":["Saldo Inicial","Transações do Período","Repasses Realizados","Saldo Razão"]},
    {"id":"mf-moeda-frota","nome":"Moeda Eletrônica - Frota","codigo":"49992000004","tipo":"passivo","icon":"⛽","empresas":["mf"],"campos":["Saldo Inicial","Emissões do Período","Resgates / Utilizações","Saldo Razão"]},
    {"id":"mf-trans-pre-frota","nome":"Transitória Transações Pré - Frota","codigo":"49992000008","tipo":"passivo","icon":"🔄","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-trans-pre-pat","nome":"Transitória Transações Pré - PAT","codigo":"49992000007","tipo":"passivo","icon":"🔄","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-trans-pos-frota","nome":"Transitória Transações Pós - Frota Abastec.","codigo":"49992000011","tipo":"passivo","icon":"🔄","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-adto-cli","nome":"Adiantamento de Clientes","codigo":"49992000014","tipo":"passivo","icon":"💰","empresas":["mf"],"campos":["Saldo Inicial","Novos Adiantamentos","Amortizações","Saldo Razão"]},
    {"id":"mf-caucao-cli","nome":"Caução de Clientes","codigo":"49992000015","tipo":"passivo","icon":"🔒","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-emp-consig","nome":"Empréstimo Consignado Colaboradores","codigo":"49992000016","tipo":"passivo","icon":"💳","empresas":["mf"],"campos":["Saldo Inicial","Novos Consignados","Amortizações","Saldo Razão"]},
    {"id":"mf-vt","nome":"Vale Transporte","codigo":"49992000017","tipo":"passivo","icon":"🚌","empresas":["mf"],"campos":["Saldo Inicial","Emissões do Período","Utilizações","Saldo Razão"]},
    {"id":"mf-trans-fat-rede","nome":"Transitória de Faturamento de Rede","codigo":"49992000019","tipo":"passivo","icon":"🔄","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-trans-antec","nome":"Transitória de Antecipado","codigo":"49992000024","tipo":"passivo","icon":"🔄","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"moeda-frt","nome":"Moeda Eletrônica Frota Papel","codigo":"49992000023","tipo":"passivo","icon":"⛽","empresas":["mf"],"campos":["Saldo Inicial","Emissões do Período","Resgates / Utilizações","Saldo Razão"]},
    {"id":"mf-trans-enc","nome":"Transitória de Encontro de Contas","codigo":"49992000026","tipo":"passivo","icon":"🔄","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-trans-mx","nome":"Transações MX","codigo":"49992000027","tipo":"passivo","icon":"🔄","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-trans-fastpass","nome":"Transitória Transação - Maxifrota Fast Pass","codigo":"49992000029","tipo":"passivo","icon":"🔄","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-outras-cp","nome":"Outras Contas a Pagar","codigo":"49992000099","tipo":"passivo","icon":"📋","empresas":["mf"],"campos":["Saldo Inicial","Novos Valores","Pagamentos","Saldo Razão"]},
    {"id":"mf-cotas","nome":"Cotas","codigo":"61110280001","tipo":"passivo","icon":"🏛️","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-lucros","nome":"Lucros/Prejuízos Acumulados","codigo":"61810000001","tipo":"passivo","icon":"📊","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
    {"id":"mf-div-lucros","nome":"Dividendos e Lucros Pagos Antecipadamente (-)","codigo":"61880000001","tipo":"passivo","icon":"💰","empresas":["mf"],"campos":["Saldo Relatório Auxiliar","Saldo Razão"]},
]

EMPRESAS = {
    "nc": {"nome": "Nutricash", "razao": "NUTRICASH SERVIÇOS LTDA", "cor": "#1C3557", "acc": "#2196C4"},
    "mf": {"nome": "MaxiFrota", "razao": "MAXIFROTA LTDA", "cor": "#003D78", "acc": "#F5A800"},
}

MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
         "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

# ── SESSION STATE ──────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "pagina": "selecao",      # selecao | dashboard | modulo
        "empresa": None,
        "conta": None,
        "status": {},             # {emp_id: status}
        "historico": [],          # lista de registros
        "busca": "",
        "res": None,
        "arquivo_pdf": None,
        "arquivo_xls": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── HELPERS ────────────────────────────────────────────────────────────────────
def fmt_br(v):
    if v is None: return "–"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def get_contas(emp):
    return [c for c in CONTAS if emp in c["empresas"]]

def get_status(emp, cid):
    return st.session_state.status.get(f"{emp}_{cid}", "pendente")

def set_status(emp, cid, v):
    st.session_state.status[f"{emp}_{cid}"] = v

def cor_empresa():
    e = st.session_state.empresa
    return EMPRESAS[e]["cor"] if e else "#1C3557"

def acc_empresa():
    e = st.session_state.empresa
    return EMPRESAS[e]["acc"] if e else "#2196C4"

# ── CSS GLOBAL ─────────────────────────────────────────────────────────────────
def inject_css():
    cor = cor_empresa()
    acc = acc_empresa()
    st.markdown(f"""
    <style>
    /* Reset e base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [data-testid="stApp"] {{
        font-family: 'Inter', sans-serif !important;
        background: #F7FAFC !important;
        color: #2D3748;
    }}

    /* Remove padding padrão Streamlit */
    [data-testid="stAppViewContainer"] > .main {{
        padding: 0 !important;
    }}
    .main .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    [data-testid="stSidebar"] {{
        background: #ffffff !important;
        border-right: 1px solid #E2E8F0;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 0 !important;
    }}
    section[data-testid="stSidebar"] {{
        width: 260px !important;
        min-width: 260px !important;
    }}

    /* Header da sidebar */
    .sidebar-header {{
        background: {cor};
        padding: 16px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
        color: white;
    }}
    .sidebar-header .emp-name {{
        font-size: 13px;
        font-weight: 700;
        color: rgba(255,255,255,0.95);
        letter-spacing: .03em;
    }}
    .sidebar-header .emp-razao {{
        font-size: 10px;
        color: rgba(255,255,255,0.65);
        margin-top: 2px;
    }}

    /* Topbar principal */
    .topbar {{
        background: {cor};
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 24px;
        position: sticky;
        top: 0;
        z-index: 999;
        box-shadow: 0 2px 8px rgba(0,0,0,.18);
    }}
    .topbar-title {{
        color: rgba(255,255,255,0.9);
        font-size: 13px;
        font-weight: 600;
        letter-spacing: .06em;
        text-transform: uppercase;
    }}

    /* Cards de empresa */
    .emp-card {{
        background: white;
        border: 1.5px solid #E2E8F0;
        border-radius: 12px;
        padding: 32px 28px;
        cursor: pointer;
        transition: all .2s;
        box-shadow: 0 2px 8px rgba(0,0,0,.06);
        text-align: center;
    }}
    .emp-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,.1);
    }}

    /* KPI cards */
    .kpi-row {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 20px;
    }}
    .kpi-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,.04);
    }}
    .kpi-icon {{
        width: 38px; height: 38px;
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 17px; flex-shrink: 0;
    }}
    .kpi-label {{
        font-size: 10px; font-weight: 600; color: #A0AEC0;
        text-transform: uppercase; letter-spacing: .04em; margin-bottom: 2px;
    }}
    .kpi-value {{
        font-size: 21px; font-weight: 700; line-height: 1;
    }}
    .kpi-sub {{
        font-size: 10px; color: #A0AEC0; margin-top: 2px;
    }}

    /* Conta cards */
    .conta-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        cursor: pointer;
        transition: all .18s;
        box-shadow: 0 1px 3px rgba(0,0,0,.04);
        position: relative;
        overflow: hidden;
        margin-bottom: 8px;
    }}
    .conta-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,.1);
        border-color: {acc};
    }}
    .conta-card .tipo-badge {{
        font-size: 9px; font-weight: 700;
        padding: 2px 7px; border-radius: 3px;
        letter-spacing: .04em;
    }}
    .badge-ativo {{ background: #DBEAFE; color: #1E40AF; }}
    .badge-passivo {{ background: #FCE7F3; color: #9D174D; }}

    /* Status pills */
    .pill-ok {{ background: #E8F8EF; color: #27AE60; padding: 3px 8px; border-radius: 3px; font-size: 10px; font-weight: 700; }}
    .pill-pend {{ background: #FEF3E7; color: #E67E22; padding: 3px 8px; border-radius: 3px; font-size: 10px; font-weight: 700; }}

    /* Busca balão */
    .search-wrapper {{
        background: #F1F5F9;
        border-radius: 8px;
        padding: 4px 8px;
        margin: 8px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1.5px solid #E2E8F0;
        transition: border .15s;
    }}
    .search-wrapper:focus-within {{
        border-color: {acc};
        background: white;
    }}

    /* Seção tipo */
    .tipo-lbl {{
        font-size: 10px; font-weight: 700; color: #A0AEC0;
        letter-spacing: .08em; text-transform: uppercase;
        margin: 16px 0 8px;
        display: flex; align-items: center; gap: 8px;
    }}
    .tipo-lbl::after {{
        content: ''; flex: 1; height: 1px; background: #E2E8F0;
    }}

    /* Diff box */
    .diff-ok {{
        background: #E8F8EF; border: 1px solid #A7F3D0;
        border-radius: 8px; padding: 16px 20px;
        display: flex; align-items: center; justify-content: space-between;
    }}
    .diff-nok {{
        background: #FDEDEC; border: 1px solid #FECACA;
        border-radius: 8px; padding: 16px 20px;
        display: flex; align-items: center; justify-content: space-between;
    }}

    /* Streamlit element overrides */
    div[data-testid="stButton"] > button {{
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }}
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {{
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #718096 !important;
        text-transform: uppercase !important;
        letter-spacing: .04em !important;
    }}
    /* Ocultar ícone hamburger e deploy */
    #MainMenu, header, footer,
    [data-testid="stToolbar"],
    .stDeployButton, #stDecoration {{
        display: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: SELEÇÃO DE EMPRESA
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.pagina == "selecao":
    st.markdown("""
    <div style="min-height:60px;background:#1C3557;display:flex;align-items:center;padding:0 32px;">
        <span style="color:white;font-size:18px;font-weight:700;letter-spacing:-.01em;">
            📊 Conciliação Contábil
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h2 style='text-align:center;font-size:22px;font-weight:700;color:#2D3748;'>Selecione a empresa</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center;color:#718096;margin-bottom:32px;'>Escolha a empresa para acessar o módulo de conciliação contábil</p>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        pass
    with col2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="emp-card">
                <div style="font-size:36px;margin-bottom:12px;">🏦</div>
                <div style="font-size:16px;font-weight:700;color:#2D3748;margin-bottom:6px;">Nutricash</div>
                <div style="font-size:11px;color:#718096;margin-bottom:16px;">Benefícios, alimentação e gestão de pagamentos corporativos</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ACESSAR →", key="btn_nc", use_container_width=True, type="primary"):
                st.session_state.empresa = "nc"
                st.session_state.pagina = "dashboard"
                st.rerun()
        with c2:
            st.markdown("""
            <div class="emp-card">
                <div style="font-size:36px;margin-bottom:12px;">🚛</div>
                <div style="font-size:16px;font-weight:700;color:#2D3748;margin-bottom:6px;">MaxiFrota</div>
                <div style="font-size:11px;color:#718096;margin-bottom:16px;">Gestão de frotas, abastecimento e mobilidade corporativa</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ACESSAR →", key="btn_mf", use_container_width=True, type="primary"):
                st.session_state.empresa = "mf"
                st.session_state.pagina = "dashboard"
                st.rerun()
    with col3:
        pass

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.pagina == "dashboard":
    emp = st.session_state.empresa
    emp_info = EMPRESAS[emp]
    contas = get_contas(emp)
    cor = emp_info["cor"]
    acc = emp_info["acc"]

    ok_count = sum(1 for c in contas if get_status(emp, c["id"]) == "ok")
    pend_count = sum(1 for c in contas if get_status(emp, c["id"]) == "pendente")
    hist_emp = [h for h in st.session_state.historico if h["emp"] == emp]

    # Topbar
    st.markdown(f"""
    <div class="topbar">
        <span class="topbar-title">📊 {emp_info['nome']} — Conciliação Contábil</span>
        <span style="color:rgba(255,255,255,0.7);font-size:11px;">{emp_info['razao']}</span>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-header">
            <div>
                <div class="emp-name">{emp_info['nome']}</div>
                <div class="emp-razao">{emp_info['razao']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='padding:8px 12px;'>", unsafe_allow_html=True)

        # Busca
        busca = st.text_input("🔍 Buscar conta...", value=st.session_state.busca,
                               placeholder="Nome ou código...", key="busca_input",
                               label_visibility="collapsed")
        st.session_state.busca = busca

        # Navegação
        tab_escolha = st.radio("", ["📊 Painel", "🕐 Histórico"],
                                label_visibility="collapsed", key="nav_tab")

        st.divider()

        # Ativo
        contas_ativo = [c for c in contas if c["tipo"] == "ativo"]
        if busca:
            contas_ativo = [c for c in contas_ativo
                           if busca.lower() in c["nome"].lower() or busca in c["codigo"]]

        st.markdown("<div class='tipo-lbl'>Ativo</div>", unsafe_allow_html=True)
        for c in contas_ativo:
            st_ok = get_status(emp, c["id"]) == "ok"
            ativo = st.session_state.conta and st.session_state.conta["id"] == c["id"]
            label = f"{c['icon']} {c['nome'][:26]}{'…' if len(c['nome'])>26 else ''}"
            btn_style = "primary" if ativo else "secondary"
            if st.button(label, key=f"sb_{c['id']}", use_container_width=True):
                st.session_state.conta = c
                st.session_state.pagina = "modulo"
                st.session_state.res = None
                st.rerun()

        st.divider()

        # Passivo
        contas_passivo = [c for c in contas if c["tipo"] == "passivo"]
        if busca:
            contas_passivo = [c for c in contas_passivo
                             if busca.lower() in c["nome"].lower() or busca in c["codigo"]]

        st.markdown("<div class='tipo-lbl'>Passivo</div>", unsafe_allow_html=True)
        for c in contas_passivo:
            label = f"{c['icon']} {c['nome'][:26]}{'…' if len(c['nome'])>26 else ''}"
            if st.button(label, key=f"sb_{c['id']}", use_container_width=True):
                st.session_state.conta = c
                st.session_state.pagina = "modulo"
                st.session_state.res = None
                st.rerun()

        st.divider()
        if st.button("← Trocar Empresa", use_container_width=True):
            st.session_state.pagina = "selecao"
            st.session_state.empresa = None
            st.session_state.conta = None
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ── CONTEÚDO PRINCIPAL ──────────────────────────────────────────────────
    st.markdown("<div style='padding:22px 28px 60px;'>", unsafe_allow_html=True)

    if "Painel" in tab_escolha:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:#E8F8EF;">✅</div>
                <div>
                    <div class="kpi-label">Contas OK</div>
                    <div class="kpi-value" style="color:#27AE60;">{ok_count}</div>
                    <div class="kpi-sub">Conciliadas</div>
                </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:#FEF3E7;">⏳</div>
                <div>
                    <div class="kpi-label">Pendentes</div>
                    <div class="kpi-value" style="color:#E67E22;">{pend_count}</div>
                    <div class="kpi-sub">Aguardando</div>
                </div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:#EBF8FF;">📋</div>
                <div>
                    <div class="kpi-label">Total</div>
                    <div class="kpi-value" style="color:{acc};">{len(contas)}</div>
                    <div class="kpi-sub">Contas</div>
                </div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:#F5F6F7;">🕐</div>
                <div>
                    <div class="kpi-label">Histórico</div>
                    <div class="kpi-value" style="color:#718096;">{len(hist_emp)}</div>
                    <div class="kpi-sub">Registros</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Busca no painel
        busca_painel = st.text_input("🔍 Buscar conta no painel...",
                                      placeholder="Digite nome ou código da conta",
                                      key="busca_painel")

        # Grid de contas
        col_a, col_p = st.columns(2)

        with col_a:
            st.markdown("<div class='tipo-lbl'>Ativo</div>", unsafe_allow_html=True)
            contas_ativo_painel = [c for c in contas if c["tipo"] == "ativo"]
            if busca_painel:
                contas_ativo_painel = [c for c in contas_ativo_painel
                                       if busca_painel.lower() in c["nome"].lower() or busca_painel in c["codigo"]]
            for c in contas_ativo_painel:
                st_status = get_status(emp, c["id"])
                pill = f'<span class="pill-ok">● OK</span>' if st_status=="ok" else f'<span class="pill-pend">● Pendente</span>'
                st.markdown(f"""
                <div class="conta-card">
                    <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:6px;">
                        <span style="font-size:18px;">{c['icon']}</span>
                        <span class="tipo-badge badge-ativo">ATIVO</span>
                    </div>
                    <div style="font-size:12px;font-weight:700;color:#2D3748;margin-bottom:3px;">{c['nome']}</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#A0AEC0;margin-bottom:8px;">{c['codigo']}</div>
                    {pill}
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Abrir →", key=f"painel_{c['id']}", use_container_width=True):
                    st.session_state.conta = c
                    st.session_state.pagina = "modulo"
                    st.session_state.res = None
                    st.rerun()

        with col_p:
            st.markdown("<div class='tipo-lbl'>Passivo</div>", unsafe_allow_html=True)
            contas_pass_painel = [c for c in contas if c["tipo"] == "passivo"]
            if busca_painel:
                contas_pass_painel = [c for c in contas_pass_painel
                                      if busca_painel.lower() in c["nome"].lower() or busca_painel in c["codigo"]]
            for c in contas_pass_painel:
                st_status = get_status(emp, c["id"])
                pill = f'<span class="pill-ok">● OK</span>' if st_status=="ok" else f'<span class="pill-pend">● Pendente</span>'
                st.markdown(f"""
                <div class="conta-card">
                    <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:6px;">
                        <span style="font-size:18px;">{c['icon']}</span>
                        <span class="tipo-badge badge-passivo">PASSIVO</span>
                    </div>
                    <div style="font-size:12px;font-weight:700;color:#2D3748;margin-bottom:3px;">{c['nome']}</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#A0AEC0;margin-bottom:8px;">{c['codigo']}</div>
                    {pill}
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Abrir →", key=f"painel_{c['id']}", use_container_width=True):
                    st.session_state.conta = c
                    st.session_state.pagina = "modulo"
                    st.session_state.res = None
                    st.rerun()

    else:  # Histórico
        st.markdown(f"<h3 style='font-size:18px;font-weight:700;color:#2D3748;'>Histórico de Conciliações — {emp_info['nome']}</h3>", unsafe_allow_html=True)
        if not hist_emp:
            st.info("Nenhuma conciliação realizada ainda.")
        else:
            hist_rev = list(reversed(hist_emp))
            cols_h = ["Conta", "Código", "Período", "Diferença", "Status", "Data"]
            rows_h = []
            for h in hist_rev:
                rows_h.append({
                    "Conta": h["conta"],
                    "Código": h["codigo"],
                    "Período": h["ref"],
                    "Diferença": fmt_br(abs(h["diff"])),
                    "Status": "✅ OK" if h["ok"] else "⚠️ Divergência",
                    "Data": h["data"],
                })
            st.dataframe(rows_h, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: MÓDULO DE CONCILIAÇÃO
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.pagina == "modulo":
    emp = st.session_state.empresa
    emp_info = EMPRESAS[emp]
    c = st.session_state.conta
    cor = emp_info["cor"]
    acc = emp_info["acc"]

    if not c:
        st.session_state.pagina = "dashboard"
        st.rerun()

    # Topbar
    st.markdown(f"""
    <div class="topbar">
        <span class="topbar-title">{c['icon']} {c['nome']}</span>
        <span style="color:rgba(255,255,255,0.7);font-size:11px;">{emp_info['razao']} · {c['codigo']}</span>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-header">
            <div>
                <div class="emp-name">{emp_info['nome']}</div>
                <div class="emp-razao">{emp_info['razao']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='padding:8px 12px;'>", unsafe_allow_html=True)

        # Busca na sidebar do módulo
        busca_mod = st.text_input("🔍 Buscar conta...", value=st.session_state.busca,
                                   placeholder="Nome ou código...",
                                   key="busca_mod", label_visibility="collapsed")
        st.session_state.busca = busca_mod

        contas = get_contas(emp)

        st.markdown("<div class='tipo-lbl'>Ativo</div>", unsafe_allow_html=True)
        contas_ativo = [x for x in contas if x["tipo"] == "ativo"]
        if busca_mod:
            contas_ativo = [x for x in contas_ativo
                           if busca_mod.lower() in x["nome"].lower() or busca_mod in x["codigo"]]
        for conta in contas_ativo:
            ativo = conta["id"] == c["id"]
            label = f"{conta['icon']} {conta['nome'][:24]}{'…' if len(conta['nome'])>24 else ''}"
            if st.button(label, key=f"sb2_{conta['id']}", use_container_width=True,
                        type="primary" if ativo else "secondary"):
                st.session_state.conta = conta
                st.session_state.res = None
                st.rerun()

        st.divider()
        st.markdown("<div class='tipo-lbl'>Passivo</div>", unsafe_allow_html=True)
        contas_passivo = [x for x in contas if x["tipo"] == "passivo"]
        if busca_mod:
            contas_passivo = [x for x in contas_passivo
                             if busca_mod.lower() in x["nome"].lower() or busca_mod in x["codigo"]]
        for conta in contas_passivo:
            ativo = conta["id"] == c["id"]
            label = f"{conta['icon']} {conta['nome'][:24]}{'…' if len(conta['nome'])>24 else ''}"
            if st.button(label, key=f"sb2_{conta['id']}", use_container_width=True,
                        type="primary" if ativo else "secondary"):
                st.session_state.conta = conta
                st.session_state.res = None
                st.rerun()

        st.divider()
        if st.button("← Voltar ao Painel", use_container_width=True):
            st.session_state.pagina = "dashboard"
            st.session_state.conta = None
            st.session_state.res = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── CONTEÚDO DO MÓDULO ──────────────────────────────────────────────────
    st.markdown("<div style='padding:22px 28px 60px;max-width:900px;'>", unsafe_allow_html=True)

    tipo_cor_bg = "#DBEAFE" if c["tipo"] == "ativo" else "#FCE7F3"
    tipo_cor_tx = "#1E40AF" if c["tipo"] == "ativo" else "#9D174D"

    st.markdown(f"""
    <span style="background:{tipo_cor_bg};color:{tipo_cor_tx};font-size:10px;font-weight:700;
                 padding:3px 9px;border-radius:3px;letter-spacing:.04em;">
        {c['tipo'].upper()}
    </span>
    <h1 style="font-size:22px;font-weight:700;color:#2D3748;margin:6px 0 2px;letter-spacing:-.02em;">
        {c['icon']} {c['nome']}
    </h1>
    <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#718096;margin-bottom:22px;">
        Conta: {c['codigo']} · {emp_info['razao']}
    </div>
    """, unsafe_allow_html=True)

    # ── PASSO 1: Período e valores ──────────────────────────────────────────
    with st.expander("📅 Passo 01 — Período e Documentos", expanded=True):
        st.markdown("<div style='font-size:12px;color:#718096;margin-bottom:12px;'>Selecione o mês/ano de referência e preencha os saldos para processar a conciliação.</div>", unsafe_allow_html=True)

        col_m, col_a = st.columns([1, 1])
        with col_m:
            mes = st.selectbox("Mês", options=range(1, 13),
                               format_func=lambda x: MESES[x-1],
                               index=datetime.now().month - 1, key="ref_mes")
        with col_a:
            ano = st.number_input("Ano", min_value=2020, max_value=2099,
                                  value=datetime.now().year, key="ref_ano")

        ref_label = f"{MESES[mes-1]}/{ano}"

        st.divider()

        # Upload de arquivo
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            arquivo_pdf = st.file_uploader("📄 Razão Analítico (PDF/Excel)",
                                           type=["pdf","xlsx","xls"],
                                           key="up_pdf")
            if arquivo_pdf:
                st.success(f"✓ {arquivo_pdf.name}")

        with col_up2:
            arquivo_xls = st.file_uploader("📊 Relatório Auxiliar (XLSX/CSV/PDF)",
                                           type=["xlsx","xls","csv","pdf","txt","ods","json"],
                                           key="up_xls")
            if arquivo_xls:
                st.success(f"✓ {arquivo_xls.name}")

        st.divider()

        # Campos manuais
        with st.expander("▶ Preencher valores manualmente"):
            st.markdown("<div style='font-size:11px;color:#718096;margin-bottom:10px;'>Preencha os saldos manualmente caso não tenha os arquivos disponíveis.</div>", unsafe_allow_html=True)
            campos = c["campos"]
            vals_input = []
            n_cols = min(len(campos), 3)
            cols_campos = st.columns(n_cols)
            for i, campo in enumerate(campos):
                with cols_campos[i % n_cols]:
                    v = st.number_input(
                        campo,
                        min_value=0.0,
                        value=0.0,
                        step=0.01,
                        format="%.2f",
                        key=f"campo_{c['id']}_{i}"
                    )
                    vals_input.append(v)

        # Botão processar
        tem_dados = any(v > 0 for v in vals_input) or arquivo_pdf or arquivo_xls
        if st.button("⚡ Processar Conciliação", type="primary",
                     disabled=not tem_dados, key="btn_proc"):
            campos = c["campos"]
            vals = vals_input

            # Lógica de conciliação
            sR = vals[-1] if vals else 0.0
            if len(vals) == 2:
                tA = vals[0]
            else:
                tA = vals[0]
                for i in range(1, len(vals)-1):
                    if i % 2 == 1:
                        tA += vals[i]
                    else:
                        tA -= vals[i]

            diff = sR - tA
            ok = abs(diff) < 0.01

            # Salva resultado
            st.session_state.res = {
                "conta": c, "vals": vals, "ref": ref_label,
                "sR": sR, "tA": tA, "diff": diff, "ok": ok
            }

            # Salva status e histórico
            set_status(emp, c["id"], "ok" if ok else "pendente")
            h_item = {
                "emp": emp, "id": c["id"], "conta": c["nome"],
                "codigo": c["codigo"], "icon": c["icon"],
                "ref": ref_label, "diff": diff, "ok": ok,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.historico = [
                h for h in st.session_state.historico
                if not (h["emp"]==emp and h["id"]==c["id"] and h["ref"]==ref_label)
            ]
            st.session_state.historico.append(h_item)
            st.rerun()

    # ── PASSO 2: Resultado ──────────────────────────────────────────────────
    if st.session_state.res:
        r = st.session_state.res
        sR, tA, diff, ok = r["sR"], r["tA"], r["diff"], r["ok"]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
                    color:#A0AEC0;margin-bottom:8px;padding-bottom:8px;border-bottom:1px solid #E2E8F0;">
            Passo 02 de 02 — Resultado da Conciliação
        </div>
        """, unsafe_allow_html=True)

        # KPIs resultado
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Saldo Razão", fmt_br(sR), delta=None)
        with col_r2:
            st.metric("Rel. Auxiliar", fmt_br(tA), delta=None)
        with col_r3:
            st.metric("Diferença", fmt_br(abs(diff)),
                      delta="Zerada ✅" if ok else "Divergência ⚠️",
                      delta_color="normal" if ok else "inverse")

        # Tabela composição
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#A0AEC0;margin-bottom:8px;'>Composição do Saldo</div>", unsafe_allow_html=True)

        campos = c["campos"]
        vals = r["vals"]
        rows_tab = []
        if len(campos) == 2:
            rows_tab.append({"Descrição": campos[0], "Valor (R$)": fmt_br(vals[0]), "D/C": "D"})
        else:
            for i, (campo, val) in enumerate(zip(campos[:-1], vals[:-1])):
                rows_tab.append({"Descrição": campo, "Valor (R$)": fmt_br(val), "D/C": "D" if i%2==0 else "C"})
        rows_tab.append({"Descrição": "Total Auxiliar", "Valor (R$)": fmt_br(tA), "D/C": ""})
        rows_tab.append({"Descrição": "Saldo Razão", "Valor (R$)": fmt_br(sR), "D/C": ""})
        rows_tab.append({"Descrição": "DIFERENÇA", "Valor (R$)": fmt_br(abs(diff)), "D/C": "✅ OK" if ok else "⚠️ REVISAR"})

        st.dataframe(rows_tab, use_container_width=True, hide_index=True)

        # Box resultado final
        if ok:
            st.markdown(f"""
            <div class="diff-ok">
                <div>
                    <div style="font-size:13px;font-weight:700;color:#27AE60;">✅ Conciliação Zerada</div>
                    <div style="font-size:11px;color:#27AE60;opacity:.8;margin-top:2px;">
                        Razão ({fmt_br(sR)}) ≡ Auxiliar ({fmt_br(tA)})
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="font-size:20px;font-weight:700;color:#27AE60;">{fmt_br(abs(diff))}</div>
                    <span style="background:#27AE60;color:white;font-size:10px;font-weight:700;
                                 padding:4px 12px;border-radius:3px;">APROVADA</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="diff-nok">
                <div>
                    <div style="font-size:13px;font-weight:700;color:#E74C3C;">⚠️ Conciliação com Divergência</div>
                    <div style="font-size:11px;color:#E74C3C;opacity:.8;margin-top:2px;">
                        Razão ({fmt_br(sR)}) ≠ Auxiliar ({fmt_br(tA)})
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="font-size:20px;font-weight:700;color:#E74C3C;">{fmt_br(abs(diff))}</div>
                    <span style="background:#E74C3C;color:white;font-size:10px;font-weight:700;
                                 padding:4px 12px;border-radius:3px;">REVISAR</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.warning(f"⚠️ **Atenção:** Divergência de **{fmt_br(abs(diff))}**. Verifique os lançamentos do período.")

        # Ações
        st.markdown("<br>", unsafe_allow_html=True)
        col_a1, col_a2, col_a3 = st.columns([1, 1, 1])
        with col_a1:
            if st.button("← Novo Período", use_container_width=True):
                st.session_state.res = None
                st.rerun()
        with col_a2:
            # Export Excel
            try:
                import openpyxl
                from openpyxl.styles import Font, PatternFill, Alignment
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Conciliação"
                ws.append([f"CONCILIAÇÃO — {c['nome'].upper()}"])
                ws.append([f"{emp_info['razao']} | Conta: {c['codigo']} | Ref.: {r['ref']}"])
                ws.append([])
                ws.append(["Descrição", "Valor (R$)", "D/C"])
                for row in rows_tab:
                    ws.append([row["Descrição"], row["Valor (R$)"], row["D/C"]])
                ws.append([])
                ws.append([f"Emitido em: {datetime.now().strftime('%d/%m/%Y')}"])
                buf = io.BytesIO()
                wb.save(buf)
                buf.seek(0)
                st.download_button("⬇ Excel", data=buf,
                                   file_name=f"conc_{c['id']}_{mes:02d}{ano}.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)
            except ImportError:
                st.button("⬇ Excel (instale openpyxl)", disabled=True, use_container_width=True)
        with col_a3:
            # Export PDF simples como CSV
            linhas = [f"CONCILIAÇÃO — {c['nome'].upper()}",
                      f"{emp_info['razao']} | Conta: {c['codigo']} | Ref.: {r['ref']}",
                      "",
                      "Descrição;Valor;D/C"]
            for row in rows_tab:
                linhas.append(f"{row['Descrição']};{row['Valor (R$)']};{row['D/C']}")
            linhas.append(f"\nEmitido em: {datetime.now().strftime('%d/%m/%Y')}")
            csv_str = "\n".join(linhas)
            st.download_button("⬇ CSV/PDF", data=csv_str,
                               file_name=f"conc_{c['id']}_{mes:02d}{ano}.csv",
                               mime="text/csv",
                               use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
