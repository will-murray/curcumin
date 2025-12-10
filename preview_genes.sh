if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <arg>"
    exit 1
fi

python3 get_significant_genes.py diff/5s_vs_4s.gene_exp.diff $1 | awk 'NR > 2 {print $2}  '
