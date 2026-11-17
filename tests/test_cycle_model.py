"""Testy jednostkowe dla modelu obiegu pompy ciepła (TESPy + SciPy + CoolProp)."""

import pytest
from src.cycle_model import CycleInput, HeatPumpCycle
from src.optimizer import (
    find_evap_temp_for_target_cop,
    optimize_subcooling,
    run_sensitivity_grid,
)
from src.plotting import (
    create_cop_contour_plot,
    create_cycle_schematic,
    create_energy_balance_bar,
    create_ph_diagram,
    create_subcooling_curve_plot,
    create_ts_diagram,
)
from src.utils import SCENARIO_PRESETS


def test_single_stage_r290_energy_balance():
    """Sprawdza zbieżność modelu TESPy dla R290 oraz zamknięcie bilansu energii."""
    inp = CycleInput(
        fluid="R290",
        t_evap_c=0.0,
        t_cond_c=45.0,
        superheat_k=5.0,
        subcooling_k=5.0,
        eta_s=0.78,
        q_cond_kw=10.0,
    )
    res = HeatPumpCycle(inp).solve()

    assert res.q_cond_kw == pytest.approx(10.0, rel=1e-4)
    assert abs(res.energy_balance_error_w) < 1e-2
    assert res.q_cond_kw == pytest.approx(res.q_evap_kw + res.p_comp_kw, rel=1e-4)
    assert res.cop_heating == pytest.approx(res.cop_cooling + 1.0, rel=1e-3)
    assert 3.0 < res.cop_heating < 6.0
    assert len(res.state_points_df) == 4
    assert 0.0 < res.x_4 < 1.0
    assert res.t_discharge_c > inp.t_cond_c
    assert res.q_desuperheat_kw + res.q_cond_latent_kw + res.q_subcool_kw == pytest.approx(
        res.q_cond_kw, rel=1e-2
    )
    assert res.q_evap_latent_kw + res.q_superheat_kw == pytest.approx(
        res.q_evap_kw, rel=1e-2
    )


@pytest.mark.parametrize(
    "fluid", ["R290", "R32", "R134a", "R410A", "R1234yf", "R600a", "R717"]
)
def test_multiple_refrigerants(fluid: str):
    """Sprawdza działanie modelu dla wszystkich obsługiwanych czynników chłodniczych."""
    inp = CycleInput(
        fluid=fluid,
        t_evap_c=-5.0,
        t_cond_c=40.0,
        superheat_k=4.0,
        subcooling_k=4.0,
        eta_s=0.75,
        q_cond_kw=8.0,
    )
    res = HeatPumpCycle(inp).solve()
    assert res.cop_heating > 2.5
    assert res.pressure_ratio > 1.5
    assert res.mass_flow_kg_s > 0.0


def test_scenario_presets_solve():
    """Sprawdza, czy wszystkie gotowe scenariusze edukacyjne rozwiązują się poprawnie."""
    for preset in SCENARIO_PRESETS.values():
        inp = CycleInput(
            fluid=preset.fluid,
            t_evap_c=preset.t_evap_c,
            t_cond_c=preset.t_cond_c,
            superheat_k=preset.superheat_k,
            subcooling_k=preset.subcooling_k,
            eta_s=preset.eta_s,
            q_cond_kw=preset.q_cond_kw,
        )
        res = HeatPumpCycle(inp).solve()
        assert res.cop_heating > 2.0
        assert abs(res.energy_balance_error_w) < 1e-2


def test_validation_errors():
    """Weryfikuje zgłaszanie wyjątków dla niefizycznych parametrów wejściowych."""
    with pytest.raises(ValueError, match="Temperatura parowania"):
        HeatPumpCycle(CycleInput(t_evap_c=45.0, t_cond_c=40.0))

    with pytest.raises(ValueError, match="Nieobsługiwany czynnik"):
        HeatPumpCycle(CycleInput(fluid="UNKNOWN_FLUID"))


def test_scipy_root_scalar_target_cop():
    """Sprawdza wyznaczanie temperatury parowania dla zadanego COP za pomocą SciPy."""
    base = CycleInput(fluid="R290", t_evap_c=0.0, t_cond_c=45.0)
    target = 4.2
    sol = find_evap_temp_for_target_cop(base, target_cop=target)

    assert sol["converged"] is True
    assert sol["achieved_cop"] == pytest.approx(target, abs=1e-2)


def test_scipy_optimize_subcooling_and_grid():
    """Sprawdza optymalizację dochłodzenia i interpolację siatki wrażliwości SciPy."""
    base = CycleInput(fluid="R290", t_evap_c=0.0, t_cond_c=45.0, subcooling_k=5.0)
    opt = optimize_subcooling(base, pinch_sink_temp_c=32.0)
    assert 0.0 <= opt["optimal_subcooling_k"] <= 20.0
    assert opt["max_cop"] > 3.0
    assert len(opt["curve_sc_k"]) == 15
    assert len(opt["curve_cop"]) == 15

    grid = run_sensitivity_grid(
        base, t_evap_range=(-10.0, 10.0), t_cond_range=(35.0, 50.0), n_points=4
    )
    assert grid["cop_grid"].shape == (4, 4)
    assert grid["fine_cop"].shape == (35, 35)


def test_plotting_diagrams():
    """Sprawdza generowanie wszystkich wykresów Plotly (schemat, bilans, log(p)-h, T-s, mapa COP)."""
    inp = CycleInput(fluid="R290", t_evap_c=0.0, t_cond_c=45.0)
    res = HeatPumpCycle(inp).solve()

    fig_schematic = create_cycle_schematic(res)
    fig_balance = create_energy_balance_bar(res)
    fig_ph = create_ph_diagram(res.plot_data)
    fig_ts = create_ts_diagram(res.plot_data)
    grid = run_sensitivity_grid(inp, n_points=4)
    fig_contour = create_cop_contour_plot(grid, inp.t_evap_c, inp.t_cond_c)
    opt = optimize_subcooling(inp, pinch_sink_temp_c=32.0)
    fig_subcool = create_subcooling_curve_plot(opt)

    assert len(fig_schematic.data) >= 5
    assert len(fig_balance.data) == 3
    assert len(fig_ph.data) == 3
    assert len(fig_ts.data) == 3
    assert len(fig_contour.data) == 2
    assert len(fig_subcool.data) == 2
