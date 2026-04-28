# TCASL
*A lightweight classification application for learning American Sign Language.*

<img src="./images/tcasl.png" alt="TCASL Logo" width="25%">

## Table of Contents

1. [Background](#background)
3. [Getting Started](#getting-started)
    - [App (TCASLApp)](#app-tcaslapp)
    - [Pip Library (TCASLCore)](#pip-library-tcaslcore)
4. [Known Limitations](#known-limitations)

## Background

Millions of people around the world are deaf, and require the use of sign langauge to communicate. However, for those who do not know sign language, it can be difficult to understand what a person signing is saying. This challenge is especially prominent due to the fast nature of the signing gestures. To solve this, we mimic dynamic vision sensing (DVS) cameras, mimicing neuromorphic vision, only attending to movement (i.e., gestures). This makes our classification of ASL much more efficient, and even able to run on edge devices. This allows someone to easily use their laptop to capture a person signing letters in real-time, and provide a translation of what they are spelling.

## Getting Started

### App (TCASLApp)

This app provides an easy way for individuals to learn American Sign Language. It is in the style of Wordle, allowing you to spell words in 3 difficulty levels. It utilizes any webcam connected or on your laptop to capture real-time gestures by a user, and utilize such data to check if you are signing each letter correctly.

For detailed documentation, please refer to the [TCASLApp README](https://github.com/keshavshankar08/TCASL/blob/main/TCASLApp/README.md).


### Pip Library (TCASLCore)

This library provies an interface to easily take real-time or static frames from any laptop and webcame, then predict the ASL character being gestured.

For detailed documentation, please refer to the [TCASLCore README](https://github.com/keshavshankar08/TCASL/blob/main/TCASLCore/README.md).

## Known Limitations

- Lighting: 
  - Temporal Contrast emulation relies on intensity changes in pixels. Therefore, different lighting conditions will alter results.
