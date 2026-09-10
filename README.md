# Análise de Cobertura da Rede Wi-Fi

Dashboard desenvolvido em Python + Streamlit para analisar a cobertura
Wi-Fi do campus.

## Estrutura

- `dados/wifi.csv`: medições do Wi-Fi.
- `dados/pontos_mapa.csv`: posição dos IDs na imagem.
- `mapa/campus.png`: planta/imagem real enviada para o projeto.
- `analise/`: classificação, prioridade e diagnóstico.
- `graficos/`: gráficos interativos.
- `mapa/`: mapa interativo.
- `app.py`: aplicação principal.

## Executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Observação

As coordenadas de `pontos_mapa.csv` estão em pixels da imagem
`mapa/campus.png` (1266 x 694). Se um ponto precisar ser reposicionado,
basta alterar X e Y no CSV.
