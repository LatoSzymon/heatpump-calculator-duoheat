# Kalkulator i Symulator Obiegu Pompy Ciepła (`heatpump-calculator`)

Interaktywny kalkulator jednostopniowego obiegu sprężarkowej pompy ciepła z przegrzaniem i dochłodzeniem, zbudowany w języku Python przy użyciu bibliotek:
- **TESPy** (`tespy`) — modelowanie topologii układu i rozwiązywanie nieliniowego układu równań bilansu masy i energii,
- **CoolProp** (`CoolProp`) — wyznaczanie własności termodynamicznych czynników chłodniczych (`R290`, `R32`, `R134a`, `R410A`, `R1234yf`, `R600a`, `R717`),
- **SciPy** (`scipy.optimize`, `scipy.interpolate`) — poszukiwanie punktu pracy dla zadanego $\text{COP}$, optymalizacja dochłodzenia oraz dwuwymiarowa interpolacja kubiczna mapy sprawności,
- **Streamlit** + **Plotly** — interaktywna aplikacja webowa z wykresami $\log(p)\text{-}h$ (Molliera) oraz $T\text{-}s$ na żywo.

---

##  Szybki start

### 1. Aktywacja środowiska wirtualnego i instalacja zależności

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Uruchomienie aplikacji webowej Streamlit

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

### 3. Uruchomienie testów jednostkowych

```powershell
.\.venv\Scripts\pytest.exe -v
```

---

## Struktura projektu

- `src/cycle_model.py` — klasa `HeatPumpCycle` budująca i rozwiązująca obieg w `TESPy` (`CycleCloser`, `Compressor`, `SimpleHeatExchanger`, `Valve`).
- `src/optimizer.py` — algorytmy numeryczne oparte na `SciPy` (`root_scalar`, `minimize_scalar`, `RegularGridInterpolator`).
- `src/plotting.py` — generowanie wykresów $\log(p)\text{-}h$, $T\text{-}s$ oraz mapy konturowej $\text{COP}$.
- `src/utils.py` — baza czynników chłodniczych, konwersje jednostek i walidacja ograniczeń fizycznych (punkt krytyczny).
- `app.py` — interfejs użytkownika w `Streamlit`.
- `tests/test_cycle_model.py` — testy jednostkowe bilansu energii i modułu `SciPy`.
- `DOCS.md` — **pełna dokumentacja techniczna i edukacyjna** dla nowych pracowników (omówienie fizyki, bibliotek, funkcji i architektury).
