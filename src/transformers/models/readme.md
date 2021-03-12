
## 3.3 Encoder Pre-net

In Tacotron2, a 3-layer CNN is applied to the input text em- beddings, which can model the longer-term context in the in- put character sequence. In our Transformer TTS model, we input the phoneme sequence into the same network, which is called ”encoder pre-net”. Each phoneme has a trainable embedding of 512 dims, and the output of each convolution layer has 512 channels, followed by a batch normalization and ReLU activation, and a dropout layer as well. In addi- tion, we add a linear projection after the final ReLU acti- vation, since the output range of ReLU is [0, +∞), while each dimension of these triangle positional embeddings is in [−1, 1]. Adding 0-centered positional information onto non- negative embeddings will result in a fluctuation not centered on the origin and harm model performance, which will be demonstrated in our experiment. Hence we add a linear pro- jection for center consistency.


## 3.4 Decoder Pre-net

The mel spectrogram is first consumed by a neural network composed of two fully connected layers(each has 256 hid- den units) with ReLU activation, named ”decoder pre-net”, and it plays an important role in the TTS system. Phonemes has trainable embeddings thus their subspace is adaptive,
training data is not sufficient enough, and some exceptions have too few occurrences for neural networks to learn. So we make a rule system and implement it as a text-to-phoneme converter, which can cover the vast majority of cases.


## 3.5 Encoder
In Tacotron2, the encoder is a bi-directional RNN. We re- place it with Transformer encoder which is described in Sec. 2.3 . Comparing to original bi-directional RNN, multi-head attention splits one attention into several subspaces so that it can model the frame relationship in multiple different as- pects, and it directly builds the long-time dependency be- tween any two frames thus each of them considers global context of the whole sequence. This is crucial for synthe- sized audio prosody especially when the sentence is long, as generated samples sound more smooth and natural in our experiments. In addition, employing multi-head atten- tion instead of original bi-directional RNN can enable par- allel computing to improve training speed.

## 3.6 Decoder
In Tacotron2, the decoder is a 2-layer RNN with location- sensitive attention (Chorowski et al. 2015). We replace it with Transformer decoder which is described in Sec. 2.3. Employing Transformer decoder makes two main differ- ences, adding self-attention, which can bring similar advan- tages described in Sec. 3.5, and using multi-head attention instead of the location-sensitive attention. The multi-head attention can integrate the encoder hidden states in multiple perspectives and generate better context vectors. Taking attention matrix of previous decoder time steps into consid- eration, location-sensitive attention used in Tacotron2 can encourage the model to generate consistent attention results. We try to modify the dot product based multi-head attention to be location sensitive, but that doubles the training time and easily run out of memory.

## 3.7 Mel Linear, Stop Linear and Post-net
Same as Tacotron2, we use two different linear projections to predict the mel spectrogram and the stop token respec- tively, and use a 5-layer CNN to produce a residual to refine the reconstruction of mel spectrogram. It’s worth mention- ing that, for the stop linear, there is only one positive sample in the end of each sequence which means ”stop”, while hun- dreds of negative samples for other frames. This imbalance may result in unstoppable inference. We impose a positive weight (5.0 ∼ 8.0) on the tail positive stop token when cal- culating binary cross entropy loss, and this problem was ef- ficiently solved.
