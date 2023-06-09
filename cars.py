from matplotlib.text import Text
import requests
from bs4 import BeautifulSoup
import time
import json
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredOffsetbox, AnnotationBbox, OffsetBox, TextArea

model = str(input('Podaj marke samochodu: ')).lower().replace(' ', '-')
print(model)
url = f'https://www.otomoto.pl/osobowe/{model}/?page='
headers = {'User-agent': 'Mozilla/5.0'}

# ustaw maksymalną ilość stron, które chcesz przeszukać
max_pages = int(input('Ile stron chcesz przeszukac?: '))

#ustaw kwote
initial_amount = int(input('Jaki jest twoj budzet?: '))

#lista, ktora wpisujemy do jsona
data = []

#scrapowanie
for page in range(1, max_pages + 1):
    print(f"Strona:{page} ")
    print(f"Model: {model}")
    response = requests.get(url + str(page), headers=headers)
    if response.status_code != 200:
        print(f"Wystąpił błąd. Kod odpowiedzi: {response.status_code}")
        continue
    soup = BeautifulSoup(response.content, 'html.parser')

    #kontenery, ktore zawieraja cale info o autach
    container_of_elements = soup.find_all('article', {'class': 'ooa-1nix3k0 evg565y0'}) 

    for elements in container_of_elements:
        prices = soup.find_all('span', {'class': 'ooa-1bmnxg7 evg565y11'}) #ceny na stronie
        links = soup.find_all('h2', {'class': 'evg565y6 evg565y20 ooa-10p8u4x er34gjf0'}) #linki do aut

for elements in container_of_elements:
    prices = soup.find_all('span', {'class': 'ooa-1bmnxg7 evg565y11'}) #ceny na stronie
    links = soup.find_all('h2', {'class': 'evg565y6 evg565y20 ooa-10p8u4x er34gjf0'}) #linki do aut

    for striped_price in prices:
        final_price_value = float(striped_price.text.strip().replace(' ', '').replace('PLN', '').replace('USD', '').replace('EUR', ''))

        #"algorytm" przyporzadkowujacy ceny do odpowiednich linkow i ich wstawienie do jsona
        if final_price_value <= initial_amount:
            print(int(final_price_value))
            for i, one_price in enumerate(prices):
                if one_price == striped_price:
                    final_link = links[i].a['href']
                    print(final_link)
            data.append({'price': final_price_value, 'link': final_link})
            with open("prices.json", 'w') as f:
                json.dump(data, f)


    time.sleep(0.8)  # aby nie przeciążyć serwera, dodalem opóźnienie

#wizualizacja danych
with open("prices.json", 'r') as f:
    data = json.load(f)

prices_visualization = [item['price'] for item in data]
links_visualization = [' '.join(item['link'].split('/oferta/')[1].split("-ID")[0].replace("-", " ").split()[:2]) for item in data]

# Generuj wykres słupkowy
fig, ax = plt.subplots()
bars = ax.bar(range(len(prices_visualization)), prices_visualization)
plt.xlabel('Indeks')
plt.ylabel('Cena')
plt.title('Ceny samochodów')

# Ustaw etykiety osi x na linki
ax.set_xticks(range(len(prices_visualization)))
ax.set_xticklabels(links_visualization, rotation='vertical')



# Wyświetl wykres
plt.tight_layout()
plt.show()
