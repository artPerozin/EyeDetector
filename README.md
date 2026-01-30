# 👁️ Eye Detector – Detector de Atenção em Tempo Real

Este projeto utiliza **Visão Computacional** para detectar, em tempo real, se o usuário está olhando diretamente para a câmera. Caso o usuário desvie o olhar, um alerta sonoro (`alert.mp3`) é reproduzido automaticamente. Quando o usuário volta a olhar para a câmera, o som é interrompido.

## 🎯 Aplicações

O sistema é ideal para:

- Monitoramento de atenção
- Estudos e foco
- Projetos acadêmicos
- Aprendizado de Visão Computacional
- Prototipagem de sistemas de vigilância ou UX

---

## 🧠 Tecnologias Utilizadas

- **Python 3.11**
- **OpenCV** – Captura e processamento de vídeo
- **MediaPipe Face Mesh** – Detecção de landmarks faciais e íris
- **NumPy** – Cálculos matemáticos
- **Pygame** – Reprodução de áudio

---

## 📁 Estrutura do Projeto

```
VisaoComputacional/
├── venv/
├── main.py
├── requirements.txt
├── alert.mp3
└── README.md
```

---

## ⚙️ Pré-requisitos

- Python 3.10 ou 3.11
- Webcam funcional
- Sistema operacional: Windows (testado com DirectShow)

---

## 🚀 Como iniciar o projeto (do zero)

### 1️⃣ Clonar ou criar a pasta do projeto

```bash
mkdir EyeDetector
cd EyeDetector
```

### 2️⃣ Criar e ativar ambiente virtual

```bash
python -m venv venv
```

**Ativar (Windows):**

```bash
venv\Scripts\activate
```

### 3️⃣ Criar o arquivo `requirements.txt`

```txt
opencv-python
mediapipe==0.10.9
numpy
pygame
```

**Instalar dependências:**

```bash
pip install -r requirements.txt
```

### 4️⃣ Adicionar o arquivo de áudio

Coloque um arquivo chamado `alert.mp3` na raiz do projeto. Pode ser qualquer som curto de alerta.

### 5️⃣ Executar o sistema

```bash
python main.py
```

---

## 👁️ Como usar o Eye Detector

Ao executar, uma janela com a imagem da câmera será aberta. O sistema detecta:

- Rosto
- Olhos
- Posição da íris

### Funcionamento:

- ✅ **Olhando para a câmera** → música para
- ❌ **Olhando para outro lugar** → música toca

A detecção ocorre em tempo real. Pressione **ESC** para encerrar o programa.

---

## 🎯 Sensibilidade do olhar

A sensibilidade é controlada por este trecho no código:

```python
if 0.48 < gaze < 0.52:
    looking = True
```

Quanto menor o intervalo, mais rigoroso o sistema.

### Exemplos:

| Modo | Intervalo |
|------|-----------|
| Normal | `0.45 < gaze < 0.55` |
| Sensível | `0.48 < gaze < 0.52` |
| Extremamente sensível | `0.49 < gaze < 0.51` |

---

## 🧪 Dicas importantes

- Use boa iluminação
- Evite reflexos fortes nos olhos
- Óculos podem afetar a precisão
- Quanto mais centralizado o rosto, melhor a detecção

---

## 🧯 Problemas comuns

### ❌ Câmera não abre

O sistema foi configurado para:

```python
cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

Se não funcionar, teste índices 1 ou 2.

### ❌ Erro com MediaPipe

Garanta que:

- Não exista `mediapipe.py` no projeto
- A versão instalada seja exatamente `0.10.9`

Verificar versão:

```bash
pip show mediapipe
```

---

## 🚀 Possíveis evoluções do projeto

- Detectar piscar de olhos
- Adicionar delay antes do alerta
- Criar score de atenção
- Salvar logs de foco
- Transformar em aplicativo `.exe`
- Usar como base para TCC ou artigo

---

## 📜 Licença

Projeto educacional e experimental. Uso livre para fins de estudo e aprendizado.