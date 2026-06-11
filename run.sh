CUDA_ID=2
for id in 00004 00007 00014 00015 00016 00021; do
    CUDA_VISIBLE_DEVICES=$CUDA_ID python scripts/rsl_rl/train.py \
        --task Isaac-AutoMate-Assembly-Direct-v0 \
        --assembly_id $id \
        --headless > outputs/train_$id.log 2>&1 &
    CUDA_ID=$((CUDA_ID + 1))
done