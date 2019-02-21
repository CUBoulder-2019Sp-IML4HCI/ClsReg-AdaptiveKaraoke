# ClsReg-AdaptiveKaraoke
**Original concept:** A singing game that changes the scoring parameters based on the range of the singer.

**Final concept:** A sort of vocal-controlled Temple Run–like game where a singer must 1) control their pitch to stay within a track and 2) move out of the webcam's view to "dodge" obstacles.

**Team Members:** Ian Wilkins, Calvin Ritger, Shawn Polson

# Adaptive Karaoke
![Screenshot](https://github.com/CUBoulder-2019Sp-IML4HCI/ClsReg-AdaptiveKaraoke/blob/master/Game%20demo%20screenshot.png)

## Goals:
Our project had an original goal that was completely modified mid-project. Both are explained below.
### Original Goal
To design and implement a singing game that changes the scoring parameters based on the range of the singer. Regression will be used to map the frequency pattern of the singer to the frequency pattern of the song. This continuous model will be used both for input display (i.e. a status sprite to show how accurate a singer’s pitch is), and for scoring. Classification will be used to identify the singer and select the singer’s voice model for scoring. Since singers are discrete, a classifier is an appropriate tool for discerning between singers and selecting the appropriate model.

### Final Modified Goal
To design and implement a sort of vocal-controlled Temple Run–like game where the player's goal is to keep a circular sprite within an autoscrolling track by singing with varying pitch. The player is scored based on how well they keep the sprite within the track. Additionally, vertical-bar obstacles frequently appear and the player must "dodge" them by physically moving out of the webcam's view. We're excited about this final implementation because, for one, it works whereas the original idea did not. But moreover, it's fun to play! Singing and moving quickly are engaging activities, and because the game is trained to the player's vocal range, it feels personal. Regression is used to map the player's vocal range to the Y-axis position of the sprite, and classification is used to detect whether the player is in front of the webcam.

## Accomplishments:
We were not able to accomplish the original concept of our project, but we're proud of what we ended up making. The biggest reason our first idea did not work was that Wekinator does not allow multiple projects to listen to the same port; that would've been required to train multiple models on multiple voices and have them all responding to the same audio input. We explored the code behind our audio input program, Maximilian, but there is seemingly no place in the source code to change the OSC port it uses. Moving on to what does work, however, we're successfully extracting sung pitch from an audio input (using Maximillian's Const-Q analyser and Peak frequency), we're mapping that input to a value between 0 and 1 (with soft limits) using a neural net in Wekinator, and we're using that output in a totally custom-built Python program that is our game. Our biggest accomplishment by far was writing the Python code to create our game. We're also successfully using webcam input to detect if a player is in view. Our classification model is capable of detecting an arbitrarily large number of players, but for this game we only care if one player is in view. 

## Input Data:
There are 2 categories of input data: vocal data to create voice mapping models, and video data to use for singer identification.
The vocal data is input as unprocessed audio waves recorded by a microphone. Maximilian recieves the audio waves and outputs a combination of Const-Q analysis and Peak frequency of that wave, which effectively extracts pitch as 105 real-value inputs. The video data is input as a live feed from a webcam that is compressed to 1600 pixel values.

- Maximilian sends OSC messages Const-Q and Peak frequency (105 inputs) to Wekinator on port 6448
    - Wekinator sends output message “/wek/update” to port 12000
- Webcam sends OSC messages (1600 inputs) to Wekinator on port 6449
    - Wekinator sends output message “/wek/singer” to port 12000
- SingingGame.py listens on port 12000
    - “/wek/update” is a real value for regression
    - “/wek/singer” is an int value for classification



## Feature Engineering:
 - Audio processing with the Maximillian program (e.g., Constant Q analyser and Peak frequency)


## How to Use Our Project:
TBD

## Demo Video:
TBD
      
