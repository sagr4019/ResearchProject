#!/bin/bash
cd ..
ROOT_DIR=${PWD}
echo "Working directory is: $ROOT_DIR"

mkdir -p $ROOT_DIR/bi-tbcnn_tf_files
python3 $ROOT_DIR/tbcnn_network/bi-tbcnn/train_tbcnn.py $ROOT_DIR/bi-tbcnn_tf_files $ROOT_DIR/vec/trees.pkl $ROOT_DIR/vec/pretrained_vectors.pkl True True






