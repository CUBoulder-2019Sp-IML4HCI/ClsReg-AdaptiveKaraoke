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

## Analysis of model performance
TBD
_"4. An analysis of model performance, justifying your choices about model construction. Demonstrate quantitatively why the ML algorithm and parameters you used were the right ones. If you experimented with different options, provide and interpret data documenting the results of your experiments."_

## What We Learned
We learned a lot during the course of this project. We learned: 
 - How to extract pitch from an unprocessed audio wave using Const-Q analysis and Peak frequency
    - Peak frequency returns the one frequency which is most present in a wave
    - Const-Q analysis effectively bins the audio wave by bands/octaves, so by looking at which bins are "full" (and how "full" they are) one can approximate which musical notes are present in the wave
- How to use multiple inputs and multiple Wekinator projects to send inputs to the same output (by varying port/OSC message)
- How to classify people using simple Webcam input
- _How to create a game in Python!_
    - We wrote upwards of 200 lines of custom Python code to render all the graphics of our game and to smooth the jittery input provided by the vocal data. That was nothing short of a monumental marathon. 
    
We would have liked to learn how to implement our original idea. It was such a fascinating idea, and the killer of the idea seems to be Wekinator's limitations. We'd love to learn how to disable Wekinator's requirement that no two projects share the same input port. 

## Feature Engineering:
 - Audio processing with the Maximillian program (Constant-Q analyser and Peak frequency)
 - Value smoothing in Python
 
For feature engineering, we're extracting sung pitch from an audio input by use of Maximillian's Const-Q analyser and Peak frequency and then smoothing that input in Python. Peak frequency returns the one frequency which is most present in an audio wave, and Const-Q analysis effectively bins the wave by bands/octaves, so by looking at which bins are "full" (and how "full" they are) one can approximate which musical notes are present in the wave. Our Wekinator model performs regression on that input from Maximilian, sends the output of the regression to our Python game, and in the Python code we take the average of 20 pitch samples to compute the Y-axis position of the circular sprite.

## How to Use Our Project:
There are five main components to our project, each of which must be present for the game to work.
1. Maximilain. This is a C++ program available at http://www.wekinator.org/examples/#Audio (under the **Audio -> Various audio features** header)
2. The "simple webcam" with 1600 inputs. This is a Processing program that we have stored in the `SingerClassifier_1600Inputs` folder in this repo.
3. A Wekinator project with the following configurations:
 - 105 inputs 
 - listening for message "/wek/inputs" on port 6448
 - outputting 1 continuous output with the message "/wek/update" to port 12000
4. Another Wekinator project with the following configurations:
 - 1600 inputs
 - listening for message "/wek/inputs" on port 6449
 - outputing one classifier with at least 2 classes with the message "/wek/singer" to port 12000
5. The Python game (`SingingGame.py` in this repo).

Open and run Maximilian. Uncheck all boxes except for "Const-Q" and "Peak frequency". Open and run the simple webcam program. Create the two Wekinator projects as described above. Train the first Wekinator project with a neural network by following these steps:
 1. Manually set the slider to ~0.1
 2. Record a singer holding one "low" note
 3. Manually set the slider to ~0.9
 4. Record a singer holding one "high" note
 5. Train the model
 
Note that `SingGUI_InitialExperimentation` in this repo contains a Wekinator project which is correctly set up as just described. After that, train the second Wekinator project with the KNN algorithm by following these steps:
 1. Manually set the class to "1"
 2. Record some examples of just the background, i.e., without the singer in view
 3. Manually set the class to "2"
 4. Record some examples of the singer being in view
 5. Train the model
 
After all that, the inputs and Wekinator projects are ready to go. So run both Wekinator projects then run `SingingGame.py` (e.g. `python SingingGame.py`). The game starts. 
Sing higher notes to move the sprite upward, and sing lower notes to move the sprite downward. When vertical red bars appear, quickly move out of view to avoid penalties. 

## Demo Video:
TBD
      
