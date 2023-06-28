# NormPULSE: A Generative Approach for Clinical Term Normalization

<!--
**Here are some ideas to get you started:**
🙋‍♀️ A short introduction - what is your organization all about?
🌈 Contribution guidelines - how can the community get involved?
👩‍💻 Useful resources - where can the community find your docs? Is there anything else the community should know?
🍿 Fun facts - what does your team eat for breakfast?
🧙 Remember, you can do mighty things with the power of [Markdown](https://docs.github.com/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
-->

This repository is a sub-repository of [PULSE](https://github.com/openmedlab/PULSE).
<!-- Insert the project banner here -->
<div align="center">
    <a href="https://"><img width="1000px" height="auto" src="https://github.com/JOHNNY-fans/HierNorm/blob/main/figure/pulse.png"></a>
</div>

---

## Key Features

This repository provides the official implementation of NormPULSE.

Key feature bulletin points here
- A knowledge transfer approach that utilizes data distillation from LLMs through prompt engineering, converting short clinical terms into knowledge cards that contain enhanced information and clinical knowledge.
- Leverage the hierarchical structure in the standard term and develop an algorithm for building the tree structure with ICD codes.
- A generative framework, to find the candidate terms via knowledge-enhanced retrieval and generate the final standard term with hierarchical reasoning.

<!-- give an introduction of your project -->
## Details

We outline the comprehensive framework of our solution to clinical term normalization, NormPULSE, which is based on PULSE and comprises three steps: 
1. Training, There are three tasks in the training step, knowledge card generation, aiming at enhancing the knowledge inside term by distilling knowledge from LLM; hierarchical tree construction based on the ICD codes and term normalization, making the model get the ability to select the standard terms from a certain candidate list.  
2. knowledge-enhanced retrieval, the model retrieves candidates for the given mention using the generated knowledge cards and locates each candidate's path in the constructed hierarchical tree to build a subtree.
3. hierarchical reasoning, the model reasons out the final result layer by layer through the subtree.

<!-- Insert a pipeline of your algorithm here if got one -->
<div align="center">
    <a href="https://"><img width="1000px" height="auto" src="https://github.com/JOHNNY-fans/HierNorm/blob/main/figure/architecture_zh.png"></a>
</div>

## Dataset
[data4normpulse](https://huggingface.co/datasets/Johnnyfans/data4normpulse)

## Demo
Here is our simple demo.
<div align="center">
    <a href="https://"><img width="1000px" height="auto" src="https://github.com/JOHNNY-fans/HierNorm/blob/main/figure/norm_demo_v2.png"></a>
</div>

## Get Started
**Main Requirements**  
> transformers>=4.27.4
> faiss-gpu==1.7.2
> torch==1.12.1
> fastapi
> uvicorn

**Installation**
```bash
pip install requirements.txt
```

**Download Model**
You can find the pre-trained model weights and the NormPULSE weights in the following huggingface repositories.
- [PULSE](https://huggingface.co/OpenMEDLab/PULSE-7bv5)
- [NormPULSE] 

## To be continued~

**Preprocess**
```bash
python DDD
```


**Training**
```bash
python DDD
```

**Usage**
```bash
python DDD
```

## 🛡️ License

The code of this project is licensed under [Apache 2.0](https://github.com/JOHNNY-fans/NormPULSE/blob/main/LICENSE), and the model weights are licensed under [GNU AGPL 3.0](https://github.com/JOHNNY-fans/NormPULSE/blob/main/MODEL_LICENSE). If the models contained in this project, or any modified versions thereof, are used in a service which results in misleading or harmful statements causing adverse effects, the responsibility lies with the service provider and is not associated with or attributable to this project.

## 🙏 Acknowledgement

- Shanghai AI Laboratory.
- East China University of Science and Technology.

<!--
## 📝 Citation

If you find this repository useful, please consider citing this paper:
```
@article{John2023,
  title={paper},
  author={John},
  journal={arXiv preprint arXiv:},
  year={2023}
}
-->
```
