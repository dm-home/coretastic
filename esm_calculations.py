import numpy as np

def compute_mineral_mass(bd, depth, soc, k=1.9):
    MT = bd * depth * 1e4 * 1e-6
    return MT * (1 - k * soc)

def esm_correction_fixed(bd_i, soc_i, bd_n, soc_n, depth=30, k=1.9):
    Da = depth * (bd_i / bd_n) * ((1 - k * soc_i) / (1 - k * soc_n))
    original = bd_n * depth * soc_n * 1e-2
    corrected = bd_n * Da * soc_n * 1e-2
    return Da, original, corrected

def exponential_soc_profile(soc0, soc_inf, depth, k_decay, increments=1):
    depths = np.arange(increments, depth + increments, increments)
    return soc_inf + (soc0 - soc_inf) * np.exp(-depths * k_decay)

def linear_bd_profile(bd_surface, bd_bottom, depth, increments=1):
    return np.linspace(bd_surface, bd_bottom, int(depth / increments))

def esm_correction_profile(bd_i_profile, soc_i_profile, bd_n_profile, soc_n_profile,
                           depth, increments=1, k=1.9):
    mi = bd_i_profile * increments * 1e4 * 1e-6 * (1 - k * soc_i_profile)
    mn = bd_n_profile * increments * 1e4 * 1e-6 * (1 - k * soc_n_profile)
    delta_m = mi.sum() - mn.sum()
    j = len(bd_n_profile) - 1
    Da = depth + delta_m / (bd_n_profile[j] * (1 - k * soc_n_profile[j]) * increments * 1e4 * 1e-6)
    base = (bd_n_profile * increments * soc_n_profile * 1e-2).sum()
    extra = bd_n_profile[j] * (increments + Da - depth) * soc_n_profile[j] * 1e-2
    return base - (bd_n_profile[j]*increments*soc_n_profile[j]*1e-2) + extra
