## Team 1
We tried to adapt our problem of implicit/explicit  flow detection with the help of  [this](https://bdqnghi.github.io/files/AAAI_18_cross_language_learning.pdf) paper.
In the underlying folder structure there are two run scripts.
```
ast2vec_network/run.sh
tbcnn_network/run.sh
```
To reproduce our results execute these scripts in the order above. 
You can change the amount of generated programs in the file ```generate_programs.py```
and the network hyperparameter for both networks in there corresponding ```parameters.py```