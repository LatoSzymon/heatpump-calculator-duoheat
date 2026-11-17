"""Moduł optymalizacji i analiz parametrycznych wykorzystujący bibliotekę SciPy."""

from dataclasses import replace
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy.optimize import root_scalar, minimize_scalar
from scipy.interpolate import RegularGridInterpolator

from src.cycle_model import CycleInput, HeatPumpCycle
from src.utils import get_fluid_limits


def find_evap_temp_for_target_cop(
    base_input: CycleInput,
    target_cop: float,
    t_evap_bounds: Tuple[float, float] = (-25.0, 25.0),
) -> Dict[str, Any]:
    """
    Wyznacza za pomocą `scipy.optimize.root_scalar` (metoda Brenta) wymaganą temperaturę
    parowania T_evap [°C], aby osiągnąć zadany współczynnik COP_grzewcze.
    """
    limits = get_fluid_limits(base_input.fluid)
    low = max(t_evap_bounds[0], limits["T_min_C"] + 2.0)
    high = min(
        t_evap_bounds[1],
        base_input.t_cond_c - max(base_input.subcooling_k + 1.0, 3.0),
    )

    if low >= high:
        raise ValueError(
            "Przedział poszukiwań temperatury parowania jest pusty dla zadanej temperatury skraplania."
        )

    def objective(t_evap: float) -> float:
        trial_input = replace(base_input, t_evap_c=float(t_evap))
        res = HeatPumpCycle(trial_input).solve()
        return res.cop_heating - target_cop

    f_low = objective(low)
    f_high = objective(high)

    if f_low * f_high > 0:
        cop_min = f_low + target_cop
        cop_max = f_high + target_cop
        raise ValueError(
            f"Zadane COP = {target_cop:.2f} jest poza osiągalnym zakresem "
            f"[{cop_min:.2f}, {cop_max:.2f}] dla T_evap w [{low:.1f}, {high:.1f}] °C."
        )

    sol = root_scalar(objective, bracket=[low, high], method="brentq", xtol=1e-3)
    optimal_input = replace(base_input, t_evap_c=float(sol.root))
    optimal_result = HeatPumpCycle(optimal_input).solve()

    return {
        "converged": bool(sol.converged),
        "iterations": int(sol.iterations),
        "t_evap_c": float(sol.root),
        "achieved_cop": optimal_result.cop_heating,
        "p_comp_kw": optimal_result.p_comp_kw,
    }


def optimize_subcooling(
    base_input: CycleInput,
    pinch_sink_temp_c: float,
    max_subcooling_k: float = 20.0,
) -> Dict[str, Any]:
    """
    Optymalizuje stopień dochłodzenia cieczy za pomocą `scipy.optimize.minimize_scalar` (metoda bounded)
    w celu maksymalizacji efektywnego COP przy uwzględnieniu temperatury wody powrotnej górnego źródła.
    """
    upper_bound = min(
        max_subcooling_k,
        max(1.0, base_input.t_cond_c - base_input.t_evap_c - 3.0),
        max(1.0, base_input.t_cond_c - pinch_sink_temp_c + 5.0),
    )

    def eval_cop(sc_k: float) -> float:
        # Gdy dochłodzenie próbuje zejść poniżej (T_powrotu + 2 K pinch),
        # konieczne jest podniesienie temperatury skraplania, co obniża COP.
        effective_t_cond = max(base_input.t_cond_c, pinch_sink_temp_c + sc_k + 2.0)
        trial = replace(
            base_input,
            subcooling_k=float(sc_k),
            t_cond_c=float(effective_t_cond),
        )
        res = HeatPumpCycle(trial).solve()
        return res.cop_heating

    opt = minimize_scalar(
        lambda sc: -eval_cop(sc), bounds=(0.0, upper_bound), method="bounded"
    )
    best_sc = float(opt.x)
    best_cop = float(-opt.fun)

    # Krzywa poglądowa COP(ΔT_sc) dla wykresu edukacyjnego
    sc_samples = np.linspace(0.0, upper_bound, 15)
    cop_samples = [eval_cop(float(sc)) for sc in sc_samples]

    return {
        "optimal_subcooling_k": best_sc,
        "max_cop": best_cop,
        "iterations": int(opt.nfev),
        "curve_sc_k": sc_samples.tolist(),
        "curve_cop": cop_samples,
    }


def run_sensitivity_grid(
    base_input: CycleInput,
    t_evap_range: Tuple[float, float] = (-15.0, 15.0),
    t_cond_range: Tuple[float, float] = (30.0, 60.0),
    n_points: int = 7,
) -> Dict[str, Any]:
    """
    Generuje siatkę charakterystyk COP i mocy sprężarki dla zakresu (T_evap, T_cond)
    oraz buduje interpolator `scipy.interpolate.RegularGridInterpolator` do szybkiego
    zagęszczenia mapy sprawności.
    """
    limits = get_fluid_limits(base_input.fluid)
    safe_evap_min = max(t_evap_range[0], limits["T_min_C"] + 2.0)
    safe_cond_max = min(t_cond_range[1], limits["T_crit_C"] - 3.0)
    safe_cond_min = max(t_cond_range[0], safe_evap_min + 5.0)
    safe_evap_max = min(t_evap_range[1], safe_cond_min - 3.0)

    t_evap_vals = np.linspace(safe_evap_min, safe_evap_max, n_points)
    t_cond_vals = np.linspace(safe_cond_min, safe_cond_max, n_points)

    cop_grid = np.zeros((n_points, n_points))
    p_comp_grid = np.zeros((n_points, n_points))

    records = []
    for i, t_ev in enumerate(t_evap_vals):
        for j, t_cd in enumerate(t_cond_vals):
            sc = min(base_input.subcooling_k, max(0.0, t_cd - t_ev - 3.0))
            trial = replace(
                base_input,
                t_evap_c=float(t_ev),
                t_cond_c=float(t_cd),
                subcooling_k=float(sc),
            )
            res = HeatPumpCycle(trial).solve()
            cop_grid[i, j] = res.cop_heating
            p_comp_grid[i, j] = res.p_comp_kw
            records.append(
                {
                    "T_evap [°C]": float(t_ev),
                    "T_cond [°C]": float(t_cd),
                    "COP [-]": round(res.cop_heating, 3),
                    "P_comp [kW]": round(res.p_comp_kw, 3),
                    "Q_evap [kW]": round(res.q_evap_kw, 3),
                }
            )

    interp_cop = RegularGridInterpolator(
        (t_evap_vals, t_cond_vals), cop_grid, method="cubic"
    )

    fine_evap = np.linspace(safe_evap_min, safe_evap_max, 35)
    fine_cond = np.linspace(safe_cond_min, safe_cond_max, 35)
    ee, cc = np.meshgrid(fine_evap, fine_cond, indexing="ij")
    fine_cop = interp_cop((ee, cc))

    return {
        "t_evap_vals": t_evap_vals,
        "t_cond_vals": t_cond_vals,
        "cop_grid": cop_grid,
        "p_comp_grid": p_comp_grid,
        "fine_evap": fine_evap,
        "fine_cond": fine_cond,
        "fine_cop": fine_cop,
        "dataframe": pd.DataFrame(records),
    }
