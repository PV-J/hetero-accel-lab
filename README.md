# hetero-accel-lab

`hetero-accel-lab` is a Python toy lab for experimenting with a **system of accelerators**.

All core components live under the `accel_system/` package:

- `matrix_accel.py` – Matrix accelerator (AI/ML-style compute)
- `dsp_accel.py` – DSP accelerator (signal processing)
- `rf_radio.py` – RF module (link with front-end constraints and latency)
- `pqc_security.py` – PQC security accelerator (post-quantum, toy model)
- `scheduler.py` – Identifies the current bottleneck stage
- `system_model.py` – Ties accelerators and scheduler together

Supporting folders:

- `examples/` – End-to-end pipelines using matrix + DSP + RF + security
  - `example_inference_with_pqc.py` – Single run with CLI knobs
  - `compare_bottlenecks.py` – Compute-heavy vs communication-heavy comparison
  - `scheduler_demo.py` – Shows `EnhancedScheduler` recommendations for three bottleneck scenarios
- `tests/` – Basic end-to-end checks

The goal is to explore how changes in workload size and link bandwidth shift the system bottleneck between compute, communication, and security, without writing RTL or using vendor tools.

## Quickstart

Clone the repo and run a simple example:

git clone https://github.com/PV-J/hetero-accel-lab.git
cd hetero-accel-lab

Single pipeline run with default configuration
python examples/example_inference_with_pqc.py

Compare compute-heavy vs communication-heavy bottlenecks
python examples/compare_bottlenecks.py

## What this shows

- Simple matrix–vector computation offloaded to a `MatrixAccelerator`.
- A `DSPAccelerator` that applies a toy filter to the matrix output.
- An `RFModule` that models propagation delay and bandwidth-limited serialization.
- A toy post-quantum `PQCSecurityAccelerator` that “protects” the result.
- A system model that reports per-stage latency and highlights the bottleneck stage for each run.

These pieces together behave like a tiny heterogeneous accelerator system that you can probe from the command line.

## Documentation

- [Latency and configuration](docs/latency_and_configuration.md)
- [Bottlenecks and scheduler](docs/bottlenecks_and_scheduler.md)
- [Bottleneck scenarios](docs/bottleneck_scenarios.md)

## Roadmap

- [x] Basic matrix + DSP + PQC pipeline with toy latency model  
- [x] CLI knobs for matrix size and DSP window  
- [x] Add RF/wireless-style module (latency + bandwidth constraints)  
- [x] Add simple scheduler that chooses which accelerator is the bottleneck  
- [ ] Add plots for latency breakdown vs configuration  
- [x] Draft first blog post linking to this repo
