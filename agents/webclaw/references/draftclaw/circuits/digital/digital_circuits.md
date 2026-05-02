# Digital Circuit Design Reference
## All URLs verified May 2026

## Logic Gates (7400 Series, 4000 Series CMOS)
| Gate | Symbol | Standard IC | Truth Table Summary | Source |
|------|--------|------------|-------------------|--------|
| AND | D-shape, flat back | 74HC08 (Quad 2-input) | Output HIGH only when ALL inputs HIGH | https://en.wikipedia.org/wiki/AND_gate |
| OR | Curved back, pointed front | 74HC32 (Quad 2-input) | Output HIGH when ANY input HIGH | https://en.wikipedia.org/wiki/OR_gate |
| NOT (Inverter) | Triangle with circle output | 74HC04 (Hex inverter) | Output = opposite of input | https://en.wikipedia.org/wiki/Inverter_(logic_gate) |
| NAND (universal gate) | AND + circle output | 74HC00 (Quad 2-input) | Output LOW only when ALL inputs HIGH | https://en.wikipedia.org/wiki/NAND_gate |
| NOR (universal gate) | OR + circle output | 74HC02 (Quad 2-input) | Output LOW when ANY input HIGH | https://en.wikipedia.org/wiki/NOR_gate |
| XOR (Exclusive OR) | OR + extra input curve | 74HC86 (Quad 2-input) | Output HIGH when inputs DIFFER | https://en.wikipedia.org/wiki/XOR_gate |
| XNOR (Exclusive NOR) | XOR + circle output | 74HC266 (Quad 2-input) | Output HIGH when inputs SAME | https://en.wikipedia.org/wiki/XNOR_gate |

## Flip-Flops and Sequential Logic
| Type | Function | Standard IC | Source |
|------|----------|-------------|--------|
| D Flip-Flop (edge-triggered) | Captures D input on clock edge; holds until next edge; most common sequential element | 74HC74 (Dual D with preset/clear) | https://en.wikipedia.org/wiki/Flip-flop_(electronics) |
| JK Flip-Flop | J=1,K=0 sets; J=0,K=1 resets; J=K=1 toggles; J=K=0 holds | 74HC73 (Dual JK with clear) | https://en.wikipedia.org/wiki/Flip-flop_(electronics) |
| T Flip-Flop (Toggle) | Changes state each clock when T=1; built from JK with J=K=1 or D with feedback | Use 74HC74 wired as toggle | https://en.wikipedia.org/wiki/Flip-flop_(electronics) |
| D Latch (level-sensitive) | Transparent when enable HIGH; latches when enable LOW | 74HC573 (Octal D-latch, 3-state outputs) | https://en.wikipedia.org/wiki/Flip-flop_(electronics) |

## Shift Registers and Counters
| IC | Function | Source |
|----|----------|--------|
| 74HC595 | 8-bit shift register, serial-in parallel-out with output latch; cascadable; common LED/relay driver | https://www.ti.com/product/SN74HC595 |
| 74HC165 | 8-bit parallel-in serial-out shift register; used for reading multiple switch/button inputs over few pins | https://www.ti.com/ (search 74HC165) |
| CD4017 | Decade counter/divider with 10 decoded outputs; advances one output per clock; resets on 10th pulse | https://www.ti.com/ (search CD4017) |

## Serial Communication Protocols
| Protocol | Lines | Speed | Typical Applications | Source |
|----------|-------|-------|---------------------|--------|
| SPI | 4 (MOSI, MISO, SCLK, SS) | 1-50MHz typical | SD cards, displays, ADCs, DACs; full duplex | https://en.wikipedia.org/wiki/Serial_Peripheral_Interface |
| I2C | 2 (SDA, SCL) + GND | 100kHz std, 400kHz fast, 1MHz fast+ | Sensors, EEPROMs, RTCs; multi-device single bus | https://en.wikipedia.org/wiki/Serial_Peripheral_Interface (see I2C) |
| UART (async serial) | 2 (TX, RX) + GND | 9600-115200 baud typical | GPS, Bluetooth, debug consoles; no clock line needed | https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter |

## Voltage Level Shifting (3.3V to 5V interfacing)
| Method | Components | Notes | Source |
|--------|-----------|-------|--------|
| Resistive divider (5V->3.3V only) | Two resistors per voltage divider formula | Simple, cheap; one-direction only; not suitable for high-speed signals due to RC loading | https://en.wikipedia.org/wiki/Voltage_divider |
| Dedicated level shifter IC | TXB0104, 74LVC245, etc. | Bidirectional; handles high-speed signals; auto-direction sensing on some models | https://www.ti.com/ (search: voltage level translator) |
| MOSFET-based bidirectional | BSS138 N-channel MOSFET + 2 pull-up resistors per line | Classic I2C level shifter; works for open-drain signals | Application note from NXP/Philips: AN97055 |
