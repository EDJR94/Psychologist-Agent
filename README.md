# Telegram Chatbot - Psicólogo

### Acesse o chatbot usando seu telegram aqui: [Telegram Chatbot](https://t.me/GregSchedulerAssistantBot)

#### Imagine ter alguém para conversar ou pedir um conselho qualquer momento do seu dia, sem julgamentos.
#### Converse com a Pam, sua Psicóloga 24/7!
----

### 🤝 Se você aprendeu algo novo com esse repo, me siga nas minhas redes sociais:

<a href="https://www.linkedin.com/in/edilsonsantosjr/"><img align="left" src="https://raw.githubusercontent.com/yushi1007/yushi1007/main/images/linkedin.svg" alt="Yu Shi | LinkedIn" width="21px"/></a>
<a href="https://www.instagram.com/edjr.ai?igsh=MWlmNm55dnRtbGoyeg%3D%3D&utm_source=qr"><img align="left" src="https://raw.githubusercontent.com/yushi1007/yushi1007/main/images/instagram.svg" alt="Yu Shi | Instagram" width="21px"/></a>
</br>
- 💬 Se tiver qualquer dúvida ou sugestão, entre em contato!
<p align="center">
  <img src="https://github.com/user-attachments/assets/4123a0a1-abd9-48ce-a2bc-85370c8e5c99" alt="Telegram agent" width="300">
</p>

## Geral
O chatbot é feito para simular uma conversa com um psicólogo por chat no telegram, incluindo textos e áudios. As especialidades são:
- Ansiedade
- Estresse
- Relacionamentos
- Crescimento pessoal

**Disclaimer**: Obviamente esse chatbot não substitui um psicólogo profissional, caso tenha problemas mais graves, consultar uma pessoa especializada.

## Como usar

### Pré-requisitos

- Python 3.9+
- Groq API key (for Llama3)
- Openai API Key(GPT)
- Criar um bot no telegram
- Instalar bibliotecas necessárias(no requirements.txt)

### Setup

1. **Clonar o repositório:**

   ```sh
   git clone https://github.com/AIXerum/AI-Telegram-Assistant.git
   cd AI-Telegram-Assistant
   ```

2. **Criar e ativar o ambiente virtual:**

   ```sh
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```

3. **Instalar as bibliotecas necessárias:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do seu diretório e adicionei as API KEYS como está no `.env.example`

5. **Criar bot no telegram:**

    Você precisará criar um bot no telegram para interagir com ele, siga esse vídeo. [guide](https://www.youtube.com/watch?v=ozQfKhdNjJU)

6. **Rodar o projeto localmente**:
   
    Inicie a API do FAST API:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port 8080
     ```
  
    Exponha a API com o ngrok para que o telegram possa acessar:
    ```bash
     ngrok http 8080
     ```
    Insira a URL única gerada pelo ngrok no script `set_telegram_webook.py` junto com seu token do telegram e inicie o script com
    ```bash
     python set_telegram_webhook.py
     ```
7. **Envie uma mensagem para o bot usando o telegram!**
  

