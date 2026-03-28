# 🍽️ Sabor & Dados | Dashboard de Sentimentos (Azure AI)

Este projeto faz parte do plano de aula para a certificação **AI-900**, demonstrando o uso prático de Inteligência Artificial para análise de feedbacks de clientes em um restaurante fictício.

## 🚀 Tecnologias Utilizadas
* **Azure Cognitive Services**: API de Linguagem (Text Analytics) para detecção de sentimentos.
* **Streamlit**: Framework para criação do Dashboard interativo.
* **Python**: Linguagem base para integração e raspagem de dados.
* **Plotly**: Visualização de dados dinâmica.

## 🛠️ Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/geraldocafe1/analise_sentimentos_api_microsoft.git](https://github.com/geraldocafe1/analise_sentimentos_api_microsoft.git)

2. **Instale as dependências::**

Bash
**pip install -r requirements.txt**
Configure as credenciais:
Crie um arquivo .env na raiz do projeto com suas chaves da Azure:

Plaintext
**AZURE_AI_ENDPOINT=**seu_endpoint_aqui
**AZURE_AI_KEY=**sua_chave_aqui
Inicie o Dashboard:

Bash
**streamlit run app.py**


3. 📊 **Funcionalidades**
Extração de comentários de um arquivo HTML.

Classificação automática em Positivo, Negativo e Neutro.

Gráficos de pizza para distribuição de sentimentos.

Indicador de confiança da IA por comentário.