import sys
import pandas as pd

# Run with:
# python3 report.py simulations/new/*.csv > report_sim.md

if __name__ == '__main__':
    files = sys.argv[1:]
    for f in files:
        df = pd.read_csv(f)
        n = len(eval(df.iloc[0,0]))
        d = df.iloc[0,2]
        k = df.iloc[0,3]
        tot = df.shape[0]

        approx_mean = df["approximation"].mean()
        approx_std = df["approximation"].std()
        approx_median = df["approximation"].median()
        approx_time = df["approximation_time"].mean()

        fpt_mean = df["fpt"].mean()
        fpt_std = df["fpt"].std()
        fpt_median = df["fpt"].median()
        fpt_time = df["fpt_time"].mean()

        print(f'# N={n}, d={d}, k={k}, simulations={tot}')
        print('| | mean | std | median | avg time (s) |')
        print('|--|--|--|--|--|')
        print(f'| approximation | {approx_mean:.4f} | {approx_std:.4f} | {approx_median:.4f} | {approx_time:.4E} |')
        print(f'| FPT | {fpt_mean:.4f} | {fpt_std:.4f} | {fpt_median:.4f} | {fpt_time:.4E} |')
        print()

