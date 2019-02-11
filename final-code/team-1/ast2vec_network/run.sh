#!/bin/bash
cd ..
ROOT_DIR=${PWD}
echo "Working directory is: $ROOT_DIR"
mkdir -p $ROOT_DIR/vec
echo "generating programs"
python3 generate_programs.py
echo "merge programs"
python3 $ROOT_DIR/ast2ast_converter.py pickle merged.pkl
echo "convert to nodes"
python3 $ROOT_DIR/fast_to_nodes.py $ROOT_DIR/vec/merged.pkl $ROOT_DIR/vec/nodes.pkl
echo "convert to trees"
python3 $ROOT_DIR/fast_to_training_trees.py $ROOT_DIR/vec/merged.pkl $ROOT_DIR/vec/trees.pkl
echo "train pretrained vectors"
python3 $ROOT_DIR/ast2vec_network/ast2vec/train.py $ROOT_DIR/vec/nodes.pkl $ROOT_DIR/vec/merged.pkl_map $ROOT_DIR/vec/pretrained_vectors.pkl
