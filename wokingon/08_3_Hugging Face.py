# * 다양한 모델을 공유하는 많은 사이트가 있습니다. 
#   Pytorch에서 제공되는 pretrained model은 제한적이므로 필요한 내용에 따라 다른 사이트를 활용할 수 있습니다.

#   - Pytorch Hub: https://pytorch.org/hub/
#   - Hugging Face: https://huggingface.co/
#   - OpenMMLab: https://github.com/open-mmlab


# 시계열 예측 모델을 만들기 위해서 구글의 최신 Foundation 모델인 TimesFM 모델을 허깅페이스에서 사용해봅시다.

# Paper: https://arxiv.org/pdf/2310.10688
# Blog: https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/
# github: https://github.com/google-research/timesfm 
# 모델(checkpoint): https://huggingface.co/google/timesfm-1.0-200m

# Install in Terminal

# git clone https://github.com/google-research/timesfm.git
# conda env create --file=environment_cpu.yml  
   # gpu 버전은 conda env create --file=environment.yml   
   

