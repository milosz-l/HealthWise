# AASD 24Z projekt
- prowadzący: Tomasz Śliwińśki
- zespół: MegaAgentyAI
- skład zespołu:
    - Marcel Tracz
    - Maksim Makaranka
    - Jan Retkowski
    - Miłosz Łopatto
- repozytorium: https://github.com/milosz-l/AASD

## Dokumentacja wstępna: raport A - identyfikacja problemu 

### Analiza burzy mózgów

Podczas burzy mózgów skoncentrowano się na tworzeniu koncepcji systemów, które mogłyby wspierać rozwój "mądrego miasta". W trakcie dyskusji zaproponowano różne rozwiązania, mające na celu ułatwienie życia mieszkańcom i odwiedzającym miasto poprzez optymalizację i integrację dostępnych usług.

Jednym z rozważanych pomysłów był system do identyfikacji i zarządzania problemami z infrastrukturą miejską. System ten miał umożliwiać mieszkańcom zgłaszanie problemów, takich jak awarie czy uszkodzenia, przy jednoczesnym sprawdzeniu ich statusu i priorytetu. Ostatecznie pomysł ten został odrzucony, ponieważ podobne aplikacje już funkcjonują w wielu miastach, efektywnie obsługując tego rodzaju zgłoszenia, np. w przypadku Warszawy istnieje serwis dostępny pod [linkiem](https://warszawa19115.pl/incydenty).

Innym pomysłem było stworzenie informatora o wydarzeniach i ciekawych miejscach dla turystów i mieszkańców. Projekt ten miał na celu dostarczanie spersonalizowanych informacji o lokalnych wydarzeniach i atrakcjach, bazując na zainteresowaniach użytkowników i ich bieżącej lokalizacji. Zrezygnowano jednak z tego rozwiązania z uwagi na dużą liczbę dostępnych już narzędzi oferujących podobne usługi.


### Identyfikacja i opis problemu
Współczesne społeczeństwo stoi przed wyzwaniem szybkiego rozprzestrzeniania się chorób zakaźnych, co często wyprzedza możliwości ich szybkiego wykrycia i kontrolowania. Brakuje zintegrowanego systemu monitorującego objawy chorób w czasie rzeczywistym, co ogranicza zdolność do szybkiej identyfikacji potencjalnych ognisk epidemicznych.

Dodatkowym problemem jest brak narzędzi umożliwiających ludziom łatwe zgłaszanie objawów oraz otrzymywanie wstępnej oceny ich znaczenia. Bez takiego systemu trudno jest gromadzić i analizować dane na temat zdrowia publicznego w sposób skuteczny. Potrzebne jest rozwiązanie, które nie tylko umożliwi zbieranie i analizowanie danych o objawach z różnych lokalizacji, ale także wspierać będzie służby zdrowia w identyfikacji zagrożeń epidemicznych i reagowaniu na nie w odpowiednim czasie.
#### Interesariusze:
- Służby zdrowia (np. sanepid, instytuty epidemiologiczne)
- Władze lokalne i krajowe (np. ministerstwa zdrowia)
- Badacze i naukowcy (specjaliści zajmujący się epidemiologią)
- Pracownicy służb ratunkowych (np. zespoły medyczne, ratownicy)
- Pacjenci (osoby dotknięte zakażeniem)
- Lekarze
- Dostawcy systemów danych medycznych (bazy danych, aplikacje zdrowotne)
- Specjaliści ds. epidemiologii (analitycy zajmujący się danymi o chorobach)

#### Zastosowania:
- Dokonywanie wspępnej diagnozy na podstawie objawów
- Pomaganie specjalistom w diagnozowaniu pacjentów
- Polecanie użytkownikom do jakiej specjalizacji lekarza się udać
- Lokalizacja ognisk zakażeń chorób zakaźnych

### Propozycja i sprecyzowanie rozwiązania

W obliczu zidentyfikowanego problemu proponujemy stworzenie innowacyjnego systemu, który w znaczący sposób usprawni wczesną identyfikację i kontrolę potencjalnych ognisk epidemicznych. Projekt zakłada opracowanie zintegrowanej platformy, która umożliwi:

1. **Łatwe zgłaszanie objawów**: Użytkownicy będą mogli przesyłać informacje o swoich objawach za pośrednictwem intuicyjnego interfejsu obsługiwanego za pomocą języka naturalnego. Umożliwi to szybkie przeprowadzenie wstępnej oceny medycznej bez potrzeby bezpośredniego kontaktu z placówkami zdrowia, co zredukuje obciążenie systemu opieki zdrowotnej.

2. **Gromadzenie i analiza danych zdrowotnych**: Dane zebrane od użytkowników będą przechowywane i analizowane w czasie rzeczywistym, co pozwoli na identyfikację oraz śledzenie wzorców zachorowań w różnych lokalizacjach.

3. **Wsparcie dla służb zdrowia**: System zapewni cenne informacje instytucjom medycznym i badaczom, ułatwiając monitorowanie sytuacji epidemiologicznej oraz wspieranie decyzji dotyczących zarządzania zdrowiem publicznym.

4. **Informacje zwrotne i rekomendacje**: Użytkownicy otrzymają rekomendacje dotyczące dalszych kroków, np. czy powinni skonsultować się ze specjalistą, oraz informacje na temat lokalnych placówek medycznych.

Dzięki temu rozwiązaniu możliwe jest nie tylko usprawnienie indywidualnego zarządzania zdrowiem użytkowników, ale także wsparcie służb medycznych w reagowaniu na sytuacje kryzysowe związane z chorobami zakaźnymi. W rezultacie proponowany system stanowi istotny wkład w poprawę zdrowia publicznego i bezpieczeństwa epidemiologicznego.

### Proponowana architektura rozwiązania
Planowana jest implementacja systemu wieloagentowego opartego na dużych modelach językowych (LLM), co umożliwi efektywne rozdzielenie zadań między wyspecjalizowanymi modułami, zwiększając możliwości przetwarzania i analizy danych. Dzięki zastosowaniu LLM, system będzie mógł lepiej rozumieć kontekst i intencje użytkowników, dostarczając trafniejsze rekomendacje oraz szybciej adaptując się do dynamicznie zmieniających się warunków.

Poniżej znajdują się opisy prototypowych agentów, które pełnią różne funkcje w systemie, począwszy od prowadzenia rozmów z użytkownikiem, aż po analizę i wizualizację danych dotyczących ognisk epidemicznych. Każdy z tych agentów specjalizuje się w konkretnym zadaniu, co zwiększa precyzję i skuteczność całego systemu w reagowaniu na potencjalne zagrożenia zdrowotne.

- Agent chatbota – prowadzi rozmowy z użytkownikiem, uwzględniając historię konwersacji.
- Agent walidacji – analizuje wiadomości użytkownika pod kątem medycznym, normalizuje listę objawów (w tym celu można zdefiniować listę dostępnych opcji) oraz informuje agenta chatbota, aby poprosił o lokalizację użytkownika, jeśli nie została podana wcześniej.
- Agent doradczy – określa właściwą dziedzinę medycyny (np. dermatologia, onkologia) i wykonuje podstawowe polecenia medyczne, które są następnie przekazywane do agenta chatbota w celu dalszej komunikacji z użytkownikiem. Przekazuje również informacje o powiązaniu lokalizacji z objawami do agenta analizy ognisk. Możliwe jest doradztwo bez opierania się na RAG, korzystając z wiedzy wbudowanej w LLM, w celu uproszczenia procesu implementacji.
- Agent analizy ognisk epidemiologicznych – zbiera dane dotyczące lokalizacji i objawów, identyfikuje powtarzające się wzorce w określonych obszarach, przekazuje zidentyfikowane przypadki w spójnych obszarach do agenta wizualizacyjnego oraz dostarcza informacji o potencjalnym zagrożeniu epidemicznym agentowi chatbota.
- Agent wizualizacyjny – wizualizuje ogniska na mapie, zaznaczając obszary o podobnych objawach w jednolitych kolorach.

#### Potencjalne rozszerzenie zakresu systemu:
- Agent prognozowania epidemii – analizuje wzrost obszaru epidemii w czasie, modelując rozwój epidemii w przyszłości, przekazuje te dane do agenta administratora, który je wizualizuje.
- Integracja z placówkami medycznymi, aby zbierać więcej informacji o przypadkach chorobowych w celu usprawnienia analizy i prognozowania ognisk.
- Sugerowanie użytkownikom odpowiednich placówek medycznych w pobliżu.

### Udział w Hackathonie

Nasz zespół planuje wzięcie udziału w hackathonie, który odbywa się na platformie [lablab.ai](lablab.ai). Hackathon Challenge, pod hasłem Lōkahi, skupia się na współpracy i innowacjach w dziedzinie opieki zdrowotnej.

Celem wydarzenia jest stworzenie ekosystemu zdrowotnego, który integruje różne aspekty opieki medycznej, płatności, zdrowia publicznego, bezpieczeństwa pacjentów i badań klinicznych przy pomocy sztucznej inteligencji. Rozwiązania te mają oferować większą kontrolę prywatności, poprawiać zdrowie przy niższych kosztach oraz promować równość zdrowotną.

Hackathon jest otwarty do 24 listopada. Informacje o hackathonie są dostępne pod [linkiem](https://lablab.ai/event/lokahi-innovation-in-healthcare).