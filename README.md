# 🐍🎮 Run from the Slimes

Um jogo estilo platformer desenvolvido em **Python** com **PgZero**, onde você precisa sobreviver o maior tempo possível fugindo dos slimes inimigos!

## 📌 Sobre o Jogo

Você controla um herói que deve correr e pular entre plataformas para escapar dos inimigos. À medida que o tempo passa, mais slimes aparecem! Cuidado para não encostar neles, ou é **game over**!

**Funcionalidades:**
- Menu com botões interativos
- Sons e música de fundo (ligar/desligar)
- Sistema de pontuação baseado no tempo de sobrevivência
- Inimigos com movimentação e animação
- Plataformas com colisão
- Game Over com opção de voltar ao menu

## 🎮 Controles

- **Seta Direita/Esquerda** – Move o jogador
- **Seta Cima** – Pula
- **Mouse** – Clica nos botões do menu
- **ESC** – Voltar ao menu após o Game Over

## 🧠 Como Jogar

1. Execute o jogo via terminal usando o **PgZero**:

   ```bash
   pgzrun main.py
   ```

2. No menu principal, clique em **Começar o jogo**.
3. Fuja dos slimes, pulando pelas plataformas.
4. Tente bater seu recorde de pontos!
5. Clique em **Saída** ou pressione `ESC` após o game over para voltar ao menu.

## 🔊 Áudio

- O jogo toca uma música de fundo e efeitos sonoros.
- Você pode ativar/desativar o som no menu clicando no botão `Música/Sons`.

## 📁 Estrutura do Projeto

Certifique-se de ter os seguintes arquivos e pastas na mesma pasta do jogo:

```
📂 projeto/
├── main.py
├── images/
│   ├── hero_idle1.png
│   ├── hero_idle2.png
│   ├── hero_walk1.png
│   ├── hero_walk2.png
│   ├── hero_walk3.png
│   ├── vilain_iddle1.png
│   ├── vilain_iddle2.png
│   └── ... até vilain_iddle10.png
│   ├── platform_grass.png
│   ├── bg.png
│   └── imagem_fundo.png
├── sounds/
│   ├── jump.wav
│   ├── game_over.wav
├── music/
│   └── musica_fundo.mp3
```

> **Importante:** os arquivos de imagem devem estar na pasta `images/`, e os sons na pasta `sounds/`, conforme o padrão do **PgZero**.

## 🛠️ Requisitos

- Python 3.x
- Biblioteca **Pygame**
- Biblioteca **PgZero**

Para instalar os requisitos, use:

```bash
pip install pygame pgzero
```

## 📜 Licença

Este projeto é apenas para fins educacionais. Sinta-se à vontade para modificar e expandir!

---

Feito com 💚 por Richard Jr ;)
