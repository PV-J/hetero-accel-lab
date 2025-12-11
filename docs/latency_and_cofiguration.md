# Latency and Configuration in hetero-accel-lab

This note explains how the simple configuration knobs in `hetero-accel-lab` affect the toy latency model of the accelerator pipeline.

## Pipeline overview

The current Python pipeline is:

1. MatrixAccelerator: dense matrix–vector multiply.
2. DSPAccelerator: moving-average filter on the matrix output.
3. PQCSecurityAccelerator: toy post-quantum "encapsulation" and "decapsulation".

Each stage reports its own latency, and the system model reports the total.

## Configuration knobs

The main knobs exposed in `examples/example_inference_with_pqc.py` are:

- `--matrix-size` (default: 3)  
  Controls the square matrix size \(N\) used in the matrix–vector multiply (N x N). Larger N increases the number of multiply-accumulate operations and therefore matrix latency.

- `--dsp-window` (default: 3)  
  Controls the window size for the moving-average filter in `DSPAccelerator`. Larger windows increase the amount of work per output sample and therefore DSP latency.

- `--seed` (default: 0)  
  Controls deterministic random generation of the input matrix and vector. This does not change latency, but makes runs repeatable.

These knobs represent, in a very simplified way, how algorithm complexity and filter parameters can change the workload presented to each accelerator.

## Latency model

The latency numbers are **toy models** intended for architectural exploration, not real performance measurements:

- MatrixAccelerator:
  - Latency = `base_latency + k_matrix * (N * N)`
- DSPAccelerator:
  - Latency = `base_latency + k_dsp * (num_samples * window)`
- PQCSecurityAccelerator:
  - Latency is fixed per operation (keygen, encapsulate, decapsulate).

As you increase `--matrix-size`, matrix latency grows roughly with \(N^2\), while DSP latency grows with the number of samples. As you increase `--dsp-window`, DSP latency grows roughly linearly with the window size for a fixed number of samples.

PQCSecurityAccelerator latency stays constant in this version, modelling a fixed-cost security offload independent of data size.

## How to interpret runs

Example commands:

Small matrix and narrow DSP window
python examples/example_inference_with_pqc.py --matrix-size 4 --dsp-window 3

C:\Users\admin\Desktop\hetero-accel-lab>python examples/example_inference_with_pqc.py --matrix-size 3 --dsp-window 3
=== hetero-accel-lab: matrix + DSP + PQC example ===
Matrix size: 3x3
DSP window: 3
Matrix output: [0.5344833699895771, -0.06378485584971479, -0.22686636957812087]
DSP output: [0.5344833699895771, 0.23534925706993118, 0.08127738152058049]
Shared secret match: True
Latency breakdown (time units):
            matrix: 1.0090
               dsp: 0.5045
        pqc_keygen: 2.0000
   pqc_encapsulate: 1.5000
   pqc_decapsulate: 1.5000
             total: 6.5135

Larger matrix, same DSP window
python examples/example_inference_with_pqc.py --matrix-size 16 --dsp-window 3

C:\Users\admin\Desktop\hetero-accel-lab>python examples/example_inference_with_pqc.py --matrix-size 16 --dsp-window 3
=== hetero-accel-lab: matrix + DSP + PQC example ===
Matrix size: 16x16
DSP window: 3
Matrix output: [0.04181013512964185, 0.8557761320826778, 0.22947714712812395, -0.27635618768590203, 1.075129911358199, -0.2732297570907255, -0.5212108980759071, -0.317840774151403, -0.7762670351691283, 1.0469738872661756, -1.602087475597602, 1.6987111596257276, 1.0890257665250105, -0.02705329704753312, -0.707963427821008, 1.1364822653939737]
DSP output: [0.04181013512964185, 0.4487931336061598, 0.3756878047801479, 0.2696323638416332, 0.3427502902668069, 0.1751813221938571, 0.09356308539718876, -0.37076047643934523, -0.5384395691321462, -0.015711307351451913, -0.4437935411668516, 0.38119919043143374, 0.39521648351771205, 0.920227876367735, 0.1180030138854898, 0.13382184684181087]
Shared secret match: True
Latency breakdown (time units):
            matrix: 1.2560
               dsp: 0.5240
        pqc_keygen: 2.0000
   pqc_encapsulate: 1.5000
   pqc_decapsulate: 1.5000
             total: 6.7800

Larger matrix and wider DSP window
python examples/example_inference_with_pqc.py --matrix-size 16 --dsp-window 8

C:\Users\admin\Desktop\hetero-accel-lab>python examples/example_inference_with_pqc.py --matrix-size 16 --dsp-window 8
=== hetero-accel-lab: matrix + DSP + PQC example ===
Matrix size: 16x16
DSP window: 8
Matrix output: [0.04181013512964185, 0.8557761320826778, 0.22947714712812395, -0.27635618768590203, 1.075129911358199, -0.2732297570907255, -0.5212108980759071, -0.317840774151403, -0.7762670351691283, 1.0469738872661756, -1.602087475597602, 1.6987111596257276, 1.0890257665250105, -0.02705329704753312, -0.707963427821008, 1.1364822653939737]
DSP output: [0.04181013512964185, 0.4487931336061598, 0.3756878047801479, 0.2126768066636354, 0.3851674276025481, 0.2754345634870025, 0.1616280689780154, 0.1016944635868381, -0.0005651827005081697, 0.023334536697429055, -0.20561104114328668, 0.041272377270667016, 0.04300935916651846, 0.07378141667191751, 0.05043735045377991, 0.232227730396952]
Shared secret match: True
Latency breakdown (time units):
            matrix: 1.2560
               dsp: 0.5640
        pqc_keygen: 2.0000
   pqc_encapsulate: 1.5000
   pqc_decapsulate: 1.5000
             total: 6.8200


Look at the printed latency breakdown:

- When `--matrix-size` increases, matrix latency should dominate total latency.
- When `--dsp-window` increases (for fixed size), DSP latency becomes a larger fraction of total latency.
- PQC latencies remain constant and are more visible when compute and DSP workloads are small.

This behaviour is useful for systemization discussions: it shows how changing one subsystem (e.g., AI or DSP load) shifts the bottleneck between accelerators, even in a simple toy model.

## Link to future architecture writing

In future architecture or blog documents, you can:

- Use `--matrix-size` and `--dsp-window` as stand-ins for "AI model size" and "signal processing complexity".
- Show how a scheduler or resource planner might allocate budget between matrix, DSP, and PQC accelerators as these knobs change.
- Replace the toy latency formulas with more realistic models without changing the public configuration interface.



