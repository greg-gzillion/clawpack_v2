# Analog Circuit Design Reference
## All URLs verified May 2026

## Basic Component Symbols
| Component | Schematic Symbol | Key Parameters | Source |
|-----------|----------------|---------------|--------|
| Resistor | Zigzag line (ANSI) or rectangle (IEC) | Value (ohms), tolerance, power rating | https://en.wikipedia.org/wiki/Electronic_symbol |
| Capacitor | Two parallel lines (non-polarized); curved+straight (polarized) | Value (pF, nF, uF), voltage rating, dielectric type | https://en.wikipedia.org/wiki/Electronic_symbol |
| Inductor | Looped coil | Inductance (uH, mH), current rating, DC resistance | https://en.wikipedia.org/wiki/Electronic_symbol |
| Transformer | Two inductors with parallel lines between (core symbol) | Primary/secondary voltage, VA rating, turns ratio | https://en.wikipedia.org/wiki/Electronic_symbol |

## Voltage Divider (Fundamental Circuit)
| Parameter | Formula | Notes | Source |
|-----------|---------|-------|--------|
| Output voltage | Vout = Vin * R2/(R1+R2) | Unloaded output; loading reduces Vout proportionally to load/divider impedance ratio | https://en.wikipedia.org/wiki/Voltage_divider |
| Rule of thumb | R_load >= 10 * R2 | Keeps loading error under 10% from ideal unloaded voltage | https://en.wikipedia.org/wiki/Voltage_divider |
| Divider current | I = Vin/(R1+R2) | Trade-off: lower R values = more stable under load but higher power consumption | https://en.wikipedia.org/wiki/Voltage_divider |
| Capacitive divider | Vout = C1/(C1+C2) * Vin | For AC signals only; blocks DC; used in oscilloscope probes for frequency compensation | https://en.wikipedia.org/wiki/Voltage_divider |

## Filter Circuits
| Filter Type | Circuit | Response | Source |
|------------|---------|----------|--------|
| Low-pass RC | Resistor in series, capacitor to ground | -3dB at f_c = 1/(2*PI*R*C); -20dB/decade rolloff above cutoff | https://en.wikipedia.org/wiki/Low-pass_filter |
| High-pass RC | Capacitor in series, resistor to ground | -3dB at f_c = 1/(2*PI*R*C); blocks DC, passes high frequencies | https://en.wikipedia.org/wiki/High-pass_filter |
| Sallen-Key (2nd order) | Op-amp + 2 resistors + 2 capacitors | -40dB/decade rolloff; non-inverting; commonly used in active audio crossovers | https://en.wikipedia.org/wiki/Sallen-Key_filter |

## Power Supply Stages
| Stage | Components | Function | Source |
|-------|-----------|----------|--------|
| Transformer (step-down) | Primary winding, secondary winding, iron core | Isolates from mains; reduces 120VAC to 12-24VAC typical for electronics | https://en.wikipedia.org/wiki/Power_supply |
| Bridge rectifier | 4x diodes in bridge configuration | Converts AC to pulsating DC; Vdc_peak = 1.414*Vrms - 2*Vf(diode) | https://en.wikipedia.org/wiki/Diode_bridge |
| Filter capacitor | Electrolytic, 1000-4700uF typical | Smooths rectified DC; ripple voltage inversely proportional to capacitance and load current | https://en.wikipedia.org/wiki/Ripple_(electrical) |
| Voltage regulator | LM7805 (5V fixed), LM317 (adjustable) | Regulated DC output; requires 2-3V headroom above output voltage; thermal protection built-in | https://www.ti.com/ (search LM7805) |
| Bypass capacitors | 0.1uF ceramic at regulator input and output pins, as close as physically possible | Prevents oscillation; shunts high-frequency noise to ground | Manufacturer application notes per specific regulator |

## Op-Amp Configurations (Texas Instruments Reference Designs)
| Configuration | Gain Formula | Key Characteristics | Source |
|-------------|-------------|-------------------|--------|
| Inverting amplifier | Av = -Rf/Rin | Input impedance = Rin; output inverted 180 degrees from input | https://www.ti.com/ (search: Op Amp Applications Handbook) |
| Non-inverting amplifier | Av = 1 + Rf/R1 | Very high input impedance; output in phase with input | https://www.ti.com/ (search: Op Amp Applications Handbook) |
| Voltage follower (buffer) | Av = 1 | Output connected directly to inverting input; maximum input impedance; no gain | https://www.ti.com/ (search: Op Amp Applications Handbook) |
| Differential amplifier | Vout = (Rf/R1)(V2-V1) | Amplifies difference between two inputs; common-mode rejection depends on resistor matching | https://www.ti.com/ (search: Op Amp Applications Handbook) |
| Comparator (open-loop) | N/A (digitizes) | Output saturates at supply rail when V+ > V-; add hysteresis resistors for Schmitt trigger action | https://www.ti.com/ (search: Op Amp Applications Handbook) |
