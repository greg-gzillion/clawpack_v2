# Circuit and Wiring Diagram Standards

## Circuit Symbols (IEEE 315 / ANSI Y32.2)
| Symbol | Description | URL |
|--------|-------------|-----|
| Resistor | Zigzag line (US) or rectangle (IEC) | https://en.wikipedia.org/wiki/Electronic_symbol |
| Capacitor | Two parallel lines (non-polarized), curved+straight (polarized) | https://en.wikipedia.org/wiki/Electronic_symbol |
| Inductor | Looped coil symbol | https://en.wikipedia.org/wiki/Electronic_symbol |
| Diode | Triangle pointing to line | https://en.wikipedia.org/wiki/Electronic_symbol |
| LED | Diode with arrows showing light emission | https://en.wikipedia.org/wiki/Electronic_symbol |
| Transistor (NPN) | Circle with emitter arrow pointing out | https://en.wikipedia.org/wiki/Electronic_symbol |
| Transistor (PNP) | Circle with emitter arrow pointing in | https://en.wikipedia.org/wiki/Electronic_symbol |
| Ground | Three decreasing horizontal lines | https://en.wikipedia.org/wiki/Electronic_symbol |
| Battery | Long line (+) and short line (-) pairs | https://en.wikipedia.org/wiki/Electronic_symbol |
| Switch (SPST) | Break in line with angled contact | https://en.wikipedia.org/wiki/Electronic_symbol |
| Fuse | Rectangle with line through it | https://en.wikipedia.org/wiki/Electronic_symbol |
| Transformer | Two inductors with lines between | https://en.wikipedia.org/wiki/Electronic_symbol |
| Relay | Coil symbol with switch contacts | https://en.wikipedia.org/wiki/Electronic_symbol |

## Common Circuit Designs
| Circuit | Components | URL |
|---------|-----------|-----|
| Voltage divider | Two resistors in series | https://en.wikipedia.org/wiki/Voltage_divider |
| RC filter | Resistor + capacitor | https://en.wikipedia.org/wiki/RC_circuit |
| Bridge rectifier | Four diodes in bridge configuration | https://en.wikipedia.org/wiki/Diode_bridge |
| Voltage regulator | LM7805 + capacitors | https://en.wikipedia.org/wiki/Voltage_regulator |
| Astable multivibrator | Two transistors + RC network | https://en.wikipedia.org/wiki/Multivibrator |
| H-bridge | Four switches for motor control | https://en.wikipedia.org/wiki/H-bridge |
| Current limiter | Transistor + sense resistor | https://en.wikipedia.org/wiki/Current_limiting |
| Pull-up resistor | Resistor to VCC for logic high default | https://en.wikipedia.org/wiki/Pull-up_resistor |
| Debounce circuit | RC network + Schmitt trigger | https://en.wikipedia.org/wiki/Switch#Contact_bounce |

## PCB Design Standards (IPC)
| Standard | Description | URL |
|----------|-------------|-----|
| IPC-2221 | Generic standard for printed board design | https://www.ipc.org/ipc-2221 |
| Trace width | Based on current: 10mil per 1A typical | https://www.ipc.org/ipc-2221 |
| Via size | 0.3mm drill, 0.6mm pad typical | https://www.ipc.org/ipc-2221 |
| Clearance | 0.15mm minimum between traces | https://www.ipc.org/ipc-2221 |
| Copper weight | 1 oz/ft^2 standard, 2 oz for power | https://www.ipc.org/ipc-2221 |
| Solder mask | Green LPI standard, 0.05mm clearance | https://www.ipc.org/ipc-2221 |
| Silkscreen | White epoxy ink, 0.15mm minimum line | https://www.ipc.org/ipc-2221 |
| Board thickness | 1.6mm standard (FR-4) | https://www.ipc.org/ipc-2221 |
