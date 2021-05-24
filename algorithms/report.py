import sys
import pandas as pd

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

        fpt_mean = df["ftp"].mean()
        fpt_std = df["ftp"].std()
        fpt_median = df["ftp"].median()

        print(f'# N={n}, d={d}, k={k}, simulations={tot}')
        print('| | mean | std | median |')
        print('|--|--|--|--|')
        print(f'| approximation | {approx_mean} | {approx_std} | {approx_median} |')
        print(f'| FPT | {fpt_mean} | {fpt_std} | {fpt_median} |')
        print()
