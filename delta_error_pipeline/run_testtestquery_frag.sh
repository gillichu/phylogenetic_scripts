#!/bin/bash

refdir="/home/gchu4/scratch/warnow/aln_pp/frag_seq"
procdir="/home/gchu4/scratch/warnow/aln_pp/est_backbones/backbone_alignment"
gup="/home/gchu4/scratch/warnow/trial_aln_pp/sepp/tools/bundled/Linux/guppy-64"
treecomp="pplacerDC/common/treecompare.py"
nw_prune="/home/gchu4/scratch/warnow/trial_aln_pp/newick_utils/src/nw_prune"

mkdir  -p ${procdir}
declare -a dataset_arr=("1000S5" "1000M5" "1000L1" "1000L5") 
declare -a method_arr=("mda" "mla" "mlpaf" "mmpaf" "upp")
declare -a frag_arr=("low_frag" "high_frag") 
declare -a rep_arr=("R0" "R1" "R2" "R3" "R4" "R5" "R6" "R7" "R8" "R9" "R10" "R11" "R12" "R13" "R14" "R15" "R16" "R17" "R18" "R19")
mkdir -p "result_stats_estbb"

for dataset in "${dataset_arr[@]}"
do
for frag in "${frag_arr[@]}"
do
for rep in "${rep_arr[@]}"
do 
        mkdir -p "result_stats_estbb/results_${dataset}_${frag}"
        result_file="result_stats_estbb/results_${dataset}_${frag}/${rep}"

        if [ -f "$FILE" ]; then
            echo "${result_file} exists already."
        else 
            echo "Dataset, Rep, Method, sum delta error, num queries" > "${result_file}" 
            for method in "${method_arr[@]}" 
            do 
                dirname="${procdir}/${frag}/${dataset}/${rep}"
                refdirname="${refdir}/${dataset}/${rep}"
       
                if [ ${frag} == "high_frag" ]; then 
                    flvl="HF"
                else
                    flvl="LF"
                fi
                bb_tree="${refdirname}/magus_backbone_align.tre" # already created FastTree tree
                bb_aln="${dirname}/magus_backbone_align.txt" # already created
                bb_info="${dirname}/RAxML_info.magus_backbone_${frag}_truebb_infotxt"  # already created

                jplace="${dirname}/magus_backbone_align_${method}aln_pplacer.json" # already created
                outputtree="${dirname}/magus_backbone_align_${method}aln_pplacer.tre" # will create
        
                if [ -f "$outputtree" ]; then
                  echo "$outputtree exists already."
                else
                  echo "$outputtree missing"
                  echo "Step 1: Extract estimated placement tree | ${gup} tog -o ${outputtree} ${jplace}"
                  ${gup} tog -o ${outputtree} ${jplace}
                fi

                true_topo="1000s/sate_journal/${dataset}/${rep}/rose.mt"

                backbonetree="${dirname}/magus_backbone.truetre" # already created from run_induce5.sh
                query_seq="${dirname}/${flvl}_frag.fasta" 
                backbone_true="${dirname}/${method}_bbext.truetre"  # will created
                query_seq_label="${dirname}/fraglabel_${method}_${rep}.txt" # is created

                if true; then
                  echo "Step 2: Create true backbone | ${nw_prune} ${true_topo} ${query_seq} &> ${backbone_true}"
                  ${nw_prune} ${true_topo} ${query_seq_label} > ${backbone_true}

                  echo "Step 3: Calculate DE | python3 ${treecomp} ${true_topo} ${outputtree} ${backbonetree} ${backbone_true}"
                  echo "Step 3: Calculate DE | $(python3 ${treecomp} ${true_topo} ${outputtree} ${backbonetree} ${backbone_true}))"
                  de=$(python3 ${treecomp} ${true_topo} ${outputtree} ${backbonetree} ${backbone_true})

                  echo "Step 4: Num Queries | numq=$(grep -c ">" ${query_seq})"
                  numq=$(grep -c ">" ${query_seq})
                  echo "${dirname}, ${rep}, ${method}, ${de}, ${numq} " >> ${result_file}
                fi 
            done 
        fi 
done 
done
done
