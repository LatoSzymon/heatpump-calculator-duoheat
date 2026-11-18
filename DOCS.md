#  Kompletna Dokumentacja Techniczna i Edukacyjna: Kalkulator Obiegu Pompy Ciepła (`heatpump-calculator`)

## Spis treści

1. [Po co powstał ten kalkulator i jak działa pompa ciepła?](#1-po-co-powstał-ten-kalkulator-i-jak-działa-pompa-ciepła)
2. [Architektura i struktura plików projektu](#2-architektura-i-struktura-plików-projektu)
3. [Użyte biblioteki i technologie (od podstaw)](#3-użyte-biblioteki-i-technologie-od-podstaw)
4. [Szczegółowe omówienie kodu — moduł po module](#4-szczegółowe-omówienie-kodu--moduł-po-module)
   - [`src/utils.py` — dane czynników, presety i walidacja](#41-srcutilspy--dane-czynników-presety-i-walidacja)
   - [`src/cycle_model.py` — serce symulacji (TESPy + CoolProp)](#42-srccycle_modelpy--serce-symulacji-tespy--coolprop)
   - [`src/optimizer.py` — algorytmy numeryczne (SciPy)](#43-srcoptimizerpy--algorytmy-numeryczne-scipy)
   - [`src/plotting.py` — wizualizacje interaktywne (Plotly)](#44-srcplottingpy--wizualizacje-interaktywne-plotly)
   - [`app.py` — interfejs webowy (Streamlit)](#45-apppy--interfejs-webowy-streamlit)
   - [`tests/test_cycle_model.py` — testy automatyczne (pytest)](#46-teststest_cycle_modelpy--testy-automatyczne-pytest)
5. [Uruchamianie aplikacji i testów](#5-uruchamianie-aplikacji-i-testów)

---

## 1. Po co powstał ten kalkulator i jak działa pompa ciepła?

Pompa ciepła **nie wytwarza** ciepła ze spalania paliwa ani z grzałki elektrycznej — ona **przenosi energię cieplną** z miejsca o niższej temperaturze (powietrze zewnętrzne, grunt) do miejsca o wyższej temperaturze (instalacja grzewcza w budynku).

Kalkulator modeluje **jednostopniowy lewobieżny obieg sprężarkowej pompy ciepła** (obieg Lindego) złożony z 4 głównych urządzeń i 4 punktów węzłowych:

1. **Parownik (`4 → 1`):** Ciekły czynnik chłodniczy pod niskim ciśnieniem (`p_evap`) wrze w niskiej temperaturze (`T_evap`), pobierając darmowe ciepło z otoczenia (`Q_evap`). Na końcu parownika para jest lekko **przegrzana** o `ΔT_sh`, aby żadna kropla cieczy nie trafiła do sprężarki.
2. **Sprężarka (`1 → 2`):** Zasysa chłodną parę (punkt `1`) i spręża ją do wysokiego ciśnienia (`p_cond`), zużywając energię elektryczną (`P_comp`). Wzrost ciśnienia powoduje gwałtowny wzrost temperatury do temperatury tłoczenia (`T_2`).
3. **Skraplacz (`2 → 3`):** Gorąca para oddaje ciepło do budynku (`Q_cond`). Proces ma 3 fazy: schładzanie gorącej pary (*desuperheating*), właściwe skraplanie w stałej temperaturze (`T_cond`) oraz **dochłodzenie** cieczy o `ΔT_sc` (do `T_3`).
4. **Zawór dławiący (`3 → 4`):** Ciecz pod wysokim ciśnieniem przepływa przez zwężkę. Ciśnienie spada do `p_evap` przy stałej entalpii (`h = const`), a czynnik gwałtownie stygnie do `T_4`, częściowo odparowując (powstaje tzw. *flash gas*, opisany stopniem suchości `x_4`).

### Najważniejsza zasada bilansu energii
$$\dot{Q}_{\text{cond}} = \dot{Q}_{\text{evap}} + P_{\text{comp}}$$

Współczynnik efektywności grzewczej **COP** (*Coefficient of Performance*) mówi, ile kilowatów ciepła otrzymujemy z 1 kW pobranego prądu:
$$\text{COP} = \frac{\dot{Q}_{\text{cond}}}{P_{\text{comp}}}$$

Im mniejsza różnica temperatur $\Delta T_{\text{lift}} = T_{\text{cond}} - T_{\text{evap}}$, tym mniej pracy musi wykonać sprężarka i tym wyższe jest `COP`.

---

## 2. Architektura i struktura plików projektu

```text
heatpump-calculator/
├── app.py                   # Warstwa prezentacji (interfejs webowy Streamlit + CSS + cache)
├── README.md                # Krótki opis projektu i instrukcja szybkiego startu
├── DOCS.md                  # Niniejsza szczegółowa dokumentacja techniczna
├── requirements.txt         # Lista bibliotek Pythona do zainstalowania przez pip
├── pyproject.toml           # Metadane projektu i konfiguracja pytest
├── src/
│   ├── __init__.py          # Eksport głównych klas i funkcji pakietu src
│   ├── utils.py             # Baza czynników, presety edukacyjne, konwersje jednostek, walidacja
│   ├── cycle_model.py       # Fizyczny model obiegu w TESPy + własności płynów z CoolProp
│   ├── optimizer.py         # Optymalizacja i analiza wrażliwości w SciPy
│   └── plotting.py          # Schemat ideowy, wykresy log(p)-h, T-s, bilans i mapa COP w Plotly
└── tests/
    └── test_cycle_model.py  # Zestaw testów jednostkowych (pytest)
```

Podział na osobne moduły w `src/` oddziela **fizykę** (`cycle_model.py`), **matematykę/optymalizację** (`optimizer.py`) i **grafikę** (`plotting.py`) od **interfejsu użytkownika** (`app.py`). Dzięki temu model można testować automatycznie bez uruchamiania przeglądarki.

---

## 3. Użyte biblioteki i technologie (od podstaw)

| Biblioteka | Rola w projekcie | Jak działa (w prostych słowach) |
|---|---|---|
| **TESPy** (`tespy`) | Rozwiązywanie bilansów masy i energii | Pozwala połączyć komponenty (`Compressor`, `SimpleHeatExchanger`, `Valve`, `CycleCloser`) w sieć i automatycznie rozwiązuje nieliniowy układ równań metodą Newtona-Raphsona. |
| **CoolProp** (`CoolProp`) | Baza własności termodynamicznych | Zwraca dokładne parametry czynników chłodniczych (ciśnienie nasycenia, entalpię `h`, entropię `s`, gęstość `ρ`, stopień suchości `x`) na podstawie równań stanu (Helmholtza). |
| **SciPy** (`scipy`) | Metody numeryczne | `root_scalar` (znajdowanie pierwiastka funkcją Brenta), `minimize_scalar` (szukanie minimum w przedziale) oraz `RegularGridInterpolator` (interpolacja kubiczna 2D na siatce). |
| **Streamlit** (`streamlit`) | Aplikacja webowa w czystym Pythonie | Zamienia skrypt `app.py` w interaktywną stronę WWW. Każda zmiana suwaka uruchamia skrypt ponownie z nowymi wartościami. |
| **Plotly** (`plotly`) | Interaktywne wykresy i schematy | Generuje wykresy wektorowe w przeglądarce z podpowiedziami po najechaniu myszką (`hovertemplate`), powiększaniem i przezroczystym tłem dla trybu ciemnego i jasnego. |
| **NumPy** (`numpy`) | Obliczenia na tablicach | Tworzy wektory punktów (`linspace`, `geomspace`, `meshgrid`) do rysowania krzywych nasycenia i siatek 2D. |
| **Pandas** (`pandas`) | Tabele danych | Przechowuje tabelę punktów węzłowych `1–4` (`DataFrame`) i pozwala ją pobrać jako plik CSV. |
| **pytest** (`pytest`) | Testy automatyczne | Uruchamia funkcje testowe w `tests/`, sprawdzając m.in. zamknięcie bilansu energii oraz poprawność optymalizacji. |

### Ważne konstrukcje Pythona użyte w projekcie
- **`@dataclass` i `@dataclass(frozen=True)`**: Automatycznie generują konstruktor `__init__` dla klas przechowujących dane (`CycleInput`, `CycleResult`, `RefrigerantInfo`, `ScenarioPreset`). Opcja `frozen=True` sprawia, że obiektu nie można przypadkowo zmodyfikować po utworzeniu.
- **Type hints (podpowiedzi typów)** np. `def c_to_k(temp_c: float) -> float:`: Informują programistę i edytor kodu, jakiego typu argumenty przyjmuje funkcja i co zwraca.
- **`@st.cache_data` (w `app.py`)**: Dekorator Streamlit zapamiętujący wynik funkcji dla danego zestawu argumentów. Jeśli użytkownik wróci do wcześniejszych nastaw, aplikacja odczyta wynik z pamięci zamiast ponownie uruchamiać solver TESPy.

---

## 4. Szczegółowe omówienie kodu — moduł po module

### 4.1. `src/utils.py` — dane czynników, presety i walidacja

Moduł przechowuje stałe słowniki konfiguracyjne i pilnuje, aby do modelu nie trafiły wartości niefizyczne.

- **`RefrigerantInfo` (`dataclass`)**: Opisuje czynnik chłodniczy polami: `code`, `name`, `chemical_formula`, `safety_group` (`A1`, `A2L`, `A3`, `B2L`), `gwp` (*Global Warming Potential*) oraz `description`.
- **`REFRIGERANTS`**: Słownik 7 obsługiwanych czynników: `R290`, `R32`, `R134a`, `R410A`, `R1234yf`, `R600a`, `R717`.
- **`ScenarioPreset` i `SCENARIO_PRESETS`**: 4 gotowe scenariusze edukacyjne (`air_floor_spring`, `air_radiators_winter`, `ground_floor`, `dhw_heating`) pokazujące typowe warunki pracy w praktyce.
- **`c_to_k`, `k_to_c`, `pa_to_bar`, `bar_to_pa`**: Proste funkcje przeliczające jednostki (`°C ↔ K`, `Pa ↔ bar`), ponieważ CoolProp operuje na jednostkach SI (`K`, `Pa`, `J/kg`), a inżynierowie i TESPy używają zwykle `°C`, `bar` i `kJ/kg`.
- **`get_fluid_limits(fluid: str) -> Dict[str, float]`**: Pyta `CP.PropsSI` o temperaturę krytyczną (`Tcrit`), ciśnienie krytyczne (`pcrit`) i minimalną temperaturę modelu (`Tmin`) dla wybranego czynnika.
- **`validate_cycle_inputs(...) -> None`**: Sprawdza m.in., czy `t_evap_c < t_cond_c - 2.0`, czy `t_cond_c` nie przekracza temperatury krytycznej (model jest podkrytyczny), czy temperatura po dochłodzeniu nie spada poniżej `t_evap_c`, oraz czy `eta_s` mieści się w `[0.1, 1.0]`. W razie błędu rzuca czytelny wyjątek `ValueError`.

---

### 4.2. `src/cycle_model.py` — serce symulacji (TESPy + CoolProp)

- **`_NETWORK_CACHE` i `_get_or_create_network(fluid: str)`**:
  Tworzenie sieci TESPy od zera jest czasochłonne. Dlatego dla każdego czynnika gotowa topologia sieci (`CycleCloser → Compressor → SimpleHeatExchanger (Skraplacz) → Valve → SimpleHeatExchanger (Parownik)`) jest tworzona raz i zapisywana w słowniku `_NETWORK_CACHE`.
  Ustawienia sieci (`nw.units.set_defaults(...)`) narzucają jednostki: `degC`, `bar`, `kJ/kg`, `kg/s`, `W`. Spadki ciśnienia w wymiennikach są pominięte (`pr=1.0`).
- **`_sample_isobar_segment(...)` i `_sample_isenthalp_segment(...)`**:
  Funkcje pomocnicze próbkujące pośrednie punkty termodynamiczne między głównymi węzłami. Dzięki nim na wykresie `T-s` schładzanie gorącej pary (`2 → x=1`), dochładzanie cieczy (`x=0 → 3`) i dławienie (`3 → 4`) są gładkimi, fizycznie dokładnymi krzywymi zamiast łamanych linii prostych.
- **`CycleInput` (`dataclass`)**: Struktura przechowująca 7 parametrów wejściowych (`fluid`, `t_evap_c`, `t_cond_c`, `superheat_k`, `subcooling_k`, `eta_s`, `q_cond_kw`).
- **`CycleResult` (`dataclass`)**: Struktura wynikowa zawierająca m.in.:
  - wskaźniki efektywności (`cop_heating`, `cop_cooling`, `cop_carnot`, `eta_exergetic`),
  - moce i przepływy (`q_cond_kw`, `q_evap_kw`, `p_comp_kw`, `mass_flow_kg_s`, `v_dot_suction_m3_h`),
  - ciśnienia i temperatury w punktach `1–4` (`p_evap_bar`, `p_cond_bar`, `pressure_ratio`, `t_1_c`, `t_discharge_c`, `t_3_c`, `t_4_c`),
  - podział ciepła w wymiennikach (`q_desuperheat_kw`, `q_cond_latent_kw`, `q_subcool_kw`, `q_evap_latent_kw`, `q_superheat_kw`),
  - `x_4` (stopień suchości pary za zaworem), `energy_balance_error_w` (kontrola błędu bilansu TESPy), `state_points_df` (tabela Pandas) oraz `plot_data` (słownik dla Plotly).
- **`HeatPumpCycle.solve(self) -> CycleResult`**:
  1. Wylicza ciśnienia nasycenia `p_evap_pa` i `p_cond_pa` oraz entalpie `h_1` (punkt `1`) i `h_3` (punkt `3`) w `CoolProp`.
  2. Pobiera sieć z `_NETWORK_CACHE`, zadaje moc skraplacza (`cond.set_attr(Q=-p.q_cond_kw * 1e3)` — znak minus oznacza oddawanie ciepła), sprawność sprężarki (`eta_s`) oraz ciśnienia/entalpie na połączeniach `c1`, `c2`, `c3`.
  3. Uruchamia `nw.solve(mode="design")`. Jeśli sieć z cache nie zbiegła, resetuje cache dla tego czynnika i ponawia próbę; w przypadku braku zbieżności rzuca `RuntimeError`.
  4. Odczytuje wyniki i zwraca gotowy obiekt `CycleResult`.

---

### 4.3. `src/optimizer.py` — algorytmy numeryczne (SciPy)

Moduł wykorzystuje `dataclasses.replace(base_input, ...)`, aby tworzyć zmodyfikowane kopie obiektu `CycleInput` bez zmieniania oryginału.

- **`find_evap_temp_for_target_cop(base_input, target_cop, t_evap_bounds)`**:
  Wykorzystuje `scipy.optimize.root_scalar(..., method="brentq")` do znalezienia miejsca zerowego funkcji `cop_heating(T_evap) - target_cop = 0`. Zwraca wymaganą temperaturę parowania `t_evap_c`, moc sprężarki i liczbę iteracji. Jeśli docelowe `COP` leży poza zakresem temperatur, zgłasza `ValueError`.
- **`optimize_subcooling(base_input, pinch_sink_temp_c, max_subcooling_k)`**:
  Wykorzystuje `scipy.optimize.minimize_scalar(..., method="bounded")` do znalezienia optymalnego dochłodzenia `ΔT_sc`. Uwzględnia ograniczenie fizyczne: jeśli dochłodzenie próbuje zejść poniżej temperatury wody powrotnej (`pinch_sink_temp_c + 2 K`), model wymusza podniesienie `t_cond_c`, co obniża `COP`. Zwraca również punkty krzywej `curve_sc_k` i `curve_cop` do narysowania wykresu.
- **`run_sensitivity_grid(base_input, t_evap_range, t_cond_range, n_points)`**:
  Oblicza siatkę `n_points × n_points` pełnych symulacji TESPy dla kombinacji `(T_evap, T_cond)`, a następnie używa `scipy.interpolate.RegularGridInterpolator(..., method="cubic")` do zagęszczenia danych na gęstą siatkę `35 × 35` dla płynnej mapy konturowej.

---

### 4.4. `src/plotting.py` — wizualizacje interaktywne (Plotly)

Wszystkie wykresy używają przezroczystego tła (`paper_bgcolor="rgba(0,0,0,0)"`, `plot_bgcolor="rgba(0,0,0,0)"`), dzięki czemu wyglądają spójnie zarówno w ciemnym, jak i jasnym motywie Streamlit.

- **`_compute_saturation_dome(fluid, n_points=120)`**: Wylicza punkty krzywej granicznej cieczy (`Q=0`) i pary (`Q=1`) w CoolProp, łącząc je w punkcie krytycznym w tzw. „dzwon nasycenia”.
- **`create_cycle_schematic(result)`**: Rysuje interaktywny schemat 4 komponentów (Parownik, Sprężarka, Skraplacz, Zawór) z kolorowymi przewodami, kierunkami przepływu, wartościami `T` i `p` w punktach `1–4` oraz strzałkami mocy `Q_evap`, `P_el`, `Q_cond`.
- **`create_energy_balance_bar(result)`**: Poziomy wykres słupkowy zestawiający `Q_evap + P_el` (źródło) z `Q_cond` (ciepło oddane do budynku).
- **`create_ph_diagram(plot_data)`**: Wykres Molliera `log(p)-h` z logarytmiczną osią ciśnienia. Adnotacje obszarów fazowych używają `np.log10(...)` dla współrzędnej `y`, ponieważ Plotly na osi logarytmicznej wymaga wartości zlogarytmowanych dla adnotacji.
- **`create_ts_diagram(plot_data)`**: Wykres `T-s` z gładką ścieżką przemian.
- **`create_cop_contour_plot(sensitivity_data, current_t_evap, current_t_cond)`**: Mapa konturowa `COP` z czerwoną gwiazdką oznaczającą aktualny punkt pracy.
- **`create_subcooling_curve_plot(opt_res)`**: Wykres `COP` w funkcji dochłodzenia `ΔT_sc` z zaznaczonym optimum.

---

### 4.5. `app.py` — interfejs webowy (Streamlit)

- **Konfiguracja i responsywny CSS**:
  `st.set_page_config(..., layout="wide", initial_sidebar_state="auto")` sprawia, że na komputerach pasek boczny jest widoczny, a na telefonach automatycznie się zwija. Własny CSS definiuje:
  - `.kpi-grid` (CSS Grid układający 6 kart KPI w 6 kolumn na dużym ekranie i 2 kolumny na telefonie),
  - `.step-card` (półprzezroczyste karty 4 etapów obiegu),
  - poziome przewijanie zakładek (`[data-baseweb="tab-list"]`) na ekranach `< 768px`.
- **Zarządzanie stanem (`st.session_state`) i callbacki**:
  - `_apply_preset(preset_id)` wpisuje parametry wybranego scenariusza do `st.session_state`.
  - `_on_preset_change()` aktualizuje suwaki przy wyborze scenariusza.
  - `_mark_custom()` automatycznie przełącza listę scenariuszy na `"Własne ustawienia"`, gdy użytkownik ręcznie przesunie dowolny suwak.
- **Buforowanie (`@st.cache_data`)**:
  Funkcje `solve_cycle_cached`, `find_evap_temp_cached`, `optimize_subcooling_cached` i `run_sensitivity_grid_cached` przyspieszają działanie aplikacji, unikając powtarzania identycznych obliczeń.
- **Obsługa błędów**:
  Każdy etap (pobieranie granic czynnika, solver TESPy, generowanie wykresów, optymalizacje SciPy) jest zabezpieczony blokami `try / except`, które w razie problemu wyświetlają czytelny komunikat po polsku zamiast surowego błędu Pythona.
- **5 zakładek aplikacji**:
  1. `Schemat i mechanika` — schemat ideowy na żywo, bilans mocy i opis 4 etapów z aktualnymi liczbami.
  2. `Wykresy log(p)-h i T-s` — instrukcja czytania wykresów + oba wykresy termodynamiczne.
  3. `Punkty i bilans` — tabela stanów `1–4` z eksportem do CSV, podział mocy w wymiennikach i kontrola błędu bilansu TESPy.
  4. `Optymalizacja (SciPy)` — wyznaczanie `T_evap` dla zadanego `COP`, optymalizacja dochłodzenia z wykresem oraz mapa konturowa `COP`.
  5. `Słowniczek` — kompendium pojęć (`COP`, Carnot, przegrzanie, dochłodzenie, stopień suchości, `GWP`, grupy bezpieczeństwa).
- **Stopka**: Informacja o autorze aplikacji — klikalny link do profilu GitHub Szymona Lato (`https://github.com/LatoSzymon`).

---

### 4.6. `tests/test_cycle_model.py` — testy automatyczne (pytest)

Zawiera 13 przypadków testowych weryfikujących:
- `test_single_stage_r290_energy_balance` — zamknięcie bilansu energii (`|Q_cond - (Q_evap + P_comp)| < 1e-2 W`), zależność `COP_grz ≈ COP_chł + 1` oraz podział stref ciepła.
- `test_multiple_refrigerants` — poprawność obliczeń dla wszystkich 7 czynników (`R290`, `R32`, `R134a`, `R410A`, `R1234yf`, `R600a`, `R717`).
- `test_scenario_presets_solve` — sprawdzenie, czy wszystkie presety z `SCENARIO_PRESETS` zbiegają bez błędów.
- `test_validation_errors` — weryfikacja rzucania `ValueError` dla błędnych danych wejściowych.
- `test_scipy_root_scalar_target_cop` oraz `test_scipy_optimize_subcooling_and_grid` — testy modułu `optimizer.py`.
- `test_plotting_diagrams` — weryfikacja poprawnego generowania obiektów `go.Figure` w `plotting.py`.

---

## 5. Uruchamianie aplikacji i testów

W katalogu głównym projektu (w środowisku `.venv`):

```powershell
# Uruchomienie aplikacji webowej Streamlit
.\.venv\Scripts\streamlit.exe run app.py

# Uruchomienie pełnego zestawu testów jednostkowych
.\.venv\Scripts\pytest.exe -v
```
