# Image Recognition Tester

## Descrição
O **Image Recognition Tester** é uma ferramenta para captura e reconhecimento de imagem. O programa permite que o usuário carregue um template de imagem e reconheça sua presença em capturas de tela, marcando todas as ocorrências do template encontrado. Ele foi criado com o intuito de testar o reconhecimento dessas imagens para posterior inserção em um outro programa.

## Funcionalidades
- **Captura de Tela**: Capture a tela inteira e exiba a captura na interface do programa.
- **Carregar Template**: Carregue uma imagem template para reconhecimento.
- **Reconhecimento de Template**: Identifique todas as ocorrências do template na captura de tela e marque-as com retângulos vermelhos.
- **Zoom In/Out**: Aplique zoom in ou zoom out na imagem para melhor visualização.
- **Ajuste de Sensibilidade**: Ajuste a sensibilidade do reconhecimento de template.
- **Salvar Resultados**: Salve a imagem capturada com as marcações de reconhecimento.

## Instalação
### Pré-requisitos
- Python 3.x
- PIP (gerenciador de pacotes do Python)

### Passos de Instalação
1. Clone o repositório:
    `ash
    git clone https://github.com/seu-usuario/DeteccaoImagens.git
    cd DeteccaoImagens/projeto
    `

2. Crie e ative um ambiente virtual:
    `ash
    python -m venv venv
    .\venv\Scripts\activate  # No Windows
    source venv/bin/activate  # No macOS/Linux
    `

3. Instale as dependências:
    `ash
    pip install -r requirements.txt
    `

## Uso
### Execução do Programa
1. Ative o ambiente virtual, se ainda não estiver ativado:
    `ash
    .\venv\Scripts\activate  # No Windows
    source venv/bin/activate  # No macOS/Linux
    `

2. Execute o programa:
    `ash
    python src/main.py
    `

### Interface do Usuário
- **Menu**:
  - File > Load Template: Carrega um template de imagem.
  - File > Capture Screen: Captura a tela inteira.
  - File > Save Results: Salva a imagem capturada com as marcações.
  - File > Exit: Sai do programa.
- **Toolbar**:
  - Open Template: Carrega um template de imagem.
  - Capture Screen: Captura a tela inteira.
  - Recognize: Reconhece o template na captura de tela.
  - Set Sensitivity: Ajusta a sensibilidade do reconhecimento de template.
  - Zoom In: Aumenta o zoom na imagem.
  - Zoom Out: Diminui o zoom na imagem.
  - Save Results: Salva a imagem capturada com as marcações.

### Exemplos de Uso
1. **Carregar Template**:
    - Clique em File > Load Template e selecione a imagem template que deseja usar.
2. **Capturar Tela**:
    - Clique em File > Capture Screen para capturar a tela inteira.
3. **Reconhecimento de Template**:
    - Clique em Recognize para identificar todas as ocorrências do template na captura de tela.
4. **Ajustar Sensibilidade**:
    - Clique em Set Sensitivity para ajustar a sensibilidade do reconhecimento.
5. **Aplicar Zoom**:
    - Clique em Zoom In ou Zoom Out para ajustar o zoom na imagem.
6. **Salvar Resultados**:
    - Clique em Save Results para salvar a imagem capturada com as marcações.

## Contribuição
Para contribuir com este projeto, por favor, siga as diretrizes padrão para pull requests e issues.

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contato
Para mais informações, entre em contato com [seu-email@dominio.com].

