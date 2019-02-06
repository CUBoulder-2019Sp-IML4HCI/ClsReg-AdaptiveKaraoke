# ClsReg-AdaptiveKaraoke
A singing game that changes the scoring parameters based on the range of the singer.

**Team Members:** Ian Wilkins, Calvin Ritger, Shawn Polson

# Adaptive Karaoke

## Goals:
To design and implement a singing game that changes the scoring parameters based on the range of the singer. Regression will be used to map the frequency pattern of the singer to the frequency pattern of the song. This continuous model will be used both for input display (i.e. a status sprite to show how accurate a singer’s pitch is), and for scoring. Classification will be used to identify the singer and select the singer’s voice model for scoring. Since singers are discrete, a classifier is an appropriate tool for discerning between singers and selecting the appropriate model.

## Motivation:
By creating a continuous model that can map a singer’s voice to the desired pattern, the game can be adapted to the specific details of the singer. Sickness, morphological differences, age differences, emotive differences can all contribute to differences from the mean human voice and the expected voice pattern of the song. An adaptive continuous model of each player’s voice can be used to map a unique individual’s voice pattern to the expected pattern. Player’s will no longer be scored on how well they meet an absolute standard, they will instead be scored based on their control within their own range.

## Input Data:
There are 2 categories of input data: vocal data to create voice mapping model, and image data (AffdexMe facial recognition) to use for singer identification.

### Vocal Data:
We have considered 2 main options for recording voices.
Utilize a mobile phone and the corresponding beam forming features in a mobile phone’s mic to isolate the singer’s voice from surrounding noise.
Utilize a cardioid mic with a low range to record the singer’s voice and block background noise.

### Digitize Vocal Data: 
(Using Maximillian)

## Classification + Regression:
 - Classification: Facial detection to identify different singers
 - Regression: Frequency mapping

## Feature Engineering:
 - Audio processing with the Maximillian program (e.g., FFTs, Constant Q Transforms)

## Storyboard:
Coming soon?

## How to Use Our Project:
TBD

## Demo Video:
TBD
      
