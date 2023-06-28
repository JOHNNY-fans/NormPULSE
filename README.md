# NormPULSE: A Generative Approach for Clinical Term Normalization
<!-- select Model and/or Data and/or Code as needed>

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

This repository provides the official implementation of HierNorm: A Generative Approach with Distilled Knowledge and Tree Structure for Clinical Term Normalization.

Key feature bulletin points here
- A knowledge transfer approach that utilizes data distillation from LLMs through prompt engineering, converting short clinical terms into knowledge cards that contain enhanced information and clinical knowledge.
- Leverage the hierarchical structure in the standard term and develop an algorithm for building the tree structure with ICD codes.
- HierNorm, a generative framework, to find the candidate terms via knowledge-enhanced retrieval and generate the final standard term with hierarchical reasoning. The proposed framework does not need to be trained on any specific dataset, showing strong generalizability, and could be deployed to various datasets without re-training.

## Links

- [Paper](https://)
- [Model](https://)
- [Code](https://) 
<!-- [Code] may link to your project at your institute>


<!-- give an introduction of your project -->
## Details

We outline the comprehensive framework of our solution, HierNorm, which comprises two primary stages: the offline stage and the online inference stage, as shown in the following Figure.  
During the offline stage, we adopt two main tasks: knowledge card generation, aiming at enhancing the knowledge inside term by distilling knowledge from LLM; hierarchical tree construction based on the ICD codes.  
The online inference stage involves two main steps: knowledge-enhanced retrieval and hierarchical reasoning, creating a complete normalization flow path. In the first step, the model retrieves candidates for the given mention using the generated knowledge cards and locates the path of each candidate in the constructed hierarchical tree to build a subtree. In the second step, the model reasons out the final result layer by layer through the subtree.

<!-- Insert a pipeline of your algorithm here if got one -->
<div align="center">
    <a href="https://"><img width="1000px" height="auto" src="https://github.com/JOHNNY-fans/HierNorm/blob/main/figure/architecture_zh.png"></a>
</div>

## Demo
Here is our simple demo.
<div align="center">
    <a href="https://"><img width="1000px" height="auto" src="https://github.com/JOHNNY-fans/HierNorm/blob/main/figure/norm_demo_v2.png"></a>
</div>


## Dataset Links
### Open source
- [Yidu-N7k](http://openkg.cn/dataset/yidu-n7k)
- [CHIP-CDN](https://tianchi.aliyun.com/dataset/95414)

## Get Started
To be continued~
<!--
**Main Requirements**  
> connected-components-3d  
> h5py==3.6.0  
> monai==0.9.0  
> torch==1.11.0  
> tqdm  
> fastremap  

**Installation**
```bash
pip install DDD
```

**Download Model**


**Preprocess**
```bash
python DDD
```


**Training**
```bash
python DDD
```


**Validation**
```bash
python DDD
```


**Testing**
```bash
python DDD
```

## 🙋‍♀️ Feedback and Contact

- Email
- Webpage 
- Social media
-->

## 🛡️ License

This project is under the CC-BY-NC 4.0 license. See [LICENSE](https://github.com/JOHNNY-fans/HierNorm/blob/main/LICENSE) for details.

## 🙏 Acknowledgement

- Shanghai AI Laboratory.
- East China University of Science and Technology. 

## 📝 Citation

If you find this repository useful, please consider citing this paper:
```
@article{John2023,
  title={paper},
  author={John},
  journal={arXiv preprint arXiv:},
  year={2023}
}
```
