N = [80, 160, 320]
DK = [3, 4, 5]
I = [100]

rule master:
    input:
        expand('simulations/new/n{n}_d{dk}_k{dk}_i{i}.csv',
            n = N,
            dk = DK,
            i = I)

rule run_estimate:
    output:
        'simulations/new/n{n}_d{dk}_k{dk}_i{i}.csv'
    shell:
        '''
            ./run_estimates.sh -n {wildcards.n} -d {wildcards.dk} -k {wildcards.dk} -i {wildcards.i} > simulations/new/n{wildcards.n}_d{wildcards.dk}_k{wildcards.dk}_i{wildcards.i}.csv
        '''