# Ascensão

App pessoal que uso para acompanhar uma campanha de 180 dias de treino e alimentação. Funciona como um jogo: cada dia tem missões, o progresso vira nível e conquistas, e um coach com voz comenta a evolução.

Abrir o app: https://vitordbl.github.io/ascensao/

## O que dá para fazer

- Registrar peso, medidas e fotos de antes e depois
- Registrar treinos, com volume da semana, carga por exercício e cronômetro de rounds
- Montar o diário alimentar e fotografar o prato para estimar os nutrientes
- Conversar com o coach, que responde por texto ou por voz
- Ver o relatório da semana com os padrões de treino e alimentação

## Como foi feito

É um PWA em HTML, CSS e JavaScript, sem framework. Instala na tela inicial do iPhone pelo Safari e também roda no computador.

Os dados ficam no próprio aparelho, em localStorage e IndexedDB. A sincronização entre aparelhos é opcional e usa um Gist secreto do GitHub.

O coach usa a API do Gemini, com uma chave gratuita do Google AI Studio que o usuário configura dentro do app. A chave nunca fica no repositório.

A voz em português roda offline com o Piper e tem um efeito de rádio. Também dá para usar a voz do próprio iPhone.

As notificações saem pelo app ntfy, disparadas por um workflow agendado do GitHub Actions.

Nada pessoal (fotos, medidas ou chaves) fica neste repositório.
