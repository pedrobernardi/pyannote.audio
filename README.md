# Serviço de Diarização de Áudio com FastAPI e pyannote.audio

Este repositório contém um serviço de API construído com FastAPI que realiza a diarização de áudio utilizando o `pyannote.audio`. O serviço está preparado para ser implantado no Railway utilizando Docker.

## Estrutura do Projeto

/diarization-api 
├── main.py 
├── requirements.txt 
├── Dockerfile 
└── README.md


## Configuração e Implantação

### 1. Obter o Token da Hugging Face

- Acesse: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Clique em "New token" e selecione o escopo **"read"**
- Copie o token gerado

### 2. Configurar o Railway

- Acesse [https://railway.app](https://railway.app) e crie um novo projeto
- Selecione "Deploy from GitHub repo" e conecte este repositório
- No painel do projeto, vá para a seção **Variables** e adicione:

HUGGINGFACE_TOKEN=seu_token_aqui


- O Railway detectará o `Dockerfile` e iniciará o processo de construção e implantação
- Após a implantação, uma URL pública será gerada para acessar a API

### 3. Testar a API

- Utilize ferramentas como `curl` ou Postman para enviar requisições `POST` para o endpoint `/diarize` com um arquivo de áudio no formato `.wav`

## Exemplo de Uso

bash
curl -X 'POST' 
  'https://seu-projeto.up.railway.app/diarize' 
  -H 'accept: application/json' 
  -H 'Content-Type: multipart/form-data' 
  -F 'file=@/caminho/para/seu_audio.wav'

A resposta será um JSON contendo os segmentos de áudio com os respectivos locutores e timestamps.

Notas
Certifique-se de que o arquivo de áudio esteja no formato .wav e com qualidade adequada para melhores resultados

Ajuste as configurações de CORS no main.py conforme necessário para o seu ambiente de produção


---

## 🚀 Passos para Implantação

1. **Preparar o Repositório:**
   - Crie um novo repositório no GitHub e adicione os arquivos acima.
   - Certifique-se de que o repositório esteja atualizado com todos os arquivos necessários.

2. **Implantar no Railway:**
   - Acesse [https://railway.app](https://railway.app) e faça login.
   - Crie um novo projeto e selecione "Deploy from GitHub repo".
   - Conecte o repositório que contém os arquivos do projeto.
   - No painel do projeto, vá para a seção **Variables** e adicione o token da Hugging Face:

     ```
     HUGGINGFACE_TOKEN=seu_token_aqui
     ```

   - O Railway iniciará o processo de construção e implantação automaticamente.

3. **Testar o Serviço:**
   - Após a implantação, o Railway fornecerá uma URL pública para o serviço.
   - Utilize ferramentas como `curl`, Postman ou seu frontend em React/TypeScript para enviar requisições ao endpoint `/diarize`.

---

## 🎯 Considerações Finais

- **Formato do Áudio:** Certifique-se de que os arquivos de áudio enviados estejam no formato `.wav` para compatibilidade com o `pyannote.audio`.
- **Configurações de CORS:** Ajuste as configurações de CORS no `main.py` para permitir apenas origens confiáveis, especialmente em ambientes de produção.
- **Desempenho:** Embora o serviço funcione bem em instâncias com CPU, considere utilizar instâncias com suporte a GPU para melhorar o desempenho em processamento de áudio de maior volume.

---

Se precisar de assistência adicional ou tiver dúvidas durante o processo de implantação, não hesite em perguntar!
::contentReference[oaicite:0]{index=0}
 

